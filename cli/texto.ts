#!/usr/bin/env node
/**
 * (Opcional) Genera un clip de TEXTO ANIMADO con fondo transparente, listo para
 * ponerse encima del video como capa (overlays) a pantalla completa.
 *
 *   node cli/texto.ts --texto "Hola" [--estilo rebote|deslizar|maquina|resaltar|subtitulo]
 *                     [--resalta "palabra"] [--duracion 3] [--formato vertical|horizontal]
 *                     [--out titulo.webm]
 *
 * El texto se diseña en HTML/CSS y se captura cuadro por cuadro en un Chromium
 * controlado: la animación se congela en cada cuadro exacto, así que sale fluida
 * aunque la máquina vaya lenta. Salida: WebM VP9 con canal alfa (ligero, se ve en la
 * web y el render lo decodifica con libvpx-vp9 conservando la transparencia).
 */
import { chromium } from 'playwright-core'
import { spawnSync } from 'node:child_process'
import { existsSync, mkdtempSync, readdirSync, rmSync } from 'node:fs'
import { homedir, tmpdir } from 'node:os'
import { join, resolve } from 'node:path'
import process from 'node:process'

const FFMPEG = process.env.FFMPEG || 'ffmpeg'
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

const opts: Record<string, string> = { estilo: 'rebote', duracion: '3', formato: 'vertical' }
const argv = process.argv.slice(2)
for (let i = 0; i < argv.length; i++) {
  const a = argv[i]
  if (a === '--help' || a === '-h') {
    console.log('Uso: node cli/texto.ts --texto "Hola" [--estilo rebote|deslizar|maquina|resaltar|subtitulo] [--resalta palabra] [--duracion 3] [--formato vertical|horizontal] [--out x.webm]')
    process.exit(0)
  }
  if (!a.startsWith('--')) fail(`Argumento inesperado: ${a}`)
  opts[a.slice(2)] = argv[++i] ?? ''
}
const texto = opts.texto
if (!texto) fail('Falta --texto')
const dur = Number(opts.duracion)
if (!(dur > 0.5)) fail('--duracion debe ser mayor a 0.5 segundos')
const [W, H] = opts.formato === 'horizontal' ? [1920, 1080] : [1080, 1920]
const out = resolve(opts.out || `texto-${Date.now()}.webm`)

const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
const OUT_MS = 350 // salida al final de cada estilo
const outDelay = Math.max(0, dur * 1000 - OUT_MS)

// Cada estilo: html del bloque + css. Todas las animaciones son CSS para poder
// congelarlas por cuadro con document.getAnimations().
function estilo(): { html: string; css: string } {
  const t = esc(texto)
  const base = `
    .wrap{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding:0 7%}
    .txt{font:900 ${opts.formato === 'horizontal' ? 104 : 96}px/1.12 -apple-system,'SF Pro Display','Segoe UI',system-ui,sans-serif;
      color:#fff;text-align:center;letter-spacing:-.01em;
      text-shadow:0 6px 24px rgba(0,0,0,.55),0 2px 4px rgba(0,0,0,.6)}
    .salida{animation:salida ${OUT_MS}ms ease-in ${outDelay}ms forwards}
    @keyframes salida{to{opacity:0;transform:scale(.92)}}`
  switch (opts.estilo) {
    case 'deslizar':
      return {
        html: `<div class="wrap salida"><div class="txt desl">${t}</div></div>`,
        css: `${base}
          .desl{animation:entra .55s cubic-bezier(.2,.9,.25,1) both}
          @keyframes entra{from{opacity:0;transform:translateX(-120px)}to{opacity:1;transform:none}}`,
      }
    case 'maquina': {
      const n = texto.length
      return {
        html: `<div class="wrap salida"><div class="txt maq">${t}</div></div>`,
        css: `${base}
          .maq{white-space:nowrap;overflow:hidden;border-right:.07em solid #fff;width:0;
            animation:escribe ${Math.min(dur * 0.6, n * 0.06)}s steps(${n}) .1s forwards,cursor .7s step-end infinite}
          @keyframes escribe{to{width:${n}ch}}
          @keyframes cursor{50%{border-color:transparent}}
          .maq{font-family:ui-monospace,'SF Mono',Menlo,monospace;font-size:${opts.formato === 'horizontal' ? 84 : 72}px}`,
      }
    }
    case 'resaltar': {
      const palabra = opts.resalta ? esc(opts.resalta) : ''
      const marcado = palabra && t.includes(palabra) ? t.replace(palabra, `<span class="hl">${palabra}</span>`) : `<span class="hl">${t}</span>`
      return {
        html: `<div class="wrap salida"><div class="txt res">${marcado}</div></div>`,
        css: `${base}
          .res{animation:aparece .4s ease-out both}
          @keyframes aparece{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:none}}
          .hl{position:relative;display:inline-block;padding:0 .12em;z-index:0;color:#111;text-shadow:none}
          .hl::before{content:'';position:absolute;left:0;right:0;top:.06em;bottom:.04em;z-index:-1;border-radius:.12em;
            background:#f5c518;transform:scaleX(0);transform-origin:left;animation:marca .45s ease-out .45s forwards}
          @keyframes marca{to{transform:scaleX(1)}}`,
      }
    }
    case 'subtitulo':
      return {
        html: `<div class="wrap salida sub"><div class="txt cap">${t}</div></div>`,
        css: `${base}
          .sub{align-items:flex-end;padding-bottom:${opts.formato === 'horizontal' ? 8 : 18}%}
          .cap{font-size:${opts.formato === 'horizontal' ? 64 : 60}px;font-weight:800;background:rgba(0,0,0,.62);
            border-radius:18px;padding:.35em .6em;text-shadow:none;animation:sube .35s ease-out both}
          @keyframes sube{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:none}}`,
      }
    case 'rebote':
    default:
      return {
        html: `<div class="wrap salida"><div class="txt reb">${t}</div></div>`,
        css: `${base}
          .reb{animation:pop .6s cubic-bezier(.34,1.56,.64,1) both}
          @keyframes pop{0%{opacity:0;transform:scale(.4)}100%{opacity:1;transform:scale(1)}}`,
      }
  }
}

const { html, css } = estilo()
const page = `<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:${W}px;height:${H}px;background:transparent;overflow:hidden}
${css}</style></head><body>${html}</body></html>`

const tmp = mkdtempSync(join(tmpdir(), 'texto-'))
const browser = await chromium.launch({ executablePath: findChromium(), headless: true })
try {
  const p = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 })
  await p.setContent(page, { waitUntil: 'load' })
  await p.evaluate(() => document.fonts.ready)
  const frames = Math.round(dur * FPS)
  console.log(`estilo «${opts.estilo}» · ${W}×${H} · ${dur}s → ${frames} cuadros`)
  for (let f = 0; f < frames; f++) {
    const ms = (f / FPS) * 1000
    await p.evaluate((t) => {
      for (const a of document.getAnimations()) {
        a.pause()
        a.currentTime = t
      }
    }, ms)
    await p.screenshot({ path: join(tmp, `f${String(f).padStart(5, '0')}.png`), omitBackground: true })
  }
} finally {
  await browser.close()
}

const r = spawnSync(FFMPEG, ['-v', 'error', '-y', '-framerate', String(FPS), '-i', join(tmp, 'f%05d.png'),
  '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-b:v', '0', '-crf', '30', '-row-mt', '1', '-auto-alt-ref', '0', out], { encoding: 'utf8' })
rmSync(tmp, { recursive: true, force: true })
if (r.status !== 0) fail(`ffmpeg falló:\n${r.stderr}`)
console.log(`✔ ${out}`)
