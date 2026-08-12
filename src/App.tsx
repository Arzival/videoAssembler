import { useEffect, useRef, useState } from 'react'
import type { Manifest, OutputFormat } from './lib/types.ts'
import { keepIntervals } from './lib/graph.ts'
import type { BinItem, ClipState, Selection, TrackState } from './state.ts'
import {
  baseName,
  binPlaceholder,
  buildManifest,
  clipAt,
  clipFromBin,
  clipFromSpec,
  clipOutSeconds,
  isAudioFile,
  newId,
  probeMedia,
  trackFromBin,
  trackFromSpec,
  trackSegments,
} from './state.ts'
import { TopBar } from './components/TopBar.tsx'
import { MediaBin } from './components/MediaBin.tsx'
import { PreviewPane } from './components/PreviewPane.tsx'
import { Inspector } from './components/Inspector.tsx'
import { TimelinePane } from './components/TimelinePane.tsx'

export default function App() {
  const [name, setName] = useState('mi-video')
  const [bin, setBin] = useState<BinItem[]>([])
  const [clips, setClips] = useState<ClipState[]>([])
  const [voice, setVoice] = useState<TrackState | null>(null)
  const [music, setMusic] = useState<TrackState | null>(null)
  const [outputs, setOutputs] = useState<OutputFormat[]>(['vertical'])
  const [selection, setSelection] = useState<Selection>(null)
  const [playhead, setPlayhead] = useState(0)
  const [restored, setRestored] = useState(false)

  // instantánea para los atajos de teclado (el listener vive fuera del ciclo de render)
  const snap = useRef({ clips, voice, music, selection, playhead })
  snap.current = { clips, voice, music, selection, playhead }

  // ---- deshacer ----

  interface HistoryEntry {
    clips: ClipState[]
    voice: TrackState | null
    music: TrackState | null
    selection: Selection
  }
  const history = useRef<HistoryEntry[]>([])

  /** Guarda el estado actual antes de una operación destructiva */
  const pushHistory = () => {
    const { clips, voice, music, selection } = snap.current
    history.current.push({ clips, voice, music, selection })
    if (history.current.length > 50) history.current.shift()
  }

  const undo = () => {
    const prev = history.current.pop()
    if (!prev) return
    setClips(prev.clips)
    setVoice(prev.voice)
    setMusic(prev.music)
    setSelection(prev.selection)
  }

  // controles del preview, registrados por PreviewPane (para la barra espaciadora)
  const playerRef = useRef<{ toggle: () => void } | null>(null)

  // ---- biblioteca de archivos ----

  const addFiles = (list: FileList | null) => {
    if (!list?.length) return
    const prepared = Array.from(list).map((file) => ({
      file,
      url: URL.createObjectURL(file),
      kind: (isAudioFile(file) ? 'audio' : 'video') as 'audio' | 'video',
    }))

    setBin((prev) => {
      const next = [...prev]
      for (const p of prepared) {
        const idx = next.findIndex((b) => !b.media && b.name === p.file.name)
        if (idx >= 0) next[idx] = { ...next[idx], media: p.file, url: p.url, kind: p.kind }
        else next.push({ id: newId(), name: p.file.name, media: p.file, url: p.url, kind: p.kind, duration: 0, width: 0, height: 0 })
      }
      return next
    })
    setClips((prev) =>
      prev.map((c) => {
        if (c.media) return c
        const p = prepared.find((p) => baseName(c.file) === p.file.name)
        return p ? { ...c, media: p.file, url: p.url } : c
      }),
    )
    const fillTrack = (t: TrackState | null) => {
      if (!t || t.media) return t
      const p = prepared.find((p) => baseName(t.file) === p.file.name)
      return p ? { ...t, media: p.file, url: p.url } : t
    }
    setVoice(fillTrack)
    setMusic(fillTrack)

    for (const p of prepared) {
      void probeMedia(p.url, p.kind).then((meta) => {
        if (meta.duration <= 0) return
        setBin((prev) => prev.map((b) => (b.url === p.url ? { ...b, ...meta } : b)))
        setClips((prev) =>
          prev.map((c) =>
            c.url === p.url && c.duration === 0
              ? { ...c, ...meta, trimOut: c.trimOut > 0 ? Math.min(c.trimOut, meta.duration) : meta.duration }
              : c,
          ),
        )
        const fillDur = (t: TrackState | null) =>
          t && t.url === p.url && t.duration === 0 ? { ...t, duration: meta.duration } : t
        setVoice(fillDur)
        setMusic(fillDur)
      })
    }
  }

  const removeBinItem = (item: BinItem) => {
    pushHistory()
    setBin((prev) => prev.filter((b) => b.id !== item.id))
    setClips((prev) => prev.filter((c) => !(item.url ? c.url === item.url : baseName(c.file) === item.name)))
    const clearTrack = (t: TrackState | null) =>
      t && (item.url ? t.url === item.url : baseName(t.file) === item.name) ? null : t
    setVoice(clearTrack)
    setMusic(clearTrack)
    setSelection(null)
    if (item.url) URL.revokeObjectURL(item.url)
  }

  // ---- línea de tiempo ----

  const addToTimeline = (item: BinItem) => {
    pushHistory()
    const c = clipFromBin(item)
    setClips((prev) => [...prev, c])
    setSelection({ type: 'clip', id: c.id })
  }

  const assignVoice = (item: BinItem) => {
    pushHistory()
    setVoice(trackFromBin(item, voice?.volume ?? 1))
    setSelection({ type: 'voice', segment: 0 })
  }

  const assignMusic = (item: BinItem) => {
    pushHistory()
    setMusic(trackFromBin(item, music?.volume ?? 0.15))
    setSelection({ type: 'music', segment: 0 })
  }

  const updateClip = (id: string, patch: Partial<ClipState>) =>
    setClips((prev) => prev.map((c) => (c.id === id ? { ...c, ...patch } : c)))

  const removeClip = (id: string) => {
    pushHistory()
    setClips((prev) => prev.filter((c) => c.id !== id))
    setSelection(null)
  }

  const duplicateClip = (id: string) => {
    pushHistory()
    setClips((prev) => {
      const i = prev.findIndex((c) => c.id === id)
      if (i < 0) return prev
      const copy = { ...prev[i], id: newId() }
      return [...prev.slice(0, i + 1), copy, ...prev.slice(i + 1)]
    })
  }

  const moveClip = (from: number, to: number) =>
    setClips((prev) => {
      if (to < 0 || to >= prev.length || from === to) return prev
      const next = [...prev]
      const [item] = next.splice(from, 1)
      next.splice(to, 0, item)
      return next
    })

  // ---- cortar (S) y borrar (⌫) ----

  const splitAtPlayhead = () => {
    const { clips, voice, music, selection, playhead } = snap.current
    pushHistory()

    if (selection?.type === 'voice' || selection?.type === 'music') {
      const track = selection.type === 'voice' ? voice : music
      if (!track || track.duration === 0) return
      const setTrack = selection.type === 'voice' ? setVoice : setMusic
      // el playhead es tiempo global; la pista corre desde 0 → mapear a tiempo del archivo
      let remaining = playhead
      let src: number | null = null
      for (const [a, b] of keepIntervals(track.trimIn, track.trimOut ?? track.duration, track.cuts)) {
        const len = b - a
        if (remaining <= len) {
          src = a + remaining
          break
        }
        remaining -= len
      }
      if (src == null) return
      const rounded = Math.round(src * 1000) / 1000
      setTrack((t) =>
        t ? { ...t, splits: [...new Set([...(t.splits ?? []), rounded])].sort((a, b) => a - b) } : t,
      )
      return
    }

    // sin selección de pista → corta el clip de video bajo el cursor
    const hit = clipAt(clips, playhead)
    if (!hit) return
    const { clip, index, src } = hit
    const margin = 0.05
    if (src <= clip.trimIn + margin || src >= (clip.trimOut || clip.duration) - margin) return
    const first: ClipState = { ...clip, trimOut: src }
    const second: ClipState = { ...clip, id: newId(), trimIn: src }
    setClips((prev) => [...prev.slice(0, index), first, second, ...prev.slice(index + 1)])
    setSelection({ type: 'clip', id: second.id })
  }

  const deleteSelected = () => {
    const { voice, music, selection } = snap.current
    if (!selection) return
    if (selection.type !== 'clip') pushHistory() // el camino de clip ya la guarda en removeClip
    if (selection.type === 'clip') {
      removeClip(selection.id)
      return
    }
    const track = selection.type === 'voice' ? voice : music
    const setTrack = selection.type === 'voice' ? setVoice : setMusic
    if (!track || selection.segment == null) return
    const segments = trackSegments(track)
    const seg = segments[selection.segment]
    if (!seg) return
    if (segments.length === 1) {
      setTrack(null)
    } else {
      setTrack((t) =>
        t
          ? {
              ...t,
              cuts: [...t.cuts, { from: seg.from, to: seg.to }],
              splits: (t.splits ?? []).filter((s) => s <= seg.from || s >= seg.to),
            }
          : t,
      )
    }
    setSelection(null)
  }

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const tgt = e.target as HTMLElement
      if (tgt.tagName === 'INPUT' || tgt.tagName === 'TEXTAREA' || tgt.isContentEditable) return
      if (document.querySelector('.modal-overlay')) return // no editar con un modal abierto
      if ((e.metaKey || e.ctrlKey) && (e.key === 'z' || e.key === 'Z')) {
        e.preventDefault()
        undo()
      } else if (e.key === 's' || e.key === 'S') {
        e.preventDefault()
        splitAtPlayhead()
      } else if (e.key === 'Delete' || e.key === 'Backspace') {
        e.preventDefault()
        deleteSelected()
      } else if (e.key === ' ') {
        e.preventDefault()
        playerRef.current?.toggle()
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
        e.preventDefault()
        const step = (e.shiftKey ? 1 : 0.1) * (e.key === 'ArrowLeft' ? -1 : 1)
        const total = snap.current.clips.reduce((s, c) => s + clipOutSeconds(c), 0)
        setPlayhead((p) => Math.min(total, Math.max(0, Math.round((p + step) * 10) / 10)))
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // ---- manifiesto ----

  const loadManifest = (m: Manifest) => {
    setName(m.name || 'mi-video')
    setOutputs(m.outputs?.length ? m.outputs : ['vertical'])

    const findLoaded = (ref: string) => bin.find((b) => b.media && b.name === baseName(ref))
    const refs: Array<{ name: string; kind: 'video' | 'audio' }> = m.clips.map((c) => ({
      name: baseName(c.file),
      kind: 'video',
    }))
    if (m.voice) refs.push({ name: baseName(m.voice.file), kind: 'audio' })
    if (m.music) refs.push({ name: baseName(m.music.file), kind: 'audio' })
    setBin((prev) => {
      const next = [...prev]
      for (const r of refs) if (!next.some((b) => b.name === r.name)) next.push(binPlaceholder(r.name, r.kind))
      return next
    })

    setClips(
      m.clips.map((spec) => {
        const s = clipFromSpec(spec)
        const b = findLoaded(spec.file)
        return b
          ? {
              ...s,
              media: b.media,
              url: b.url,
              duration: b.duration,
              width: b.width,
              height: b.height,
              trimOut: s.trimOut > 0 ? s.trimOut : b.duration,
            }
          : s
      }),
    )
    const loadTrack = (spec: NonNullable<Manifest['voice']>) => {
      const t = trackFromSpec(spec)
      const b = findLoaded(spec.file)
      return b ? { ...t, media: b.media, url: b.url, duration: b.duration } : t
    }
    setVoice(m.voice ? loadTrack(m.voice) : null)
    setMusic(m.music ? loadTrack(m.music) : null)
    setSelection(null)
    setPlayhead(0)
  }

  // ---- autoguardado en el navegador ----

  const AUTOSAVE_KEY = 'videassembler-autosave'

  useEffect(() => {
    try {
      const raw = localStorage.getItem(AUTOSAVE_KEY)
      if (!raw) return
      const m = JSON.parse(raw) as Manifest
      if (Array.isArray(m.clips) && (m.clips.length > 0 || m.voice || m.music)) {
        loadManifest(m)
        setRestored(true)
      }
    } catch {
      localStorage.removeItem(AUTOSAVE_KEY)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    const id = setTimeout(() => {
      if (clips.length === 0 && !voice && !music) localStorage.removeItem(AUTOSAVE_KEY)
      else localStorage.setItem(AUTOSAVE_KEY, JSON.stringify(buildManifest(name, clips, voice, music, outputs)))
    }, 400)
    return () => clearTimeout(id)
  }, [clips, voice, music, name, outputs])

  const resetProject = () => {
    localStorage.removeItem(AUTOSAVE_KEY)
    history.current = []
    setBin((prev) => {
      prev.forEach((b) => b.url && URL.revokeObjectURL(b.url))
      return []
    })
    setClips([])
    setVoice(null)
    setMusic(null)
    setSelection(null)
    setPlayhead(0)
    setName('mi-video')
    setOutputs(['vertical'])
    setRestored(false)
  }

  // ---- derivados ----

  const totalDuration = clips.reduce((s, c) => s + clipOutSeconds(c), 0)
  const totalBytes =
    clips.reduce((s, c) => s + (c.media?.size ?? 0), 0) + (voice?.media?.size ?? 0) + (music?.media?.size ?? 0)
  const totalMB = Math.round(totalBytes / (1024 * 1024))
  const has4k = clips.some((c) => Math.max(c.width, c.height) >= 2160)
  const missing = [
    ...clips.filter((c) => !c.media).map((c) => baseName(c.file)),
    ...(voice && !voice.media ? [baseName(voice.file)] : []),
    ...(music && !music.media ? [baseName(music.file)] : []),
  ].filter((v, i, arr) => arr.indexOf(v) === i)

  const selClipIndex = selection?.type === 'clip' ? clips.findIndex((c) => c.id === selection.id) : -1
  const selClip = selClipIndex >= 0 ? clips[selClipIndex] : null
  const scrub = clipAt(clips, playhead)

  return (
    <div className="editor">
      <TopBar
        name={name}
        onName={setName}
        outputs={outputs}
        onOutputs={setOutputs}
        clips={clips}
        voice={voice}
        music={music}
        missing={missing}
        onLoadManifest={loadManifest}
      />

      {restored && (
        <div className="banner banner-info">
          💾 Proyecto recuperado del autoguardado — agrega los archivos en «Archivos» para reconectarlos.
          <button className="small" onClick={() => setRestored(false)}>Entendido</button>
          <button className="small danger" onClick={resetProject}>Empezar de cero</button>
        </div>
      )}
      {(missing.length > 0 || totalBytes > 800 * 1024 * 1024 || has4k) && (
        <div className="banner">
          {missing.length > 0 && <span>⚠ Faltan archivos: {missing.join(', ')} — agrégalos en «Archivos». </span>}
          {(totalBytes > 800 * 1024 * 1024 || has4k) && (
            <span>
              ⚠ {totalBytes > 800 * 1024 * 1024 ? `Material pesado (${totalMB} MB)` : 'Hay clips 4K'} — para exportar,
              mejor guarda el manifiesto y usa el CLI.
            </span>
          )}
        </div>
      )}

      <main className="workspace">
        <MediaBin
          items={bin}
          onAddFiles={addFiles}
          onAddToTimeline={addToTimeline}
          onAssignVoice={assignVoice}
          onAssignMusic={assignMusic}
          onRemove={removeBinItem}
        />
        <PreviewPane
          clip={selClip}
          clips={clips}
          voice={voice}
          music={music}
          scrub={scrub}
          playhead={playhead}
          onPlayhead={setPlayhead}
          onClipChange={updateClip}
          playerRef={playerRef}
        />
        {selClip ? (
          <Inspector
            kind="clip"
            clip={selClip}
            index={selClipIndex}
            count={clips.length}
            onChange={(patch) => updateClip(selClip.id, patch)}
            onRemove={() => removeClip(selClip.id)}
            onDuplicate={() => duplicateClip(selClip.id)}
            onMove={(dir) => moveClip(selClipIndex, selClipIndex + dir)}
          />
        ) : selection?.type === 'voice' && voice ? (
          <Inspector
            kind="voice"
            track={voice}
            onChange={(patch) => setVoice((v) => (v ? { ...v, ...patch } : v))}
            onRemove={() => {
              setVoice(null)
              setSelection(null)
            }}
          />
        ) : selection?.type === 'music' && music ? (
          <Inspector
            kind="music"
            track={music}
            onChange={(patch) => setMusic((v) => (v ? { ...v, ...patch } : v))}
            onRemove={() => {
              setMusic(null)
              setSelection(null)
            }}
          />
        ) : (
          <Inspector kind="none" />
        )}
      </main>

      <TimelinePane
        clips={clips}
        voice={voice}
        music={music}
        selection={selection}
        playhead={playhead}
        totalDuration={totalDuration}
        totalMB={totalMB}
        onSelect={setSelection}
        onMove={moveClip}
        onScrub={setPlayhead}
      />
    </div>
  )
}
