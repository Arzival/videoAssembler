"""Subtítulos palabra por palabra en el estilo de cada sección (PRUEBA DE LOOK: se activan por video cuando se aprueben).

  python3 cli/subtitulos.py <manifest.json> --estilo plastilina|bauhaus|recorte|escritorio|sombras
                           [--audio voz-final.wav | --video render.mp4] [--base ~/Documents/Videos] [--out carpeta] [--manifest-out x.json]

1. Transcribe el audio del video FINAL (del render o de la voz ya recortada) por frases, cada una por separado
   (así Whisper no se cicla en audios largos), con tiempos por palabra.
2. Agrupa en frases cortas (≤ 3 palabras, corta en pausas > 0.3 s y en puntuación) y corrige términos con
   cli/subtitulos-diccionario.json.
3. Arma UNA capa HTML transparente con todo el video: la palabra que suena se resalta con el color del estilo; se esconden
   durante las escenas a pantalla completa (capas cuyo contenido llena el cuadro) para no encimarse con su texto grande.
4. La graba con capturar.ts (a 10 pasos por segundo: la palabra cambia como mucho cada 0.1 s) y, con --manifest-out,
   escribe una copia del manifiesto con la capa agregada al final (encima de todo).
Zona: tercio inferior (y ≈ 1330–1520), arriba de los botones de TikTok y debajo de las tarjetas.
"""
import argparse, html, importlib.util, json, os, re, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
_sp = importlib.util.spec_from_file_location('rv', os.path.join(AQUI, 'revisar-voz.py'))
RV = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(RV)
_sp = importlib.util.spec_from_file_location('re_', os.path.join(AQUI, 'revisar-entrega.py'))
RE = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(RE)

ESTILOS = {
    # fuente, tamaño, color del texto, contorno/caja, color de la palabra que suena, fondo de la palabra
    'plastilina': dict(fonts='family=Fredoka:wght@600;700', fam="'Fredoka'", peso=700, size=74, color='#ffffff',
                       caja='', sombra='0 6px 0 #2b2350, 0 0 0 transparent', trazo='10px #2b2350', ac='#ffd84d', acfondo='transparent'),
    'bauhaus': dict(fonts='family=Jost:wght@800', fam="'Jost'", peso=800, size=72, color='#151515',
                    caja='background:#efe8da;padding:6px 22px;box-shadow:8px 8px 0 #151515', sombra='none', trazo='0', ac='#151515', acfondo='#f3c11b'),
    'recorte': dict(fonts='family=Archivo:wdth,wght@100,900', fam="'Archivo'", peso=900, size=76, color='#171513',
                    caja='background:#f3ecdf;padding:4px 20px;transform:rotate(-1.5deg)', sombra='none', trazo='0', ac='#171513', acfondo='#ffe14a'),
    'escritorio': dict(fonts='family=VT323', fam="'VT323'", peso=400, size=86, color='#0a0a0a',
                       caja='background:#ffffff;border:4px solid #0a0a0a;box-shadow:6px 6px 0 #0a0a0a;padding:2px 22px', sombra='none', trazo='0',
                       ac='#ffffff', acfondo='#0a1f8f'),
    'sombras': dict(fonts='family=Share+Tech+Mono', fam="'Share Tech Mono'", peso=400, size=64, color='#d9d4c7',
                    caja='', sombra='0 0 18px #000, 0 0 4px #000', trazo='0', ac='#ff3b2f', acfondo='transparent'),
}


def palabras_finales(audio):
    """Palabras con tiempos del video final, transcribiendo cada frase por separado."""
    a, wav = RV.leer(audio)
    fr = RV.frases(a, 16000, [])
    tmp = tempfile.mkdtemp()
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(RV.transcribe, [(wav, x, y, tmp, i) for i, (x, y) in enumerate(fr)]))
    out = []
    for _, ws in res:
        for w, x, y in ws:
            w = w.strip()
            if w and not any(al in RV.norm(w) for al in ('suscribete',)):
                out.append([w, max(0.0, x), y])
    out.sort(key=lambda p: p[1])
    return out


def corrige(ws):
    """Términos que Whisper escribe mal (cli/subtitulos-diccionario.json: «palabra en minúsculas» → «cómo va»)."""
    dic = os.path.join(AQUI, 'subtitulos-diccionario.json')
    d = json.load(open(dic)) if os.path.exists(dic) else {}
    for p in ws:
        m = re.match(r'^([¿¡"«(]*)(.*?)([.,;:?!"»)]*)$', p[0])
        if m and m.group(2).lower() in d:
            p[0] = m.group(1) + d[m.group(2).lower()] + m.group(3)
    return ws


def grupos(ws):
    g, cur = [], []
    for i, p in enumerate(ws):
        if cur and (len(cur) >= 3 or p[1] - cur[-1][2] > .3 or re.search(r'[.,;:?!¿¡]$', cur[-1][0])):
            g.append(cur); cur = []
        cur.append(p)
    if cur:
        g.append(cur)
    return [dict(ini=c[0][1], fin=min(c[-1][2] + .3, (g[k + 1][0][1] if k + 1 < len(g) else c[-1][2] + .3)),
                 w=[(p[0], p[1], p[2]) for p in c]) for k, c in enumerate(g)]


def pagina(G, ocultar, estilo, dur):
    e = ESTILOS[estilo]
    data = json.dumps([dict(i=round(g['ini'], 2), f=round(g['fin'], 2), w=[[html.escape(w), round(a, 2), round(b, 2)] for w, a, b in g['w']]) for g in G],
                      ensure_ascii=False)
    css = (f"*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden;background:transparent}}"
           f"#s{{position:absolute;left:60px;right:60px;top:1330px;height:200px;display:flex;align-items:center;justify-content:center;text-align:center}}"
           f"#s span.l{{display:inline-block;font-family:{e['fam']},sans-serif;font-weight:{e['peso']};font-size:{e['size']}px;line-height:1.05;color:{e['color']};"
           f"-webkit-text-stroke:{e['trazo']};paint-order:stroke fill;text-shadow:{e['sombra']};{e['caja']}}}"
           f"#s i{{font-style:normal;padding:0 .08em;border-radius:.12em}}#s i.on{{color:{e['ac']};background:{e['acfondo']}}}")
    js = (f"const G={data},O={json.dumps(ocultar)};const el=document.getElementById('s');let ult=-2;"
          "window.__cps=10;window.__seek=s=>{s=Math.floor(s*10+1e-6)/10;"
          "if(O.some(([a,b])=>s>=a&&s<b)){el.innerHTML='';ult=-2;return}"
          "const k=G.findIndex(g=>s>=g.i&&s<g.f);if(k<0){el.innerHTML='';ult=-2;return}"
          "const g=G[k];let on=-1;g.w.forEach(([w,a],j)=>{if(s>=a-.05)on=j});"
          "el.innerHTML='<span class=l>'+g.w.map(([w],j)=>`<i class=\"${j===on?'on':''}\">${w}</i>`).join(' ')+'</span>'};"
          f"window.__listo=document.fonts.load('{e['peso']} 80px {e['fam'].strip(chr(39))}').then(()=>document.fonts.ready);window.__seek(0);")
    return (f"<!doctype html><html><head><meta charset=utf-8><link href=\"https://fonts.googleapis.com/css2?{e['fonts']}&display=block\" rel=stylesheet>"
            f"<style>{css}</style></head><body><div id=s></div><script>{js}</script></body></html>")


def pantallas_completas(m, base):
    """Tramos donde una capa llena el cuadro (escena a pantalla completa): ahí no van subtítulos."""
    out = []
    for ov in m.get('overlays') or []:
        p = os.path.join(base, ov['file'])
        if not p.endswith('.webm') or not os.path.exists(p) or ov['end'] - ov['start'] < .5:
            continue
        mid = (ov['end'] - ov['start']) / 2 + ov.get('trimIn', 0)
        bx = RE.alfa_bbox(p, mid)
        if bx and (bx[2] - bx[0]) * (bx[3] - bx[1]) > .9 * 1080 * 1920:
            out.append([round(ov['start'], 2), round(ov['end'], 2)])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('manifest')
    ap.add_argument('--estilo', required=True, choices=sorted(ESTILOS))
    ap.add_argument('--audio')
    ap.add_argument('--video')
    ap.add_argument('--base', default=os.path.expanduser('~/Documents/Videos'))
    ap.add_argument('--out')
    ap.add_argument('--manifest-out')
    o = ap.parse_args()
    m = json.load(open(o.manifest))
    fuente = o.audio or o.video
    if not fuente:
        sys.exit('Hace falta --audio (voz final) o --video (render) para tener los tiempos del video final')
    dur = RE.dur_clip
    total = sum(dur(c) for c in m['clips'])
    out = o.out or os.path.join(os.path.dirname(os.path.abspath(o.manifest)), 'subtitulos')
    os.makedirs(out, exist_ok=True)
    cache = os.path.join(out, 'palabras.json')
    firma = [os.path.abspath(fuente), os.path.getmtime(fuente)]
    if os.path.exists(cache) and json.load(open(cache)).get('fuente') == firma:
        ws = json.load(open(cache))['palabras']   # misma fuente: no se vuelve a transcribir
    else:
        ws = palabras_finales(fuente)
        json.dump(dict(fuente=firma, palabras=ws), open(cache, 'w'), ensure_ascii=False)
    ws = corrige(ws)
    G = grupos(ws)
    oc = pantallas_completas(m, o.base)
    h = os.path.join(out, f'subtitulos-{o.estilo}.html')
    open(h, 'w').write(pagina(G, oc, o.estilo, total))
    json.dump(dict(grupos=G, ocultar=oc), open(os.path.join(out, f'subtitulos-{o.estilo}.json'), 'w'), ensure_ascii=False, indent=1)
    webm = os.path.join(out, f'subtitulos-{o.estilo}.webm')
    r = subprocess.run(['node', os.path.join(AQUI, 'animaciones', 'capturar.ts'), h, f'{total:.2f}', webm], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr[-800:])
    if o.manifest_out:
        rel = os.path.relpath(webm, o.base)
        m2 = dict(m, name=os.path.splitext(os.path.basename(o.manifest_out))[0],
                  overlays=(m.get('overlays') or []) + [dict(file=rel, start=0, end=round(total, 2), trimIn=0, scale=1, position='center')])
        json.dump(m2, open(o.manifest_out, 'w'), indent=2, ensure_ascii=False)
        print(o.manifest_out)
    print(f'{len(ws)} palabras en {len(G)} grupos; ocultos en {len(oc)} tramos de pantalla completa')


if __name__ == '__main__':
    main()
