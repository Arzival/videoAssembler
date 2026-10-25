"""El Log #06 · diseño «Trayecto» (gloss 2 + widget oscuro de ruta) con la cinta de noticiero arriba.
Reutiliza de ellog-04-trayecto.py la tarjeta de ruta (tray, baraja, TCSS, TRJS) y de ellog-04-destino.py la cinta y el 3D base.
Tiempos = voz recortada de noticias/6 (voz/voz-norm.wav, 139.62 s). Necesita internet al capturar.
Uso: SALIDA=noticias/6/animaciones REL=noticias/6/animaciones python3 ejemplos/ellog-06-trayecto.py [ids…]   (SOLO_HTML=1 para revisar)
"""
import importlib.util, json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import ellog_gloss as G
from ellog_gloss import js

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('trayecto', os.path.join(HERE, 'ellog-04-trayecto.py'))
T = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(T)
D = T.D
tray, baraja, K, sw, BG, TOP = T.tray, T.baraja, T.K, T.sw, T.BG, T.TOP
TX, TW, TK, CYT = T.TX, T.TW, T.TK, T.CYT

CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.getcwd()))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
FIN = 139.62

# la cinta del módulo base se arma con estos datos
D.FIN = FIN
D.NOTICIAS = [(0.0, 2, '01', 'Un agente de OpenAI usó una cartera ajena'),
              (31.04, 1, '02', 'App Store prohíbe los deepfakes íntimos'),
              (69.4, 'amb', '03', 'Así revisa código el equipo de Claude Code'),
              (108.32, 4, '04', 'Anthropic: menos junior y más reuniones'),
              (129.06, 0, '✓', '¿Le darías tu cartera a un agente?')]
D.CORRIDO = ['OpenAI: el agente revisó 362 carteras con frases de recuperación públicas', 'Red de prueba Sepolia: los tokens no tenían valor real',
             'El agente no avisó que había usado una cartera ajena', 'Apple: nueva regla 2.5.19 contra apps que esconden funciones tras la revisión',
             'Quien rompa las reglas puede perder su app y su cuenta de desarrollador', 'Claude Code: de 2,500 a más de 30,000 cambios al día en su monorepo',
             'Reverts: más de 40 % menos entre junio y septiembre', 'Anthropic: técnicos junior bajan de 21 % a 14 %',
             'Las horas de agentes ya son 6× las de sus empleados']

# piezas 3D nuevas: ethereum y candado
LIB = D.LIB + r"""
R.eth=(h)=>{const G=R.group(),r=h*.42;const top=new THREE.Mesh(new THREE.ConeGeometry(R.u(r),R.u(h*.62),4),R.iri('#c9c0ff',{metalness:.6,roughness:.1,opacity:1,transparent:false,emissive:'#5b4bd6',emissiveIntensity:.25,flatShading:true}));
 top.position.y=R.u(h*.31);G.add(top);const bot=new THREE.Mesh(new THREE.ConeGeometry(R.u(r),R.u(h*.38),4),R.iri('#8f84f0',{metalness:.6,roughness:.12,opacity:1,transparent:false,emissive:'#3a2bb0',emissiveIntensity:.3,flatShading:true}));
 bot.rotation.x=Math.PI;bot.position.y=R.u(-h*.19);G.add(bot);return G};
R.lock=(w)=>{const G=R.group();G.add(R.rbox(w,w*.8,w*.34,w*.12,R.metal('#ffcf4d',{roughness:.2})));
 const sh=new THREE.Mesh(new THREE.TorusGeometry(R.u(w*.29),R.u(w*.07),20,48,Math.PI),R.metal('#e8ecf3',{roughness:.15}));sh.position.y=R.u(w*.4);G.add(sh);
 const kh=new THREE.Mesh(new THREE.CylinderGeometry(R.u(w*.07),R.u(w*.07),R.u(w*.05),24),R.gloss('#1b1e26'));kh.rotation.x=Math.PI/2;kh.position.set(0,R.u(w*.04),R.u(w*.18));G.add(kh);
 G.userData.sh=sh;return G};
"""

PIEZAS = []


def escena(pid, start, end, n, css, body, js3d=None, sigue=True):
    if sigue:
        end += G.COLA
    PIEZAS.append((pid, start, end, G.page(T.TCSS + css, T.RGDEF + body, end - start, f'const S0={start};' + T.TRJS, n=n, js3d=js3d, salida=not sigue, t0=start)))


def st(items, S, size=88):
    return G.steps(items, S, top=TOP, size=size)


def fase(n, a, b=None):
    return T.fase(n, a, b)


def gl(name, color='#fff'):
    return G.logo(name, color)


def em(e):
    return f'<span class="em">{e}</span>'


def N(keys, f='', suf=''):
    """Contador animado (data-n)."""
    return f'<b data-n=\'{keys}\'' + (f' data-f="{f}"' if f else '') + (f' data-suf="{suf}"' if suf else '') + '>0</b>'


def below(html, top, t, A, cls='pill on', extra=''):
    return f'<div class="below" style="top:{top}px"><span class="{cls} stamp" style="font-size:40px;{extra}animation-delay:{A(t)}">{html}</span></div>'


SIG = {  # próximas paradas (píldoras de atrás)
    1: [('🍎', 'App Store', '0:31', 1), ('🔍', 'Revisión de código', '1:09', 'amb')],
    2: [('🔍', 'Revisión de código', '1:09', 'amb'), ('👥', 'Anthropic por dentro', '1:48', 4)],
    3: [('👥', 'Anthropic por dentro', '1:48', 4), ('💬', 'Tu opinión', '2:09', 0)],
    4: [('💬', 'Tu opinión', '2:09', 0)],
}
VIO = BG.format(a='#e9e0ff', b='#8c7cf0')
GRIS = BG.format(a='#3a3a44', b='#121218')
CORAL = BG.format(a='#ffd9cc', b='#ff8a6b')
AMB = BG.format(a='#ffe6c2', b='#ffb340')
CIAN = BG.format(a='#d3f4ff', b='#4fd2ff')

# ───────── 0:00 · #01 el agente de OpenAI: revisó 362 carteras hasta dar con una con fondos; luego «dale lo mínimo»
S = 0.0; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 2, 0.2, A, gl('openai'), 'Agente de investigación', ring=(N(K((0, 0), (4.9, 362, 1.6))), K((0, 0), (2.6, 30, .6), (4.9, 100, 1.6))),
          btn=('Siguiente', 7.0),
          mL=('Revisó', N(K((0, 0), (4.9, 362, 1.6))) + ' carteras', 4.9), mR=('Y tomó', '<b>ETH</b> ajeno', 5.0),
          bar=K((0, 0), (2.6, 30, .6), (4.9, 100, 1.6)),
          cols=[('Tarea', 'smart contracts', 5.8), ('Faucets', '✕ sin fondos', 6.2), ('Al final', 'cartera ajena', 6.6)],
          stops=[('Le pidieron', 'actualizar una app', 5.7), ('En la red', 'Ethereum Sepolia', 6.4)],
          thumbs=[('◆', VIO, 5.0), ('💻', BG.format(a='#dbe8ff', b='#6ea8ff'), 5.8)])
c2 = tray(TX, CYT, TW, TK, 'gris', 7.8, A, em('🔐'), 'Si le das acceso', ring=(N(K((0, 0), (13.45, 1, .3), (15.26, 2, .3))) + '/2', K((0, 0), (13.45, 50, .5), (15.26, 100, .5))),
          btn=('Siguiente', 19.4),
          mL=('Permisos', '<b>mínimos</b>', 12.9), mR=('Entorno', '<b>aislado</b>', 14.7),
          bar=K((0, 0), (13.45, 50, .6), (15.26, 100, .6)),
          cols=[('Credenciales', 'solo las justas', 10.0), ('', '', None), ('Cartera', 'con lo mínimo', 11.3)],
          stops=[('Con tal de', 'cumplir el objetivo', 16.8), ('Se puede', 'saltar los límites', 18.4)],
          thumbs=[('🔑', AMB, 10.0), ('👛', VIO, 11.3)])
escena('e00-cartera', S, 19.94, 2, fase(1, 0, A(7.4)) + fase(2, A(7.5)),
       f"""<div class="p1">{st([('Un agente de <em>OpenAI</em>', 0.3, 4.7), ('Tomó <em>Ethereum</em><br>que no era suyo', 4.8, None)], S, 88)}{baraja(CYT, TK, A, 0.6, SIG[1])}{c1}</div>
<div class="p2">{st([('¿Le das <em>acceso</em>?', 7.7, 12.0), ('Dale lo <em>mínimo</em>', 12.1, 16.0), ('Se puede <em>saltar</em><br>los límites', 16.1, None)], S, 86)}{baraja(CYT, TK, A, 7.9, SIG[1])}{c2}</div>""",
LIB + r"""const et=R.eth(300);R.scene.add(et);const lk=R.lock(230);R.scene.add(lk);const SH=lk.userData.sh;
return t=>{const a=R.eb(R.k(t,.6,.9)),o=R.eo(R.k(t,7.0,.4)),b=R.eb(R.k(t,10.2,.8)),cl=R.eio(R.k(t,13.4,.4)),op=R.eb(R.k(t,18.3,.5));
 et.visible=t<7.5;et.scale.setScalar(Math.max(.001,a*(1-o)));R.at(et,540,1650+12*Math.sin(t*1.6),2);et.rotation.set(.12*Math.sin(t*1.1),(1-a)*3+t*.9+(t>4.9?R.eio(R.k(t,4.9,1.2))*4:0),0);
 lk.visible=t>10;lk.scale.setScalar(Math.max(.001,b));R.at(lk,540,1660+10*Math.sin(t*1.4),2);lk.rotation.set(.15+.05*Math.sin(t*1.2),(1-b)*3+.45*Math.sin(t*.9),0);
 SH.position.y=R.u(230*(.4+.22*(1-cl)+.3*op));SH.rotation.y=op*.9}""")

# ───────── 0:20 · #01 (parte 2): era de prueba… pero entró a una cartera ajena
S = 19.94; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 2, 20.1, A, em('🧪'), 'Ojo: era una prueba', ring=('test', K((0, 0), (21.1, 100, 1.0))),
          btn=('Siguiente', 30.5),
          mL=('Modelo de', '<b>investigación</b>', 21.1), mR=('Dinero real', '<b>$0</b>', 24.0),
          bar=K((0, 0), (22.3, 60, .8), (24.4, 100, .6)),
          cols=[('Fecha', '26 jun', 21.3), ('Tokens', 'de prueba', 22.6), ('Red', 'Sepolia', 22.9)],
          stops=[('Le pidieron', 'una tarea de código', 25.8), ('Y acabó en', 'una cartera ajena', 29.3)],
          thumbs=[('💻', BG.format(a='#dbe8ff', b='#6ea8ff'), 27.3), ('👛', VIO, 30.0)])
escena('e01-prueba', S, 31.04, 2, '',
       f"""<div class="p1">{st([('Ojo: era <em>de prueba</em>', 20.0, 25.2), ('Pero entró a una<br>cartera <em>ajena</em>', 25.3, None)], S, 88)}{baraja(CYT, TK, A, 20.3, SIG[1])}{c1}
 {below('💸 no era dinero real', 1420, 24.3, A, 'pill ok', '--r:-3deg;')}</div>""",
LIB + r"""const et=R.eth(260);R.scene.add(et);
return t=>{const a=R.eb(R.k(t,20.4,.9)),w=R.k(t,29.6,.6),sh=w>0&&w<1?Math.sin(t*40)*.08:0;et.scale.setScalar(Math.max(.001,a));
 R.at(et,540,1740+12*Math.sin(t*1.5),2);et.rotation.set(.1*Math.sin(t*1.1),(1-a)*3+t*.8,sh)}""")

# ───────── 0:31 · #02 App Store: regla 1.2 contra las imágenes íntimas sin consentimiento; luego prevenir y eliminar
S = 31.04; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 1, 31.2, A, gl('apple'), 'App Store · regla 1.2', ring=('1.2', K((0, 0), (33.9, 100, 1.0))),
          btn=('Siguiente', 42.6),
          mL=('Prohíbe', 'apps <b>con IA</b>', 34.0), mR=('Sin', '<b>consentimiento</b>', 41.35),
          bar=K((0, 0), (34.0, 60, 1.6), (41.4, 100, .8)),
          cols=[('Publicado', '16 oct', 34.6), ('Regla', '1.2 contenido', 35.9), ('Y la nueva', '2.5.19', 36.4)],
          stops=[('Que generan', 'imágenes íntimas', 39.8), ('De', 'personas reales', 40.5)],
          thumbs=[('🚫', CORAL, 39.8), ('👤', CORAL, 40.5)])
c2 = tray(TX, CYT, TW, TK, 1, 43.2, A, em('🧑‍💻'), 'Ahora los desarrolladores', ring=(N(K((0, 0), (45.87, 1, .3), (46.48, 2, .3))) + '/2', K((0, 0), (45.87, 50, .5), (46.48, 100, .5))),
          btn=('Siguiente', 49.8),
          mL=('Deben', '<b>prevenir</b>', 45.87), mR=('Y también', '<b>eliminar</b>', 46.48),
          bar=K((0, 0), (45.87, 50, .5), (46.48, 100, .5)),
          cols=[('Qué', 'deepfakes', 47.3), ('Dónde', 'en su app', 48.8), ('Si no', 'pierden la cuenta', 49.3)])
escena('e02-appstore', S, 50.28, 1, fase(1, 0, A(42.8)) + fase(2, A(42.9)),
       f"""<div class="p1">{st([('La <em>App Store</em><br>se pone estricta', 31.2, None)], S, 86)}{baraja(CYT, TK, A, 31.5, SIG[2])}{c1}</div>
<div class="p2">{st([('Y no solo <em>eso</em>', 43.1, 47.0), ('Fuera los <em>deepfakes</em>', 47.1, None)], S, 88)}{baraja(CYT, TK, A, 43.3, SIG[2])}{c2}</div>""",
LIB + "const AP=" + js(G.svgpath('apple')) + ",SH=" + js(D.SHIELD) + r""";
const ap=R.shape(AP,230,3,R.metal('#d9dbe2',{roughness:.14}),.5);R.scene.add(ap);
const sh=R.shape(SH,230,5,R.gloss('#8d96a8',{emissive:'#3ee08a',emissiveIntensity:0,roughness:.16}));R.scene.add(sh);
return t=>{const a=R.eb(R.k(t,31.6,.9)),o=R.eo(R.k(t,42.5,.4)),b=R.eb(R.k(t,43.6,.8)),g=R.k(t,46.48,.5);
 ap.visible=t<43;ap.scale.setScalar(Math.max(.001,a*(1-o)));R.at(ap,540,1650+10*Math.sin(t*1.4),1);ap.rotation.set(.15,(1-a)*3+.5*Math.sin(t*.8),0);
 sh.visible=t>43.4;sh.scale.setScalar(Math.max(.001,b));R.at(sh,540,1650,2);sh.rotation.set(.15,(1-b)*3+.4*Math.sin(t*1.1),0);
 sh.material.color.set(g>.5?'#9ff0c2':'#8d96a8');sh.material.emissiveIntensity=.4*g}""")

# ───────── 0:50 · #02 (parte 2): después de Grok en X; si tu app genera imágenes → filtros, reporte, revisión
S = 50.28; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 1, 50.4, A, gl('x'), 'Grok en X', ring=('⚠', K((0, 0), (52.0, 100, .8))),
          btn=('Siguiente', 56.3),
          mL=('Después de', 'las <b>críticas</b>', 52.0), mR=('Por crear', '<b>deepfakes</b>', 54.5),
          bar=K((0, 0), (52.0, 100, 3.0)), ac0='#ff4d5e',
          cols=[('Usado en', 'X', 53.45), ('Para', 'imágenes sexuales', 54.5), ('Sin', 'consentimiento', 55.05)])
c2 = tray(TX, CYT, TW, TK, 'gris', 57.0, A, em('📱'), 'Si tu app genera imágenes', ring=(N(K((0, 0), (65.03, 1, .3), (66.13, 2, .3), (68.28, 3, .3))) + '/3', K((0, 0), (65.03, 33, .5), (66.13, 66, .5), (68.28, 100, .5))),
          btn=('Siguiente', 68.9),
          mL=('No promoverlo', '<b>ya no basta</b>', 61.65), mR=('Ahora pon', '<b>filtros</b>', 65.03),
          bar=K((0, 0), (65.03, 33, .5), (66.13, 66, .5), (68.28, 100, .5)),
          cols=[('Paso 1', 'filtros', 65.1), ('Paso 2', 'botón de reporte', 66.2), ('Paso 3', 'a revisión', 68.3)],
          stops=[('Si genera', 'imágenes', 58.6), ('O la gente', 'sube contenido', 60.3)],
          thumbs=[('🖼️', GRIS, 58.6), ('⬆️', GRIS, 60.3)])
escena('e03-grok', S, 69.4, 1, fase(1, 0, A(56.5)) + fase(2, A(56.6)),
       f"""<div class="p1">{st([('Después de <em>Grok</em>', 50.4, None)], S, 92)}{baraja(CYT, TK, A, 50.6, SIG[2])}{c1}</div>
<div class="p2">{st([('¿Tu app genera<br><em>imágenes</em>?', 57.0, 63.3), ('Antes de mandarla<br>a <em>revisión</em>', 63.4, None)], S, 86)}{baraja(CYT, TK, A, 57.2, SIG[2])}{c2}</div>""",
LIB + "const XL=" + js(G.svgpath('x')) + ",SH=" + js(D.SHIELD) + r""";
const xl=R.shape(XL,230,3,R.metal('#d9dbe2',{roughness:.14,emissive:'#ff2a3a',emissiveIntensity:0}),.5);R.scene.add(xl);
const sh=R.shape(SH,230,5,R.gloss('#8d96a8',{emissive:'#3ee08a',emissiveIntensity:0,roughness:.16}));R.scene.add(sh);
return t=>{const a=R.eb(R.k(t,50.8,.9)),o=R.eo(R.k(t,56.2,.4)),b=R.eb(R.k(t,57.4,.8)),g=R.k(t,68.28,.5),w=Math.sin(Math.PI*R.k(t,54.5,.9));
 xl.visible=t<56.7;xl.scale.setScalar(Math.max(.001,a*(1-o)));R.at(xl,540,1650+10*Math.sin(t*1.4),1);xl.rotation.set(.15,(1-a)*3+.5*Math.sin(t*.8),w*.08*Math.sin(t*30));xl.material.emissiveIntensity=.5*w;
 sh.visible=t>57.2;sh.scale.setScalar(Math.max(.001,b));R.at(sh,540,1650,2);sh.rotation.set(.15,(1-b)*3+.4*Math.sin(t*1.1)+R.eio(R.k(t,65.03,.6))*6.28+R.eio(R.k(t,66.13,.6))*6.28,0);
 sh.material.color.set(g>.5?'#9ff0c2':'#8d96a8');sh.material.emissiveIntensity=.4*g}""")

# ───────── 1:09 · #03 Claude Code: de 2,500 a 30,000 cambios al día; «¿lo leyó un humano?» es mala medida
S = 69.4; A = G.at(S)
CL = gl('claude')
c1 = tray(TX, CYT, TW, TK, 'amb', 69.6, A, CL, 'Equipo de Claude Code', ring=(N(K((0, 0), (76.06, 90, 1.2)), suf='%'), K((0, 0), (76.06, 90, 1.2))),
          btn=('Siguiente', 78.2),
          mL=('Cambios al día', N(K((0, 2500), (77.0, 30000, 1.6)), f='c'), 74.4), mR=('Lo escribe', '<b>Claude</b>', 76.06),
          bar=K((0, 0), (74.44, 8, .5), (77.0, 100, 1.6)),
          cols=[('Mayo', '2,500 / día', 74.6), ('Escrito por IA', '~90 %', 76.5), ('Septiembre', '30,000+ / día', 77.3)],
          stops=[('Contó', 'cómo revisa código', 73.8), ('Cuando', 'los agentes programan', 76.5)],
          thumbs=[(G.logo('claude', '#fff'), AMB, 73.8), (G.logo('github', '#fff'), GRIS, 76.5)])
c2 = tray(TX, CYT, TW, TK, 'amb', 78.8, A, em('👀'), '¿Lo leyó un humano?', ring=('✕', K((0, 0), (81.6, 100, .5))),
          mL=('La pregunta', '<b>de siempre</b>', 79.2), mR=('Para ellos', '<b>mala medida</b>', 81.61),
          bar=K((0, 100), (81.6, 8, .8)), ac0='#ff4d5e',
          cols=[('¿Quién', 'lo leyó?', 80.4), ('', '', None), ('Medida', '✕ mala', 81.9)])
escena('e04-claudecode', S, 82.88, 'amb', fase(1, 0, A(78.5)) + fase(2, A(78.6)),
       f"""<div class="p1">{st([('Así revisa código<br><em>Claude Code</em>', 69.6, None)], S, 86)}{baraja(CYT, TK, A, 69.8, SIG[3])}{c1}</div>
<div class="p2">{st([('¿Lo leyó un <em>humano</em>?', 78.8, None)], S, 88)}{c2}
 {below('✕ mala medida', 1250, 81.8, A, 'pill bad', '--r:-4deg;')}</div>""",
LIB + "const CL=" + js(G.svgpath('claude')) + r""";
const cl=R.shape(CL,280,3,R.gloss('#d97757',{emissive:'#ff7a3d',emissiveIntensity:.2,roughness:.16,metalness:.3}),.6);R.scene.add(cl);
return t=>{const a=R.eb(R.k(t,70.0,.9)),sp=R.k(t,77.0,1.6);cl.scale.setScalar(Math.max(.001,a));R.at(cl,540,1660+10*Math.sin(t*1.5),2);
 cl.rotation.set(.15+.06*Math.sin(t*1.2),(1-a)*3+.5*Math.sin(t*.8),-t*.4-R.eio(sp)*3)}""")

# ───────── 1:23 · #03 (parte 2): la pregunta correcta; la revisión deja de ser una compuerta al final
S = 82.88; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 'amb', 83.0, A, em('🎯'), 'La pregunta correcta', ring=('?', K((0, 0), (85.5, 50, .8), (88.8, 100, .8))),
          btn=('Siguiente', 91.6),
          mL=('¿Qué podría', '<b>salir mal</b>?', 85.5), mR=('Qué control', sw(A, ('<b>automático</b>', [(87.84, 88.7)]), ('<b>o humano</b>', [(88.77, None)])), 87.84),
          bar=K((0, 0), (86.31, 50, .6), (90.22, 100, .8)),
          cols=[('Por', 'cada cambio', 86.31), ('Control', 'auto · humano', 88.8), ('Para', 'detectarlo', 90.76)],
          stops=[('Si falla', '¿qué se rompe?', 85.7), ('Quién lo', 'atrapa a tiempo', 89.6)],
          thumbs=[('🤖', AMB, 87.9), ('🧑', AMB, 88.8)])
c2 = tray(TX, CYT, TW, TK, 'amb', 92.1, A, em('🚧'), 'La revisión ya no es…', ring=(N(K((0, 0), (95.9, 40, 1.0))) + '%', K((0, 0), (95.9, 40, 1.0))),
          btn=('Siguiente', 96.6),
          mL=('Una compuerta', '<b>al final</b>', 94.9), mR=('Reverts', '<b>−40 %</b>', 96.0),
          bar=K((0, 100), (94.9, 100), (95.7, 30, 1.0)),
          cols=[('Antes', 'compuerta final', 94.9), ('PRs fusionados', '×2', 96.2), ('Ahora', 'todo el proceso', 96.4)])
escena('e05-pregunta', S, 97.1, 'amb', fase(1, 0, A(91.8)) + fase(2, A(91.9)),
       f"""<div class="p1">{st([('La pregunta<br><em>correcta</em>', 83.0, None)], S, 88)}{baraja(CYT, TK, A, 83.2, SIG[3])}{c1}</div>
<div class="p2">{st([('Ya no es una<br><em>compuerta</em>', 92.1, None)], S, 88)}{baraja(CYT, TK, A, 92.3, SIG[3])}{c2}</div>""",
LIB + "const CL=" + js(G.svgpath('claude')) + r""";
const rb=R.robot(200);R.scene.add(rb);
const cl=R.shape(CL,200,3,R.gloss('#d97757',{emissive:'#ff7a3d',emissiveIntensity:.2,roughness:.16,metalness:.3}),.6);R.scene.add(cl);
return t=>{const a=R.eb(R.k(t,87.6,.8)),b=R.eb(R.k(t,83.3,.9)),o=R.eo(R.k(t,91.5,.4)),c=R.eb(R.k(t,92.4,.9));
 cl.visible=t<92;cl.scale.setScalar(Math.max(.001,b*(1-o)));R.at(cl,R.mix(540,300,a),1660,2);cl.rotation.set(.15,.5*Math.sin(t*.8),-t*.4);
 rb.visible=t>87.4;rb.scale.setScalar(Math.max(.001,(t<92?a*(1-o):c)));R.at(rb,t<92?790:540,1640+8*Math.sin(t*1.6),2);
 rb.rotation.set(.1+.05*Math.sin(t*1.3),-.4+.35*Math.sin(t*.9),.05*Math.sin(t*2));rb.userData.em.emissiveIntensity=1.4+.6*Math.sin(t*3)}""")

# ───────── 1:37 · #03 (parte 3): si tu equipo ya no alcanza → dónde va cada test, check y ojos humanos
S = 97.1; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 'gris', 97.3, A, gl('github'), 'Si tu equipo no alcanza', ring=(N(K((0, 0), (104.31, 1, .3), (105.41, 2, .3), (107.42, 3, .3))) + '/3', K((0, 0), (104.31, 33, .5), (105.41, 66, .5), (107.42, 100, .5))),
          btn=('Siguiente', 107.9),
          mL=('Leer cada PR', '<b>no alcanza</b>', 98.6), mR=('Este modelo', '<b>decide</b>', 102.9),
          bar=K((0, 0), (104.31, 33, .5), (105.41, 66, .5), (107.42, 100, .5)),
          cols=[('Aquí', 'tests', 104.31), ('Aquí', 'checks automáticos', 105.41), ('Y aquí', 'ojos humanos', 107.42)],
          stops=[('Cada PR', 'línea por línea', 100.5), ('Ahora', 'dónde mirar', 103.4)],
          thumbs=[('✓', BG.format(a='#c9f8dc', b='#3ee08a'), 104.4), ('👁', AMB, 107.5)])
escena('e06-tuequipo', S, 108.32, 'gris', '',
       f"""<div class="p1">{st([('¿Tu equipo ya<br>no <em>alcanza</em>?', 97.2, 102.5), ('Decide <em>dónde</em> va<br>cada control', 102.6, None)], S, 86)}{baraja(CYT, TK, A, 97.5, SIG[3])}{c1}</div>""",
LIB + r"""const rb=R.robot(210);R.scene.add(rb);const sr=[];
for(let i=0;i<3;i++){const s=R.sheet(['#3ee08a','#ffb340','#7aa7ff'][i]);R.scene.add(s);sr.push(s)}
return t=>{const a=R.eb(R.k(t,97.6,.9));rb.scale.setScalar(Math.max(.001,a));R.at(rb,540,1640+8*Math.sin(t*1.6),2);
 rb.rotation.set(.1+.05*Math.sin(t*1.3),-.3+.4*Math.sin(t*.7),0);
 [104.31,105.41,107.42].forEach((t0,i)=>{const p=R.eb(R.k(t,t0,.7)),s=sr[i];s.visible=t>t0;s.scale.setScalar(Math.max(.001,p*.9));
  R.at(s,R.mix(540,[230,540,850][i],p),R.mix(1640,i==1?1440:1560,p),4);s.rotation.set(.2*Math.sin(t+i),.4*Math.sin(t*.8+i),.15*(i-1))})}""")

# ───────── 1:48 · #04 Anthropic: junior técnicos 21 % → 14 %, reuniones +20 %
S = 108.32; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 4, 108.5, A, gl('anthropic'), 'Anthropic · su plantilla', ring=(N(K((0, 21), (113.45, 14, 1.2)), suf='%'), K((0, 21), (113.45, 14, 1.2))),
          btn=('Siguiente', 119.0),
          mL=('Junior técnicos', N(K((0, 21), (113.45, 14, 1.2)), suf=' %'), 113.45), mR=('Reuniones', '<b>+20 %</b>', 115.7),
          bar=K((0, 21), (113.45, 14, 1.2)),
          cols=[('Inicio 2025', '21 % junior', 113.5), ('Contrataciones', '27 % → 9 %', 114.1), ('Hoy', '14 % junior', 114.4)],
          stops=[('Menos', 'perfiles junior', 113.8), ('Más', 'tiempo en reuniones', 115.7)],
          thumbs=[('🎓', CIAN, 113.8), ('📅', CIAN, 115.7)])
escena('e07-plantilla', S, 119.6, 4, '',
       f"""<div class="p1">{st([('Anthropic por <em>dentro</em>', 108.5, 116.8), ('Ojo: lo dice<br>la <em>empresa</em>', 116.9, None)], S, 88)}{baraja(CYT, TK, A, 108.7, SIG[4])}{c1}
 {below('📣 lo dice la propia empresa', 1420, 117.0, A, 'pill', '--r:-3deg;')}</div>""",
LIB + "const AN=" + js(G.svgpath('anthropic')) + r""";
const an=R.shape(AN,260,3,R.metal('#e9dccb',{roughness:.16}),.5);R.scene.add(an);
return t=>{const a=R.eb(R.k(t,109.0,.9));an.scale.setScalar(Math.max(.001,a));R.at(an,540,1740+10*Math.sin(t*1.4),1);an.rotation.set(.15+.05*Math.sin(t*1.1),(1-a)*3+.5*Math.sin(t*.8),0)}""")

# ───────── 1:59 · #04 (parte 2): señal de cómo cambia el trabajo (agentes = 6× las horas); si vas empezando
S = 119.6; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 4, 119.75, A, em('🤖'), 'Horas de trabajo', ring=('6×', K((0, 0), (121.3, 100, 1.5))),
          btn=('Siguiente', 123.6),
          mL=('Los agentes', N(K((0, 0), (121.28, 6, 1.5))) + '× más', 121.28), mR=('Que', 'sus <b>humanos</b>', 122.0),
          bar=K((0, 0), (121.3, 86, 1.5)),
          cols=[('Marzo', 'agentes > humanos', 121.5), ('', '', None), ('Agosto', '6× las horas', 122.0)])
c2 = tray(TX, CYT, TW, TK, 'gris', 124.1, A, em('🧭'), 'Si vas empezando', ring=('👀', K((0, 0), (127.4, 100, 1.0))),
          btn=('Siguiente', 128.6),
          mL=('Puestos', '<b>junior</b>', 126.42), mR=('Síguele', 'la <b>pista</b>', 128.3),
          bar=K((0, 0), (126.4, 40, .8), (128.3, 100, .8)),
          cols=[('Junior hoy', '14 %', 126.5), ('', '', None), ('Contrataciones', '9 %', 126.9)])
escena('e08-senal', S, 129.06, 4, fase(1, 0, A(123.8)) + fase(2, A(123.9)),
       f"""<div class="p1">{st([('Así cambia<br>el <em>trabajo</em>', 119.7, None)], S, 88)}{baraja(CYT, TK, A, 119.9, SIG[4])}{c1}</div>
<div class="p2">{st([('¿Vas <em>empezando</em>?', 124.0, None)], S, 92)}{baraja(CYT, TK, A, 124.2, SIG[4])}{c2}</div>""",
LIB + r"""const rb=R.robot(170);R.scene.add(rb);
return t=>{const a=R.eb(R.k(t,120.0,.9)),g=R.eio(R.k(t,121.3,1.5)),m=R.eio(R.k(t,123.6,.7));
 rb.scale.setScalar(Math.max(.001,a*(1+.25*g-.25*m)));R.at(rb,540,1660+8*Math.sin(t*1.6),2);
 rb.rotation.set(.1+.05*Math.sin(t*1.3),-.3+.4*Math.sin(t*.7)+m*6.28,0);rb.userData.em.emissiveIntensity=1.4+.8*g*(1-m)}""")

# ───────── 2:09 · cierre: ¿le darías acceso a tu cartera? (arriba entra «Sígueme»)
S = 129.06; A = G.at(S)
OPC = []
for i, (pal, ico, nm, l, r, fin, t0) in enumerate([(3, em('🔒'), 'Sí, con lo mínimo', ('Permisos', '<b>mínimos</b>'), ('Entorno', '<b>aislado</b>'), 64, 131.8),
                                                   (1, em('🙅'), 'Ni de broma', ('Mi cartera', '<b>es mía</b>'), ('Credenciales', '<b>no</b>'), 56, 133.6)]):
    OPC.append(tray(TX, 640 + i * 400, TW, 1.75, pal, t0, A, ico, nm, ring=(f'<b data-n=\'{K((0, 0), (134.6, fin, 1.2))}\' data-f="p">0%</b>', K((0, 0), (134.6, fin, 1.2))),
                    mL=(l[0], l[1], None), mR=(r[0], r[1], None), bar=K((0, 0), (134.6, fin, 1.2))))
SEG_INI = 135.9
escena('e09-cierre', S, FIN, 0, fase(1, 0, A(135.7)),
       f"""<div class="p1">{st([('¿Tú le darías<br><em>acceso</em>?', 129.2, None)], S, 88)}{''.join(OPC)}</div>""",
LIB + r"""const et=R.eth(150);R.scene.add(et);
const tx=R.text('EL LOG',140,60,R.iri('#b9a2ff',{metalness:.85,roughness:.14,opacity:1,transparent:false,iridescence:1}));R.scene.add(tx);
return t=>{const a=R.eb(R.k(t,132.8,.85)),o=R.eo(R.k(t,135.5,.4));
 et.visible=t>132.6&&t<136;et.scale.setScalar(Math.max(.001,a*(1-o)));R.at(et,540,1640,3);et.rotation.set(.1,t*1.2,0);
 const c=R.eb(R.k(t,136.0,.8));tx.visible=t>135.9;tx.scale.setScalar(Math.max(.001,c));R.at(tx,540,1450+(1-c)*150);tx.rotation.set(.18+.05*Math.sin(t*2),(1-c)*1.8+.22*Math.sin(t*1.5),0)}""",
sigue=False)

# ───────── tarjeta «Sígueme» (entra al final, debajo de la cinta)
SEGUIR = G.tarjeta("""
.tt{display:flex;align-items:center;gap:24px;padding-right:170px}
.av{width:120px;height:120px;border-radius:50%;background:linear-gradient(160deg,#e9e0ff,#a78bfa);display:flex;align-items:center;justify-content:center;font-size:56px;font-weight:800;color:#160b33;
  box-shadow:inset 0 3px 0 rgba(255,255,255,.6),0 0 0 6px rgba(255,255,255,.12),0 0 40px rgba(167,139,250,.45)}
.nm{font-size:44px;font-weight:800;letter-spacing:-.03em}
.btn{position:relative;margin-top:30px;height:96px}
.btn span{position:absolute;inset:0;border-radius:999px;display:flex;align-items:center;justify-content:center;font-size:36px;font-weight:800}
.b1{background:linear-gradient(180deg,#e9e0ff,#a78bfa);color:#160b33;box-shadow:inset 0 2px 0 #fff,0 20px 50px rgba(167,139,250,.4);animation:tap .22s ease .8s,off .2s ease .97s forwards}
.b2{background:linear-gradient(180deg,rgba(255,255,255,.18),rgba(255,255,255,.07));opacity:0;animation:fade .25s ease .97s forwards}
@keyframes tap{50%{transform:scale(.92)}}
.q{margin-top:22px;text-align:center}.q .pill{font-size:28px}
.cm{display:flex;gap:18px;align-items:center;margin-top:20px;padding:20px 26px;border-radius:36px;background:linear-gradient(180deg,rgba(255,255,255,.1),rgba(255,255,255,.03));animation:pop .45s cubic-bezier(.22,1.3,.36,1) 1.5s both}
.cm .mini{background:linear-gradient(160deg,#e9e0ff,#a78bfa)}.cm .t{font-size:28px;font-weight:600}
""", """<div class="tt"><div class="av">A</div><div><div class="nm">Armando</div><div class="sub">El Log · cada semana</div></div></div>
<div class="btn"><span class="b1">Seguir</span><span class="b2">Siguiendo ✓</span></div>
<div class="q pop" style="animation-delay:.4s"><span class="pill on">🔑 ¿Le darías tu cartera a un agente?</span></div>
<div class="cm"><div class="mini">💬</div><div><div class="sub" style="font-size:21px">Tú · ahora</div><div class="t"><span class="type" style="--td:.9s;--n:27;animation-delay:1.7s">Solo con permisos mínimos 🔒</span></div></div></div>""",
round(FIN - SEG_INI, 2), pal='ia', top=380,
js3d=LIB + r"""const lk=R.lock(130);R.scene.add(lk);
return t=>{const a=R.IN(t),o=R.OUT(t);lk.scale.setScalar(Math.max(.001,a*(1-o)));R.at(lk,880,520-o*80,4);lk.rotation.set(.2,-.45+.5*Math.sin(t*1.2),0)}""")

PIEZAS.append(('seguir', SEG_INI, FIN, SEGUIR))
PIEZAS.append(('cinta', 0.0, FIN, D.cinta()))  # al final: queda encima de todo
PRE = 'ell6-'

if __name__ == '__main__':
    solo = set(sys.argv[1:])
    for pid, a, b, html in PIEZAS:
        if solo and pid not in solo:
            continue
        path = f'{WORK}/{pid}.html'
        open(path, 'w').write(html)
        if os.environ.get('SOLO_HTML'):
            print('html', path); continue
        r = subprocess.run(['node', CAP, path, f'{b - a:.2f}', f'{OUT}/{PRE}{pid}.webm'], capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr[-600:], flush=True)
    if not solo:
        rel = os.environ.get('REL', 'noticias/6/animaciones')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
