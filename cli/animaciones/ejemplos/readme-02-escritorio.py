"""El Readme #02 · RAG — edición «Escritorio» (idea nueva): el RAG es literalmente una búsqueda en tu computadora, contado en LogOS,
un sistema operativo retro inventado (System 7 / Windows 98). La carpeta docs/ se parte en pedazos con barra de progreso, la ventana
de Búsqueda encuentra los que más se parecen (por significado), el cursor los arrastra al chat de la IA y ésta contesta solo con eso.
Diálogos de advertencia que se sacuden para los tres cuidados, «memoria insuficiente» para el contexto largo y ⌘S para cerrar.
Capas: mesa (escritorio con íconos, opaca, todo el video) → una pieza transparente por sección (sus ventanas se abren y cierran con
los rectángulos de zoom) → barra de menú arriba con la sección actual. Nada se desvanece: todo va a pasos.
Tiempos = readme/2/voz/voz-norm.wav (132.34 s), los mismos de readme-02.py.
Uso: SALIDA=~/Documents/Videos/readme/2/escritorio REL=readme/2/escritorio python3 ejemplos/readme-02-escritorio.py [ids…]   (SOLO_HTML=1 para revisar)
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import escritorio as E
from escritorio import ventana, teclea, grande, dialogo, progreso, N, icono, cursor, ap, sprite

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.path.expanduser('~/Documents/Videos/readme/2/escritorio')))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
FIN = 132.34
PIEZAS = []
X, W = 40, 1000            # ventanas a lo ancho
AZ, RJ, VD = '#0a1f8f', '#d8262a', '#14a046'

# sprites extra (solo en memoria; la librería no se toca)
E.SPR['papelera'] = ["   kkkkkkkkkk   ", "  kggggggggggk  ", " kkkkkkkkkkkkkk ", "  kgsgsgsgsgsk  ", "  kgsgsgsgsgsk  ", "  kgsgsgsgsgsk  ",
                     "  kgsgsgsgsgsk  ", "  kgsgsgsgsgsk  ", "  kgsgsgsgsgsk  ", "  kgsgsgsgsgsk  ", "  kgsgsgsgsgsk  ", "  kgsgsgsgsgsk  ",
                     "   kkkkkkkkkk   ", "                ", "                ", "                "]
E.SPR['pedazo'] = ["  kkkkkkk       ", "  kwwwwwwkk     ", "  kwkkkwwwk     ", "  kwwwwwwwk     ", "  kwkkkkkwk  k  ", "  kwwwwwwwk k k ",
                   "  kwkkkkwwk  k  ", "  kwwwwwwwk k k ", "  kkkkkkkkk  k  ", "                ", "                ", "                ",
                   "                ", "                ", "                ", "                "]
E.SPR['libro'] = ["  kkkkkkkkkkkk  ", " krrrrrrrrrrrrk ", " krwwwwwwwwwwrk ", " krwkkkkkkkkwrk ", " krwwwwwwwwwwrk ", " krwkkkkkkwwwrk ",
                  " krwwwwwwwwwwrk ", " krrrrrrrrrrrrk ", " krrrrrrrrrrrrk ", " krrrrrrrrrrrrk ", " krrrrrrrrrrrrk ", " krrrrrrrrrrrrk ",
                  " kwwwwwwwwwwwwk ", " kkkkkkkkkkkkkk ", "                ", "                "]

# íconos de la mesa (abajo) — de aquí salen las ventanas con el zoom
IC = {'readme': (155, 1755), 'docs': (385, 1755), 'serv': (615, 1755), 'pap': (845, 1755)}


def mini(spr, label, color='#0a0a0a', size=64, w=150):
    """Ícono pequeño dentro de una ventana (en línea)."""
    return (f'<div style="display:inline-block;width:{w}px;text-align:center;vertical-align:top;font-size:24px;font-weight:600;color:{color}">'
            f'{sprite(spr, size, "margin:0 auto 6px")}<span>{label}</span></div>')


def apila(items, A, h, extra=''):
    """Contenidos que se reemplazan en el mismo lugar: [(html, entra, sale|None)]."""
    return (f'<div style="position:relative;height:{h}px;{extra}">'
            + ''.join(ap(html, A, a, sale=b, extra='position:absolute;left:0;top:0;right:0') for html, a, b in items) + '</div>')


def titulo(lineas_items, A, t, sale, h=250, size=100, nombre='notas.txt', y=110, desde=None):
    """Bloc de notas arriba con el titular grande (se reemplaza a pasos)."""
    cu = apila([(grande(ln, A, a, size=size), a, b) for ln, a, b in lineas_items], A, h)
    return ventana(X, y, W, f'Bloc de notas — {nombre}', cu, A, t, sale=sale, desde=desde or IC['readme'])


def term(x, y, w, lineas, A, t, sale, titulo_='Terminal', size=44, desde=None, h=None):
    """Terminal: lineas = [(texto, t, dur_tecleo)]."""
    cu = ''.join(f'<div>{teclea(tx, A, a, dt)}</div>' for tx, a, dt in lineas) + f'<span class="car"></span>'
    return ventana(x, y, w, titulo_, f'<div style="font-size:{size}px">{cu}</div>', A, t, sale=sale, cu='negro', icono='compu', desde=desde, h=h)


def sac(html, A, t, z=45):
    """Envuelve una ventana para que se sacuda al aparecer (diálogo de error)."""
    return f'<div style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:{z};pointer-events:none;animation:sac .4s steps(6) {A(t)} both">{html}</div>'


def ps(txt, size=38, extra=''):
    return f'<div class="ps" style="font-size:{size}px;line-height:1.25;font-weight:600;{extra}">{txt}</div>'


def fila(spr, nombre, desc, pct, A, t, sel=None, color='#0a0a0a'):
    """Renglón de resultados de búsqueda; sel = cuándo se selecciona en azul."""
    s = f'class="sl" style="--s:{A(sel)}"' if sel is not None else ''
    return ap(f'<div {s}><div style="display:flex;align-items:center;gap:18px;padding:8px 10px">{sprite(spr, 44)}'
              f'<span class="vt" style="font-size:42px;width:250px">{nombre}</span><span class="ps" style="flex:1;font-size:30px;font-weight:600">{desc}</span>'
              f'<span class="vt" style="font-size:46px;color:inherit">{pct}</span></div></div>', A, t)


def seccion(pid, start, end, body, css=''):
    end = end + E.COLA if end < FIN else end
    PIEZAS.append((pid, start, end, E.page(css, body, round(end - start, 2), S0=start, transparente=True)))


# ───────────────────────── mesa: escritorio LogOS (todo el video, opaca)
A = E.at(0)
MESA = (f'<div style="position:absolute;left:0;right:0;top:760px;text-align:center;font-weight:700;font-size:150px;color:rgba(255,255,255,.07);letter-spacing:.05em">LogOS</div>'
        f'<div class="vt" style="position:absolute;left:0;right:0;top:930px;text-align:center;font-size:46px;color:rgba(255,255,255,.12)">README.md · #02 · RAG</div>'
        + icono(60, 1700, 'archivo', 'README.md', A, 0) + icono(290, 1700, 'carpeta', 'docs/', A, 0) + icono(520, 1700, 'servidor', 'homelab', A, 0)
        + icono(750, 1700, 'papelera', 'Papelera', A, 0))
MESA_CSS = '.mesa{background-image:radial-gradient(rgba(0,0,0,.18) 1.2px,transparent 1.4px),linear-gradient(rgba(255,255,255,.035) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.035) 2px,transparent 2px);background-size:6px 6px,96px 96px,96px 96px}'
PIEZAS.append(('mesa', 0.0, FIN, E.page(MESA_CSS, MESA, FIN, S0=0.0, mesa='morado', menu=False)))

# ───────────────────────── 0:00 · gancho: tu IA contesta sin conocer tus datos → se lo inventa → 3 pasos
S = 0.0; A = E.at(S); NX = 4.6
_ia = 'IA › probablemente… <span style="color:#d8262a">(no lo leyó)</span>'
CHAT0 = (f'<div style="font-size:40px">{teclea("Tú › ¿qué dice mi contrato?", A, .3, .5)}</div>'
         f'<div style="font-size:40px;margin-top:14px">{teclea(_ia, A, 1.15, .6)}</div>')
b = (titulo([(['Tu IA contesta', '_sin tus datos_'], .15, None)], A, .1, NX, h=230, size=100, nombre='gancho.txt')
     + ventana(X, 470, W, 'Chat con la IA', f'<div class="vt" style="font-size:44px">{CHAT0}</div>', A, .25, sale=NX, icono='robot', cu='negro', desde=IC['readme'])
     + ventana(X, 760, 560, 'Mis archivos', mini('carpeta', '¿tus docs?') + mini('archivo', '¿tus notas?') + mini('archivo', '¿contrato.pdf?'), A, 1.2, sale=NX, icono='carpeta', desde=IC['docs'])
     + ap(f'<div style="position:absolute;left:610px;top:800px;width:420px" class="ps"><span style="font-size:40px;font-weight:700;color:#fff;text-shadow:3px 3px 0 #000">no los abrió ↙</span></div>', A, 1.5, sale=NX)
     + sac(dialogo(90, 1080, 900, 'error', 'Respuesta <b>inventada</b>: la IA no conoce tus datos.', A, 1.9, botones=('Aceptar',), pulsa=2.45, sale=2.6, titulo='Error'), A, 1.9)
     + ventana(140, 1100, 800, 'arreglo.txt', grande(['Arreglo:', '_3 pasos_'], A, 2.65, size=110), A, 2.6, sale=NX, icono='info', desde=(540, 1350))
     + cursor([(1.5, 900, 1560), (2.3, 540, 1315), (2.45, 540, 1315, True), (3.4, 760, 1520)]))
seccion('s0-gancho', S, NX, b)

# ───────────────────────── 0:04 · RAG: que conteste con tus datos | en vez de todo, busca solo lo que sirve
S = 4.6; A = E.at(S); NX = 21.85; F1 = 10.9
SELD = {'baja.md': 19.95, 'ajustes.md': 20.07, 'plan.md': 20.19}
DOCS = ''.join(ap(mini('archivo', f'<span class="sl" style="--s:{A(SELD[n])};padding:0 4px">{n}</span>' if n in SELD else n, size=56, w=148), A, 11.3 + i * .07,
                  extra='display:inline-block') for i, n in enumerate(
    ['contrato.pdf', 'plan.md', 'notas.md', 'factura.pdf', 'faq.md', 'precios.md', 'ayuda.md', 'baja.md', 'ajustes.md', 'correo.txt', 'logo.png', 'equipo.md']))
DOCS_SEL = ''
f1 = (ventana(X, 110, W, 'Diccionario — RAG', grande(['RAG'], A, 4.8, size=250)
              + f'<div class="ps" style="font-size:44px;font-weight:700;margin-top:10px">{teclea("<u>R</u>etrieval-<u>A</u>ugmented <u>G</u>eneration", A, 5.0, .7)}</div>',
              A, 4.65, sale=F1, icono='info', desde=IC['readme'])
      + term(X, 610, W, [('RAG = buscar → contestar', 5.9, .6)], A, 5.85, sale=F1, size=54)
      + ventana(X, 870, W, 'Bloc de notas — idea.txt', grande(['Contesta con', '_tus datos_'], A, 8.86, size=110), A, 8.8, sale=F1, desde=IC['readme'])
      + dialogo(150, 1240, 780, 'info', 'Y <b>no se lo imagina</b>.', A, 10.5, sale=F1, titulo='LogOS', desde=(540, 1340)))
f2 = (titulo([(['En vez de', 'pasarle *todo*…'], 11.1, 14.25), (['_Busca_ primero'], 14.3, 19.85), (['Solo lo que', '*sirve*'], 19.9, None)], A, 11.05, NX,
             h=230, size=100, nombre='idea.txt')
      + ventana(X, 470, W, 'docs/ — 412 archivos', f'<div style="position:relative">{DOCS}{DOCS_SEL}</div>', A, 11.2, sale=NX, icono='carpeta', desde=IC['docs'])
      + sac(dialogo(110, 900, 860, 'alerta', '¿Pasarle <b>todos</b> los documentos? Son 412.', A, 12.9, botones=('No', 'Sí'), pulsa=14.0, sale=14.15, titulo='Advertencia'), A, 12.9)
      + ventana(X, 900, W, 'Buscar', f'<div style="display:flex;gap:20px;align-items:center">{sprite("lupa", 80)}<div class="pg" style="flex:1;height:auto;padding:10px 16px">'
                f'<span class="vt" style="font-size:48px">{teclea("tu pregunta…", A, 14.6, .5)}</span></div></div>'
                + apila([(f'<div class="vt" style="font-size:42px;margin-bottom:10px">buscando en 412 archivos…</div>' + progreso([(0, 0), (15.0, 100, 4.4)]), 14.9, 19.85),
                         (f'<div class="ps" style="font-size:40px;font-weight:700">contexto: <span style="color:#0a1f8f">3 pedazos</span> · nada más ✓</div>', 19.9, None)], A, 130,
                        extra='margin-top:22px'),
                A, 14.3, sale=NX, icono='lupa', cu='gris', desde=IC['docs'])
      + cursor([(14.0, 640, 1700), (14.45, 500, 1060, True), (19.6, 520, 1180), (19.95, 330, 760, True), (21.0, 900, 1500)]))
seccion('s1-rag', S, NX, f1 + f2)

# ───────────────────────── 0:21 · 3 pasos: prepara (pedazos con significado) → busca (los que más se parecen) → contesta solo con eso
S = 21.85; A = E.at(S); NX = 47.0; F1, F2 = 34.2, 39.25
PZ = ''.join(ap(mini('pedazo', f'pedazo_{n}', size=72, w=200), A, 26.47 + i * .12, extra='display:inline-block') for i, n in enumerate(['014', '015', '016', '017']))
f1 = (titulo([(['Paso 1 · *prepara*'], 21.95, None)], A, 21.9, F1, h=110, size=100, nombre='pasos.txt')
      + ventana(X, 330, W, 'Partir en pedazos', f'<div style="display:flex;gap:26px;align-items:center">{sprite("archivo", 110)}'
                f'<div style="flex:1"><div class="vt" style="font-size:44px;margin-bottom:10px">docs/contrato.md → pedazos</div>{progreso([(0, 0), (22.4, 100, 4.0)])}</div></div>'
                f'<div style="margin-top:24px;min-height:150px">{PZ}</div>'
                + apila([(ps('✂ pedazos pequeños'), 26.6, 29.1), (ps(f'✓ cada uno conserva su <span class="sl" style="--s:{A(29.3)}">significado</span>'), 29.14, None)], A, 60),
                A, 22.2, sale=F1, icono='archivo', cu='gris', desde=IC['docs'])
      + term(X, 990, W, [('$ rag index ./docs → pedazos', 22.0, .6), ('buscar «cancelar plan»', 29.95, .5), ('     ≈ «dar de baja»', 30.6, .5)], A, 21.95, sale=F1)
      + dialogo(X, 1310, 470, 'info', 'Busca <b>por idea</b> ✓', A, 31.42, sale=F1, titulo='Búsqueda', desde=(275, 1400))
      + sac(dialogo(530, 1340, 510, 'error', '<b>Palabra exacta</b> ✕', A, 32.94, sale=F1, titulo='Búsqueda', z=46), A, 32.94, z=46))
RES = (fila('pedazo', 'pedazo_014', 'dar de baja', '92%', A, 34.7, sel=37.0) + fila('pedazo', 'pedazo_017', 'cancelar suscripción', '88%', A, 34.77, sel=37.15)
       + fila('pedazo', 'pedazo_031', 'ajustes › plan', '81%', A, 34.84, sel=37.3) + fila('pedazo', 'pedazo_010', 'precios 2024', '40%', A, 34.91)
       + fila('pedazo', 'pedazo_022', 'logo y colores', '12%', A, 34.98) + fila('pedazo', 'pedazo_026', 'contacto', '9%', A, 35.05))
f2 = (titulo([(['Paso 2 · *busca*'], 34.3, None)], A, 34.26, F2, h=110, size=100, nombre='pasos.txt', desde=(540, 200))
      + ventana(X, 330, W, 'Buscar', f'<div style="display:flex;gap:20px;align-items:center;margin-bottom:18px">{sprite("lupa", 70)}<div class="pg" style="flex:1;height:auto;padding:10px 16px">'
                f'<span class="vt" style="font-size:46px">{teclea("¿cómo cancelo mi plan?", A, 34.5, .6)}</span></div></div>'
                f'<div style="background:#fff;padding:6px;box-shadow:inset 3px 3px 0 #828282">{RES}</div>'
                + apila([(ps(f'3 seleccionados · los que más se <span class="sl" style="--s:{A(38.5)}">parecen</span>'), 38.31, None)], A, 60, extra='margin-top:16px'),
                A, 34.3, sale=F2, icono='lupa', cu='gris', desde=IC['docs'])
      + term(X, 1180, W, [('$ rag search "pregunta" → top 3', 34.4, .6)], A, 34.35, sale=F2)
      + cursor([(35.6, 900, 1500), (36.9, 300, 600, True), (37.3, 300, 760, True), (39.2, 300, 760), (39.22, -300, 760)]))
ADJ = ''.join(ap(mini('pedazo', n, size=56, w=140), A, 42.43 + i * .1, extra='display:inline-block') for i, n in enumerate(['014', '017', '031']))
GHOST = ("<div class=\"cur\" data-c='" + json.dumps([[41.3, 120, 470, False], [42.35, 640, 700, False], [42.37, -900, 700, False]]) + "'>"
         "<div style=\"width:360px;height:200px;border:4px dotted #0a0a0a;outline:2px dotted #fff;margin:-30px 0 0 -30px\"></div><i class=\"ck\"></i></div>")
f3 = (titulo([(['Paso 3 · *contesta*'], 39.3, None)], A, 39.28, NX, h=110, size=100, nombre='pasos.txt', desde=(540, 200))
      + ventana(X, 330, 470, 'Resultados', ''.join(ap(f'<div style="background:#0a1f8f;color:#fff;display:flex;gap:12px;align-items:center;padding:6px 10px;margin-bottom:6px">'
                                                      f'{sprite("pedazo", 40)}<span class="vt" style="font-size:40px">pedazo_{n}</span></div>', A, 39.4 + i * .08)
                                                   for i, n in enumerate(['014', '017', '031'])), A, 39.35, sale=NX, icono='lupa', desde=(275, 450))
      + ventana(530, 330, 510, 'Chat con la IA', f'<div class="vt" style="font-size:40px">{teclea("Tú › ¿cómo cancelo", A, 39.5, .4)}<br>{teclea("     mi plan?", A, 39.9, .3)}</div>'
                f'<div style="min-height:110px;margin-top:10px">{ADJ}</div>'
                + apila([(f'<div class="ps" style="font-size:34px;line-height:1.25;font-weight:600;background:#e8e8ff;padding:12px 16px">IA › Ve a <b>Ajustes › Plan</b> y toca <i>Dar de baja</i>.</div>', 44.2, None)], A, 170),
                A, 39.45, sale=NX, icono='robot', desde=(785, 450))
      + term(X, 1030, W, [('ia(pregunta, pedazos)', 39.4, .5), ('› contesta usando solo eso ✓', 43.65, .7)], A, 39.38, sale=NX)
      + dialogo(150, 1320, 780, 'info', 'Contestó <b>solo con eso</b>: pregunta + pedazos.', A, 45.76, sale=NX, titulo='LogOS', desde=(540, 1420))
      + GHOST + cursor([(40.5, 900, 1500), (41.3, 150, 500, True), (42.35, 670, 730), (42.43, 670, 730, True), (43.5, 900, 1560)]))
seccion('s2-pasos', S, NX, f1 + f2 + f3)

# ───────────────────────── 0:47 · libro entero vs la página que ocupa
S = 47.0; A = E.at(S); NX = 60.3; F1 = 54.85
PAGS = ''.join(f'<i style="display:inline-block;width:92px;height:122px;margin:7px;background:#fff;box-shadow:inset 0 0 0 3px #0a0a0a,4px 4px 0 #828282;'
               f'background-image:repeating-linear-gradient(#fff 0 16px,#bbb 16px 20px);background-size:70% 100%;background-position:center;background-repeat:no-repeat"></i>' for _ in range(24))
LIBRO = (f'<div style="display:flex;gap:18px"><div style="flex:1;height:440px;overflow:hidden;position:relative">'
         f'<div style="animation:scrl 6s steps(30) {A(48.8)} both">{PAGS}{PAGS}</div></div>'
         f'<div style="width:40px;background:#dcdcdc;box-shadow:inset 3px 3px 0 #828282;position:relative"><i style="position:absolute;left:4px;right:4px;height:70px;background:#c3c3c3;'
         f'box-shadow:inset -3px -3px 0 #0a0a0a,inset 3px 3px 0 #fff;animation:thumb 6s steps(30) {A(48.8)} both"></i></div></div>'
         f'<div class="vt" style="font-size:44px;margin-top:14px">página {N([(0, 1), (48.8, 412, 4.5)])} de 412</div>')
PAG = (f'<div class="vt" style="font-size:36px;color:#828282">pág. 217</div>'
       + ''.join(f'<div style="height:16px;width:{w}%;background:#ccc;margin-top:18px"></div>' for w in (92, 80, 88))
       + f'<div class="ps" style="font-size:44px;font-weight:700;margin-top:24px"><span class="sl" style="--s:{A(56.69)}">Cancela en Ajustes › Plan</span></div>'
       + ''.join(f'<div style="height:16px;width:{w}%;background:#ccc;margin-top:18px"></div>' for w in (86, 74, 90, 60)))
f1 = (titulo([(['¿Le das *todo*', 'el contexto?'], 47.1, None)], A, 47.05, F1, h=230, size=100, nombre='contexto.txt')
      + ventana(X, 470, W, 'libro.pdf — 412 páginas', LIBRO, A, 47.3, sale=F1, icono='libro', cu='gris', desde=IC['docs'])
      + sac(dialogo(110, 1190, 860, 'alerta', 'Eso es darle un <b>libro entero</b>.', A, 50.81, sale=F1, titulo='Advertencia'), A, 50.81)
      + ventana(110, 1430, 860, 'Buscar', f'<div style="display:flex;gap:18px;align-items:center">{sprite("lupa", 60)}'
                f'<span class="vt" style="font-size:44px">{teclea("…y que encuentre la página", A, 52.4, .8)}</span></div>', A, 52.2, sale=F1, icono='lupa', cu='gris', desde=(540, 1500)))
f2 = (titulo([(['Con RAG:', 'solo *esa página*'], 54.9, None)], A, 54.88, NX, h=230, size=100, nombre='contexto.txt', desde=(540, 200))
      + ventana(X, 470, W, 'pagina_217.txt', PAG, A, 55.1, sale=NX, icono='archivo', desde=(540, 600))
      + ventana(X, 1150, W, 'Chat con la IA', f'<div class="vt" style="font-size:46px">{teclea("Tú › ¿cómo cancelo mi plan?", A, 59.4, .6)}</div>', A, 59.36, sale=NX, icono='robot', cu='negro',
                desde=(540, 1250)))
seccion('s3-libro', S, NX, f1 + f2,
        css='@keyframes scrl{to{transform:translateY(-620px)}}@keyframes thumb{from{top:4px}to{top:360px}}')

# ───────────────────────── 1:00 · mi ejemplo: el homelab recaba redes y proyectos → Claude contesta solo con eso (medio RAG)
S = 60.3; A = E.at(S); NX = 77.3; F1 = 68.0
f1 = (titulo([(['Mi *homelab*'], 60.4, None)], A, 60.35, F1, h=110, size=110, nombre='ejemplo.txt')
      + ventana(X, 330, W, 'Servidor — homelab', f'<div style="display:flex;gap:30px;align-items:center">{sprite("servidor", 230)}<div style="flex:1">'
                f'<div class="ps" style="font-size:34px;font-weight:700">Registros recabados</div>'
                f'<div class="vt" style="font-size:150px;line-height:.9;color:#0a1f8f">{N([(0, 0), (64.6, 1284, 3.0)], f="c")}</div>'
                f'{progreso([(0, 0), (64.6, 100, 3.0)], color="#14a046")}</div></div>', A, 60.8, sale=F1, icono='servidor', cu='gris', desde=IC['serv'])
      + dialogo(X, 760, 520, 'info', 'Esto es <b>medio RAG</b>.', A, 63.79, sale=F1, titulo='LogOS', desde=(300, 860))
      + ventana(X, 1080, 480, 'redes/', mini('archivo', 'tiktok.csv', w=128) + mini('archivo', 'ig.csv', w=128) + mini('archivo', 'yt.csv', w=128), A, 66.77, sale=F1, icono='carpeta',
                desde=(280, 1180))
      + ventana(560, 1080, 480, 'proyectos/', mini('carpeta', 'gastos', w=128) + mini('carpeta', 'videos', w=128) + mini('carpeta', 'hub', w=128), A, 67.51, sale=F1, icono='carpeta',
                desde=(800, 1180)))
f2 = (titulo([(['Claude contesta', 'solo con *eso*'], 68.1, None)], A, 68.05, NX, h=230, size=100, nombre='ejemplo.txt', desde=(540, 200))
      + ventana(X, 470, W, 'Claude', f'<div class="vt" style="font-size:46px">{teclea("Tú › ¿cómo van mis redes?", A, 68.1, .6)}</div>'
                + apila([(f'<div class="ps" style="font-size:38px;font-weight:600;background:#fde9e1;padding:14px 18px;margin-top:14px">Claude › Con lo que se guardó en el homelab, '
                          f'<b>y nada más</b>: TikTok subió 12 % esta semana.</div>', 70.6, None)], A, 180),
                A, 68.05, sale=NX, icono='robot', desde=IC['serv'])
      + term(X, 920, W, [('contexto = datos guardados', 70.45, .6), ('          · nada más', 71.1, .4)], A, 70.4, sale=NX)
      + sac(dialogo(110, 1200, 860, 'info', '<b>Solo esos datos</b> ✓', A, 72.46, sale=NX, titulo='LogOS'), A, 72.46))
seccion('s4-ejemplo', S, NX, f1 + f2)

# ───────────────────────── 1:17 · > ⚠ Ojo: mal cortado · desactualizado · búsqueda equivocada → revisa qué encontró
S = 77.3; A = E.at(S); NX = 99.4
C1, C2, C3, C4 = 79.5, 83.94, 90.72, 96.4
CAB = ventana(X, 110, W, 'Bloc de notas — ojo.txt', f'<div style="display:flex;align-items:center;gap:26px">{sprite("alerta", 110)}'
              f'{grande(["&gt; Ojo"], A, 77.4, size=110)}<span class="ps" style="font-size:40px;font-weight:700;color:#d8262a;margin-left:auto">{teclea("tres cuidados", A, 77.9, .4)}</span></div>',
              A, 77.35, sale=NX, desde=IC['readme'])


def adv(n, txt, t, sale):
    return sac(dialogo(X, 330, W, 'alerta', f'<div style="font-size:30px;color:#828282">Advertencia {n} de 3</div>'
                       f'<div style="font-family:Jersey 15;font-weight:700;font-size:82px;line-height:1">{txt}</div>', A, t, sale=sale, titulo=f'⚠ {n}/3', z=30), A, t, z=30)


c1 = (adv(1, 'Pedazos mal<br>cortados', C1, C2)
      + ventana(X, 780, 480, 'pedazo_A.txt', f'<div class="ps" style="font-size:44px;font-weight:600">«El plan cuesta…</div>', A, 80.52, sale=C2, icono='pedazo', desde=(280, 880))
      + ventana(560, 820, 480, 'pedazo_B.txt', f'<div class="ps" style="font-size:44px;font-weight:600;color:#828282">…$99 al mes»</div>', A, 80.7, sale=C2, icono='pedazo', desde=(800, 920))
      + sac(dialogo(110, 1120, 860, 'error', '✂ Cortado <b>a medias</b>: le falta la mitad.', A, 83.51, sale=C2, titulo='Error'), A, 83.51))
c2 = (adv(2, 'Datos<br>desactualizados', C2, C3)
      + ventana(X, 780, 440, 'precios_2024.txt', f'<div class="vt" style="font-size:90px;text-align:center">$79</div>', A, 85.13, sale=C3, icono='archivo', desde=(260, 880))
      + ap('<div style="position:absolute;left:500px;top:820px;font-family:Jersey 15;font-weight:700;font-size:150px;color:#fff;text-shadow:5px 5px 0 #000">≠</div>', A, 85.4, sale=C3)
      + ventana(600, 780, 440, 'hoy.txt', f'<div class="vt" style="font-size:90px;text-align:center;color:#14a046">$99</div>', A, 85.6, sale=C3, icono='archivo', desde=(820, 880))
      + sac(dialogo(110, 1120, 860, 'error', 'Ya <b>no es cierto</b>: la IA te contesta con el precio viejo.', A, 89.62, sale=C3, titulo='Error'), A, 89.62))
c3 = (adv(3, 'Búsqueda<br>equivocada', C3, C4)
      + ventana(X, 780, W, 'Buscar', f'<div style="display:flex;gap:18px;align-items:center;margin-bottom:14px">{sprite("lupa", 60)}<span class="vt" style="font-size:46px">{teclea("«baja»", A, 91.0, .3)}</span></div>'
                + ap(f'<div class="ps" style="font-size:40px;font-weight:600;background:#fff;padding:12px 16px">→ trae <span style="position:relative">«bajar precio»'
                     f'<i style="position:absolute;left:-6px;right:-6px;top:48%;height:8px;background:#d8262a;transform-origin:left;animation:tch .3s steps(4) {A(92.34)} both"></i></span></div>', A, 91.5),
                A, 90.9, sale=C4, icono='lupa', cu='gris', desde=(540, 880))
      + sac(dialogo(110, 1150, 860, 'error', 'Trae <b>lo que no es</b>.', A, 92.34, sale=C4, titulo='Error'), A, 92.34))
c4 = (ventana(X, 330, W, 'Bloc de notas — revisa.txt', grande(['_Revisa_ qué', 'encontró'], A, 96.45, size=110), A, 96.4, desde=(540, 430), sale=NX)
      + term(X, 720, W, [('$ rag search --show-sources', 96.5, .7), ('✓ pedazo_017 · pedazo_031', 97.61, .6)], A, 96.45, sale=NX)
      + dialogo(150, 1050, 780, 'info', 'Revisa las <b>fuentes</b> antes de creerle ✓', A, 97.61, sale=NX, titulo='LogOS', desde=(540, 1150)))
seccion('s5-ojo', S, NX, CAB + c1 + c2 + c3 + c4, css='@keyframes tch{from{transform:scaleX(0)}to{transform:scaleX(1)}}')

# ───────────────────────── 1:39 · ¿y el contexto largo? pocos docs: pásalos todos · miles: tokens, tiempo, se pierde a la mitad
S = 99.4; A = E.at(S); NX = 115.5; F1 = 108.2
f1 = (titulo([(['«Ya aguantan', 'mucho *contexto*»'], 99.6, 104.9), (['¿Pocos docs?'], 104.96, None)], A, 99.55, F1, h=230, size=100, nombre='contexto.txt')
      + dialogo(X, 470, W, 'info', 'Es cierto: los modelos de hoy aguantan <b>muchísimo</b> contexto ✓', A, 102.0, sale=F1, titulo='LogOS', desde=(540, 570))
      + ventana(X, 830, W, 'docs/ — 4 archivos', ''.join(ap(mini('archivo', f'{i + 1}.md', size=90, w=220), A, 105.1 + i * .1, extra='display:inline-block') for i in range(4)),
                A, 105.0, sale=F1, icono='carpeta', desde=IC['docs'])
      + dialogo(150, 1180, 780, 'info', '<b>Pásale todos</b> ✓', A, 107.34, sale=F1, titulo='LogOS', desde=(540, 1280)))
MEM = (f'<div style="display:flex;gap:24px;align-items:flex-start">{sprite("error", 110)}<div style="flex:1">'
       f'<div style="font-family:Jersey 15;font-weight:700;font-size:64px;line-height:1">Memoria insuficiente</div>'
       f'<div class="vt" style="font-size:66px;color:#0a1f8f;margin-top:10px">{N([(0, 5), (108.3, 3000, 1.2)], f="c")} documentos</div></div></div>'
       f'<div class="vt" style="font-size:42px;margin:18px 0 8px">tokens del límite: {N([(0, 4), (109.7, 96, 1.4)], suf=" %")}</div>'
       + progreso([(0, 4), (109.7, 96, 1.4)], color='#d8262a'))
f2 = (titulo([(['¿Y con', '*miles*?'], 108.3, None)], A, 108.26, NX, h=230, size=100, nombre='contexto.txt', desde=(540, 200))
      + sac(ventana(X, 470, W, 'Error', MEM, A, 108.3, sale=NX, cu='gris', z=30, t1='#7a1414', t2='#d8262a'), A, 108.3, z=30)
      + ventana(X, 960, 470, 'Costo', f'<div class="vt" style="font-size:64px;color:#d8262a">+ tokens</div>', A, 110.87, sale=NX, icono='chip', cu='gris', desde=(275, 1060))
      + ventana(570, 960, 470, 'Espera', f'<div style="display:flex;gap:16px;align-items:center">{sprite("reloj", 70)}<span class="vt" style="font-size:64px;color:#d8262a">+ tiempo</span></div>',
                A, 112.29, sale=NX, icono='reloj', cu='gris', desde=(805, 1060))
      + sac(dialogo(110, 1250, 860, 'alerta', 'Y con tanto, <b>se pierde a la mitad</b>.', A, 114.23, sale=NX, titulo='Advertencia'), A, 114.23))
seccion('s6-contexto', S, NX, f1 + f2)

# ───────────────────────── 1:55 · funciona hoy → si tus datos ya no caben, ponlo a buscar antes de contestar
S = 115.5; A = E.at(S); NX = 124.7; F1 = 119.75
f1 = (titulo([(['Funciona *hoy* ✓'], 115.6, None)], A, 115.55, F1, h=110, size=110, nombre='hoy.txt')
      + dialogo(X, 330, W, 'info', 'Con los modelos que tenemos <b>en 2026</b>.', A, 116.3, sale=F1, titulo='Acerca de', desde=(540, 430))
      + ventana(X, 640, W, 'Estado', f'<div style="display:flex;gap:20px;align-items:center">{sprite("compu", 90)}<span class="vt" style="font-size:66px;color:#14a046">'
                f'{teclea("RAG: funciona ✓", A, 117.92, .5)}</span></div>', A, 117.9, sale=F1, icono='compu', cu='gris', desde=(540, 740)))
f2 = (titulo([(['¿Ya no _caben_?'], 119.9, None)], A, 119.82, NX, h=110, size=110, nombre='hoy.txt', desde=(540, 200))
      + term(X, 330, W, [('si datos > chat →', 119.9, .5), ('  1. busca · 2. contesta', 122.0, .6)], A, 119.85, sale=NX)
      + sac(dialogo(X, 640, W, 'error', 'Tus datos <b>no caben</b> en la conversación.', A, 121.25, sale=NX, titulo='Error'), A, 121.25)
      + ventana(X, 1000, 470, 'Buscar', f'<div style="text-align:center">{sprite("lupa", 120, "margin:0 auto")}<div class="ps" style="font-size:36px;font-weight:700">1 · busca primero</div></div>',
                A, 122.93, sale=NX, icono='lupa', cu='gris', desde=(275, 1100))
      + ventana(570, 1000, 470, 'Chat con la IA', f'<div style="text-align:center">{sprite("robot", 120, "margin:0 auto")}<div class="ps" style="font-size:36px;font-weight:700">2 · luego contesta</div></div>',
                A, 123.72, sale=NX, icono='robot', cu='gris', desde=(805, 1100))
      + cursor([(122.5, 900, 1560), (122.93, 300, 1180, True), (123.72, 800, 1180, True)]))
seccion('s7-hoy', S, NX, f1 + f2)

# ───────────────────────── 2:04 · resumen para guardar + pregunta
S = 124.7; A = E.at(S); NX = 128.75
LISTA = ''.join(f'<div class="vt" style="font-size:58px">{teclea(t_, A, t0, .35)}</div>'
                for t_, t0 in [('1. Prepara', 125.1), ('2. Busca', 125.35), ('3. Contesta', 125.6), ('&gt; ⚠ Revisa', 126.0)])
b = (ventana(X, 110, W, 'Pregunta', f'<div style="display:flex;gap:24px;align-items:flex-start">{sprite("info", 100)}'
             f'{grande(["¿Le pasas *todo*", "a tu IA o la pones", "a _buscar_ primero?"], A, 124.9, size=72)}</div>'
             f'<div style="display:flex;gap:20px;justify-content:center;margin-top:24px"><span class="btn def">Le paso todo</span><span class="btn">Busca primero</span></div>',
             A, 124.75, sale=NX, cu='gris', desde=IC['readme'])
     + ventana(X, 640, W, 'README.md', LISTA, A, 125.0, sale=NX, icono='archivo', desde=IC['readme'])
     + ap('<div class="ps" style="position:absolute;left:120px;top:1180px;font-size:56px;font-weight:700;color:#fff;text-shadow:4px 4px 0 #000">cuéntame en los comentarios 👇</div>', A, 126.4, sale=NX))
seccion('s8-pregunta', S, NX, b)

# ───────────────────────── 2:08 · cierre: «nos vemos cuando toque actualizar este README» (⌘S)
S = 128.75; A = E.at(S)
b = (ventana(X, 110, W, 'README.md', grande(['Nos vemos cuando', 'toque *actualizar*', 'este README'], A, 128.8, size=90), A, 128.78, icono='archivo', desde=IC['readme'])
     + dialogo(110, 560, 860, 'info', '¿Guardar los cambios en <b>README.md</b>?', A, 129.0, botones=('Guardar', 'No'), pulsa=129.55, sale=129.7, titulo='⌘S', desde=(540, 660))
     + ventana(110, 560, 860, 'Guardando…', '<div class="vt" style="font-size:44px;margin-bottom:10px">README.md</div>' + progreso([(0, 0), (129.7, 100, .3)]),
               A, 129.7, sale=130.05, cu='gris')
     + dialogo(110, 560, 860, 'info', '<b>✓ guardado</b>', A, 130.05, titulo='LogOS')
     + cursor([(128.9, 900, 1500), (129.55, 385, 770, True), (130.6, 800, 1300)]))
seccion('s9-cierre', S, FIN, b)

# ───────────────────────── barra de menú (todo el video, transparente, encima): LogOS · README.md #02 RAG + sección actual
SECC = [(0.0, '# RAG'), (4.6, '## ¿Qué es?'), (21.85, '## Paso 1 · Prepara'), (34.2, '## Paso 2 · Busca'), (39.25, '## Paso 3 · Contesta'),
        (47.0, '## Libro vs página'), (60.3, '## Mi ejemplo'), (77.3, '&gt; ⚠ Ojo'), (99.4, '## ¿Y el contexto largo?'), (115.5, '## Funciona hoy'),
        (124.7, '## Tu turno'), (128.75, '✓ guardado')]
A = E.at(0)
SECS = ''.join(ap(f'<span>{n}</span>', A, t, sale=SECC[i + 1][0] if i + 1 < len(SECC) else None, extra='position:absolute;right:24px;top:0;height:64px;display:flex;align-items:center')
               for i, (t, n) in enumerate(SECC))
BARRA = (f'<div class="barra"><span class="lg">{sprite("compu", 40)}LogOS</span><span style="font-weight:500">README.md · #02 RAG</span>'
         f'<span class="vt" style="margin-left:auto;font-size:40px;position:relative;width:440px;height:64px;color:#0a1f8f">{SECS}</span></div>')
PIEZAS.append(('barra', 0.0, FIN, E.page('', BARRA, FIN, S0=0.0, transparente=True)))
PRE = 'rme2-'

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
        rel = os.environ.get('REL', 'readme/2/escritorio')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
