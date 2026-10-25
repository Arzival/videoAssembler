"""El Readme #03 · Bandido multibrazo (muestreo de Thompson) — edición «Escritorio» (LogOS, SO retro inventado).
Las tragamonedas son ventanitas con rodillos que giran a pasos; el número al azar de cada máquina rueda como contador; el hub del autor
es una app de LogOS (videos = jugadas, filtros por serie/horario/duración/gancho) y las «montañas» de cada horario son distribuciones
Beta dibujadas en barras pixeladas que se adelgazan con cada video. Diálogos que se sacuden para lo que sale mal, ⌘S para cerrar.
Capas: mesa (opaca, todo el video) → una pieza transparente por sección → barra de menú arriba con la sección actual.
Tiempos = readme/3/voz/voz-norm.wav (141.38 s).
Uso: SALIDA=~/Documents/Videos/readme/3/escritorio REL=readme/3/escritorio python3 ejemplos/readme-03-escritorio.py [ids…]   (SOLO_HTML=1 para revisar)
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import escritorio as E
from escritorio import ventana, teclea, grande, dialogo, progreso, N, icono, cursor, ap, sprite

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.path.expanduser('~/Documents/Videos/readme/3/escritorio')))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
FIN = 141.38
PIEZAS = []
X, W = 40, 1000
VD, RJ, AZ = '#14a046', '#d8262a', '#0a1f8f'
CM, CT, CN = '#ffd400', '#33ff66', '#b8a2ff'   # mañana · tarde · noche

# sprites extra (solo en memoria; la librería no se toca)
E.SPR['slot'] = ["   kkkkkkkkk    ", "  krrrrrrrrrk   ", "  krkkkkkkkrk y ", "  krkwkwkwkrk k ", "  krkrkykvkrk k ", "  krkwkwkwkrk k ",
                 "  krkkkkkkkrkkk ", "  krrrrrrrrrk   ", "  krrkkkkkrrk   ", "  krrrrrrrrrk   ", "  kkkkkkkkkkk   ", "  ksssssssssk   ",
                 "  kkkkkkkkkkk   ", "                ", "                ", "                "]
E.SPR['video'] = ["                ", " kkkkkkkkkkkkkk ", " krrrrrrrrrrrrk ", " krrrrwrrrrrrrk ", " krrrrwwrrrrrrk ", " krrrrwwwrrrrrk ",
                  " krrrrwwwwrrrrk ", " krrrrwwwrrrrrk ", " krrrrwwrrrrrrk ", " krrrrwrrrrrrrk ", " krrrrrrrrrrrrk ", " kkkkkkkkkkkkkk ",
                  "                ", "                ", "                ", "                "]
E.SPR['moneda'] = ["     kkkkkk     ", "   kkyyyyyykk   ", "  kyyyyooyyyyk  ", " kyyyooooooyyyk ", " kyyoyyooyyyyyk ", " kyyyooooooyyyk ",
                   " kyyyyyooyyoyyk ", " kyyyooooooyyyk ", "  kyyyyooyyyyk  ", "   kkyyyyyykk   ", "     kkkkkk     ", "                ",
                   "                ", "                ", "                ", "                "]
E.SPR['papelera'] = ["   kkkkkkkkkk   ", "  kggggggggggk  ", " kkkkkkkkkkkkkk ", "  kgsgsgsgsgsk  ", "  kgsgsgsgsgsk  ", "  kgsgsgsgsgsk  ",
                     "  kgsgsgsgsgsk  ", "  kgsgsgsgsgsk  ", "  kgsgsgsgsgsk  ", "  kgsgsgsgsgsk  ", "  kgsgsgsgsgsk  ", "  kgsgsgsgsgsk  ",
                     "   kkkkkkkkkk   ", "                ", "                ", "                "]
assert all(len(r) == 16 for s in ('slot', 'video', 'moneda') for r in E.SPR[s])

IC = {'readme': (155, 1755), 'hub': (385, 1755), 'slot': (615, 1755), 'pap': (845, 1755)}

CSS = """
.rl{display:inline-block;width:76px;height:96px;overflow:hidden;background:#fff;box-shadow:inset 3px 3px 0 #828282,inset -3px -3px 0 #dfdfdf;margin:0 4px;vertical-align:top}
.rl div{animation:gira .6s steps(7) var(--g) forwards}
.rl i{display:block;font-style:normal;font-family:VT323;font-size:84px;line-height:96px;text-align:center}
@keyframes gira{to{transform:translateY(-672px)}}
.bd{display:inline-block;padding:4px 14px;font-family:'Jersey 15';font-weight:700;font-size:40px;color:#fff;background:#14a046;box-shadow:4px 4px 0 #0a0a0a}
"""

# montañas: distribuciones Beta en barras pixeladas (gancho window.__xs de escritorio.py)
MONT_JS = """<script>(window.__xs=window.__xs||[]).push(t=>{
const lg=z=>{const c=[0.99999999999980993,676.5203681218851,-1259.1392167224028,771.32342877765313,-176.61502916214059,12.507343278686905,-0.13857109526572012,9.9843695780195716e-6,1.5056327351493116e-7];
 if(z<.5)return Math.log(Math.PI/Math.sin(Math.PI*z))-lg(1-z);z-=1;let x=c[0];for(let i=1;i<9;i++)x+=c[i]/(z+i);const q=z+7.5;return .5*Math.log(2*Math.PI)+(z+.5)*Math.log(q)-q+Math.log(x)};
const pdf=(x,a,b)=>Math.exp((a-1)*Math.log(x)+(b-1)*Math.log(1-x)+lg(a+b)-lg(a)-lg(b));
for(const cv of document.querySelectorAll('canvas[data-m]')){const m=JSON.parse(cv.dataset.m),w=cv.width,h=cv.height,c=cv.getContext('2d'),B=h-46;
 c.fillStyle='#0a0a0a';c.fillRect(0,0,w,h);c.strokeStyle='#0d4d1d';c.lineWidth=2;
 for(let x=0;x<=w;x+=w/10){c.beginPath();c.moveTo(x,0);c.lineTo(x,B);c.stroke()}for(let y=B;y>0;y-=60){c.beginPath();c.moveTo(0,y);c.lineTo(w,y);c.stroke()}
 c.fillStyle='#33ff66';c.font='34px VT323';c.textBaseline='bottom';c.fillText('0 %',6,h-4);c.textAlign='right';c.fillText('100 %',w-6,h-4);c.textAlign='center';c.fillText('probabilidad de ganar →',w/2,h-4);
 for(const k of m.c){if(t<k.on||(k.off&&t>=k.off))continue;const a=_v(k.a,t),b=_v(k.b,t),al=k.al?_v(k.al,t):1,bw=12;
  for(let x=0;x<w;x+=bw){const p=Math.min(.995,Math.max(.005,(x+bw/2)/w));const v=Math.min(1,pdf(p,a,b)/m.ymax),y=Math.round(v*(B-10)/6)*6;
   c.globalAlpha=al*.28;c.fillStyle=k.col;c.fillRect(x,B-y,bw-2,y);c.globalAlpha=al;c.fillRect(x,B-y-6,bw-2,6)}c.globalAlpha=1}
 for(const s of (m.s||[])){if(t<s[0]||(s[1]&&t>=s[1]))continue;const k=m.c[s[2]],x=Math.round(s[3]*w);c.fillStyle=k.col;
  for(let y=0;y<B;y+=18)c.fillRect(x-2,y,4,10);c.fillRect(x-14,6,28,28);c.font='44px VT323';c.textAlign=x>w-90?'right':x<90?'left':'center';c.textBaseline='top';
  c.fillText(Math.round(s[3]*100),x+(x>w-90?-20:x<90?20:0),40)}}});</script>"""


def montana(w, h, curvas, ymax=6, muestras=()):
    """curvas = [{a: keys, b: keys, col, on, off?, al?: keys}] · muestras = [(t_on, t_off|None, i_curva, x 0–1)]."""
    return f"<canvas width=\"{w}\" height=\"{h}\" data-m='{json.dumps({'c': curvas, 'ymax': ymax, 's': [list(s) for s in muestras]})}' style=\"display:block\"></canvas>"


def mini(spr, label, color='#0a0a0a', size=64, w=150):
    return (f'<div style="display:inline-block;width:{w}px;text-align:center;vertical-align:top;font-size:24px;font-weight:600;color:{color}">'
            f'{sprite(spr, size, "margin:0 auto 6px")}<span>{label}</span></div>')


def apila(items, A, h, extra=''):
    """Contenidos que se reemplazan en el mismo lugar: [(html, entra, sale|None)]."""
    return (f'<div style="position:relative;height:{h}px;{extra}">'
            + ''.join(ap(html, A, a, sale=b, extra='position:absolute;left:0;top:0;right:0') for html, a, b in items) + '</div>')


def titulo(lineas_items, A, t, sale, h=250, size=100, nombre='notas.txt', y=110, desde=None):
    cu = apila([(grande(ln, A, a, size=size), a, b) for ln, a, b in lineas_items], A, h)
    return ventana(X, y, W, f'Bloc de notas — {nombre}', cu, A, t, sale=sale, desde=desde or IC['readme'])


def term(x, y, w, lineas, A, t, sale, titulo_='Terminal', size=44, desde=None, h=None):
    cu = ''.join(f'<div>{teclea(tx, A, a, dt)}</div>' for tx, a, dt in lineas) + f'<span class="car"></span>'
    return ventana(x, y, w, titulo_, f'<div style="font-size:{size}px">{cu}</div>', A, t, sale=sale, cu='negro', icono='compu', desde=desde, h=h)


def sac(html, A, t, z=45):
    return f'<div style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:{z};pointer-events:none;animation:sac .4s steps(6) {A(t)} both">{html}</div>'


def ps(txt, size=38, extra=''):
    return f'<div class="ps" style="font-size:{size}px;line-height:1.25;font-weight:600;{extra}">{txt}</div>'


def vt(txt, size=44, color='#0a0a0a', extra=''):
    return f'<div class="vt" style="font-size:{size}px;color:{color};{extra}">{txt}</div>'


SIMB = {'7': RJ, '$': VD, '3': AZ, 'A': '#f08c1c', 'K': '#6b5bd6', '?': '#828282'}


def rodillos(finales, A, t_gira=None, seed=0):
    """Tres rodillos: muestran «?» y, si t_gira, giran a pasos hasta los símbolos finales."""
    pool = '7$3AK7$3AK'
    out = ''
    for i, f in enumerate(finales):
        col = ['?'] + [pool[(seed + i * 3 + j) % len(pool)] for j in range(6)] + [f]
        anim = f'--g:{A(t_gira + i * .12)}' if t_gira is not None else 'animation:none'
        out += (f'<span class="rl"><div style="{anim}">' + ''.join(f'<i style="color:{SIMB[s]}">{s}</i>' for s in col) + '</div></span>')
    return f'<div style="white-space:nowrap">{out}</div>'


def rueda(t0, seq, dt=.13):
    """Keys de N para un número que rueda al azar y se queda en el último valor."""
    return [(t0 + i * dt, v, dt * .8) for i, v in enumerate(seq)]


def seccion(pid, start, end, body, css=''):
    end = end + E.COLA if end < FIN else end
    PIEZAS.append((pid, start, end, E.page(CSS + css, body, round(end - start, 2), S0=start, transparente=True)))


# ───────────────────────── mesa: escritorio LogOS (todo el video, opaca)
A = E.at(0)
MESA = (f'<div style="position:absolute;left:0;right:0;top:760px;text-align:center;font-weight:700;font-size:150px;color:rgba(255,255,255,.07);letter-spacing:.05em">LogOS</div>'
        f'<div class="vt" style="position:absolute;left:0;right:0;top:930px;text-align:center;font-size:46px;color:rgba(255,255,255,.12)">README.md · #03 · Bandido multibrazo</div>'
        + icono(60, 1700, 'archivo', 'README.md', A, 0) + icono(290, 1700, 'servidor', 'hub', A, 0) + icono(520, 1700, 'slot', 'casino/', A, 0)
        + icono(750, 1700, 'papelera', 'Papelera', A, 0))
MESA_CSS = '.mesa{background-image:radial-gradient(rgba(0,0,0,.18) 1.2px,transparent 1.4px),linear-gradient(rgba(255,255,255,.035) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.035) 2px,transparent 2px);background-size:6px 6px,96px 96px,96px 96px}'
PIEZAS.append(('mesa', 0.0, FIN, E.page(MESA_CSS, MESA, FIN, S0=0.0, mesa='morado', menu=False)))

# ───────────────────────── 0:00 · gancho: «cientos de pruebas» → yo con 9 videos → horarios, títulos, prompts
S = 0.0; A = E.at(S); NX = 12.1
VIDS = ''.join(ap(mini('video', f'video_0{i + 1}', size=60, w=180), A, 5.2 + i * .12, extra='display:inline-block') for i in range(9))
b = (titulo([(['¿Cientos de', '*pruebas*?'], .1, 4.3), (['Yo llevo', '_9 videos_'], 4.35, 7.55), (['Esto te va', 'a *servir*'], 7.6, None)], A, .05, NX,
            h=230, size=100, nombre='gancho.txt')
     + sac(dialogo(X, 470, W, 'alerta', 'Para saber qué funciona necesitas <b>cientos de pruebas</b>.', A, 1.3, sale=4.3, titulo='Advertencia'), A, 1.3)
     + ventana(X, 470, W, f'videos/ — {9} archivos', f'<div>{VIDS}</div>'
               + vt(f'jugadas hasta hoy: {N([(0, 0), (6.6, 9, .5)])}', 46, AZ, 'margin-top:10px'), A, 4.9, sale=7.55, icono='carpeta', desde=IC['hub'])
     + ventana(X, 470, W, '¿Qué estás probando?', mini('reloj', 'horarios', size=110, w=300) + mini('archivo', 'títulos', size=110, w=300)
               + mini('robot', 'prompts', size=110, w=300), A, 8.6, sale=NX, cu='gris', icono='info', desde=IC['readme'])
     + cursor([(8.6, 900, 1500), (9.1, 190, 640, True), (9.7, 490, 640, True), (10.55, 790, 640, True), (11.6, 900, 1450)], fin=NX))
seccion('s0-gancho', S, NX, b)

# ───────────────────────── 0:12 · bandido multibrazo: tragamonedas · ¿solo la primera? · ¿todas por igual?
S = 12.1; A = E.at(S); NX = 30.62; F1 = 16.94
f1 = (ventana(X, 110, W, 'Diccionario — bandido multibrazo', grande(['Bandido', '_multibrazo_'], A, 12.2, size=130)
              + f'<div class="ps" style="font-size:40px;font-weight:700;margin-top:12px">{teclea("(en inglés: <i>multi-armed bandit</i>)", A, 13.5, .6)}</div>',
              A, 12.15, sale=F1, icono='info', desde=IC['readme'])
      + sac(dialogo(X, 700, W, 'slot', 'Viene de las <b>tragamonedas</b>: el «bandido de un brazo» es la máquina con palanca.', A, 14.4, sale=F1, titulo='LogOS'), A, 14.4)
      + ventana(X, 1060, W, 'casino/', mini('slot', 'brazo 1', size=120, w=300) + mini('slot', 'brazo 2', size=120, w=300) + mini('slot', 'brazo 3', size=120, w=300),
                A, 15.6, sale=F1, icono='slot', cu='gris', desde=IC['slot']))
MX = {'A': 40, 'B': 385, 'C': 730}


def maq(L, cuerpo, t, sale, z=20):
    return ventana(MX[L], 470, 310, f'Máquina {L}', cuerpo, A, t, sale=sale, icono='slot', cu='gris', desde=IC['slot'], z=z)


EST = lambda items, h=110: apila([(vt(tx, 44, col, 'text-align:center;margin-top:14px'), a, b_) for tx, col, a, b_ in items], A, h)
f2 = (titulo([(['¿Cuál da', '*más*?'], 17.0, 20.85), (['¿Solo la', 'primera?'], 20.9, 26.0), (['¿Todas', 'por igual?'], 26.05, None)], A, 16.98, NX,
             h=230, size=100, nombre='casino.txt', desde=(540, 200))
      + maq('A', rodillos('77$', A, 21.75, 0) + EST([('¿?', '#828282', 17.6, 21.7), ('+$5', VD, 22.5, 26.8), ('-$10', RJ, 26.95, None)]), 17.4, NX)
      + maq('B', rodillos('3K7', A, 27.3, 4) + EST([('¿?', '#828282', 17.7, 27.2), ('-$10', RJ, 28.0, None)]), 17.55, NX)
      + maq('C', rodillos('$$$', A, 27.75, 7) + EST([('¿?', '#828282', 17.8, 24.5), ('pagaba ×3', VD, 24.55, 27.7), ('-$10', RJ, 28.45, None)]), 17.7, NX)
      + sac(dialogo(X, 1000, W, 'alerta', 'Por quedarte con la primera, te perdiste de una que daba <b>aún más</b>.', A, 25.0, sale=26.0, titulo='Advertencia'), A, 25.0)
      + ventana(X, 1000, W, 'Monedero', f'<div style="display:flex;gap:24px;align-items:center">{sprite("moneda", 110)}'
                f'<div class="vt" style="font-size:120px;color:{RJ}">{N([(0, 100), (28.95, 40, 1.4)], pre="$")}</div></div>', A, 28.4, sale=NX, icono='moneda', cu='gris',
                desde=(540, 1100))
      + sac(dialogo(110, 1330, 860, 'error', 'Así solo estás <b>tirando tu dinero</b>.', A, 29.9, sale=NX, titulo='Error'), A, 29.9)
      + cursor([(17.5, 900, 1560), (21.3, 260, 900), (21.6, 260, 900, True), (26.5, 260, 900, True), (27.1, 600, 900, True), (27.6, 950, 900, True), (29.0, 900, 1560)], fin=NX))
seccion('s1-bandido', S, NX, f1 + f2)

# ───────────────────────── 0:30 · muestreo de Thompson: número al azar por máquina · más ganado → número más alto · juega el más alto
#                               · la que casi no conoces: su número salta mucho → a veces le toca
S = 30.62; A = E.at(S); NX = 55.45
REC = {'A': '8 de 10', 'B': '3 de 10', 'C': '1 de 2'}
NUM = {'A': [(0, 0)] + rueda(36.3, [55, 31, 72, 66]) + rueda(40.4, [74, 88, 81]) + rueda(49.5, [78, 83, 80, 79], .3) + rueda(52.3, [77, 79]),
       'B': [(0, 0)] + rueda(36.35, [20, 61, 44, 38]) + rueda(40.45, [41, 25, 33]) + rueda(49.5, [31, 36, 29, 32], .3) + rueda(52.3, [28, 30]),
       'C': [(0, 0)] + rueda(36.4, [90, 12, 57, 51]) + rueda(40.5, [22, 69, 47]) + rueda(49.5, [12, 91, 30, 77, 8, 64], .25) + rueda(52.3, [40, 93])}
BADGE = {'A': [(44.2, 52.3)], 'C': [(53.0, None)]}


def maq2(L):
    cu = (apila([(vt(f'ganó {REC[L]}', 42, AZ, 'text-align:center'), 38.4 + .15 * 'ABC'.index(L), None)], A, 50)
          + f'<div class="vt" style="font-size:150px;line-height:1;text-align:center;margin-top:8px">{N(NUM[L])}</div>'
          + apila([(f'<div style="text-align:center"><span class="bd">JUEGA ✓</span></div>', a, b_) for a, b_ in BADGE.get(L, [])]
                  + ([(vt('¿la conoces?', 40, RJ, 'text-align:center'), 47.9, 52.95)] if L == 'C' else []), A, 64, extra='margin-top:10px'))
    return ventana(MX[L], 470, 310, f'Máquina {L}', cu, A, 30.9 + .12 * 'ABC'.index(L), sale=NX, icono='slot', cu='gris', desde=IC['slot'])


b = (titulo([(['Muestreo de', '_Thompson_'], 30.66, 33.65), (['Un número', 'al *azar*'], 33.72, 37.8), (['Más ganado →', '*número más alto*'], 37.88, 42.25),
             (['Juegas el', '_más alto_'], 42.3, 46.15), (['¿Y la que', '*casi no conoces*?'], 46.2, 51.15), (['A veces', '_le toca_'], 51.2, None)], A, 30.64, NX,
            h=230, size=100, nombre='thompson.txt')
     + maq2('A') + maq2('B') + maq2('C')
     + dialogo(X, 960, W, 'info', 'Lo resuelve de una manera <b>muy simple</b>.', A, 32.4, sale=33.7, titulo='Muestreo de Thompson', desde=(540, 1060))
     + term(X, 960, W, [('$ número = azar(lo que sabes de la máquina)', 34.0, .9), ('$ juega(la del número más alto)', 43.0, .7)], A, 33.75, sale=49.4)
     + sac(dialogo(X, 960, W, 'alerta', 'La que casi no conoces: su número <b>salta mucho</b>.', A, 49.46, sale=53.9, titulo='Ojo'), A, 49.46)
     + dialogo(X, 960, W, 'info', '¡Le tocó a la <b>C</b>! Así también <b>la vas conociendo</b>.', A, 53.95, sale=NX, titulo='LogOS', desde=(885, 900))
     + cursor([(43.5, 900, 1560), (44.9, 200, 760, True), (46.4, 900, 1500), (53.5, 890, 760, True), (54.8, 900, 1560)], fin=NX))
seccion('s2-thompson', S, NX, b)

# ───────────────────────── 0:55 · mi hub: cada video = una jugada · gana si a 48 h llega a la mediana · por serie, horario, duración y gancho
S = 55.45; A = E.at(S); NX = 70.6; F1 = 64.2
FILAS = [('video_09', True), ('video_08', False), ('video_07', True), ('video_06', True), ('video_05', False)]
ROWS = ''.join(ap(f'<div style="display:flex;align-items:center;gap:18px;padding:6px 10px">{sprite("video", 50)}<span class="vt" style="font-size:46px;width:220px">{n}</span>'
                  + ap(f'<div style="display:flex;align-items:center;gap:10px">{sprite("slot", 46)}<span class="ps" style="font-size:30px;font-weight:700">jugada</span></div>', A, 58.0 + i * .1)
                  + f'<span style="margin-left:auto">'
                  + ap(vt('✓ ganó' if g else '✕ no', 50, VD if g else RJ), A, 63.0 + i * .12) + '</span></div>', A, 56.2 + i * .08)
               for i, (n, g) in enumerate(FILAS))
f1 = (titulo([(['Mi *hub*', 'y mis videos'], 55.5, 57.55), (['Cada video =', '_una jugada_'], 57.6, 59.45), (['¿Ganó? 48 h', 'vs _mediana_'], 59.5, None)], A, 55.48, F1,
             h=230, size=100, nombre='hub.txt')
      + ventana(X, 470, W, 'Hub — mis videos', f'<div style="background:#fff;padding:6px;box-shadow:inset 3px 3px 0 #828282">{ROWS}</div>', A, 55.9, sale=F1, icono='servidor',
                cu='gris', desde=IC['hub'])
      + term(X, 1080, W, [('$ gana = vistas(48 h) ≥ mediana', 59.6, .8), ('  mediana = mi video típico', 62.6, .5)], A, 59.5, sale=F1))
BTN = lambda txt, t, extra='': ap(f'<span class="btn" style="font-size:44px;min-width:440px;{extra}">{txt}</span>', A, t, extra='display:inline-block;margin:10px')
f2 = (titulo([(['Lo reviso', 'por…'], 64.25, 68.1), (['Sobre todo:', '_el gancho_'], 68.15, None)], A, 64.22, NX, h=230, size=100, nombre='hub.txt', desde=(540, 200))
      + ventana(X, 470, W, 'Hub — filtros', f'<div style="text-align:center">{BTN("serie", 65.77)}{BTN("horario", 66.4)}{BTN("duración", 67.28)}'
                f'{BTN("<span class=sl style=--s:" + A(69.95) + ">gancho</span>", 69.6, "outline:4px solid #0a0a0a;outline-offset:3px")}</div>', A, 64.6, sale=NX,
                icono='servidor', cu='gris', desde=IC['hub'])
      + cursor([(68.3, 900, 1560), (69.9, 790, 790, True)], fin=NX))
seccion('s3-hub', S, NX, f1 + f2)

# ───────────────────────── 1:10 · la montaña: ancha = no sé nada · cada video la adelgaza · más videos, más seguro
S = 70.6; A = E.at(S); NX = 87.1
KA = [(0, 1.6), (78.4, 3, .7), (79.5, 5, .7), (80.6, 9, .7), (81.7, 15, .8), (83.0, 26, 1.4)]
KB = [(0, 1.4), (78.4, 2, .7), (79.5, 3, .7), (80.6, 5, .7), (81.7, 9, .8), (83.0, 15, 1.4)]
KV = [(0, 1), (78.4, 3, .7), (79.5, 6, .7), (80.6, 12, .7), (81.7, 22, .8), (83.0, 39, 1.4)]
PANEL = (montana(920, 560, [{'a': [list(k) for k in KA], 'b': [list(k) for k in KB], 'col': CT, 'on': 71.4}])
         + f'<div style="display:flex;align-items:center;gap:16px;margin-top:14px"><i style="width:34px;height:34px;background:{CT};box-shadow:3px 3px 0 #0a0a0a"></i>'
         f'<span class="vt" style="font-size:46px">horario: tarde · videos: {N([list(k) for k in KV])}</span></div>'
         + apila([(vt('ancha = casi no sé nada ✕', 46, RJ), 74.9, 81.6), (vt('delgada = ya sé ✓', 46, VD), 81.65, None)], A, 56, extra='margin-top:6px'))
b = (titulo([(['Cada horario,', 'su *montaña*'], 70.68, 73.5), (['Ancha =', '_no sé nada_'], 73.58, 77.85), (['Cada video la', '*adelgaza*'], 77.9, 82.2),
             (['Más videos,', '_más seguro_'], 82.25, None)], A, 70.65, NX, h=230, size=100, nombre='panel.txt')
     + ventana(X, 470, W, 'Hub — panel', PANEL, A, 70.9, sale=NX, icono='servidor', desde=IC['hub'])
     + dialogo(X, 1400, W, 'info', 'Más seguro de que <b>ese horario sí va a funcionar</b> ✓', A, 85.3, sale=NX, titulo='Hub', desde=(540, 1500)))
seccion('s4-montana', S, NX, b)

# ───────────────────────── 1:27 · ejemplo: la tarde ganó 3 de 3 → el panel recomienda tarde · la noche casi sin probar → a veces le toca
S = 87.1; A = E.at(S); NX = 102.15
CUR = [{'a': [[0, 2]], 'b': [[0, 2]], 'col': CM, 'on': 87.4, 'al': [[0, .35]]},
       {'a': [[0, 4]], 'b': [[0, 1]], 'col': CT, 'on': 87.4, 'al': [[0, .35], [88.4, 1, .3], [94.45, .45, .3]]},
       {'a': [[0, 1.3]], 'b': [[0, 1.6]], 'col': CN, 'on': 87.4, 'al': [[0, .35], [94.45, 1, .3]]}]
MU = [(92.3, 94.4, 0, .42), (92.4, 94.4, 1, .86), (92.5, 94.4, 2, .25), (98.3, None, 0, .37), (98.4, None, 1, .74), (98.5, None, 2, .89)]
LEY = ''.join(f'<div style="display:flex;align-items:center;gap:16px;margin-top:8px"><i style="width:34px;height:34px;background:{col};box-shadow:3px 3px 0 #0a0a0a"></i>'
              f'<span class="vt" style="font-size:44px">{n}</span>' + (ap(vt(extra, 44, c2), A, te, extra='margin-left:12px') if extra else '') + '</div>'
              for col, n, extra, c2, te in [(CM, 'mañana', '', '', 0), (CT, 'tarde', '· ganó 3 de 3 ✓', VD, 89.5), (CN, 'noche', '· casi sin probar', RJ, 95.6)])
CAL = ''.join(ap(f'<span class="{"sl " if d == "N" else ""}vt" style="display:inline-block;width:132px;text-align:center;font-size:64px;margin:4px;background:#fff;'
                 f'box-shadow:inset 3px 3px 0 #828282;{"--s:" + A(101.5) if d == "N" else ""}">{d}</span>', A, 99.9 + i * .1, extra='display:inline-block')
              for i, d in enumerate('TTNTMT'))
b = (titulo([(['Ejemplo:', 'la *tarde*'], 87.15, 91.35), (['Recomienda:', '_la tarde_'], 91.4, 94.4), (['Ojo con', 'la *noche*'], 94.46, 97.4),
             (['A veces', 'toca _noche_'], 97.48, None)], A, 87.12, NX, h=230, size=100, nombre='panel.txt')
     + ventana(X, 470, W, 'Hub — panel · horarios', montana(920, 470, CUR, muestras=MU) + LEY, A, 87.3, sale=NX, icono='servidor', desde=IC['hub'])
     + dialogo(X, 1290, W, 'info', 'Próximo video: <b>en la tarde</b>.', A, 92.9, sale=94.4, titulo='Hub recomienda', desde=(540, 1390))
     + sac(dialogo(X, 1290, W, 'alerta', 'Esta vez la <b>noche</b> sacó el número más alto.', A, 98.7, sale=99.75, titulo='Hub recomienda'), A, 98.7)
     + ventana(X, 1290, W, 'Próximas publicaciones', f'<div>{CAL}</div>' + vt('T = tarde · M = mañana · N = noche', 36, '#0a0a0a', 'margin-top:10px'),
               A, 99.8, sale=NX, icono='reloj', cu='gris', desde=(540, 1390)))
seccion('s5-ejemplo', S, NX, b)

# ───────────────────────── 1:42 · > ⚠ Ojo: no adivina el futuro · decide qué probar · si pega por el tema, la hora se lleva el crédito → revisar seguido
S = 102.15; A = E.at(S); NX = 116.6; F2 = 109.0
CAB = ventana(X, 110, W, 'Bloc de notas — ojo.txt', f'<div style="display:flex;align-items:center;gap:26px">{sprite("alerta", 110)}'
              f'{grande(["&gt; Ojo"], A, 102.25, size=110)}<span class="ps" style="font-size:40px;font-weight:700;color:{RJ};margin-left:auto">{teclea("no es magia", A, 102.8, .4)}</span></div>',
              A, 102.2, sale=NX, desde=IC['readme'])
f1 = (sac(dialogo(X, 470, W, 'error', 'Función no disponible: <b>adivinar el futuro</b>.', A, 104.96, sale=F2, titulo='Error'), A, 104.96)
      + term(X, 820, W, [('$ hub decide', 106.0, .4), ('› con lo poco que sé:', 106.8, .5), ('  probar tarde · a veces noche', 107.5, .7)], A, 105.9, sale=F2))
f2 = (ventana(X, 470, 480, 'video_07', f'<div style="display:flex;gap:16px;align-items:center">{sprite("video", 80)}<div>'
              f'<div class="ps" style="font-size:30px;font-weight:700">tema: <span style="color:{RJ}">viral</span></div>'
              f'<div class="vt" style="font-size:70px;color:{VD}">{N([(0, 1200), (109.8, 48000, 1.2)], f="c")}</div></div></div>' + vt('vistas', 34), A, 109.1, sale=NX,
              icono='video', cu='gris', desde=(280, 570))
      + ventana(560, 470, 480, 'Hub — crédito', vt('¿quién ganó?', 40) + apila([(vt('la hora: tarde', 60, RJ, 'margin-top:12px'), 111.1, None)], A, 80)
                + apila([(f'<span class="bd" style="background:{RJ}">+1 a la hora ✕</span>', 112.5, None)], A, 60), A, 110.9, sale=NX, icono='servidor', cu='gris',
                desde=(800, 570))
      + sac(dialogo(X, 860, W, 'alerta', 'Pegó por el <b>tema</b>, pero el crédito se lo lleva <b>la hora</b>.', A, 112.0, sale=NX, titulo='Advertencia'), A, 112.0)
      + ventana(X, 1200, W, 'Tareas programadas', f'<div style="display:flex;gap:20px;align-items:center">{sprite("reloj", 90)}'
                f'<span class="vt" style="font-size:54px">{teclea("revisar el panel · muy seguido ✓", A, 114.3, .8)}</span></div>', A, 113.6, sale=NX, icono='reloj', cu='gris',
                desde=(540, 1300)))
seccion('s6-ojo', S, NX, CAB + f1 + f2)

# ───────────────────────── 1:56 · «9 videos son muy poquitos» → sí, pero justo por eso me sirve → pruébalo en tu trabajo
S = 116.6; A = E.at(S); NX = 132.8; F1, F2 = 121.7, 128.15
f1 = (titulo([(['«9 videos son', '*muy poquitos*»'], 116.66, None)], A, 116.63, F1, h=230, size=100, nombre='dudas.txt')
      + ventana(X, 470, W, 'Comentarios', f'<div style="display:flex;gap:20px;align-items:flex-start">{sprite("compu", 80)}<div class="ps" style="font-size:42px;font-weight:600">'
                f'<b>@alguien</b><br>{teclea("9 videos son muy poquitos…", A, 117.4, .8)}</div></div>', A, 117.0, sale=F1, icono='info', desde=IC['readme'])
      + dialogo(110, 820, 860, 'info', 'La verdad es que sí: <b>tienes razón</b> ✓', A, 120.6, sale=F1, titulo='LogOS', desde=(540, 920)))
f2 = (titulo([(['Justo por eso', '_me sirve_'], 121.75, None)], A, 121.73, F2, h=230, size=100, nombre='dudas.txt', desde=(540, 200))
      + ventana(X, 470, W, 'Decidir', vt('esperar a tener cientos de videos', 44) + progreso([(0, 0), (123.7, 3, 1.0)], color=RJ)
                + vt(f'videos: 9 de 300 · {N([(0, 0), (123.7, 3, 1.0)], suf=" %")}', 40, RJ, 'margin:8px 0 26px')
                + apila([(f'<div style="display:flex;gap:18px;align-items:center">{sprite("compu", 70)}<span class="vt" style="font-size:54px;color:{VD}">decidir con lo que ya sé ✓</span></div>',
                          124.9, None)], A, 90), A, 122.6, sale=F2, icono='reloj', cu='gris', desde=(540, 570)))
f3 = (titulo([(['¿Pruebas algo', 'en tu *trabajo*?'], 128.2, None)], A, 128.18, NX, h=230, size=100, nombre='tu-turno.txt', desde=(540, 200))
      + ventana(X, 470, W, 'Tus pruebas', ''.join(ap(mini(s_, n, size=100, w=300), A, 129.3 + i * .25, extra='display:inline-block')
                                                 for i, (s_, n) in enumerate([('reloj', 'horarios'), ('archivo', 'títulos'), ('robot', 'prompts')])),
                A, 129.0, sale=NX, icono='carpeta', cu='gris', desde=IC['readme'])
      + dialogo(110, 860, 860, 'info', 'Vale la pena <b>darle un chance</b> ✓', A, 130.7, sale=NX, titulo='LogOS', desde=(540, 960)))
seccion('s7-pocos', S, NX, f1 + f2 + f3)

# ───────────────────────── 2:12 · lo iremos viendo · pregunta + resumen para guardar
S = 132.8; A = E.at(S); NX = 138.8
LISTA = ''.join(f'<div class="vt" style="font-size:54px">{teclea(t_, A, t0, .35)}</div>'
                for t_, t0 in [('1. Cada video = una jugada', 135.4), ('2. Número al azar por opción', 135.7), ('3. Juega el más alto', 136.0), ('&gt; ⚠ No adivina el futuro', 136.4)])
b = (dialogo(X, 110, W, 'info', 'Esto lo iremos viendo <b>poco a poco</b>.', A, 132.88, sale=134.9, titulo='Continuará…', desde=IC['readme'])
     + ventana(X, 110, W, 'Pregunta', f'<div style="display:flex;gap:24px;align-items:flex-start">{sprite("info", 100)}'
               f'{grande(["¿Tú cómo decides", "qué *probar*", "y qué _no_?"], A, 134.95, size=80)}</div>', A, 134.92, sale=NX, cu='gris', desde=IC['readme'])
     + ventana(X, 640, W, 'README.md', LISTA, A, 135.2, sale=NX, icono='archivo', desde=IC['readme'])
     + ap('<div class="ps" style="position:absolute;left:120px;top:1150px;font-size:56px;font-weight:700;color:#fff;text-shadow:4px 4px 0 #000">cuéntame en los comentarios ↓</div>',
          A, 136.6, sale=NX))
seccion('s8-pregunta', S, NX, b)

# ───────────────────────── 2:18 · cierre: «nos vemos cuando toque actualizar el README» (⌘S)
S = 138.8; A = E.at(S)
b = (ventana(X, 110, W, 'README.md', grande(['Nos vemos cuando', 'toque *actualizar*', 'el README'], A, 138.85, size=90), A, 138.83, icono='archivo', desde=IC['readme'])
     + dialogo(110, 560, 860, 'info', '¿Guardar los cambios en <b>README.md</b>?', A, 139.1, botones=('Guardar', 'No'), pulsa=139.65, sale=139.8, titulo='⌘S', desde=(540, 660))
     + ventana(110, 560, 860, 'Guardando…', '<div class="vt" style="font-size:44px;margin-bottom:10px">README.md</div>' + progreso([(0, 0), (139.8, 100, .3)]),
               A, 139.8, sale=140.15, cu='gris')
     + dialogo(110, 560, 860, 'info', '<b>✓ guardado</b>', A, 140.15, titulo='LogOS')
     + cursor([(139.0, 900, 1500), (139.65, 385, 770, True), (140.6, 800, 1300)]))
seccion('s9-cierre', S, FIN, b)

# ───────────────────────── barra de menú (todo el video, transparente, encima)
SECC = [(0.0, '# Probar sin cientos'), (12.1, '## ¿Qué es?'), (30.62, '## Muestreo de Thompson'), (55.45, '## Mi hub'), (70.6, '## La montaña'),
        (87.1, '## Ejemplo: horarios'), (102.15, '&gt; ⚠ Ojo'), (116.6, '## ¿9 videos?'), (132.8, '## Tu turno'), (138.8, '✓ guardado')]
A = E.at(0)
SECS = ''.join(ap(f'<span>{n}</span>', A, t, sale=SECC[i + 1][0] if i + 1 < len(SECC) else None, extra='position:absolute;right:24px;top:0;height:64px;display:flex;align-items:center')
               for i, (t, n) in enumerate(SECC))
BARRA = (f'<div class="barra"><span class="lg">{sprite("compu", 40)}LogOS</span><span style="font-weight:500">README.md · #03</span>'
         f'<span class="vt" style="margin-left:auto;font-size:40px;position:relative;width:560px;height:64px;color:#0a1f8f">{SECS}</span></div>')
PIEZAS.append(('barra', 0.0, FIN, E.page('', BARRA, FIN, S0=0.0, transparente=True)))
PRE = 'rme3-'

# las piezas con montañas llevan su script de dibujo
PIEZAS = [(p, a, b_, h.replace('</body>', MONT_JS + '</body>') if 'data-m=' in h else h) for p, a, b_, h in PIEZAS]

if __name__ == '__main__':
    solo = set(sys.argv[1:])
    for pid, a, b_, html in PIEZAS:
        if solo and pid not in solo:
            continue
        path = f'{WORK}/{pid}.html'
        open(path, 'w').write(html)
        if os.environ.get('SOLO_HTML'):
            print('html', path, f'{b_ - a:.2f}'); continue
        r = subprocess.run(['node', CAP, path, f'{b_ - a:.2f}', f'{OUT}/{PRE}{pid}.webm'], capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr[-600:], flush=True)
    if not solo:
        rel = os.environ.get('REL', 'readme/3/escritorio')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b_, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b_, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
