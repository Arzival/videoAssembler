import { useEffect, useRef, useState } from 'react'
import type { Manifest } from '../lib/types.ts'
import type { DirHandle } from '../lib/mediaFolder.ts'
import { findFilesByName, findProxies, folderPermission, requestFolderPermission } from '../lib/mediaFolder.ts'
import type { ClipState, OverlayState, TrackState } from '../state.ts'
import { baseName, clipAt, clipFromSpec, clipOutSeconds, formatTime, overlayFromSpec, probeMedia, trackFromSpec } from '../state.ts'
import { PreviewPane, type PlayerHandle } from './PreviewPane.tsx'

/**
 * Modo de comparar: hasta 4 manifiestos lado a lado con un solo control de reproducción. El audio sale de un panel (🔊);
 * ese panel es el reloj maestro y los demás se recolocan si se desfasan más de 80 ms. Solo para ver: no se edita aquí.
 */
export const MAX_COMPARAR = 4
// los paneles se comparan con su tiempo exacto; si uno se separa más que esto se recoloca, pero no más de una vez cada AJUSTE_MS
// (recolocar seguido era lo que trababa la vista: cada salto vuelve a decodificar desde el cuadro clave)
const DESFASE = 0.15
const AJUSTE_MS = 1500

interface Panel {
  id: string
  name: string
  clips: ClipState[]
  voice: TrackState | null
  music: TrackState | null
  overlays: OverlayState[]
  total: number
  /** Los mismos clips sin su audio propio, para los paneles que no son el 🔊 */
  clipsMudos: ClipState[]
}

interface Media {
  media: File
  url: string
  duration: number
  /** Es la versión ligera de .proxies/ (no hace falta volver a buscarla) */
  proxy: boolean
}

interface Props {
  manifests: Manifest[]
  /** La lista vive en App: así lo que se suelta sobre la ventana con el modo abierto se agrega aquí */
  onManifests: (ms: Manifest[]) => void
  folder: DirHandle | null
  /** Archivos ya cargados en el editor (por nombre): se reusan sin volver a leer la carpeta */
  loaded: Map<string, File>
  onClose: () => void
}

function refsOf(m: Manifest): string[] {
  return [...m.clips.map((c) => c.file), ...(m.voice ? [m.voice.file] : []), ...(m.music ? [m.music.file] : []), ...(m.overlays ?? []).map((o) => o.file)]
}

export function CompararPane({ manifests, onManifests, folder, loaded, onClose }: Props) {
  const [panels, setPanels] = useState<Panel[]>([])
  const [faltan, setFaltan] = useState<string[]>([])
  const [permiso, setPermiso] = useState(false)
  const [maestro, setMaestro] = useState(0)
  const [playing, setPlaying] = useState(false)
  const [heads, setHeads] = useState<number[]>([])
  const [ampliado, setAmpliado] = useState<number | null>(null)
  const [cargando, setCargando] = useState(true)
  const ultimoAjuste = useRef<number[]>([])
  const players = useRef<Array<React.MutableRefObject<PlayerHandle | null>>>([])
  const headsRef = useRef<number[]>([])
  headsRef.current = heads
  // caché común: las pruebas comparten clips, voz y música → cada archivo se lee una sola vez
  const cache = useRef(new Map<string, Media>())
  const htmlCache = useRef(new Map<string, string>())

  const tiempo = heads[maestro] ?? 0
  const total = Math.max(0, ...panels.map((p) => p.total))

  // ---- carga y resolución de archivos ----
  useEffect(() => {
    let vivo = true
    const cargar = async () => {
      detener()
      setCargando(true)
      const refs = [...new Set(manifests.flatMap(refsOf))]
      const permitido = folder ? (await folderPermission(folder)) === 'granted' : false
      if (folder && !permitido && vivo) setPermiso(true)
      // primero las versiones ligeras (cli/proxies.py): 2–4 tomas 4K HDR decodificándose a la vez traban la vista;
      // también reemplazan a los originales que ya se hubieran tomado del editor antes de dar permiso a la carpeta
      const files: Array<{ f: File; proxy: boolean }> = []
      if (folder && permitido) {
        const sinProxy = refs.filter((r) => !cache.current.get(baseName(r))?.proxy)
        for (const f of (await findProxies(folder, sinProxy)).values()) files.push({ f, proxy: true })
      }
      const conProxy = new Set(files.map((x) => x.f.name))
      const pendientes = refs.filter((r) => !cache.current.has(baseName(r)) && !conProxy.has(baseName(r)))
      for (const r of pendientes) {
        const f = loaded.get(baseName(r))
        if (f) files.push({ f, proxy: false })
      }
      const sinArchivo = pendientes.filter((r) => !loaded.has(baseName(r)))
      if (sinArchivo.length && folder && permitido) for (const f of await findFilesByName(folder, sinArchivo)) files.push({ f, proxy: false })
      await Promise.all(
        files.map(async ({ f, proxy }) => {
          const url = URL.createObjectURL(f)
          const kind = /\.(wav|mp3|m4a|aac|ogg|flac)$/i.test(f.name) ? 'audio' : 'video'
          const meta = await probeMedia(url, kind)
          const viejo = cache.current.get(f.name)
          if (viejo) URL.revokeObjectURL(viejo.url)
          cache.current.set(f.name, { media: f, url, duration: meta.duration, proxy })
        }),
      )

      // escenas del motor (HTML) para verlas en vivo
      const htmlRefs = [...new Set(manifests.flatMap((m) => (m.overlays ?? []).filter((o) => o.html).map((o) => o.html as string)))].filter(
        (r) => !htmlCache.current.has(baseName(r)),
      )
      if (htmlRefs.length && folder && (await folderPermission(folder)) === 'granted') {
        for (const f of await findFilesByName(folder, htmlRefs)) htmlCache.current.set(f.name, URL.createObjectURL(new Blob([await f.text()], { type: 'text/html' })))
      }
      if (!vivo) return
      const con = <T extends { file: string; media: File | null; url: string | null; duration: number }>(x: T): T => {
        const m = cache.current.get(baseName(x.file))
        return m ? { ...x, media: m.media, url: m.url, duration: m.duration } : x
      }
      const nuevos = manifests.map((m, i) => {
        const clips = m.clips.map((c) => {
          const s = con(clipFromSpec(c))
          return { ...s, trimOut: s.trimOut > 0 ? s.trimOut : s.duration }
        })
        return {
          id: `${i}-${m.name}`,
          name: m.name || `manifiesto ${i + 1}`,
          clips,
          voice: m.voice ? con(trackFromSpec(m.voice)) : null,
          music: m.music ? con(trackFromSpec(m.music)) : null,
          overlays: (m.overlays ?? []).map((o) => {
            const x = con(overlayFromSpec(o))
            return x.html ? { ...x, htmlUrl: htmlCache.current.get(baseName(x.html)) ?? null } : x
          }),
          total: clips.reduce((t, c) => t + clipOutSeconds(c), 0),
          clipsMudos: clips.map((c) => ({ ...c, keepAudio: false })),
        }
      })
      setPanels(nuevos)
      setHeads(nuevos.map(() => 0))
      setCargando(false)
      const conHtml = new Set(manifests.flatMap((m) => (m.overlays ?? []).filter((o) => o.html && htmlCache.current.has(baseName(o.html))).map((o) => o.file)))
      setFaltan(refs.filter((r) => !cache.current.has(baseName(r)) && !conHtml.has(r)).map(baseName))
    }
    void cargar()
    return () => {
      vivo = false
    }
  }, [manifests, folder, loaded, permiso])

  useEffect(() => () => cache.current.forEach((m) => URL.revokeObjectURL(m.url)), [])
  // el botón ▶ del editor quedaba con el foco detrás de esta vista: que la barra espaciadora no lo active
  useEffect(() => {
    if (document.activeElement instanceof HTMLElement) document.activeElement.blur()
  }, [])

  while (players.current.length < panels.length) players.current.push({ current: null })

  // ---- reloj maestro: los demás paneles siguen al que suena ----
  useEffect(() => {
    if (!playing) return
    const id = setInterval(() => {
      const m = players.current[maestro]?.current
      const t = m?.ahora() ?? 0
      if (!m?.isPlaying() && t >= (panels[maestro]?.total ?? 0) - 0.1) {
        detener()
        return
      }
      const ahora = performance.now()
      panels.forEach((p, i) => {
        if (i === maestro || t >= p.total - 0.05) return
        const pl = players.current[i]?.current
        if (!pl || ahora - (ultimoAjuste.current[i] ?? 0) < AJUSTE_MS) return
        if (Math.abs(pl.ahora() - t) > DESFASE) {
          ultimoAjuste.current[i] = ahora
          pl.play(t)
        }
      })
    }, 250)
    return () => clearInterval(id)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [playing, maestro, panels])

  const reproducir = (desde = tiempo) => {
    // antes de que terminen de cargar los paneles no hay nada que arrancar (quedaba «reproduciendo» en silencio)
    if (cargando || !panels.length) return
    ultimoAjuste.current = panels.map(() => performance.now())
    const t = desde >= total - 0.05 ? 0 : desde
    panels.forEach((p, i) => {
      if (t < p.total - 0.05) players.current[i]?.current?.play(t)
    })
    setPlaying(true)
  }
  const detener = () => {
    players.current.forEach((p) => p.current?.stop())
    setPlaying(false)
  }
  const mover = (t: number) => {
    setHeads((h) => h.map(() => t))
    if (playing) reproducir(t)
  }
  const cambiarMaestro = (i: number) => {
    setMaestro(i)
    // las voces se arrancan con su volumen: para cambiar de panel con audio se recoloca todo en el mismo punto
    if (playing) setTimeout(() => reproducir(headsRef.current[maestro] ?? 0), 0)
  }
  const quitar = (i: number) => {
    detener()
    onManifests(manifests.filter((_, k) => k !== i))
    setMaestro(0)
    setAmpliado(null)
  }
  const agregar = (files: FileList | null) => {
    if (!files) return
    void Promise.all(Array.from(files).map((f) => f.text().then((t) => JSON.parse(t) as Manifest))).then((nuevos) => {
      detener()
      onManifests([...manifests, ...nuevos.filter((m) => Array.isArray(m.clips))].slice(0, MAX_COMPARAR))
    })
  }

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement) return
      if (e.code === 'Space') {
        e.preventDefault()
        if (playing) detener()
        else reproducir()
      } else if (e.key === 'Escape') {
        if (ampliado != null) setAmpliado(null)
        else onClose()
      } else if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        mover(Math.min(total, Math.max(0, tiempo + (e.key === 'ArrowRight' ? 1 : -1))))
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  })

  const silenciar = (t: TrackState | null) => (t ? { ...t, volume: 0 } : null)

  return (
    <div className="comparar">
      <header className="comparar-barra">
        <strong>Comparar</strong>
        <button className="primary" onClick={() => (playing ? detener() : reproducir())} disabled={cargando || !panels.length}>
          {cargando ? 'Cargando…' : playing ? '■ Detener' : '▶ Reproducir'}
        </button>
        <input
          className="comparar-cabezal"
          type="range"
          min={0}
          max={Math.max(0.1, total)}
          step={0.05}
          value={Math.min(tiempo, total)}
          onChange={(e) => mover(Number(e.target.value))}
        />
        <span className="preview-time">
          {formatTime(tiempo)} / {formatTime(total)}
        </span>
        {manifests.length < MAX_COMPARAR && (
          <label className="btn">
            + Agregar manifiesto
            <input type="file" accept="application/json,.json" multiple onChange={(e) => (agregar(e.target.files), (e.target.value = ''))} />
          </label>
        )}
        <button onClick={() => (detener(), onClose())}>Cerrar</button>
      </header>
      {permiso && folder && (
        <div className="banner banner-info">
          📂 El navegador pide tu clic para leer la carpeta «{folder.name}».
          <button className="small primary" onClick={async () => (await requestFolderPermission(folder)) && setPermiso(false)}>
            Cargar archivos
          </button>
        </div>
      )}
      {faltan.length > 0 && !permiso && (
        <div className="banner">⚠ Faltan archivos: {faltan.join(', ')} — conecta la carpeta de medios o agrégalos en el editor.</div>
      )}
      <div className={`comparar-paneles n${ampliado != null ? 1 : panels.length}`}>
        {panels.map((p, i) => (
          <section key={p.id} className="comparar-panel" style={ampliado != null && ampliado !== i ? { display: 'none' } : undefined}>
            <div className="comparar-titulo">
              <button className={`small ${i === maestro ? 'primary' : ''}`} onClick={() => cambiarMaestro(i)} title="Escuchar este panel">
                {i === maestro ? '🔊' : '🔈'}
              </button>
              <span title={p.name}>{p.name}</span>
              <span className="preview-time">{formatTime(p.total)}</span>
              <button className="small" onClick={() => setAmpliado(ampliado === i ? null : i)} title="Pantalla completa / regresar">
                {ampliado === i ? '⤡' : '⤢'}
              </button>
              <button className="small" onClick={() => quitar(i)} title="Quitar de la comparación">
                ✕
              </button>
            </div>
            <PreviewPane
              clip={null}
              clips={i === maestro ? p.clips : p.clipsMudos}
              voice={i === maestro ? p.voice : silenciar(p.voice)}
              music={i === maestro ? p.music : silenciar(p.music)}
              overlays={p.overlays}
              scrub={clipAt(p.clips, Math.min(heads[i] ?? 0, Math.max(0, p.total - 0.01)))}
              playhead={heads[i] ?? 0}
              onPlayhead={(t) => setHeads((h) => h.map((x, k) => (k === i ? t : x)))}
              onClipChange={() => {}}
              playerRef={players.current[i]}
              onMediaError={() => {}}
            />
          </section>
        ))}
        {!panels.length && <div className="preview-empty">{cargando && manifests.length ? 'Cargando…' : 'Agrega de 2 a 4 manifiestos para compararlos.'}</div>}
      </div>
      <footer className="comparar-ayuda preview-time">
        Espacio: reproducir/detener · ←/→: 1 s · 🔊: de qué panel sale el audio · ⤢: ver uno solo · Esc: regresar
      </footer>
    </div>
  )
}
