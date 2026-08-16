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

export type OverlayPosition =
  | 'top-left'
  | 'top'
  | 'top-right'
  | 'left'
  | 'center'
  | 'right'
  | 'bottom-left'
  | 'bottom'
  | 'bottom-right'

/** Capa de video superpuesta durante un rango del video final */
export interface OverlaySpec {
  file: string
  /** Segundo del VIDEO FINAL donde aparece */
  start: number
  /** Segundo del video final donde desaparece */
  end: number
  /** Desde qué segundo del archivo fuente se toma (default 0) */
  trimIn: number
  /** Ancho de la capa como fracción del ancho de salida (0.15–0.8) */
  scale: number
  position: OverlayPosition
}

export interface Manifest {
  name: string
  clips: ClipSpec[]
  voice: AudioSpec | null
  music: AudioSpec | null
  overlays?: OverlaySpec[]
  outputs: OutputFormat[]
}
