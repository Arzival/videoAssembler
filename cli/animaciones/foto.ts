#!/usr/bin/env node
/**
 * Foto fija de una página HTML (1080×1920) en el segundo t, con el mismo contrato que capturar.ts (__listo, __seek).
 *   node cli/animaciones/foto.ts pagina.html salida.png [t=0] [--transparente]
 */
import { chromium } from 'playwright-core'
import { existsSync, readdirSync } from 'node:fs'
import { homedir } from 'node:os'
import { join, resolve } from 'node:path'
import { pathToFileURL } from 'node:url'
import process from 'node:process'

const args = process.argv.slice(2)
const transp = args.includes('--transparente')
const [html, out, tS] = args.filter((a) => a !== '--transparente')
if (!html || !out || !existsSync(html)) {
  console.error('Uso: node cli/animaciones/foto.ts pagina.html salida.png [t] [--transparente]')
  process.exit(1)
}
let exe = process.env.CHROME_PATH ?? ''
const cache = join(homedir(), 'Library/Caches/ms-playwright')
if (!exe && existsSync(cache))
  for (const d of readdirSync(cache).filter((d) => d.startsWith('chromium')).sort().reverse()) {
    const p = join(cache, d, 'chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing')
    if (existsSync(p)) {
      exe = p
      break
    }
  }
const b = await chromium.launch({ executablePath: exe || undefined, headless: true })
try {
  const page = await b.newPage({ viewport: { width: 1080, height: 1920 } })
  await page.goto(pathToFileURL(resolve(html)).href, { waitUntil: 'load', timeout: 60000 })
  await page.evaluate(() => document.fonts.ready)
  await page.evaluate(() => (window as unknown as { __listo?: Promise<void> }).__listo)
  await page.evaluate((ms) => {
    for (const a of document.getAnimations()) {
      a.pause()
      a.currentTime = ms
    }
    ;(window as unknown as { __seek?: (s: number) => void }).__seek?.(ms / 1000)
  }, Number(tS || 0) * 1000)
  await page.screenshot({ path: resolve(out), omitBackground: transp })
  console.log(`✔ ${resolve(out)}`)
} finally {
  await b.close()
}
