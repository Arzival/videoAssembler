#!/usr/bin/env node
/**
 * (Opcional) Convierte una animación HTML exportada por TextDecoration en un
 * clip MP4 listo para el manifiesto — la «grabación de pantalla» pero automática:
 * abre el HTML en un Chromium controlado, graba la animación completa y la
 * transcodifica a H.264.
 *
 *   node cli/textclip.ts animacion.html [--out clip.mp4]
 *
 * Requiere un navegador Chromium instalado. Se busca en este orden:
 *   $CHROME_PATH → caché de Playwright → Google Chrome → Chromium.
 * La duración se lee del propio HTML (TOTAL_MS) y el tamaño del elemento .stage.
 */
import { chromium } from 'playwright-core'
import { spawnSync } from 'node:child_process'
import { existsSync, readdirSync, rmSync } from 'node:fs'
import { homedir } from 'node:os'
import { join, resolve } from 'node:path'
import { pathToFileURL } from 'node:url'
import process from 'node:process'

const FFMPEG = process.env.FFMPEG || 'ffmpeg'

function fail(msg: string): never {
  console.error(`✖ ${msg}`)
  process.exit(1)
}

function findChromium(): string {
  if (process.env.CHROME_PATH && existsSync(process.env.CHROME_PATH)) return process.env.CHROME_PATH
  const cache = join(homedir(), 'Library/Caches/ms-playwright')
  if (existsSync(cache)) {
    for (const dir of readdirSync(cache).filter((d) => d.startsWith('chromium')).sort().reverse()) {
      for (const app of ['chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing', 'chrome-mac/Chromium.app/Contents/MacOS/Chromium']) {
        const p = join(cache, dir, app)
        if (existsSync(p)) return p
      }
    }
  }
  for (const p of [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
  ]) {
    if (existsSync(p)) return p
  }
  fail('No se encontró un Chromium. Instala Google Chrome o define CHROME_PATH.')
}

const argv = process.argv.slice(2)
let input = ''
let output = ''
for (let i = 0; i < argv.length; i++) {
  const a = argv[i]
  if (a === '--out') output = argv[++i]
  else if (a === '--help' || a === '-h') {
    console.log('Uso: node cli/textclip.ts animacion.html [--out clip.mp4]')
    process.exit(0)
  } else if (!input) input = a
  else fail(`Argumento inesperado: ${a}`)
}
if (!input) fail('Falta el HTML. Uso: node cli/textclip.ts animacion.html')
input = resolve(input)
if (!existsSync(input)) fail(`No existe: ${input}`)
if (!output) output = input.replace(/\.html?$/i, '') + '.mp4'
output = resolve(output)

const url = pathToFileURL(input).href
const exe = findChromium()
const browser = await chromium.launch({ executablePath: exe, headless: true })

// pasada 1: medir el escenario y la duración de la animación
const probe = await browser.newPage({ viewport: { width: 2400, height: 2400 } })
await probe.goto(url, { waitUntil: 'load' })
const info = await probe.evaluate(() => {
  const stage = document.querySelector('.stage') as HTMLElement | null
  // TOTAL_MS es una const de ámbito global del script exportado (no cuelga de globalThis)
  let total: number | null = null
  try {
    // eslint-disable-next-line no-eval
    const v = eval('TOTAL_MS')
    if (typeof v === 'number') total = v
  } catch {
    total = null
  }
  return {
    w: stage?.offsetWidth ?? 1080,
    h: stage?.offsetHeight ?? 1920,
    totalMs: total,
  }
})
await probe.close()
if (!info.totalMs) fail('El HTML no parece una exportación de TextDecoration (no se encontró TOTAL_MS)')
console.log(`escenario ${info.w}×${info.h} · animación de ${(info.totalMs / 1000).toFixed(1)}s — grabando en tiempo real…`)

// pasada 2: grabar la animación completa
const ctx = await browser.newContext({
  viewport: { width: info.w, height: info.h },
  recordVideo: { dir: join(process.cwd(), '.textclip-tmp'), size: { width: info.w, height: info.h } },
})
const page = await ctx.newPage()
await page.goto(url, { waitUntil: 'load' })
await page.waitForTimeout(info.totalMs + 600)
const video = page.video()
await ctx.close()
const webm = video ? await video.path() : null
await browser.close()
if (!webm || !existsSync(webm)) fail('La grabación no se generó')

// transcodificar a H.264 (el render del manifiesto normaliza fps después)
const r = spawnSync(FFMPEG, ['-v', 'error', '-y', '-i', webm, '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an', output], { encoding: 'utf8' })
rmSync(join(process.cwd(), '.textclip-tmp'), { recursive: true, force: true })
if (r.status !== 0) fail(`ffmpeg falló:\n${r.stderr}`)

const dur = spawnSync(process.env.FFPROBE || 'ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', output], { encoding: 'utf8' }).stdout.trim()
console.log(`✔ clip de ${Number(dur).toFixed(1)}s (incluye ~2s de espera inicial de la animación — recórtala con trimIn)`)
console.log(`  ${output}`)
