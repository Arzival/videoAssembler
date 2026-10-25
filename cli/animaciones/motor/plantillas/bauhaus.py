"""Plantillas del estilo «Bauhaus» (Inventario) para el motor.

Bloques de color plano que entran deslizándose y encajan, formas puras y textos revelados por una barra (bauhaus.py y los
bloques de ejemplos/video10-bauhaus.py, los mismos que usan los guiones hechos a mano).
  tarjeta  — capa transparente sobre la cámara (mitad de arriba, sin tapar el gadget) con piezas
  escena   — pantalla completa: entra con el círculo de color desde una esquina y sale deslizándose
  dato     — tarjeta lista: titular negro + valor grande (con contador) + etiqueta de color
  sigueme  — cierre con la pregunta, «Seguir ✓» y despedida
"""
import importlib.util, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import bauhaus as B

_EJ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'ejemplos', 'video10-bauhaus.py')
_sp = importlib.util.spec_from_file_location('v10bh_motor', _EJ)
V10 = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(V10)
C = B.COL
CSS = V10.CSS + """
.fill{position:absolute;left:0;top:0;bottom:0;right:0;transform-origin:left;transform:scaleX(0);animation:barx 1.6s cubic-bezier(.3,0,.3,1) var(--d) forwards}
@keyframes barx{to{transform:scaleX(var(--f1,1))}}
"""


def _g(p, k, d=None):
    return p.get(k, d)


def pieza(p, A):
    t = p['tipo']
    if t == 'blq':
        return V10.blq(p['x'], p['y'], p['w'], p['h'], C.get(p['color'], p['color']), p.get('html', ''), A, p['en'], desde=_g(p, 'desde', 'izq'),
                       sale=_g(p, 'sale'), hacia=_g(p, 'hacia', 'izq'), pad=_g(p, 'pad', '26px 34px'), z=_g(p, 'z', 5), txt=_g(p, 'txt', '#151515'),
                       extra=_g(p, 'extra', ''), dur=_g(p, 'dur', .7))
    if t == 'forma':
        return B.forma(p['forma'], p['x'], p['y'], p['w'], p['h'], C.get(p['color'], p['color']), A, p['en'], desde=_g(p, 'desde', 'izq'), sale=_g(p, 'sale'),
                       hacia=_g(p, 'hacia', 'izq'), rot=_g(p, 'rot', 0), gira=_g(p, 'gira', False), z=_g(p, 'z', 5), dur=_g(p, 'dur', .7),
                       escala=_g(p, 'escala', False))
    if t == 'lab':
        return V10.lab(p['x'], p['y'], p['html'], A, p['en'], _g(p, 'sale'), z=_g(p, 'z', 9), extra=_g(p, 'extra', ''))
    if t == 'texto':
        return B.texto(p['lineas'], A, p['en'], x=_g(p, 'x', 70), y=_g(p, 'y', 300), size=_g(p, 'size', 120), sale=_g(p, 'sale'),
                       ac=C.get(_g(p, 'ac'), _g(p, 'ac')), step=_g(p, 'step', .12))
    if t == 'html':
        return p['html']
    raise ValueError(f'pieza desconocida: {t}')


def h(txt, size, extra=''):
    return V10.h(txt, size, extra)


def s(txt, size, extra=''):
    return V10.s(txt, size, extra)


def tarjeta(e, fin):
    A = B.at(e['inicio'])
    body = ''.join(pieza(p, A) for p in e['datos']['piezas'])
    return e['inicio'], e['fin'], B.page(CSS, body, round(e['fin'] - e['inicio'], 2), S0=e['inicio'], transparente=True)


def escena(e, fin):
    d = e['datos']
    A = B.at(e['inicio'])
    ds = round(e['fin'] - e['inicio'], 2)
    body = ''.join(pieza(p, A) for p in d['piezas'])
    css = (CSS + f'.lz.sal{{animation:ci .7s cubic-bezier(.7,0,.25,1) both,lzsale .5s cubic-bezier(.6,0,.85,.45) {ds - .55:.2f}s forwards}}'
           '@keyframes lzsale{to{transform:translateX(-1200px)}}')
    html = B.page(css, body, ds, S0=e['inicio'], fondo=C.get(d.get('fondo', 'crema'), d.get('fondo', 'crema')), entra=d.get('entra', 'sd'))
    return e['inicio'], e['fin'], html.replace('class="lz"', 'class="lz sal"', 1)


def dato(e, fin):
    """Tarjeta lista: titular (negro) arriba, valor grande con contador y etiqueta de color abajo; todo sale a la izquierda."""
    d = e['datos']
    S, X = e['inicio'], e['fin'] - .35
    A = B.at(S)
    en = d.get('en', S + .2)
    valor = d['valor']
    if isinstance(valor, (int, float)):
        valor = V10.N([(0, 0), (d.get('cuenta_en', en + .8), valor, d.get('dur', 1.2))], f=d.get('formato', 'c'))
    body = (V10.blq(80, 230, 920, 150, C['negro'], h(d['titulo'], 76, f'color:{C["crema"]}'), A, en, desde='izq', sale=X, hacia='izq', pad='0 40px')
            + V10.blq(80, 410, 920, 230, C.get(d.get('color', 'amarillo'), d.get('color', 'amarillo')),
                      f'<div class="h" style="font-size:130px">{valor}<span style="font-size:56px;margin-left:14px">{d.get("unidad", "")}</span></div>',
                      A, en + .4, desde='der', sale=X, hacia='der', pad='0 44px'))
    if d.get('etiqueta'):
        body += V10.lab(110, 670, h(d['etiqueta'], 46, f'padding:6px 18px;background:{C["rojo"]};color:{C["blanco"]};width:max-content'), A,
                        d.get('etiqueta_en', en + 1.2), X, z=9)
    return S, e['fin'], B.page(CSS, body, round(e['fin'] - S, 2), S0=S, transparente=True)


def sigueme(e, fin):
    d = e['datos']
    S, X = e['inicio'], fin - .35
    A = B.at(S)
    body = (V10.blq(570, 240, 430, 330, C['amarillo'], s('Sígueme', 40, 'font-weight:600') + h(d.get('nombre', 'Armando'), 92, 'margin-top:6px')
                    + s(d.get('detalle', 'gadgets · IA · código'), 34, 'margin-top:10px;font-weight:600'), A, S + .1, desde='der', sale=X, hacia='der',
                    pad='30px 36px')
            + B.forma('c', 940, 200, 110, 110, C['rojo'], A, S + .4, desde='arriba', sale=X, hacia='arriba', z=7)
            + V10.blq(600, 600, 370, 100, C['rojo'], h('Seguir ✓', 54, f'color:{C["blanco"]};text-align:center;width:100%'), A, S + 1.0, desde='abajo',
                      sale=X, hacia='der', pad='0', z=6)
            + V10.blq(80, 240, 470, 380, C['crema'], h(d['pregunta'], 46, 'white-space:normal;line-height:1.12')
                      + s(d.get('pie', 'te leo en los comentarios'), 32, f'margin-top:20px;color:{C["azul"]};font-weight:600'), A, S + .5, desde='izq',
                      sale=X, hacia='izq', pad='30px 34px'))
    if d.get('despedida'):
        body += V10.blq(80, 740, 920, 110, C['negro'], h(d['despedida'], 46, f'color:{C["amarillo"]}'), A, d.get('despedida_en', S + 4.8), desde='abajo',
                        sale=X, hacia='izq', pad='0 36px', z=7)
    return S, fin, B.page(CSS, body, round(fin - S, 2), S0=S, transparente=True)


CAPAS = {
    'tarjeta': dict(f=tarjeta, req=('piezas',), opc=()),
    'escena': dict(f=escena, req=('piezas',), opc=('fondo', 'entra')),
    'dato': dict(f=dato, req=('titulo', 'valor'), opc=('en', 'cuenta_en', 'dur', 'formato', 'unidad', 'color', 'etiqueta', 'etiqueta_en')),
    'sigueme': dict(f=sigueme, req=('pregunta',), opc=('nombre', 'detalle', 'pie', 'despedida', 'despedida_en')),
}
PANTALLA = {}
PLANTILLAS = {**CAPAS}


def escena_pantalla(e, siguiente=True):   # en Bauhaus todo pasa por CAPAS (la escena ya trae su entrada y salida)
    raise ValueError('estilo bauhaus: usa las plantillas tarjeta/escena/dato/sigueme')
