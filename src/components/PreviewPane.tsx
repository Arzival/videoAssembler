import { useEffect, useRef, useState } from 'react'
import type { ClipState, TrackState } from '../state.ts'
import { clipAt, clipOutOffsetAt, clipOutSeconds, formatTime, trackSourceTimeAt } from '../state.ts'

interface Props {
  clip: ClipState | null
  clips: ClipState[]
  voice: TrackState | null
  music: TrackState | null
  /** Clip bajo el cursor del timeline + tiempo fuente equivalente */
  scrub: { clip: ClipState; index: number; src: number } | null
  playhead: number
  onPlayhead: (t: number) => void
  onClipChange: (id: string, patch: Partial<ClipState>) => void
}

export function PreviewPane({ clip, clips, voice, music, scrub, playhead, onPlayhead, onClipChange }: Props) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const voiceRef = useRef<HTMLAudioElement>(null)
  const musicRef = useRef<HTMLAudioElement>(null)
  const [seq, setSeq] = useState<number | null>(null) // índice del clip sonando al reproducir la timeline
  const [time, setTime] = useState(0)
  const startSrcRef = useRef<{ index: number; src: number } | null>(null)

  const active = seq != null ? (clips[seq] ?? null) : (scrub?.clip ?? clip)

  // el cursor del timeline manda cuando no se está reproduciendo
  useEffect(() => {
    const v = videoRef.current
    if (v && seq == null && scrub && active?.id === scrub.clip.id) {
      v.currentTime = scrub.src
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [scrub?.clip.id, scrub?.src])

  const stopAll = () => {
    setSeq(null)
    startSrcRef.current = null
    videoRef.current?.pause()
    voiceRef.current?.pause()
    musicRef.current?.pause()
  }

  /** Reproduce el segmento del clip `c` (desde startSrc si se indica), saltando cortes */
  const playClip = (c: ClipState, onEnd: () => void, startSrc?: number) => {
    const v = videoRef.current
    if (!v) return
    const cuts = [...(c.cuts ?? [])].sort((a, b) => a.from - b.from)
    v.playbackRate = c.speed
    v.muted = !c.keepAudio
    v.volume = Math.min(1, c.audioVolume)
    v.currentTime = startSrc ?? c.trimIn
    const onTime = () => {
      const t = v.currentTime
      const cut = cuts.find((x) => t >= x.from && t < x.to)
      if (cut) {
        v.currentTime = cut.to
        return
      }
      if (t >= (c.trimOut || c.duration)) {
        v.removeEventListener('timeupdate', onTime)
        v.pause()
        onEnd()
      }
    }
    v.addEventListener('timeupdate', onTime)
    void v.play()
  }

  useEffect(() => {
    if (seq == null) {
      voiceRef.current?.pause()
      musicRef.current?.pause()
      return
    }
    const c = clips[seq]
    if (!c || !c.url) {
      setSeq(null)
      return
    }
    const start = startSrcRef.current?.index === seq ? startSrcRef.current.src : undefined
    startSrcRef.current = null
    const id = requestAnimationFrame(() => {
      playClip(c, () => setSeq((s) => (s != null && s + 1 < clips.length ? s + 1 : null)), start)
    })
    return () => cancelAnimationFrame(id)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [seq])

  /** Arranca voz y música en el punto del timeline T (mejor esfuerzo) */
  const startAudioAt = (T: number) => {
    for (const [ref, track] of [
      [voiceRef, voice],
      [musicRef, music],
    ] as const) {
      const el = ref.current
      if (!el || !track) continue
      const src = trackSourceTimeAt(track, T)
      if (src == null) continue // la pista ya terminó antes de este punto
      el.currentTime = src
      el.volume = Math.min(1, track.volume)
      void el.play()
    }
  }

  const playAll = () => {
    if (clips.length === 0 || clips.some((c) => !c.url)) return
    stopAll()
    const total = clips.reduce((s, c) => s + clipOutSeconds(c), 0)
    const from = playhead >= total - 0.05 ? 0 : playhead // cursor al final → desde el inicio
    const hit = clipAt(clips, from)
    if (hit) startSrcRef.current = { index: hit.index, src: hit.src }
    startAudioAt(from)
    setSeq(hit?.index ?? 0)
  }

  const playSegment = () => {
    const target = active
    if (!target?.url) return
    stopAll()
    playClip(target, () => {})
  }

  const handleTimeUpdate = (t: number) => {
    setTime(t)
    if (seq != null && active) {
      const base = clips.slice(0, seq).reduce((s, c) => s + clipOutSeconds(c), 0)
      onPlayhead(base + clipOutOffsetAt(active, t))
    }
  }

  const segDuration = active ? clipOutSeconds(active) : 0

  return (
    <section className="preview-pane">
      <div className="preview-stage">
        {active?.url ? (
          <video
            key={active.id}
            ref={videoRef}
            src={active.url}
            className="preview-video"
            playsInline
            preload="metadata"
            onClick={seq == null ? playAll : stopAll}
            onTimeUpdate={(e) => handleTimeUpdate(e.currentTarget.currentTime)}
            onLoadedMetadata={(e) => {
              const v = e.currentTarget
              if (seq == null && active.duration === 0) {
                onClipChange(active.id, {
                  duration: v.duration,
                  width: v.videoWidth,
                  height: v.videoHeight,
                  trimOut: active.trimOut > 0 ? Math.min(active.trimOut, v.duration) : v.duration,
                })
              } else if (seq == null && scrub && active.id === scrub.clip.id) {
                v.currentTime = scrub.src
              }
            }}
          />
        ) : (
          <div className="preview-empty">
            {clips.length === 0
              ? 'Agrega archivos y mándalos a la línea de tiempo'
              : 'Mueve el cursor en la línea de tiempo o selecciona un clip'}
          </div>
        )}
      </div>
      <div className="preview-controls">
        {seq == null ? (
          <button
            className="primary"
            onClick={playAll}
            disabled={clips.length === 0 || clips.some((c) => !c.url)}
            title="Reproduce desde el cursor rojo, con voz y música (aprox.)"
          >
            ▶ Reproducir
          </button>
        ) : (
          <button className="primary" onClick={stopAll}>■ Detener</button>
        )}
        <button onClick={playSegment} disabled={!active?.url || seq != null} title="Reproduce solo el clip actual">
          ▶ Clip
        </button>
        <span className="preview-time">
          {formatTime(seq != null ? playhead : time)}
          {active && seq == null ? ` · clip: ${formatTime(segDuration)}` : ''}
          {seq != null ? ` · clip ${seq + 1}/${clips.length}` : ''}
        </span>
      </div>
      {voice?.url && <audio ref={voiceRef} src={voice.url} preload="auto" />}
      {music?.url && <audio ref={musicRef} src={music.url} preload="auto" />}
    </section>
  )
}
