"""Devlog 1 · «¿cómo hago mis videos?» (Claude Code + el motor de animaciones) · edición «Recorte», dos propuestas:
  A = como El Log: escenas a pantalla completa encadenadas casi todo el video; la cámara solo asoma en el gancho, el repo, el logo
      de Arc en la mano, el editor en vivo, la Mac y el cierre.
  B = devlog con más animación: tarjetas de papel en la franja de arriba (sobre las repisas, sin tapar los monitores) y solo dos
      escenas a pantalla completa para lo que la cámara no enseña (voz → texto → guion y el tiempo de grabación con dos compus).
Las dos llevan el logo de Arc pegado a la mano abierta (posiciones medidas cuadro a cuadro en IMG_5961) y el Sígueme.
Tiempos = timeline final de devlog/1 (154.70 s), anclados a palabras de voz/palabras.json con W().
Uso: PROP=A|B SALIDA=~/Documents/Videos/devlog/1/animaciones REL=devlog/1/animaciones python3 ejemplos/devlog01-recorte.py [ids…]
     (SOLO_HTML=1 para revisar; escribe overlays-<PROP>.json y escenas-<PROP>.json = tramos a pantalla completa para el manifiesto)
Prefijo de archivos: «dr1-».
"""
import json, os, re, subprocess, sys, unicodedata
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import recorte as K
from recorte import titular, flecha, recorte, nota, sello, ticket, N, logo, mano, fase, subraya, circulo, tacha, palomita

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
VID = os.path.expanduser('~/Documents/Videos/devlog/1')
OUT = os.path.abspath(os.environ.get('SALIDA', os.path.join(VID, 'animaciones')))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
PROP = os.environ.get('PROP', 'A')
PRE = 'dr1-'
FIN = 154.70
PIEZAS = []          # (id, inicio, fin, html, propuestas, pantalla_completa)

_PAL = json.load(open(os.path.join(VID, 'voz', 'palabras.json')))['words']


def _n(s):
    s = unicodedata.normalize('NFD', s.lower())
    return re.sub(r'[^a-z0-9ñ%]', '', ''.join(c for c in s if unicodedata.category(c) != 'Mn'))


def W(palabra, n=1, desde=0.0):
    """Inicio de la n-ésima vez que se dice `palabra` desde el segundo `desde` (video final)."""
    k = 0
    for w in _PAL:
        if w['start'] >= desde and _n(w['word']) == _n(palabra):
            k += 1
            if k == n:
                return round(w['start'], 2)
    raise KeyError(f'{palabra} n={n} desde {desde}')


CSS = """
.ar{font-weight:900;font-stretch:62%;text-transform:uppercase;line-height:.9}
.cv{font-family:'Caveat',cursive;font-weight:700}
.rw{animation:slam .4s cubic-bezier(.2,1.5,.4,1) var(--d) both}
.on{opacity:0;animation:apar .01s linear var(--d) forwards}
.onoff{opacity:0;animation:apar .01s linear var(--d) forwards,quita .01s linear var(--q) forwards}
@keyframes quita{to{opacity:0}}
.bar{height:64px;border-radius:8px 18px 10px 20px;transform-origin:left center;transform:scaleX(0) skewX(-6deg);animation:barra .8s steps(8) var(--d) forwards}
@keyframes barra{to{transform:scaleX(1) skewX(-6deg)}}
.cm{display:flex;gap:18px;align-items:flex-start}.cm .av{flex-shrink:0;width:64px;height:64px;border-radius:50%;background:var(--c,#8c7cf0);color:#fff;
  display:flex;align-items:center;justify-content:center;font-weight:900;font-size:34px}
.cm .q{font-family:'Instrument Serif',serif;font-style:italic;line-height:1.08}
.cm small{display:block;font-family:'JetBrains Mono',monospace;font-size:24px;color:#8a8579;margin-bottom:4px}
.nav{display:flex;gap:10px;align-items:center;padding:14px 18px;background:#1b1a18;border-radius:14px 14px 0 0}
.nav i{width:18px;height:18px;border-radius:50%;background:#e3342a}.nav i+i{background:#ffe14a}.nav i+i+i{background:#17a35a}
.nav b{margin-left:14px;flex:1;background:#3a3834;color:#d8d2c4;border-radius:10px;padding:4px 16px;font:500 24px 'JetBrains Mono',monospace}
"""


def ar(txt, size, extra=''):
    return f'<div class="ar" style="font-size:{size}px;{extra}">{acento(txt)}</div>'


def acento(s):
    return re.sub(r'\*(.+?)\*', r'<span style="font-family:\'Instrument Serif\',serif;font-style:italic;font-weight:400;font-stretch:100%;'
                  r'text-transform:none;color:var(--rojo);font-size:1.08em">\1</span>', s)


def cartel(x, y, w, h, lineas, A, t, size=90, rot=-2.0, seed=11, pad='26px 34px', sale=None, cls=''):
    """Titular sobre papel (sobre la cámara un titular suelto no se lee)."""
    return recorte(x, y, w, h, ''.join(ar(l, size) for l in lineas), A, t, sale=sale, rot=rot, seed=seed, pad=pad, cls=cls)


def sellop(x, y, txt, A, t, size=56, rot=-6.0, color=None):
    """Sello sobre etiqueta de papel (se lee encima de la cámara)."""
    return sello(x, y, txt, A, t, size=size, rot=rot, color=color).replace('style="', 'style="background:#fbf8f1;-webkit-mask:none;mask:none;box-shadow:0 12px 20px rgba(0,0,0,.35);', 1)


CAM = '.mano{text-shadow:0 3px 0 rgba(0,0,0,.85),0 0 14px rgba(0,0,0,.75)}'


def tarjeta(pid, start, end, body, props='AB'):
    """Tarjeta transparente sobre la cámara; al final todo el grupo se barre (sin desvanecido)."""
    A = K.at(start)
    body = fase(body, A, sale=round(end - .5, 2))
    PIEZAS.append((pid, start, end, K.page(CSS + CAM, body, round(end - start, 2), S0=start, transparente=True), props, False))


def escena(pid, start, end, fases, props, fondo='papel', seed=1, ac='var(--rojo)', sale=True):
    """Escena a pantalla completa: la hoja entra rasgada; fases = [(html, fin_de_fase)] (cada grupo se barre al acabar su fase);
    al final la hoja completa se barre y debajo ya corre la cámara."""
    A = K.at(start)
    body = ''.join(fase(h, A, sale=(round(f - .45, 2) if f is not None else None)) for h, f in fases)
    dur = round(end - start, 2)
    css = CSS + (f'body{{animation:salehoja .5s cubic-bezier(.6,0,.9,.4) {dur - .5:.2f}s forwards}}'
                 '@keyframes salehoja{to{transform:translate(-1250px,260px) rotate(-14deg)}}' if sale else '')
    PIEZAS.append((pid, start, end, K.page(css, body, dur, S0=start, fondo=fondo, seed=seed, ac=ac), props, True))


# ═════════════════════════ piezas compartidas (cámara a la vista) ═════════════════════════
# Zonas libres de la cámara: tomas 5957–5960 y 5967–5968 (monitor lejos) → franja de arriba hasta y≈560; tomas 5962–5964 (cerca, la
# vista previa del editor ocupa x 240–520) → columna derecha x 570–1040; toma 5965 (modo comparar a todo lo ancho) → franja y 150–430.

# 0:00 · gancho · «Todas esas animaciones las hizo Claude y tú puedes tener un video así sin saber editar»
S = 0.0; A = K.at(S)
tarjeta('c01-gancho', S, 5.40,
        cartel(60, 190, 720, 330, ['Todo esto', 'lo animó *Claude*'], A, W('todas'), size=96, rot=-2, seed=3)
        + flecha(600, 470, 470, 700, A, W('animaciones') + .5, color='var(--amarillo)', curva=-.3, grosor=12)
        + sellop(650, 500, 'Sin editar', A, W('editar'), rot=7, size=56))

# 0:05 · «si ya usas Claude Code, es completamente gratis: clonas mi repo, le dices que lea el README y le pides un video»
S = 5.35; A = K.at(S)
T_CLONA = W('clonas')
tarjeta('c02-repo', S, 16.70,
        fase(nota(60, 200, '¿Ya usas<br>Claude Code?', A, W('usas'), rot=-5, w=340, size=56)
             + sellop(470, 250, '100% gratis', A, W('gratis'), rot=-6, size=70, color='var(--verde)'), A, sale=T_CLONA - .5)
        + ticket(70, 190, 940, [('<i>$</i> git clone <b>Arzival/videoAssembler</b>', T_CLONA, .7),
                                ('<i>›</i> lee el README', W('dices'), .5),
                                ('<i>›</i> créame un video 🎬', W('pides'), .6)], A, rot=-1.5, size=38))

# 0:52 · el logo de Arc entra… «cuando yo digo ARC» → pegado a la palma abierta (IMG_5961, medido cuadro a cuadro)
T_ARC = W('ark', 2)
S = round(T_ARC - .35, 2); E = 53.90; A = K.at(S)
CAMINO = [(53.00, 760, 1170), (53.30, 768, 1185), (53.45, 765, 1180), (53.60, 772, 1190), (53.72, 790, 1215), (53.90, 860, 1330)]
kf = ''.join(f'{(t - S) / (E - S) * 100:.1f}%{{transform:translate({x - 130}px,{y - 130}px)}}' for t, x, y in [(S, *CAMINO[0][1:])] + CAMINO)
ARC = (f'<div style="position:absolute;left:0;top:0;animation:palma {E - S:.2f}s linear both">'
       + logo('arc', 0, 0, 260, A, T_ARC - .05, sale=53.66, rot=-8, bg='#e3342a', color='#ffffff') + '</div>')
html = K.page(CSS + f'@keyframes palma{{{kf}}}', ARC, round(E - S, 2), S0=S, transparente=True).replace('const _Q=1000/12', 'const _Q=1000/60')
PIEZAS.append(('m-arc', S, E, html, 'AB', False))

# 1:21 · «antes de renderizarlo lo veo en vivo en el editor; con el modo de comparar puedo ver hasta 4 videos a la vez» (columna derecha)
S = 81.25; A = K.at(S)
tarjeta('c08-vivo', S, 89.45,
        sellop(610, 180, '● En vivo', A, W('vivo'), rot=-5, size=62, color='var(--rojo)')
        + mano(620, 300, 'sin renderizar', A, W('editor') + .2, size=54, color='var(--amarillo)', rot=-3)
        + recorte(600, 390, 420, 250, ar('Comparar', 60) + f'<div class="ar" style="font-size:130px;color:var(--azul)">{N([(0, 1), (W("4"), 4, .5)])}</div>'
                  + '<div class="cv" style="font-size:38px">videos a la vez</div>', A, W('comparar'), rot=3, seed=81, pad='22px 34px'))

# 1:46 · «lo que estamos viendo aquí es la Mac… y también ocupo la Legion que forma parte de mi homelab» (franja de arriba)
for pid, S, props in (('c10-compus', 104.55, 'B'), ('c10-compus-a', 105.95, 'A')):
    A = K.at(S)
    tarjeta(pid, S, 112.70,
            cartel(50, 170, 350, 260, ['Dos', '*compus*'], A, W('dos', 1, 104), size=88, rot=-3, seed=12)
            + recorte(420, 180, 280, 140, ar('🍎 Mac', 76), A, W('mac', 1, 105), rot=-3, seed=101, pad='30px 30px')
            + mano(450, 340, 'esta ↓', A, W('mac', 1, 105) + .3, size=58, color='var(--amarillo)', rot=4)
            + recorte(730, 170, 310, 200, ar('Legion', 72) + '<div class="cv" style="font-size:36px;color:#d8d2c4">en mi homelab</div>', A, W('legion'), rot=4,
                      cls='negro', seed=102, pad='26px 30px'), props=props)

# 2:18 · «…recuerda que el repo es 100% gratis. Te lo dejo en el link que tienes en mi biografía»
S = 138.75; A = K.at(S)
tarjeta('c12-gratis', S, 147.05,
        ticket(70, 190, 760, [('<i>github.com/</i><b>Arzival</b>/videoAssembler', W('repo', 2) - .3, .8)], A, rot=-2, size=36)
        + sellop(560, 340, '100% gratis', A, W('100%'), rot=-7, size=70, color='var(--verde)')
        + nota(80, 330, '🔗 link en<br>mi bio', A, W('link'), rot=-4, w=330, size=56))

# 2:27 · Sígueme + «¿qué video harías tú, ahora que la IA lo puede animar?»
S = 147.20; A = K.at(S)
_r = 'Mi tutorial… ¡sin editar! 🎬'
SEG = (nota(610, 190, '<div style="font-size:42px">Sígueme</div><div class="ar" style="font-size:88px;font-family:Archivo">Armando</div>'
                      '<div style="font-size:38px;margin-top:6px">homelab · IA · código</div>', A, S + .2, rot=4, w=400, size=56)
       + sellop(660, 580, 'Seguir ✓', A, W('animar') + .3, size=56, rot=-5, color='var(--verde)')
       + recorte(60, 210, 520, 330, '<div class="ser" style="font-size:46px;line-height:1.1">🎬 ¿Qué video harías tú si la IA lo anima?</div>'
                 f'<div style="margin-top:20px;font-family:Caveat;font-weight:700;font-size:40px;color:var(--azul);white-space:nowrap;'
                 f'clip-path:inset(0 100% 0 0);animation:tip 1s steps({len(_r) + 1}) {A(W("animar") + .9)} forwards">{_r}</div>',
                 A, W('que', 1, 147.5), rot=-3, seed=57))
PIEZAS.append(('seguir', S, FIN, K.page(CSS, SEG, round(FIN - S, 2), S0=S, transparente=True), 'AB', False))


# ═════════════════════════ contenidos (tarjeta en B, fase de escena a pantalla completa en A) ═════════════════════════
def f_comentarios(A, carta):
    """«Me han preguntado cómo es que hago mis videos y sí, uso Claude Code, pero ojo, Claude Code no edita solamente a mano»."""
    q1 = ('<div class="cm" style="--c:#8c7cf0"><div class="av">G</div><div><small>comentario · hace 2 d</small>'
          f'<div class="q" style="font-size:{44 if carta else 62}px">«Bro, ¿cómo haces esos videos? ¿Usas Claude?»</div></div></div>')
    if carta:
        return (recorte(60, 180, 700, 210, q1, A, W('preguntado'), rot=-2, seed=31, pad='30px 34px')
                + sellop(520, 420, 'Sí: Claude Code', A, W('uso'), rot=-5, size=48, color='var(--verde)')
                + cartel(60, 410, 400, 140, ['Pero *ojo* 👀'], A, W('ojo'), size=76, rot=3, seed=34))
    return (recorte(70, 330, 940, 320, q1, A, W('preguntado'), rot=-2, seed=31, pad='44px 44px')
            + sello(110, 720, 'Sí: Claude Code', A, W('uso'), rot=-6, size=92, color='var(--verde)')
            + titular(['Pero *ojo* 👀'], A, W('ojo'), top=1000, size=170, seed=33)
            + mano(130, 1220, 'no edita solo, a mano', A, W('edita') + .2, size=80, rot=-3))


MIO = [('📱 grabo mis tomas', W('grabo')), ('🎙️ grabo mi voz', W('voz')), ('🗣️ le digo qué video', W('digo')), ('✅ reviso y apruebo', W('reviso'))]


def f_mio(A, carta):
    """«Yo solo grabo mis tomas con el teléfono y también mi voz. Ya después le digo qué video es el que quiero, reviso y apruebo»."""
    filas = ''.join(f'<div class="fade0" style="--d:{A(t)};font-family:Caveat;font-weight:700;font-size:{48 if carta else 76}px;line-height:1.14">{tx}</div>'
                    for tx, t in MIO)
    if carta:
        return (recorte(60, 180, 600, 330, filas, A, MIO[0][1] - .3, rot=-2, seed=41, pad='26px 36px')
                + cartel(700, 190, 330, 220, ['Mi', '*parte*'], A, W('yo'), size=96, rot=3, seed=42)
                + sellop(700, 450, 'Solo esto', A, W('apruebo') + .1, rot=-8, size=48))
    return (titular(['Lo que hago', '*yo*'], A, W('yo'), top=330, size=170, seed=42)
            + recorte(80, 740, 920, 480, filas, A, MIO[0][1] - .3, rot=-1.5, seed=41, pad='44px 54px')
            + sello(520, 1290, 'Solo esto', A, W('apruebo') + .1, rot=-8, size=96))


def f_voz(A):
    """«Primero Claude pasa mi voz a texto, palabra por palabra. Eso corre en mi propia computadora»."""
    lineas = [(f'<i>[{W(p, n, 31):05.2f}]</i> {p}', W(p, n, 31) + .1, .3) for p, n in (('palabra', 1), ('por', 1), ('palabra', 2))]
    return (titular(['Tu voz', '→ *texto*'], A, W('primero'), top=330, size=200, seed=51)
            + ticket(90, 790, 700, lineas, A, rot=-2, size=56)
            + logo('apple', 770, 900, 240, A, W('computadora') - .2, rot=8, emoji='💻')
            + sello(110, 1250, '100% local', A, W('propia'), rot=-6, size=110, color='var(--azul)')
            + mano(150, 1500, 'nada sale de mi compu', A, W('computadora') + .3, size=74, rot=-3))


def f_errores(A):
    """«…y luego quita los silencios y también todos los errores que cometí a la hora de grabar» (en este video: 3 intentos)."""
    tomas = [('Primero Claude pasa mi voz… y eso ocurre', 'intento 1'), ('Primero Claude pasa mi voz… las equivocaciones', 'intento 2'),
             ('Primero Claude pasa mi voz a texto', 'el bueno ✓')]
    h = titular(['Quita *silencios*', 'y _errores_'], A, W('quita'), top=330, size=150, seed=52)
    t0 = W('errores')
    for i, (tx, et) in enumerate(tomas):
        y = 730 + i * 240
        h += recorte(70, y, 940, 190, f'<div class="ser" style="font-size:54px">«{tx}»</div><div class="cv" style="font-size:42px;color:#8a8579">{et}</div>',
                     A, W('silencios') + i * .35, rot=[-1.5, 1, -1][i], seed=53 + i, pad='26px 36px', cinta=False)
        if i < 2:
            h += tacha(90, y + 120, 900, A, t0 + i * .4, grosor=18, seed=60 + i)
    return h + palomita(880, 1240, 110, A, W('grabar') - .3) + mano(330, 1560, 'en este mismo video 😅', A, W('grabar') + .2, size=80, rot=-3)


def f_guion(A):
    """«Después de que ya tiene todo eso, escribe un guion para la animación. Cada escena entra justo cuando digo una palabra.
    Por ejemplo, el logo de Arc entra cuando yo digo Arc»."""
    return (titular(['Escribe el', '*guion*'], A, W('despues', 1, 42) + .2, top=330, size=200, seed=61)
            + ticket(70, 790, 940, [('{ <b>"plantilla"</b>: "logo",', W('guion') + .2, .6),
                                    ('  <b>"logo"</b>: "arc",', W('animacion') + .1, .5),
                                    ('  <b>"entra"</b>: {"palabra": <b>"Arc"</b>} }', W('cada') + .1, .8)], A, rot=-1.5, size=44)
            + mano(120, 1170, 'entra justo en esa palabra ↓', A, W('justo'), size=74, rot=-3)
            + logo('arc', 620, 1300, 300, A, W('ark') - .05, rot=-8, bg='#e3342a', color='#ffffff'))


def f_datos(A, carta):
    """«Y aquí viene lo importante: Claude no escribe código nuevo en cada video, solo va cambiando los datos que están en pantalla»."""
    vals = [('Arc se apaga', W('datos') - .8), ('PHP2Shell', W('datos') + .2), ('RAG', W('pantalla'))]
    v = ''.join(f'<span class="onoff" style="position:absolute;left:0;top:0;white-space:nowrap;--d:{A(t)};--q:{A(vals[i + 1][1]) if i + 1 < len(vals) else "999s"}">"{x}"</span>'
                for i, (x, t) in enumerate(vals))
    js = (f'<div style="font:500 {34 if carta else 52}px/1.4 \'JetBrains Mono\',monospace">{{ <b style="color:var(--rojo)">"titulo"</b>:<br>'
          f'&nbsp;&nbsp;<span style="position:relative;display:inline-block;width:80%;height:1.3em;color:var(--azul)">{v}</span> }}</div>')
    if carta:
        return (recorte(580, 170, 440, 150, ar('Código nuevo', 60), A, W('codigo') - .1, rot=-3, seed=71, pad='40px 30px')
                + tacha(600, 270, 400, A, W('nuevo') + .2, seed=72)
                + recorte(580, 360, 450, 170, js, A, W('datos') - .9, rot=2, seed=73, pad='26px 30px')
                + mano(560, 560, 'solo cambian los datos ✓', A, W('datos') + .1, size=46, color='var(--amarillo)'))
    return (titular(['Lo *importante*'], A, W('importante') - .3, top=330, size=160, seed=71)
            + recorte(80, 580, 900, 210, ar('Código nuevo', 110), A, W('codigo') - .1, rot=-3, seed=72, pad='40px 40px')
            + tacha(100, 700, 820, A, W('nuevo') + .2, grosor=18, seed=73)
            + recorte(80, 900, 920, 280, js, A, W('datos') - .9, rot=1.5, seed=74, pad='44px 50px')
            + mano(150, 1240, 'solo cambian los datos ✓', A, W('datos') + .1, size=80, color='var(--verde)')
            + nota(600, 1360, 'mismas plantillas,<br>otro video', A, W('pantalla'), rot=4, w=400, size=54))


def f_web(A, carta):
    """«Por eso le puedo pedir video tras video: cada animación es una página web y un navegador escondido graba cada video con transparencia»."""
    win = (f'<div class="nav"><i></i><i></i><i></i><b>escena.html</b></div><div style="background:#fbf8f1;padding:{16 if carta else 34}px 26px">'
           f'{ar("Arc se *apaga*", 52 if carta else 100)}</div>')
    if carta:
        return (recorte(580, 170, 440, 190, win, A, W('pagina'), rot=-3, seed=81, pad='0', cinta=False)
                + mano(600, 380, '= una página web', A, W('web'), size=48, color='var(--amarillo)')
                + recorte(600, 470, 420, 170, ar('🎥 .webm', 64) + '<div class="cv" style="font-size:36px;color:#d8d2c4">con transparencia</div>',
                          A, W('transparencia') - .3, rot=4, cls='negro', seed=82, pad='26px 30px'))
    return (titular(['Video tras', '*video*'], A, W('video', 1, 63) - .1, top=330, size=160, seed=81)
            + recorte(70, 700, 680, 340, win, A, W('pagina'), rot=-3, seed=82, pad='0', cinta=False)
            + mano(110, 1070, '= una página web', A, W('web'), size=76)
            + nota(640, 1060, 'un navegador<br>escondido la graba 🕶️', A, W('navegador'), rot=5, w=390, size=52)
            + recorte(110, 1340, 600, 240, ar('🎥 .webm', 120) + '<div class="cv" style="font-size:50px;color:#d8d2c4">con transparencia</div>',
                      A, W('transparencia') - .3, rot=-2, cls='negro', seed=83, pad='30px 40px'))


def f_motor(A, carta):
    """«Al principio estaba ocupando HyperFrames, pero tomé esa idea base y terminé construyendo este motor de animaciones»."""
    q2 = ('<div class="cm" style="--c:#17a35a"><div class="av">M</div><div><small>comentario</small>'
          f'<div class="q" style="font-size:{40 if carta else 60}px">«¿Claude + HyperFrames?»</div></div></div>')
    if carta:
        return (recorte(570, 170, 470, 170, q2, A, W('hyperframes') - .5, rot=-2, seed=91, pad='28px 30px')
                + mano(600, 370, 'la idea base 💡', A, W('idea'), size=52, color='var(--amarillo)')
                + sellop(600, 470, 'Motor propio', A, W('motor'), rot=-7, size=60, color='var(--rojo)'))
    return (recorte(70, 330, 940, 220, q2, A, W('hyperframes') - .5, rot=-2, seed=91, pad='40px 40px')
            + titular(['HyperFrames'], A, W('hyperframes'), top=660, size=150, seed=92)
            + mano(120, 830, '→ la idea base 💡', A, W('idea'), size=76)
            + tacha(80, 760, 700, A, W('final'), grosor=16, seed=93)
            + titular(['Mi *motor*', 'de animaciones'], A, W('construyendo'), top=1010, size=150, seed=94)
            + sello(260, 1400, 'Hecho en casa', A, W('animaciones', 1, 79), rot=-7, size=76, color='var(--verde)'))


def f_numeros(A, carta):
    """«El Log lleva más o menos unas 140 animaciones; desde que grabo el audio hasta la parte final tarda unos 45 minutos»."""
    n140 = N([(0, 0), (W('140'), 140, 1.0)])
    n45 = N([(0, 0), (W('45'), 45, .8)])
    if carta:
        return (recorte(60, 160, 450, 260, ar('El Log', 54) + f'<div class="ar" style="font-size:130px;color:var(--rojo)">~{n140}</div>'
                        + '<div class="cv" style="font-size:38px">animaciones</div>', A, W('log') - .1, rot=-3, seed=101, pad='20px 34px')
                + recorte(560, 165, 460, 250, ar('Audio → video', 50) + f'<div class="ar" style="font-size:130px;color:var(--azul)">{n45} min</div>',
                          A, W('45') - .4, rot=3, seed=102, pad='24px 34px'))
    return (fase(titular(['*El Log*', 'lleva…'], A, W('log') - .2, top=330, size=160, seed=101)
                 + K.numero(70, 720, f'~{n140}', A, W('140') - .1, size=440, color='var(--rojo)')
                 + mano(130, 1150, 'animaciones por video', A, W('animaciones', 1, 92), size=78)
                 + logo('anthropic', 740, 1300, 240, A, W('animaciones', 1, 92) + .3, rot=8, bg='#d97757', color='#ffffff'), A, sale=W('desde') - .1)
            + titular(['Del audio al', '*video final*'], A, W('desde'), top=330, size=150, seed=103)
            + K.numero(70, 760, f'{n45}<span style="font-size:.45em"> min</span>', A, W('45') - .1, size=400, color='var(--azul)')
            + ticket(110, 1200, 860, [('🎙️ grabo el audio', W('grabar', 1, 95), .5), ('🤖 Claude edita y anima', W('hasta', 1, 97), .6),
                                      ('🎬 video final', W('final', 1, 98), .4)], A, rot=-1.5, size=50))


def f_granja(A):
    """«Antes la grabación tardaba unos 9 minutos, pero ahora que lo divido entre las dos computadoras, unos 2 minutos y medio en promedio»."""
    fila = lambda y, et, w, col, val, t: (
        f'<div class="L" style="left:90px;top:{y}px;width:920px"><div class="ar rw" style="font-size:76px;--d:{A(t - .4)}">{et}</div>'
        f'<div style="display:flex;align-items:center;gap:24px;margin-top:18px"><div class="bar" style="height:96px;width:{w}px;background:{col};--d:{A(t)}"></div>'
        f'<div class="ar rw" style="font-size:110px;color:{col};--d:{A(t + .6)}">{val}</div></div></div>')
    return (titular(['Grabar las', '*animaciones*'], A, W('grabacion') - .3, top=330, size=150, seed=111)
            + fila(720, 'Antes · solo la Mac', 600, 'var(--tinta)', '9 min', W('9'))
            + fila(1060, 'Ahora · Mac + Legion', 170, 'var(--verde)', '2.5 min', W('2'))
            + sello(130, 1440, '3.5× más rápido', A, W('promedio') - .2, rot=-6, size=100, color='var(--verde)'))


def f_revisa(A, carta):
    """«Claude hace el trabajo pesado, pero yo tengo que estar revisando que el video completo esté bien, darle el visto bueno y que se ponga a renderizar»."""
    if carta:
        return (recorte(60, 190, 440, 190, ar('Claude 🤖', 70) + '<div class="cv" style="font-size:42px">el trabajo pesado</div>', A, W('cloud', 1, 126) - .2,
                        rot=-3, seed=121, pad='26px 32px')
                + recorte(540, 190, 470, 190, ar('Yo 👀', 70) + '<div class="cv" style="font-size:42px">reviso todo el video</div>', A, W('revisando'),
                          rot=3, seed=122, pad='26px 32px')
                + sellop(300, 420, 'Visto bueno ✓', A, W('visto'), rot=-5, size=64, color='var(--verde)'))
    return (titular(['El trabajo', '*pesado*'], A, W('y', 1, 124.4) + .1, top=330, size=160, seed=121)
            + recorte(80, 720, 440, 320, ar('Claude', 100) + '<div style="font-size:100px">🤖</div>', A, W('cloud', 1, 126), rot=-3, seed=122, pad='34px 40px')
            + recorte(560, 720, 440, 320, ar('Yo', 100) + '<div style="font-size:100px">👀</div>', A, W('yo', 1, 128), rot=3, seed=123, pad='34px 40px')
            + mano(560, 1070, 'reviso el video completo', A, W('revisando'), size=60, rot=-2)
            + sello(150, 1250, 'Visto bueno ✓', A, W('visto'), rot=-6, size=104, color='var(--verde)')
            + mano(280, 1520, '→ y ahora sí: render', A, W('renderizarlo', 1, 130) - .2, size=80, rot=-3))


# ═════════════════════════ propuesta B: tarjetas + dos escenas ═════════════════════════
S = 16.75; A = K.at(S)
tarjeta('b03-pregunta', S, 23.95, f_comentarios(A, True), props='B')
S = 24.05; A = K.at(S)
tarjeta('b04-mio', S, 31.45, f_mio(A, True), props='B')
S = 31.55; A = K.at(S)
escena('e1-voz', S, 51.95, [(f_voz(A), W('quita') - .1), (f_errores(A), W('despues', 1, 42) - .1), (f_guion(A), None)], 'B', fondo='cuad', seed=5,
       ac='var(--azul)')
S = 53.95; A = K.at(S)
tarjeta('b05-datos', S, 62.45, f_datos(A, True), props='B')
S = 62.5; A = K.at(S)
tarjeta('b06-web', S, 71.7, f_web(A, True), props='B')
S = 71.75; A = K.at(S)
tarjeta('b07-motor', S, 81.15, f_motor(A, True), props='B')
S = 89.5; A = K.at(S)
tarjeta('b09-numeros', S, 101.95, f_numeros(A, True), props='B')
S = 102.05; A = K.at(S)
tarjeta('b10-rapido', S, 104.5, cartel(60, 180, 560, 270, ['Para ir más', '*rápido*…'], A, W('para', 1, 102), size=88, rot=-2, seed=13), props='B')
S = 112.75; A = K.at(S)
escena('e2-granja', S, 124.45, [(f_granja(A), None)], 'B', fondo='papel', seed=7, ac='var(--verde)')
S = 124.5; A = K.at(S)
tarjeta('b11-revisa', S, 138.7, f_revisa(A, True), props='B')

# ═════════════════════════ propuesta A: como El Log ═════════════════════════
S = 16.75; A = K.at(S)
escena('a1-proceso', S, 51.95, [(f_comentarios(A, False), W('yo') - .1), (f_mio(A, False), W('primero') - .1), (f_voz(A), W('quita') - .1),
                                (f_errores(A), W('despues', 1, 42) - .1), (f_guion(A), None)], 'A', fondo='papel', seed=5)
S = 53.95; A = K.at(S)
escena('a2-motor', S, 81.2, [(f_datos(A, False), W('por', 1, 62) - .05), (f_web(A, False), W('al', 1, 71) - .1), (f_motor(A, False), None)],
       'A', fondo='cuad', seed=6, ac='var(--azul)')
S = 89.5; A = K.at(S)
escena('a3-numeros', S, 105.9, [(f_numeros(A, False), W('para', 1, 102) - .1),
                                (titular(['Para ir más', '*rápido*:'], A, W('para', 1, 102), top=330, size=160, seed=13)
                                 + K.numero(70, 720, '2', A, W('dos', 1, 104), size=560, color='var(--rojo)')
                                 + mano(420, 960, 'computadoras', A, W('computadoras', 1, 104), size=100, rot=-4), None)],
       'A', fondo='papel', seed=8)
S = 112.75; A = K.at(S)
escena('a4-granja', S, 138.7, [(f_granja(A), W('y', 1, 124.4) - .05), (f_revisa(A, False), None)], 'A', fondo='papel', seed=7, ac='var(--verde)')

PIEZAS.sort(key=lambda p: p[1])

if __name__ == '__main__':
    solo = set(sys.argv[1:])
    mias = [p for p in PIEZAS if PROP in p[4]]
    trabajos = []
    for pid, a, b, html, _, _ in mias:
        if solo and pid not in solo:
            continue
        path = f'{WORK}/{pid}.html'
        open(path, 'w').write(html)
        print('html', pid, f'{a:7.2f}–{b:7.2f}')
        trabajos.append(dict(html=path, dur=round(b - a, 2), out=f'{OUT}/{PRE}{pid}.webm'))
    json.dump(trabajos, open(f'{OUT}/lote-{PROP}.json', 'w'), indent=1)
    if not solo:
        rel = os.environ.get('REL', 'devlog/1/animaciones')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'html': f'{rel}/_html/{pid}.html', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0,
                'scale': 1, 'position': 'center'} for pid, a, b, _, _, _ in mias]
        json.dump(ovs, open(f'{OUT}/overlays-{PROP}.json', 'w'), indent=2, ensure_ascii=False)
        json.dump([[a, b] for _, a, b, _, _, full in mias if full], open(f'{OUT}/escenas-{PROP}.json', 'w'))
        print(f'overlays-{PROP}.json · escenas-{PROP}.json')
