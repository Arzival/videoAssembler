"""El Log #06 · diseño «Catálogo» (gloss 2 + fichas oscuras tipo catálogo de modelos) con la cinta de noticiero arriba.
Reutiliza de ellog-04-catalogo.py la ficha (card, chip, CCSS) y de ellog-04-destino.py la cinta y el 3D base.
Tiempos = voz recortada de noticias/6 sin los 3 errores (voz/voz-norm.wav, 135.08 s). Necesita internet al capturar.
Uso: SALIDA=noticias/6/catalogo REL=noticias/6/catalogo python3 ejemplos/ellog-06-catalogo.py [ids…]   (SOLO_HTML=1 para revisar)
"""
import importlib.util, json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import ellog_gloss as G
from ellog_gloss import js

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('catalogo', os.path.join(HERE, 'ellog-04-catalogo.py'))
C = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(C)
D = C.D
card, chip, ic, TOP = C.card, C.chip, C.ic, C.TOP
BX, BW, BK, BIH = C.BX, C.BW, C.BK, C.BIH
LX, RX, SW, SK, SIH = C.LX, C.RX, C.SW, C.SK, C.SIH

CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.getcwd()))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
FIN = 135.08

# la cinta del módulo base se arma con estos datos
D.FIN = FIN
D.NOTICIAS = [(0.0, 2, '01', 'Un agente de OpenAI usó una cartera ajena'),
              (30.08, 1, '02', 'App Store prohíbe los deepfakes íntimos'),
              (68.0, 'amb', '03', 'Así revisa código el equipo de Claude Code'),
              (106.86, 4, '04', 'Anthropic: menos junior y más reuniones'),
              (127.88, 0, '✓', '¿Le darías tu cartera a un agente?')]
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


def escena(pid, start, end, n, css, body, js3d=None, script='', sigue=True):
    if sigue:
        end += 0.45
    PIEZAS.append((pid, start, end, G.page(C.CCSS + css, body, end - start, script, n=n, js3d=js3d, salida=not sigue, t0=start)))


def st(items, S, size=88):
    return G.steps(items, S, top=TOP, size=size)


def fase(n, a, b=None):
    return C.fase(n, a, b)


def em(e, size=None):
    return f'<div class="em"' + (f' style="font-size:{size}px"' if size else '') + f'>{e}</div>'


def below(html, top, t, A, cls='pill on', extra=''):
    return f'<div class="below" style="top:{top}px"><span class="{cls} stamp" style="font-size:40px;{extra}animation-delay:{A(t)}">{html}</span></div>'


def contador(S, el, t0, dur, a, b, fmt):
    """Contador en JS (window.__cnt): de a → b entre t0 y t0+dur (segundos del video)."""
    return (f"""window.__cnt=t=>{{t+={S};const e=1-Math.pow(1-Math.min(1,Math.max(0,(t-{t0})/{dur})),3),v={a}+({b}-{a})*e;"""
            f"""document.getElementById('{el}').textContent={fmt}}}""")


# ───────── 0:00 · #01 el agente de OpenAI: la tarea → los faucets fallan → cartera ajena; luego «dale lo mínimo»
S = 0.0; A = G.at(S)
lo1, hi1 = card(BX, 430, BW, 1240, BK, 2, 0.2, A, 'agente-de-openai', [('cpu', '<b>OpenAI</b>'), ('clock', 'modelo de investigación')],
                'Se metió a una cartera que no era suya y tomó Ethereum para terminar una tarea de programación.',
                [('rd', 'cartera ajena', 2.0), ('v', 'ethereum', 3.78), ('cy', '362 carteras revisadas', 4.6)],
                [('🎯', 'Tarea', [(0.3, 1.9)]), ('⛽', 'Faucets', [(2.0, 3.4)]), ('👛', 'Cartera', [(3.5, None)])],
                [('<i>$</i> deploy <em>--network sepolia</em>', [(0.3, 1.9)]), ('<i>faucet:</i> <em>sin fondos ✕</em>', [(2.0, 3.4)]),
                 ('<i>seed pública →</i> <em>362 carteras</em>', [(3.5, None)])], ih=BIH, dd=1.0,
                hi_in=chip(f'{G.logo("openai", "#fff")}OpenAI', 30, 30, 0.5, A))
CY = 620
lo2a, hi2a = card(LX, CY, SW, 790, SK, 'fin', 10.0, A, 'permisos-mínimos', [('lock', 'solo lo justo')], 'Credenciales y cartera con lo mínimo.',
                  [('gr', 'mínimos', 11.82)], [(ic('term'), 'Permisos', [(10.2, None)])], [('<i>scope:</i> <em>read-only</em>', [(11.6, None)])], ih=SIH)
lo2b, hi2b = card(RX, CY, SW, 790, SK, 4, 12.6, A, 'entorno-aislado', [('cpu', 'sandbox')], 'Que no toque nada fuera de su caja.',
                  [('cy', 'aislado', 13.99)], [(ic('term'), 'Docker', [(12.8, None)])], [('<i>$</i> docker run <em>--network none</em>', [(13.6, None)])], ih=SIH,
                  lo_in=em('📦'))
escena('e00-cartera', S, 18.5, 2, fase(1, 0, A(6.4)) + fase(2, A(6.5)),
       f"""<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>
<div class="p2 lo">{lo2a}{lo2b}</div><div class="p2">{st([('¿Le das <em>acceso</em>?', 6.7, 10.7), ('Dale lo <em>mínimo</em>', 10.8, 14.5), ('Se puede <em>saltar</em><br>los límites', 14.6, None)], S, 86)}{hi2a}{hi2b}
 {below('⚠️ con tal de cumplir el objetivo', CY + 830, 15.2, A, 'pill bad', '--r:-3deg;')}</div>""",
LIB + r"""const et=R.eth(320);R.scene.add(et);const lk=R.lock(170);R.scene.add(lk);const SH=lk.userData.sh;
return t=>{const a=R.eb(R.k(t,.4,.9)),o=R.eo(R.k(t,6.1,.4)),b=R.eb(R.k(t,10.2,.8)),cl=R.eio(R.k(t,11.8,.4)),op=R.eb(R.k(t,17.1,.5));
 et.visible=t<6.6;et.scale.setScalar(Math.max(.001,a*(1-o)));R.at(et,540,780+12*Math.sin(t*1.6),2);et.rotation.set(.12*Math.sin(t*1.1),(1-a)*3+t*.9+(t>3.78?R.eio(R.k(t,3.78,1.2))*4:0),0);
 lk.visible=t>10;lk.scale.setScalar(Math.max(.001,b));R.at(lk,285,815+8*Math.sin(t*1.4),2);lk.rotation.set(.15+.05*Math.sin(t*1.2),(1-b)*3+.4*Math.sin(t*.9),0);
 SH.position.y=R.u(170*(.4+.22*(1-cl)+.3*op));SH.rotation.y=op*.9}""")

# ───────── 0:18 · #01 (parte 2): era de prueba… pero entró a una cartera ajena
S = 18.5; A = G.at(S)
lo1, hi1 = card(BX, 430, BW, 1240, BK, 2, 18.7, A, 'era-de-prueba', [('lock', 'red de prueba'), ('clock', '26 jun')],
                'Era un modelo de investigación y eran tokens de prueba: no era dinero real. Pero acabó entrando a una cartera ajena.',
                [('v', 'investigación', 19.77), ('cy', 'tokens de prueba', 21.06), ('gr', '$0 reales', 22.86), ('rd', 'no lo avisó', 28.75)],
                [('🧪', 'Sepolia', [(19.0, 23.8)]), ('💻', 'Tarea', [(23.9, 27.6)]), ('👛', 'Cartera ajena', [(27.66, None)])],
                [('<i>red:</i> <em>sepolia</em> <i>· valor real:</i> $0', [(19.0, 23.8)]), ('<i>tarea:</i> <em>terminar el código</em>', [(23.9, 27.6)]),
                 ('<i>tx:</i> <em>firmada sin permiso</em>', [(27.66, None)])], ih=BIH, dd=19.2,
                hi_in=chip('🧪 testnet', 30, 30, 18.9, A))
escena('e01-prueba', S, 30.08, 2, '', f'<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>',
LIB + r"""const et=R.eth(280);R.scene.add(et);
return t=>{const a=R.eb(R.k(t,18.9,.9)),w=R.k(t,28.75,.6),sh=w>0&&w<1?Math.sin(t*40)*.08:0;et.scale.setScalar(Math.max(.001,a));
 R.at(et,540,780+12*Math.sin(t*1.5),2);et.rotation.set(.1*Math.sin(t*1.1),(1-a)*3+t*.8,sh)}""")

# ───────── 0:30 · #02 App Store: regla 1.2 (las pestañas recorren la regla); luego prevenir | eliminar
S = 30.08; A = G.at(S)
lo1, hi1 = card(BX, 430, BW, 1240, BK, 1, 30.3, A, 'app-store-review', [('file', 'regla <b>1.2</b>'), ('clock', '16 oct')],
                'Apple ya prohíbe las apps con IA que generan imágenes íntimas de personas sin su consentimiento.',
                [('v', 'apps con IA', 36.78), ('rd', 'imágenes íntimas', 38.45), ('rd', 'sin consentimiento', 40.2)],
                [('📄', '1.2 Contenido', [(30.5, 36.7)]), ('🤖', 'Apps con IA', [(36.78, None)])],
                [('<i>guía</i> <em>1.2</em> <i>· contenido de usuarios</i>', [(30.5, 36.7)]), ('<i>genera:</i> <em>imágenes íntimas</em>', [(36.78, 40.1)]),
                 ('<i>estado:</i> <em>rechazada ✕</em>', [(40.2, None)])], ih=BIH, dd=32.6,
                hi_in=chip(f'{G.logo("apple", "#fff")}App Store', 30, 30, 30.5, A))
lo2a, hi2a = card(LX, CY, SW, 790, SK, 'fin', 42.4, A, 'prevenir', [('check', 'antes de que pase')], 'Que la app no los genere.',
                  [('gr', 'filtros', 44.6)], [(ic('term'), 'Filtro', [(42.6, None)])], [('<i>if</i> nsfw <em>→ bloquear</em>', [(44.6, None)])], ih=SIH)
lo2b, hi2b = card(RX, CY, SW, 790, SK, 1, 44.9, A, 'eliminar', [('lock', 'si ya pasó')], 'Bajar los deepfakes que aparezcan.',
                  [('rd', 'deepfakes', 45.94)], [(ic('term'), 'Moderar', [(45.0, None)])], [('<i>reporte →</i> <em>borrar</em>', [(45.4, None)])], ih=SIH,
                  lo_in=em('🗑️'))
escena('e02-appstore', S, 48.6, 1, fase(1, 0, A(41.4)) + fase(2, A(41.5)),
       f"""<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>
<div class="p2 lo">{lo2a}{lo2b}</div><div class="p2">{st([('Y no solo <em>eso</em>', 41.7, 45.8), ('Fuera los <em>deepfakes</em>', 45.9, None)], S, 92)}{hi2a}{hi2b}
 {below('⚠️ si no, pierdes tu cuenta', CY + 830, 46.9, A, 'pill bad', '--r:-3deg;')}</div>""",
LIB + "const AP=" + js(G.svgpath('apple')) + ",SH=" + js(D.SHIELD) + r""";
const ap=R.shape(AP,250,3,R.metal('#d9dbe2',{roughness:.14}),.5);R.scene.add(ap);
const sh=R.shape(SH,170,5,R.gloss('#8d96a8',{emissive:'#3ee08a',emissiveIntensity:0,roughness:.16}));R.scene.add(sh);
return t=>{const a=R.eb(R.k(t,30.6,.9)),o=R.eo(R.k(t,41.1,.4)),b=R.eb(R.k(t,42.7,.8)),g=R.k(t,44.6,.5);
 ap.visible=t<41.6;ap.scale.setScalar(Math.max(.001,a*(1-o)));R.at(ap,540,780+10*Math.sin(t*1.4),1);ap.rotation.set(.15,(1-a)*3+.5*Math.sin(t*.8),0);
 sh.visible=t>42.5;sh.scale.setScalar(Math.max(.001,b));R.at(sh,285,810,2);sh.rotation.set(.15,(1-b)*3+.4*Math.sin(t*1.1),0);
 sh.material.color.set(g>.5?'#9ff0c2':'#8d96a8');sh.material.emissiveIntensity=.4*g}""")

# ───────── 0:49 · #02 (parte 2): después de Grok en X; si tu app genera imágenes → filtros, reporte, revisión
S = 48.6; A = G.at(S)
GY = 640
lo1, hi1 = card(BX, GY, BW, 1070, BK, 1, 48.8, A, 'grok-en-x', [('chat', '<b>X</b>'), ('clock', 'las críticas')],
                'Llega después de las críticas por usar Grok en X para crear imágenes sexuales no consentidas.',
                [('rd', 'grok', 51.89), ('rd', 'no consentidas', 54.22)],
                [(G.logo('x', '#fff'), 'Publicación', [(49.0, None)])], [('<i>@grok</i> <em>edita esta foto…</em>', [(51.9, None)])], ih=520, dd=49.4)
lo2, hi2 = card(BX, GY, BW, 1070, BK, 'gris', 55.9, A, 'tu-app', [('code', 'generas imágenes'), ('user', 'o suben contenido')],
                'Ya no basta con no promoverlo: ponle filtros y una forma de reportar antes de mandarla a revisión.',
                [('rd', 'no basta', 60.32), ('gr', 'filtros', 63.85), ('gr', 'reportar', 64.95), ('cy', 'a revisión', 67.1)],
                [('🧹', 'Filtros', [(56.1, 64.9)]), ('🚩', 'Reportar', [(64.95, 67.0)]), ('📤', 'Revisión', [(67.1, None)])],
                [('<i>if</i> nsfw(img) <em>→ bloquear</em>', [(56.1, 64.9)]), ('<i>botón:</i> <em>Reportar contenido</em>', [(64.95, 67.0)]),
                 ('<i>$</i> submit <em>--app-review</em>', [(67.1, None)])], ih=520, dd=60.2)
escena('e03-grok', S, 68.0, 1, fase(1, 0, A(55.4)) + fase(2, A(55.5)),
       f"""<div class="p1 lo">{lo1}</div><div class="p1">{st([('Después de <em>Grok</em>', 48.7, None)], S, 92)}{hi1}</div>
<div class="p2 lo">{lo2}</div><div class="p2">{st([('¿Tu app genera<br><em>imágenes</em>?', 55.8, 61.9), ('Antes de mandarla<br>a <em>revisión</em>', 62.0, None)], S, 86)}{hi2}</div>""",
LIB + "const XL=" + js(G.svgpath('x')) + ",SH=" + js(D.SHIELD) + r""";
const xl=R.shape(XL,230,3,R.metal('#d9dbe2',{roughness:.14,emissive:'#ff2a3a',emissiveIntensity:0}),.5);R.scene.add(xl);
const sh=R.shape(SH,210,5,R.gloss('#8d96a8',{emissive:'#3ee08a',emissiveIntensity:0,roughness:.16}));R.scene.add(sh);
return t=>{const a=R.eb(R.k(t,49.0,.9)),o=R.eo(R.k(t,55.1,.4)),b=R.eb(R.k(t,56.2,.8)),g=R.k(t,67.1,.5),w=Math.sin(Math.PI*R.k(t,53.0,1.2));
 xl.visible=t<55.6;xl.scale.setScalar(Math.max(.001,a*(1-o)));R.at(xl,540,920+10*Math.sin(t*1.4),1);xl.rotation.set(.15,(1-a)*3+.5*Math.sin(t*.8),w*.08*Math.sin(t*30));xl.material.emissiveIntensity=.5*w;
 sh.visible=t>56;sh.scale.setScalar(Math.max(.001,b));R.at(sh,540,920,2);sh.rotation.set(.15,(1-b)*3+.4*Math.sin(t*1.1)+R.eio(R.k(t,63.85,.6))*6.28+R.eio(R.k(t,64.95,.6))*6.28,0);
 sh.material.color.set(g>.5?'#9ff0c2':'#8d96a8');sh.material.emissiveIntensity=.4*g}""")

# ───────── 1:08 · #03 Claude Code: de 2,500 a 30,000 cambios al día; «¿lo leyó un humano?» es mala medida
S = 68.0; A = G.at(S)
lo1, hi1 = card(BX, 430, BW, 1240, BK, 'amb', 68.2, A, 'claude-code', [('code', '<b>Anthropic</b>'), ('clock', '15 oct')],
                'Su equipo contó cómo revisa código cuando los agentes generan gran parte de los cambios.',
                [('v', '~90 % lo escribe Claude', 74.75), ('cy', 'monorepo', 75.6), ('gr', '×12 cambios', 76.45)],
                [('📅', 'Mayo', [(68.4, 75.9)]), ('🚀', 'Septiembre', [(76.0, None)])],
                [('<i>cambios al día:</i> <em id="cd">2,500</em>', [(68.4, None)])], ih=BIH, dd=72.1,
                hi_in=chip(f'{G.logo("claude", "#fff")}Claude Code', 30, 30, 68.4, A))
lo2, hi2 = card(60, 640, 960, 520, 2.4, 'gris', 77.4, A, '¿lo-leyó-un-humano?', [('user', 'la medida de siempre')],
                'Para ellos, preguntar si un humano leyó el código es una mala medida.', [('rd', 'mala medida', 80.43)], iw=400, lo_in=em('👀', 170))
escena('e04-claudecode', S, 81.36, 'amb', fase(1, 0, A(77.0)) + fase(2, A(77.1)),
       f"""<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>
<div class="p2 lo">{lo2}</div><div class="p2">{st([('¿Lo leyó un <em>humano</em>?', 77.3, None)], S, 88)}{hi2}
 {below('✕ mala medida', 1250, 80.5, A, 'pill bad', '--r:-4deg;')}</div>""",
LIB + "const CL=" + js(G.svgpath('claude')) + r""";
const cl=R.shape(CL,300,3,R.gloss('#d97757',{emissive:'#ff7a3d',emissiveIntensity:.2,roughness:.16,metalness:.3}),.6);R.scene.add(cl);
return t=>{const a=R.eb(R.k(t,68.5,.9)),o=R.eo(R.k(t,76.7,.4)),sp=R.k(t,76.0,1.4);cl.visible=t<77.2;cl.scale.setScalar(Math.max(.001,a*(1-o)));R.at(cl,540,780+10*Math.sin(t*1.5),2);
 cl.rotation.set(.15+.06*Math.sin(t*1.2),(1-a)*3+.5*Math.sin(t*.8),-t*.4-R.eio(sp)*3)}""",
contador(S, 'cd', 76.0, 1.4, 2500, 30000, "Math.round(v).toLocaleString('en-US')"))

# ───────── 1:21 · #03 (parte 2): la pregunta correcta (pestañas automático | humano); luego «ya no es una compuerta»
S = 81.36; A = G.at(S)
lo1, hi1 = card(BX, 430, BW, 1240, BK, 'amb', 81.5, A, 'la-pregunta-correcta', [('check', 'por cada cambio')],
                '¿Qué podría salir mal con cada cambio y qué control, automático o humano, es el adecuado para detectarlo?',
                [('rd', 'qué sale mal', 83.91), ('v', 'automático', 86.61), ('gr', 'humano', 87.59)],
                [('⚠️', 'Riesgo', [(81.7, 86.5)]), ('🤖', 'Automático', [(86.61, 87.5)]), ('🧑', 'Humano', [(87.59, None)])],
                [('<i>riesgo:</i> <em>¿qué se rompe?</em>', [(81.7, 86.5)]), ('<i>control:</i> <em>tests · checks · agente</em>', [(86.61, 87.5)]),
                 ('<i>control:</i> <em>ojos humanos</em>', [(87.59, None)])], ih=BIH, dd=82.0)
lo2a, hi2a = card(LX, CY, SW, 640, SK, 'gris', 91.0, A, 'antes', [('clock', 'al final')], 'Una compuerta al final del proceso.',
                  [('rd', 'compuerta', 93.58)], ih=SIH, lo_in=em('🚧'))
lo2b, hi2b = card(RX, CY, SW, 640, SK, 'amb', 93.9, A, 'ahora', [('check', 'en todo el proceso')], 'Revisión continua, antes del PR.',
                  [('gr', 'reverts −40 %', 94.6), ('cy', 'PRs ×2', 95.0)], ih=SIH)
escena('e05-pregunta', S, 95.92, 'amb', fase(1, 0, A(90.3)) + fase(2, A(90.4)),
       f"""<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>
<div class="p2 lo">{lo2a}{lo2b}</div><div class="p2">{st([('Ya no es una<br><em>compuerta</em>', 90.6, None)], S, 88)}{hi2a}{hi2b}
 <div class="vs stamp" style="left:540px;top:{CY + 170}px;--r:-6deg;font-size:56px;animation-delay:{A(93.8)}">→</div></div>""",
LIB + "const CL=" + js(G.svgpath('claude')) + r""";
const rb=R.robot(200);R.scene.add(rb);const cl=R.shape(CL,170,3,R.gloss('#d97757',{emissive:'#ff7a3d',emissiveIntensity:.2,roughness:.16,metalness:.3}),.6);R.scene.add(cl);
return t=>{const a=R.eb(R.k(t,81.7,.9)),o=R.eo(R.k(t,90.0,.4)),c=R.eb(R.k(t,94.1,.8)),h=R.k(t,87.59,.6);
 rb.visible=t<90.5;rb.scale.setScalar(Math.max(.001,a*(1-o)));R.at(rb,540,780+8*Math.sin(t*1.6),2);
 rb.rotation.set(.1+.05*Math.sin(t*1.3),-.4+.35*Math.sin(t*.9)+R.eio(h)*6.28,.05*Math.sin(t*2));rb.userData.em.emissiveIntensity=1.4+.6*Math.sin(t*3);
 cl.visible=t>93.9;cl.scale.setScalar(Math.max(.001,c));R.at(cl,795,805,2);cl.rotation.set(.15,.5*Math.sin(t*.8),-t*.5)}""")

# ───────── 1:36 · #03 (parte 3): si tu equipo no alcanza → tests, checks y ojos humanos (las pestañas avanzan)
S = 95.92; A = G.at(S)
lo1, hi1 = card(BX, 430, BW, 1240, BK, 'gris', 96.1, A, 'tu-equipo', [('user', 'ya no alcanzan'), ('code', 'cada PR')],
                'Este modelo te sirve para decidir dónde va cada test, cada check automático y, sobre todo, los ojos humanos.',
                [('v', 'tests', 102.79), ('cy', 'checks', 103.58), ('gr', 'ojos humanos', 105.62)],
                [('📄', 'PR', [(96.3, 101.3)]), ('🧪', 'Tests', [(101.36, 103.5)]), ('⚙️', 'Checks', [(103.58, 105.5)]), ('👀', 'Humanos', [(105.62, None)])],
                [('<i>PR #</i>4821 <i>·</i> <em>+1,204 −310</em> <i>líneas</i>', [(96.3, 101.3)]), ('<i>$</i> npm <em>test</em>', [(101.36, 103.5)]),
                 ('<i>ci:</i> <em>lint · tipos · agente</em>', [(103.58, 105.5)]), ('<i>review:</i> <em>@humano</em>', [(105.62, None)])],
                ih=BIH, dd=99.86, hi_in=chip(f'{G.logo("github", "#fff")}Tu repo', 30, 30, 96.3, A))
escena('e06-tuequipo', S, 106.86, 'gris', '', f'<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>',
LIB + r"""const rb=R.robot(200);R.scene.add(rb);const sr=[];
for(let i=0;i<3;i++){const s=R.sheet(['#3ee08a','#ffb340','#7aa7ff'][i]);R.scene.add(s);sr.push(s)}
return t=>{const a=R.eb(R.k(t,96.4,.9));rb.scale.setScalar(Math.max(.001,a));R.at(rb,540,790+8*Math.sin(t*1.6),2);
 rb.rotation.set(.1+.05*Math.sin(t*1.3),-.3+.4*Math.sin(t*.7),0);
 [102.79,103.58,105.62].forEach((t0,i)=>{const p=R.eb(R.k(t,t0,.7)),s=sr[i];s.visible=t>t0;s.scale.setScalar(Math.max(.001,p*.85));
  R.at(s,R.mix(540,[260,540,820][i],p),R.mix(790,i==1?600:700,p),4);s.rotation.set(.2*Math.sin(t+i),.4*Math.sin(t*.8+i),.15*(i-1))})}""")

# ───────── 1:47 · #04 Anthropic: junior técnicos 21 % → 14 %, reuniones +20 %
S = 106.86; A = G.at(S)
lo1, hi1 = card(BX, 430, BW, 1240, BK, 4, 107.0, A, 'anthropic · plantilla', [('user', '<b>Anthropic</b>'), ('clock', 'último año')],
                'Dice que su plantilla se volvió menos junior y que ahora pasa más tiempo en reuniones.',
                [('cy', 'junior 21 % → 14 %', 112.2), ('v', 'reuniones +20 %', 114.52), ('rd', 'lo dice la empresa', 115.79)],
                [('🎓', 'Junior', [(107.2, 114.4)]), ('📅', 'Reuniones', [(114.52, None)])],
                [('<i>junior técnicos:</i> <em id="jr">21 %</em>', [(107.2, 114.4)]), ('<i>reuniones por persona:</i> <em>+20 %</em>', [(114.52, None)])],
                ih=BIH, dd=108.3, hi_in=chip(f'{G.logo("anthropic", "#fff")}Anthropic', 30, 30, 107.2, A))
escena('e07-plantilla', S, 118.21, 4, '',
       f"""<div class="p1 lo">{lo1}</div><div class="p1">{hi1}
 {below('📣 lo dice la propia empresa', 990, 115.8, A, 'pill', '--r:-3deg;')}</div>""",
LIB + "const AN=" + js(G.svgpath('anthropic')) + r""";
const an=R.shape(AN,280,3,R.metal('#e9dccb',{roughness:.16}),.5);R.scene.add(an);
return t=>{const a=R.eb(R.k(t,107.3,.9));an.scale.setScalar(Math.max(.001,a));R.at(an,540,720+10*Math.sin(t*1.4),1);an.rotation.set(.15+.05*Math.sin(t*1.1),(1-a)*3+.5*Math.sin(t*.8),0)}""",
contador(S, 'jr', 112.2, 1.2, 21, 14, "Math.round(v)+' %'"))

# ───────── 1:58 · #04 (parte 2): agentes vs. humanos (horas); si vas empezando, síguele la pista
S = 118.21; A = G.at(S)
lo1a, hi1a = card(LX, CY, SW, 640, SK, 4, 118.4, A, 'agentes', [('bot', 'horas de trabajo')], 'Ya trabajan 6× las horas de quienes los dirigen.',
                  [('cy', '6× horas', 120.1)], ih=SIH)
lo1b, hi1b = card(RX, CY, SW, 640, SK, 'gris', 119.6, A, 'humanos', [('user', 'empleados')], 'Coordinan, deciden y revisan.',
                  [('v', 'más reuniones', 120.8)], ih=SIH, lo_in=em('🧑‍💻'))
lo2, hi2 = card(BX, 640, BW, 1070, BK, 'gris', 123.0, A, 'si-vas-empezando', [('user', 'puestos junior')],
                'Si vas empezando o te preocupan los puestos junior, vale la pena seguirle la pista.',
                [('rd', 'junior: 14 %', 125.35), ('gr', 'síguele la pista', 127.0)],
                [('🧭', 'Seguir', [(123.2, None)])], [('<i>$</i> watch <em>empleo-junior</em>', [(126.6, None)])], ih=520, dd=123.5, lo_in=em('🧭', 170))
escena('e08-senal', S, 127.88, 4, fase(1, 0, A(122.5)) + fase(2, A(122.6)),
       f"""<div class="p1 lo">{lo1a}{lo1b}</div><div class="p1">{st([('Así cambia<br>el <em>trabajo</em>', 118.3, None)], S, 88)}{hi1a}{hi1b}
 <div class="vs stamp" style="left:540px;top:{CY + 170}px;--r:6deg;font-size:48px;animation-delay:{A(120.1)}">6×</div></div>
<div class="p2 lo">{lo2}</div><div class="p2">{st([('¿Vas <em>empezando</em>?', 122.9, None)], S, 92)}{hi2}</div>""",
LIB + r"""const rb=R.robot(170);R.scene.add(rb);
return t=>{const a=R.eb(R.k(t,118.6,.9)),o=R.eo(R.k(t,122.2,.4)),g=R.eio(R.k(t,120.1,1.0));
 rb.visible=t<122.7;rb.scale.setScalar(Math.max(.001,a*(1-o)*(1+.2*g)));R.at(rb,285,805+8*Math.sin(t*1.6),2);
 rb.rotation.set(.1+.05*Math.sin(t*1.3),.4+.3*Math.sin(t*.7),0);rb.userData.em.emissiveIntensity=1.4+.8*g}""")

# ───────── 2:08 · cierre: ¿le darías acceso a tu cartera o tus credenciales? (arriba entra «Sígueme»)
S = 127.88; A = G.at(S)
lo1a, hi1a = card(LX, CY, SW, 790, SK, 'fin', 128.4, A, 'con-lo-mínimo', [('lock', 'permisos mínimos')], 'Sí, pero en un entorno aislado.',
                  [('gr', 'sandbox', None)], [(ic('term'), 'Dar acceso', [(128.6, None)])], [('<i>$</i> grant <em>--read-only</em>', [(129.0, None)])],
                  copy=(130.0, None), ih=SIH)
lo1b, hi1b = card(RX, CY, SW, 790, SK, 1, 129.8, A, 'ni-de-broma', [('lock', 'mi cartera es mía')], 'Mis credenciales no se tocan.',
                  [('rd', 'no', None)], [(ic('term'), 'Negar', [(130.0, None)])], [('<i>$</i> deny <em>--all</em>', [(130.4, None)])],
                  copy=(130.9, None), ih=SIH)
SEG_INI = 131.6
escena('e09-cierre', S, FIN, 0, fase(1, 0, A(131.4)),
       f"""<div class="p1 lo">{lo1a}{lo1b}</div><div class="p1">{st([('¿Tú le darías<br><em>acceso</em>?', 128.0, None)], S, 88)}{hi1a}{hi1b}
 <div class="vs stamp" style="left:540px;top:{CY + 170}px;--r:6deg;font-size:42px;animation-delay:{A(130.3)}">¿o?</div></div>""",
LIB + r"""const lk=R.lock(150);R.scene.add(lk);const et=R.eth(190);R.scene.add(et);
const tx=R.text('EL LOG',140,60,R.iri('#b9a2ff',{metalness:.85,roughness:.14,opacity:1,transparent:false,iridescence:1}));R.scene.add(tx);
return t=>{const a=R.eb(R.k(t,128.7,.85)),b=R.eb(R.k(t,130.1,.85)),o=R.eo(R.k(t,131.2,.4));
 lk.visible=t>128.5&&t<131.7;lk.scale.setScalar(Math.max(.001,a*(1-o)));R.at(lk,285,810,2);lk.rotation.set(.15,(1-a)*3+.45*Math.sin(t*1.1),0);
 et.visible=t>129.9&&t<131.7;et.scale.setScalar(Math.max(.001,b*(1-o)));R.at(et,795,800,2);et.rotation.set(.1,t*1.2,0);
 const c=R.eb(R.k(t,131.7,.8));tx.visible=t>131.6;tx.scale.setScalar(Math.max(.001,c));R.at(tx,540,1450+(1-c)*150);tx.rotation.set(.18+.05*Math.sin(t*2),(1-c)*1.8+.22*Math.sin(t*1.5),0)}""",
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
PRE = 'cat6-'

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
        rel = os.environ.get('REL', 'noticias/6/catalogo')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
