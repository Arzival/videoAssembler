import type { AudioSpec, ClipSpec, Cut, Manifest, OutputFormat } from './lib/types.ts'
import { keepIntervals } from './lib/graph.ts'

export interface ClipState {
  id: string
  file: string
  media: File | null
  url: string | null
  duration: number
  width: number
  height: number
  trimIn: number
  trimOut: number
  speed: number
  keepAudio: boolean
  audioVolume: number
  cuts: Cut[]
}

export interface TrackState {
  file: string
  media: File | null
  url: string | null
  duration: number
  trimIn: number
  trimOut: number | null
  volume: number
  cuts: Cut[]
  /** Marcas de corte (tiempo del archivo) hechas con la tecla S; solo visuales, no van al manifiesto */
  splits: number[]
}

export const newId = () => crypto.randomUUID()

export function clipFromFile(file: File): ClipState {
  return {
    id: newId(),
    file: file.name,
    media: file,
    url: URL.createObjectURL(file),
    duration: 0,
    width: 0,
    height: 0,
    trimIn: 0,
    trimOut: 0,
    speed: 1,
    keepAudio: false,
    audioVolume: 1,
    cuts: [],
  }
}

export function clipFromSpec(spec: ClipSpec): ClipState {
  return {
    id: newId(),
    file: spec.file,
    media: null,
    url: null,
    duration: 0,
    width: 0,
    height: 0,
    trimIn: spec.trimIn ?? 0,
    trimOut: spec.trimOut ?? 0,
    speed: spec.speed ?? 1,
    keepAudio: spec.keepAudio ?? false,
    audioVolume: spec.audioVolume ?? 1,
    cuts: spec.cuts ?? [],
  }
}

export function trackFromFile(file: File, volume: number): TrackState {
  return {
    file: file.name,
    media: file,
    url: URL.createObjectURL(file),
    duration: 0,
    trimIn: 0,
    trimOut: null,
    volume,
    cuts: [],
    splits: [],
  }
}

export function trackFromSpec(spec: AudioSpec): TrackState {
  return {
    file: spec.file,
    media: null,
    url: null,
    duration: 0,
    trimIn: spec.trimIn ?? 0,
    trimOut: spec.trimOut ?? null,
    volume: spec.volume ?? 1,
    cuts: spec.cuts ?? [],
    splits: [],
  }
}

export const baseName = (path: string) => path.split('/').pop() ?? path

export function buildManifest(
  name: string,
  clips: ClipState[],
  voice: TrackState | null,
  music: TrackState | null,
  outputs: OutputFormat[],
): Manifest {
  return {
    name: name.trim() || 'video',
    clips: clips.map((c) => ({
      file: c.file,
      trimIn: c.trimIn,
      trimOut: c.trimOut || c.duration,
      speed: c.speed,
      keepAudio: c.keepAudio,
      audioVolume: c.audioVolume,
      ...(c.cuts.length > 0 ? { cuts: c.cuts } : {}),
    })),
    voice: voice ? trackSpec(voice) : null,
    music: music ? trackSpec(music) : null,
    outputs,
  }
}

function trackSpec(t: TrackState): AudioSpec {
  return {
    file: t.file,
    trimIn: t.trimIn,
    trimOut: t.trimOut,
    volume: t.volume,
    ...(t.cuts.length > 0 ? { cuts: t.cuts } : {}),
  }
}

/** Acepta "83", "83.5" o "1:23.5" y devuelve segundos */
export function parseTime(input: string): number | null {
  const t = input.trim()
  if (!t) return null
  const m = /^(\d+):([0-5]?\d(?:\.\d+)?)$/.exec(t)
  if (m) return Number(m[1]) * 60 + Number(m[2])
  const n = Number(t)
  return Number.isFinite(n) && n >= 0 ? n : null
}

export function formatTime(totalSeconds: number): string {
  const s = Math.max(0, totalSeconds)
  const m = Math.floor(s / 60)
  const r = s - m * 60
  return `${m}:${r.toFixed(1).padStart(4, '0')}`
}

// ---- Biblioteca de medios (bin) y selección del editor ----

export interface BinItem {
  id: string
  name: string
  media: File | null
  url: string | null
  kind: 'video' | 'audio'
  duration: number
  width: number
  height: number
}

export type Selection =
  | { type: 'clip'; id: string }
  | { type: 'voice'; segment?: number }
  | { type: 'music'; segment?: number }
  | null

const AUDIO_EXT = /\.(wav|mp3|m4a|aac|ogg|flac)$/i

export function isAudioFile(file: File): boolean {
  return file.type.startsWith('audio/') || AUDIO_EXT.test(file.name)
}

export function binFromFile(file: File): BinItem {
  return {
    id: newId(),
    name: file.name,
    media: file,
    url: URL.createObjectURL(file),
    kind: isAudioFile(file) ? 'audio' : 'video',
    duration: 0,
    width: 0,
    height: 0,
  }
}

export function binPlaceholder(name: string, kind: 'video' | 'audio'): BinItem {
  return { id: newId(), name, media: null, url: null, kind, duration: 0, width: 0, height: 0 }
}

/** Lee duración y dimensiones de un archivo de medios ya cargado como object URL */
export function probeMedia(
  url: string,
  kind: 'video' | 'audio',
): Promise<{ duration: number; width: number; height: number }> {
  return new Promise((resolve) => {
    const el = document.createElement(kind) as HTMLVideoElement
    el.preload = 'metadata'
    el.onloadedmetadata = () =>
      resolve({ duration: el.duration || 0, width: el.videoWidth || 0, height: el.videoHeight || 0 })
    el.onerror = () => resolve({ duration: 0, width: 0, height: 0 })
    el.src = url
  })
}

export function clipFromBin(item: BinItem): ClipState {
  return {
    id: newId(),
    file: item.name,
    media: item.media,
    url: item.url,
    duration: item.duration,
    width: item.width,
    height: item.height,
    trimIn: 0,
    trimOut: item.duration,
    speed: 1,
    keepAudio: false,
    audioVolume: 1,
    cuts: [],
  }
}

export function trackFromBin(item: BinItem, volume: number): TrackState {
  return {
    file: item.name,
    media: item.media,
    url: item.url,
    duration: item.duration,
    trimIn: 0,
    trimOut: null,
    volume,
    cuts: [],
    splits: [],
  }
}

// ---- mapeo timeline ↔ tiempo fuente ----

/** Segundos que un clip aporta al video final (recortes y cortes descontados, velocidad aplicada) */
export function clipOutSeconds(c: ClipState): number {
  return keepIntervals(c.trimIn, c.trimOut || c.duration, c.cuts).reduce((s, [a, b]) => s + (b - a), 0) / c.speed
}

/** Convierte un offset de salida (seg dentro del clip en el timeline) a tiempo del archivo fuente */
export function clipSourceTimeAt(c: ClipState, outOffset: number): number | null {
  let remaining = outOffset * c.speed
  for (const [a, b] of keepIntervals(c.trimIn, c.trimOut || c.duration, c.cuts)) {
    const len = b - a
    if (remaining <= len) return a + remaining
    remaining -= len
  }
  return null
}

/** Clip bajo un tiempo global del timeline, con índice y tiempo fuente equivalente */
export function clipAt(
  clips: ClipState[],
  time: number,
): { clip: ClipState; index: number; src: number } | null {
  let acc = 0
  for (let i = 0; i < clips.length; i++) {
    const secs = clipOutSeconds(clips[i])
    if (time < acc + secs) {
      const src = clipSourceTimeAt(clips[i], time - acc)
      return src == null ? null : { clip: clips[i], index: i, src }
    }
    acc += secs
  }
  return null
}

export interface TrackSegment {
  from: number
  to: number
}

/** Segmentos visibles de una pista: intervalos útiles subdivididos por las marcas S */
export function trackSegments(t: TrackState): TrackSegment[] {
  const end = t.trimOut ?? t.duration
  const segs: TrackSegment[] = []
  for (const [a, b] of keepIntervals(t.trimIn, end, t.cuts)) {
    const inner = (t.splits ?? []).filter((s) => s > a + 0.05 && s < b - 0.05).sort((x, y) => x - y)
    let cur = a
    for (const s of inner) {
      segs.push({ from: cur, to: s })
      cur = s
    }
    segs.push({ from: cur, to: b })
  }
  return segs
}

/** Convierte tiempo global del timeline a tiempo del archivo de la pista */
export function trackSourceTimeAt(t: TrackState, time: number): number | null {
  let remaining = time
  const end = t.trimOut ?? t.duration
  for (const [a, b] of keepIntervals(t.trimIn, end, t.cuts)) {
    const len = b - a
    if (remaining <= len) return a + remaining
    remaining -= len
  }
  return null
}

/** Inverso de clipSourceTimeAt: dado un tiempo fuente dentro del clip, offset de salida en el timeline */
export function clipOutOffsetAt(c: ClipState, src: number): number {
  let out = 0
  for (const [a, b] of keepIntervals(c.trimIn, c.trimOut || c.duration, c.cuts)) {
    if (src <= a) break
    out += Math.min(src, b) - a
    if (src <= b) break
  }
  return out / c.speed
}
