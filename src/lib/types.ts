export type OutputFormat = 'vertical' | 'horizontal'

/** Rango interno a eliminar, en segundos del archivo original */
export interface Cut {
  from: number
  to: number
}

export interface ClipSpec {
  file: string
  trimIn: number
  trimOut: number
  speed: number
  keepAudio: boolean
  audioVolume: number
  cuts?: Cut[]
}

export interface AudioSpec {
  file: string
  trimIn: number
  trimOut: number | null
  volume: number
  cuts?: Cut[]
}

export interface Manifest {
  name: string
  clips: ClipSpec[]
  voice: AudioSpec | null
  music: AudioSpec | null
  outputs: OutputFormat[]
}
