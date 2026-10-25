"""Video 10 · la Legion 5 llega al homelab (devlog) · edición «Escritorio» (idea nueva, sin gloss ni recorte).
Ventanas de LogOS, un sistema operativo retro inventado (System 7 / Windows 98), flotando sobre la cámara en la mitad de arriba:
anuncio de Mercado Libre con el precio que cuenta y el cursor que pulsa «Comprar», «Propiedades del sistema» con las specs,
«Administrador de tareas» que pasa el trabajo de la ZenBook a la Legion, terminal que transcribe, monitor de rendimiento,
diálogo de copia de la base de datos y ventana de perfil para el «Sígueme». Una sola escena a pantalla completa (respaldo mutuo):
escritorio que se enciende como monitor viejo, diálogos de error que sacuden y se apaga en una línea al final.
Nada se desvanece: las ventanas abren y cierran con los rectángulos de zoom del sistema, los textos se teclean.
Tiempos = timeline final de videos/10 (115.62 s), los mismos de video10-gloss.py / video10-recorte.py.
Uso: SALIDA=~/Documents/Videos/videos/10/escritorio REL=videos/10/escritorio python3 ejemplos/video10-escritorio.py [ids…]   (SOLO_HTML=1 para revisar)
Los archivos salen con prefijo «gre10-».
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import escritorio as E
import ellog as _L
from escritorio import ventana, teclea, grande, dialogo, progreso, N, icono, cursor, grafica, ap, sprite

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.path.expanduser('~/Documents/Videos/videos/10/escritorio')))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
PRE = 'gre10-'
FIN = 115.62
PIEZAS = []

CSS = """
.px{font-family:'Jersey 15';font-weight:700;line-height:1}
.pl{font-family:'IBM Plex Sans',sans-serif;font-weight:600}
.gr{color:#5a5a5a}
.ab{position:absolute}
.row{position:absolute;left:0;right:0;display:flex;align-items:center;gap:22px}
.tab{position:absolute;left:0;right:0;display:grid;grid-template-columns:1fr 210px 150px;align-items:center;font-family:'IBM Plex Sans';font-weight:600;font-size:34px;padding:0 6px}
.tab.hd{font-family:'Jersey 15';font-size:28px;background:#c3c3c3;box-shadow:inset -2px -2px 0 #828282,inset 2px 2px 0 #fff;height:48px}
.chipv{display:inline-block;padding:4px 14px;font-family:'Jersey 15';font-size:30px;font-weight:700;color:#fff}
.vu{position:absolute;inset:0;visibility:hidden;animation:ab .01s steps(1) var(--d) forwards}
.vu.x{animation:ab .01s steps(1) var(--d) forwards,ci .01s steps(1) var(--x) forwards}
.vuela{animation:vuela 1s steps(8) var(--d) infinite}
@keyframes vuela{0%{transform:translate(0,0)}50%{transform:translate(210px,-60px)}100%{transform:translate(420px,0)}}
.gbar{height:46px;padding:4px;background:#fff;box-shadow:inset 3px 3px 0 #828282,inset -3px -3px 0 #fff,inset 6px 6px 0 #0a0a0a}
.gbar b{display:block;height:100%;width:0;background:repeating-linear-gradient(90deg,var(--pc) 0 26px,transparent 26px 32px)}
/* al cerrar, recorta la ventana entera: los hijos con visibility propia (ap/vu/botones) no se quedan flotando */
.vn.x{animation:ab .01s steps(1) var(--d) forwards,ci .01s steps(1) var(--x) forwards,cierra .01s steps(1) var(--x) forwards}
.vn.sac.x{animation:ab .01s steps(1) var(--d) forwards,sac .4s steps(6) var(--d),ci .01s steps(1) var(--x) forwards,cierra .01s steps(1) var(--x) forwards}
@keyframes cierra{to{clip-path:inset(50% 50%)}}
.oc{position:absolute;inset:0;animation:cierra .01s steps(1) var(--x) forwards}
"""


def tarjeta(pid, start, dur, body):
    PIEZAS.append((pid, start, round(start + dur, 2), E.page(CSS, body, dur, S0=start, transparente=True)))


def vu(html, A, t, sale=None):
    """Capa absoluta que aparece de golpe en t y desaparece en sale (cambio de estado sin desvanecido)."""
    cls, st = 'vu', f'--d:{A(t)};'
    if sale is not None:
        cls += ' x'; st += f'--x:{A(sale)};'
    return f'<div class="{cls}" style="{st}">{html}</div>'


def oculta(html, A, t):
    """Recorta de golpe todo lo de adentro en t (para cursores que deben irse con su ventana)."""
    return f'<div class="oc" style="--x:{A(t)}">{html}</div>'


def caja(h, html):
    """Contenido con alto fijo (las piezas internas se colocan con .ab en coordenadas conocidas)."""
    return f'<div style="position:relative;height:{h}px">{html}</div>'


def btn(txt, A=None, pulsa=None, extra=''):
    pr = f' pr" style="--p:{A(pulsa)};{extra}' if pulsa is not None else f'" style="{extra}'
    return f'<span class="btn def{pr}">{txt}</span>'


def tg_logo(size=56):
    return _L.logo('telegram', '#fff', size)


# ───────── 0:00 · «esta laptop me costó $9,000 pesos usada y va a ser el músculo de mi homelab»
S = 0.2; A = E.at(S)
X, Y = 90, 200          # ventana; el contenido empieza en (X+5+28, Y+63+24)
AN = caja(330,
          f'<div class="ab" style="left:0;top:0">{sprite("compu", 170)}</div>'
          f'<div class="ab px" style="left:200px;top:4px;font-size:58px">Lenovo Legion 5</div>'
          f'<div class="ab pl gr" style="left:202px;top:76px;font-size:32px">{teclea("Ryzen 7 · RTX 3050 Ti · 15.6″", A, .5)}</div>'
          f'<div class="ab px" style="left:200px;top:130px;font-size:120px;white-space:nowrap">${N([(0, 0), (.9, 9000, .9)], f="c")}<span style="font-size:44px"> MXN</span></div>'
          f'<div class="ab" style="left:0;top:206px">{ap(f"""<span class="chipv" style="background:#14a046">♻️ USADA</span>""", A, 2.0)}</div>'
          f'<div class="ab" style="left:560px;top:262px">{btn("Comprar", A, 2.55)}</div>')
CUR = oculta(cursor([(.6, 960, 980), (2.25, 690, 570), (2.55, 690, 570, True), (3.3, 720, 640)]), A, 4.05)
tarjeta('c01-precio', S, 4.1,
        ventana(X, Y, 900, 'Mercado Libre — Legion 5 usada', AN, A, .25, sale=4.05, h=420, icono='mundo', desde=(540, 1500))
        + dialogo(150, 690, 780, 'info', 'Va a ser el <b>músculo</b> de mi homelab 💪', A, 2.8, botones=('¡Sí!',), sale=4.05, titulo='LogOS', desde=(690, 570), z=45)
        + CUR)

# ───────── 0:08 · Ryzen 7 (8 núcleos · 16 hilos) · 16 GB de RAM expandible · ⭐ lo más importante: RTX 3050 Ti de 4 GB
S = 8.3; A = E.at(S)
X, Y = 70, 170
FILAS = [('chip', 'Procesador', 'Ryzen 7', '8 núcleos · 16 hilos', 9.0), ('servidor', 'Memoria', '16 GB de RAM', 'y se puede expandir', 13.2),
         ('chip', 'Gráficos', 'RTX 3050 Ti', '4 GB de memoria', 20.8)]
fl = ''
for i, (sp, lab, val, sub, t) in enumerate(FILAS):
    y = 150 + i * 150
    v = f'<span class="sl" style="--s:{A(t + .9)}">{val}</span>' if i == 2 else val
    fl += ap(f'<div class="ab" style="left:0;top:{y}px">{sprite(sp, 96)}</div>'
             f'<div class="ab pl gr" style="left:120px;top:{y - 4}px;font-size:28px">{lab}</div>'
             f'<div class="ab px" style="left:120px;top:{y + 30}px;font-size:60px;white-space:nowrap">{v}</div>'
             f'<div class="ab pl gr" style="left:540px;top:{y + 44}px;font-size:32px;white-space:nowrap">{teclea(sub, A, t + .3)}</div>', A, t)
PROP = caja(600,
            f'<div class="ab" style="left:0;top:0">{sprite("compu", 110)}</div>'
            f'<div class="ab px" style="left:130px;top:6px;font-size:56px">Lenovo Legion 5</div>'
            f'<div class="ab pl gr" style="left:132px;top:72px;font-size:30px">{teclea("la encontré en Marketplace", A, 8.9)}</div>'
            '<div class="ab" style="left:0;right:0;top:128px;height:3px;background:#828282;box-shadow:0 3px 0 #fff"></div>'
            + fl)
CUR = oculta(cursor([(17.6, 980, 1000), (18.6, 330, 600), (20.9, 330, 630, True), (22.3, 560, 760)]), A, 23.05)
tarjeta('c02-specs', S, 15.0,
        ventana(X, Y, 940, 'Propiedades del sistema', PROP, A, 8.5, sale=23.05, h=700, icono='compu', desde=(540, 1500))
        + dialogo(170, 880, 760, 'alerta', '⭐ <b>Lo más importante:</b><br>la tarjeta gráfica.', A, 18.9, botones=('Ver',), pulsa=20.9, sale=20.85, titulo='Nota', desde=(330, 640), z=45)
        + CUR)

# ───────── 0:33 · trabajo pesado: capturas de mis redes · precios que rastreo (Mercado Libre, Amazon) · hoy ZenBook → Legion
S = 33.0; A = E.at(S)
X, Y = 70, 170
TAREAS = [('📸 Capturas de mis redes', 34.8, 96), ('🏷️ Precios · Mercado Libre', 38.9, 88), ('🏷️ Precios · Amazon', 39.8, 91)]
rows = '<div class="tab hd" style="top:0"><span>Tarea</span><span>Equipo</span><span>CPU</span></div>'
for i, (n, t, cpu) in enumerate(TAREAS):
    y = 64 + i * 92
    eq = (vu('<span class="chipv" style="background:#0a1f8f">💻 ZenBook</span>', E.at(S), t, 41.9)
          + vu('<span class="chipv" style="background:#d8262a">🎮 Legion</span>', E.at(S), 41.9 + i * .12))
    rows += ap(f'<div class="tab" style="top:{y}px;height:80px;border-bottom:2px dotted #c3c3c3"><span style="white-space:nowrap">{n}</span>'
               f'<span style="position:relative;height:50px">{eq}</span>'
               f'<span class="px" style="font-size:40px">{N([(0, 0), (t + .2, cpu, .6), (41.9 + i * .12, 18 + i * 3, .5)], suf="%")}</span></div>', A, t)
TM = caja(470,
          rows
          + '<div class="ab pl" style="left:6px;top:360px;font-size:32px">' + ap('Corriendo en: <b>💻 ZenBook</b>', A, 40.6, 41.9)
          + ap('Corriendo en: <b style="color:#d8262a">🎮 Legion</b>', A, 41.9) + '</div>'
          + f'<div class="ab" style="left:560px;top:350px">{btn("Mover a Legion", A, 41.6, "min-width:300px")}</div>')
CUR = oculta(cursor([(39.9, 1000, 1000), (41.3, 720, 600), (41.6, 720, 600, True), (42.7, 820, 760)]), A, 43.35)
tarjeta('c03-tareas', S, 10.6,
        ventana(X, Y, 940, 'Administrador de tareas — trabajo pesado', TM, A, 33.25, sale=43.35, h=570, icono='chip', desde=(540, 1500))
        + CUR)

# ───────── 0:44 · después: pasar todos los videos a texto, para un análisis
S = 43.9; A = E.at(S)
TERM = (f'<div>{teclea("$ transcribe mis_videos/*.mp4", A, 44.4, .7)}</div>'
        f'<div style="color:#ffd400">{teclea("[##########] 100 %", A, 45.1, .3)}</div>'
        f'<div>{teclea("→ transcripción lista", A, 45.3, .5)}</div>'
        f'<div style="color:#fff">{teclea("«Esta laptop me costó 9,000…»", A, 46.2, 1.2)}<span class="car"></span></div>')
tarjeta('c05-texto', S, 5.9,
        ventana(90, 200, 900, 'Terminal — transcribir', TERM, A, 44.1, sale=49.55, icono='archivo', cu='negro', desde=(540, 1500), h=330)
        + dialogo(170, 590, 740, 'info', 'Texto listo <b>para un análisis</b> 🔬', A, 48.5, botones=('Abrir',), sale=49.55, titulo='LogOS', desde=(540, 420), z=45))

# ───────── 0:59 · animaciones 3D: Mac 1× · ZenBook 9× más lenta · Legion con GPU → las 3 juntas, más rápido
S = 58.9; A = E.at(S)
X, Y = 70, 160
BARRAS = [('🍎 Mac', 11, '#0a0a0a', '1×', 59.7), ('💻 ZenBook', 100, '#d8262a', '9× más lento', 61.2), ('🎮 Legion', 22, '#14a046', 'GPU ⚡', 64.8)]
br = ''
for i, (n, w, c, lab, t) in enumerate(BARRAS):
    y = 20 + i * 120
    br += ap(f'<div class="ab px" style="left:0;top:{y + 4}px;font-size:44px;white-space:nowrap">{n}</div>'
             f'<div class="ab gbar" style="left:260px;right:0;top:{y}px;--pc:{c}"><b data-k=\'{json.dumps([[0, 0], [t, w, .8]])}\'></b></div>'
             f'<div class="ab pl" style="left:{260 if w > 60 else 260 + w * 5.8 + 24:.0f}px;top:{y + 56 if w > 60 else y + 4}px;font-size:{30 if w > 60 else 36}px;color:{c};white-space:nowrap">'
             f'{ap(lab, A, t + .8)}</div>', A, t - .3)
MON = caja(400, f'<div class="ab pl gr" style="left:0;top:-14px;font-size:28px">Animaciones 3D de todos mis videos</div>'
          + f'<div style="position:absolute;inset:30px 0 0 0">{br}</div>')
tarjeta('c04-render', S, 10.6,
        ventana(X, Y, 940, 'Monitor de rendimiento — render 3D', MON, A, 59.1, sale=69.25, h=500, icono='chip', desde=(540, 1500))
        + ventana(560, 690, 450, 'GPU — Legion', grafica(410, 190, [(0, 8), (64.8, 22, .4), (65.4, 88, 1.2)], ruido=5), A, 64.9, sale=69.25, cu='negro', h=270, desde=(800, 520), z=24)
        + dialogo(70, 700, 470, 'info', 'Las 3 juntas<br>→ <b>más rápido</b> 🤝', A, 66.3, botones=('OK',), sale=69.25, titulo='LogOS', desde=(300, 600), z=45))

# ───────── 1:10 · escena a pantalla completa: respaldo mutuo (local 0–19.1 → video 69.5–88.6)
S = 69.5; A = E.at(S)


def L(t):
    return S + t


def maquina(x, nombre, spr, estados, t0):
    """Ventana de una máquina con su estado; estados = [(html, entra, sale)]."""
    est = ''.join(vu(f'<div class="ab px" style="left:0;right:0;top:250px;text-align:center;font-size:40px;white-space:nowrap">{h}</div>', A, a, b) for h, a, b in estados)
    body = caja(320, f'<div class="ab" style="left:50%;top:6px;transform:translateX(-50%)">{sprite(spr, 150)}</div>'
                     f'<div class="ab px" style="left:0;right:0;top:170px;text-align:center;font-size:62px">{nombre}</div>' + est)
    return body


ZB = maquina(60, 'ZenBook', 'compu', [('<span style="color:#14a046">● en línea</span>', L(.6), L(5.3)), ('<span style="color:#d8262a">✕ no responde</span>', L(5.3), L(14.7)),
                                       ('<span style="color:#0a1f8f">● respaldo</span>', L(14.7), None)], .4)
LG = maquina(560, 'Legion', 'servidor', [('<span style="color:#0a1f8f">● respaldo</span>', L(1.1), L(6.3)), ('<span style="color:#14a046">⚡ tomó el control</span>', L(6.3), L(14.7)),
                                          ('<span style="color:#d8262a">✕ no responde</span>', L(14.7), None)], .9)
SERV = [('🗄️ Base de datos', 9.8), ('⚙️ Servicios', 10.7), ('🧭 Mi hub', 11.4)]
sv = ''
for i, (n, t) in enumerate(SERV):
    y = 6 + i * 84
    sv += ap(f'<div class="ab pl" style="left:0;top:{y}px;font-size:42px;white-space:nowrap">{n}</div>'
             f'<div class="ab" style="right:0;top:{y + 4}px;width:260px;height:56px">'
             + vu('<span class="chipv" style="background:#d8262a;float:right">→ Legion</span>', A, L(t), L(15.8))
             + vu('<span class="chipv" style="background:#0a1f8f;float:right">→ ZenBook</span>', A, L(15.8) + i * .15) + '</div>', A, L(t))
TITS = (vu(f'<div style="padding-top:4px">{grande(["Respaldo _mutuo_"], A, L(.2), size=96)}</div>', A, L(.1), L(5.0))
        + vu(f'<div style="padding-top:4px">{grande(["Si se cae la *ZenBook*…"], A, L(5.0), size=86)}</div>', A, L(5.0), L(14.5))
        + vu(f'<div style="padding-top:4px">{grande(["…y si cae la *Legion*"], A, L(14.5), size=86)}</div>', A, L(14.5)))
RESP = (icono(80, 1620, 'compu', 'ZenBook', A, L(.25)) + icono(330, 1620, 'servidor', 'Legion', A, L(.25)) + icono(580, 1620, 'archivo', 'respaldo.db', A, L(.25))
        + icono(830, 1620, 'carpeta', 'Mi hub', A, L(.25))
        + ventana(40, 110, 1000, 'Bloc de notas — respaldo.txt', caja(120, TITS), A, L(.15), h=220, icono='archivo', desde=(540, 900))
        + ventana(40, 370, 480, 'ZenBook', ZB, A, L(.4), h=420, icono='compu', desde=(175, 1680), t1='#0a1f8f')
        + ventana(560, 370, 480, 'Legion', LG, A, L(.9), h=420, icono='servidor', desde=(425, 1680), t1='#7a1414', t2='#d8262a')
        + dialogo(110, 840, 860, 'error', '<b>ZenBook no responde.</b><br>La Legion toma el control.', A, L(5.3), botones=('Aceptar',), pulsa=L(8.6), sale=L(8.9),
                  titulo='Error del sistema', sacude=True, z=50)
        + ventana(40, 840, 1000, 'Servicios', caja(250, sv), A, L(9.6), h=350, icono='chip', desde=(540, 1000))
        + ventana(110, 1240, 860, 'Telegram',
                  f'<div style="display:flex;align-items:center;gap:24px"><div style="width:84px;height:84px;flex-shrink:0;background:#2a9fd6;display:flex;align-items:center;justify-content:center">{tg_logo(56)}</div>'
                  f'<div class="pl" style="font-size:34px;line-height:1.2">La ZenBook se cayó ·<br><b>la Legion tomó el control</b></div></div>',
                  A, L(13.0), sale=L(14.3), icono='info', z=48, t1='#1c6ea4', t2='#2a9fd6', desde=(980, 120))
        + dialogo(110, 1240, 860, 'error', '<b>Legion no responde.</b><br>Regresa todo a la ZenBook.', A, L(14.7), botones=('Aceptar',), pulsa=L(16.1), sale=L(16.35),
                  titulo='Error del sistema', sacude=True, z=50)
        + dialogo(110, 1240, 860, 'info', '🔁 <b>La ZenBook vuelve a hacer todo.</b>', A, L(16.4), botones=('OK',), titulo='LogOS', desde=(540, 1240), z=50)
        + cursor([(L(6.8), 900, 1500), (L(8.3), 470, 1035), (L(8.6), 470, 1035, True), (L(12.4), 820, 1150), (L(15.8), 470, 1435), (L(16.1), 470, 1435, True), (L(17.5), 760, 1560)]))
# el monitor «se enciende» al entrar y «se apaga» en una línea al final (sin desvanecidos)
CRT = """
.mesa{animation:crtOn .35s steps(5) both,crtOff .4s steps(6) 18.6s forwards}
@keyframes crtOn{0%{transform:scale(0,.004);filter:brightness(4)}40%{transform:scale(1,.004);filter:brightness(4)}100%{transform:none;filter:none}}
@keyframes crtOff{0%{transform:none}55%{transform:scale(1,.004);filter:brightness(4)}100%{transform:scale(0,.004);filter:brightness(4)}}
"""
PIEZAS.append(('s1-respaldo', S, round(S + 19.1, 2), E.page(CSS + CRT, RESP, 19.1, S0=S)))

# ───────── 1:29 · bases de datos copiadas al segundo → cambio rápido y simple
S = 88.57; A = E.at(S)
CICLO = [(0, 0)]
for i in range(7):
    t0 = 91.17 + i
    CICLO += [(t0, 0.9, 0.9), (t0 + .92, 0.0, .05)]
PROG = [(0, 0)]
for i in range(8):
    t0 = 90.2 + i
    PROG += [(t0, 100, .85), (t0 + .9, 0, .05)]
COPIA = caja(430,
             f'<div class="ab" style="left:20px;top:10px;text-align:center;width:200px">{sprite("compu", 130)}<div class="px" style="font-size:40px;margin-top:6px">ZenBook</div></div>'
             f'<div class="ab" style="right:20px;top:10px;text-align:center;width:200px">{sprite("servidor", 130)}<div class="px" style="font-size:40px;margin-top:6px">Legion</div></div>'
             f'<div class="ab" style="left:200px;top:40px">{ap(f"""<div class="vuela" style="--d:{A(90.2)}">{sprite("archivo", 72)}</div>""", A, 90.2)}</div>'
             f'<div class="ab pl" style="left:0;right:0;top:230px;font-size:34px">Copiando <b>respaldo.db</b> → Legion</div>'
             f'<div class="ab" style="left:0;right:0;top:282px">{progreso(PROG, "#14a046")}</div>'
             f'<div class="ab px" style="left:0;right:0;top:360px;font-size:44px">{ap("⏱ última copia: hace " + N(CICLO, f="1") + " s", A, 91.17)}</div>')
tarjeta('c06-replica', S, 8.8,
        ventana(80, 200, 920, 'Copiando base de datos…', COPIA, A, 88.85, sale=97.12, h=530, icono='archivo', cu='gris', desde=(540, 1500))
        + dialogo(160, 790, 760, 'info', '⚡ Cambio <b>rápido y simple</b>', A, 95.17, botones=('OK',), sale=97.12, titulo='LogOS', desde=(540, 700), z=45))

# ───────── 1:48 · Sígueme + «¿qué le pondrías a una 2.ª compu?» → «Un servidor de Minecraft 😅»
S = 108.37; A = E.at(S)
PERF = caja(210,
            '<div class="ab" style="left:0;top:0;width:180px;height:180px;background:#0a1f8f;color:#fff;display:flex;align-items:center;justify-content:center;'
            'font-family:Jersey 15;font-weight:700;font-size:120px;box-shadow:inset -4px -4px 0 #000,inset 4px 4px 0 #3d6fd6">A</div>'
            '<div class="ab px" style="left:210px;top:10px;font-size:80px">Armando</div>'
            '<div class="ab pl gr" style="left:212px;top:100px;font-size:34px">homelab · IA · código</div>'
            f'<div class="ab" style="left:600px;top:130px">{vu(btn("Seguir", A, 109.4, "min-width:236px"), A, 108.5, 109.65)}'
            f'{vu(btn("Siguiendo ✓", extra="min-width:236px;color:#14a046"), A, 109.65)}</div>')
COM = (f'<div class="pl" style="font-size:36px;line-height:1.25">🖥️ ¿Qué le pondrías a una 2.ª compu?</div>'
       f'<div style="display:flex;gap:16px;align-items:center;margin-top:20px;padding:14px 18px;background:#fff;box-shadow:inset 3px 3px 0 #828282,inset -3px -3px 0 #fff">'
       f'<span class="px" style="font-size:30px;color:#5a5a5a;white-space:nowrap">Tú ›</span>'
       f'<span class="pl" style="font-size:36px;white-space:nowrap">{teclea("Un servidor de Minecraft 😅", A, 111.0, 1.0)}<span class="car"></span></span></div>')
tarjeta('seguir', S, round(FIN - S, 2),
        ventana(80, 220, 920, 'Perfil — Armando', PERF, A, 108.5, sale=115.37, h=310, icono='compu', desde=(540, 1500))
        + ventana(80, 580, 920, 'Comentarios', COM, A, 109.9, sale=115.37, h=290, icono='info', cu='gris', desde=(540, 450))
        + oculta(cursor([(108.6, 980, 900), (109.2, 810, 410), (109.4, 810, 410, True), (110.6, 900, 760)]), A, 115.37))
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
        rel = os.environ.get('REL', 'videos/10/escritorio')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
