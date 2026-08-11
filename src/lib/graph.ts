import type { AudioSpec, Cut, Manifest, OutputFormat } from './types.ts'

export const FORMATS: Record<OutputFormat, { w: number; h: number }> = {
  vertical: { w: 1080, h: 1920 },
  horizontal: { w: 1920, h: 1080 },
}

export const FPS = 60

export type Encoder = 'videotoolbox' | 'x264' | 'wasm'

export interface BuildOptions {
  format: OutputFormat
  encoder: Encoder
  /** Nombres de archivo de entrada, en el orden de inputFiles(manifest) */
  inputNames: string[]
  /** Por clip: si el archivo realmente tiene pista de audio (default: true) */
  clipHasAudio?: boolean[]
  outputName: string
}

/** Archivos de entrada en orden: clips…, voz?, música? */
export function inputFiles(m: Manifest): string[] {
  const files = m.clips.map((c) => c.file)
  if (m.voice) files.push(m.voice.file)
  if (m.music) files.push(m.music.file)
  return files
}

/** Resta los cortes internos al rango [trimIn, trimOut] → intervalos que sí se usan */
export function keepIntervals(trimIn: number, trimOut: number, cuts?: Cut[]): Array<[number, number]> {
  let intervals: Array<[number, number]> = [[trimIn, trimOut]]
  const sorted = [...(cuts ?? [])].filter((c) => c.to > c.from).sort((a, b) => a.from - b.from)
  for (const cut of sorted) {
    const next: Array<[number, number]> = []
    for (const [a, b] of intervals) {
      if (cut.to <= a || cut.from >= b) {
        next.push([a, b])
        continue
      }
      if (cut.from > a) next.push([a, cut.from])
      if (cut.to < b) next.push([cut.to, b])
    }
    intervals = next
  }
  return intervals.filter(([a, b]) => b - a > 0.01)
}

/** Duración estimada del video final en segundos */
export function outputDuration(m: Manifest): number {
  return m.clips.reduce(
    (sum, c) =>
      sum + keepIntervals(c.trimIn, c.trimOut, c.cuts).reduce((s, [a, b]) => s + (b - a), 0) / c.speed,
    0,
  )
}

export function outputFileName(m: Manifest, format: OutputFormat): string {
  const base = (m.name || 'video').replace(/[^\w.-]+/g, '-')
  return `${base}-${format}.mp4`
}

const fmt = (n: number) => String(Math.round(n * 1000) / 1000)

const AUDIO_NORM = 'aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo'

/** Cadena de filtros para una pista de audio (voz/música) con recorte, cortes y volumen */
function audioTrackChain(track: AudioSpec, inputIdx: number, label: string, parts: string[]): void {
  const end = track.trimOut ?? Number.POSITIVE_INFINITY
  const intervals = keepIntervals(track.trimIn, end, track.cuts)
  if (intervals.length === 0) throw new Error(`Los cortes eliminan toda la pista "${track.file}"`)
  const post = `volume=${fmt(track.volume)},${AUDIO_NORM}`
  const atrim = ([a, b]: [number, number]) =>
    `atrim=start=${fmt(a)}${Number.isFinite(b) ? `:end=${fmt(b)}` : ''},asetpts=PTS-STARTPTS`
  if (intervals.length === 1) {
    parts.push(`[${inputIdx}:a:0]${atrim(intervals[0])},${post}[${label}]`)
    return
  }
  const segLabels: string[] = []
  intervals.forEach((iv, k) => {
    parts.push(`[${inputIdx}:a:0]${atrim(iv)}[${label}s${k}]`)
    segLabels.push(`[${label}s${k}]`)
  })
  parts.push(`${segLabels.join('')}concat=n=${intervals.length}:v=0:a=1,${post}[${label}]`)
}

/** Construye la lista completa de argumentos de ffmpeg (sin el binario) */
export function buildArgs(m: Manifest, o: BuildOptions): string[] {
  const { w, h } = FORMATS[o.format]

  // Cada clip se expande en 1+ segmentos según sus cortes internos
  interface Seg {
    input: number
    from: number
    to: number
    speed: number
    useAudio: boolean
    audioVolume: number
  }
  const segs: Seg[] = []
  m.clips.forEach((c, i) => {
    const hasAudio = o.clipHasAudio ? o.clipHasAudio[i] !== false : true
    for (const [from, to] of keepIntervals(c.trimIn, c.trimOut, c.cuts)) {
      segs.push({ input: i, from, to, speed: c.speed, useAudio: c.keepAudio && hasAudio, audioVolume: c.audioVolume })
    }
  })
  if (segs.length === 0) throw new Error('El manifiesto no tiene clips (o los cortes eliminan todo)')

  const parts: string[] = []

  segs.forEach((s, j) => {
    const dur = (s.to - s.from) / s.speed
    parts.push(
      `[${s.input}:v:0]trim=start=${fmt(s.from)}:end=${fmt(s.to)},` +
        `setpts=(PTS-STARTPTS)/${fmt(s.speed)},fps=${FPS},split=2[c${j}a][c${j}b]`,
      `[c${j}a]scale=${w}:${h}:force_original_aspect_ratio=decrease:force_divisible_by=2,setsar=1[c${j}fg]`,
      `[c${j}b]scale=${w}:${h}:force_original_aspect_ratio=increase,crop=${w}:${h},setsar=1,` +
        `boxblur=luma_radius=24:luma_power=2:chroma_radius=12:chroma_power=2[c${j}bg]`,
      `[c${j}bg][c${j}fg]overlay=x=(main_w-overlay_w)/2:y=(main_h-overlay_h)/2,format=yuv420p[v${j}]`,
    )
    if (s.useAudio) {
      parts.push(
        `[${s.input}:a:0]atrim=start=${fmt(s.from)}:end=${fmt(s.to)},asetpts=PTS-STARTPTS,` +
          `atempo=${fmt(s.speed)},volume=${fmt(s.audioVolume)},${AUDIO_NORM}[a${j}]`,
      )
    } else {
      parts.push(`anullsrc=r=44100:cl=stereo,atrim=start=0:end=${fmt(dur)},asetpts=PTS-STARTPTS[a${j}]`)
    }
  })

  const pairs = segs.map((_, j) => `[v${j}][a${j}]`).join('')
  parts.push(`${pairs}concat=n=${segs.length}:v=1:a=1[vcat][acat]`)

  const mixInputs = ['[acat]']
  let inputIdx = m.clips.length
  for (const [track, label] of [
    [m.voice, 'voz'],
    [m.music, 'mus'],
  ] as const) {
    if (!track) continue
    audioTrackChain(track, inputIdx, label, parts)
    mixInputs.push(`[${label}]`)
    inputIdx++
  }

  let audioMap: string
  if (mixInputs.length > 1) {
    parts.push(`${mixInputs.join('')}amix=inputs=${mixInputs.length}:duration=first:normalize=0[aout]`)
    audioMap = '[aout]'
  } else {
    audioMap = '[acat]'
  }

  const args = ['-y']
  for (const name of o.inputNames) args.push('-i', name)
  args.push('-filter_complex', parts.join(';'), '-map', '[vcat]', '-map', audioMap)

  if (o.encoder === 'videotoolbox') {
    args.push('-c:v', 'h264_videotoolbox', '-b:v', '12M', '-maxrate', '16M', '-bufsize', '24M', '-allow_sw', '1')
  } else if (o.encoder === 'x264') {
    args.push('-c:v', 'libx264', '-preset', 'medium', '-crf', '20')
  } else {
    args.push('-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '23')
  }
  args.push('-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-movflags', '+faststart', o.outputName)
  return args
}
