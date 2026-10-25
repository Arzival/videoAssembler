#!/usr/bin/env node
/**
 * (Opcional) Convierte un HTML animado en un clip WebM VP9 con transparencia,
 * listo para usarse como capa (overlays) a pantalla completa en el manifiesto.
 *
 *   node cli/animaciones/capturar.ts animacion.html 6.5 salida.webm [--formato vertical|horizontal]
 *   node cli/animaciones/capturar.ts --lote piezas.json        (lista [{html, dur, out, formato?}] con un solo navegador)
 *
 * La animación se congela cuadro por cuadro (CSS vía document.getAnimations() y, si
 * existe, window.__seek(segundos) para contadores en JS), así que sale fluida sin
 * importar la velocidad de la máquina. Fondo transparente salvo que el HTML pinte uno.
 *
 * Velocidad (sin tocar los ajustes del VP9):
 *  - Los PNG van directo a ffmpeg por tubería mientras se captura (la compresión ya no espera al final).
 *  - Si la página declara window.__cps (estilos que se mueven a pasos, p. ej. 12 cps), los cuadros del mismo paso
 *    son idénticos y se repite el PNG anterior en vez de volver a capturar. window.__liso = [[a, b], …] marca tramos
 *    (segundos locales) que van lisos a propósito y se capturan cuadro por cuadro.
 *  - Si la pieza no cambió (mismo HTML, duración y formato), se reusa el .webm anterior (huella en <salida>.huella).
 *    NO_CACHE=1 obliga a regrabar.
 */
import { chromium, type Browser } from 'playwright-core'
import { spawn } from 'node:child_process'
import { createHash } from 'node:crypto'
import { existsSync, readFileSync, readdirSync, renameSync, rmSync, writeFileSync } from 'node:fs'
import { homedir } from 'node:os'
import { join, resolve } from 'node:path'
import { once } from 'node:events'
import { pathToFileURL } from 'node:url'
import process from 'node:process'

const FPS = 30
const VERSION = 'capturar-2' // cambia la huella si cambia la forma de capturar
const VP9 = ['-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-b:v', '0', '-crf', '28', '-row-mt', '1', '-auto-alt-ref', '0']

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

interface Pieza {
  html: string
  dur: number
  out: string
  formato?: string
}

function huella(p: Pieza): string {
  return createHash('sha1').update(`${VERSION}\n${p.dur}\n${p.formato ?? 'vertical'}\n`).update(readFileSync(p.html)).digest('hex')
}

async function capturar(browser: Browser, p: Pieza): Promise<string> {
  const out = resolve(p.out)
  const marca = `${out}.huella`
  const h = huella(p)
  if (!process.env.NO_CACHE && existsSync(out) && existsSync(marca) && readFileSync(marca, 'utf8').trim() === h) return `= ${out} (sin cambios, se reusa)`
  const [W, H] = p.formato === 'horizontal' ? [1920, 1080] : [1080, 1920]
  const tmpOut = `${out}.tmp.webm`
  const ff = spawn(process.env.FFMPEG || 'ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-', ...VP9, tmpOut], {
    stdio: ['pipe', 'ignore', 'pipe'],
  })
  let ffErr = ''
  ff.stderr.on('data', (d) => (ffErr = (ffErr + d).slice(-3000)))
  const cerrado = once(ff, 'close')
  const emitir = async (png: Buffer) => {
    if (!ff.stdin.write(png)) await Promise.race([once(ff.stdin, 'drain'), cerrado])
  }
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 })
  let capturados = 0
  const frames = Math.round(p.dur * FPS)
  try {
    // 'load' ya espera la hoja de Google Fonts; networkidle a veces se cuelga y tumbaba capturas
    for (let intento = 1; ; intento++) {
      try {
        await page.goto(pathToFileURL(resolve(p.html)).href, { waitUntil: 'load', timeout: 60000 })
        break
      } catch (err) {
        if (intento >= 3) throw err
      }
    }
    await page.evaluate(() => document.fonts.ready)
    // escenas con capa 3D (three.js): esperan a que carguen modelos/fuentes antes del primer cuadro
    await page.evaluate(() => (window as unknown as { __listo?: Promise<void> }).__listo)
    const { cps, liso } = await page.evaluate(() => {
      const w = window as unknown as { __cps?: number; __liso?: [number, number][] }
      return { cps: Number(w.__cps) || 0, liso: Array.isArray(w.__liso) ? w.__liso : [] }
    })
    // captura directa por CDP: page.screenshot() re-aplica el fondo transparente y espera a que la página «se asiente» en cada
    // cuadro (~2.5 s/cuadro con 3D y desenfoques); Page.captureScreenshot con optimizeForSpeed tarda ~0.3 s y da el mismo PNG
    const cdp = await page.context().newCDPSession(page)
    await cdp.send('Emulation.setDefaultBackgroundColorOverride', { color: { r: 0, g: 0, b: 0, a: 0 } })
    let prevKey = ''
    let prev: Buffer | null = null
    for (let f = 0; f < frames; f++) {
      const s = f / FPS
      const enLiso = liso.some(([a, b]) => s >= a - 1e-6 && s < b)
      const key = cps > 0 && !enLiso ? `p${Math.floor(s * cps + 1e-6)}` : `f${f}`
      if (prev && key === prevKey) {
        await emitir(prev)
        continue
      }
      await page.evaluate((ms) => {
        for (const a of document.getAnimations()) {
          a.pause()
          a.currentTime = ms
        }
        const w = window as unknown as { __seek?: (s: number) => void }
        w.__seek?.(ms / 1000)
      }, s * 1000)
      const shot = (await cdp.send('Page.captureScreenshot', { format: 'png', optimizeForSpeed: true, captureBeyondViewport: false } as never)) as { data: string }
      prev = Buffer.from(shot.data, 'base64')
      prevKey = key
      capturados++
      await emitir(prev)
    }
  } catch (err) {
    ff.kill('SIGKILL')
    rmSync(tmpOut, { force: true })
    throw err
  } finally {
    await page.close()
  }
  ff.stdin.end()
  const [code] = (await cerrado) as [number]
  if (code !== 0) {
    rmSync(tmpOut, { force: true })
    throw new Error(`ffmpeg falló:\n${ffErr}`)
  }
  renameSync(tmpOut, out)
  writeFileSync(marca, h + '\n')
  return `✔ ${out}` + (capturados < frames ? ` (${capturados}/${frames} cuadros capturados; el resto eran pasos repetidos)` : '')
}

const args = process.argv.slice(2)
let piezas: Pieza[]
const li = args.indexOf('--lote')
if (li >= 0) {
  piezas = JSON.parse(readFileSync(args[li + 1], 'utf8')) as Pieza[]
} else {
  const fi = args.indexOf('--formato')
  const formato = fi >= 0 ? args.splice(fi, 2)[1] : 'vertical'
  const [html, durS, outArg] = args
  if (!html || !durS || !outArg) fail('Uso: node cli/animaciones/capturar.ts animacion.html <segundos> salida.webm [--formato vertical|horizontal]')
  piezas = [{ html, dur: Number(durS), out: outArg, formato }]
}
for (const p of piezas) {
  if (!existsSync(p.html)) fail(`No existe: ${p.html}`)
  if (!(p.dur > 0)) fail(`La duración debe ser mayor a 0 (${p.html})`)
}

const browser = await chromium.launch({ executablePath: findChromium(), headless: true })
let fallas = 0
try {
  for (const p of piezas) {
    try {
      console.log(await capturar(browser, p))
    } catch (err) {
      fallas++
      console.error(`✖ ${p.html}: ${err instanceof Error ? err.message : err}`)
    }
  }
} finally {
  await browser.close()
}
if (fallas) process.exit(1)
