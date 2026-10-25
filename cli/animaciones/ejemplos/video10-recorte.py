"""Video 10 · la Legion 5 llega al homelab (devlog) · edición «Recorte» (nueva, sin la base gloss ni 3D).
Tarjetas de papel pegadas sobre la cámara (mitad de arriba, sin tapar la demo): etiqueta de precio de cartón con cordel,
hoja de especificaciones con cinta y palomitas, nota adhesiva de pendientes, ticket de transcripción, gráfica de barras
dibujada a mano, diagrama de réplica; una sola escena a pantalla completa (respaldo mutuo) que entra rasgada y sale barrida.
Entradas y salidas con las animaciones de recorte.py (cae/vuela, pega, sello, barrido), todo a 12 cps.
Tiempos = timeline final de videos/10 (115.62 s), los mismos de video10-gloss.py.
Uso: SALIDA=~/Documents/Videos/videos/10/recorte REL=videos/10/recorte python3 ejemplos/video10-recorte.py [ids…]   (SOLO_HTML=1 para revisar)
Los archivos salen con prefijo «gr10-».
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import recorte as K
from recorte import titular, flecha, recorte, nota, sello, ticket, N, logo, mano, fase, subraya, circulo

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.path.expanduser('~/Documents/Videos/videos/10/recorte')))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
PRE = 'gr10-'
FIN = 115.62
PIEZAS = []

CSS = """
.ar{font-weight:900;font-stretch:62%;text-transform:uppercase;line-height:.9}
.cv{font-family:'Caveat',cursive;font-weight:700}
.rw{animation:slam .4s cubic-bezier(.2,1.5,.4,1) var(--d) both}
.on{opacity:0;animation:apar .01s linear var(--d) forwards}
.onoff{opacity:0;animation:apar .01s linear var(--d) forwards,quita .01s linear var(--q) forwards}
@keyframes quita{to{opacity:0}}
.sl.q{animation:sello .32s cubic-bezier(.3,1.7,.5,1) var(--d) both,quita .01s linear var(--q) forwards}
.bar{height:44px;border-radius:8px 18px 10px 20px;transform-origin:left center;transform:scaleX(0) skewX(-6deg);animation:barra .8s steps(8) var(--d) forwards}
@keyframes barra{to{transform:scaleX(1) skewX(-6deg)}}
.cb{position:absolute;width:56px;height:56px;border:6px solid #171513;border-radius:10px}
.nt{min-height:0!important}
"""


def tarjeta(pid, start, dur, body, sale=True):
    """Tarjeta transparente sobre la cámara; al final todo el grupo se barre de la mesa (sin desvanecido)."""
    A = K.at(start)
    if sale:
        body = fase(body, A, sale=round(start + dur - .55, 2))
    PIEZAS.append((pid, start, round(start + dur, 2), K.page(CSS, body, dur, S0=start, transparente=True)))


def check(x, y, s, A, t, color='var(--verde)', grosor=14):
    """Palomita dibujada en coordenadas locales del contenedor."""
    return (f'<svg class="gb" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;--d:{A(t)};--dd:.35s" viewBox="0 0 100 100">'
            f'<path d="M6 55 L38 90 L96 8" pathLength="1" stroke="{color}" stroke-width="{grosor}"/></svg>')


def sq(x, y, txt, A, t, q, size=46, rot=-8.0, color=None):
    """Sello que aparece en t y se quita de golpe en q (cambio de estado)."""
    c = f'color:{color};' if color else ''
    qq = f'--q:{A(q)};' if q else '--q:9999s;'
    return f'<div class="sl q" style="left:{x}px;top:{y}px;font-size:{size}px;--r:{rot}deg;--d:{A(t)};{qq}{c}">{txt}</div>'


def sellop(x, y, txt, A, t, size=56, rot=-6.0, color=None):
    """Sello sobre etiqueta de papel (se lee encima de la cámara)."""
    return sello(x, y, txt, A, t, size=size, rot=rot, color=color).replace('style="', 'style="background:#fbf8f1;-webkit-mask:none;mask:none;box-shadow:0 12px 20px rgba(0,0,0,.35);', 1)


def ar(txt, size=80, extra=''):
    return f'<div class="ar" style="font-size:{size}px;{extra}">{txt}</div>'


def cv(txt, size=48, extra=''):
    return f'<div class="cv" style="font-size:{size}px;line-height:1;{extra}">{txt}</div>'


# ───────── 0:00 · «esta laptop me costó $9,000 pesos usada y va a ser el músculo de mi homelab»
S = 0.2; A = K.at(S)
TAG_CLIP = 'polygon(0 50%,13% 0,100% 0,100% 100%,13% 100%)'
TAG = (f'<div class="rcw" style="left:150px;top:300px;width:660px;height:300px;--r:-6deg;--d:{A(.25)}">'
       f'<div class="rc kraft" style="width:100%;height:100%;padding:34px 40px 30px 120px;clip-path:{TAG_CLIP}">'
       '<i style="position:absolute;left:46px;top:126px;width:44px;height:44px;border-radius:50%;background:#f3ecdf;box-shadow:inset 0 3px 6px rgba(0,0,0,.4)"></i>'
       + cv('mi nueva laptop', 50, 'color:#3b2a12')
       + f'<div class="ar" style="font-size:170px;color:#171513;margin-top:6px;white-space:nowrap">${N([(0, 0), (.9, 9000, .9)], f="c")}'
         '<span style="font-size:50px;margin-left:12px">MXN</span></div></div></div>'
       # cordel
       f'<svg class="gb" style="left:0;top:0;width:1080px;height:1920px;--d:{A(.35)};--dd:.5s;z-index:14" viewBox="0 0 1080 1920">'
       '<path d="M60 250 C110 330,150 380,210 455" pathLength="1" stroke="#7a5a2a" stroke-width="7"/></svg>')
tarjeta('c01-precio', S, 4.1,
        TAG
        + sellop(600, 545, '♻️ usada', A, 2.0, size=62, rot=9)
        + recorte(120, 680, 740, 116, ar('💪 el músculo de mi homelab', 54, 'color:#fff;white-space:nowrap'), A, 2.8, rot=-2, cls='rojo', seed=40, pad='26px 34px', cinta=False))

# ───────── 0:08 · Ryzen 7 (8 núcleos · 16 hilos) · 16 GB de RAM expandible · ⭐ lo más importante: RTX 3050 Ti de 4 GB
S = 8.3; A = K.at(S)
FILAS = [('Ryzen 7', '8 núcleos · 16 hilos', 9.0), ('16 GB de RAM', 'y se puede expandir', 13.2), ('RTX 3050 Ti', '4 GB de memoria', 20.8)]
fl = ''
for i, (n, s_, t) in enumerate(FILAS):
    y = 170 + i * 118
    fl += (f'<div class="rw" style="position:absolute;left:40px;top:{y}px;--d:{A(t)}"><i class="cb" style="left:0;top:4px"></i>'
           f'<div style="margin-left:84px">{ar(n, 66)}{cv(s_, 40, "color:#6b6457;margin-top:2px")}</div></div>'
           + check(36, y - 14, 72, A, t + .35))
HOJA = recorte(150, 270, 780, 540,
               ar('Lenovo Legion 5', 74) + cv('la encontré en Marketplace', 44, 'color:var(--azul);margin-top:4px') + fl,
               A, 8.5, rot=-1.5, cls='crema', seed=41, pad='34px 40px')
tarjeta('c02-specs', S, 15.0,
        HOJA
        + sellop(380, 830, '⭐ lo más importante', A, 18.9, size=50, rot=-6)
        + circulo(450, 722, 440, 120, A, 20.95, seed=42, grosor=8)
        + logo('', 830, 600, 150, A, 20.8, rot=10, bg='#2457e6', emoji='🎮'))

# ───────── 0:33 · trabajo pesado: capturas de mis redes · precios que rastreo (Mercado Libre, Amazon) · hoy ZenBook → Legion
S = 33.0; A = K.at(S)
PEND = (f'<div style="font-size:60px;text-decoration:underline;text-decoration-thickness:4px">Trabajo pesado</div>'
        f'<div class="on" style="--d:{A(34.8)};margin-top:14px">📸 capturas de mis redes</div>'
        f'<div class="on" style="--d:{A(36.9)};margin-top:6px">🏷️ precios que rastreo</div>')
tarjeta('c03-tareas', S, 10.6,
        nota(110, 280, PEND, A, 33.2, rot=-3, w=580, size=50)
        + logo('', 760, 280, 170, A, 38.8, rot=-8, bg='#ffe600', emoji='🤝')
        + recorte(735, 455, 230, 66, ar('Mercado Libre', 34, 'white-space:nowrap'), A, 38.9, rot=-5, cls='amarillo', seed=46, pad='14px 18px', cinta=False, z=19)
        + logo('amazon', 800, 520, 170, A, 39.8, rot=7, bg='#fff')
        + recorte(90, 730, 420, 120, ar('💻 hoy: ZenBook', 50, 'white-space:nowrap'), A, 40.6, rot=-2, seed=43, pad='32px 30px', cinta=False, z=20)
        + flecha(520, 795, 605, 790, A, 41.6, curva=-.3)
        + recorte(615, 710, 360, 150, ar('🎮 Legion', 66, 'color:#fff;white-space:nowrap'), A, 41.9, rot=3, cls='rojo', seed=44, pad='38px 34px', z=20))

# ───────── 0:44 · después: pasar todos los videos a texto, para un análisis
S = 43.9; A = K.at(S)
tarjeta('c05-texto', S, 5.9,
        ticket(130, 290, 820, [('<i>$</i> transcribe mis_videos/*.mp4', 44.4, .7), ('<i>→</i> <b>transcripción</b> lista', 45.3, .5),
                               ('«Esta laptop me costó 9,000…»', 46.2, 1.4)], A, rot=-1.5, size=36)
        + sellop(500, 600, '🔬 para un análisis', A, 48.5, size=56, rot=-5))

# ───────── 0:59 · animaciones 3D: Mac 1× · ZenBook 9× más lenta · Legion con GPU → las 3 juntas, más rápido
S = 58.9; A = K.at(S)
BARRAS = [('🍎 Mac', '11%', 'var(--tinta)', '1×', 59.7, 'var(--tinta)'), ('💻 ZenBook', '100%', 'var(--rojo)', '9× más lento', 61.2, 'var(--rojo)'),
          ('🎮 Legion', '22%', 'var(--verde)', 'GPU ⚡', 64.8, 'var(--verde)')]
br = ''
for i, (n, w, c, x, t, cc) in enumerate(BARRAS):
    y = 150 + i * 110
    br += (f'<div class="rw" style="position:absolute;left:40px;top:{y}px;--d:{A(t - .3)}">{ar(n, 50)}</div>'
           f'<div style="position:absolute;left:290px;right:40px;top:{y + 4}px"><div class="bar" style="width:{w};background:{c};--d:{A(t)}"></div></div>'
           + (f'<div class="cv on" style="position:absolute;right:60px;top:{y + 46}px;font-size:40px;color:{cc};--d:{A(t + .8)}">{x}</div>' if w == '100%' else
              f'<div class="cv on" style="position:absolute;left:{290 + float(w[:-1]) / 100 * 530 + 18:.0f}px;top:{y - 2}px;font-size:46px;color:{cc};--d:{A(t + .8)}">{x}</div>'))
GRAF = recorte(110, 270, 860, 500,
               ar('Animaciones 3D', 70) + cv('las de todos mis videos', 42, 'color:#6b6457') + br,
               A, 59.1, rot=1.2, cls='crema', seed=45, pad='34px 40px')
tarjeta('c04-render', S, 10.6,
        GRAF + sellop(220, 760, '🤝 las 3 juntas → más rápido', A, 66.3, size=50, rot=-4, color='var(--verde)'))

# ───────── 1:10 · escena a pantalla completa: respaldo mutuo (local 0–19.1 → video 69.5–88.6)
S = 69.5; A = K.at(S)


def L(t):
    return S + t


def laptop(x, nombre, rol, color, t, seed):
    ic = (f'<div style="margin:0 auto 14px;width:200px"><div style="height:120px;border-radius:12px 12px 0 0;border:8px solid #171513;background:{color}"></div>'
          '<div style="height:18px;margin:0 -24px;border-radius:0 0 14px 14px;background:#171513"></div></div>')
    return recorte(x, 620, 430, 380, f'<div style="text-align:center">{ic}{ar(nombre, 70)}'
                                       f'<div class="cv" style="font-size:42px;color:#6b6457">{rol}</div></div>', A, L(t), rot=[-2, 2][seed % 2], seed=seed, pad='40px 30px')


SERV = [('🗄️ Base de datos', 9.8), ('⚙️ Servicios', 10.7), ('🧭 Mi hub', 11.4)]
sv = ''
for i, (n, t) in enumerate(SERV):
    y = 34 + i * 92
    sv += (f'<div class="rw" style="position:absolute;left:40px;top:{y}px;--d:{A(L(t))}">{ar(n, 56)}</div>'
           f'<div class="ar onoff" style="position:absolute;right:40px;top:{y + 6}px;font-size:46px;color:var(--verde);--d:{A(L(t))};--q:{A(L(15.8))}">→ Legion</div>'
           f'<div class="ar on" style="position:absolute;right:40px;top:{y + 6}px;font-size:46px;color:var(--azul);--d:{A(L(15.8))}">→ ZenBook</div>')
TG = (f'<div style="display:flex;align-items:center;gap:26px;height:100%"><div style="width:96px;height:96px;flex-shrink:0;border-radius:24px;background:#fff;'
      f'display:flex;align-items:center;justify-content:center">{K.G.logo("telegram", "#2457e6")}</div>'
      '<div><div class="cv" style="font-size:40px;opacity:.85">Telegram · ahora</div>'
      f'{ar("La ZenBook se cayó · la Legion tomó el control", 46)}</div></div>')
RESP = (titular(['Respaldo', '*mutuo*'], A, L(.1), x=L(4.8), top=300, size=170, seed=46)
        + titular(['Si se cae la', '*ZenBook*…'], A, L(5.0), x=L(14.3), top=300, size=150, seed=47)
        + titular(['…y si cae la', '*Legion*'], A, L(14.5), top=300, size=150, seed=48)
        + laptop(70, 'ZenBook', 'hoy hace todo', '#6ea8ff', .4, 51) + laptop(580, 'Legion', 'la nueva', '#c86bff', .9, 52)
        + flecha(500, 760, 580, 760, A, L(1.6), color='var(--tinta)', curva=-.4, grosor=8) + flecha(580, 860, 500, 860, A, L(1.8), color='var(--tinta)', curva=-.4, grosor=8)
        # estados (cambian de golpe)
        + sq(150, 940, '● en línea', A, L(.6), L(5.2), size=40, rot=-4, color='var(--verde)')
        + sq(110, 760, '✕ caída', A, L(5.3), L(14.6), size=76, rot=-12)
        + sq(140, 940, '● respaldo', A, L(14.7), None, size=40, rot=-4, color='var(--azul)')
        + sq(670, 940, '● respaldo', A, L(1.1), L(6.2), size=40, rot=4, color='var(--azul)')
        + sq(600, 935, '⚡ tomó el control', A, L(6.3), L(14.6), size=40, rot=4, color='var(--verde)')
        + sq(630, 760, '✕ caída', A, L(14.7), None, size=76, rot=10)
        + recorte(90, 1070, 900, 330, sv, A, L(9.6), rot=-1, cls='crema', seed=53, pad='0')
        + recorte(90, 1440, 900, 190, TG, A, L(13.0), sale=L(14.3), rot=1.5, cls='azul', seed=54, pad='30px 40px')
        + nota(200, 1440, '🔁 la ZenBook vuelve a hacer todo', A, L(16.4), rot=-3, w=680, size=62))
PIEZAS.append(('s1-respaldo', S, round(S + 19.1, 2),
               K.page(CSS + 'body{animation:sale .5s cubic-bezier(.6,0,.9,.4) 18.55s forwards}@keyframes sale{to{transform:translate(-1250px,260px) rotate(-14deg)}}',
                      RESP, 19.1, S0=S, fondo='papel', seed=9, ac='var(--azul)')))

# ───────── 1:29 · bases de datos copiadas al segundo → cambio rápido y simple
S = 88.57; A = K.at(S)
CICLO = [(0, 0)]
for i in range(7):
    t0 = 91.17 + i
    CICLO += [(t0, 0.9, 0.9), (t0 + .92, 0.0, .05)]
tarjeta('c06-replica', S, 8.8,
        recorte(110, 290, 360, 230, f'<div style="text-align:center">{ar("💻 ZenBook", 56)}{cv("base de datos", 40, "color:#6b6457")}</div>', A, 89.07, rot=-3, seed=55, pad='44px 20px')
        + recorte(610, 290, 360, 230, f'<div style="text-align:center">{ar("🎮 Legion", 56)}{cv("copia exacta", 40, "color:#6b6457")}</div>', A, 89.47, rot=3, seed=56, pad='44px 20px')
        + flecha(485, 360, 595, 360, A, 89.77, color='var(--verde)', curva=-.35) + flecha(595, 450, 485, 450, A, 89.97, color='var(--verde)', curva=-.35)
        + ticket(190, 600, 700, [(f'<i>⏱</i> última copia: hace <b>{N(CICLO, f="1")}</b> s', 91.17, .6)], A, rot=-1)
        + sellop(290, 790, '⚡ cambio rápido y simple', A, 95.17, size=50, rot=-6, color='var(--verde)'))

# ───────── 1:48 · Sígueme + «¿qué le pondrías a una 2.ª compu?» → «Un servidor de Minecraft 😅»
S = 108.37; A = K.at(S)
_r = 'Un servidor de Minecraft 😅'
SEG = (nota(600, 300, '<div style="font-size:42px">Sígueme</div><div class="ar" style="font-size:88px;font-family:Archivo">Armando</div>'
            '<div style="font-size:38px;margin-top:6px">homelab · IA · código</div>', A, 108.5, rot=4, w=390, size=56)
       + sellop(640, 690, 'Seguir ✓', A, 109.4, size=60, rot=-5, color='var(--verde)')
       + recorte(80, 330, 480, 330, '<div class="ser" style="font-size:44px;line-height:1.1">🖥️ ¿Qué le pondrías a una 2.ª compu?</div>'
                 f'<div style="margin-top:20px;font-family:Caveat;font-weight:700;font-size:38px;color:var(--azul);white-space:nowrap;'
                 f'clip-path:inset(0 100% 0 0);animation:tip 1s steps({len(_r) + 1}) {A(111.0)} forwards">{_r}</div>',
                 A, 109.9, rot=-3, seed=57))
PIEZAS.append(('seguir', S, FIN, K.page(CSS, SEG, round(FIN - S, 2), S0=S, transparente=True)))
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
        rel = os.environ.get('REL', 'videos/10/recorte')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
