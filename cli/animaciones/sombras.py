"""Sombras: estilo para historias narradas (terror). Siluetas articuladas con contraluz sobre fondos de shader
(espacio, planeta, nubes, ojo, niebla, cosmos), grano, viñeta e interferencia en los cortes.

Cada escena es una página 1080×1920 opaca con un solo <canvas>; el runtime está en sombras.js y se incrusta
para que la página viaje sola a otras máquinas. Una escena = una función JS draw(t) con t en segundos locales.

    page(pid, dur, js, q=.5)   → escribe _html/<pid>.html
    escena(pid, ini, fin, js)  → registra la escena con tiempos del video final (para overlays.json)
"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.environ.get('SALIDA', os.path.join(AQUI, '_html', 'sombras'))
REL = os.environ.get('REL', '')
PRE = os.environ.get('PRE', '')
COLA = .12  # cada escena dura un poco más para que no asome negro entre una y la siguiente
RUNTIME = open(os.path.join(AQUI, 'sombras.js')).read()

ESCENAS = []


def page(pid, dur, js, q=.5):
    html = f'''<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=block" rel="stylesheet">
<style>html,body{{margin:0;background:#000;overflow:hidden}}canvas{{display:block;width:1080px;height:1920px}}</style></head>
<body><canvas id="c" width="1080" height="1920"></canvas>
<script>window.DUR={dur:.2f};window.ESC={{q:{q},draw:null}};</script>
<script>{RUNTIME}</script>
<script>window.ESC.draw=(t)=>{{{js}}};</script>
</body></html>'''
    os.makedirs(os.path.join(SALIDA, '_html'), exist_ok=True)
    path = os.path.join(SALIDA, '_html', f'{pid}.html')
    open(path, 'w').write(html)
    return path


def escena(pid, ini, fin, js, q=.5):
    ESCENAS.append(dict(pid=pid, ini=ini, fin=fin, js=js, q=q))


def correr(ids=None):
    """Escribe los HTML (y overlays.json si no se piden ids); captura salvo SOLO_HTML=1."""
    sel = [e for e in ESCENAS if not ids or e['pid'] in ids]
    trabajos = []
    for e in sel:
        dur = e['fin'] - e['ini'] + COLA
        h = page(e['pid'], dur, e['js'], e['q'])
        trabajos.append((h, dur, os.path.join(SALIDA, f'{PRE}{e["pid"]}.webm')))
    if not ids:
        ov = [{'file': os.path.join(REL, f'{PRE}{e["pid"]}.webm') if REL else f'{PRE}{e["pid"]}.webm',
               'start': round(e['ini'], 2), 'end': round(e['fin'] + COLA, 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for e in ESCENAS]
        json.dump(ov, open(os.path.join(SALIDA, 'overlays.json'), 'w'), indent=2)
    print(f'{len(trabajos)} escenas, {sum(d for _, d, _ in trabajos):.1f} s')
    if os.environ.get('SOLO_HTML'):
        return
    cap = os.path.join(AQUI, 'capturar.ts')

    def uno(tr):
        h, d, o = tr
        for _ in range(2):
            r = subprocess.run(['node', cap, h, f'{d:.2f}', o], capture_output=True, text=True)
            if r.returncode == 0:
                return f'ok {os.path.basename(o)}'
        return f'FALLO {os.path.basename(o)}: {r.stderr[-300:]}'
    with ThreadPoolExecutor(int(os.environ.get('P', 4))) as ex:
        for r in ex.map(uno, sorted(trabajos, key=lambda x: -x[1])):
            print(r, flush=True)


if __name__ == '__main__':
    print(__doc__)
    sys.exit(0)
