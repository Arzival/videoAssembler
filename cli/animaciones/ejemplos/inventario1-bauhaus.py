"""Inventario #1 · las powerbanks (sección de gadgets) · edición «Bauhaus» (geométrica y plana).
Tarjetas de bloques de color en la mitad de arriba (sobre los monitores, sin tapar el gadget que enseña) y UNA escena a
pantalla completa solo mientras dice «En mi recámara solo tengo un enchufe y me queda lejos»: entra con el círculo desde una
esquina y sale deslizándose; debajo sigue el mismo clip, así que la salida no tropieza. Sin desvanecidos.
Tiempos = timeline final de inventario/1 (85.46 s).
Uso: SALIDA=~/Documents/Videos/inventario/1/animaciones REL=inventario/1/animaciones python3 ejemplos/inventario1-bauhaus.py [ids…]
Los archivos salen con prefijo «ginv1-».
"""
import importlib.util, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bauhaus as B
from bauhaus import forma, texto, N

HERE = os.path.dirname(os.path.abspath(__file__))
_sp = importlib.util.spec_from_file_location('v10bh', os.path.join(HERE, 'video10-bauhaus.py'))
V10 = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(V10)
blq, h, s, lab = V10.blq, V10.h, V10.s, V10.lab

CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.path.expanduser('~/Documents/Videos/inventario/1/animaciones')))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
PRE = 'ginv1-'
FIN = 85.46
PIEZAS = []
C = B.COL
CR, AM, AZ, RJ, NG, BL = C['crema'], C['amarillo'], C['azul'], C['rojo'], C['negro'], C['blanco']
VD = '#2b9a5a'

CSS = V10.CSS + """
.fill{position:absolute;left:0;top:0;bottom:0;right:0;transform-origin:left;transform:scaleX(0);animation:barx 1.6s cubic-bezier(.3,0,.3,1) var(--d) forwards}
@keyframes barx{to{transform:scaleX(var(--f1,1))}}
"""


def et(txt, size, fondo, color=NG):
    return h(txt, size, f'padding:6px 18px;background:{fondo};color:{color};width:max-content')


def tarjeta(pid, start, dur, body):
    PIEZAS.append((pid, start, round(start + dur, 2), B.page(CSS, body, dur, S0=start, transparente=True)))


# ───────── 0:00 · «Todos tenemos un gadget que no podemos dejar de comprar» → identidad de la sección
S = 0.15; A = B.at(S); X = 3.3
tarjeta('c01-inventario', S, 3.6,
        blq(80, 250, 700, 190, NG, h('INVENTARIO', 104, f'color:{CR}'), A, .2, desde='izq', sale=X, hacia='izq', pad='0 44px')
        + forma('c', 800, 200, 220, 220, RJ, A, .55, desde='der', sale=X, hacia='der', z=7)
        + blq(800, 200, 220, 220, 'transparent', h('#01', 88, f'color:{BL};text-align:center;width:100%'), A, .55, desde='der', sale=X, hacia='der', pad='0', z=8)
        + blq(80, 470, 900, 130, AM, h('el gadget que no dejo de comprar', 54), A, 1.7, desde='abajo', sale=X, hacia='izq', pad='0 40px', z=6))

# ───────── 0:04 · «En mi caso son las powerbanks, ya tengo 5 y esta fue la que me costó $1,500 pesos»
S = 4.3; A = B.at(S); X = 9.85
PILA = ''.join(blq(110 + i * 150, 560, 120, 190, [AZ, RJ, NG, BL, AM][i], '', A, 5.75 + i * .1, desde='abajo', sale=X, hacia='abajo', pad='0', z=6,
                   extra=f'border-radius:22px;overflow:hidden;box-shadow:inset 0 0 0 7px {NG}') for i in range(5))
tarjeta('c02-cinco', S, 5.95,
        blq(80, 230, 620, 150, NG, h('🔋 Powerbanks', 82, f'color:{CR}'), A, 4.4, desde='izq', sale=X, hacia='izq', pad='0 40px')
        + blq(80, 400, 620, 130, CR, f'<div class="h" style="font-size:64px">ya tengo <span style="color:{RJ}">{N([(0, 0), (5.6, 5, .6)])}</span></div>',
              A, 5.5, desde='izq', sale=X, hacia='izq', pad='0 40px', z=6)
        + PILA
        + forma('c', 740, 230, 270, 270, AM, A, 7.9, desde='der', sale=X, hacia='der', z=7)
        + blq(740, 230, 270, 270, 'transparent', '<div style="text-align:center;width:100%">' + s('esta', 36, 'font-weight:600')
              + h('$1,500', 70, 'margin-top:4px') + s('MXN', 32, 'font-weight:600;margin-top:2px') + '</div>', A, 7.9, desde='der', sale=X, hacia='der', pad='0', z=8))


# ───────── 0:10 · «En mi recámara solo tengo un enchufe y me queda lejos» (recámara 10.43 · enchufe 12.08 · lejos 13.17)
S, E = 10.34, 14.15
A = B.at(S)
DS = round(E - S, 2)
ESC = (texto(['Un solo [enchufe]'], A, 10.45, y=230, size=118, ac=RJ)
       + texto(['…y [lejos]'], A, 12.7, y=350, size=118, ac=RJ)
       # el cuarto, la cama y el enchufe en la pared de enfrente
       + blq(90, 620, 900, 900, 'transparent', '', A, 10.5, desde='abajo', pad='0', z=3, extra=f'box-shadow:inset 0 0 0 10px {NG}')
       + blq(150, 1180, 440, 270, AZ, '<div style="position:absolute;left:24px;top:24px;width:140px;height:84px;background:#faf7f0;border:6px solid #151515"></div>'
             + h('mi cama', 48, f'color:{BL};position:absolute;left:26px;bottom:20px'), A, 10.75, desde='izq', pad='0', z=4, extra=f'box-shadow:inset 0 0 0 7px {NG}')
       + forma('c', 780, 670, 180, 180, AM, A, 11.9, desde='der', z=4, escala=True)
       + blq(815, 705, 110, 110, CR, '<div style="display:flex;gap:22px;justify-content:center;width:100%"><i style="width:14px;height:40px;background:#151515"></i>'
             '<i style="width:14px;height:40px;background:#151515"></i></div>', A, 12.0, desde='der', pad='0', z=5, extra=f'box-shadow:inset 0 0 0 7px {NG}')
       + lab(735, 870, et('1 enchufe', 40, NG, CR), A, 12.15, z=9)
       # la distancia: línea punteada de la cama al enchufe
       + f'<div class="ap" style="--d:{A(12.45)}"><div class="gr" style="position:absolute;left:500px;top:1150px;width:420px;height:12px;z-index:6;'
         f'background:repeating-linear-gradient(90deg,{RJ} 0 34px,transparent 34px 56px);transform-origin:left;rotate:-40deg;--d:{A(12.45)}"></div></div>'
       + lab(560, 960, et('lejos 😩', 54, RJ, BL), A, 12.8, z=9))
PIEZAS.append(('s1-recamara', S, E,
           B.page(V10.CSS + f'.lz.sal{{animation:ci .7s cubic-bezier(.7,0,.25,1) both,lzsale .5s cubic-bezier(.6,0,.85,.45) {DS - .55:.2f}s forwards}}'
                            '@keyframes lzsale{to{transform:translateX(-1200px)}}', ESC, DS, S0=S, fondo=CR, entra='sd').replace('class="lz"', 'class="lz sal"', 1)))

# ───────── 0:29 · «también tengo la cara… pero es la que me llevo cuando salgo, porque con esta sí puedo cargar mi laptop»
S = 29.8; A = B.at(S); X = 38.1
tarjeta('c03-cara', S, 8.6,
        blq(80, 240, 520, 150, RJ, h('💸 la cara', 76, f'color:{BL}'), A, 30.0, desde='izq', sale=X, hacia='izq', pad='0 40px')
        + forma('tri', 620, 270, 100, 90, NG, A, 30.3, desde='izq', sale=X, hacia='izq', rot=90, z=6)
        + blq(80, 420, 760, 130, CR, h('🎒 la que me llevo al salir', 54), A, 34.5, desde='der', sale=X, hacia='der', pad='0 36px')
        + blq(80, 580, 640, 130, AZ, h('💻 carga mi laptop', 58, f'color:{BL}'), A, 37.2, desde='izq', sale=X, hacia='izq', pad='0 36px'))

# ───────── 0:39 · «capacidad de 25,000 mAh y me entrega hasta 165 W por USB-C»
S = 38.7; A = B.at(S); X = 46.6
tarjeta('c04-specs', S, 8.15,
        blq(80, 230, 920, 230, NG, s('capacidad', 40, f'color:{AM};font-weight:600')
            + f'<div class="h" style="font-size:120px;color:{CR};margin-top:6px">{N([(0, 0), (40.3, 25000, 1.6)], f="c")}<span style="font-size:52px;margin-left:14px">mAh</span></div>',
            A, 39.0, desde='izq', sale=X, hacia='izq', pad='0 44px')
        + forma('c', 80, 490, 300, 300, AM, A, 44.4, desde='izq', sale=X, hacia='izq', z=6)
        + blq(80, 490, 300, 300, 'transparent', '<div style="text-align:center;width:100%">' + s('hasta', 36, 'font-weight:600')
              + h(N([(0, 0), (44.6, 165, .7)]) + '<span style="font-size:50px"> W</span>', 96, 'margin-top:4px') + '</div>', A, 44.4, desde='izq', sale=X, hacia='izq', pad='0', z=7)
        + blq(410, 600, 420, 110, RJ, h('⚡ por USB-C', 56, f'color:{BL}'), A, 46.0, desde='der', sale=X, hacia='der', pad='0 30px'))

# ───────── 0:47 · «estas otras dos, por una emergencia… también carga mi laptop, pero no una carga completa»
S = 48.5; A = B.at(S); X = 56.4
LAP = (f'<div style="position:relative;width:820px;height:56px;border:7px solid {NG};background:{BL}">'
       f'<div class="fill" style="background:{AM};--f1:.6;--d:{A(52.4)}"></div></div>')
tarjeta('c05-emergencia', S, 7.9,
        blq(80, 230, 700, 150, RJ, h('🚨 para emergencias', 66, f'color:{BL}'), A, 48.7, desde='izq', sale=X, hacia='izq', pad='0 40px')
        + forma('c', 830, 220, 170, 170, NG, A, 49.0, desde='der', sale=X, hacia='der', z=6)
        + blq(830, 220, 170, 170, 'transparent', h('×2', 76, f'color:{AM};text-align:center;width:100%'), A, 49.0, desde='der', sale=X, hacia='der', pad='0', z=7)
        + blq(80, 410, 920, 260, CR, s('💻 también carga mi laptop', 46, 'font-weight:700') + f'<div style="margin-top:22px">{LAP}</div>'
              + V10.rv(s('…pero no al 100 %', 40, f'margin-top:16px;color:{RJ};font-weight:700'), A, 55.2),
              A, 52.2, desde='abajo', sale=X, hacia='izq', pad='30px 44px'))

# ───────── 1:02 · «con un cargador basta… y sí, funciona. El problema: el enchufe no siempre está donde tú estás. Una powerbank sí.»
S = 63.8; A = B.at(S); X = 72.25
tarjeta('c06-cargador', S, 8.6,
        blq(80, 230, 440, 230, CR, h('🔌', 80) + h('cargador', 58, 'margin-top:6px'), A, 64.0, desde='izq', sale=X, hacia='izq', pad='0 36px')
        + lab(110, 480, et('✓ funciona', 46, VD, BL), A, 65.8, X, z=9)
        + blq(80, 560, 920, 120, NG, h('…si hay enchufe cerca', 56, f'color:{CR}'), A, 67.8, desde='abajo', sale=X, hacia='izq', pad='0 40px')
        + blq(560, 230, 440, 230, AM, h('🔋', 80) + h('powerbank', 58, 'margin-top:6px'), A, 71.2, desde='der', sale=X, hacia='der', pad='0 36px')
        + lab(590, 480, et('✓ siempre contigo', 46, VD, BL), A, 71.5, X, z=9))

# ───────── 1:12 · «ya me están dando ganas de comprarme otra»
S = 74.2; A = B.at(S); X = 77.25
tarjeta('c07-otra', S, 3.2,
        blq(80, 240, 640, 160, NG, f'<div class="h" style="font-size:80px;color:{CR}">la #{N([(0, 5), (75.2, 6, .4)])}… <span style="font-size:70px">😅</span></div>',
            A, 74.4, desde='izq', sale=X, hacia='izq', pad='0 40px')
        + forma('c', 760, 230, 180, 180, RJ, A, 75.3, desde='der', sale=X, hacia='der', z=6))

# ───────── 1:17 · Sígueme + «¿qué gadget no puedes dejar de comprar?» → «nos vemos en el próximo inventario»
S = 77.5; A = B.at(S); X = FIN - .35
SEG = (blq(570, 240, 430, 330, AM, s('Sígueme', 40, 'font-weight:600') + h('Armando', 92, 'margin-top:6px') + s('gadgets · IA · código', 34, 'margin-top:10px;font-weight:600'),
           A, 77.6, desde='der', sale=X, hacia='der', pad='30px 36px')
       + forma('c', 940, 200, 110, 110, RJ, A, 77.9, desde='arriba', sale=X, hacia='arriba', z=7)
       + blq(600, 600, 370, 100, RJ, h('Seguir ✓', 54, f'color:{BL};text-align:center;width:100%'), A, 78.5, desde='abajo', sale=X, hacia='der', pad='0', z=6)
       + blq(80, 240, 470, 380, CR, h('🔋 ¿Qué gadget<br>no puedes dejar<br>de comprar?', 46, 'white-space:normal;line-height:1.12')
             + s('te leo en los comentarios', 32, f'margin-top:20px;color:{AZ};font-weight:600'), A, 78.0, desde='izq', sale=X, hacia='izq', pad='30px 34px')
       + blq(80, 740, 920, 110, NG, h('nos vemos en el próximo INVENTARIO', 46, f'color:{AM}'), A, 82.3, desde='abajo', sale=X, hacia='izq', pad='0 36px', z=7))
PIEZAS.append(('seguir', S, FIN, B.page(CSS, SEG, round(FIN - S, 2), S0=S, transparente=True)))
PIEZAS.sort(key=lambda p: p[1])


def captura(p):
    pid, a, b, html = p
    path = f'{WORK}/{pid}.html'
    open(path, 'w').write(html)
    if os.environ.get('SOLO_HTML'):
        return f'html {path} {b - a:.2f}'
    r = subprocess.run(['node', CAP, path, f'{b - a:.2f}', f'{OUT}/{PRE}{pid}.webm'], capture_output=True, text=True)
    return r.stdout.strip() or r.stderr[-600:]


if __name__ == '__main__':
    solo = set(sys.argv[1:])
    todo = [p for p in PIEZAS if not solo or p[0] in solo]
    with ThreadPoolExecutor(int(os.environ.get('P', 6))) as ex:
        for r in ex.map(captura, todo):
            print(r, flush=True)
    rel = os.environ.get('REL', 'inventario/1/animaciones')
    ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
    json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
    print('overlays.json')
