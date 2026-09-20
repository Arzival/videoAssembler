#!/usr/bin/env node
/**
 * (Opcional) Limpia el audio de un clip grabado con el celular: elimina ruido de
 * fondo y reverberación con DeepFilterNet (red neuronal local) y normaliza la voz.
 * El video se conserva; opcionalmente recorta el inicio sin voz.
 *
 *   node cli/limpiar-audio.ts clip.MOV [--out salida.MOV] [--recortar-inicio]
 *
 * - Con video y sin recorte: el stream de video se COPIA (sin recompresión).
 * - Con --recortar-inicio: detecta dónde arranca la voz (sobre el audio ya limpio),
 *   recorta desde 0.25s antes y re-encodea el video (VideoToolbox).
 * - Acepta también archivos de solo audio (wav/mp3/m4a).
 *
 * Requiere el binario `deep-filter` (descarga única, nativo, sin dependencias):
 *   https://github.com/Rikorose/DeepFilterNet/releases → deep-filter-*-aarch64-apple-darwin
 *   → guárdalo como ~/.local/bin/deep-filter y dale chmod +x (o define DEEP_FILTER).
 */
import { spawnSync } from 'node:child_process'
import { existsSync, mkdirSync, mkdtempSync, rmSync } from 'node:fs'
import { homedir, tmpdir } from 'node:os'
import { basename, join, resolve } from 'node:path'
import process from 'node:process'

const FFMPEG = process.env.FFMPEG || 'ffmpeg'
const FFPROBE = process.env.FFPROBE || 'ffprobe'
const SPEECHNORM = 'speechnorm=e=6.25:r=0.00001:l=1'
const PAD = 0.25 // colchón antes de la primera palabra al recortar el inicio

function fail(msg: string): never {
  console.error(`✖ ${msg}`)
  process.exit(1)
}

function findDeepFilter(): string {
  const candidates = [process.env.DEEP_FILTER, join(homedir(), '.local/bin/deep-filter'), 'deep-filter']
  for (const c of candidates) {
    if (!c) continue
    const r = spawnSync(c, ['--version'], { encoding: 'utf8' })
    if (r.status === 0) return c
  }
  fail(
    'No se encontró deep-filter. Descarga el binario para tu plataforma de\n' +
      '  https://github.com/Rikorose/DeepFilterNet/releases\n' +
      '  y guárdalo como ~/.local/bin/deep-filter (chmod +x), o define DEEP_FILTER.',
  )
}

const argv = process.argv.slice(2)
let input = ''
let output = ''
let trimStart = false
for (let i = 0; i < argv.length; i++) {
  const a = argv[i]
  if (a === '--out') output = argv[++i]
  else if (a === '--recortar-inicio') trimStart = true
  else if (a === '--help' || a === '-h') {
    console.log('Uso: node cli/limpiar-audio.ts clip.MOV [--out salida.MOV] [--recortar-inicio]')
    process.exit(0)
  } else if (!input) input = a
  else fail(`Argumento inesperado: ${a}`)
}
if (!input) fail('Falta el archivo. Uso: node cli/limpiar-audio.ts clip.MOV [--recortar-inicio]')
input = resolve(input)
if (!existsSync(input)) fail(`No existe: ${input}`)

// ffprobe con -of csv puede agregar coma final ("video,") — se limpia aquí
const probe = (args: string[]) =>
  spawnSync(FFPROBE, ['-v', 'error', ...args, input], { encoding: 'utf8' }).stdout.trim().replace(/,+$/, '')
const hasVideo = probe(['-select_streams', 'v:0', '-show_entries', 'stream=codec_type', '-of', 'csv=p=0']) === 'video'
const height = Number(probe(['-select_streams', 'v:0', '-show_entries', 'stream=height', '-of', 'csv=p=0'])) || 0
const durIn = Number(probe(['-show_entries', 'format=duration', '-of', 'csv=p=0'])) || 0

if (!output) {
  output = hasVideo ? input.replace(/(\.[^.]+)$/, '-limpio$1') : input.replace(/(\.[^.]+)$/, '-limpio.wav')
}
output = resolve(output)

const deepFilter = findDeepFilter()
const tmp = mkdtempSync(join(tmpdir(), 'limpiar-'))
try {
  // 1. extraer audio a WAV 48k y pasarlo por DeepFilterNet
  const inDir = join(tmp, 'in')
  const outDir = join(tmp, 'out')
  mkdirSync(inDir)
  mkdirSync(outDir)
  const wav = join(inDir, 'audio.wav')
  let r = spawnSync(FFMPEG, ['-v', 'error', '-y', '-i', input, '-map', '0:a:0', '-ar', '48000', '-c:a', 'pcm_s16le', wav], { encoding: 'utf8' })
  if (r.status !== 0) fail(`No se pudo extraer el audio:\n${r.stderr}`)
  console.log('limpiando con DeepFilterNet…')
  r = spawnSync(deepFilter, [wav, '-o', outDir], { encoding: 'utf8' })
  const clean = join(outDir, basename(wav))
  if (r.status !== 0 || !existsSync(clean)) fail(`deep-filter falló:\n${(r.stderr || '').slice(-800)}`)

  // 2. detectar el inicio de la voz sobre el audio limpio (si se pidió recorte)
  let start = 0
  if (trimStart) {
    const det = spawnSync(FFMPEG, ['-v', 'info', '-t', '30', '-i', clean, '-af', 'silencedetect=noise=-38dB:d=0.4', '-f', 'null', '-'], { encoding: 'utf8' }).stderr
    const m = /silence_start: 0[\s\S]*?silence_end: ([\d.]+)/.exec(det)
    if (m) start = Math.max(0, Number(m[1]) - PAD)
    console.log(start > 0 ? `voz detectada en ${(start + PAD).toFixed(2)}s → recorte desde ${start.toFixed(2)}s` : 'no hay silencio inicial que recortar')
  }

  // 3. armar la salida
  const audioFilter = ['-af', SPEECHNORM, '-c:a', 'aac', '-b:a', '192k']
  if (!hasVideo) {
    const isWav = /\.wav$/i.test(output)
    const args = ['-v', 'error', '-y', '-ss', String(start), '-i', clean, '-af', SPEECHNORM,
      ...(isWav ? ['-c:a', 'pcm_s16le'] : ['-c:a', 'aac', '-b:a', '192k']), output]
    r = spawnSync(FFMPEG, args, { encoding: 'utf8' })
  } else if (start > 0) {
    // recorte: re-encodea el video con aceleración por hardware
    const bitrate = height >= 2000 ? '25M' : '12M'
    r = spawnSync(FFMPEG, ['-v', 'error', '-y', '-ss', String(start), '-i', input, '-ss', String(start), '-i', clean,
      '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'hevc_videotoolbox', '-b:v', bitrate, '-tag:v', 'hvc1',
      ...audioFilter, '-shortest', '-movflags', '+faststart', output], { encoding: 'utf8' })
  } else {
    // sin recorte: el video se copia tal cual, solo cambia el audio
    r = spawnSync(FFMPEG, ['-v', 'error', '-y', '-i', input, '-i', clean, '-map', '0:v:0', '-map', '1:a:0',
      '-c:v', 'copy', ...audioFilter, '-shortest', '-movflags', '+faststart', output], { encoding: 'utf8' })
  }
  if (r.status !== 0) fail(`ffmpeg falló al armar la salida:\n${r.stderr}`)

  const durOut = Number(spawnSync(FFPROBE, ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', output], { encoding: 'utf8' }).stdout.trim()) || 0
  console.log(`✔ ${durIn.toFixed(1)}s → ${durOut.toFixed(1)}s${start > 0 ? ` (inicio sin voz recortado)` : ''}`)
  console.log(`  ${output}`)
} finally {
  rmSync(tmp, { recursive: true, force: true })
}
