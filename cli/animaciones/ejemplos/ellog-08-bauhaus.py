"""El Log #08 · edición «Bauhaus»: formas primarias que encajan en la retícula al ritmo de la voz, color plano por capítulo,
textos revelados por una barra que barre y un círculo gigante del color nuevo que crece desde una esquina en cada cambio.
Arriba, cinta negra de El Log con «ÚLTIMA HORA» que parpadea, el capítulo actual y una franja amarilla que corre los datos.
Tiempos = voz recortada de noticias/8 (97.46 s), los mismos de ellog-08-recorte.py.
Uso: SALIDA=~/Documents/Videos/noticias/8/bauhaus REL=noticias/8/bauhaus python3 ejemplos/ellog-08-bauhaus.py [ids…]   (SOLO_HTML=1 para revisar)
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bauhaus as B
from bauhaus import forma, etiqueta, numero, N, ap, linea

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.path.expanduser('~/Documents/Videos/noticias/8/bauhaus')))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
FIN = 97.46
C = B.COL
ROJO, AMA, AZUL, NEG, CRE, BLA = C['rojo'], C['amarillo'], C['azul'], C['negro'], C['crema'], C['blanco']
NAR = '#ff6600'
TOP = 230          # primer renglón útil (debajo de la cinta)
PIEZAS = []

# fases: grupos que se deslizan fuera hacia la izquierda en `sale`
GCSS = """
.gp{position:absolute;inset:0;z-index:10}
.gp.x{animation:gps .5s cubic-bezier(.7,0,.9,.4) var(--x) forwards}
@keyframes gps{to{transform:translateX(-1300px)}}
.tx .hl{color:#151515}
.ch{position:absolute;font-weight:800;line-height:1;text-align:center;z-index:12}
.et{white-space:nowrap}
"""
# estilo por fondo: (color de texto, color de la barra, acento, css extra)
TEMA = {
    'crema': (NEG, NEG, ROJO, '', 'rgba(21,21,21,.10)'),
    'negro': (CRE, AMA, ROJO, '', 'rgba(239,232,218,.08)'),
    'azul': (CRE, AMA, AMA, '', 'rgba(239,232,218,.12)'),
    'rojo': (CRE, NEG, AMA, '', 'rgba(239,232,218,.14)'),
    'amarillo': (NEG, NEG, ROJO, '.tx .hl{background:#151515;color:#f3c11b}', 'rgba(21,21,21,.12)'),
}
FONDO = {'crema': CRE, 'negro': NEG, 'azul': AZUL, 'rojo': ROJO, 'amarillo': AMA}


def gp(html, A=None, sale=None):
    if sale is None:
        return f'<div class="gp">{html}</div>'
    return f'<div class="gp x" style="--x:{A(sale)}">{html}</div>'


def escena(pid, start, end, body, fondo='crema', entra='sd', sigue=True):
    if sigue:
        end += B.COLA
    col, bar, ac, css, lin = TEMA[fondo]
    PIEZAS.append((pid, start, end, B.page(GCSS + css, body, round(end - start, 2), S0=start, fondo=FONDO[fondo], entra=entra, lineas=lin)))


def T(fondo):
    """texto() con los colores del fondo de la escena."""
    col, bar, ac, _, _ = TEMA[fondo]

    def f(lineas, A, t, **kw):
        kw.setdefault('color', col); kw.setdefault('bar', bar); kw.setdefault('ac', ac)
        return B.texto(lineas, A, t, **kw)
    return f


def ch(txt, x, y, w, size, A, t, color=NEG, sale=None):
    """Texto centrado sobre una forma (aparece de golpe). Envoltorio propio con z-index: B.ap crea un contexto de apilamiento
    (animación de opacidad) que lo dejaba debajo de las formas."""
    cls, st = 'ap', f'position:absolute;inset:0;z-index:12;pointer-events:none;--d:{A(t)};'
    if sale is not None:
        cls += ' x'; st += f'--x:{A(sale)};'
    return f'<div class="{cls}" style="{st}"><div class="ch" style="left:{x}px;top:{y}px;width:{w}px;font-size:{size}px;color:{color}">{txt}</div></div>'


# ───────── 0:00 · «Dicen que PHP está muerto…» → dos fallos críticos | ¿Laravel, WordPress o PHP? → te toca actualizar
S = 0.0; A = B.at(S); tx = T('negro')
f1 = (tx(['Dicen que PHP', 'está [muerto]…'], A, .3, y=TOP, size=112)
      + forma('barra', 330, 382, 430, 20, ROJO, A, 1.5, desde='izq', z=30, dur=.45)
      + tx(['DOS FALLOS', '{CRÍTICOS}'], A, 1.8, y=560, size=130)
      + forma('c', 640, 880, 340, 340, ROJO, A, 1.8, desde='der')
      + ch('2', 640, 930, 340, 240, A, 2.0, color=CRE)
      + forma('tri', 120, 1260, 220, 190, AMA, A, 2.2, desde='abajo')
      + etiqueta('Urgente', 90, 900, A, 2.5, fondo=ROJO, color=CRE, size=52)
      + etiqueta('# CVE-2026-109618', 90, 1010, A, 3.0, fondo=CRE, color=NEG, size=36)
      + etiqueta('# CVE-2026-109619', 90, 1080, A, 3.6, fondo=CRE, color=NEG, size=36)
      + forma('sq', 420, 1330, 150, 150, AZUL, A, 2.4, desde='abajo'))
f2 = (tx(['¿Laravel,', 'WordPress', 'o [PHP]?'], A, 5.2, y=TOP, size=120)
      + forma('sq', 90, 700, 260, 260, ROJO, A, 6.6, desde='izq')
      + forma('c', 410, 700, 260, 260, AZUL, A, 7.2, desde='abajo')
      + forma('medio', 730, 830, 260, 130, AMA, A, 8.8, desde='der')
      + etiqueta('Laravel', 90, 985, A, 6.7, fondo=CRE, color=NEG)
      + etiqueta('WordPress', 410, 985, A, 7.3, fondo=CRE, color=NEG)
      + etiqueta('o cualquier PHP', 650, 1040, A, 8.9, fondo=AMA, color=NEG)
      + tx(['Te toca', '{actualizar}'], A, 9.2, y=1110, size=150)
      + etiqueta('Ahorita', 650, 1440, A, 9.8, fondo=ROJO, color=CRE, size=60))
escena('e00-alerta', S, 10.9, gp(f1, A, 5.0) + gp(f2, A), fondo='negro', entra='c')

# ───────── 0:11 · se llama PHP2Shell · lo encontraron con IA
S = 10.9; A = B.at(S); tx = T('crema')
escena('e01-php2shell', S, 17.0, gp(
    tx(['Lo llamaron'], A, 11.0, y=TOP, size=110)
    + forma('sq', 60, 400, 960, 250, ROJO, A, 11.3, desde='der')
    + tx(['PHP2Shell'], A, 11.5, x=100, y=440, size=160, color=CRE, bar=AMA)
    + etiqueta('Así le pusieron', 100, 690, A, 13.6)
    + tx(['Lo encontraron', 'con [IA]'], A, 14.7, y=820, size=110)
    + forma('c', 600, 1110, 360, 360, AZUL, A, 15.6, desde='der')
    + forma('sq', 680, 1230, 60, 60, AMA, A, 15.9, escala=True, z=7)
    + forma('sq', 820, 1230, 60, 60, AMA, A, 16.0, escala=True, z=7)
    + forma('barra', 650, 1350, 260, 18, CRE, A, 16.1, escala=True, z=7)
    + forma('tri', 120, 1110, 200, 180, AMA, A, 15.0, desde='izq')
    + etiqueta('La IA ayudó a hallarlo', 90, 1520, A, 16.3, fondo=AZUL, color=CRE)), entra='sd')

# ───────── 0:17 · PHP saca un parche hoy · dos fallos de 9.2 | del 0 al 10 → casi lo máximo
S = 17.0; A = B.at(S); tx = T('amarillo')
f1 = (tx(['PHP saca un', '{parche} hoy'], A, 17.1, y=TOP, size=130, sale=21.5)
      + etiqueta('php.net › versión de seguridad', 80, 560, A, 18.2, size=34)
      + etiqueta('✓ corrige 2 fallos', 80, 630, A, 21.7, fondo=ROJO, color=CRE, size=34)
      + tx(['Dos fallos', 'de [9.2]'], A, 21.7, y=TOP, size=130)
      + forma('c', 700, 1250, 300, 300, NEG, A, 17.6, desde='der')
      + forma('medio', 90, 1450, 300, 150, ROJO, A, 18.0, desde='abajo')
      + numero(N([(0, 0), (24.1, 9.2, 1.0)], f='1'), 60, 760, 440, A, 24.0, color=ROJO)
      + etiqueta('de 10 posibles', 90, 1230, A, 24.6, size=36))
TICKS = ''.join(forma('barra', 86 + i * 90, 780 - (90 if i % 5 == 0 else 60), 10, 90 if i % 5 == 0 else 60, NEG, A, 26.6 + i * .03, desde='arriba', dur=.5)
                + ch(str(i), 61 + i * 90, 800, 60, 44, A, 26.7 + i * .03)
                for i in range(11))
f2 = (tx(['Del 0 al 10…'], A, 25.4, y=TOP, size=130, sale=29.9)
      + linea(80, 780, 930, A, 26.6, grosor=10)
      + TICKS
      + etiqueta('← nada grave', 80, 880, A, 26.8, size=34)
      + etiqueta('lo máximo →', 720, 880, A, 27.1, fondo=ROJO, color=CRE, size=34)
      + forma('tri', 869, 960, 80, 70, ROJO, A, 29.2, desde='abajo', z=8)
      + etiqueta('9.2', 860, 1040, A, 29.3, fondo=ROJO, color=CRE, size=60)
      + tx(['Casi lo', '[máximo]'], A, 30.1, y=1160, size=170)
      + etiqueta('🔥 Crítico', 90, 1560, A, 31.6, fondo=NEG, color=AMA, size=44))
escena('e02-parche', S, 32.85, gp(f1, A, 25.2) + gp(f2, A), fondo='amarillo', entra='ii')

# ───────── 0:33 · ejecución remota de código → corre comandos en tu servidor | tu teclado a un desconocido
S = 32.85; A = B.at(S); tx = T('azul')
MONO = '<span class="mono">{}</span>'
f1 = (tx(['Ejecución', '{remota}', 'de código'], A, 32.95, y=TOP, size=140, sale=37.8)
      + etiqueta('Sin iniciar sesión', 90, 690, A, 36.6, fondo=ROJO, color=CRE, size=40)
      + tx(['Corre comandos', 'en [tu servidor]'], A, 38.0, y=TOP, size=110)
      + forma('c', 560, 820, 400, 400, CRE, A, 38.0, desde='der')
      + forma('barra', 650, 960, 220, 26, NEG, A, 38.3, escala=True, z=7)
      + forma('barra', 650, 1010, 220, 26, NEG, A, 38.4, escala=True, z=7)
      + forma('barra', 650, 1060, 220, 26, NEG, A, 38.5, escala=True, z=7)
      + forma('tri', 150, 930, 220, 190, ROJO, A, 38.8, desde='izq', rot=90)
      + linea(90, 1024, 470, A, 39.0, grosor=12, color=ROJO)
      + etiqueta(MONO.format('$ whoami'), 90, 1330, A, 39.6, fondo=NEG, color=AMA, size=38)
      + etiqueta(MONO.format('$ ls /var/www'), 90, 1405, A, 40.9, fondo=NEG, color=AMA, size=38)
      + etiqueta(MONO.format('$ cat config.php'), 90, 1480, A, 41.6, fondo=NEG, color=AMA, size=38)
      + etiqueta('¡Y no es tuyo!', 600, 1560, A, 41.9, fondo=ROJO, color=CRE, size=44))
KEYS = ''.join(forma('sq', 90 + c * 100, 790 + r * 100, 82, 82, CRE, A, 43.5 + (r * 9 + c) * .012, desde='abajo', dur=.5)
               for r in range(4) for c in range(9))
f2 = (tx(['Tu [teclado]', 'a un', '{desconocido}'], A, 42.7, y=TOP, size=130)
      + KEYS
      + forma('c', 600, 1230, 340, 340, AMA, A, 44.2, desde='der')
      + ch('?', 600, 1270, 340, 240, A, 44.4, color=NEG)
      + forma('barra', 120, 1330, 420, 20, ROJO, A, 44.3, desde='izq'))
escena('e03-remoto', S, 45.4, gp(f1, A, 42.5) + gp(f2, A), fondo='azul', entra='id')

# ───────── 0:45 · no es cualquier cosa · millones de sitios · sitios en alerta | Hacker News: Países Bajos (sin confirmar)
S = 45.4; A = B.at(S); tx = T('crema')
GRID = ''
for i in range(56):
    c, r = i % 8, i // 8
    GRID += forma('sq', 84 + c * 114, 600 + r * 114, 92, 92, [NEG, AZUL, NEG, NEG][(i * 7) % 4], A, 47.3 + ((i * 13) % 56) * .03, desde='arriba', dur=.45)
    if (i * 11) % 5 == 0:
        GRID += forma('sq', 84 + c * 114, 600 + r * 114, 92, 92, ROJO, A, 50.2 + (i % 9) * .14, escala=True, z=6, dur=.35)
f1 = (tx(['No es cualquier', '[cosa]'], A, 45.5, y=TOP, size=120, sale=46.9)
      + tx(['{Millones}', 'de sitios'], A, 47.0, y=TOP, size=140, sale=49.7)
      + tx(['Sitios en', '[alerta]'], A, 49.9, y=TOP, size=140)
      + GRID
      + etiqueta('«Sitios en alerta», dicen los medios', 84, 1440, A, 51.5, fondo=ROJO, color=CRE, size=34))
QUOTE = (tx(['El centro de ciberseguridad'], A, 55.6, x=110, y=560, size=60)
         + tx(['de [Países Bajos]'], A, 57.1, x=110, y=640, size=60)
         + tx(['quedó fuera de línea'], A, 58.3, x=110, y=720, size=60)
         + tx(['por usar PHP'], A, 59.1, x=110, y=800, size=60))
f2 = (forma('sq', 90, 240, 170, 170, NAR, A, 53.1, desde='izq')
      + ch('Y', 90, 255, 170, 140, A, 53.3, color=CRE)
      + tx(['Lo que dicen en', '[Hacker News]'], A, 53.0, x=300, y=250, size=80, ancho=720, ac=NAR)
      + forma('barra', 66, 560, 18, 310, NAR, A, 55.4, desde='arriba')
      + QUOTE
      + etiqueta('Sin confirmar', 560, 950, A, 60.2, fondo=ROJO, color=CRE, size=48)
      + tx(['Ojo: aún', '{sin confirmar}'], A, 60.0, y=1110, size=120)
      + forma('c', 760, 1440, 200, 200, AZUL, A, 60.4, desde='der'))
escena('e04-sitios', S, 63.5, gp(f1, A, 52.8) + gp(f2, A), entra='si')

# ───────── 1:03 · PHP no es malo · la IA ya encuentra fallos · saldrán más seguido | no lo dejes para después
S = 63.5; A = B.at(S); tx = T('rojo')
CODE = ''.join(forma('barra', 90, 1080 + i * 64, w, 30, CRE, A, 67.6 + i * .06, desde='izq', dur=.5) for i, w in enumerate([420, 620, 540, 700, 480, 360]))
f1 = (gp(tx(['PHP no es', '[malo]'], A, 63.6, y=TOP, size=150)
         + etiqueta('✓ sigue bien', 90, 560, A, 66.5, fondo=CRE, color=ROJO, size=48), A, 67.2)
      + tx(['La IA', 'encuentra', '{fallos}'], A, 67.4, y=TOP, size=120, sale=71.0)
      + forma('c', 660, 640, 320, 320, CRE, A, 67.4, desde='der')
      + forma('sq', 730, 740, 54, 54, NEG, A, 67.8, escala=True, z=7)
      + forma('sq', 850, 740, 54, 54, NEG, A, 67.9, escala=True, z=7)
      + CODE
      + forma('barra', 70, 1060, 940, 8, AMA, A, 68.0, desde='izq', z=8)
      + forma('sq', 660, 1208, 60, 30, AMA, A, 69.2, escala=True, z=8)
      + forma('sq', 820, 1272, 60, 30, AMA, A, 70.1, escala=True, z=8)
      + tx(['Saldrán más', '[seguido]'], A, 71.1, y=TOP, size=130)
      + ''.join(forma('barra', 620 + i * 80, 1560 - h, 56, h, AMA, A, 72.3 + i * .08, desde='abajo', dur=.55) for i, h in enumerate([60, 110, 170, 250, 340]))
      + etiqueta('más reportes', 620, 1580, A, 72.6, fondo=NEG, color=AMA, size=34))
f2 = (tx(['No lo dejes', 'para [después]'], A, 73.3, y=TOP, size=120)
      + etiqueta('Después…', 100, 680, A, 73.8, fondo=CRE, color=NEG, size=80)
      + forma('barra', 80, 722, 400, 18, NEG, A, 74.6, desde='izq', z=30, dur=.45)
      + forma('c', 520, 880, 420, 420, AMA, A, 75.9, escala=True)
      + ch('HOY', 520, 1000, 420, 170, A, 76.0, color=NEG))
escena('e05-ia', S, 76.6, gp(f1, A, 73.1) + gp(f2, A), fondo='rojo', entra='sd')

# ───────── 1:17 · ¿qué versión tienes? · corre php -v · ya con el parche | PHP no está muerto · hoy lo actualizamos
S = 76.6; A = B.at(S); tx = T('negro')
RAMAS = [('8.5.12', 83.2, ROJO, CRE), ('8.4.27', 83.5, AZUL, CRE), ('8.3.36', 83.8, AMA, NEG), ('8.2.35', 84.1, CRE, NEG)]
VER = ''.join(forma('barra', 90, 820 + i * 170, 760 - i * 90, 130, c, A, t, desde='izq')
              + ch(f'{v} ✓', 90, 852 + i * 170, 420, 72, A, t + .25, color=k) for i, (v, t, c, k) in enumerate(RAMAS))
f1 = (tx(['¿Qué versión', '[tienes]?'], A, 76.7, y=TOP, size=130, sale=79.4)
      + tx(['Corre', '{php -v}'], A, 79.6, y=TOP, size=140, sale=83.0)
      + etiqueta(MONO.format('$ php -v → PHP 8.4.27'), 90, 600, A, 80.0, fondo=CRE, color=NEG, size=40)
      + etiqueta('compárala con la última de tu rama', 90, 680, A, 81.8, fondo=AMA, color=NEG, size=32)
      + tx(['Ya con el', '{parche}'], A, 83.2, y=TOP, size=130)
      + VER)
f2 = (tx(['PHP no está', '[muerto]'], A, 86.2, y=TOP, size=150)
      + forma('barra', 60, 440, 540, 22, AMA, A, 87.3, desde='izq', z=30, dur=.45)
      + forma('c', 120, 700, 520, 520, AMA, A, 88.0, desde='izq', gira=True)
      + forma('cuarto', 380, 700, 260, 260, ROJO, A, 88.2, desde='arriba', gira=True)
      + forma('c', 300, 880, 160, 160, NEG, A, 88.3, escala=True)
      + tx(['Tan vivo que hoy', 'lo {actualizamos}'], A, 88.3, y=1300, size=96)
      + etiqueta('♥ vivo', 720, 1060, A, 89.8, fondo=ROJO, color=CRE, size=56))
escena('e06-version', S, 91.1, gp(f1, A, 86.0) + gp(f2, A), fondo='negro', entra='ii')

# ───────── 1:31 · cierre: ¿cada cuánto actualizas tu servidor? (abajo entra «Sígueme»)
S = 91.1; A = B.at(S); tx = T('crema')
escena('e07-cierre', S, FIN, gp(
    tx(['¿Cada cuánto', 'actualizas tu', '[servidor]?'], A, 91.2, y=TOP, size=120)
    + forma('sq', 90, 700, 900, 150, NEG, A, 92.1, desde='izq')
    + tx(['📅 Siempre al día'], A, 92.2, x=130, y=735, size=70, color=CRE, bar=AMA)
    + forma('sq', 90, 880, 900, 150, ROJO, A, 92.9, desde='der')
    + tx(['🔥 Cuando algo truena'], A, 93.0, x=130, y=915, size=70, color=CRE, bar=AMA)
    + forma('c', 880, 560, 120, 120, AMA, A, 91.6, escala=True)), entra='id', sigue=False)

# ───────── «Sígueme» (transparente, sobre el cierre)
SEG_INI = 93.9
S = SEG_INI; A = B.at(S)
SEG = (forma('sq', 90, 1120, 900, 490, AZUL, A, 94.0, desde='der')
       + forma('c', 830, 1060, 160, 160, AMA, A, 94.2, escala=True, z=6)
       + B.texto(['Sígueme'], A, 94.1, x=130, y=1150, size=76, color=CRE, bar=AMA)
       + B.texto(['Armando · El Log cada semana'], A, 94.3, x=130, y=1245, size=44, color=CRE, bar=AMA)
       + forma('sq', 130, 1325, 320, 92, AMA, A, 94.8, escala=True, z=6)
       + ch('Seguir ✓', 130, 1340, 320, 58, A, 94.9, color=NEG)
       + etiqueta('🛠️ ¿Cada cuánto actualizas?', 130, 1450, A, 95.0, fondo=CRE, color=NEG, size=36)
       + etiqueta('Cada semana, ya aprendí 😅', 130, 1520, A, 95.3, fondo=NEG, color=AMA, size=36))
PIEZAS.append(('seguir', SEG_INI, FIN, B.page(GCSS, SEG, round(FIN - SEG_INI, 2), S0=SEG_INI, transparente=True)))

# ───────── cinta de El Log: barra negra con «ÚLTIMA HORA», capítulo actual y franja amarilla que corre los datos (todo el video)
CORRIDO = ['PHP 8.5.12, 8.4.27, 8.3.36 y 8.2.35 corrigen los dos fallos', 'CVE-2026-109618 y CVE-2026-109619: 9.2 de 10',
           'Ejecución de código sin iniciar sesión', 'Parche de emergencia: salió un día antes por una filtración',
           'Los encontraron investigadores de Calif, Wiz y OpenAI', 'Hacker News: lo de Países Bajos aún no está confirmado', 'Revisa tu versión: php -v']
CAPS = [(0.0, 'Alerta'), (10.9, 'PHP2Shell'), (17.0, 'El parche'), (32.85, 'Ejecución remota'), (45.4, 'Sitios en alerta'), (63.5, 'La IA'),
        (76.6, 'Tu versión'), (91.1, 'Tu opinión')]
A = B.at(0)
CAPH = ''.join(ap(f'<div class="cp">{i + 1:02d} · {n}</div>', A, t, CAPS[i + 1][0] if i + 1 < len(CAPS) else None) for i, (t, n) in enumerate(CAPS))
TICK = '<span class="sp">■</span>'.join(f'<span>{c}</span>' for c in CORRIDO)
CINTA_CSS = """
.ci{position:absolute;left:0;right:0;top:0;height:144px;z-index:90;animation:ciIn .5s cubic-bezier(.3,1.3,.45,1) both}
@keyframes ciIn{from{transform:translateY(-150px)}to{transform:none}}
.ci .tp{position:absolute;left:0;right:0;top:0;height:96px;background:#151515;color:#efe8da;display:flex;align-items:center;gap:22px;padding:0 34px}
.ci .lg{font-weight:900;font-size:44px;letter-spacing:-.01em;white-space:nowrap}.ci .lg b{color:#f3c11b;font-weight:900}
.ci .ul{font-weight:800;font-size:28px;letter-spacing:.06em;text-transform:uppercase;background:#e2352b;color:#efe8da;padding:6px 14px;white-space:nowrap;animation:ulb 1s steps(1) infinite}
@keyframes ulb{50%{background:#efe8da;color:#e2352b}}
.ci .cp{position:absolute;right:34px;top:26px;font-weight:700;font-size:34px;color:#efe8da;white-space:nowrap}
.ci .ln{position:absolute;left:0;right:0;top:96px;height:48px;background:#f3c11b;overflow:hidden;display:flex;align-items:center}
.ci .mv{display:flex;gap:26px;white-space:nowrap;font-weight:700;font-size:28px;color:#151515;text-transform:uppercase;letter-spacing:.02em;padding-left:300px;animation:mv 80s linear infinite}
.ci .sp{color:#e2352b}
@keyframes mv{to{transform:translateX(-100%)}}
"""
CINTA = (f'<div class="ci"><div class="tp"><span class="lg">EL LOG <b>·</b> N.º 08</span><span class="ul">⚠ Última hora</span></div>{CAPH}'
         f'<div class="ln"><div class="mv">{TICK}<span class="sp">■</span>{TICK}</div></div></div>')
PIEZAS.append(('cinta', 0.0, FIN, B.page(CINTA_CSS, CINTA, FIN, S0=0.0, transparente=True)))
PRE = 'ellb8-'

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
        rel = os.environ.get('REL', 'noticias/8/bauhaus')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
