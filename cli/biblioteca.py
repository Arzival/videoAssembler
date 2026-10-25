"""Biblioteca de rellenos: catálogo de las tomas sueltas (p. ej. ~/Documents/Videos/ayuda) para elegir rellenos sin adivinar.

  python3 cli/biblioteca.py catalogar <carpeta>          crea/actualiza <carpeta>/catalogo.json + miniaturas en <carpeta>/.biblioteca/
  python3 cli/biblioteca.py hoja <carpeta>               hoja de contacto de todas las tomas (.biblioteca/hoja.jpg) para describirlas
  python3 cli/biblioteca.py buscar <carpeta> <texto>     tomas cuya descripción o temas coinciden, con avisos de calidad

Por toma: resolución en pantalla (con rotación), fps, HDR/SDR, duración, fecha, orientación y avisos («1080p: sin margen para
recortar», «30 fps», «HDR», «horizontal»). Los campos «descripcion» y «temas» se escriben a mano (o los llena Claude viendo la
hoja) y se conservan al volver a catalogar.
"""
import json, os, subprocess, sys
from datetime import datetime

EXT = ('.mov', '.mp4', '.m4v')


def probe(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                        'stream=width,height,r_frame_rate,color_transfer,codec_name:stream_side_data=rotation:format=duration:format_tags=com.apple.quicktime.creationdate,creation_time',
                        '-of', 'json', p], capture_output=True, text=True)
    d = json.loads(r.stdout or '{}')
    s = (d.get('streams') or [{}])[0]
    w, h = s.get('width', 0), s.get('height', 0)
    rot = next((abs(int(x.get('rotation', 0))) for x in s.get('side_data_list', []) if 'rotation' in x), 0)
    if rot in (90, 270):
        w, h = h, w
    num, den = (s.get('r_frame_rate') or '0/1').split('/')
    fps = round(float(num) / float(den or 1), 2) if float(den or 1) else 0
    tags = (d.get('format') or {}).get('tags') or {}
    trc = s.get('color_transfer', '')
    return dict(ancho=w, alto=h, fps=fps, hdr=trc in ('arib-std-b67', 'smpte2084'), codec=s.get('codec_name'),
                duracion=round(float((d.get('format') or {}).get('duration', 0)), 2),
                fecha=tags.get('com.apple.quicktime.creationdate') or tags.get('creation_time', ''))


def avisos(c):
    a = []
    corto = min(c['ancho'], c['alto'])
    if corto and corto < 2000:
        a.append(f'{corto}p: sin margen para recortar (se ve menos nítido que las tomas 4K)')
    if c['fps'] and c['fps'] < 50:
        a.append(f'{c["fps"]:g} fps (las tomas actuales van a 60)')
    if c['hdr']:
        a.append('HDR (el render lo pasa a SDR solo)')
    if c['ancho'] > c['alto']:
        a.append('horizontal (en vertical se recorta mucho)')
    return a


def catalogar(carpeta):
    cat_p = os.path.join(carpeta, 'catalogo.json')
    viejo = {c['archivo']: c for c in json.load(open(cat_p))['tomas']} if os.path.exists(cat_p) else {}
    mini = os.path.join(carpeta, '.biblioteca')
    os.makedirs(mini, exist_ok=True)
    tomas = []
    for raiz, dirs, files in os.walk(carpeta):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in sorted(files):
            if not f.lower().endswith(EXT):
                continue
            p = os.path.join(raiz, f)
            rel = os.path.relpath(p, carpeta)
            c = dict(archivo=rel, **probe(p))
            c['orientacion'] = 'vertical' if c['alto'] >= c['ancho'] else 'horizontal'
            c['avisos'] = avisos(c)
            c['descripcion'] = viejo.get(rel, {}).get('descripcion', '')
            c['temas'] = viejo.get(rel, {}).get('temas', [])
            jpg = os.path.join(mini, rel.replace('/', '__') + '.jpg')
            if not os.path.exists(jpg) or os.path.getmtime(jpg) < os.path.getmtime(p):
                d = c['duracion'] or 1
                subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y'] + sum([['-ss', f'{d * k:.2f}', '-i', p] for k in (.2, .5, .8)], []) +
                               ['-filter_complex', '[0]scale=-2:320[a];[1]scale=-2:320[b];[2]scale=-2:320[c];[a][b][c]hstack=3', '-frames:v', '1', jpg])
            c['miniatura'] = os.path.relpath(jpg, carpeta)
            tomas.append(c)
    json.dump(dict(actualizado=datetime.now().isoformat(timespec='seconds'), tomas=tomas), open(cat_p, 'w'), indent=1, ensure_ascii=False)
    print(f'{len(tomas)} tomas → {cat_p}')
    for c in tomas:
        print(f'  {c["archivo"]:32s} {c["ancho"]}×{c["alto"]} {c["fps"]:g}fps {c["duracion"]:6.1f}s  {"; ".join(c["avisos"]) or "ok"}')


def hoja(carpeta):
    """Hoja de contacto con el nombre de cada toma (PIL: el ffmpeg de Homebrew no trae drawtext)."""
    from PIL import Image, ImageDraw
    cat = json.load(open(os.path.join(carpeta, 'catalogo.json')))['tomas']
    filas = []
    for c in cat:
        im = Image.open(os.path.join(carpeta, c['miniatura'])).convert('RGB')
        im = im.resize((720, int(im.height * 720 / im.width)))
        d = ImageDraw.Draw(im)
        txt = f'{os.path.basename(c["archivo"])}  {c["ancho"]}x{c["alto"]} {c["fps"]:g}fps'
        d.rectangle([0, 0, 8 + 7 * len(txt), 20], fill=(0, 0, 0))
        d.text((4, 4), txt, fill=(255, 255, 255))
        filas.append(im)
    out = Image.new('RGB', (720, sum(f.height for f in filas)))
    y = 0
    for f in filas:
        out.paste(f, (0, y)); y += f.height
    dst = os.path.join(carpeta, '.biblioteca', 'hoja.jpg')
    out.save(dst, quality=85)
    print(dst)


def buscar(carpeta, texto):
    cat = json.load(open(os.path.join(carpeta, 'catalogo.json')))['tomas']
    q = [w for w in texto.lower().split() if len(w) > 2]
    res = []
    for c in cat:
        campo = (c.get('descripcion', '') + ' ' + ' '.join(c.get('temas', []))).lower()
        p = sum(1 for w in q if w in campo)
        if p:
            res.append((p, c))
    for p, c in sorted(res, key=lambda x: -x[0]):
        print(f'{c["archivo"]:32s} {c.get("descripcion", "")}' + (f'\n    ⚠ {"; ".join(c["avisos"])}' if c['avisos'] else ''))
    if not res:
        print('sin coincidencias (¿falta describir las tomas? python3 cli/biblioteca.py hoja <carpeta>)')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    {'catalogar': lambda: catalogar(sys.argv[2]), 'hoja': lambda: hoja(sys.argv[2]),
     'buscar': lambda: buscar(sys.argv[2], ' '.join(sys.argv[3:]))}.get(sys.argv[1], lambda: sys.exit(__doc__))()
