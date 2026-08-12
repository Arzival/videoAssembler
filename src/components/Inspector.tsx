import type { ClipState, TrackState } from '../state.ts'
import { clipOutSeconds, formatTime } from '../state.ts'

interface ClipProps {
  kind: 'clip'
  clip: ClipState
  index: number
  count: number
  onChange: (patch: Partial<ClipState>) => void
  onRemove: () => void
  onDuplicate: () => void
  onMove: (dir: -1 | 1) => void
}

interface TrackProps {
  kind: 'voice' | 'music'
  track: TrackState
  onChange: (patch: Partial<TrackState>) => void
  onRemove: () => void
}

type Props = ClipProps | TrackProps | { kind: 'none' }

export function Inspector(props: Props) {
  if (props.kind === 'none') {
    return (
      <aside className="inspector">
        <div className="panel-head"><h2>Propiedades</h2></div>
        <p className="hint">
          Selecciona algo en la línea de tiempo. Para recortar: pon el cursor donde quieras y presiona{' '}
          <kbd>S</kbd>; borra el pedazo sobrante con <kbd>⌫</kbd>.
        </p>
      </aside>
    )
  }

  if (props.kind === 'clip') {
    const { clip, index, count, onChange, onRemove, onDuplicate, onMove } = props
    return (
      <aside className="inspector">
        <div className="panel-head"><h2>Clip {index + 1}</h2></div>
        <div className="insp-file" title={clip.file}>{clip.file}</div>
        <div className="insp-meta">
          {clip.width > 0 && `${clip.width}×${clip.height} · `}
          dura {formatTime(clipOutSeconds(clip))} en el video
          {(clip.trimIn > 0 || (clip.duration > 0 && clip.trimOut < clip.duration)) &&
            ` · usa ${clip.trimIn.toFixed(1)}s → ${clip.trimOut.toFixed(1)}s`}
        </div>
        {!clip.media && <p className="missing">Falta el archivo — agrégalo en «Archivos»</p>}

        <div className="insp-controls">
          <label>
            Velocidad <span className="val">×{clip.speed.toFixed(2)}</span>
            <input
              type="range"
              min={0.5}
              max={2}
              step={0.05}
              value={clip.speed}
              onChange={(e) => onChange({ speed: Number(e.target.value) })}
            />
          </label>
          <label className="check">
            <input
              type="checkbox"
              checked={clip.keepAudio}
              onChange={(e) => onChange({ keepAudio: e.target.checked })}
            />
            Conservar audio del clip
          </label>
          {clip.keepAudio && (
            <label>
              Vol. clip <span className="val">{Math.round(clip.audioVolume * 100)}%</span>
              <input
                type="range"
                min={0}
                max={2}
                step={0.01}
                value={clip.audioVolume}
                onChange={(e) => onChange({ audioVolume: Number(e.target.value) })}
              />
            </label>
          )}
        </div>

        <p className="hint">
          Recorta en la línea de tiempo: cursor + <kbd>S</kbd> corta, <kbd>⌫</kbd> borra el pedazo seleccionado.
        </p>

        <div className="insp-buttons">
          <button onClick={() => onMove(-1)} disabled={index === 0} title="Mover a la izquierda">←</button>
          <button onClick={() => onMove(1)} disabled={index === count - 1} title="Mover a la derecha">→</button>
          <button onClick={onDuplicate} title="Duplicar clip">⧉ Duplicar</button>
          <button className="danger" onClick={onRemove} title="Quitar de la línea de tiempo">✕ Quitar</button>
        </div>
      </aside>
    )
  }

  const { kind, track, onChange, onRemove } = props
  const title = kind === 'voice' ? 'Voz' : 'Música'
  return (
    <aside className="inspector">
      <div className="panel-head"><h2>{title}</h2></div>
      <div className="insp-file" title={track.file}>{track.file}</div>
      <div className="insp-meta">
        {track.duration > 0 && `archivo de ${formatTime(track.duration)}`}
        {(track.cuts?.length ?? 0) > 0 && ` · ${track.cuts.length} corte${track.cuts.length === 1 ? '' : 's'}`}
      </div>
      {!track.media && <p className="missing">Falta el archivo — agrégalo en «Archivos»</p>}
      {track.url && <audio src={track.url} controls preload="metadata" className="audio-preview" />}
      <div className="insp-controls">
        <label>
          Volumen <span className="val">{Math.round(track.volume * 100)}%</span>
          <input
            type="range"
            min={0}
            max={2}
            step={0.01}
            value={track.volume}
            onChange={(e) => onChange({ volume: Number(e.target.value) })}
          />
        </label>
      </div>
      <p className="hint">
        Recorta en la línea de tiempo: selecciona la pista, cursor + <kbd>S</kbd> corta, <kbd>⌫</kbd> borra el
        segmento seleccionado.
      </p>
      <div className="insp-buttons">
        <button className="danger" onClick={onRemove}>✕ Quitar pista</button>
      </div>
    </aside>
  )
}
