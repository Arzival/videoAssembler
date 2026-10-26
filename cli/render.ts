#!/usr/bin/env node
/**
 * Renderiza un manifiesto del Video Assembler con ffmpeg nativo.
 *
 *   node cli/render.ts manifiesto.json [--base <dir>] [--out <dir>] [--encoder maxima|videotoolbox|x264]
 *
 * --base    Carpeta raíz donde buscar los archivos del manifiesto (default: carpeta del manifiesto).
 *           Las rutas se resuelven directo contra --base; si no existen, se busca
 *           recursivamente por nombre de archivo.
 * --out     Carpeta de salida (default: carpeta actual).
 * --encoder default: maxima (x264 lento CRF 14 + AAC 320k: un solo archivo final para todas las redes). videotoolbox = rápido por
 *           hardware en macOS (pruebas); x264 = intermedio.
 * FFMPEG / FFPROBE: variables de entorno para rutas alternativas de los binarios.
 */
import { spawn, spawnSync } from 'node:child_process'
import { existsSync, mkdirSync, readdirSync, readFileSync, renameSync, statSync } from 'node:fs'
import { basename, dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import process from 'node:process'
import type { Manifest } from '../src/lib/types.ts'
import { buildArgs, inputFiles, outputDuration, outputFileName, type Encoder } from '../src/lib/graph.ts'

const FFMPEG = process.env.FFMPEG || 'ffmpeg'
const FFPROBE = process.env.FFPROBE || 'ffprobe'

function fail(msg: string): never {
  console.error(`✖ ${msg}`)
  process.exit(1)
}

// ---- argumentos ----
const argv = process.argv.slice(2)
let manifestPath = ''
let baseDir = ''
let outDir = process.cwd()
let encoder: Encoder = 'maxima'

for (let i = 0; i < argv.length; i++) {
  const a = argv[i]
  if (a === '--base') baseDir = argv[++i]
  else if (a === '--out') outDir = argv[++i]
  else if (a === '--encoder') {
    const e = argv[++i]
    if (e !== 'maxima' && e !== 'videotoolbox' && e !== 'x264') fail(`Encoder desconocido: ${e}`)
    encoder = e
  } else if (a === '--help' || a === '-h') {
    console.log('Uso: node cli/render.ts manifiesto.json [--base <dir>] [--out <dir>] [--encoder maxima|videotoolbox|x264]')
    process.exit(0)
  } else if (!manifestPath) manifestPath = a
  else fail(`Argumento inesperado: ${a}`)
}

if (!manifestPath) fail('Falta el manifiesto. Uso: node cli/render.ts manifiesto.json [--base <dir>]')
manifestPath = resolve(manifestPath)
if (!existsSync(manifestPath)) fail(`No existe: ${manifestPath}`)
if (!baseDir) baseDir = dirname(manifestPath)
baseDir = resolve(baseDir)
outDir = resolve(outDir)
mkdirSync(outDir, { recursive: true })

const manifest = JSON.parse(readFileSync(manifestPath, 'utf8')) as Manifest
if (!Array.isArray(manifest.clips) || manifest.clips.length === 0) fail('El manifiesto no tiene clips')
const outputs = manifest.outputs?.length ? manifest.outputs : ['vertical' as const]

// ---- resolución de archivos ----
function findByName(dir: string, name: string, hits: string[] = []): string[] {
  for (const entry of readdirSync(dir)) {
    if (entry.startsWith('.') || entry === 'node_modules') continue
    const full = join(dir, entry)
    const st = statSync(full)
    if (st.isDirectory()) findByName(full, name, hits)
    else if (entry === name) hits.push(full)
  }
  return hits
}

function resolveFile(ref: string): string {
  const direct = resolve(baseDir, ref)
  if (existsSync(direct)) return direct
  const hits = findByName(baseDir, basename(ref))
  if (hits.length === 0) fail(`No se encontró "${ref}" bajo ${baseDir}`)
  if (hits.length > 1) console.warn(`⚠ "${basename(ref)}" aparece ${hits.length} veces; usando ${hits[0]}`)
  return hits[0]
}

// escenas del motor que se revisaron en vivo pero aún no se graban: avisar claro en vez de «no se encontró»
const sinGrabar = (manifest.overlays ?? []).filter((o) => o.html && !existsSync(resolve(baseDir, o.file)) && findByName(baseDir, basename(o.file)).length === 0)
if (sinGrabar.length)
  fail(`Faltan grabar ${sinGrabar.length} escenas del motor (${sinGrabar.map((o) => basename(o.file)).join(', ')}).\n` +
    '  Corre: python3 cli/animaciones/motor/motor.py <guion.json> --capturar')

const refs = inputFiles(manifest)
const inputNames = refs.map(resolveFile)
console.log('Archivos:')
for (const p of inputNames) console.log(`  ${p}`)

// ---- ¿los clips con keepAudio tienen audio? ----
function hasAudioStream(file: string): boolean {
  const r = spawnSync(FFPROBE, ['-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index', '-of', 'csv=p=0', file], {
    encoding: 'utf8',
  })
  if (r.error || r.status !== 0) return true // sin ffprobe, asumimos que sí
  return r.stdout.trim().length > 0
}

const clipHasAudio = manifest.clips.map((c, i) => {
  if (!c.keepAudio) return true
  const ok = hasAudioStream(inputNames[i])
  if (!ok) console.warn(`⚠ ${c.file} no tiene audio; se usará silencio`)
  return ok
})

// ---- tomas HDR (HLG/PQ del iPhone) → SDR BT.709 con la LUT de cli/luts ----
const LUT_DIR = join(dirname(fileURLToPath(import.meta.url)), 'luts')
function hdrOf(file: string): 'hlg' | 'pq' | null {
  const r = spawnSync(FFPROBE, ['-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=color_transfer', '-of', 'csv=p=0', file], {
    encoding: 'utf8',
  })
  const trc = (r.stdout || '').split(/[,\n]/)[0].trim() // csv deja una coma final en tomas con side data (Dolby Vision)
  return trc === 'arib-std-b67' ? 'hlg' : trc === 'smpte2084' ? 'pq' : null
}
const clipHdr: Array<'hlg' | 'pq' | null> = manifest.clips.map((_, i) => hdrOf(inputNames[i]))
const nHdr = clipHdr.filter(Boolean).length
if (nHdr) {
  for (const k of ['hlg', 'pq'] as const)
    if (clipHdr.includes(k) && !existsSync(join(LUT_DIR, `${k}-a-bt709.cube`))) fail(`Falta cli/luts/${k}-a-bt709.cube (python3 cli/luts/generar.py)`)
  console.log(`HDR → SDR: ${nHdr} de ${clipHdr.length} clips (LUT de cli/luts)`)
  await preconvertirHdr()
}

/**
 * La conversión HDR (escalar 4K 10 bits + LUT) corre en un solo hilo dentro del render (~25 cps). Para no tardar 15× la
 * duración del video, cada tramo HDR usado se convierte antes, varios a la vez y con decodificación por hardware, a un
 * intermedio SDR de alta calidad (x264 crf 10) en <out>/.hdr-cache; el render usa ese intermedio (ya SDR) y va normal.
 */
function primerCuadro(file: string, desde: number): number {
  const p = (args: string[]) => spawnSync(FFPROBE, ['-v', 'error', '-select_streams', 'v:0', ...args, '-of', 'csv=p=0', file], { encoding: 'utf8' }).stdout
  const t0 = Number.parseFloat(p(['-show_entries', 'stream=start_time'])) || 0
  const ts = p(['-read_intervals', `${(desde + t0).toFixed(3)}%+0.3`, '-show_entries', 'frame=best_effort_timestamp_time'])
    .split('\n').map((x) => Number.parseFloat(x)).filter((x) => Number.isFinite(x)).map((x) => x - t0).sort((a, b) => a - b)
  return ts.find((x) => x >= desde - 1e-4) ?? desde
}

async function preconvertirHdr() {
  const fmt0 = outputs[0] === 'horizontal' ? [1920, 1080] : [1080, 1920]
  const cache = join(outDir, '.hdr-cache')
  mkdirSync(cache, { recursive: true })
  const trabajos: Array<() => Promise<void>> = []
  manifest.clips.forEach((c, i) => {
    const hdr = clipHdr[i]
    if (!hdr) return
    const desde = Math.max(0, c.trimIn - 0.5)
    const hasta = c.trimOut + 0.5
    const destino = join(cache, `${basename(inputNames[i]).replace(/\.[^.]+$/, '')}-${desde.toFixed(3)}-${hasta.toFixed(3)}-${fmt0[0]}x${fmt0[1]}.mp4`)
    const usar = () => {
      // el intermedio empieza en el primer cuadro de la toma que cae en `desde` o después (rejilla de 59.94): se mide
      // para no correr el video un cuadro respecto a la voz
      const f0 = primerCuadro(inputNames[i], desde)
      inputNames[i] = destino
      clipHdr[i] = null
      manifest.clips[i] = {
        ...c,
        trimIn: c.trimIn - f0,
        trimOut: c.trimOut - f0,
        cuts: c.cuts?.map((k) => ({ from: k.from - f0, to: k.to - f0 })),
      }
    }
    if (existsSync(destino) && statSync(destino).mtimeMs > statSync(inputNames[i]).mtimeMs) return usar()
    const vf =
      `scale=${fmt0[0]}:${fmt0[1]}:force_original_aspect_ratio=increase:in_color_matrix=bt2020:in_range=tv:out_range=pc,format=gbrp16le,` +
      `lut3d=file='${LUT_DIR}/${hdr}-a-bt709.cube':interp=tetrahedral,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,` +
      `setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv`
    const args = ['-v', 'error', '-y', '-hwaccel', 'videotoolbox', '-ss', desde.toFixed(3), '-to', hasta.toFixed(3), '-i', inputNames[i],
      '-vf', vf, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '10', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709',
      '-color_trc', 'bt709', '-colorspace', 'bt709', '-c:a', 'copy', destino + '.tmp.mp4']
    trabajos.push(
      () =>
        new Promise((ok, mal) => {
          const p = spawn(FFMPEG, args, { stdio: ['ignore', 'ignore', 'pipe'] })
          let err = ''
          p.stderr.on('data', (d) => (err = (err + d).slice(-2000)))
          p.on('close', (code) => {
            if (code !== 0) return mal(new Error(`conversión HDR de ${c.file} falló:\n${err}`))
            renameSync(destino + '.tmp.mp4', destino)
            usar()
            ok()
          })
        }),
    )
  })
  if (!trabajos.length) return
  const t0 = Date.now()
  const N = Math.min(6, trabajos.length)
  let k = 0
  await Promise.all(Array.from({ length: N }, async () => { while (k < trabajos.length) await trabajos[k++]() }))
  console.log(`  ${trabajos.length} tramos HDR convertidos en ${((Date.now() - t0) / 1000).toFixed(0)}s (${N} a la vez)`)
}

// ---- render ----
const totalDur = outputDuration(manifest)

function render(format: (typeof outputs)[number]): Promise<string> {
  const outPath = join(outDir, outputFileName(manifest, format))
  const args = buildArgs(manifest, { format, encoder, inputNames, clipHasAudio, clipHdr, lutDir: LUT_DIR, outputName: outPath })
  args.push('-progress', 'pipe:1', '-nostats')

  return new Promise((resolvePromise, reject) => {
    console.log(`\n▶ Renderizando ${format} → ${outPath}`)
    const proc = spawn(FFMPEG, args, { stdio: ['ignore', 'pipe', 'pipe'] })
    let stderrTail = ''

    proc.stdout.setEncoding('utf8')
    proc.stdout.on('data', (chunk: string) => {
      const m = /out_time_us=(\d+)/.exec(chunk)
      if (m) {
        const pct = Math.min(100, (Number(m[1]) / 1e6 / totalDur) * 100)
        process.stdout.write(`\r  ${pct.toFixed(1)}%   `)
      }
    })
    proc.stderr.setEncoding('utf8')
    proc.stderr.on('data', (chunk: string) => {
      stderrTail = (stderrTail + chunk).slice(-4000)
    })
    proc.on('error', (err) => reject(new Error(`No se pudo ejecutar ${FFMPEG}: ${err.message}`)))
    proc.on('close', (code) => {
      process.stdout.write('\r  100.0%   \n')
      if (code === 0) resolvePromise(outPath)
      else reject(new Error(`ffmpeg falló (código ${code}):\n${stderrTail}`))
    })
  })
}

const started = Date.now()
try {
  const results: string[] = []
  for (const format of outputs) {
    results.push(await render(format))
  }
  const secs = ((Date.now() - started) / 1000).toFixed(1)
  console.log(`\n✔ Listo en ${secs}s (duración del video: ${totalDur.toFixed(1)}s)`)
  for (const r of results) console.log(`  ${r}`)
} catch (err) {
  fail(err instanceof Error ? err.message : String(err))
}
