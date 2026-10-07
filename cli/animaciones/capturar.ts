#!/usr/bin/env node
/**
 * (Opcional) Convierte un HTML animado en un clip WebM VP9 con transparencia,
 * listo para usarse como capa (overlays) a pantalla completa en el manifiesto.
 *
 *   node cli/animaciones/capturar.ts animacion.html 6.5 salida.webm [--formato vertical|horizontal]
 *
 * La animación se congela cuadro por cuadro (CSS vía document.getAnimations() y, si
 * existe, window.__seek(segundos) para contadores en JS), así que sale fluida sin
 * importar la velocidad de la máquina. Fondo transparente salvo que el HTML pinte uno.
 */
import { chromium } from 'playwright-core'
import { spawnSync } from 'node:child_process'
import { existsSync, mkdtempSync, readdirSync, rmSync } from 'node:fs'
import { homedir, tmpdir } from 'node:os'
import { join, resolve } from 'node:path'
import { pathToFileURL } from 'node:url'
import process from 'node:process'

const FPS = 30

function fail(msg: string): never {
  console.error(`✖ ${msg}`)
  process.exit(1)
}

function findChromium(): string {
  if (process.env.CHROME_PATH && existsSync(process.env.CHROME_PATH)) return process.env.CHROME_PATH
  const cache = join(homedir(), 'Library/Caches/ms-playwright')
  if (existsSync(cache)) {
    for (const dir of readdirSync(cache).filter((d) => d.startsWith('chromium')).sort().reverse()) {
      const p = join(cache, dir, 'chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing')
      if (existsSync(p)) return p
    }
  }
  for (const p of ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Chromium.app/Contents/MacOS/Chromium']) {
    if (existsSync(p)) return p
  }
  fail('No se encontró un Chromium. Instala Google Chrome o define CHROME_PATH.')
}

const args = process.argv.slice(2)
const fi = args.indexOf('--formato')
const formato = fi >= 0 ? args.splice(fi, 2)[1] : 'vertical'
const [html, durS, outArg] = args
if (!html || !durS || !outArg) fail('Uso: node cli/animaciones/capturar.ts animacion.html <segundos> salida.webm [--formato vertical|horizontal]')
if (!existsSync(html)) fail(`No existe: ${html}`)
const dur = Number(durS)
if (!(dur > 0)) fail('La duración debe ser mayor a 0')
const [W, H] = formato === 'horizontal' ? [1920, 1080] : [1080, 1920]
const out = resolve(outArg)

const tmp = mkdtempSync(join(tmpdir(), 'capturar-'))
const browser = await chromium.launch({ executablePath: findChromium(), headless: true })
try {
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 })
  // 'load' ya espera la hoja de Google Fonts; networkidle a veces se cuelga y tumbaba capturas
  for (let intento = 1; ; intento++) {
    try {
      await page.goto(pathToFileURL(resolve(html)).href, { waitUntil: 'load', timeout: 60000 })
      break
    } catch (err) {
      if (intento >= 3) throw err
    }
  }
  await page.evaluate(() => document.fonts.ready)
  const frames = Math.round(dur * FPS)
  for (let f = 0; f < frames; f++) {
    await page.evaluate((ms) => {
      for (const a of document.getAnimations()) {
        a.pause()
        a.currentTime = ms
      }
      const w = window as unknown as { __seek?: (s: number) => void }
      w.__seek?.(ms / 1000)
    }, (f / FPS) * 1000)
    await page.screenshot({ path: join(tmp, `f${String(f).padStart(5, '0')}.png`), omitBackground: true })
  }
} finally {
  await browser.close()
}
const r = spawnSync(process.env.FFMPEG || 'ffmpeg', ['-v', 'error', '-y', '-framerate', String(FPS), '-i', join(tmp, 'f%05d.png'),
  '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-b:v', '0', '-crf', '28', '-row-mt', '1', '-auto-alt-ref', '0', out], { encoding: 'utf8' })
rmSync(tmp, { recursive: true, force: true })
if (r.status !== 0) fail(`ffmpeg falló:\n${r.stderr}`)
console.log(`✔ ${out}`)
