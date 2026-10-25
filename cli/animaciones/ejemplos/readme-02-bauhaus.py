"""El Readme #02 · RAG — edición «Bauhaus»: geometría plana y primarios sobre la retícula. El RAG se explica con formas:
documentos = rectángulos que se parten en cuadritos (pedazos), la búsqueda = un anillo (lupa) que recorre la retícula y pinta
los cuadritos que coinciden, pregunta + pedazos → flecha (triángulo) → bloque de respuesta; libro entero (pila de barras) vs una
página; homelab como pila de rectángulos con contador; tres advertencias en triángulos amarillos; barra de tokens que se llena.
Cada sección cambia de color de fondo y entra con un círculo que crece desde una esquina distinta.
Arriba, una franja negra transparente sobre todo el video («etiqueta») con README.md · #02 RAG y la sección actual.
Tiempos = readme/2/voz/voz-norm.wav (132.34 s), los mismos de readme-02-recorte.py.
Uso: SALIDA=~/Documents/Videos/readme/2/bauhaus REL=readme/2/bauhaus python3 ejemplos/readme-02-bauhaus.py [ids…]   (SOLO_HTML=1 para revisar)
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bauhaus as B
from bauhaus import forma, N, numero, etiqueta, linea, ap, COL

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.path.expanduser('~/Documents/Videos/readme/2/bauhaus')))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
FIN = 132.34
TOP = 190          # primer renglón útil (debajo de la franja de 0–130)
PIEZAS = []
CR, RJ, AM, AZ, NG = COL['crema'], COL['rojo'], COL['amarillo'], COL['azul'], COL['negro']

# esquema de color por fondo: texto, barra que revela, acento, resalte (fondo, tinta), líneas de la retícula, tinta de código
SCH = {
    'crema': dict(fondo=CR, txt=NG, bar=NG, ac=RJ, hl=(AM, NG), lin='rgba(21,21,21,.10)', cb=NG, cc=CR),
    'azul': dict(fondo=AZ, txt=CR, bar=AM, ac=AM, hl=(AM, NG), lin='rgba(255,255,255,.13)', cb=NG, cc=AM),
    'rojo': dict(fondo=RJ, txt=CR, bar=NG, ac=AM, hl=(AM, NG), lin='rgba(255,255,255,.13)', cb=NG, cc=CR),
    'negro': dict(fondo=NG, txt=CR, bar=RJ, ac=AM, hl=(AM, NG), lin='rgba(255,255,255,.10)', cb=CR, cc=NG),
    'amarillo': dict(fondo=AM, txt=NG, bar=NG, ac=RJ, hl=(AZ, CR), lin='rgba(21,21,21,.12)', cb=NG, cc=AM),
}

# fases internas (se barren a la izquierda) y bloques de código (revelado a pasos)
CSS = """
.fz{position:absolute;inset:0;z-index:10}
.fz.x{animation:fsale .5s cubic-bezier(.7,0,.9,.4) var(--x) forwards}
.fz.in{opacity:0;animation:apo .01s steps(1) var(--d) forwards}
.fz.in.x{opacity:0;animation:apo .01s steps(1) var(--d) forwards,fsale .5s cubic-bezier(.7,0,.9,.4) var(--x) forwards}
@keyframes fsale{to{transform:translateX(-1250px)}}
.cd{position:absolute;z-index:22;font-family:'JetBrains Mono',monospace;font-weight:500;font-size:var(--fs,34px);padding:12px 22px;background:var(--b,#151515);color:var(--c,#efe8da);
  white-space:nowrap;clip-path:inset(0 100% 0 0);animation:rev .5s steps(12) var(--d) forwards}
.cd.x{animation:rev .5s steps(12) var(--d) forwards,apc .01s steps(1) var(--x) forwards}
.cd b{font-weight:700;color:var(--k,#f3c11b)}
.bl{width:100%;height:100%;display:flex;flex-direction:column;justify-content:center;font-weight:800;line-height:1.02}
.mono{font-family:'JetBrains Mono',monospace}
.lp{position:absolute;inset:0;z-index:12}
"""


def escena(pid, start, end, esq, fondo, body, css='', sigue=True):
    if sigue:
        end += B.COLA
    s = SCH[fondo]
    c = CSS + f'.tx .hl{{background:{s["hl"][0]};color:{s["hl"][1]}}}' + css
    PIEZAS.append((pid, start, end, B.page(c, body, round(end - start, 2), S0=start, fondo=s['fondo'], entra=esq, lineas=s['lin'])))


def T(lineas, A, t, s, y=TOP, size=120, **kw):
    return B.texto(lineas, A, t, y=y, size=size, color=s['txt'], bar=s['bar'], ac=s['ac'], **kw)


def cod(txt, x, y, A, t, s, sale=None, size=34, b=None, c=None, k=None):
    st = f'left:{x}px;top:{y}px;--fs:{size}px;--d:{A(t)};--b:{b or s["cb"]};--c:{c or s["cc"]};' + (f'--k:{k};' if k else '')
    cls = 'cd'
    if sale is not None:
        cls += ' x'; st += f'--x:{A(sale)};'
    return f'<div class="{cls}" style="{st}">{txt}</div>'


def fz(html, A, entra=None, sale=None):
    cls, st = 'fz', ''
    if entra is not None:
        cls += ' in'; st += f'--d:{A(entra)};'
    if sale is not None:
        cls += ' x'; st += f'--x:{A(sale)};'
    return f'<div class="{cls}" style="{st}">{html}</div>'


def doc(titulo, color, tinta, n=4, size=24):
    ws = (88, 64, 80, 56, 74, 68, 84, 60)
    lines = ''.join(f'<i style="display:block;height:12px;width:{ws[i % 8]}%;background:{tinta};opacity:.4;margin-top:14px"></i>' for i in range(n))
    return (f'<div style="width:100%;height:100%;background:{color};padding:22px 24px;color:{tinta}">'
            f'<div class="mono" style="font-size:{size}px;font-weight:700">{titulo}</div>{lines}</div>')


def caja(html, color, tinta, size=52, pad='26px 34px', radio='0', align='left'):
    return (f'<div class="bl" style="background:{color};color:{tinta};font-size:{size}px;padding:{pad};border-radius:{radio};text-align:{align};'
            f'{"align-items:center;" if align == "center" else ""}"><div>{html}</div></div>')


def sello(txt, color, tinta, size=44):
    """Círculo con texto (sello geométrico)."""
    return caja(txt, color, tinta, size=size, pad='0', radio='50%', align='center')


def tri_txt(txt, color, tinta, size=46):
    """Triángulo con texto abajo (advertencia)."""
    return (f'<div style="width:100%;height:100%;background:{color};clip-path:polygon(50% 0,100% 100%,0 100%);display:flex;align-items:flex-end;'
            f'justify-content:center;padding-bottom:12%;font-weight:900;font-size:{size}px;color:{tinta}">{txt}</div>')


def lupa(x, y, s, color, A, t, sale=None, desde='der'):
    return (forma('anillo', x, y, s, s, color, A, t, desde=desde, sale=sale)
            + forma('barra', x + s * .78, y + s * .72, s * .17, s * .52, color, A, t + .06, desde=desde, sale=sale, rot=-45))


def tri(x, y, w, h, color, A, t, rot=90, sale=None, desde='izq'):
    return forma('tri', x, y, w, h, color, A, t, desde=desde, rot=rot, sale=sale)


# ───────────────────────── 0:00 · gancho: tu IA contesta sin conocer tus datos → se lo inventa → 3 pasos
S = 0.0; A = B.at(S); s = SCH['crema']
escena('s0-gancho', S, 4.6, 'sd', 'crema',
       T(['Tu IA contesta', '{sin tus datos}'], A, .15, s, size=110)
       + cod('› ¿qué dice <b>mi contrato</b>?', 70, 470, A, .3, s)
       + cod('🤖 probablemente… (no lo leyó)', 70, 550, A, 1.15, s, b=AZ, c=CR)
       + forma(doc('¿tus docs?', AZ, CR, 6, 30), 90, 680, 380, 420, 'transparent', A, 1.2, desde='izq')
       + forma(doc('¿tus notas?', AM, NG, 6, 30), 610, 720, 380, 420, 'transparent', A, 1.5, desde='der')
       + forma(sello('INVEN-<br>TADO', RJ, CR, 50), 390, 760, 300, 300, 'transparent', A, 1.9, escala=True, dur=.45)
       + T(['Arreglo:', '[3 pasos]'], A, 2.55, s, y=1160, size=100)
       + forma('c', 560, 1170, 150, 150, RJ, A, 2.6, desde='der')
       + forma('sq', 740, 1170, 150, 150, AZ, A, 2.75, desde='der')
       + forma('tri', 560, 1350, 160, 150, NG, A, 2.9, desde='abajo')
       + cod('prepara · busca · contesta', 70, 1420, A, 2.9, s))

# ───────────────────────── 0:04 · RAG: que conteste con tus datos | en vez de todo, busca solo lo que sirve
S = 4.6; A = B.at(S); s = SCH['azul']
RAGL = [('R', 'etrieval', CR, NG), ('A', 'ugmented', AM, NG), ('G', 'eneration', RJ, CR)]
f1 = (numero('RAG', 70, TOP, 360, A, 4.8, color=AM)
      + ''.join(forma(caja(f'<span><b style="font-weight:900;font-size:1.25em">{a}</b>{b}</span>', c, k, 58, '0 34px'), 90, 540 + i * 115, 900, 100, 'transparent', A, 5.0 + i * .15)
                for i, (a, b, c, k) in enumerate(RAGL))
      + cod('RAG = <b>buscar</b> → <b>contestar</b>', 90, 900, A, 5.9, s, size=38)
      + T(['Contesta con', '{tus datos}'], A, 8.86, s, y=1060, size=120)
      + forma(sello('NO SE LO<br>IMAGINA', AM, NG, 40), 680, 1330, 290, 290, 'transparent', A, 10.5, escala=True, dur=.45))
DOCS = ''.join(forma(doc(f'doc_{i + 1}.md', CR, NG, 5), 90 + (i % 3) * 310, 480 + (i // 3) * 220, 280, 190, 'transparent', A, 11.3 + i * .08,
                     desde='izq' if i % 2 else 'arriba') for i in range(6))
CHK = ''.join(forma(doc(f'pedazo {n}', AM, NG, 3, 28), 90 + i * 310, 1040, 280, 230, 'transparent', A, 19.95 + i * .14, desde='der')
              for i, n in enumerate(['014', '017', '031']))
f2 = (T(['En vez de', 'pasarle [todo]…'], A, 11.1, s, size=120, sale=14.15)
      + T(['{Busca}', 'primero'], A, 14.3, s, size=120, sale=19.8)
      + T(['Solo lo que', '[sirve]'], A, 19.9, s, size=120)
      + DOCS
      + forma('barra', 60, 690, 960, 28, RJ, A, 12.9, rot=-12, sale=14.2, hacia='der')
      + cod('✕ todos los docs', 90, 940, A, 12.9, s, sale=14.2, b=RJ, c=CR)
      + f'<div class="lp" style="animation:lp1 4.6s cubic-bezier(.65,0,.35,1) {A(14.7)} both">{lupa(150, 500, 160, AM, A, 14.4, sale=19.8)}</div>'
      + cod('$ rag search <b>"tu pregunta"</b>', 90, 940, A, 14.3, s, sale=19.85)
      + CHK
      + linea(90, 1300, 900, A, 20.4, grosor=10, color=AM)
      + cod('contexto: <b>3 pedazos</b> · nada más', 90, 1340, A, 19.9, s, size=38))
escena('s1-rag', S, 21.85, 'ii', 'azul', fz(f1, A, sale=10.9) + fz(f2, A, entra=11.0),
       css='@keyframes lp1{0%{transform:translate(0,0)}25%{transform:translate(620px,0)}50%{transform:translate(620px,220px)}75%{transform:translate(0,220px)}100%{transform:translate(310px,110px)}}')

# ───────────────────────── 0:21 · 3 pasos: prepara (pedazos con significado, por idea) → busca (los que más se parecen) → contesta solo con eso
S = 21.85; A = B.at(S); s = SCH['crema']
P4 = [(520, 520, '014', RJ, CR), (780, 520, '015', AZ, CR), (520, 760, '016', AM, NG), (780, 760, '017', NG, CR)]
f1 = (T(['Paso 1', '[prepara]'], A, 21.95, s, size=140)
      + cod('$ rag index ./docs → <b>pedazos</b>', 90, 1030, A, 22.0, s)
      + forma(doc('docs/', AZ, CR, 10, 30), 90, 520, 360, 460, 'transparent', A, 22.2, desde='izq')
      + ''.join(forma(doc(n, c, k, 3, 26), x, y, 220, 200, 'transparent', A, 26.47 + i * .12, escala=True, dur=.5)
                for i, (x, y, n, c, k) in enumerate(P4))
      + cod('✂ pedazos pequeños', 520, 470, A, 26.5, s, size=28, b=RJ, c=CR)
      + T(['Conserva su', '{significado}'], A, 29.0, s, y=1120, size=100)
      + cod('buscar «cancelar plan» ≈ «dar de baja»', 90, 1370, A, 29.95, s, size=32)
      + etiqueta('Por idea ✓', 90, 1470, A, 31.42, fondo=AZ, color=CR)
      + etiqueta('Palabra exacta ✕', 470, 1470, A, 32.94, fondo=RJ, color=CR))
G6 = [(90 + (i % 3) * 310, 700 + (i // 3) * 230, f'0{10 + i * 4}') for i in range(6)]
HIT = [0, 1, 3]
f2 = (T(['Paso 2', '[busca]'], A, 34.3, s, size=140)
      + forma(caja('¿cómo cancelo mi plan?', NG, CR, 50, '0 34px'), 90, 520, 900, 120, 'transparent', A, 34.5, desde='der')
      + ''.join(forma(doc(f'pedazo {n}', CR, NG, 3, 26), x, y, 280, 200, 'transparent', A, 34.7 + i * .07, desde='abajo')
                + (ap(f'<div style="position:absolute;left:{x}px;top:{y}px;width:280px;height:200px;z-index:6">{doc(f"pedazo {n}", AM, NG, 3, 26)}</div>', A, 37.0 + HIT.index(i) * .15, estilo='position:absolute;inset:0;z-index:7')
                   if i in HIT else '') for i, (x, y, n) in enumerate(G6))
      + f'<div class="lp" style="animation:lp2 1.9s cubic-bezier(.65,0,.35,1) {A(35.1)} both">{lupa(110, 690, 150, RJ, A, 35.0)}</div>'
      + ''.join(forma(doc(f'pedazo {G6[h][2]}', RJ, CR, 2, 24), 90 + i * 310, 1180, 280, 170, 'transparent', A, 38.31 + i * .1, desde='arriba')
                for i, h in enumerate(HIT))
      + cod('$ rag search <b>"pregunta"</b> → top 3', 90, 1400, A, 34.4, s)
      + cod('los que más se parecen ↑', 90, 1480, A, 38.31, s, b=RJ, c=CR))
f3 = (T(['Paso 3', '[contesta]'], A, 39.3, s, size=140)
      + forma(caja('¿cómo cancelo<br>mi plan?', NG, CR, 46, '0 30px'), 90, 520, 400, 200, 'transparent', A, 39.4, desde='izq')
      + forma('barra', 525, 600, 70, 20, RJ, A, 39.6, desde='arriba') + forma('barra', 550, 575, 20, 70, RJ, A, 39.6, desde='arriba')
      + ''.join(forma(doc(f'pedazo {n}', AM, NG, 2, 24), 630 + i * 30, 500 + i * 30, 300, 150, 'transparent', A, 39.7 + i * .1, desde='der')
                for i, n in enumerate(['014', '017', '031']))
      + tri(470, 760, 140, 110, NG, A, 42.43, rot=180, desde='arriba')
      + cod('pregunta + pedazos', 640, 790, A, 42.43, s, size=30, b=AZ, c=CR)
      + forma(caja('«Ve a <span style="color:#f3c11b">Ajustes › Plan</span><br>y toca Dar de baja.»', AZ, CR, 52), 90, 900, 900, 240, 'transparent', A, 44.2, desde='izq')
      + cod('ia(<b>pregunta</b>, <b>pedazos</b>)', 90, 1190, A, 39.4, s)
      + cod('› contesta <b>usando solo eso</b> ✓', 90, 1270, A, 43.65, s)
      + forma(sello('SOLO<br>ESO', RJ, CR, 56), 680, 1330, 280, 280, 'transparent', A, 45.76, escala=True, dur=.45))
escena('s2-pasos', S, 47.0, 'si', 'crema', fz(f1, A, sale=34.2) + fz(f2, A, entra=34.26, sale=39.2) + fz(f3, A, entra=39.28),
       css='@keyframes lp2{0%{transform:translate(0,0)}35%{transform:translate(310px,0)}70%{transform:translate(620px,0)}100%{transform:translate(0,230px)}}')

# ───────────────────────── 0:47 · libro entero vs la página que ocupa
S = 47.0; A = B.at(S); s = SCH['rojo']
LIBRO = ''.join(f'<i style="display:block;height:30px;background:{CR};margin-bottom:14px;width:{[100, 96, 100, 92, 98, 100, 94, 100, 97, 100, 95, 100, 93][i]}%"></i>' for i in range(13))
f1 = (T(['¿Le das [todo]', 'el contexto?'], A, 47.1, s, size=115)
      + forma(f'<div style="width:100%;height:100%;padding:24px;background:{NG}">{LIBRO}</div>', 90, 500, 520, 620, 'transparent', A, 47.3, desde='izq')
      + numero(N([(0, 1), (48.8, 412, 1.4)]), 660, 520, 190, A, 48.8, color=AM)
      + cod('páginas', 670, 720, A, 48.9, s, b=NG, c=CR)
      + etiqueta('Libro entero', 90, 1170, A, 50.81, fondo=NG, color=CR, size=44)
      + f'<div class="lp" style="animation:lp3 2.2s cubic-bezier(.65,0,.35,1) {A(52.4)} both">{lupa(380, 520, 180, AM, A, 52.2)}</div>'
      + cod('…y que encuentre <b>la página</b>', 90, 1270, A, 52.28, s))
f2 = (T(['Con RAG:', 'solo [esa página]'], A, 54.9, s, size=115)
      + forma(f'<div style="width:100%;height:100%;background:{CR};padding:40px 44px;color:{NG}"><div class="mono" style="font-size:30px;font-weight:700;opacity:.6">pág. 217</div>'
              + ''.join(f'<i style="display:block;height:16px;width:{w}%;background:{NG};opacity:.25;margin-top:22px"></i>' for w in (90, 72, 84, 66))
              + '<div style="margin-top:28px;font-weight:800;font-size:36px;line-height:1.1;min-height:60px">'
              + ap('<span style="background:' + AM + ';padding:2px 8px">Cancela en Ajustes › Plan</span>', A, 56.69, estilo='position:relative;inset:auto') + '</div>'
              + ''.join(f'<i style="display:block;height:16px;width:{w}%;background:{NG};opacity:.25;margin-top:22px"></i>' for w in (80, 92, 58))
              + '</div>', 260, 500, 620, 720, 'transparent', A, 55.1, desde='izq')
      + cod('tu pregunta', 90, 1300, A, 59.36, s, b=AM, c=NG)
      + tri(380, 1260, 110, 100, AM, A, 59.5, rot=0, desde='abajo'))
escena('s3-libro', S, 60.3, 'id', 'rojo', fz(f1, A, sale=54.85) + fz(f2, A, entra=54.9),
       css='@keyframes lp3{0%{transform:translate(0,0)}50%{transform:translate(-120px,240px)}100%{transform:translate(0,420px)}}')

# ───────────────────────── 1:00 · mi ejemplo: el homelab recaba redes y proyectos → Claude contesta solo con eso (medio RAG)
S = 60.3; A = B.at(S); s = SCH['negro']
RACK = ''.join(f'<div style="height:120px;margin-top:{20 if i else 0}px;background:{CR};display:flex;align-items:center;gap:16px;padding:0 28px">'
               + ''.join(f'<i class="led" style="width:24px;height:24px;border-radius:50%;background:{[RJ, AM, AZ][j]};animation:led .5s steps(1) {(i * 3 + j) * .17:.2f}s infinite"></i>' for j in range(3))
               + f'<i style="flex:1;height:16px;margin-left:30px;background:{NG}"></i></div>' for i in range(3))
f1 = (T(['Mi [homelab]'], A, 60.4, s, size=140)
      + etiqueta('Medio RAG', 90, 370, A, 63.79, fondo=AM, color=NG)
      + forma(f'<div style="width:100%;height:100%">{RACK}</div>', 90, 480, 400, 400, 'transparent', A, 60.8, desde='izq')
      + numero(N([(0, 0), (64.6, 1284, 3.0)], f='c'), 540, 480, 170, A, 63.9, color=AM)
      + cod('registros recabados', 545, 650, A, 64.6, s)
      + forma(sello('REDES', RJ, CR, 40), 540, 760, 200, 200, 'transparent', A, 66.77, escala=True, dur=.45)
      + forma(caja('PROYEC-<br>TOS', AZ, CR, 36, '0', align='center'), 790, 760, 200, 200, 'transparent', A, 67.51, escala=True, dur=.45)
      + tri(490, 810, 70, 60, AM, A, 67.0, rot=-90, desde='der')
      + linea(540, 1000, 450, A, 67.7, grosor=10, color=AM)
      + cod('redes sociales + proyectos → homelab', 90, 1060, A, 67.6, s, size=30))
f2 = (T(['Claude contesta', 'solo con [eso]'], A, 68.1, s, size=115)
      + cod('› claude: <b>¿cómo van mis redes?</b>', 90, 500, A, 68.05, s)
      + cod('contexto = <b>datos guardados</b> · nada más', 90, 580, A, 70.45, s)
      + forma(sello('Claude', '#d97757', CR, 56), 700, 700, 280, 280, 'transparent', A, 70.11, escala=True, dur=.45)
      + forma(caja('Lo que se guardó<br>en el homelab,<br><span style="color:#e2352b">y nada más.</span>', CR, NG, 48), 90, 700, 560, 300, 'transparent', A, 70.6, desde='izq')
      + etiqueta('Solo esos datos', 90, 1070, A, 72.46, fondo=AM, color=NG, size=44))
escena('s4-ejemplo', S, 77.3, 'sd', 'negro', fz(f1, A, sale=68.0) + fz(f2, A, entra=68.05),
       css='@keyframes led{50%{background:#555}}')

# ───────────────────────── 1:17 · > ⚠️ Ojo: mal cortado · desactualizado · búsqueda equivocada → revisa qué encontró
S = 77.3; A = B.at(S); s = SCH['crema']
CAB = T(['&gt; [Ojo]'], A, 77.4, s, size=130) + cod('tres cuidados', 470, 230, A, 77.9, s, b=RJ, c=CR)


def adv(n, t):
    return (forma('tri', 84, 414, 212, 192, NG, A, t, desde='izq') + forma(tri_txt(f'{n}/3', AM, NG, 44), 90, 420, 200, 180, 'transparent', A, t + .04, desde='izq', z=6))


c1 = (adv(1, 79.5) + T(['Pedazos mal', '{cortados}'], A, 79.6, s, y=640, size=110)
      + forma(caja('«El plan cuesta…', CR, NG, 48), 90, 920, 460, 180, 'transparent', A, 80.52, rot=-3, desde='izq', extra='box-shadow:inset 0 0 0 6px #151515;')
      + forma(caja('…$99 al mes»', NG, CR, 48), 590, 980, 400, 180, 'transparent', A, 80.7, rot=4, desde='der')
      + cod('✂ a medias', 90, 1200, A, 83.51, s, b=RJ, c=CR, size=40))
c2 = (adv(2, 83.94) + T(['Datos', '{desactualizados}'], A, 84.0, s, y=640, size=100)
      + forma(caja('precio 2024<br><span style="font-size:1.6em">$79</span>', AM, NG, 44), 90, 900, 380, 240, 'transparent', A, 85.13, desde='izq')
      + forma(caja('≠', 'transparent', RJ, 150, '0', align='center'), 480, 900, 140, 240, 'transparent', A, 85.4, escala=True, dur=.4)
      + forma(caja('hoy<br><span style="font-size:1.6em">$99</span>', AZ, CR, 44), 630, 900, 360, 240, 'transparent', A, 85.6, desde='der')
      + etiqueta('Ya no es cierto', 90, 1200, A, 89.62, fondo=RJ, color=CR, size=44))
c3 = (adv(3, 90.72) + T(['Búsqueda', '{equivocada}'], A, 90.8, s, y=640, size=110)
      + cod('busca «baja» → trae «bajar precio»', 90, 920, A, 91.0, s, size=36)
      + forma('barra', 600, 942, 340, 12, RJ, A, 92.34, desde='der')
      + etiqueta('Trae lo que no es', 90, 1040, A, 92.34, fondo=RJ, color=CR, size=44))
c4 = (T(['{Revisa} qué', 'encontró'], A, 96.45, s, y=420, size=130)
      + cod('$ rag search <b>--show-sources</b>', 90, 720, A, 96.5, s)
      + cod('✓ pedazo 017 · pedazo 031', 90, 800, A, 97.61, s, b=AZ, c=CR)
      + forma(sello('✓', AZ, CR, 150), 680, 960, 290, 290, 'transparent', A, 97.61, escala=True, dur=.45)
      + forma('sq', 90, 960, 200, 200, AM, A, 97.7, desde='izq') + forma('c', 320, 1010, 150, 150, RJ, A, 97.85, desde='abajo'))
escena('s5-ojo', S, 99.4, 'ii', 'crema', CAB + fz(c1, A, entra=79.5, sale=83.9) + fz(c2, A, entra=83.94, sale=90.67) + fz(c3, A, entra=90.72, sale=96.35)
       + fz(c4, A, entra=96.4))

# ───────────────────────── 1:39 · ¿y el contexto largo? pocos docs: pásalos todos · miles: tokens, tiempo, se pierde a la mitad
S = 99.4; A = B.at(S); s = SCH['amarillo']
f1 = (T(['«Ya aguantan', 'mucho [contexto]»'], A, 99.6, s, size=110)
      + cod('es cierto ✓', 90, 470, A, 102.0, s, b=AZ, c=CR)
      + T(['¿Pocos docs?'], A, 104.96, s, y=600, size=110)
      + ''.join(forma(doc(f'{i + 1}.md', CR, NG, 6, 30), 90 + i * 235, 800, 200, 270, 'transparent', A, 105.1 + i * .1, desde='arriba') for i in range(4))
      + etiqueta('Pásale todos ✓', 90, 1130, A, 107.34, fondo=AZ, color=CR, size=44))
f2 = (T(['¿Y con', '[miles]?'], A, 108.3, s, size=140)
      + numero(N([(0, 5), (108.3, 3000, 1.2)], f='c'), 90, 520, 200, A, 108.3, color=NG)
      + cod('documentos', 95, 700, A, 109.12, s)
      + f'<div style="position:absolute;left:90px;top:800px;width:900px;height:100px;z-index:8;box-shadow:inset 0 0 0 8px {NG};padding:16px">'
        + ap('<i class="tk" style="display:block;height:68px;background:' + RJ + '"></i>', A, 109.7, estilo='position:relative;inset:auto') + '</div>'
      + numero(N([(0, 4), (109.7, 96, 1.4)], suf='%'), 90, 940, 140, A, 109.7, color=RJ)
      + cod('del límite', 480, 990, A, 110.0, s, b=RJ, c=CR)
      + etiqueta('+ tokens', 90, 1140, A, 110.87, fondo=NG, color=AM, size=48)
      + etiqueta('+ tiempo', 440, 1140, A, 112.29, fondo=NG, color=AM, size=48)
      + forma(caja('se pierde<br>a la mitad', RJ, CR, 64), 90, 1260, 640, 240, 'transparent', A, 114.23, desde='izq')
      + forma('medio', 780, 1340, 200, 100, AZ, A, 114.4, desde='der'))
escena('s6-contexto', S, 115.5, 'si', 'amarillo', fz(f1, A, sale=108.2) + fz(f2, A, entra=108.26),
       css=f'.tk{{width:4%;animation:tk 1.4s cubic-bezier(.65,0,.35,1) {A(109.7)} both}}@keyframes tk{{to{{width:96%}}}}')

# ───────────────────────── 1:55 · funciona hoy → si tus datos ya no caben, ponlo a buscar antes de contestar
S = 115.5; A = B.at(S); s = SCH['azul']
f1 = (T(['Funciona', '[hoy]'], A, 115.6, s, size=170)
      + forma(sello('✓', AM, NG, 130), 480, 350, 220, 220, 'transparent', A, 117.92, escala=True, dur=.45)
      + forma(caja('Con los modelos que<br>tenemos <span style="color:#e2352b">en 2026</span>.', CR, NG, 56), 90, 680, 900, 240, 'transparent', A, 116.3, desde='izq')
      + forma('c', 90, 1000, 180, 180, AM, A, 116.5, desde='abajo') + forma('sq', 300, 1000, 180, 180, RJ, A, 116.65, desde='abajo')
      + forma('tri', 510, 1000, 200, 180, CR, A, 116.8, desde='abajo'))
f2 = (T(['¿Ya no', '{caben}?'], A, 119.9, s, size=150)
      + etiqueta('No caben', 640, 230, A, 121.25, fondo=RJ, color=CR, size=44)
      + cod('si <b>datos &gt; chat</b> →', 90, 560, A, 119.9, s)
      + cod('1. busca · 2. contesta', 90, 640, A, 122.0, s)
      + lupa(120, 800, 220, AM, A, 122.93, desde='izq')
      + cod('busca primero', 90, 1100, A, 122.93, s)
      + tri(430, 870, 140, 120, AM, A, 123.4, rot=90, desde='izq')
      + forma(sello('CON-<br>TESTA', CR, NG, 50), 640, 800, 260, 260, 'transparent', A, 123.72, escala=True, dur=.45)
      + cod('luego contesta', 620, 1100, A, 123.72, s))
escena('s7-hoy', S, 124.7, 'id', 'azul', fz(f1, A, sale=119.75) + fz(f2, A, entra=119.82))

# ───────────────────────── 2:04 · resumen para guardar + pregunta
S = 124.7; A = B.at(S); s = SCH['crema']
LISTA = ''.join(forma(caja(f'<span><span class="mono" style="font-size:.8em;margin-right:28px">{n}</span>{t}</span>', c, k, 64, '0 40px'), 90, 640 + i * 170, 900, 140, 'transparent', A, t0,
                      desde='izq' if i % 2 == 0 else 'der')
                for i, (n, t, t0, c, k) in enumerate([('1', 'Prepara', 125.1, RJ, CR), ('2', 'Busca', 125.35, AZ, CR), ('3', 'Contesta', 125.6, AM, NG),
                                                      ('&gt;', '⚠️ Revisa', 126.0, NG, CR)]))
escena('s8-pregunta', S, 128.75, 'c', 'crema',
       T(['¿Le pasas [todo]', 'a tu IA o la pones', 'a {buscar} primero?'], A, 124.9, s, size=84)
       + LISTA + cod('cuéntame 👇', 90, 1340, A, 126.4, s, b=RJ, c=CR, size=40))

# ───────────────────────── 2:08 · cierre: «nos vemos cuando toque actualizar este README»
S = 128.75; A = B.at(S); s = SCH['negro']
escena('s9-cierre', S, FIN, 'sd', 'negro',
       T(['Nos vemos cuando', 'toque [actualizar]', 'este README'], A, 128.8, s, size=92)
       + cod('⌘S <b>README.md</b>', 90, 560, A, 129.0, s, size=44)
       + forma('tri', 90, 760, 260, 230, AZ, A, 129.2, desde='izq')
       + forma('sq', 90, 1010, 220, 220, RJ, A, 129.35, desde='abajo')
       + forma(sello('✓<br>guardado', AM, NG, 52), 560, 800, 380, 380, 'transparent', A, 130.0, escala=True, dur=.45), sigue=False)

# ───────────────────────── franja de arriba (todo el video, transparente): README.md · #02 RAG + sección actual
SECC = [(0.0, '# RAG'), (4.6, '## ¿Qué es?'), (21.85, '## Paso 1 · Prepara'), (34.2, '## Paso 2 · Busca'), (39.25, '## Paso 3 · Contesta'),
        (47.0, '## Libro vs página'), (60.3, '## Mi ejemplo'), (77.3, '&gt; ⚠️ Ojo'), (99.4, '## ¿Y el contexto largo?'), (115.5, '## Funciona hoy'),
        (124.7, '## Tu turno'), (128.75, '✓ guardado')]
A = B.at(0)
SEC = ''.join(ap(f'<span class="sc">{n}</span>', A, t, SECC[i + 1][0] if i + 1 < len(SECC) else None) for i, (t, n) in enumerate(SECC))
ETQ_CSS = f"""
.fr{{position:absolute;left:0;right:0;top:0;height:130px;z-index:90;background:{NG};animation:frIn .5s cubic-bezier(.3,1.3,.45,1) both}}
@keyframes frIn{{from{{transform:translateY(-140px)}}to{{transform:none}}}}
.fr .lg{{position:absolute;left:44px;top:22px;display:flex;align-items:center;gap:10px}}
.fr .lg i{{display:block;width:34px;height:34px}}
.fr .rd{{position:absolute;left:200px;top:14px;font-weight:800;font-size:44px;color:{CR};letter-spacing:-.01em}}
.fr .rd b{{color:{AM};font-weight:800}}
.fr .sc{{position:absolute;left:200px;top:74px;font-family:'JetBrains Mono',monospace;font-weight:500;font-size:32px;color:{AM};white-space:nowrap}}
.fr .nr{{position:absolute;right:44px;top:26px;width:78px;height:78px;border-radius:50%;background:{RJ};color:{CR};font-weight:900;font-size:34px;
  display:flex;align-items:center;justify-content:center}}
"""
ETQ = (f'<div class="fr"><div class="lg"><i style="background:{RJ};border-radius:50%"></i><i style="background:{AM}"></i>'
       f'<i style="background:{AZ};clip-path:polygon(50% 0,100% 100%,0 100%)"></i></div>'
       f'<div class="rd">README.md <b>· #02 RAG</b></div>{SEC}<div class="nr">#02</div></div>')
PIEZAS.append(('etiqueta', 0.0, FIN, B.page(ETQ_CSS, ETQ, FIN, S0=0.0, transparente=True)))
PRE = 'rmb2-'

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
        rel = os.environ.get('REL', 'readme/2/bauhaus')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
