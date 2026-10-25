"""Portada automática: 3 propuestas de portada (1080×1920) con un cuadro de la toma + el titular en el estilo de la sección.

  python3 cli/portada.py <video-final.mp4> --titulo "Mis powerbanks" [--sub "Inventario #1"] --estilo bauhaus [--out final/]

Elige 3 cuadros nítidos y quietos (varianza del laplaciano alta, poco movimiento contra el cuadro vecino), separados ≥ 4 s, de
la parte del video que es toma de cámara (se saltan los cuadros que parecen escena a pantalla completa: muy planos). Sobre cada
uno pone el titular arriba con la tipografía y los colores del estilo. Salida: portada-1.png … portada-3.png.
"""
import argparse, base64, html, importlib.util, os, subprocess
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
_sp = importlib.util.spec_from_file_location('sub', os.path.join(AQUI, 'subtitulos.py'))
SUB = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(SUB)
W, H = 108, 192


def candidatos(video, n=3, excluir=()):
    r = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', video, '-vf', f'fps=2,scale={W}:{H},format=gray', '-f', 'rawvideo', '-'], capture_output=True)
    F = np.frombuffer(r.stdout, np.uint8).reshape(-1, H, W).astype(np.float32)
    lap = np.array([np.var(f[1:-1, 1:-1] * 4 - f[:-2, 1:-1] - f[2:, 1:-1] - f[1:-1, :-2] - f[1:-1, 2:]) for f in F])
    mov = np.r_[0, np.abs(np.diff(F, axis=0)).mean((1, 2))]
    textura = F.std((1, 2))
    puntos = lap / (1 + mov * 4) * (textura > 25)          # nítido, quieto y con contenido (no una escena plana)
    puntos[:2] = 0
    for a, b in excluir:                                   # tramos con capas encima (tarjetas o escenas): solo toma limpia
        puntos[int(a * 2):int(b * 2) + 1] = 0
    elegidos = []
    for i in np.argsort(-puntos):
        if puntos[i] <= 0:
            break
        # separados en el tiempo y distintos entre sí (no tres veces la misma toma)
        if all(abs(i - j) >= 8 and np.abs(F[i] - F[j]).mean() > 18 for j in elegidos):
            elegidos.append(int(i))
        if len(elegidos) == n:
            break
    return [i / 2 for i in sorted(elegidos)]


def pagina(png, titulo, sub, estilo):
    e = SUB.ESTILOS[estilo]
    img = base64.b64encode(open(png, 'rb').read()).decode()
    caja = e['caja'] or 'padding:10px 26px'
    return (f"<!doctype html><html><head><meta charset=utf-8><link href=\"https://fonts.googleapis.com/css2?{e['fonts']}&display=block\" rel=stylesheet>"
            "<style>*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1920px;overflow:hidden}"
            f"body{{background:url(data:image/png;base64,{img}) center/cover}}"
            "#t{position:absolute;left:60px;right:60px;top:300px;display:flex;flex-direction:column;align-items:flex-start;gap:22px}"
            f"#t b{{display:inline-block;font-family:{e['fam']},sans-serif;font-weight:{e['peso']};font-size:{int(e['size'] * 1.9)}px;line-height:1;"
            f"color:{e['color']};-webkit-text-stroke:{e['trazo']};paint-order:stroke fill;text-shadow:{e['sombra']};{caja}}}"
            f"#t i{{font-style:normal;display:inline-block;font-family:{e['fam']},sans-serif;font-weight:{e['peso']};font-size:{int(e['size'] * .9)}px;"
            f"color:{e['ac'] if e['acfondo'] == 'transparent' else e['color']};background:{e['acfondo'] if e['acfondo'] != 'transparent' else 'transparent'};"
            f"padding:4px 18px;text-shadow:{e['sombra']}}}</style></head><body><div id=t>"
            + ''.join(f'<b>{html.escape(l)}</b>' for l in titulo.split('|'))
            + (f'<i>{html.escape(sub)}</i>' if sub else '')
            + f"</div><script>window.__listo=document.fonts.load('{e['peso']} 80px {e['fam'].strip(chr(39))}').then(()=>document.fonts.ready).then(()=>{{"
              "for(const b of document.querySelectorAll('#t b,#t i')){let s=parseFloat(getComputedStyle(b).fontSize);"
              "while(b.getBoundingClientRect().width>960&&s>30){s-=4;b.style.fontSize=s+'px'}}})</script></body></html>")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('video')
    ap.add_argument('--titulo', required=True, help='renglones separados con |')
    ap.add_argument('--sub', default='')
    ap.add_argument('--estilo', required=True, choices=sorted(SUB.ESTILOS))
    ap.add_argument('--out')
    ap.add_argument('--manifest', help='para usar solo cuadros de toma limpia (sin capas encima)')
    o = ap.parse_args()
    excluir = []
    if o.manifest:
        import json
        excluir = [(ov['start'], ov['end']) for ov in json.load(open(o.manifest)).get('overlays') or [] if 'subtitulos' not in ov['file']]
    out = o.out or os.path.dirname(os.path.abspath(o.video))
    os.makedirs(out, exist_ok=True)
    for k, t in enumerate(candidatos(o.video, excluir=excluir), 1):
        png = os.path.join(out, f'.cuadro-{k}.png')
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', o.video, '-frames:v', '1', '-vf', 'scale=1080:1920', png], check=True)
        h = os.path.join(out, f'.portada-{k}.html')
        open(h, 'w').write(pagina(png, o.titulo, o.sub, o.estilo))
        dst = os.path.join(out, f'portada-{k}.png')
        subprocess.run(['node', os.path.join(AQUI, 'animaciones', 'foto.ts'), h, dst], check=True, capture_output=True)
        os.remove(png); os.remove(h)
        print(f'✔ {dst}  (cuadro del segundo {t:.1f})')


if __name__ == '__main__':
    main()
