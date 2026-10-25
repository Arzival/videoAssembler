import { useEffect, useRef, useState } from 'react'
import type { OverlayState } from '../state.ts'

/**
 * Escena del motor de animaciones vista EN VIVO: la página HTML de la escena (1080×1920) en un iframe escalado al cuadro del
 * preview, movida al mismo instante que el video con el mismo contrato que usa la grabación (cli/animaciones/capturar.ts):
 * se pausan sus animaciones CSS en el tiempo local y se llama window.__seek(t). Así lo que se ve aquí es lo que se grabará.
 * La página se abre con #preview para que el 3D baje su supermuestreo (la grabación final va en calidad completa).
 */
interface Props {
  overlay: OverlayState
  /** Ancho en px del cuadro del video dentro del preview */
  width: number
  playhead: number
  playing: boolean
  /** Tiempo exacto del video final mientras se reproduce (el cursor de App se actualiza ~4 veces por segundo) */
  ahora: () => number
}

interface SceneWindow extends Window {
  __seek?: (s: number) => void
  __listo?: Promise<unknown>
}

export function HtmlOverlay({ overlay: o, width, playhead, playing, ahora }: Props) {
  const ref = useRef<HTMLIFrameElement>(null)
  const [lista, setLista] = useState(false)
  const [error, setError] = useState('')

  const mover = (t: number) => {
    const w = ref.current?.contentWindow as SceneWindow | null
    if (!w || !lista) return
    const local = Math.max(0, t - o.start + o.trimIn)
    try {
      for (const a of w.document.getAnimations()) {
        a.pause()
        a.currentTime = local * 1000
      }
      w.__seek?.(local)
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err))
    }
  }

  // en pausa manda el cursor; reproduciendo, cada cuadro con el tiempo exacto del video
  useEffect(() => {
    if (!playing) mover(playhead)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [playhead, playing, lista])
  useEffect(() => {
    if (!playing || !lista) return
    let id = 0
    const paso = () => {
      mover(ahora())
      id = requestAnimationFrame(paso)
    }
    id = requestAnimationFrame(paso)
    return () => cancelAnimationFrame(id)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [playing, lista])

  const onLoad = () => {
    const w = ref.current?.contentWindow as SceneWindow | null
    if (!w) return
    Promise.resolve(w.__listo)
      .then(() => setLista(true))
      .catch((err) => setError(`la escena no cargó: ${err instanceof Error ? err.message : err}`))
  }

  const visible = playhead >= o.start && playhead < o.end
  const k = width / 1080
  return (
    <div className="html-overlay" style={{ display: visible ? 'block' : 'none' }} title={o.html}>
      <iframe
        ref={ref}
        // credentialless: el editor corre con COEP (ffmpeg.wasm); así la escena puede cargar sus fuentes y three.js de CDN
        {...({ credentialless: '' } as object)}
        src={`${o.htmlUrl}#preview`}
        onLoad={onLoad}
        style={{ width: 1080, height: 1920, transform: `scale(${k})`, transformOrigin: '0 0', opacity: lista ? 1 : 0 }}
      />
      {!lista && visible && !error && <span className="html-overlay-estado">cargando escena…</span>}
      {error && <span className="html-overlay-estado error">⚠ {error}</span>}
    </div>
  )
}
