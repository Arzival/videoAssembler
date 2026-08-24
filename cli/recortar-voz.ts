#!/usr/bin/env node
/**
 * Recorta los silencios de una nota de voz replicando EXACTAMENTE el proyecto
 * hermano «recortador-voz» (mismo filtro y parámetros por defecto), pero con
 * ffmpeg nativo, para usarlo en el pipeline sin abrir el navegador.
 *
 *   node cli/recortar-voz.ts voz.wav [--out voz-recortada.wav] [--threshold -40] [--duration 0.5]
 *
 * Filtro: silenceremove=start_periods=1:start_threshold=TdB:stop_periods=-1:stop_duration=D:stop_threshold=TdB
 * (idéntico a recortador-voz; T=-40dB y D=0.5s son sus valores por defecto)
 */
import { spawnSync } from 'node:child_process'
import { existsSync } from 'node:fs'
import { resolve } from 'node:path'
import process from 'node:process'

const FFMPEG = process.env.FFMPEG || 'ffmpeg'
const FFPROBE = process.env.FFPROBE || 'ffprobe'

function fail(msg: string): never {
  console.error(`✖ ${msg}`)
  process.exit(1)
}

const argv = process.argv.slice(2)
let input = ''
let output = ''
let threshold = -40
let duration = 0.5

for (let i = 0; i < argv.length; i++) {
  const a = argv[i]
  if (a === '--out') output = argv[++i]
  else if (a === '--threshold') threshold = Number(argv[++i])
  else if (a === '--duration') duration = Number(argv[++i])
  else if (a === '--help' || a === '-h') {
    console.log('Uso: node cli/recortar-voz.ts voz.wav [--out salida.wav] [--threshold -40] [--duration 0.5]')
    process.exit(0)
  } else if (!input) input = a
  else fail(`Argumento inesperado: ${a}`)
}

if (!input) fail('Falta el audio. Uso: node cli/recortar-voz.ts voz.wav')
input = resolve(input)
if (!existsSync(input)) fail(`No existe: ${input}`)
if (!output) output = input.replace(/(\.[^.]+)$/, '-recortada$1')
output = resolve(output)

const probeDur = (f: string) =>
  Number(spawnSync(FFPROBE, ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], { encoding: 'utf8' }).stdout.trim())

// conserva el códec PCM del wav original; otros formatos salen como el original decodificado a s16
const codec = spawnSync(FFPROBE, ['-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=codec_name', '-of', 'csv=p=0', input], {
  encoding: 'utf8',
}).stdout.trim()
const audioCodec = codec.startsWith('pcm_') ? codec : 'pcm_s16le'

const t = Math.round(threshold)
const filter = `silenceremove=start_periods=1:start_threshold=${t}dB:stop_periods=-1:stop_duration=${duration}:stop_threshold=${t}dB`

const r = spawnSync(FFMPEG, ['-v', 'error', '-y', '-i', input, '-af', filter, '-c:a', audioCodec, output], { encoding: 'utf8' })
if (r.status !== 0) fail(`ffmpeg falló:\n${r.stderr}`)

const before = probeDur(input)
const after = probeDur(output)
console.log(`✔ ${before.toFixed(1)}s → ${after.toFixed(1)}s (${(before - after).toFixed(1)}s de silencio eliminados)`)
console.log(`  ${output}`)
