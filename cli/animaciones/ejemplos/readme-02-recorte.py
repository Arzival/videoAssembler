"""El Readme #02 · RAG — edición «Recorte» (nueva, sin la base Catálogo/pista): cuaderno de ingeniería sobre papel cuadriculado.
El RAG se explica con un diagrama hecho a mano que se va armando (documentos → pedazos → búsqueda → pregunta+pedazos → respuesta),
con tickets de terminal, recortes, notas, sellos y marcatextos; acento azul. Arriba, en lugar de la pestaña, una etiqueta de cinta
con «README.md · #02 RAG» y la sección actual. Todo se mueve a 12 cps y cada hoja entra rasgada sobre la anterior.
Tiempos = readme/2/voz/voz-norm.wav (132.34 s), los mismos de readme-02.py.
Uso: SALIDA=~/Documents/Videos/readme/2/recorte REL=readme/2/recorte python3 ejemplos/readme-02-recorte.py [ids…]   (SOLO_HTML=1 para revisar)
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import recorte as K
from recorte import titular, tacha, subraya, circulo, flecha, recorte, nota, sello, ticket, numero, N, logo, mano, fase, palomita, marca

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.path.expanduser('~/Documents/Videos/readme/2/recorte')))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
FIN = 132.34
TOP = 300          # primer renglón útil (debajo de la etiqueta)
PIEZAS = []
AZ, RJ, VD = 'var(--azul)', 'var(--rojo)', 'var(--verde)'


def escena(pid, start, end, body, css='', sigue=True, seed=1):
    if sigue:
        end += K.COLA
    PIEZAS.append((pid, start, end, K.page(CSS + css, body, round(end - start, 2), S0=start, fondo='cuad', seed=seed, ac=AZ)))


CSS = '.tt .sf{color:var(--azul)}'


def fz(html, A, entra=None, sale=None):
    """fase() con entrada y salida a la vez: en recorte.py .fz.in pisa la animación de .fz.x, así que se anidan."""
    if entra is not None and sale is not None:
        return fase(fase(html, A, sale=sale), A, entra=entra)
    return fase(html, A, entra=entra, sale=sale)


def caja(txt, size=96, extra=''):
    return f'<div style="font-weight:900;font-stretch:62%;font-size:{size}px;line-height:.88;text-transform:uppercase;{extra}">{txt}</div>'


def ser(txt, size=48, extra=''):
    return f'<div class="ser" style="font-size:{size}px;line-height:1.05;{extra}">{txt}</div>'


def renglones(n, ancho=(92, 70, 84, 60, 88, 76), color='#d5cfc1', alto=14, gap=18):
    """Líneas grises de «texto» para hojas y pedazos."""
    return ''.join(f'<div style="height:{alto}px;width:{ancho[i % len(ancho)]}%;background:{color};border-radius:4px;margin-top:{gap}px"></div>' for i in range(n))


def pedazo(x, y, w, h, num, A, t, rot=0.0, seed=40, cls='', sale=None, color='#2457e6'):
    """Recorte pequeño = un «pedazo» de documento, con su número."""
    body = (f'<div class="mono" style="font-size:24px;font-weight:700;color:{color}">pedazo {num}</div>' + renglones(3, alto=11, gap=14))
    return recorte(x, y, w, h, body, A, t, sale=sale, rot=rot, seed=seed, cls=cls, cinta=False, pad='20px 24px')


def hoja_doc(x, y, w, h, titulo, A, t, rot=0.0, seed=50, n=9, sale=None, cls=''):
    body = f'<div class="mono" style="font-size:26px;font-weight:700">{titulo}</div>' + renglones(n)
    return recorte(x, y, w, h, body, A, t, sale=sale, rot=rot, seed=seed, cls=cls, pad='28px 30px')


# ───────────────────────── 0:00 · gancho: tu IA contesta sin conocer tus datos → se lo inventa → 3 pasos
S = 0.0; A = K.at(S)
escena('s0-gancho', S, 4.6,
       titular(['Tu IA contesta', '_sin tus datos_'], A, .15, top=TOP, size=150, seed=1)
       + ticket(80, 650, 920, [('<i>›</i> ¿qué dice <b>mi contrato</b>?', .3, .5), ('<i>🤖</i> probablemente… <i>(no lo leyó)</i>', 1.15, .6),
                               ('<i>arreglo:</i> <b>3 pasos</b>', 2.55, .4)], A, rot=-1.2, size=36)
       + nota(90, 1000, '¿tus docs?', A, 1.2, rot=-5, w=300, size=58)
       + nota(420, 1040, '¿tus notas?', A, 1.5, rot=4, w=300, size=58, color='#cfe0ff')
       + sello(440, 1290, 'Inventado', A, 1.9, size=88, rot=-8)
       + mano(110, 1500, '→ arreglo en 3 pasos', A, 2.6, size=70, color=AZ), seed=1)

# ───────────────────────── 0:04 · RAG: que conteste con tus datos | en vez de todo, busca solo lo que sirve
S = 4.6; A = K.at(S)
f1 = (numero(70, TOP, 'RAG', A, 4.8, size=400, color=AZ)
      + recorte(80, 680, 920, 170, ser('<b style="font-family:Archivo;font-style:normal;font-weight:900;font-stretch:62%">R</b>etrieval-'
                                       '<b style="font-family:Archivo;font-style:normal;font-weight:900;font-stretch:62%">A</b>ugmented '
                                       '<b style="font-family:Archivo;font-style:normal;font-weight:900;font-stretch:62%">G</b>eneration', 62), A, 5.0, rot=-1.5, seed=60, pad='40px 44px')
      + ticket(80, 920, 700, [('<i>RAG =</i> <b>buscar</b> <i>→</i> <b>contestar</b>', 5.9, .6)], A, rot=1.2, size=38)
      + titular(['Contesta con', '_tus datos_'], A, 8.86, top=1130, size=150, seed=2)
      + sello(430, 1450, 'No se lo imagina', A, 10.5, size=60, rot=-7))
DOCS = ''.join(hoja_doc(90 + i * 34, 640 + i * 30, 280, 360, f'doc_{i + 1}.md', A, 11.3 + i * .08, rot=(-8 + i * 3.5), seed=61 + i, n=8) for i in range(5))
TROZOS = ''.join(pedazo(660, 560 + i * 230, 340, 200, ['014', '017', '031'][i], A, 19.95 + i * .14, rot=[-3, 2, -1.5][i], seed=70 + i) for i in range(3))
f2 = (titular(['En vez de', 'pasarle *todo*…'], A, 11.1, x=14.15, top=TOP, size=150, seed=3)
      + titular(['_Busca_', 'primero'], A, 14.3, x=19.8, top=TOP, size=150, seed=4)
      + titular(['Solo lo que', '*sirve*'], A, 19.9, top=TOP, size=160, seed=5)
      + DOCS
      + mano(110, 1110, 'todos tus documentos', A, 11.6, size=56)
      + sello(110, 1210, '✕ todos los docs', A, 12.9, size=56, rot=-6)
      + logo('', 470, 760, 170, A, 14.4, rot=-10, bg='#2457e6', emoji='🔍')
      + flecha(400, 820, 470, 830, A, 14.5, color=AZ, curva=.4)
      + ticket(80, 1360, 920, [('<i>$</i> rag search <b>"tu pregunta"</b>', 14.3, .6), ('<i>contexto:</i> <b>3 pedazos</b> <i>· nada más</i>', 19.9, .6)], A, rot=-1, size=36)
      + flecha(600, 860, 650, 640, A, 19.95, color=AZ, curva=-.3)
      + TROZOS
      + circulo(830, 900, 420, 760, A, 20.4, color=AZ, seed=12))
escena('s1-rag', S, 21.85, fase(f1, A, sale=10.9) + fase(f2, A, entra=11.0), seed=2)

# ───────────────────────── 0:21 · 3 pasos: prepara (pedazos con significado, por idea) → busca (los que más se parecen) → contesta solo con eso
S = 21.85; A = K.at(S)
P4 = [(450, 640, '014'), (740, 640, '015'), (450, 880, '016'), (740, 880, '017')]
f1 = (titular(['Paso 1', '*prepara*'], A, 21.95, top=TOP, size=160, seed=6)
      + hoja_doc(80, 640, 320, 440, 'docs/', A, 22.2, rot=-3, seed=80, n=10)
      + ''.join(pedazo(x, y, 270, 200, n, A, 26.47 + i * .12, rot=[-3, 2, 3, -2][i], seed=81 + i) for i, (x, y, n) in enumerate(P4))
      + mano(690, 575, '✂ pedazos pequeños', A, 26.5, size=46, color=AZ)
      + circulo(875, 980, 330, 250, A, 27.6, color=AZ, seed=13)
      + mano(470, 1110, 'conserva su ' + marca('significado', A, 29.14), A, 29.0, size=56, color='var(--tinta)', rot=-2)
      + ticket(80, 1210, 920, [('<i>$</i> rag index ./docs <i>→</i> <b>pedazos</b>', 22.0, .6), ('<i>buscar</i> «cancelar plan» <i>≈</i> «dar de baja»', 29.95, .8)], A, rot=-1, size=34)
      + sello(80, 1470, 'Por idea ✓', A, 31.42, size=62, rot=-5, color=AZ)
      + sello(450, 1490, 'Palabra exacta ✕', A, 32.94, size=54, rot=6))
G6 = [(430 + (i % 3) * 190, 640 + (i // 3) * 200, f'0{10 + i * 4}') for i in range(6)]
f2 = (titular(['Paso 2', '*busca*'], A, 34.3, top=TOP, size=160, seed=7)
      + nota(80, 650, '¿cómo cancelo mi plan?', A, 34.5, rot=-4, w=300, size=54)
      + ''.join(pedazo(x, y, 170, 170, n, A, 34.7 + i * .07, rot=[-3, 2, -2, 3, -1, 2][i], seed=90 + i) for i, (x, y, n) in enumerate(G6))
      + flecha(370, 760, 430, 720, A, 35.2, color=AZ, curva=.3)
      + logo('', 110, 1000, 150, A, 35.0, rot=10, bg='#2457e6', emoji='🔍')
      + circulo(515, 725, 220, 210, A, 37.0, color=AZ, seed=14) + circulo(705, 725, 220, 210, A, 37.15, color=AZ, seed=15)
      + circulo(515, 925, 220, 210, A, 37.3, color=AZ, seed=16)
      + mano(430, 1100, 'los que más se ' + marca('parecen', A, 38.31), A, 38.2, size=56, color='var(--tinta)', rot=-2)
      + ticket(80, 1260, 920, [('<i>$</i> rag search <b>"pregunta"</b> <i>→ top 3</i>', 34.4, .6)], A, rot=1, size=36))
f3 = (titular(['Paso 3', '*contesta*'], A, 39.3, top=TOP, size=160, seed=8)
      + nota(80, 650, '¿cómo cancelo mi plan?', A, 39.4, rot=-4, w=300, size=54)
      + mano(395, 740, '+', A, 39.6, size=110, color=AZ, rot=0)
      + ''.join(pedazo(460 + i * 26, 640 + i * 30, 220, 170, ['014', '017', '031'][i], A, 39.7 + i * .1, rot=[-4, 2, 5][i], seed=100 + i) for i in range(3))
      + flecha(740, 760, 830, 760, A, 42.43, color=AZ, curva=-.3)
      + logo('', 830, 680, 160, A, 42.5, rot=-8, bg='#2457e6', emoji='🤖')
      + mano(420, 930, 'pregunta + pedazos', A, 42.43, size=58, color=AZ)
      + ticket(80, 1060, 920, [('<i>ia(</i><b>pregunta</b><i>,</i> <b>pedazos</b><i>)</i>', 39.4, .6), ('<i>›</i> contesta <b>usando solo eso</b> <i>✓</i>', 43.65, .7)], A, rot=-1, size=36)
      + recorte(80, 1300, 600, 230, ser('«Ve a <b>Ajustes › Plan</b> y toca <i>Dar de baja</i>.»', 46), A, 44.2, rot=2, seed=110, pad='34px 40px')
      + sello(700, 1380, 'Solo eso', A, 45.76, size=70, rot=-8, color=AZ))
escena('s2-pasos', S, 47.0, fz(f1, A, sale=34.2) + fz(f2, A, entra=34.26, sale=39.2) + fz(f3, A, entra=39.28), seed=3)

# ───────────────────────── 0:47 · libro entero vs la página que ocupa
S = 47.0; A = K.at(S)
f1 = (titular(['¿Le das *todo*', 'el contexto?'], A, 47.1, top=TOP, size=150, seed=9)
      + recorte(90, 660, 540, 680, caja('Libro<br>entero', 130, 'color:#2a1c0c') + f'<div class="mono" style="font-size:40px;margin-top:30px;color:#2a1c0c">'
                f'{N([(0, 1), (48.8, 412, 1.4)])} páginas</div>' + renglones(6, color='rgba(42,28,12,.25)'), A, 47.3, rot=-3, cls='kraft', seed=120, pad='46px 50px')
      + sello(120, 1370, 'Libro entero', A, 50.81, size=70, rot=-6)
      + logo('', 700, 860, 170, A, 52.2, rot=12, bg='#2457e6', emoji='🔍')
      + mano(660, 1060, '…y que encuentre', A, 52.28, size=56, color=RJ)
      + mano(680, 1130, 'la página', A, 52.6, size=56, color=RJ))
f2 = (titular(['Con RAG:', 'solo *esa página*'], A, 54.9, top=TOP, size=150, seed=10)
      + recorte(220, 650, 640, 720, f'<div class="mono" style="font-size:28px;font-weight:700;color:#8a8579">pág. 217</div>'
                + renglones(4) + f'<div style="margin-top:22px;font-size:40px;font-weight:700;line-height:1.25">{marca("Cancela en Ajustes › Plan", A, 56.69)}</div>'
                + renglones(5), A, 55.1, rot=1.5, seed=121, pad='44px 48px')
      + nota(90, 1400, 'tu pregunta', A, 59.36, rot=-5, w=300, size=58)
      + flecha(400, 1480, 560, 1360, A, 59.5, color=AZ))
escena('s3-libro', S, 60.3, fase(f1, A, sale=54.85) + fase(f2, A, entra=54.9), seed=4)

# ───────────────────────── 1:00 · mi ejemplo: el homelab recaba redes y proyectos → Claude contesta solo con eso (medio RAG)
S = 60.3; A = K.at(S)
RACK = ''.join(f'<div style="height:110px;margin-top:{16 if i else 0}px;border-radius:12px;background:#2a2926;display:flex;align-items:center;gap:14px;padding:0 26px">'
               + ''.join(f'<i class="led" style="width:20px;height:20px;border-radius:50%;background:#17a35a;box-shadow:0 0 14px #17a35a;animation:led .5s steps(1) {(i * 3 + j) * .17:.2f}s infinite"></i>' for j in range(3))
               + '<i style="flex:1;height:14px;margin-left:30px;background:#3d3b37;border-radius:6px"></i></div>' for i in range(3))
f1 = (titular(['Mi *homelab*'], A, 60.4, top=TOP, size=170, seed=11)
      + sello(640, 505, 'Medio RAG', A, 63.79, size=52, rot=-6, color=AZ)
      + recorte(80, 620, 420, 470, RACK, A, 60.8, rot=-2, cls='negro', seed=130, pad='30px')
      + numero(560, 620, N([(0, 0), (64.6, 1284, 3.0)], f='c'), A, 63.9, size=190, color=AZ)
      + mano(570, 790, 'registros recabados', A, 64.6, size=52)
      + logo('', 560, 990, 170, A, 66.77, rot=-8, bg='#ff8fb1', emoji='📣')
      + mano(540, 1180, 'redes sociales', A, 66.9, size=50)
      + logo('', 800, 990, 170, A, 67.51, rot=8, bg='#ffe14a', emoji='📁')
      + mano(810, 1180, 'proyectos', A, 67.6, size=50)
      + flecha(645, 975, 512, 900, A, 67.0, color=AZ, curva=.2) + flecha(885, 970, 512, 960, A, 67.7, color=AZ, curva=.15))
f2 = (titular(['Claude contesta', 'solo con *eso*'], A, 68.1, top=TOP, size=132, seed=12)
      + ticket(80, 650, 920, [('<i>›</i> claude: <b>¿cómo van mis redes?</b>', 68.05, .7), ('<i>contexto =</i> <b>datos guardados</b> <i>· nada más</i>', 70.45, .8)], A, rot=-1, size=36)
      + logo('claude', 760, 940, 220, A, 70.11, rot=-8, bg='#d97757', color='#fff')
      + recorte(80, 950, 600, 300, ser('Lo que se guardó en el homelab, <b>y nada más</b>.', 52), A, 70.6, rot=1.5, seed=131, pad='40px 44px')
      + sello(120, 1380, 'Solo esos datos', A, 72.46, size=72, rot=-6, color=AZ))
escena('s4-ejemplo', S, 77.3, fase(f1, A, sale=68.0) + fase(f2, A, entra=68.05),
       css='@keyframes led{50%{background:#0d4d2a;box-shadow:none}}', seed=5)

# ───────────────────────── 1:17 · > ⚠️ Ojo: mal cortado · desactualizado · búsqueda equivocada → revisa qué encontró
S = 77.3; A = K.at(S)
CAB = titular(['&gt; ⚠️ *Ojo*'], A, 77.4, top=TOP, size=120, seed=13) + mano(520, 330, 'tres cuidados', A, 77.9, size=62, color=RJ)
c1 = (sello(80, 520, '⚠ 1/3', A, 79.5, size=64, rot=-6)
      + titular(['Pedazos mal', '_cortados_'], A, 79.6, top=640, size=150, seed=14)
      + recorte(80, 960, 460, 220, ser('«El plan cuesta…', 54), A, 80.52, rot=-4, seed=140, pad='60px 40px')
      + recorte(570, 990, 430, 220, ser('…$99 al mes»', 54, 'color:#8a8579'), A, 80.7, rot=5, seed=141, pad='60px 40px')
      + mano(470, 1230, '✂ a medias', A, 83.51, size=70, color=RJ))
c2 = (sello(80, 520, '⚠ 2/3', A, 83.94, size=64, rot=-6)
      + titular(['Datos', '_desactualizados_'], A, 84.0, top=640, size=120, seed=15)
      + nota(100, 960, 'precio 2024:<br>$79', A, 85.13, rot=-5, w=360, size=62)
      + mano(500, 1060, '≠', A, 85.4, size=140, color=RJ, rot=0)
      + nota(620, 960, 'hoy:<br>$99', A, 85.6, rot=4, w=360, size=62, color='#b8f0c8')
      + sello(380, 1400, 'Ya no es cierto', A, 89.62, size=66, rot=-7))
c3 = (sello(80, 520, '⚠ 3/3', A, 90.72, size=64, rot=-6)
      + titular(['Búsqueda', '_equivocada_'], A, 90.8, top=640, size=150, seed=16)
      + ticket(80, 980, 920, [('<i>busca</i> «baja» <i>→ trae</i> «bajar precio»', 91.0, .9)], A, rot=-1, size=36)
      + tacha(640, 1040, 330, A, 92.34, grosor=12)
      + sello(380, 1240, 'Trae lo que no es', A, 92.34, size=62, rot=6))
c4 = (titular(['_Revisa_ qué', 'encontró'], A, 96.45, top=520, size=160, seed=17)
      + ticket(80, 900, 920, [('<i>$</i> rag search <b>--show-sources</b>', 96.5, .7), ('<i>✓</i> pedazo 017 · pedazo 031', 97.61, .6)], A, rot=-1, size=36)
      + palomita(720, 1250, 200, A, 97.61, color=VD))
escena('s5-ojo', S, 99.4, CAB + fz(c1, A, entra=79.5, sale=83.9) + fz(c2, A, entra=83.94, sale=90.67) + fz(c3, A, entra=90.72, sale=96.35)
       + fz(c4, A, entra=96.4), seed=6)

# ───────────────────────── 1:39 · ¿y el contexto largo? pocos docs: pásalos todos · miles: tokens, tiempo, se pierde a la mitad
S = 99.4; A = K.at(S)
f1 = (titular(['«Ya aguantan', 'mucho *contexto*»'], A, 99.6, top=TOP, size=140, seed=18)
      + mano(560, 600, 'es cierto ✓', A, 102.0, size=66, color=VD)
      + titular(['¿Pocos docs?'], A, 104.96, top=760, size=130, seed=19)
      + ''.join(hoja_doc(100 + i * 210, 980, 190, 250, f'{i + 1}.md', A, 105.1 + i * .1, rot=[-5, 3, -2, 4][i], seed=150 + i, n=5) for i in range(4))
      + sello(200, 1340, 'Pásale todos ✓', A, 107.34, size=70, rot=-5, color=AZ))
f2 = (titular(['¿Y con', '*miles*?'], A, 108.3, top=TOP, size=170, seed=20)
      + numero(80, 660, N([(0, 5), (108.3, 3000, 1.2)], f='c'), A, 108.3, size=230, color=AZ)
      + mano(90, 870, 'documentos', A, 109.12, size=56)
      + numero(560, 660, N([(0, 4), (109.7, 96, 1.4)], suf='%'), A, 109.7, size=230, color=RJ)
      + mano(570, 870, 'del límite', A, 110.0, size=56, color=RJ)
      + sello(90, 1020, '+ tokens', A, 110.87, size=72, rot=-6)
      + sello(500, 1070, '+ tiempo', A, 112.29, size=72, rot=5)
      + nota(300, 1180, 'se pierde<br>a la mitad 😵‍💫', A, 114.23, rot=-3, w=420, size=64, color='#ffd0dc'))
escena('s6-contexto', S, 115.5, fase(f1, A, sale=108.2) + fase(f2, A, entra=108.26), seed=7)

# ───────────────────────── 1:55 · funciona hoy → si tus datos ya no caben, ponlo a buscar antes de contestar
S = 115.5; A = K.at(S)
f1 = (titular(['Funciona', '*hoy*'], A, 115.6, top=TOP, size=200, seed=21)
      + palomita(780, 430, 190, A, 117.92, color=VD)
      + recorte(80, 760, 920, 200, ser('Con los modelos que tenemos <b>en 2026</b>.', 56), A, 116.3, rot=-1.5, seed=160, pad='46px 46px'))
f2 = (titular(['¿Ya no', '_caben_?'], A, 119.9, top=TOP, size=170, seed=22)
      + ticket(80, 680, 920, [('<i>si</i> <b>datos &gt; chat</b> <i>→</i>', 119.9, .6), ('<i>  1.</i> busca <i>· 2.</i> contesta', 122.0, .6)], A, rot=-1, size=38)
      + sello(600, 330, 'No caben', A, 121.25, size=60, rot=-8)
      + logo('', 120, 1020, 200, A, 122.93, rot=-8, bg='#2457e6', emoji='🔍')
      + mano(120, 1240, 'busca primero', A, 122.93, size=60, color=AZ)
      + flecha(360, 1120, 650, 1120, A, 123.4, color=AZ, curva=-.2)
      + logo('', 660, 1020, 200, A, 123.72, rot=8, bg='#17a35a', emoji='💬')
      + mano(640, 1240, 'luego contesta', A, 123.72, size=60, color=VD))
escena('s7-hoy', S, 124.7, fase(f1, A, sale=119.75) + fase(f2, A, entra=119.82), seed=8)

# ───────────────────────── 2:04 · resumen para guardar + pregunta
S = 124.7; A = K.at(S)
LISTA = ''.join(recorte(80, 820 + i * 175, 920, 150, f'<div style="display:flex;align-items:center;gap:26px;height:100%">'
                        f'<span class="mono" style="font-size:44px;font-weight:700;color:var(--azul);width:70px">{n}</span>{caja(t, 76)}</div>', A, t0,
                        rot=[-1.5, 1.2, -1, 1.5][i], seed=170 + i, pad='18px 40px', cinta=False)
                for i, (n, t, t0) in enumerate([('1', 'Prepara', 125.1), ('2', 'Busca', 125.35), ('3', 'Contesta', 125.6), ('&gt;', '⚠️ Revisa', 126.0)]))
escena('s8-pregunta', S, 128.75,
       titular(['¿Le pasas *todo*', 'a tu IA o la pones', 'a _buscar_ primero?'], A, 124.9, top=TOP, size=120, seed=23)
       + LISTA + mano(560, 1530, 'cuéntame 👇', A, 126.4, size=66, color=RJ), seed=9)

# ───────────────────────── 2:08 · cierre: «nos vemos cuando toque actualizar este README»
S = 128.75; A = K.at(S)
escena('s9-cierre', S, FIN,
       titular(['Nos vemos cuando', 'toque *actualizar*', 'este README'], A, 128.8, top=TOP, size=130, seed=24)
       + ticket(80, 820, 920, [('<i>⌘S</i> <b>README.md</b>', 129.0, .5)], A, rot=-1, size=44)
       + sello(400, 1060, '✓ guardado', A, 130.0, size=80, rot=-6, color=VD), sigue=False, seed=10)

# ───────────────────────── etiqueta de cinta arriba (todo el video, transparente): README.md · #02 RAG + sección actual
SECC = [(0.0, '# RAG'), (4.6, '## ¿Qué es?'), (21.85, '## Paso 1 · Prepara'), (34.2, '## Paso 2 · Busca'), (39.25, '## Paso 3 · Contesta'),
        (47.0, '## Libro vs página'), (60.3, '## Mi ejemplo'), (77.3, '&gt; ⚠️ Ojo'), (99.4, '## ¿Y el contexto largo?'), (115.5, '## Funciona hoy'),
        (124.7, '## Tu turno'), (128.75, '✓ guardado')]
A = K.at(0)
SEC = ''.join(f'<span class="sc" style="--d:{A(t)};{f"--x:{A(SECC[i + 1][0])};" if i + 1 < len(SECC) else ""}">{n}</span>' for i, (t, n) in enumerate(SECC))
ETQ_CSS = """
.lab{position:absolute;left:30px;right:30px;top:52px;height:150px;z-index:90;transform:rotate(-1deg);background:#ece2c8;
  box-shadow:0 8px 16px rgba(0,0,0,.22);animation:labIn .45s cubic-bezier(.2,1.3,.4,1) both;
  clip-path:polygon(0 6%,3% 0,6% 7%,9% 1%,12% 6%,100% 0,98% 22%,100% 40%,98% 62%,100% 80%,98% 100%,0 100%,2% 78%,0 56%,2% 34%)}
.lab:before{content:'';position:absolute;inset:0;background:url("FIBRA");opacity:.5}
@keyframes labIn{from{transform:translateY(-220px) rotate(-6deg)}to{transform:rotate(-1deg)}}
.lab .rd{position:absolute;left:44px;top:22px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:42px;color:#171513}
.lab .rd i{font-style:normal;color:var(--azul)}
.lab .sc{position:absolute;left:44px;top:80px;font-family:'Caveat',cursive;font-weight:700;font-size:54px;color:var(--azul);white-space:nowrap;opacity:0;
  animation:capIn .3s steps(2) var(--d) forwards}
.lab .sc[style*="--x"]{animation:capIn .3s steps(2) var(--d) forwards,capOut .01s linear var(--x) forwards}
@keyframes capIn{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}@keyframes capOut{to{opacity:0}}
.lab .nr{position:absolute;right:50px;top:30px;padding:8px 22px;border:6px solid var(--azul);border-radius:12px;color:var(--azul);font-weight:900;font-stretch:62%;
  font-size:62px;line-height:1;text-transform:uppercase;transform:rotate(4deg)}
""".replace('FIBRA', K.FIBRA)
ETQ = f'<div class="lab"><div class="rd">README.md <i>· #02 RAG</i></div>{SEC}<div class="nr">#02</div></div>'
PIEZAS.append(('etiqueta', 0.0, FIN, K.page(ETQ_CSS, ETQ, FIN, S0=0.0, transparente=True)))
PRE = 'rmr2-'

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
        rel = os.environ.get('REL', 'readme/2/recorte')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
