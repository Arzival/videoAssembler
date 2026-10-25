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
  /** Cómo entra al formato de salida: 'contain' (default) = completo con fondo borroso; 'cover' = llena el cuadro recortando lo que sobra */
  fit?: ClipFit
}

export type ClipFit = 'contain' | 'cover'

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
  /** Ancho de la capa como fracción del ancho de salida (0.15–1; 1 = pantalla completa, p. ej. textos) */
  scale: number
  position: OverlayPosition
  /**
   * Página HTML de la escena (motor de animaciones): el reproductor la muestra EN VIVO sin haberla grabado.
   * `file` sigue siendo el .webm que tendrá al grabarse; el render solo usa `file`.
   */
  html?: string
}

export interface Manifest {
  name: string
  clips: ClipSpec[]
  voice: AudioSpec | null
  music: AudioSpec | null
  overlays?: OverlaySpec[]
  outputs: OutputFormat[]
}
