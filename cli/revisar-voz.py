"""Detector de errores de voz: arranques fallidos, frases repetidas, repeticiones inmediatas y palabras sueltas.

Whisper sobre audio largo junta el intento fallido con la frase buena y la escribe una sola vez; por eso aquí cada frase
(tramo de habla entre pausas) se transcribe POR SEPARADO y luego se comparan entre sí.

  python3 cli/revisar-voz.py voz.wav [--rangos 0-10.85,56.9-67.1 | --ventanas ventanas.txt] [--out carpeta]

--rangos / --ventanas: solo revisar esos tramos (segundos del archivo); ventanas.txt = «nombre inicio fin» por línea
(p. ej. la ventana de cada clip dentro del micro continuo). Sin rangos se revisa todo el audio.
Salida: <out>/revision-voz.md (para leer) y revision-voz.json (para usar en el armado), con lo que se propone cortar.
"""
import argparse, difflib, json, os, re, subprocess, sys, tempfile, unicodedata, wave
from concurrent.futures import ThreadPoolExecutor
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
UMBRAL_DB, VENTANA, PAUSA = -40.0, 0.025, 0.35
MULETILLAS = {'bien', 'este', 'eh', 'em', 'mmm', 'mm', 'y', 'ok', 'okay', 'va', 'bueno', 'o sea', 'pues', 'a ver', 'ya'}
ALUCINACIONES = ('suscribete', 'gracias por ver', 'subtitulos', 'amara org', 'gracias por su atencion', 'antarctica films', 'cc por')


def norm(t):
    t = unicodedata.normalize('NFD', t.lower())
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9ñ ]+', ' ', t).split()


def leer(path):
    tmp = tempfile.mktemp(suffix='.wav')
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', path, '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', tmp], check=True)
    w = wave.open(tmp)
    a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return a, tmp


def frases(a, sr, rangos):
    """Tramos de habla (RMS > −40 dB) unidos si la pausa es < PAUSA s."""
    n = int(sr * VENTANA)
    k = len(a) // n
    db = 20 * np.log10(np.sqrt((a[:k * n].reshape(k, n) ** 2).mean(1)) + 1e-9)
    on = db > UMBRAL_DB
    out, i = [], 0
    while i < k:
        if on[i]:
            j = i
            while j < k and on[j]:
                j += 1
            x, y = i * VENTANA, j * VENTANA
            if out and x - out[-1][1] < PAUSA:
                out[-1][1] = y
            else:
                out.append([x, y])
            i = j
        else:
            i += 1
    out = [f for f in out if f[1] - f[0] > .12]
    if rangos:
        out = [[max(x, a0), min(y, b0)] for x, y in out for a0, b0 in rangos if y > a0 and x < b0]
    return [(round(x, 2), round(y, 2)) for x, y in out if y - x > .12]


def transcribe(args):
    wav, x, y, tmpdir, i = args
    p = os.path.join(tmpdir, f'f{i:04d}.wav')
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', f'{max(0, x - .08):.2f}', '-to', f'{y + .1:.2f}', '-i', wav, p], check=True)
    j = p + '.json'
    subprocess.run(['node', os.path.join(AQUI, 'transcribe.ts'), p, '--out', j], capture_output=True)
    try:
        d = json.load(open(j))
        return d.get('text', '').strip(), [(w['word'], x - .08 + w['start'], x - .08 + w['end']) for w in d.get('words', [])]
    except Exception:
        return '', []


def inicio_comun(a, b):
    n = 0
    for p, q in zip(a, b):
        if p != q:
            break
        n += 1
    return n


def revisar(F):
    """F: lista de dicts {x,y,texto,palabras,w(normalizadas)} en orden. Devuelve hallazgos."""
    H = []
    for i, f in enumerate(F):
        w = f['w']
        t = ' '.join(w)
        if any(al in t for al in ALUCINACIONES) or (f['y'] - f['x'] < .6 and t in ('gracias', '')):
            H.append(dict(tipo='ruido', i=i, motivo='tramo cortísimo o texto inventado por Whisper: ruido, golpe o respiración', corte=[f['x'], f['y']]))
            continue
        if f['y'] - f['x'] < .6:
            H.append(dict(tipo='palabra suelta', i=i, motivo=f'tramo de {f["y"] - f["x"]:.1f}s aislado («{f["texto"]}»)', corte=[f['x'], f['y']]))
            continue
        if 0 < len(w) <= 2 and (t in MULETILLAS or all(x in MULETILLAS for x in w)):
            H.append(dict(tipo='palabra suelta', i=i, motivo=f'«{f["texto"]}» suelto entre pausas'))
            continue
        # repetición inmediata dentro de la frase («y si y si», «que que»)
        for L in (3, 2, 1):
            for k in range(len(w) - 2 * L + 1):
                if w[k:k + L] == w[k + L:k + 2 * L] and (L > 1 or len(w[k]) > 2):
                    pal = f['palabras']
                    if len(pal) == len(w):
                        H.append(dict(tipo='repetición', i=i, motivo=f'repite «{" ".join(w[k:k + L])}»', corte=[round(pal[k][1], 2), round(pal[k + L][1], 2)]))
                    else:
                        H.append(dict(tipo='repetición', i=i, motivo=f'repite «{" ".join(w[k:k + L])}»'))
                    break
            else:
                continue
            break
        # arranque fallido: la frase empieza igual que alguna de las 2 siguientes (o es su prefijo)
        fallido = False
        for j in (i + 1, i + 2):
            if j >= len(F) or F[j]['x'] - f['y'] > 6:
                break
            c = inicio_comun(w, F[j]['w'])
            # parecido con el inicio de la siguiente aunque cambie una palabra («para ver en un minuto…» → «para ver un minuto…»)
            pre = difflib.SequenceMatcher(None, w, F[j]['w'][:len(w) + 1]).ratio() if len(w) >= 3 else 0
            corta = f['y'] - f['x'] < 3.0
            if c >= 3 or (c >= 2 and (c == len(w) or corta)) or (len(w) >= 2 and c >= max(2, int(.6 * len(w)))) or pre > .7:
                H.append(dict(tipo='arranque fallido', i=i, motivo=f'empieza igual que la frase siguiente («{" ".join(F[j]["w"][:c])}…»): se queda la segunda',
                              corte=[f['x'], F[j]['x']]))
                fallido = True
                break
        if not fallido and i + 1 < len(F) and F[i + 1]['x'] - f['y'] <= 6:
            # arranque fallido pegado al FINAL de la frase: «…ya hay una despedida. Ark pone tus pestañas y deja…» y la siguiente
            # vuelve a empezar «Arc pone tus pestañas…» (sin pausa antes del intento, así que queda dentro de la frase anterior)
            sig = F[i + 1]['w']
            for L in range(min(len(w) - 1, len(sig), 14), 2, -1):
                cola = w[-L:]
                if (difflib.SequenceMatcher(None, cola[0], sig[0]).ratio() > .6
                        and difflib.SequenceMatcher(None, cola, sig[:L]).ratio() > .75):
                    pal = f['palabras']
                    corte = [round(pal[len(w) - L][1], 2), F[i + 1]['x']] if len(pal) == len(w) else None
                    H.append(dict(tipo='arranque fallido', i=i, motivo=f'termina con un intento de la frase siguiente («{" ".join(cola)}»): '
                                  'se queda la siguiente', **({'corte': corte} if corte else {})))
                    fallido = True
                    break
        if not fallido:
            # toma repetida más adelante (frase casi idéntica)
            for j in range(i + 1, len(F)):
                if len(w) >= 5 and difflib.SequenceMatcher(None, w, F[j]['w']).ratio() > .8:
                    H.append(dict(tipo='toma repetida', i=i, motivo=f'casi igual a la frase de {F[j]["x"]:.1f}s: suele quedarse la última', corte=[f['x'], f['y']]))
                    break
    return H


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('audio')
    ap.add_argument('--rangos')
    ap.add_argument('--ventanas')
    ap.add_argument('--out', default='.')
    ap.add_argument('-P', type=int, default=4)
    o = ap.parse_args()
    rangos = []
    if o.rangos:
        rangos = [tuple(map(float, r.split('-'))) for r in o.rangos.split(',')]
    if o.ventanas:
        rangos += [(float(l.split()[1]), float(l.split()[2])) for l in open(o.ventanas) if l.strip()]
    a, wav = leer(o.audio)
    fr = frases(a, 16000, rangos)
    print(f'{len(fr)} frases; transcribiendo cada una por separado…', file=sys.stderr)
    tmpdir = tempfile.mkdtemp()
    with ThreadPoolExecutor(o.P) as ex:
        res = list(ex.map(transcribe, [(wav, x, y, tmpdir, i) for i, (x, y) in enumerate(fr)]))
    F = [dict(x=x, y=y, texto=t, palabras=p, w=norm(t)) for (x, y), (t, p) in zip(fr, res)]
    H = revisar(F)
    os.makedirs(o.out, exist_ok=True)
    json.dump(dict(audio=o.audio, frases=[{k: v for k, v in f.items() if k != 'w'} for f in F],
                   hallazgos=[dict(h, x=F[h['i']]['x'], y=F[h['i']]['y'], texto=F[h['i']]['texto']) for h in H]),
              open(os.path.join(o.out, 'revision-voz.json'), 'w'), indent=1, ensure_ascii=False)
    marcados = {h['i']: h for h in H}
    md = [f'# Revisión de voz · {os.path.basename(o.audio)}', '', f'{len(F)} frases revisadas, **{len(H)} posibles errores**.', '']
    if H:
        md += ['| Seg. | Tipo | Texto | Motivo | Propuesta de corte |', '|---|---|---|---|---|']
        for h in H:
            f = F[h['i']]
            c = h.get('corte')
            md.append(f'| {f["x"]:.2f}–{f["y"]:.2f} | {h["tipo"]} | {f["texto"]} | {h["motivo"]} | {f"{c[0]:.2f}–{c[1]:.2f}" if c else "revisar a mano"} |')
    md += ['', '## Todas las frases', '']
    for i, f in enumerate(F):
        md.append(f'- `{f["x"]:7.2f}–{f["y"]:7.2f}` {"⚠️ " if i in marcados else ""}{f["texto"]}')
    open(os.path.join(o.out, 'revision-voz.md'), 'w').write('\n'.join(md) + '\n')
    for h in H:
        print(f'{F[h["i"]]["x"]:7.2f}  {h["tipo"]:16s} {F[h["i"]]["texto"][:70]}')
    print(os.path.join(o.out, 'revision-voz.md'))


if __name__ == '__main__':
    main()
