"""Plantillas del estilo «Recorte» (El Log) para el motor.

Todas las plantillas de alto nivel (titular, cifra, comparacion, lista, cita, logo_dato, antes_despues) se expanden a la
plantilla genérica «fases»: una lista de fases (grupos que entran y se barren) con piezas de papel y objetos 3D de cartón.
Las piezas llaman a las mismas funciones de recorte.py que los guiones hechos a mano, así que el resultado es el mismo.
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import recorte as K
import ellog_gloss as G

TOP = 330          # primer renglón útil (debajo de la cabecera)

# objetos 3D de papel y cartón (los mismos de El Log #09)
LIB3D = r"""
const medalla=(d,s,bg,fg='#ffffff')=>{const G=new THREE.Group();
 const disc=new THREE.Mesh(new THREE.CylinderGeometry(P.u(s/2),P.u(s/2),P.u(18),56),[P.papel('#f3ede0'),P.papel(bg),P.papel(bg)]);disc.rotation.x=Math.PI/2;G.add(disc);
 const gl=P.recorte(d,s*.6,fg,10);gl.position.z=P.u(15);G.add(gl);return P.sombra(G)};
const appicon=(d,s,bg,fg='#ffffff')=>{const G=new THREE.Group();G.add(P.caja(s,s,s*.14,bg,false));
 const gl=P.recorte(d,s*.58,fg,12);gl.position.z=P.u(s*.07+8);G.add(gl);return P.sombra(G)};
const maletin=(w)=>{const G=new THREE.Group(),h=w*.68,d=w*.3;G.add(P.caja(w,h,d,'#a0662f',false));
 const fr=new THREE.Mesh(new THREE.BoxGeometry(P.u(w*1.01),P.u(h*.08),P.u(d*1.02)),P.papel('#6b4220'));fr.position.y=P.u(h*.18);G.add(fr);
 const asa=new THREE.Mesh(new THREE.TorusGeometry(P.u(w*.16),P.u(w*.035),10,28,Math.PI),P.papel('#6b4220'));asa.position.y=P.u(h/2);G.add(asa);
 for(const x of[-1,1]){const c=new THREE.Mesh(new THREE.BoxGeometry(P.u(w*.08),P.u(h*.12),P.u(8)),P.papel('#e2b74a'));c.position.set(P.u(x*w*.3),P.u(h*.18),P.u(d/2+3));G.add(c)}
 return P.sombra(G)};
const sello3=(w)=>{const G=new THREE.Group();
 const base=new THREE.Mesh(new THREE.BoxGeometry(P.u(w),P.u(w*.22),P.u(w*.6)),P.papel('#3a3a42'));G.add(base);
 const hule=new THREE.Mesh(new THREE.BoxGeometry(P.u(w*.94),P.u(w*.06),P.u(w*.56)),P.papel('#e3342a'));hule.position.y=P.u(-w*.14);G.add(hule);
 const m=new THREE.Mesh(new THREE.CylinderGeometry(P.u(w*.1),P.u(w*.14),P.u(w*.55),20),P.papel('#c9a26b'));m.position.y=P.u(w*.38);G.add(m);
 const k=new THREE.Mesh(new THREE.SphereGeometry(P.u(w*.19),20,14),P.papel('#c9a26b'));k.position.y=P.u(w*.72);G.add(k);return P.sombra(G)};
const lupa=(r)=>{const G=new THREE.Group();G.add(new THREE.Mesh(new THREE.TorusGeometry(P.u(r),P.u(r*.17),14,48),P.papel('#2457e6')));
 G.add(new THREE.Mesh(new THREE.CircleGeometry(P.u(r),48),P.papel('#dfe8ff',{transparent:true,opacity:.5})));
 const hd=new THREE.Mesh(new THREE.BoxGeometry(P.u(r*.34),P.u(r*1.25),P.u(r*.32)),P.papel('#c9a26b'));hd.position.set(P.u(r*1.18),P.u(-r*1.18),0);hd.rotation.z=Math.PI/4;G.add(hd);return P.sombra(G)};
"""


def caja(txt, size=96, extra=''):
    return f'<div style="font-weight:900;font-stretch:62%;font-size:{size}px;line-height:.88;text-transform:uppercase;{extra}">{txt}</div>'


def ser(txt, size=48, extra=''):
    return f'<div class="ser" style="font-size:{size}px;line-height:1.05;{extra}">{txt}</div>'


def _g(p, k, d=None):
    return p.get(k, d)


# ───────── piezas de papel: tipo → HTML (mismos nombres de argumentos que recorte.py, «en» = cuándo entra, «sale» = cuándo se va)
def pieza(p, A):
    t = p['tipo']
    if t == 'titular':
        return K.titular(p['lineas'], A, p['en'], x=_g(p, 'sale'), top=_g(p, 'top', TOP), size=_g(p, 'size', 150), align=_g(p, 'align', 'left'),
                         seed=_g(p, 'seed', 1), step=_g(p, 'step', .075), color=_g(p, 'color'))
    if t == 'tacha':
        return K.tacha(p['x'], p['y'], p['w'], A, p['en'], color=_g(p, 'color', 'var(--rojo)'), grosor=_g(p, 'grosor', 14), seed=_g(p, 'seed', 6))
    if t == 'subraya':
        return K.subraya(p['x'], p['y'], p['w'], A, p['en'], color=_g(p, 'color', 'var(--rojo)'), grosor=_g(p, 'grosor', 10), seed=_g(p, 'seed', 5),
                         doble=_g(p, 'doble', False))
    if t == 'circulo':
        return K.circulo(p['cx'], p['cy'], p['w'], p['h'], A, p['en'], color=_g(p, 'color', 'var(--rojo)'), grosor=_g(p, 'grosor', 9), seed=_g(p, 'seed', 3))
    if t == 'flecha':
        return K.flecha(p['x1'], p['y1'], p['x2'], p['y2'], A, p['en'], color=_g(p, 'color', 'var(--rojo)'), curva=_g(p, 'curva', .25), grosor=_g(p, 'grosor', 9))
    if t == 'recorte':
        html = p.get('html') or (caja(p['caja'], _g(p, 'size', 96), _g(p, 'estilo', '')) if 'caja' in p else ser(p['ser'], _g(p, 'size', 48)))
        return K.recorte(p['x'], p['y'], p['w'], p['h'], html, A, p['en'], sale=_g(p, 'sale'), rot=_g(p, 'rot', 0.0), seed=_g(p, 'seed', 11),
                         cinta=_g(p, 'cinta', True), pad=_g(p, 'pad'))
    if t == 'nota':
        return K.nota(p['x'], p['y'], p['html'], A, p['en'], sale=_g(p, 'sale'), rot=_g(p, 'rot', -3.0), w=_g(p, 'w', 330), color=_g(p, 'color', '#ffe46b'),
                      size=_g(p, 'size', 54))
    if t == 'sello':
        return K.sello(p['x'], p['y'], p['texto'], A, p['en'], rot=_g(p, 'rot', -8.0), size=_g(p, 'size', 64), color=_g(p, 'color'))
    if t == 'ticket':
        return K.ticket(p['x'], p['y'], p['w'], [tuple(l) for l in p['lineas']], A, rot=_g(p, 'rot', 0.0), sale=_g(p, 'sale'), size=_g(p, 'size', 34))
    if t == 'mano':
        return K.mano(p['x'], p['y'], p['texto'], A, p['en'], size=_g(p, 'size', 58), color=_g(p, 'color'), rot=_g(p, 'rot', -4.0))
    if t == 'numero':
        keys = [(0, p.get('de', 0)), (p['en'], p['a'], p.get('dur', .9))]
        return K.numero(p['x'], p['y'], K.N(keys, f=_g(p, 'formato', 'c'), suf=_g(p, 'suf', ''), pre=_g(p, 'pre', '')), A, p['en'] - .1,
                        size=_g(p, 'size', 300), color=_g(p, 'color'))
    if t == 'palomita':
        return K.palomita(p['x'], p['y'], p['s'], A, p['en'], color=_g(p, 'color', 'var(--verde)'), grosor=_g(p, 'grosor', 16))
    if t == 'lista':   # renglones escritos a mano que aparecen uno por uno dentro de un recorte
        filas = ''.join(f'<div class="fade0" style="--d:{A(en)};font-family:Caveat;font-weight:700;font-size:{_g(p, "size", 54)}px;line-height:1.15">'
                        f'{_g(p, "vineta", "☑")} {tx}</div>' for tx, en in p['items'])
        return K.recorte(p['x'], p['y'], p['w'], p['h'], filas, A, p['en'], sale=_g(p, 'sale'), rot=_g(p, 'rot', -2.0), seed=_g(p, 'seed', 22),
                         pad=_g(p, 'pad', '30px 40px'))
    if t == 'html':
        return p['html']
    raise ValueError(f'pieza desconocida: {t}')


# ───────── objetos 3D: tipo → constructor JS
def _ctor(o):
    t, s = o['tipo'], o.get('tam', 260)
    if t == 'medalla':
        return f"medalla(SVG[{json.dumps(o['logo'])}],{s},{json.dumps(o.get('fondo', '#d97757'))},{json.dumps(o.get('tinta', '#ffffff'))})", s
    if t == 'appicon':
        return f"appicon(SVG[{json.dumps(o['logo'])}],{s},{json.dumps(o.get('fondo', '#d97757'))},{json.dumps(o.get('tinta', '#ffffff'))})", s
    if t == 'maletin':
        return f'maletin({s})', s * .7
    if t == 'sello3':
        return f'sello3({s})', s * .9
    if t == 'lupa':
        return f'lupa({s})', s * 3.1
    raise ValueError(f'objeto 3D desconocido: {t}')


def js3d(objetos, raw=''):
    """Capa 3D: objetos declarados (suben como pop-up, se mecen y se barren con su fase) o, como vía de escape, JS propio en
    `raw` (crea objetos y devuelve la función t=>{…}; puede usar medalla/appicon/maletin/sello3/lupa y SVG[logo])."""
    if not objetos and not raw:
        return None
    if objetos and raw:
        raise ValueError('una escena usa «objetos» o «js3d», no los dos')
    import re
    logos = sorted({o['logo'] for o in objetos if 'logo' in o} | set(re.findall(r'SVG\.(\w+)', raw or '')) | set(re.findall(r'SVG\["(\w+)"\]', raw or '')))
    cab = 'const SVG=' + json.dumps({n: G.svgpath(n) for n in logos}) + ';' + LIB3D
    if raw:
        return cab + raw
    crea, act = [], []
    for i, o in enumerate(objetos):
        ctor, alto = _ctor(o)
        crea.append(f"const o{i}=P.bisagra({ctor},{o.get('alto', round(alto))});P.at(o{i},{o['x']},{o['y']},{o.get('z', 1.6)});o{i}.rotation.z={o.get('rot', 0)};scene.add(o{i});")
        a = f"P.sube(o{i},t,{o['en']},.6);o{i}.userData.o.rotation.y={o.get('giro', .25)}*Math.sin(t*{o.get('vel', 1.3)}+{i});"
        if o.get('sale') is not None:
            a += f"P.barre(o{i},t,{o['sale']});"
        act.append(a)
    return cab + '\n' + ''.join(crea) + '\nreturn t=>{' + ''.join(act) + '}'


# ───────── plantillas: datos → (fases, objetos)
def _alto_titulo(lineas, size):
    return int(len(lineas) * size * .95)


def p_fases(d):
    return d['fases'], d.get('objetos', [])


def p_titular(d):
    en, size = d.get('en', 0), d.get('size', 150)
    pz = [dict(tipo='titular', lineas=d['titulo'], en=en, size=size, seed=d.get('seed', 1))]
    y = TOP + _alto_titulo(d['titulo'], size) + 90
    if d.get('sello'):
        pz.append(dict(tipo='sello', x=90, y=y, texto=d['sello']['texto'], en=d['sello']['en'], size=d['sello'].get('size', 64), rot=-6))
        y += 200
    if d.get('nota'):
        pz.append(dict(tipo='nota', x=90, y=y, html=d['nota']['texto'], en=d['nota']['en'], rot=-4, w=400, size=56))
    if d.get('mano'):
        pz.append(dict(tipo='mano', x=520, y=y + 120, texto=d['mano']['texto'], en=d['mano']['en'], size=64, color=d.get('acento')))
    return [dict(piezas=pz)], [d['objeto']] if d.get('objeto') else []


def p_cifra(d):
    en, size = d.get('en', 0), d.get('size', 140)
    alto = _alto_titulo(d['titulo'], size)
    pz = [dict(tipo='titular', lineas=d['titulo'], en=en, size=size, seed=d.get('seed', 1)),
          dict(tipo='numero', x=70, y=TOP + alto + 40, de=d.get('de', 0), a=d['a'], en=d['cuenta_en'], dur=d.get('dur', .9), formato=d.get('formato', 'c'),
               suf=d.get('sufijo', ''), pre=d.get('prefijo', ''), size=d.get('size_cifra', 300), color=d.get('acento'))]
    if d.get('nota'):
        pz.append(dict(tipo='nota', x=560, y=TOP + alto + 420, html=d['nota']['texto'], en=d['nota']['en'], rot=4, w=420, size=52))
    return [dict(piezas=pz)], [d['objeto']] if d.get('objeto') else []


def p_comparacion(d):
    en, size = d.get('en', 0), d.get('size', 140)
    y = TOP + _alto_titulo(d['titulo'], size) + 80
    lados = d['lados']
    w = 900 // len(lados) - 20
    pz = [dict(tipo='titular', lineas=d['titulo'], en=en, size=size, seed=d.get('seed', 1))]
    for i, l in enumerate(lados):
        pz.append(dict(tipo='recorte', x=70 + i * (w + 20), y=y, w=w, h=170, caja=l['texto'], size=l.get('size', 84),
                       estilo=f"text-align:center;color:{l.get('color', '#171513')}", en=l['en'], rot=[-3, 2, -2, 3][i % 4], seed=27 + i, pad='36px 16px'))
    if d.get('veredicto'):
        pz.append(dict(tipo='sello', x=80, y=y + 330, texto=d['veredicto']['texto'], en=d['veredicto']['en'], size=54, rot=-4))
    return [dict(piezas=pz)], d.get('objetos', [])


def p_lista(d):
    en, size = d.get('en', 0), d.get('size', 140)
    y = TOP + _alto_titulo(d['titulo'], size) + 80
    items = [[it['texto'], it['en']] for it in d['items']]
    pz = [dict(tipo='titular', lineas=d['titulo'], en=en, size=size, seed=d.get('seed', 1)),
          dict(tipo='lista', x=90, y=y, w=d.get('ancho', 700), h=70 * len(items) + 90, items=items, en=min(i[1] for i in items) - .15)]
    return [dict(piezas=pz)], [d['objeto']] if d.get('objeto') else []


def p_cita(d):
    en = d.get('en', 0)
    pz = [dict(tipo='recorte', x=70, y=TOP + 40, w=940, h=d.get('alto', 520), ser=f'«{d["texto"]}»', size=d.get('size', 76), en=en, rot=-1.5, seed=31,
               pad='50px 54px')]
    if d.get('autor'):   # solo si el autor está confirmado
        pz.append(dict(tipo='mano', x=520, y=TOP + d.get('alto', 520) + 90, texto='— ' + d['autor'], en=d.get('autor_en', en + 1), size=60))
    return [dict(piezas=pz)], [d['objeto']] if d.get('objeto') else []


def p_logo_dato(d):
    en, size = d.get('en', 0), d.get('size', 140)
    y = TOP + _alto_titulo(d['titulo'], size) + 80
    pz = [dict(tipo='titular', lineas=d['titulo'], en=en, size=size, seed=d.get('seed', 1)),
          dict(tipo='mano', x=90, y=y, texto=d['dato'], en=d.get('dato_en', en + 1), size=d.get('size_dato', 70), color=d.get('fondo'))]
    obj = dict(tipo=d.get('forma', 'medalla'), logo=d['logo'], fondo=d.get('fondo', '#d97757'), tinta=d.get('tinta', '#ffffff'), tam=280,
               x=780, y=1500, en=d.get('logo_en', en + .3))
    return [dict(piezas=pz)], [obj]


def p_antes_despues(d):
    a, b = d['antes'], d['despues']
    pz = [dict(tipo='recorte', x=80, y=TOP + 60, w=600, h=180, caja=a['texto'], size=a.get('size', 74), en=a['en'], rot=-3, seed=21, pad='44px 40px'),
          dict(tipo='tacha', x=100, y=TOP + 170, w=540, en=a.get('tacha_en', a['en'] + 1), grosor=16),
          dict(tipo='titular', lineas=b['titulo'], en=b['en'], top=TOP + 330, size=b.get('size', 150), seed=d.get('seed', 3))]
    return [dict(piezas=pz)], [d['objeto']] if d.get('objeto') else []


PANTALLA = {
    'fases': dict(f=p_fases, req=('fases',), opc=('objetos', 'js3d', 'fondo', 'acento', 'css', 'seed')),
    'titular': dict(f=p_titular, req=('titulo',), opc=('en', 'size', 'sello', 'nota', 'mano', 'objeto', 'fondo', 'acento', 'seed')),
    'cifra': dict(f=p_cifra, req=('titulo', 'a', 'cuenta_en'), opc=('en', 'de', 'dur', 'formato', 'sufijo', 'prefijo', 'size', 'size_cifra', 'nota', 'objeto',
                                                                    'fondo', 'acento', 'seed')),
    'comparacion': dict(f=p_comparacion, req=('titulo', 'lados'), opc=('en', 'size', 'veredicto', 'objetos', 'fondo', 'acento', 'seed')),
    'lista': dict(f=p_lista, req=('titulo', 'items'), opc=('en', 'size', 'ancho', 'objeto', 'fondo', 'acento', 'seed')),
    'cita': dict(f=p_cita, req=('texto',), opc=('en', 'autor', 'autor_en', 'alto', 'size', 'objeto', 'fondo', 'acento', 'seed')),
    'logo_dato': dict(f=p_logo_dato, req=('titulo', 'logo', 'dato'), opc=('en', 'size', 'dato_en', 'size_dato', 'logo_en', 'forma', 'fondo', 'tinta',
                                                                          'acento', 'seed')),
    'antes_despues': dict(f=p_antes_despues, req=('antes', 'despues'), opc=('objeto', 'fondo', 'acento', 'seed')),
}


def escena_pantalla(e, siguiente=True):
    """Escena a pantalla completa → (start, end, html)."""
    d = e['datos']
    fases, objetos = PANTALLA[e['plantilla']]['f'](d)
    A = K.at(e['inicio'])
    body = ''
    for f in fases:
        html = ''.join(pieza(p, A) for p in f['piezas'])
        body += K.fase(html, A, entra=f.get('entra'), sale=f.get('sale')) if (f.get('entra') is not None or f.get('sale') is not None or len(fases) > 1) else html
    end = e['fin'] + (K.COLA if siguiente else 0)
    ac = d.get('acento', 'var(--rojo)')
    css = d.get('css', '') or (f'.tt .sf{{color:{ac}}}' if d.get('acento') else '')
    return e['inicio'], end, K.page(css, body, round(end - e['inicio'], 2), S0=e['inicio'], fondo=d.get('fondo', 'papel'), seed=d.get('seed', 1),
                                     ac=ac, js3d=js3d(objetos, d.get('js3d', '')))


# ───────── capas transparentes
def sigueme(e, fin):
    d = e['datos']
    S = e['inicio']
    A = K.at(S)
    r = d.get('respuesta', '')
    body = (K.nota(570, 1250, f'<div style="font-size:44px">Sígueme</div><div style="font-family:Archivo;font-weight:900;font-stretch:62%;font-size:84px;'
                              f'line-height:.9;text-transform:uppercase">{d.get("seccion", "El Log")}</div>'
                              f'<div style="font-size:40px;margin-top:6px">{d.get("detalle", "cada semana · Armando")}</div>', A, S + .1, rot=5, w=430, size=60)
            + K.sello(640, 1600, 'Seguir ✓', A, S + .9, size=60, rot=-4, color='var(--verde)')
            + K.recorte(60, 1280, 480, 330, f'<div class="ser" style="font-size:40px;line-height:1.1">{d["pregunta"]}</div>'
                        + (f'<div style="margin-top:18px;font-family:Caveat;font-weight:700;font-size:38px;color:var(--azul)">'
                           f'<span style="display:inline-block;white-space:nowrap;clip-path:inset(0 100% 0 0);animation:tip 1s steps({len(r) + 1}) {A(S + 1.5)} forwards">'
                           f'{r}</span></div>' if r else ''), A, S + .5, rot=-3, seed=31))
    return S, fin, K.page('', body, round(fin - S, 2), S0=S, transparente=True)


def cabecera(e, fin):
    d = e['datos']
    A = K.at(0)
    caps = d['titulares']
    caph = ''.join(f'<span class="cp" style="--d:{A(t)};{f"--x:{A(caps[i + 1][0])};" if i + 1 < len(caps) else ""}">{i + 1:02d} · {n}</span>'
                   for i, (t, n) in enumerate(caps))
    tick = '<span>⚠</span>'.join(f'<span>{c}</span>' for c in d.get('corrido', []))
    css = CABE_CSS.replace('FIBRA', K.FIBRA)
    body = (f'<div class="cab"><div class="mh"><div class="lg">El <i>Log</i></div><div class="ed"><b>Edición del día</b>{d.get("edicion", "")}</div></div>'
            f'<span class="ul">⚠ Última hora</span>{caph}<div class="tick"><div class="mv">{tick}<span>⚠</span>{tick}</div></div></div>')
    return 0.0, fin, K.page(css, body, fin, S0=0.0, transparente=True)


CABE_CSS = """
.cab{position:absolute;left:0;right:0;top:0;height:250px;z-index:90;background:#f3ecdf;box-shadow:0 10px 24px rgba(0,0,0,.35);animation:cabIn .45s cubic-bezier(.2,1.3,.4,1) both}
.cab:before{content:'';position:absolute;inset:0;background:url("FIBRA");opacity:.45}
@keyframes cabIn{from{transform:translateY(-260px)}to{transform:none}}
.cab .mh{position:absolute;left:44px;right:44px;top:22px;height:108px;display:flex;align-items:flex-end;justify-content:space-between;border-bottom:5px double #171513;padding-bottom:6px}
.cab .lg{font-family:'Instrument Serif',serif;font-size:112px;line-height:.8;letter-spacing:-.02em}
.cab .lg i{color:var(--rojo)}
.cab .ed{text-align:right;font-weight:800;font-stretch:75%;text-transform:uppercase;font-size:24px;letter-spacing:.08em;line-height:1.3}
.cab .ed b{display:block;font-size:30px;color:var(--rojo)}
.cab .cp{position:absolute;right:44px;top:142px;font-weight:900;font-stretch:62%;font-size:40px;text-transform:uppercase;opacity:0;animation:capIn .3s steps(2) var(--d) forwards}
.cab .cp[style*="--x"]{animation:capIn .3s steps(2) var(--d) forwards,capOut .01s linear var(--x) forwards}
@keyframes capIn{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:none}}@keyframes capOut{to{opacity:0}}
.cab .ul{position:absolute;left:44px;top:146px;font-weight:900;font-stretch:62%;font-size:36px;text-transform:uppercase;color:#fff;background:var(--rojo);padding:2px 16px;
  animation:lat 1s steps(1) infinite}
@keyframes lat{50%{background:#171513}}
.tick{position:absolute;left:0;right:0;top:196px;height:54px;background:var(--rojo);overflow:hidden;display:flex;align-items:center}
.tick .mv{display:flex;gap:30px;white-space:nowrap;font-weight:800;font-stretch:80%;font-size:30px;color:#fff;text-transform:uppercase;animation:mv 70s linear infinite;padding-left:1080px}
@keyframes mv{to{transform:translateX(-100%)}}
"""

for _p in PANTALLA.values():                 # comunes a todas las escenas a pantalla completa
    _p['opc'] = tuple(dict.fromkeys(tuple(_p['opc']) + ('fondo', 'acento', 'css', 'seed')))

CAPAS = {
    'sigueme': dict(f=sigueme, req=('pregunta',), opc=('respuesta', 'seccion', 'detalle')),
    'cabecera': dict(f=cabecera, req=('titulares',), opc=('corrido', 'edicion')),
}
PLANTILLAS = {**PANTALLA, **CAPAS}
