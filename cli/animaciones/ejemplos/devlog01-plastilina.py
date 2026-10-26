"""Devlog 1 · «¿cómo hago mis videos?» (Claude Code + el motor de animaciones) · edición «Plastilina» (claymation).
Es la propuesta B de devlog01-recorte.py (la que eligió Armando) pasada a plastilina: bloques de plastilina en la franja de arriba
(sobre las repisas, sin tapar los monitores; en las tomas de cerca, columna derecha) y dos escenas a pantalla completa para lo que la
cámara no enseña (voz → texto → guion y el tiempo de grabación con dos compus). El logo de Arc de plastilina cae sobre la palma
abierta (posiciones medidas cuadro a cuadro en IMG_5961) y el Sígueme cierra.
Tiempos = timeline final de devlog/1 (154.70 s), anclados a palabras de voz/palabras.json con W().
Uso: SALIDA=~/Documents/Videos/devlog/1/animaciones REL=devlog/1/animaciones python3 ejemplos/devlog01-plastilina.py [ids…]
     (SOLO_HTML=1 solo escribe los HTML; escribe overlays-pl.json, escenas-pl.json y lote-pl.json)
Prefijo de archivos: «dp1-».
"""
import importlib.util, json, os, re, sys, unicodedata
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import plastilina as P
import ellog_gloss as G
from plastilina import letras, bloque, chip, N

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('v10pl', os.path.join(HERE, 'video10-plastilina.py'))
V10 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(V10)
CSS, LIB3D, bt, sb, rw, onoff = V10.CSS, V10.LIB3D, V10.bt, V10.sb, V10.rw, V10.onoff
_spec = importlib.util.spec_from_file_location('v11pl', os.path.join(HERE, 'video11-plastilina.py'))
V11 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(V11)
LIB = V11.LIB          # LIB3D + moneda, engrane, camara, candado

VID = os.path.expanduser('~/Documents/Videos/devlog/1')
OUT = os.path.abspath(os.environ.get('SALIDA', os.path.join(VID, 'animaciones')))
WORK = os.path.join(OUT, '_html-pl'); os.makedirs(WORK, exist_ok=True)   # aparte de los HTML de Recorte (mismos ids)
PRE = 'dp1-'
FIN = 154.70
PIEZAS = []          # (id, inicio, fin, html, pantalla_completa)
C = P.PAS

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


CSS += """
.cm{display:flex;gap:18px;align-items:flex-start}.cm .av{flex-shrink:0;width:64px;height:64px;border-radius:50%;background:var(--c,#9b6bff);color:#fff;
  display:flex;align-items:center;justify-content:center;font-weight:700;font-size:34px;box-shadow:inset 0 -6px 0 rgba(0,0,0,.15)}
.cm small{display:block;font-family:Nunito;font-weight:800;font-size:24px;opacity:.55;margin-bottom:2px}
.code{font-family:Nunito;font-weight:900;line-height:1.35}.code b{color:#e0457b}.code i{font-style:normal;color:#3f6fe0}
.tach{position:relative;display:inline-block}.tach:after{content:'';position:absolute;left:-4%;right:-4%;top:46%;height:.16em;border-radius:99px;background:#ff6b6b;
  transform-origin:left center;transform:scaleX(0) rotate(-3deg);animation:tacha .4s steps(5) var(--t) forwards}
@keyframes tacha{to{transform:scaleX(1) rotate(-3deg)}}
.nav{display:flex;gap:10px;align-items:center;padding:12px 18px;background:#3b3340;border-radius:30px 30px 0 0}
.nav i{width:18px;height:18px;border-radius:50%;background:#ff6b6b}.nav i+i{background:#ffd36b}.nav i+i+i{background:#4cc38a}
.nav b{margin-left:10px;flex:1;background:#5b5160;color:#fff3e3;border-radius:99px;padding:2px 16px;font:800 24px Nunito}
"""


def tach(txt, A, t):
    return f'<span class="tach" style="--t:{A(t)}">{txt}</span>'


def tarjeta(pid, start, end, body, js3d=''):
    """Tarjeta transparente sobre la cámara; al final todo se aplasta contra la mesa (sin desvanecido)."""
    A = P.at(start)
    X = round(end - .55, 2)
    body = f'<div class="fz x" style="--x:{A(X)}">{body}</div>'
    js = (LIB + js3d.replace('XSAL', f'{X}')) if js3d else None
    PIEZAS.append((pid, start, end, P.page(CSS, body, round(end - start, 2), S0=start, transparente=True, js3d=js), False))


def fase(html, A, sale=None):
    """Grupo de piezas de una escena; al acabar su fase se aplasta contra la mesa."""
    return f'<div class="fz x" style="--x:{A(sale)}">{html}</div>' if sale is not None else f'<div class="fz">{html}</div>'


def escena(pid, S, E, body, js3d, fondo, ac):
    """Escena a pantalla completa: entra con mancha de plastilina y al salir la mancha se recoge hacia el centro (mismo patrón que
    video11-plastilina.py: la salida va suave a 30 cps)."""
    DS = round(E - S, 2)
    css = (CSS + f'body .mesa{{animation:mancha .65s steps(8) both,recoge .45s cubic-bezier(.45,0,.75,1) {DS - .5:.2f}s forwards}}'
           '@keyframes recoge{from{clip-path:circle(1110px at 540px 960px)}to{clip-path:circle(0px at 540px 960px)}}')
    html = P.page(css, body, DS, S0=S, fondo=fondo, entra=(540, 1300), ac=ac, js3d=LIB + js3d)
    html = html.replace('</body>', "<script>{const _s=window.__seek;window.__seek=s=>{_s(s);for(const a of document.getAnimations())"
                        "if(a.animationName==='recoge'){a.pause();a.currentTime=s*1000}};"
                        f"window.__liso=[[{DS - .52:.2f},{DS:.2f}]];window.__seek(0)}}</script></body>")
    PIEZAS.append((pid, S, E, html, True))


# Zonas libres de la cámara: tomas 5957–5960 y 5967–5968 (monitor lejos) → franja de arriba hasta y≈560; tomas 5962–5964 (cerca, la
# vista previa del editor ocupa x 240–520) → columna derecha x 570–1040; toma 5965 (modo comparar a todo lo ancho) → franja y 150–430.

# ───────── 0:00 · gancho · «Todas esas animaciones las hizo Claude y tú puedes tener un video así sin saber editar»
S = 0.0; A = P.at(S)
tarjeta('c01-gancho', S, 5.40,
        bloque(60, 190, 700, bt('Todo esto lo animó', 76) + bt('Claude ✨', 104, 'color:#e0457b'), A, W('todas'), color=C['blanco'])
        + bloque(560, 520, 440, bt('✂️ sin editar', 56, 'white-space:nowrap'), A, W('editar'), color=C['limon']),
        r"""const e=engrane(80,'#9b6bff');scene.add(e);
return t=>{C.brota(e,t,""" + f'{W("animaciones") + .3}' + r""");C.aplasta(e,t,XSAL);P3(e,860,330,2,t,1,.2,-.3,-t*1.6)}""")

# ───────── 0:05 · «si ya usas Claude Code, es completamente gratis: clonas mi repo, le dices que lea el README y le pides un video»
S = 5.35; A = P.at(S)
T_CLONA = W('clonas')
PASOS = [('<i>$</i> git clone <b>Arzival/videoAssembler</b>', T_CLONA), ('<i>›</i> lee el README', W('dices')), ('<i>›</i> créame un video 🎬', W('pides'))]
tarjeta('c02-repo', S, 16.70,
        bloque(60, 190, 560, bt('¿Ya usas Claude Code?', 56), A, W('usas'), sale=T_CLONA - .55, color=C['durazno'])
        + bloque(640, 200, 380, bt('100% gratis', 64, 'color:#2f9e6a'), A, W('gratis'), sale=T_CLONA - .55, color=C['menta'])
        + bloque(60, 190, 960, ''.join(rw(f'<div class="code" style="font-size:40px">{tx}</div>', A, t) for tx, t in PASOS), A, T_CLONA - .1, color=C['blanco']))

# ───────── 0:17 · «Me han preguntado cómo es que hago mis videos y sí, uso Claude Code, pero ojo, Claude Code no edita solamente a mano»
S = 16.75; A = P.at(S)
Q1 = ('<div class="cm"><div class="av">G</div><div><small>comentario · hace 2 d</small>'
      '<div class="bt" style="font-size:44px">«Bro, ¿cómo haces esos videos? ¿Usas Claude?»</div></div></div>')
tarjeta('c03-pregunta', S, 23.95,
        bloque(60, 180, 720, Q1, A, W('preguntado'), color=C['blanco'])
        + bloque(560, 440, 460, bt('✅ sí: Claude Code', 50, 'white-space:nowrap'), A, W('uso'), color=C['menta'])
        + bloque(60, 440, 440, bt('pero ojo 👀', 64, 'white-space:nowrap'), A, W('ojo'), color=C['limon']))

# ───────── 0:24 · «Yo solo grabo mis tomas con el teléfono y también mi voz. Ya después le digo qué video es el que quiero, reviso y apruebo»
S = 24.05; A = P.at(S)
MIO = [('📱 grabo mis tomas', W('grabo')), ('🎙️ grabo mi voz', W('voz')), ('🗣️ le digo qué video', W('digo')), ('✅ reviso y apruebo', W('reviso'))]
tarjeta('c04-mio', S, 31.45,
        bloque(60, 180, 640, sb('mi parte', 34) + ''.join(rw(bt(tx, 50, 'margin-top:8px;white-space:nowrap'), A, t) for tx, t in MIO), A, MIO[0][1] - .3,
               color=C['blanco'])
        + bloque(730, 420, 300, bt('solo esto', 52, 'white-space:nowrap'), A, W('apruebo') + .1, color=C['rosa']),
        r"""const cm=camara(150);scene.add(cm);
return t=>{C.cae(cm,t,""" + f'{W("grabo") + .2}' + r""",520);C.aplasta(cm,t,XSAL);P3(cm,880,300,2.5,t,1,.3,-.5,.05)}""")

# ───────── 0:31 · ESCENA · voz → texto → silencios y errores → guion con palabras («el logo de Arc entra cuando digo Arc»)
S = 31.55; A = P.at(S)
T_Q, T_D = W('quita'), W('despues', 1, 42)
PAL = [(f'[{W(p, n, 31):05.2f}] {p}', W(p, n, 31) + .1) for p, n in (('palabra', 1), ('por', 1), ('palabra', 2))]
TOMAS = [('«Primero Claude pasa mi voz… y eso ocurre»', 'intento 1'), ('«Primero Claude pasa mi voz… las equivocaciones»', 'intento 2'),
         ('«Primero Claude pasa mi voz a texto»', 'el bueno ✓')]
T_ERR = W('errores')
F1 = (letras(['Tu voz', '→ *texto*'], A, W('primero'), top=260, size=170)
      + bloque(70, 700, 640, ''.join(rw(f'<div class="code" style="font-size:52px">{tx}</div>', A, t) for tx, t in PAL), A, W('texto', 1, 31), color=C['blanco'])
      + bloque(70, 1180, 660, bt('🔒 100% en mi compu', 60, 'white-space:nowrap'), A, W('propia'), color=C['cielo']))
F2 = (letras(['Quita *silencios*', 'y *errores*'], A, T_Q, top=260, size=130)
      + ''.join(bloque(70, 640 + i * 250, 940, bt(tach(tx, A, T_ERR + i * .4) if i < 2 else tx, 46) + sb(et, 32), A, W('silencios') + i * .35,
                       color=C['blanco'] if i < 2 else C['menta']) for i, (tx, et) in enumerate(TOMAS))
      + bloque(250, 1430, 620, bt('en este mismo video 😅', 52, 'white-space:nowrap'), A, W('grabar') + .2, color=C['limon']))
GUION = [('{ <b>"plantilla"</b>: "logo",', W('guion') + .2), ('&nbsp;&nbsp;<b>"logo"</b>: "arc",', W('animacion') + .1),
         ('&nbsp;&nbsp;<b>"entra"</b>: {"palabra": <i>"Arc"</i>} }', W('cada') + .1)]
F3 = (letras(['Escribe el', '*guion*'], A, T_D + .2, top=260, size=170)
      + bloque(60, 700, 960, ''.join(rw(f'<div class="code" style="font-size:44px;white-space:nowrap">{tx}</div>', A, t) for tx, t in GUION), A, W('guion'),
               color=C['blanco'])
      + bloque(90, 1080, 760, bt('entra justo en esa palabra 👇', 52, 'white-space:nowrap'), A, W('justo'), color=C['limon']))
ARC3D = ("const arc=C.grupo();const disco=C.cil(120,46,'#ff6b6b');disco.rotation.x=Math.PI/2;arc.add(disco);"
         f"const al=C.logo({json.dumps(G.svgpath('arc'))},150,'#fff8ef',30);al.position.z=C.u(30);arc.add(al);")
escena('e1-voz', S, 51.95,
       fase(F1, A, T_Q - .55) + fase(F2, A, T_D - .55) + fase(F3, A),
       r"""const H=[];for(let i=0;i<3;i++){const h=hojita(120,['#fff8ef','#ffe3ea','#e1f1ff'][i]);scene.add(h);H.push(h)}
const lp=laptop(230,'#d9d4dc','#9fd3ff');scene.add(lp);
""" + ARC3D + r"""scene.add(arc);
return t=>{H.forEach((h,i)=>{C.cae(h,t,""" + f'{W("texto", 1, 31)}' + r"""+i*.25,600);C.aplasta(h,t,""" + f'{T_Q - .55}' + r""");P3(h,820+i*40,800+i*70,2+i*.3,t,i,.15,-.35,(i-1)*.12)});
 C.cae(lp,t,""" + f'{W("computadora") - .2}' + r""",520);C.aplasta(lp,t,""" + f'{T_Q - .55}' + r""");abre(lp,1);P3(lp,880,1480,2,t,5,.42,-.45,0);
 C.cae(arc,t,""" + f'{W("ark") - .1}' + r""",600);P3(arc,780,1450,3,t,7,.2,-.25,-.15)}""", 'cielo', '#3f6fe0')

# ───────── 0:52 · el logo de Arc de plastilina cae en la palma abierta «cuando yo digo ARC» (IMG_5961, medido cuadro a cuadro)
T_ARC = W('ark', 2)
S = round(T_ARC - .35, 2); E = 53.90; A = P.at(S)
CAMINO = [(S, 760, 1170), (53.00, 760, 1170), (53.30, 768, 1185), (53.45, 765, 1180), (53.60, 772, 1190), (53.72, 790, 1215), (53.90, 860, 1330)]
js = (ARC3D + 'scene.add(arc);const K=' + json.dumps(CAMINO) + r""";
const pos=t=>{let i=0;while(i<K.length-2&&t>K[i+1][0])i++;const [a,x0,y0]=K[i],[b,x1,y1]=K[i+1];const p=Math.min(1,Math.max(0,(t-a)/(b-a)));return [x0+(x1-x0)*p,y0+(y1-y0)*p]};
return t=>{C.cae(arc,t,""" + f'{T_ARC - .2}' + r""",420,.45);C.aplasta(arc,t,53.68,.25);const [x,y]=pos(t);P3(arc,x,y+20,3,t,1,.3,-.2,-.15)}""")
html = P.page(CSS, '', round(E - S, 2), S0=S, transparente=True, js3d=LIB + js).replace('const _Q=1000/12', 'const _Q=1000/60')
PIEZAS.append(('m-arc', S, E, html, False))

# ───────── 0:54 · «Claude no escribe código nuevo en cada video, solo va cambiando los datos que están mostrándose en pantalla» (columna derecha)
S = 53.95; A = P.at(S)
VALS = [('"Arc se apaga"', W('datos') - .8), ('"PHP2Shell"', W('datos') + .2), ('"RAG"', W('pantalla'))]
v = ''.join(onoff(tx, A, t, VALS[i + 1][1] if i + 1 < len(VALS) else None, 'position:absolute;left:0;top:0;white-space:nowrap') for i, (tx, t) in enumerate(VALS))
tarjeta('c05-datos', S, 62.45,
        bloque(580, 170, 440, bt(tach('código nuevo', A, W('nuevo') + .2), 60, 'white-space:nowrap'), A, W('codigo') - .1, color=C['rosa'])
        + bloque(580, 360, 440, f'<div class="code" style="font-size:36px"><b>"titulo"</b>:</div>'
                 f'<div class="code" style="font-size:40px;position:relative;height:56px;color:#3f6fe0">{v}</div>', A, W('datos') - .9, color=C['blanco'])
        + bloque(580, 580, 440, bt('solo cambian los datos ✓', 40, 'white-space:nowrap;color:#2f9e6a'), A, W('datos') + .1, color=C['menta']))

# ───────── 1:02 · «cada animación es una página web y un navegador escondido graba cada video con transparencia»
S = 62.5; A = P.at(S)
WIN = ('<div class="nav"><i></i><i></i><i></i><b>escena.html</b></div><div style="padding:18px 26px">'
       + bt('Arc se apaga', 54, 'white-space:nowrap') + '</div>')
tarjeta('c06-web', S, 71.7,
        bloque(580, 170, 440, WIN, A, W('pagina'), color=C['blanco'], extra='padding:0;overflow:hidden')
        + bloque(600, 400, 400, bt('= una página web', 44, 'white-space:nowrap'), A, W('web'), color=C['limon'])
        + bloque(600, 560, 420, bt('🎥 .webm', 60) + sb('con transparencia', 30), A, W('transparencia') - .3, color=C['lila']))

# ───────── 1:12 · «Al principio estaba ocupando HyperFrames, pero tomé esa idea base y terminé construyendo este motor de animaciones»
S = 71.75; A = P.at(S)
Q2 = ('<div class="cm" style="--c:#4cc38a"><div class="av">M</div><div><small>comentario</small>'
      '<div class="bt" style="font-size:42px">«¿Claude + HyperFrames?»</div></div></div>')
tarjeta('c07-motor', S, 81.15,
        bloque(570, 170, 470, Q2, A, W('hyperframes') - .5, color=C['blanco'])
        + bloque(600, 400, 420, bt('💡 la idea base', 48, 'white-space:nowrap'), A, W('idea'), color=C['limon'])
        + bloque(600, 560, 420, bt('motor propio', 56, 'white-space:nowrap;color:#e0457b'), A, W('motor'), color=C['rosa']),
        r"""const e=engrane(70,'#ff9f43');scene.add(e);
return t=>{C.brota(e,t,""" + f'{W("motor") + .3}' + r""");C.aplasta(e,t,XSAL);P3(e,960,720,2,t,1,.2,-.3,-t*1.8)}""")

# ───────── 1:21 · «antes de renderizarlo lo veo en vivo en el editor; con el modo de comparar puedo ver hasta 4 videos a la vez»
S = 81.25; A = P.at(S)
tarjeta('c08-vivo', S, 89.45,
        bloque(600, 180, 420, bt('🔴 en vivo', 60, 'white-space:nowrap') + sb('sin renderizar nada', 30), A, W('vivo'), color=C['blanco'])
        + bloque(600, 420, 420, sb('modo comparar', 32) + bt(f'{N([(0, 1), (W("4"), 4, .5)])} videos', 92, 'white-space:nowrap;color:#3f6fe0')
                 + sb('a la vez', 30), A, W('comparar'), color=C['cielo']))

# ───────── 1:30 · «El Log lleva unas 140 animaciones; desde que grabo el audio hasta la parte final, unos 45 minutos» (franja de arriba)
S = 89.5; A = P.at(S)
tarjeta('c09-numeros', S, 101.95,
        bloque(60, 160, 450, sb('El Log lleva', 34) + bt(f'~{N([(0, 0), (W("140"), 140, 1.0)])}', 120, 'color:#ff6b6b') + sb('animaciones', 30),
               A, W('log') - .1, color=C['blanco'])
        + bloque(560, 165, 460, sb('del audio al video', 34) + bt(f'{N([(0, 0), (W("45") - .4, 45, .8)])} min', 120, 'color:#3f6fe0;white-space:nowrap'),
                 A, W('45') - .4, color=C['blanco']))
S = 102.05; A = P.at(S)
tarjeta('c10-rapido', S, 104.5, bloque(60, 180, 620, bt('Para ir más rápido… 🏃', 60, 'white-space:nowrap'), A, W('para', 1, 102), color=C['limon']))

# ───────── 1:44 · «ocupo las dos computadoras: lo que estamos viendo aquí es la Mac… y la Legion que forma parte de mi homelab»
S = 104.55; A = P.at(S)
tarjeta('c11-compus', S, 112.70,
        bloque(50, 170, 330, bt('2 compus', 66, 'white-space:nowrap'), A, W('dos', 1, 104), color=C['blanco'])
        + bloque(420, 180, 290, bt('🍎 Mac', 64, 'white-space:nowrap') + sb('esta 👇', 32), A, W('mac', 1, 105), color=C['cielo'])
        + bloque(740, 170, 300, bt('Legion', 64) + sb('en mi homelab', 30), A, W('legion'), color=C['lila']))

# ───────── 1:53 · ESCENA · «Antes la grabación tardaba unos 9 minutos… ahora, dividiéndolo entre las dos computadoras, unos 2 minutos y medio»
S = 112.75; A = P.at(S)
BAR = lambda w, col, t: f'<div class="br" style="width:{w}px;height:90px;background:{col};--d:{A(t)}"></div>'
escena('e2-granja', S, 124.45,
       letras(['Grabar las', '*animaciones*'], A, W('grabacion') - .3, top=260, size=140)
       + bloque(70, 640, 940, bt('antes · solo la Mac', 58) + f'<div style="display:flex;align-items:center;gap:24px;margin-top:16px">{BAR(560, C["negro"], W("9"))}'
                + rw(bt('9 min', 92), A, W('9') + .6) + '</div>', A, W('9') - .5, color=C['blanco'])
       + bloque(70, 1000, 940, bt('ahora · Mac + Legion', 58) + f'<div style="display:flex;align-items:center;gap:24px;margin-top:16px">{BAR(160, C["verde"], W("2"))}'
                + rw(bt('2.5 min', 92, 'color:#2f9e6a'), A, W('2') + .6) + '</div>', A, W('2') - .5, color=C['blanco'])
       + bloque(170, 1400, 740, bt('⚡ 3.5× más rápido', 76, 'white-space:nowrap'), A, W('promedio') - .2, color=C['limon']),
       r"""const a=laptop(200,'#d9d4dc','#9fd3ff');scene.add(a);const b=laptop(200,'#3b3340','#9b6bff');scene.add(b);
return t=>{C.cae(a,t,""" + f'{W("9") - .4}' + r""",520);abre(a,1);P3(a,880,560,2,t,1,.42,-.45,0);
 C.cae(b,t,""" + f'{W("dos", 1, 119)}' + r""",520);abre(b,1);P3(b,880,940,2,t,2,.42,-.45,0)}""", 'menta', '#2f9e6a')

# ───────── 2:04 · «Claude hace el trabajo pesado, pero yo tengo que estar revisando el video completo… darle el visto bueno y que se ponga a renderizar»
S = 124.5; A = P.at(S)
tarjeta('c12-revisa', S, 138.7,
        bloque(60, 190, 440, bt('Claude 🤖', 66) + sb('el trabajo pesado', 32), A, W('cloud', 1, 126) - .2, color=C['cielo'])
        + bloque(540, 190, 480, bt('Yo 👀', 66) + sb('reviso todo el video', 32), A, W('revisando'), color=C['rosa'])
        + bloque(280, 440, 520, bt('✅ visto bueno', 60, 'white-space:nowrap'), A, W('visto'), color=C['menta']))

# ───────── 2:18 · «…recuerda que el repo es 100% gratis. Te lo dejo en el link que tienes en mi biografía»
S = 138.75; A = P.at(S)
tarjeta('c13-gratis', S, 147.05,
        bloque(60, 190, 820, '<div class="code" style="font-size:40px;white-space:nowrap">github.com/<b>Arzival</b>/videoAssembler</div>', A, W('repo', 2) - .3,
               color=C['blanco'])
        + bloque(560, 360, 420, bt('100% gratis', 66, 'white-space:nowrap;color:#2f9e6a'), A, W('100%'), color=C['menta'])
        + bloque(60, 360, 420, bt('🔗 link en mi bio', 50, 'white-space:nowrap'), A, W('link'), color=C['limon']))

# ───────── 2:27 · Sígueme + «¿qué video harías tú, ahora que la IA lo puede animar?» (mismo patrón que video11-plastilina.py)
S = 147.20; A = P.at(S)
_r = 'Mi tutorial… ¡sin editar! 🎬'
BOTON = (f'<div style="position:relative;height:64px;margin-top:14px">'
         + onoff(f'<span class="chip" style="--b:#ff6b6b;color:#fff;animation:none">Seguir</span>', A, W('animar'), W('animar') + .8, 'position:absolute;left:0;top:0')
         + onoff(f'<span class="chip" style="--b:#a8e6cf;animation:none">Siguiendo ✓</span>', A, W('animar') + .8, None, 'position:absolute;left:0;top:0') + '</div>')
SEG = (bloque(600, 190, 420, sb('Sígueme', 34) + bt('Armando', 80) + sb('homelab · IA · código', 30) + BOTON, A, S + .2, color=C['rosa'])
       + bloque(60, 240, 500, bt('🎬 ¿Qué video harías tú si la IA lo anima?', 46)
                + rw(f'<div class="sb" style="font-size:34px;margin-top:10px;color:#3f6fe0;opacity:1">{_r}</div>', A, W('animar') + .9), A, W('que', 1, 147.5),
                color=C['blanco']))
PIEZAS.append(('seguir', S, FIN, P.page(CSS, SEG, round(FIN - S, 2), S0=S, transparente=True), False))

PIEZAS.sort(key=lambda p: p[1])

if __name__ == '__main__':
    solo = set(sys.argv[1:])
    lote = []
    for pid, a, b, html, _ in PIEZAS:
        if solo and pid not in solo:
            continue
        path = f'{WORK}/{pid}.html'
        open(path, 'w').write(html)
        print('html', pid, f'{a:7.2f}–{b:7.2f}')
        lote.append(dict(html=path, dur=round(b - a, 2), out=f'{OUT}/{PRE}{pid}.webm'))
    json.dump(lote, open(f'{OUT}/lote-pl.json', 'w'), indent=1)
    if not solo:
        rel = os.environ.get('REL', 'devlog/1/animaciones')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'html': f'{rel}/_html-pl/{pid}.html', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0,
                'scale': 1, 'position': 'center'} for pid, a, b, _, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays-pl.json', 'w'), indent=2, ensure_ascii=False)
        json.dump([[a, b] for _, a, b, _, full in PIEZAS if full], open(f'{OUT}/escenas-pl.json', 'w'))
        print('overlays-pl.json · escenas-pl.json')
