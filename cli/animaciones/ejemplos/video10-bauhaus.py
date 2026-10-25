"""Video 10 · la Legion 5 llega al homelab (devlog) · edición «Bauhaus» (geométrica y plana, sin la base gloss ni papel).
Bloques de color plano (crema, amarillo, azul, rojo, negro) que entran deslizándose y encajan sobre la cámara (mitad de
arriba, sin tapar la demo), con los textos SIEMPRE encima de un bloque para que se lean; formas puras (círculo, triángulo,
barra) como acentos. Una sola escena a pantalla completa (respaldo mutuo) que entra con el círculo de color desde una
esquina y sale deslizándose. Sin desvanecidos: todo entra y sale deslizándose.
Tiempos = timeline final de videos/10 (115.62 s), los mismos de video10-recorte.py / video10-gloss.py.
Uso: SALIDA=~/Documents/Videos/videos/10/bauhaus REL=videos/10/bauhaus python3 ejemplos/video10-bauhaus.py [ids…]   (SOLO_HTML=1 para revisar)
Los archivos salen con prefijo «gbh10-».
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bauhaus as B
import ellog_gloss as G
from bauhaus import forma, texto, N, etiqueta, ap

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.path.expanduser('~/Documents/Videos/videos/10/bauhaus')))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
PRE = 'gbh10-'
FIN = 115.62
PIEZAS = []
C = B.COL
CR, AM, AZ, RJ, NG = C['crema'], C['amarillo'], C['azul'], C['rojo'], C['negro']

CSS = """
.bq{display:flex;flex-direction:column;justify-content:center;overflow:hidden}
.h{font-weight:800;line-height:.92;letter-spacing:-.02em;white-space:nowrap}
.s{font-weight:500;line-height:1.1;white-space:nowrap}
.up{text-transform:uppercase}
.rv{clip-path:inset(0 100% 0 0);animation:rev .35s steps(7) var(--d) forwards}
.ty{display:inline-block;white-space:pre;clip-path:inset(0 100% 0 0);animation:tip var(--td,.8s) steps(var(--n,20)) var(--d) forwards}
@keyframes tip{to{clip-path:inset(0 -4% 0 0)}}
.gr{transform-origin:left center;transform:scaleX(0);animation:gr .8s cubic-bezier(.7,0,.25,1) var(--d) forwards}
@keyframes gr{to{transform:scaleX(1)}}
.cp{position:absolute;top:0;width:34px;height:34px;background:#f3c11b;box-shadow:0 0 0 5px #151515;animation:cp 1s linear var(--d) infinite;opacity:0}
@keyframes cp{0%{transform:translateX(0);opacity:1}100%{transform:translateX(150px);opacity:1}}
"""


def blq(x, y, w, h, color, html, A, t, desde='izq', sale=None, hacia='izq', pad='26px 34px', z=5, txt='#151515', extra='', dur=.7):
    """Bloque de color plano con contenido; entra deslizándose y encaja (misma animación que B.forma)."""
    fx, fy = B.DESDE[desde]
    sx, sy = B.DESDE[hacia]
    st = (f'left:{x}px;top:{y}px;width:{w}px;height:{h}px;--d:{A(t)};--dur:{dur}s;z-index:{z};--fx:{fx};--fy:{fy};'
          f'--fr:{-12 if desde in ("izq", "arriba") else 12}deg;--sx:{sx};--sy:{sy};--sr:{12 if hacia in ("der", "abajo") else -12}deg;')
    cls = 'fm sx' + (' x' if sale is not None else '')
    if sale is not None:
        st += f'--x:{A(sale)};'
    return (f'<div class="{cls}" style="{st}{extra}"><div class="bq" style="width:100%;height:100%;background:{color};color:{txt};padding:{pad}">'
            f'{html}</div></div>')


def h(txt, size, extra=''):
    return f'<div class="h" style="font-size:{size}px;{extra}">{txt}</div>'


def s(txt, size, extra=''):
    return f'<div class="s" style="font-size:{size}px;{extra}">{txt}</div>'


def rv(html, A, t):
    """Contenido que se revela de golpe (barrido a pasos) cuando el bloque ya encajó."""
    return f'<div class="rv" style="--d:{A(t)}">{html}</div>'


def teclea(txt, A, t, dt):
    import re
    n = max(4, len(re.sub(r'<[^>]+>', '', txt)))
    return f'<span class="ty" style="--d:{A(t)};--td:{dt}s;--n:{n}">{txt}</span>'


def lab(x, y, html, A, t, sale=None, z=9, extra=''):
    """Texto que aparece de golpe en t (y se quita en sale) con su propio z-index (B.ap con hijo absoluto queda debajo de los bloques)."""
    cls, st = 'ap', f'--d:{A(t)};position:absolute;left:{x}px;top:{y}px;z-index:{z};'
    if sale is not None:
        cls += ' x'; st += f'--x:{A(sale)};'
    return f'<div class="{cls}" style="{st}{extra}">{html}</div>'


def tarjeta(pid, start, dur, body):
    PIEZAS.append((pid, start, round(start + dur, 2), B.page(CSS, body, dur, S0=start, transparente=True)))


# ───────── 0:00 · «esta laptop me costó $9,000 pesos usada y va a ser el músculo de mi homelab»
S = 0.2; A = B.at(S); X = 3.75
tarjeta('c01-precio', S, 4.1,
        blq(90, 270, 640, 380, AM, s('mi nueva laptop', 44, 'font-weight:600')
            + f'<div class="h" style="font-size:176px;margin-top:8px">${N([(0, 0), (.9, 9000, .9)], f="c")}<span style="font-size:48px;margin-left:10px">MXN</span></div>',
            A, .25, desde='izq', sale=X, hacia='izq', pad='30px 44px')
        + forma('c', 765, 230, 240, 240, RJ, A, 2.0, desde='der', sale=X, hacia='der', z=7)
        + blq(765, 230, 240, 240, 'transparent', h('usada', 64, 'color:#faf7f0;text-align:center;width:100%'), A, 2.0, desde='der', sale=X, hacia='der', pad='0', z=8)
        + blq(90, 690, 900, 120, NG, h('💪 el músculo de mi homelab', 58, 'color:#efe8da'), A, 2.8, desde='abajo', sale=X, hacia='izq', pad='0 40px', z=6))

# ───────── 0:08 · Ryzen 7 (8 núcleos · 16 hilos) · 16 GB de RAM expandible · ⭐ lo más importante: RTX 3050 Ti de 4 GB
S = 8.3; A = B.at(S); X = 22.75
FILAS = [('Ryzen 7', '8 núcleos · 16 hilos', 9.0, RJ, '#faf7f0'), ('16 GB de RAM', 'y se puede expandir', 13.2, AZ, '#faf7f0'),
         ('RTX 3050 Ti', '4 GB de memoria', 20.8, AM, '#151515')]
SPEC = blq(80, 210, 920, 760, CR, '<div style="position:absolute;left:44px;top:34px">' + h('Lenovo Legion 5', 86)
           + s('la encontré en Marketplace', 40, 'margin-top:10px;color:#1f4fd6;font-weight:600') + '</div>', A, 8.5, desde='izq', sale=X, hacia='izq', pad='0', z=4,
           extra='')
for i, (n, sub, t, col, tc) in enumerate(FILAS):
    y = 430 + i * 160
    SPEC += blq(140, y, 820, 132, col, h(n, 66, f'color:{tc}') + s(sub, 34, f'color:{tc};opacity:.85;margin-top:6px'), A, t, desde='der', sale=X, hacia='der', pad='0 36px', z=6)
SPEC += (forma('tri', 64, 774, 70, 64, NG, A, 18.9, desde='izq', sale=X, hacia='izq', rot=90, z=7)
         + blq(470, 925, 530, 76, NG, h('⭐ lo más importante', 40, f'color:{AM}'), A, 18.9, desde='der', sale=X, hacia='der', pad='0 26px', z=7))
tarjeta('c02-specs', S, 15.0, SPEC)

# ───────── 0:33 · trabajo pesado: capturas de mis redes · precios que rastreo (Mercado Libre, Amazon) · hoy ZenBook → Legion
S = 33.0; A = B.at(S); X = 43.05
tarjeta('c03-tareas', S, 10.6,
        blq(80, 220, 920, 120, NG, h('Trabajo pesado', 76, 'color:#efe8da'), A, 33.2, desde='arriba', sale=X, hacia='arriba', pad='0 40px')
        + blq(80, 370, 600, 116, AM, h('📸 capturas de mis redes', 46), A, 34.8, desde='izq', sale=X, hacia='izq', pad='0 30px')
        + blq(80, 510, 600, 116, RJ, h('🏷️ precios que rastreo', 46, 'color:#faf7f0'), A, 36.9, desde='izq', sale=X, hacia='izq', pad='0 30px')
        + blq(80, 650, 290, 84, CR, h('Mercado Libre', 38), A, 38.9, desde='abajo', sale=X, hacia='izq', pad='0 22px', z=6)
        + blq(390, 650, 290, 84, CR, h('Amazon', 38), A, 39.8, desde='abajo', sale=X, hacia='izq', pad='0 22px', z=6)
        # columna derecha: hoy ZenBook → Legion (el bloque de ZenBook se va arriba y entra el de la Legion)
        + blq(720, 370, 280, 364, AZ, s('hoy', 36, 'color:#faf7f0;font-weight:600') + h('💻<br>ZenBook', 60, 'color:#faf7f0;margin-top:10px;white-space:normal'),
              A, 40.6, desde='der', sale=41.6, hacia='arriba', pad='0 26px')
        + forma('tri', 820, 760, 80, 70, NG, A, 41.6, desde='abajo', sale=X, hacia='der', rot=0, z=6)
        + blq(720, 370, 280, 364, NG, s('ahora', 36, 'color:#f3c11b;font-weight:600') + h('🎮<br>Legion', 64, 'color:#faf7f0;margin-top:10px;white-space:normal'),
              A, 41.9, desde='abajo', sale=X, hacia='der', pad='0 26px', z=6))

# ───────── 0:44 · después: pasar todos los videos a texto, para un análisis
S = 43.9; A = B.at(S); X = 49.25
TERM = ('<div class="mono" style="font-size:36px;line-height:1.6;color:#efe8da">'
        f'<div>{teclea("<span style=color:#f3c11b>$</span> transcribe mis_videos/*.mp4", A, 44.4, .7)}</div>'
        f'<div>{teclea("<span style=color:#f3c11b>→</span> transcripción lista", A, 45.3, .5)}</div>'
        f'<div>{teclea("«Esta laptop me costó 9,000…»", A, 46.2, 1.4)}</div></div>')
tarjeta('c05-texto', S, 5.9,
        blq(80, 260, 920, 330, NG, TERM, A, 44.1, desde='izq', sale=X, hacia='izq', pad='34px 44px')
        + forma('c', 820, 520, 180, 180, AM, A, 48.4, desde='der', sale=X, hacia='der', z=6)
        + blq(300, 620, 560, 100, AZ, h('🔬 para un análisis', 50, 'color:#faf7f0'), A, 48.5, desde='abajo', sale=X, hacia='izq', pad='0 30px', z=7))

# ───────── 0:59 · animaciones 3D: Mac 1× · ZenBook 9× más lenta · Legion con GPU → las 3 juntas, más rápido
S = 58.9; A = B.at(S); X = 68.95
BARRAS = [('🍎 Mac', .12, NG, '1×', 59.7), ('💻 ZenBook', 1.0, RJ, '9× más lento', 61.2), ('🎮 Legion', .24, AZ, 'GPU ⚡', 64.8)]
br = ''
for i, (n, w, c, et, t) in enumerate(BARRAS):
    y = 420 + i * 130
    br += (lab(120, y + 18, h(n, 46), A, t - .3, sale=X, z=8)
           + f'<div class="gr" style="position:absolute;left:400px;top:{y + 8}px;width:{w * 540:.0f}px;height:80px;background:{c};z-index:8;--d:{A(t)}"></div>'
           + lab((400 + w * 540 + 18) if w < 1 else 520, y + (22 if w < 1 else 98), h(et, 42, f'color:{c}'), A, t + .8, sale=X))
tarjeta('c04-render', S, 10.6,
        f'<div class="fm sx x" style="left:0;top:0;width:1080px;height:1920px;--d:{A(59.1)};--fx:0px;--fy:0;--fr:0deg;--sx:-1300px;--sy:0;--sr:0deg;--x:{A(X)}">'
        + blq(80, 230, 920, 620, CR, '<div style="position:absolute;left:44px;top:34px">' + h('Animaciones 3D', 80)
              + s('las de todos mis videos', 38, 'margin-top:8px;font-weight:600;color:#1f4fd6') + '</div>', A, 59.1, desde='izq', pad='0', z=4)
        + br + '</div>'
        + blq(140, 880, 800, 100, AM, h('🤝 las 3 juntas → más rápido', 50), A, 66.3, desde='der', sale=X, hacia='der', pad='0 30px', z=9))

# ───────── 1:10 · escena a pantalla completa: respaldo mutuo (local 0–19.1 → video 69.5–88.6)
S = 69.5; A = B.at(S)


def L(t):
    return round(S + t, 2)


def compu(x, y, cuerpo, tapa, nombre, t, desde, sale=None, hacia='abajo'):
    """Composición geométrica de una laptop: tapa (cuadrado) + base (barra) + nombre."""
    return (forma('sq', x, y, 360, 230, tapa, A, t, desde=desde, sale=sale, hacia=hacia, z=6)
            + forma('sq', x + 30, y + 30, 300, 170, '#faf7f0', A, t + .05, desde=desde, sale=sale, hacia=hacia, z=7)
            + forma('barra', x - 30, y + 240, 420, 46, cuerpo, A, t + .1, desde=desde, sale=sale, hacia=hacia, z=6)
            + blq(x, y + 310, 360, 90, cuerpo, h(nombre, 52, 'color:#faf7f0;text-align:center;width:100%'), A, t + .15, desde=desde, sale=sale, hacia=hacia, pad='0', z=6))


def estado(txt, x, y, color, t, q=None):
    return lab(x, y, h(txt, 40, f'padding:8px 18px;background:{color};color:#faf7f0'), A, t, q, z=12)


SERV = [('🗄️ Base de datos', 9.8), ('⚙️ Servicios', 10.7), ('🧭 Mi hub', 11.4)]
sv = ''
for i, (n, t) in enumerate(SERV):
    y = 1110 + i * 100
    sv += (blq(90, y, 900, 84, CR, f'<div style="display:flex;justify-content:space-between;align-items:center;width:100%">{h(n, 44)}</div>', A, L(t), desde='izq', pad='0 30px', z=6)
           + blq(700, y + 10, 260, 64, NG, h('→ Legion', 40, 'color:#f3c11b'), A, L(t), desde='der', sale=L(15.8), hacia='der', pad='0 22px', z=8)
           + blq(700, y + 10, 260, 64, AZ, h('→ ZenBook', 40, 'color:#faf7f0'), A, L(15.85), desde='der', pad='0 22px', z=8))
TG = (f'<div style="display:flex;align-items:center;gap:26px"><div style="width:100px;height:100px;flex-shrink:0;border-radius:50%;background:#faf7f0;'
      f'display:flex;align-items:center;justify-content:center;padding:14px">{G.logo("telegram", AZ)}</div>'
      f'<div>{s("Telegram · ahora", 34, "color:#faf7f0;opacity:.85;font-weight:600")}{h("La ZenBook se cayó<br>la Legion tomó el control", 46, "color:#faf7f0;white-space:normal;margin-top:6px")}</div></div>')
RESP = (texto(['Respaldo', '[mutuo]'], A, L(.15), y=200, size=150, sale=L(4.8), ac=AZ)
        + texto(['Si se cae la', '[ZenBook]…'], A, L(5.0), y=200, size=128, sale=L(14.3), ac=AZ)
        + texto(['…y si cae la', '[Legion]'], A, L(14.5), y=200, size=128, ac=RJ)
        + compu(100, 560, AZ, AZ, 'ZenBook', L(.4), 'izq', sale=L(5.3), hacia='abajo')
        + compu(100, 560, AZ, AZ, 'ZenBook', L(14.7), 'arriba')
        + compu(620, 560, NG, RJ, 'Legion', L(.9), 'der', sale=L(14.7), hacia='abajo')
        + forma('c', 470, 640, 120, 120, AM, A, L(1.6), desde='abajo', escala=True, z=8, gira=False)
        + estado('● en línea', 110, 1000, '#2b9a5a', L(.6), L(5.3))
        + estado('✕ caída', 130, 700, RJ, L(5.4), L(14.7))
        + estado('● respaldo', 110, 1000, AZ, L(14.8))
        + estado('● respaldo', 640, 1000, AZ, L(1.1), L(6.3))
        + estado('⚡ tomó el control', 600, 1000, '#2b9a5a', L(6.3), L(14.7))
        + estado('✕ caída', 660, 700, RJ, L(14.8))
        + sv
        + blq(90, 1430, 900, 200, AZ, TG, A, L(13.0), desde='der', sale=L(14.3), hacia='der', pad='0 36px', z=9)
        + blq(90, 1430, 900, 150, AM, h('🔁 la ZenBook vuelve a hacer todo', 50), A, L(16.4), desde='abajo', pad='0 36px', z=9))
PIEZAS.append(('s1-respaldo', S, round(S + 19.1, 2),
               B.page(CSS + '.lz.sal{animation:ci .7s cubic-bezier(.7,0,.25,1) both,lzsale .5s cubic-bezier(.7,0,.9,.4) 18.55s forwards}'
                            '@keyframes lzsale{to{transform:translateX(-1200px)}}', RESP, 19.1, S0=S, fondo=CR, entra='sd').replace('class="lz"', 'class="lz sal"', 1)))

# ───────── 1:29 · bases de datos copiadas al segundo → cambio rápido y simple
S = 88.57; A = B.at(S); X = 96.82
CICLO = [(0, 0)]
for i in range(7):
    t0 = 91.17 + i
    CICLO += [(t0, 0.9, 0.9), (t0 + .92, 0.0, .05)]
COPIA = ''.join(f'<div class="cp" style="left:{i * 50}px;--d:{A(89.77 + i * .33)}"></div>' for i in range(3))
tarjeta('c06-replica', S, 8.8,
        forma('c', 100, 240, 340, 340, AZ, A, 89.07, desde='izq', sale=X, hacia='izq')
        + blq(100, 240, 340, 340, 'transparent', '<div style="text-align:center;width:100%">' + h('💻', 70) + h('ZenBook', 52, 'color:#faf7f0;margin-top:8px')
              + s('base de datos', 32, 'color:#faf7f0;margin-top:6px;font-weight:600') + '</div>', A, 89.07, desde='izq', sale=X, hacia='izq', pad='0', z=7)
        + forma('c', 640, 240, 340, 340, RJ, A, 89.47, desde='der', sale=X, hacia='der')
        + blq(640, 240, 340, 340, 'transparent', '<div style="text-align:center;width:100%">' + h('🎮', 70) + h('Legion', 52, 'color:#faf7f0;margin-top:8px')
              + s('copia exacta', 32, 'color:#faf7f0;margin-top:6px;font-weight:600') + '</div>', A, 89.47, desde='der', sale=X, hacia='der', pad='0', z=7)
        + blq(458, 390, 170, 40, 'transparent', f'<div style="position:relative;width:170px;height:34px;overflow:hidden">{COPIA}</div>', A, 89.77, desde='arriba', sale=X, hacia='arriba', pad='0')
        + blq(140, 640, 800, 110, NG, f'<div class="mono" style="font-size:40px;color:#efe8da;white-space:nowrap">⏱ última copia: hace <b style="color:#f3c11b">{N(CICLO, f="1")}</b> s</div>',
              A, 91.0, desde='abajo', sale=X, hacia='izq', pad='0 40px')
        + blq(220, 790, 640, 100, AM, h('⚡ cambio rápido y simple', 50), A, 95.17, desde='der', sale=X, hacia='der', pad='0 30px'))

# ───────── 1:48 · Sígueme + «¿qué le pondrías a una 2.ª compu?» → «Un servidor de Minecraft 😅»
S = 108.37; A = B.at(S); X = 115.05
SEG = (blq(570, 240, 430, 330, AM, s('Sígueme', 40, 'font-weight:600') + h('Armando', 92, 'margin-top:6px') + s('homelab · IA · código', 34, 'margin-top:10px;font-weight:600'),
           A, 108.5, desde='der', sale=X, hacia='der', pad='30px 36px')
       + forma('c', 940, 200, 110, 110, RJ, A, 108.8, desde='arriba', sale=X, hacia='arriba', z=7)
       + blq(600, 600, 370, 100, RJ, h('Seguir ✓', 54, 'color:#faf7f0;text-align:center;width:100%'), A, 109.4, desde='abajo', sale=X, hacia='der', pad='0', z=6)
       + blq(80, 240, 470, 380, CR, h('🖥️ ¿Qué le pondrías<br>a una 2.ª compu?', 44, 'white-space:normal;line-height:1.1')
             + f'<div class="h" style="font-size:42px;color:#1f4fd6;margin-top:22px">{teclea("Un servidor de", A, 111.0, .55)}<br>{teclea("Minecraft 😅", A, 111.6, .45)}</div>',
             A, 109.9, desde='izq', sale=X, hacia='izq', pad='30px 34px')
       + forma('tri', 80, 640, 110, 96, NG, A, 110.2, desde='izq', sale=X, hacia='izq', z=6))
PIEZAS.append(('seguir', S, FIN, B.page(CSS, SEG, round(FIN - S, 2), S0=S, transparente=True)))
PIEZAS.sort(key=lambda p: p[1])

if __name__ == '__main__':
    solo = set(sys.argv[1:])
    for pid, a, b, html in PIEZAS:
        if solo and pid not in solo:
            continue
        path = f'{WORK}/{pid}.html'
        open(path, 'w').write(html)
        if os.environ.get('SOLO_HTML'):
            print('html', path, f'{b - a:.2f}'); continue
        r = subprocess.run(['node', CAP, path, f'{b - a:.2f}', f'{OUT}/{PRE}{pid}.webm'], capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr[-600:], flush=True)
    if not solo:
        rel = os.environ.get('REL', 'videos/10/bauhaus')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
