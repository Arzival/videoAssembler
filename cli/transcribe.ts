#!/usr/bin/env node
/**
 * Transcribe un audio (la nota de voz) a texto con marcas de tiempo por palabra,
 * para poder editar el video sincronizado con lo que se dice.
 *
 *   node cli/transcribe.ts voz.wav [--out transcript.json] [--lang es] [--model ruta.bin]
 *
 * Salida: JSON con el texto completo y cada palabra con su inicio/fin en segundos
 * (tiempos del ARCHIVO de audio, igual que trimIn/cuts del manifiesto).
 *
 * Audio largo (> 30 s): se parte solo en trozos de ≤ 30 s cortando en silencios (RMS < −40 dB) y cada trozo se transcribe
 * por separado; así Whisper no se cicla ni inventa texto en audios de varios minutos. Los tiempos se devuelven del archivo.
 *
 * Requiere: whisper-cli (brew install whisper-cpp) y ffmpeg en el PATH.
 * Modelo por defecto: ~/.cache/whisper/ggml-large-v3-turbo-q5_0.bin
 *   (descarga: https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin)
 */
import { spawnSync } from 'node:child_process'
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { homedir, tmpdir } from 'node:os'
import { join, resolve } from 'node:path'
import process from 'node:process'

const FFMPEG = process.env.FFMPEG || 'ffmpeg'
const WHISPER = process.env.WHISPER || 'whisper-cli'
const DEFAULT_MODEL = join(homedir(), '.cache/whisper/ggml-large-v3-turbo-q5_0.bin')

function fail(msg: string): never {
  console.error(`✖ ${msg}`)
  process.exit(1)
}

const argv = process.argv.slice(2)
let audioPath = ''
let outPath = ''
let lang = 'es'
let model = process.env.WHISPER_MODEL || DEFAULT_MODEL

for (let i = 0; i < argv.length; i++) {
  const a = argv[i]
  if (a === '--out') outPath = argv[++i]
  else if (a === '--lang') lang = argv[++i]
  else if (a === '--model') model = argv[++i]
  else if (a === '--help' || a === '-h') {
    console.log('Uso: node cli/transcribe.ts audio.wav [--out transcript.json] [--lang es] [--model ruta.bin]')
    process.exit(0)
  } else if (!audioPath) audioPath = a
  else fail(`Argumento inesperado: ${a}`)
}

if (!audioPath) fail('Falta el audio. Uso: node cli/transcribe.ts audio.wav')
audioPath = resolve(audioPath)
if (!existsSync(audioPath)) fail(`No existe: ${audioPath}`)
if (!existsSync(model)) fail(`No existe el modelo: ${model}\nDescárgalo de https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin`)
if (!outPath) outPath = `${audioPath.replace(/\.[^.]+$/, '')}.transcript.json`

const MAX_TROZO = 30

/** Trozos [inicio, fin] de ≤ MAX_TROZO s cortados a la mitad de silencios (RMS < −40 dB en ventanas de 25 ms) */
function partir(wav: string): Array<[number, number]> {
  const buf = readFileSync(wav)
  let off = 12
  while (off < buf.length - 8 && buf.toString('ascii', off, off + 4) !== 'data') off += 8 + buf.readUInt32LE(off + 4)
  const datos = buf.subarray(off + 8)
  const n = Math.floor(datos.length / 2)
  const dur = n / 16000
  if (dur <= MAX_TROZO) return [[0, dur]]
  const win = 400
  const nv = Math.floor(n / win)
  const voz: boolean[] = []
  for (let v = 0; v < nv; v++) {
    let e = 0
    for (let i = 0; i < win; i++) {
      const x = datos.readInt16LE((v * win + i) * 2) / 32768
      e += x * x
    }
    voz.push(10 * Math.log10(e / win + 1e-12) > -40)
  }
  // centros de silencios de ≥ 0.3 s = puntos donde se puede cortar
  const cortes: number[] = []
  for (let v = 0; v < nv; ) {
    if (voz[v]) {
      v++
      continue
    }
    let w = v
    while (w < nv && !voz[w]) w++
    if ((w - v) * 0.025 >= 0.3) cortes.push(((v + w) / 2) * 0.025)
    v = w
  }
  const out: Array<[number, number]> = []
  let a = 0
  while (dur - a > MAX_TROZO) {
    const cand = cortes.filter((c) => c > a + 5 && c <= a + MAX_TROZO)
    const b = cand.length ? cand[cand.length - 1] : a + MAX_TROZO
    out.push([a, b])
    a = b
  }
  out.push([a, dur])
  return out
}

const tmp = mkdtempSync(join(tmpdir(), 'transcribe-'))
try {
  // whisper necesita WAV 16 kHz mono
  const wav16 = join(tmp, 'audio16k.wav')
  const conv = spawnSync(FFMPEG, ['-v', 'error', '-y', '-i', audioPath, '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le', wav16], {
    encoding: 'utf8',
  })
  if (conv.status !== 0) fail(`ffmpeg no pudo convertir el audio:\n${conv.stderr}`)

  interface WhisperSegment {
    offsets: { from: number; to: number }
    text: string
  }
  const whisper = (wav: string, offset: number, k: number) => {
    const prefix = join(tmp, `result${k}`)
    const run = spawnSync(WHISPER, ['-m', model, '-f', wav, '-l', lang, '-oj', '-of', prefix, '-ml', '1', '-sow', '-np'], {
      encoding: 'utf8',
      maxBuffer: 64 * 1024 * 1024,
    })
    if (run.status !== 0) fail(`whisper-cli falló:\n${(run.stderr || '').slice(-2000)}`)
    const raw = JSON.parse(readFileSync(`${prefix}.json`, 'utf8')) as { transcription: WhisperSegment[] }
    return raw.transcription
      .map((s) => ({
        word: s.text.trim(),
        start: Math.round(s.offsets.from + offset * 1000) / 1000,
        end: Math.round(s.offsets.to + offset * 1000) / 1000,
      }))
      .filter((w) => w.word.length > 0)
  }

  console.log('Transcribiendo… (el primer uso tarda más mientras carga el modelo)')
  const trozos = partir(wav16)
  if (trozos.length > 1) console.log(`  audio largo: ${trozos.length} trozos de ≤ ${MAX_TROZO} s cortados en silencios`)
  const words = trozos.flatMap(([a, b], k) => {
    if (trozos.length === 1) return whisper(wav16, 0, k)
    const part = join(tmp, `trozo${k}.wav`)
    const c = spawnSync(FFMPEG, ['-v', 'error', '-y', '-ss', a.toFixed(3), '-to', b.toFixed(3), '-i', wav16, '-c:a', 'pcm_s16le', part], { encoding: 'utf8' })
    if (c.status !== 0) fail(`ffmpeg no pudo partir el audio:\n${c.stderr}`)
    return whisper(part, a, k)
  })

  const text = words.map((w) => w.word).join(' ')
  const result = { audio: audioPath, language: lang, text, words }
  writeFileSync(outPath, JSON.stringify(result, null, 2))

  const dur = words.length > 0 ? words[words.length - 1].end : 0
  console.log(`\n✔ ${words.length} palabras · ${dur.toFixed(1)}s de audio`)
  console.log(`  ${outPath}`)
  console.log(`\n${text.slice(0, 300)}${text.length > 300 ? '…' : ''}`)
} finally {
  rmSync(tmp, { recursive: true, force: true })
}
