"""Revisión automática antes de entregar: lo que hay que mirar antes de decir «listo».

  python3 cli/revisar-entrega.py <manifest.json> [--video final.mp4] [--base ~/Documents/Videos] [--out carpeta]

Del manifest (siempre):
  · micro-clips (< 0.6 s) que se verían como un parpadeo si no los tapa una escena
  · capas que terminan después del final, duración de voz / clips / música que no cuadran
  · capas que se enciman en tiempo y en zona (cajas del alfa a la mitad del tramo común)
Del video renderizado (con --video):
  · hoja de contacto de cada corte de clip, cada entrada/salida de capa (−0.25 s, en el corte, +0.25 s)
  · cuadros negros o blancos, «tropiezos» (dos cambios de imagen bruscos a menos de 0.5 s: un fragmento que asoma)
  · cuadros con más de 55 % de blanco puro (capa 3D que perdió el contexto WebGL)
  · audio: pico y muestras que pasan de 1.0
Salida: <out>/reporte.md + hojas de contacto; código de salida 1 si hay errores graves.
"""
import argparse, json, os, subprocess, sys
import numpy as np

W, H = 96, 170   # tamaño de análisis


def dur_clip(c):
    d = c['trimOut'] - c['trimIn'] - sum(max(0, min(k['to'], c['trimOut']) - max(k['from'], c['trimIn'])) for k in c.get('cuts') or [])
    return d / c.get('speed', 1)


def dur_pista(t):
    if not t:
        return 0
    fin = t.get('trimOut')
    if fin is None:
        return None
    return fin - t.get('trimIn', 0) - sum(max(0, min(k['to'], fin) - max(k['from'], t.get('trimIn', 0))) for k in t.get('cuts') or [])


def alfa_bbox(path, t):
    """Caja (x0,y0,x1,y1) de lo visible en una capa .webm en el segundo local t (None si vacía)."""
    r = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-c:v', 'libvpx-vp9', '-i', path, '-vf', f'trim=start={t:.2f},setpts=PTS-STARTPTS,scale=108:192,format=rgba',
                        '-frames:v', '1', '-f', 'rawvideo', '-'], capture_output=True)
    if len(r.stdout) < 108 * 192 * 4:
        return None
    a = np.frombuffer(r.stdout[:108 * 192 * 4], np.uint8).reshape(192, 108, 4)[..., 3]
    ys, xs = np.where(a > 40)
    if len(xs) == 0:
        return None
    return (xs.min() * 10, ys.min() * 10, (xs.max() + 1) * 10, (ys.max() + 1) * 10)


def inter(a, b):
    x0, y0, x1, y1 = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
    if x1 <= x0 or y1 <= y0:
        return 0.0
    return (x1 - x0) * (y1 - y0) / min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('manifest')
    ap.add_argument('--video')
    ap.add_argument('--base', default=os.path.expanduser('~/Documents/Videos'))
    ap.add_argument('--out')
    o = ap.parse_args()
    m = json.load(open(o.manifest))
    out = o.out or os.path.join(os.path.dirname(os.path.abspath(o.video or o.manifest)), 'revision')
    os.makedirs(out, exist_ok=True)
    graves, avisos, eventos = [], [], []

    # ── manifest
    t, cortes = 0.0, []
    for i, c in enumerate(m['clips']):
        d = dur_clip(c)
        if i:
            cortes.append(t)
            eventos.append((t, f'corte {i}: {os.path.basename(m["clips"][i - 1]["file"])} → {os.path.basename(c["file"])}'))
        if d < .6:
            tapado = any(ov['start'] <= t + .01 and ov['end'] >= t + d - .01 and ov.get('scale', 1) >= 1 and 'seguir' not in ov['file']
                         for ov in m.get('overlays') or [])
            (avisos if tapado else graves).append(f'micro-clip de {d:.2f}s en {t:.2f}s ({os.path.basename(c["file"])})' + (' — tapado por una capa a pantalla completa (revisar que la capa sea opaca)' if tapado else ' — se verá como parpadeo'))
        t += d
    total = t
    voz = dur_pista(m.get('voice'))
    if m.get('voice') and voz is not None and abs(voz - total) > .5:
        avisos.append(f'la voz dura {voz:.2f}s y los clips {total:.2f}s')
    ovs = m.get('overlays') or []
    for ov in ovs:
        if ov['end'] > total + .05:
            avisos.append(f'capa {os.path.basename(ov["file"])} termina en {ov["end"]:.2f}s, después del final ({total:.2f}s)')
        eventos.append((ov['start'], f'entra {os.path.basename(ov["file"])}'))
        if ov['end'] < total - .05:
            eventos.append((ov['end'], f'sale {os.path.basename(ov["file"])}'))
    # capas que se enciman (en tiempo y en zona); se ignoran pares donde una es pantalla completa opaca (se tapan a propósito)
    for i in range(len(ovs)):
        for j in range(i + 1, len(ovs)):
            a, b = ovs[i], ovs[j]
            t0, t1 = max(a['start'], b['start']), min(a['end'], b['end'])
            if t1 - t0 < .3:
                continue
            pa, pb = os.path.join(o.base, a['file']), os.path.join(o.base, b['file'])
            if not (os.path.exists(pa) and os.path.exists(pb)) or not pa.endswith('.webm'):
                continue
            mid = (t0 + t1) / 2
            ba, bb = alfa_bbox(pa, mid - a['start'] + a.get('trimIn', 0)), alfa_bbox(pb, mid - b['start'] + b.get('trimIn', 0))
            if not ba or not bb:
                continue
            completa = lambda bx: (bx[2] - bx[0]) * (bx[3] - bx[1]) > .9 * 1080 * 1920
            if completa(ba) or completa(bb):
                continue
            if inter(ba, bb) > .2:
                avisos.append(f'{os.path.basename(a["file"])} y {os.path.basename(b["file"])} se enciman de {t0:.2f} a {t1:.2f}s (zona común {inter(ba, bb):.0%})')

    # ── video
    hojas = []
    if o.video:
        r = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', o.video, '-vf', f'scale={W}:{H},format=gray', '-f', 'rawvideo', '-'], capture_output=True)
        fps = 60.0
        try:
            num, den = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate', '-of', 'csv=p=0', o.video],
                                      capture_output=True, text=True).stdout.strip().split('/')
            fps = float(num) / float(den)
        except Exception:
            pass
        F = np.frombuffer(r.stdout, np.uint8).reshape(-1, H, W).astype(np.float32)
        luma = F.mean((1, 2))
        blanco = (F > 245).mean((1, 2))
        dif = np.r_[0, np.abs(np.diff(F, axis=0)).mean((1, 2))]
        def tramos(mask, minimo):
            res, i = [], 0
            while i < len(mask):
                if mask[i]:
                    j = i
                    while j < len(mask) and mask[j]:
                        j += 1
                    if j - i >= minimo:
                        res.append((i / fps, j / fps))
                    i = j
                else:
                    i += 1
            return res
        for a, b in tramos(luma < 8, 2):
            graves.append(f'cuadros negros de {a:.2f} a {b:.2f}s')
        for a, b in tramos(luma > 247, 2):
            graves.append(f'cuadros en blanco de {a:.2f} a {b:.2f}s')
        for a, b in tramos(blanco > .55, 3):
            avisos.append(f'más de la mitad del cuadro en blanco puro de {a:.2f} a {b:.2f}s (¿capa 3D perdida?)')
        saltos = np.where(dif > 28)[0]
        vistos = set()
        for k in range(len(saltos) - 1):
            a, b = saltos[k], saltos[k + 1]
            if 2 <= b - a <= .5 * fps and a not in vistos:
                # fragmento corto entre dos cambios bruscos: tropiezo si el fragmento no se parece a lo de antes ni a lo de después
                antes, frag, despues = F[max(0, a - 2)], F[(a + b) // 2], F[min(len(F) - 1, b + 1)]
                # cambio de TODO el cuadro (otra toma), no una animación que avanza por zonas (manchas, barridos a pasos)
                cambio = lambda x, y: (np.abs(x - y) > 20).mean()
                if cambio(frag, antes) > .5 and cambio(frag, despues) > .5:
                    graves.append(f'tropiezo: un fragmento de {(b - a) / fps:.2f}s asoma entre dos cambios bruscos en {a / fps:.2f}s')
                    vistos.update((a, b))
        # audio
        r = subprocess.run(['ffmpeg', '-nostdin', '-v', 'info', '-i', o.video, '-vn', '-af', 'astats=metadata=0', '-f', 'null', '-'], capture_output=True, text=True)
        pico = [l for l in r.stderr.splitlines() if 'Peak level dB' in l]
        if pico:
            p = float(pico[-1].split(':')[-1])
            (graves if p > -0.01 else avisos if p > -0.3 else []).append(f'pico de audio {p:.2f} dBFS' + (' (satura)' if p > -0.01 else ' (muy cerca de 0)'))
        # hojas de contacto de cada evento
        eventos.sort()
        filas = []
        for k, (te, txt) in enumerate(eventos):
            cuadros = []
            for dt in (-.25, 0, .25):
                f = int(np.clip(round((te + dt) * fps), 0, len(F) - 1))
                cuadros.append(f)
            filas.append((te, txt, cuadros))
        por_hoja = 8
        for h in range(0, len(filas), por_hoja):
            nombre = os.path.join(out, f'hoja-{h // por_hoja + 1:02d}.png')
            sel = filas[h:h + por_hoja]
            expr = '+'.join(f'eq(n\\,{f})' for _, _, cs in sel for f in cs)
            subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', o.video, '-vf', f"select='{expr}',scale=180:-1,tile=3x{len(sel)}", '-frames:v', '1', '-vsync', 'vfr', nombre])
            hojas.append((nombre, sel))

    md = [f'# Revisión de entrega · {m.get("name", "")}', '', f'Duración por clips: {total:.2f}s · capas: {len(ovs)} · cortes: {len(cortes)}', '']
    md += ['## Errores', ''] + ([f'- ❌ {g}' for g in graves] or ['- ninguno']) + ['', '## Avisos', ''] + ([f'- ⚠️ {a}' for a in avisos] or ['- ninguno'])
    if hojas:
        md += ['', '## Hojas de contacto (−0.25 s · corte · +0.25 s)', '']
        for nombre, sel in hojas:
            md += [f'![]({os.path.basename(nombre)})', ''] + [f'- `{te:7.2f}s` {txt}' for te, txt, _ in sel] + ['']
    open(os.path.join(out, 'reporte.md'), 'w').write('\n'.join(md) + '\n')
    for g in graves:
        print('❌', g)
    for a in avisos:
        print('⚠️ ', a)
    print(os.path.join(out, 'reporte.md'))
    sys.exit(1 if graves else 0)


if __name__ == '__main__':
    main()
