"""Archivo #01 · Knight Capital (45 minutos, 470 millones) · edición «Plano técnico» (blueprint).
Video 100 % animado sobre la voz (74.81 s): 7 hojas de plano a pantalla completa, contiguas; entre hojas la cámara barre el
plano (la retícula coincide en el corte). Encima, la capa de subtítulos como etiqueta de anotación técnica.
Tiempos = video final (voz/voz-editada.wav); cada idea entra con su palabra (W() busca en voz/palabras.json).
Uso: SALIDA=~/Documents/Videos/archivo/1/animaciones REL=archivo/1/animaciones python3 ejemplos/archivo01-plano.py [ids…]
     (SOLO_HTML=1 → solo escribe los .html; sin ids escribe además overlays-plano.json y lote-plano.json)
Los webm salen con prefijo «al1-».
"""
import json, math, os, re, subprocess, sys, unicodedata
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import plano as P
from plano import (linea, poli, rect, circ, flecha, cota, texto, etiqueta, sello, nube, tache, subraya, palomita, punteado,
                   caja_punteada, servidor_frente, servidor_iso, interruptor, sobre, reloj, codigo, campana, g, barrido, punta)

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
BASE = os.path.expanduser('~/Documents/Videos')
OUT = os.path.abspath(os.environ.get('SALIDA', os.path.join(BASE, 'archivo/1/animaciones')))
REL = os.environ.get('REL', 'archivo/1/animaciones')
VOZ = os.path.join(OUT, '..', 'voz')
WORK = os.path.join(OUT, '_html-plano'); os.makedirs(WORK, exist_ok=True)
PRE = 'al1-'
FIN = 74.81
TOTAL = 7
PIEZAS = []

_W = json.load(open(os.path.join(VOZ, 'palabras.json')))['words']
_norm = lambda s: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', s.lower()).encode('ascii', 'ignore').decode())


def W(palabra, desde=0.0):
    """Inicio de la primera `palabra` a partir del segundo `desde` (tiempo del video final)."""
    for w in _W:
        if w['start'] >= desde - .05 and _norm(w['word']) == _norm(palabra):
            return round(w['start'], 2)
    raise KeyError(f'{palabra} después de {desde}')


def hoja(pid, S, E, n, mundo, cam, chrome_t=None):
    PIEZAS.append((pid, S, E, P.page(S, round(E - S, 2), mundo, cam, n, TOTAL, chrome_t)))


# ── Hoja 1 · gancho: 470 millones en 45 minutos · ¿la razón? un servidor ───────────────────────────────────────
def h1():
    S, E = 0.0, 8.95
    t470, tmill, tdol, t45, tmin = W('470'), W('millones'), W('dólares'), W('45'), W('minutos')
    traz, tserv, tnadie, tact = W('razón'), W('servidor'), W('nadie'), W('actualizó')
    m = cota(120, 960, 300, 'PÉRDIDA', .15, .7, 30)
    m += texto(540, 640, '$470', t470 - .1, 330, 'big', 'middle', 'trazo', .75, lleno=t470 + .7)
    m += texto(540, 790, 'MILLONES', tmill, 130, 'big', 'middle', 'trazo', .5, lleno=tmill + .5)
    m += texto(540, 862, 'DE DÓLARES', tdol, 40, 'mono', 'middle', cls='fc')
    m += reloj(290, 1110, 128, t45 - .35, t45, tmin + .45 - t45)
    m += texto(470, 1190, '45', t45, 230, 'big', 'start', 'trazo', .5, lleno=t45 + .5)
    m += texto(712, 1190, 'MIN', tmin, 100, 'big', 'start', 'trazo', .4, lleno=tmin + .4)
    m += texto(472, 1252, '09:30 → 10:15', tmin + .35, 30, 'mono', cls='fc')
    # zona 2 (abajo): el servidor que nadie actualizó
    Y = 1920
    m += texto(540, Y + 300, '¿la razón?', traz - .3, 96, 'nota', 'middle', cps=22)
    m += servidor_frente(380, Y + 400, 320, 700, tserv - .15, 1.1)
    m += flecha([(800, Y + 330), (712, Y + 420)], tserv + .2, .3)
    m += texto(850, Y + 310, 'SERVIDOR', tserv + .3, 28, 'mono', 'middle')
    m += nube(345, Y + 365, 390, 770, tnadie, .5)
    m += texto(540, Y + 1235, 'nadie lo actualizó', tact - .05, 66, 'nota', 'middle', cps=48, cls='fr', rot=-3)
    ini, ent, sal = barrido(S, E, (540, 960, 1), (540, 960 + Y, 1), sin_entrada=True)
    cam = [ini] + [[traz - .5, .6, 540, 960 + Y, 1]] + sal
    hoja('h1-gancho', S, E, 1, m, cam, chrome_t=0.0)


# ── Hoja 2 · Knight Capital 2012 · sistema nuevo + interruptor que ya existía ─────────────────────────────────
def h2():
    S, E = 8.95, 21.65
    tpaso, tkn, tcap, temp, tacc, tmov, teu = W('pasó'), W('knight'), W('capital'), W('empresas'), W('acciones'), W('movían'), W('estados')
    test, tnuevo, tpren, tint, tya, tcod = W('estrenar'), W('nuevo'), W('prenderlo'), W('interruptor'), W('ya', 19), W('código', 20)
    m = etiqueta(540, 290, '01 · AGO · 2012', tpaso, 40, anchor='middle')
    m += texto(540, 560, 'KNIGHT', tkn - .05, 200, 'big', 'middle', 'trazo', .55)
    m += texto(540, 760, 'CAPITAL', tcap, 200, 'big', 'middle', 'trazo', .55)
    # diagrama de flujo: órdenes → Knight → bolsa
    for i, y in enumerate((930, 1040, 1150)):
        m += rect(70, y - 34, 180, 68, temp + i * .1, .3)
        m += texto(160, y + 9, 'ÓRDENES', temp + .15 + i * .1, 24, 'mono', 'middle')
        m += flecha([(256, y), (402, 1040)], tacc + i * .1, .35, 'ln c')
        m += flecha([(678, 1040), (782, y)], tmov + i * .1, .35, 'ln c')
        m += rect(788, y - 34, 140, 68, tmov + .1 + i * .1, .3)
    m += texto(858, 939, 'NYSE', tmov + .2, 24, 'mono', 'middle') + texto(858, 1049, 'NASDAQ', tmov + .3, 24, 'mono', 'middle')
    m += texto(858, 1159, 'OTROS', tmov + .4, 24, 'mono', 'middle')
    m += rect(408, 980, 264, 120, temp, .45, 'ln grueso')
    m += texto(540, 1056, 'KNIGHT', temp + .3, 52, 'big', 'middle', 'trazo', .4)
    m += texto(330, 900, 'acciones', tacc, 40, 'nota', 'middle', cls='fc', rot=-6)
    m += sello(540, 1240, 'TOP · EE. UU.', teu + .1, -5, 44, 'c')
    # zona B (derecha): el sistema nuevo y el interruptor
    X = 1320
    m += rect(X + 650, 440, 270, 170, test - .1, .45, 'ln grueso')
    m += texto(X + 785, 515, 'SISTEMA', test + .1, 36, 'mono', 'middle') + texto(X + 785, 565, 'NUEVO', tnuevo, 36, 'mono', 'middle', cls='fc')
    m += texto(X + 770, 400, '¡estreno!', test + .3, 64, 'nota', 'middle', cls='fc', rot=-5)
    m += interruptor(X + 300, 525, tpren - .1, [[-32], [tint + .5, .25, 0]], cables=170)
    m += texto(X + 375, 615, 'INTERRUPTOR', tint, 32, 'mono', 'middle')
    m += texto(X + 230, 860, 'ya existía', tya, 70, 'nota', 'middle', cls='fa', rot=-4)
    m += flecha([(X + 200, 790), (X + 290, 555)], tya + .3, .3, 'ln a')
    m += codigo(X + 450, 760, ['if (FLAG) {', '  arrancar()', '}'], tya + .2, 38, cps=36, gap=.1)
    m += caja_punteada(X + 70, 300, 860, 760, tcod - .45, .55)
    m += texto(X + 90, 285, 'SU CÓDIGO', tcod - .1, 30, 'mono', cls='fc')
    ini, ent, sal = barrido(S, E, (540, 960, 1), (540 + X, 960, 1))
    cam = [ini] + ent + [[test - .5, .65, 540 + X, 960, 1]] + sal
    hoja('h2-knight', S, E, 2, m, cam)


# ── Hoja 3 · ese interruptor prendía otro programa: Power Peg, apagado desde 2003 ────────────────────────────
def h3():
    S, E = 21.65, 31.5
    tprob, tint, tanos, tpren, totro, tuno, tviejo, tapag, tdesde, t2003, tnunca = (
        W('problema'), W('interruptor', 22), W('años'), W('prendía'), W('otro'), W('uno', 26), W('viejo', 26), W('apagado'),
        W('desde'), W('2003'), W('nunca'))
    m = interruptor(300, 420, S + .02, [[0]], cables=150, dur=.4)
    m += rect(640, 360, 270, 120, S + .1, .35)
    m += texto(775, 412, 'SISTEMA', S + .25, 30, 'mono', 'middle') + texto(775, 452, 'NUEVO', S + .3, 30, 'mono', 'middle', cls='fc')
    m += sello(560, 240, 'PROBLEMA', tprob, -6, 46)
    m += circ(375, 420, 120, tint, .45, 'ln r grueso')
    m += texto(250, 690, 'años antes…', tanos, 52, 'nota', 'middle', cls='fa', rot=-4)
    m += punteado('M460 430V880', tpren, .55, 'ln grueso')
    m += punta(460, 820, 460, 878, tpren + .5)
    m += caja_punteada(120, 885, 500, 210, totro - .2, .6)
    m += texto(370, 972, 'POWER PEG', tuno, 82, 'big', 'middle', 'trazo', .5)
    m += texto(370, 1016, 'programa viejo', tviejo, 30, 'mono', 'middle', cls='fc')
    m += sello(370, 1072, 'FUERA DE SERVICIO', tapag, 0, 22, 'b', doble=False)
    # línea de tiempo 2003 → 2012
    m += linea(140, 1230, 900, 1230, tdesde - .1, .5)
    for i in range(10):
        x = 140 + i * (760 / 9)
        m += linea(x, 1218, x, 1242, tdesde + i * .03, .1)
    m += texto(140, 1282, '2003', t2003, 36, 'mono', 'middle', cls='fr')
    m += texto(900, 1282, '2012', t2003 + .2, 36, 'mono', 'middle')
    m += cota(140, 900, 1170, '9 AÑOS APAGADO', t2003 + .35, .6, 28, 'ln a', 'fa')
    m += texto(790, 960, '¡nunca lo', tnunca, 56, 'nota', 'middle', cls='fr', rot=-5)
    m += texto(790, 1025, 'borraron!', tnunca + .35, 56, 'nota', 'middle', cls='fr', rot=-5)
    m += flecha([(680, 1000), (628, 1000)], tnunca + .6, .2, 'ln r')
    ini, ent, sal = barrido(S, E, (540, 960, 1), (540, 960, 1))
    hoja('h3-programa', S, E, 3, m, [ini] + ent + sal)


# ── Hoja 4 · versión nueva a 8 servidores… a 7 · abre la bolsa y el servidor olvidado despierta ──────────────
def h4():
    S, E = 31.5, 44.9
    tsub, t8, t7, tuno, tpaso = W('subieron'), W('8'), W('7'), W('uno', 36), W('pasó', 36)
    tabre, tpren, tint, tolv, tdesp, tprog = W('abre'), W('prende'), W('interruptor', 39), W('olvidado'), W('despierta'), W('programa', 43)
    m = etiqueta(540, 300, 'VERSIÓN NUEVA', tsub, 40, 'ln grueso', anchor='middle')
    pos = [(170 + 200 * (i % 4), 560 if i < 4 else 900) for i in range(8)]
    for i, (x, y) in enumerate(pos):
        m += servidor_iso(x, y, t8 + i * .07, 80, 140, 'ln')
        m += texto(x, y - 104, str(i + 1), t8 + .2 + i * .07, 26, 'mono', 'middle', cls='fc')
    # bus de despliegue: baja de la caja, corre sobre cada fila y llega a 7 de 8 (al 8 nunca le baja la línea)
    m += linea(540, 330, 540, 400, t7 - .25, .12, 'ln c') + linea(170, 400, 770, 400, t7 - .15, .3, 'ln c')
    m += poli([(170, 400), (60, 400), (60, 770), (570, 770)], t7 - .1, .35, 'ln c')
    for i, (x, y) in enumerate(pos[:7]):
        m += flecha([(x, 400 if i < 4 else 770), (x, y - 125)], t7 + .1 + i * .07, .15, 'ln c', 14)
        m += palomita(x + 64, y + 40, 18, t7 + .25 + i * .07)
    m += texto(300, 1200, '8 → 7', t7, 120, 'big', 'middle', 'trazo', .4)
    x8, y8 = pos[7]
    m += nube(x8 - 100, y8 - 120, 200, 290, tuno, .45)
    m += etiqueta(x8, y8 + 225, 'v.ANTERIOR', tuno + .3, 30, 'ln r', 'fr', anchor='middle')
    m += texto(740, 1250, 'se les pasó', tpaso - .1, 62, 'nota', 'middle', cls='fr', rot=-4, cps=30)
    # zona B (abajo): abre la bolsa, se prende el interruptor y despierta el programa viejo
    Y = 1920
    m += campana(200, Y + 300, 58, tabre - .05)
    m += etiqueta(290, Y + 300, '09:30 · ABRE LA BOLSA', tabre + .1, 30)
    m += interruptor(250, Y + 560, tpren - .25, [[-32], [tint, .25, 0]], cables=120)
    m += servidor_iso(540, Y + 700, tolv - .7, 170, 300, 'ln r grueso', .8, 6)
    m += linea(540 + 147 - 147, Y + 560, 540, Y + 560, tpren, .01, 'ln')
    m += texto(810, Y + 680, 'olvidado', tolv, 58, 'nota', 'middle', cls='fr', rot=-6)
    m += g(circ(600, Y + 820, 12, tdesp, .15, 'ln r grueso'), blink=(tdesp, E, .2))
    m += sello(215, Y + 930, 'DESPIERTA', tdesp + .1, -10, 50)
    m += punteado(f'M540 {Y + 1000}V{Y + 1110}', tdesp + .3, .3, 'ln r grueso')
    m += caja_punteada(230, Y + 1110, 620, 160, tdesp + .1, .5, 'ln r', solido=tprog)
    m += texto(540, Y + 1215, 'POWER PEG', tprog - .2, 84, 'big', 'middle', 'trazo', .45, cls='r', lleno=tprog + .4)
    ini, ent, sal = barrido(S, E, (540, 960, 1), (540, 960 + Y, 1))
    cam = [ini] + ent + [[tabre - .45, .6, 540, 960 + Y, 1]] + sal
    hoja('h4-servidores', S, E, 4, m, cam)


# ── Hoja 5 · compra caro, vende barato, sin parar · 97 correos que nadie leyó ────────────────────────────────
def h5():
    S, E = 44.9, 59.2
    temp, tcomp, tvend, tsin = W('empieza'), W('comprar'), W('vender'), W('sin', 48)
    tpeor, tantes, tmando, t97, tcorr, tavis, tnadie = W('peor'), W('antes', 50), W('mandó'), W('97'), W('correos'), W('avisando'), W('nadie', 57)
    m = servidor_iso(190, 500, S + .02, 70, 120, 'ln r grueso', .35)
    m += texto(190, 420, 'SRV 8', S + .2, 26, 'mono', 'middle', cls='fr')
    m += texto(190, 700, 'POWER PEG', temp, 30, 'mono', 'middle', cls='fr')
    m += flecha([(300, 520), (560, 360)], tcomp - .1, .35, 'ln c grueso', 30)
    m += etiqueta(580, 340, 'COMPRA · CARO', tcomp + .1, 34, 'ln c', 'fc')
    m += flecha([(300, 600), (560, 760)], tvend - .1, .35, 'ln r grueso', 30)
    m += etiqueta(580, 780, 'VENDE · BARATO', tvend + .1, 34, 'ln r', 'fr')
    lluvia = ''
    for i in range(26):
        a = -1.0 + 2.0 * P_h(i)
        L = 120 + 160 * P_h(i + 50)
        x0, y0 = 320, 560
        x1, y1 = x0 + L * math.cos(a) * 2.2, y0 + L * math.sin(a) * 1.9
        lluvia += flecha([(x0, y0), (min(930, x1), max(250, min(1000, y1)))], tsin + i * .04, .2, 'ln c fino' if i % 2 else 'ln r fino', 16)
    m += g(lluvia, jit=(tsin, E, 8))
    m += f'<text x="540" y="1150" text-anchor="middle" class="bc" style="font-size:130px" data-n="{tsin} 1.1 0 4000000 c" data-on="{tsin}"></text>'
    m += texto(540, 1222, 'OPERACIONES', tsin + .2, 32, 'mono', 'middle', cls='fc')
    # zona B (abajo): 97 correos
    Y = 1920
    m += texto(540, Y + 300, 'y lo peor…', tpeor - .25, 72, 'nota', 'middle', cls='fr', cps=30)
    m += etiqueta(540, Y + 390, '08:01 → 09:30 · ANTES DE ABRIR', tantes, 26, anchor='middle')
    sob = ''
    for i in range(97):
        x, y = 150 + 78 * (i % 10), Y + 460 + 56 * (i // 10)
        sob += sobre(x, y, 62, tmando + i * .017, .18, 'ln fino' if i else 'ln')
    m += sob
    m += f'<text x="520" y="{Y + 1170}" text-anchor="end" class="bc" style="font-size:120px" data-n="{tmando} 1.7 0 97" data-on="{tmando}"></text>'
    m += texto(545, Y + 1170, 'CORREOS', tcorr, 120, 'big', 'start', 'trazo', .5)
    card = (f'<rect x="120" y="{Y + 590}" width="840" height="230" class="tapa" stroke="#ffd166" stroke-width="5"/>'
            f'<text x="160" y="{Y + 660}" class="mono" style="font-size:28px;fill:#7fe3ff">DE: BNET · 08:01</text>'
            f'<text x="160" y="{Y + 730}" class="mono" style="font-size:36px">ASUNTO:</text>'
            f'<text x="160" y="{Y + 785}" class="mono" style="font-size:36px;fill:#ffd166">Power Peg disabled</text>'
            f'<path d="M860 {Y + 640}L910 {Y + 730}H810Z" class="ln a grueso"/><text x="860" y="{Y + 718}" text-anchor="middle" class="mono fa" style="font-size:44px">!</text>')
    m += g(g(card, pop=(tavis, .3)), on=(tavis, tnadie - .05))
    m += sello(540, Y + 760, '0 LEÍDOS', tnadie, -9, 92)
    ini, ent, sal = barrido(S, E, (540, 960, 1), (540, 960 + Y, 1))
    cam = [ini] + ent + [[tpeor - .45, .55, 540, 960 + Y, 1]] + sal
    hoja('h5-correos', S, E, 5, m, cam)


def P_h(i):
    x = math.sin(i * 12.9898 + 4.1) * 43758.5453
    return x - math.floor(x)


# ── Hoja 6 · lo apagaron, perdieron todo, empresa vendida · borra el código viejo ───────────────────────────
def h6():
    S, E = 59.2, 68.5
    tapag, tperd, temp, tterm = W('aunque'), W('perdido'), W('empresa', 62), W('terminó')
    tcod, tviejo, tpor, tborra = W('código', 65), W('viejo', 66), W('por', 66.5), W('bórralo')
    m = interruptor(300, 420, S + .02, [[0], [tapag + .35, .3, -32]], cables=150, dur=.35)
    m += etiqueta(540, 560, '10:15 · APAGADO', tapag + .5, 32, anchor='middle')
    m += cota(120, 960, 700, 'PÉRDIDA', tperd - .6, .6, 30, 'ln r', 'fr')
    m += texto(540, 900, '−$470 M', tperd, 190, 'big', 'middle', 'trazo', .6, cls='r')
    m += etiqueta(540, 1060, 'KNIGHT CAPITAL', temp - .1, 44, 'ln grueso', anchor='middle')
    m += sello(610, 1160, 'VENDIDA', tterm + .25, -9, 84)
    m += texto(540, 1290, '→ comprada por Getco (2013)', tterm + .7, 26, 'mono', 'middle', cls='fc', cps=60)
    X = 1320
    m += caja_punteada(X + 190, 430, 700, 330, tcod - .3, .55)
    m += etiqueta(X + 540, 390, 'CÓDIGO VIEJO · APAGADO', tviejo, 28, anchor='middle')
    m += codigo(X + 230, 470, ['def power_peg():', '  # apagado desde 2003', '  ...'], tcod - .1, 30, 'ln tenue', w=620, cps=70, gap=.05)
    m += texto(X + 540, 900, '«por si acaso…»', tpor, 62, 'nota', 'middle', cps=32)
    m += linea(X + 190, 430, X + 890, 760, tborra, .2, 'ln r grueso') + linea(X + 890, 430, X + 190, 760, tborra + .12, .2, 'ln r grueso')
    m += sello(X + 540, 1080, 'BÓRRALO', tborra + .2, -8, 88)
    ini, ent, sal = barrido(S, E, (540, 960, 1), (540 + X, 960, 1))
    cam = [ini] + ent + [[tcod - .55, .55, 540 + X, 960, 1]] + sal
    hoja('h6-final', S, E, 6, m, cam)


# ── Hoja 7 · deja de subir cambios a mano: automatízalo · cierre de la serie ────────────────────────────────
def h7():
    S, E = 68.5, FIN
    ttod, tsub, tmano, thoy, tbuen, tauto = W('todavía'), W('subes'), W('mano'), W('hoy'), W('buen'), W('automatizarlo')
    m = rect(90, 330, 180, 100, S + .05, .3) + texto(180, 395, 'TÚ', S + .2, 44, 'mono', 'middle')
    xs = [150 + 105 * i for i in range(8)]
    for i, x in enumerate(xs):
        m += servidor_iso(x, 700, ttod + i * .05, 40, 80, 'ln', .3, 2)
        m += flecha([(180, 432), (x, 610)], tsub + i * .1, .18, 'ln fino', 14)
    m += texto(620, 420, 'a mano', tmano - .1, 66, 'nota', 'middle', cls='fr', rot=-5)
    m += subraya(520, 720, 440, tmano + .25)
    # tubería automática
    cajas = [('COMMIT', 90), ('PRUEBAS', 390), ('DEPLOY ×8', 690)]
    for i, (txt, x) in enumerate(cajas):
        m += rect(x, 940, 260, 110, thoy + i * .25, .3, 'ln c grueso')
        m += texto(x + 130, 1007, txt, thoy + .15 + i * .25, 32, 'mono', 'middle', cls='fc')
        if i:
            m += flecha([(x - 40, 995), (x - 6, 995)], thoy + i * .25 - .1, .15, 'ln c')
    m += texto(540, 900, 'hoy es buen día', thoy, 52, 'nota', 'middle', cls='fa', rot=-3, cps=34)
    for i, x in enumerate(xs):
        m += palomita(x, 820, 16, tauto - .2 + i * .04)
    # cierre de la serie (abajo)
    Y = 1920
    tc = 73.45
    m += rect(120, Y + 470, 840, 720, tc, .5, 'ln grueso') + rect(140, Y + 490, 800, 680, tc + .1, .5, 'ln fino')
    m += texto(540, Y + 740, 'ARCHIVO', tc + .15, 210, 'big', 'middle', 'trazo', .5)
    m += linea(180, Y + 790, 900, Y + 790, tc + .3, .3)
    m += texto(540, Y + 850, '#01 · KNIGHT CAPITAL · 2012', tc + .35, 30, 'mono', 'middle', cls='fc', cps=70)
    m += texto(540, Y + 990, 'Sígueme para más', tc + .45, 64, 'nota', 'middle', cps=50)
    m += texto(540, Y + 1070, 'historias', tc + .7, 64, 'nota', 'middle', cps=40)
    m += sello(760, Y + 1150, 'REVISADO', tc + 1.0, -10, 44)
    ini, ent, sal = barrido(S, E, (540, 960, 1), (540, 960 + Y, 1))
    cam = [ini] + ent + [[tc - .45, .5, 540, 960 + Y, 1]]
    hoja('h7-cierre', S, E, 7, m, cam)


def sub():
    G = json.load(open(os.path.join(VOZ, 'grupos.json')))
    PIEZAS.append(('sub', 0.0, FIN, P.subtitulos(G, FIN)))


for fn in (h1, h2, h3, h4, h5, h6, h7, sub):
    fn()


def main():
    ids = sys.argv[1:]
    sel = [p for p in PIEZAS if not ids or p[0] in ids]
    lote, ovs = [], []
    for pid, S, E, html in sel:
        ruta = os.path.join(WORK, pid + '.html')
        open(ruta, 'w').write(html)
        lote.append(dict(html=ruta, dur=round(E - S, 2), out=os.path.join(OUT, f'{PRE}{pid}.webm')))
    for pid, S, E, _ in PIEZAS:
        ovs.append(dict(file=f'{REL}/{PRE}{pid}.webm', html=f'{REL}/_html-plano/{pid}.html', start=S, end=E, trimIn=0, scale=1, position='center'))
    print(f'{len(sel)} páginas en {WORK}')
    if not ids:
        json.dump(ovs, open(os.path.join(OUT, 'overlays-plano.json'), 'w'), ensure_ascii=False, indent=1)
        json.dump(lote, open(os.path.join(OUT, 'lote-plano.json'), 'w'), ensure_ascii=False, indent=1)
    if not os.environ.get('SOLO_HTML'):
        lp = os.path.join(WORK, '_lote.json')
        json.dump(lote, open(lp, 'w'))
        subprocess.run(['node', CAP, '--lote', lp], check=True)


if __name__ == '__main__':
    main()
