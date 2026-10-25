"""El Log #05 · diseño «Destino» (gloss 2 + tarjetas tipo destino de viaje) con la cinta de noticiero arriba.
Reutiliza de ellog-04-destino.py el sistema de tarjetas (fc, meta, boton, FCSS), el 3D base y la cinta.
Tiempos = voz recortada de noticias/5 (voz/voz-norm.wav, 125.22 s). Necesita internet al capturar.
Uso: SALIDA=noticias/5/animaciones REL=noticias/5/animaciones python3 ejemplos/ellog-05-destino.py [ids…]   (SOLO_HTML=1 para revisar)
"""
import importlib.util, json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import ellog_gloss as G
from ellog_gloss import js

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('destino', os.path.join(HERE, 'ellog-04-destino.py'))
D = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(D)
fc, meta, boton, ic = D.fc, D.meta, D.boton, D.ic
BX, BW, BK, LX, RX, SW, SK, TOP = D.BX, D.BW, D.BK, D.LX, D.RX, D.SW, D.SK, D.TOP

CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.getcwd()))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
FIN = 125.22
BY, BH = 420, 1340

# la cinta del módulo base se arma con estos datos
D.FIN = FIN
D.NOTICIAS = [(0.0, 4, '01', 'FBI detiene a ingeniero de OpenAI'),
              (36.5, 1, '02', 'Netflix despide a ~1,000 personas'),
              (58.9, 3, '03', 'Llegan las laptops NVIDIA RTX Spark'),
              (90.3, 2, '04', 'Apple: iPhone Duo y MacBook táctil'),
              (112.2, 0, '✓', '¿Esperarías al 28 de octubre?')]
D.CORRIDO = ['OpenAI: grabadora USB de $14 escondida en papel de baño', 'Kash Patel: proteger la superinteligencia es prioridad del FBI',
             'Netflix: recortes antes de su reporte del 20 de octubre', 'Producto, tecnología, legal y RR. HH., las áreas más afectadas',
             'RTX Spark: desde USD 2,599 en ASUS, Dell, HP, Lenovo, Microsoft y MSI', 'ASUS ProArt P14 en España desde 3.299,99 €',
             'iPhone Duo: desde $1,999, llega el 23 de octubre', 'Geekbench: A20 Pro con 3,986 puntos en un núcleo',
             'Gurman: MacBook Pro táctil con OLED, presentación el 28 de octubre']

# piezas 3D nuevas: micrófono, laptop, plegable, portafolio, placa
LIB = D.LIB + r"""
R.mic=(w)=>{const G=R.group();const gr=new THREE.Mesh(new THREE.SphereGeometry(R.u(w*.32),40,28),R.metal('#c9d2de',{roughness:.35,wireframe:false}));gr.position.y=R.u(w*.55);G.add(gr);
 const mesh=new THREE.Mesh(new THREE.SphereGeometry(R.u(w*.33),24,16),R.metal('#e8ecf3',{wireframe:true}));mesh.position.y=gr.position.y;G.add(mesh);
 const band=new THREE.Mesh(new THREE.TorusGeometry(R.u(w*.33),R.u(w*.03),16,60),R.metal('#9aa3b5'));band.position.y=gr.position.y;band.rotation.x=Math.PI/2;G.add(band);
 const body=new THREE.Mesh(new THREE.CylinderGeometry(R.u(w*.17),R.u(w*.12),R.u(w*.9),40),R.gloss('#1b1e26',{roughness:.25}));body.position.y=R.u(-w*.1);G.add(body);
 const led=new THREE.Mesh(new THREE.SphereGeometry(R.u(w*.04),16,12),R.gloss('#ff3030',{emissive:'#ff1010',emissiveIntensity:1.5}));led.position.set(0,R.u(w*.15),R.u(w*.15));G.add(led);G.userData.led=led;return G};
R.laptop=(w,glow)=>{const G=R.group(),d=w*.66;const base=R.rbox(w,w*.04,d,w*.02,R.metal('#2b2f38',{roughness:.3}));G.add(base);
 const kb=R.rbox(w*.86,w*.006,d*.5,w*.005,R.gloss('#0d0f14'));kb.position.set(0,R.u(w*.022),R.u(-d*.05));G.add(kb);
 const lid=R.group();const sc=R.rbox(w,w*.62,w*.025,w*.02,R.metal('#2b2f38',{roughness:.3}));sc.position.y=R.u(w*.31);lid.add(sc);
 const pn=R.rbox(w*.94,w*.56,w*.004,w*.012,R.gloss('#0a0c14',{emissive:glow,emissiveIntensity:.5,roughness:.1}));pn.position.set(0,R.u(w*.31),R.u(w*.014));lid.add(pn);
 lid.position.z=R.u(-d/2);G.add(lid);G.userData={lid,pn};return G};
R.fold=(h)=>{const G=R.group(),w=h*.45;const m=R.gloss('#e9e6f0',{roughness:.2,metalness:.4});
 const L=R.group(),Rt=R.group();const a=R.rbox(w,h,h*.03,h*.05,m);a.position.x=R.u(-w/2);L.add(a);const b=R.rbox(w,h,h*.03,h*.05,m);b.position.x=R.u(w/2);Rt.add(b);
 const s1=R.rbox(w*.94,h*.95,3,h*.04,R.gloss('#0a0c14',{emissive:'#6ea8ff',emissiveIntensity:.35}));s1.position.set(R.u(-w/2),0,R.u(h*.017));L.add(s1);
 const s2=s1.clone();s2.position.x=R.u(w/2);Rt.add(s2);G.add(L);G.add(Rt);G.userData={L,Rt};return G};
R.case=(w,col)=>{const G=R.group();G.add(R.rbox(w,w*.7,w*.26,w*.06,R.gloss(col,{roughness:.25})));
 const h=new THREE.Mesh(new THREE.TorusGeometry(R.u(w*.14),R.u(w*.03),16,40,Math.PI),R.metal('#e8ecf3'));h.position.y=R.u(w*.35);G.add(h);
 const lk=R.rbox(w*.14,w*.08,w*.04,w*.01,R.metal('#ffcf4d'));lk.position.set(0,R.u(w*.2),R.u(w*.14));G.add(lk);return G};
R.badge=(r)=>{const G=R.group();G.add(R.star(5,r,r*.55,r*.25,R.metal('#ffcf4d',{roughness:.2})));
 const c=new THREE.Mesh(new THREE.CylinderGeometry(R.u(r*.42),R.u(r*.42),R.u(r*.3),48),R.gloss('#1a3a8a',{roughness:.2}));c.rotation.x=Math.PI/2;c.position.z=R.u(r*.08);G.add(c);
 const tx=R.text('FBI',r*.32,r*.08,R.metal('#fff4d0'));tx.position.z=R.u(r*.25);G.add(tx);return G};
"""

PIEZAS = []


def escena(pid, start, end, n, css, body, js3d=None, script='', sigue=True):
    if sigue:
        end += 0.45
    PIEZAS.append((pid, start, end, G.page(D.FCSS + css, body, end - start, script, n=n, js3d=js3d, salida=not sigue, t0=start)))


def st(items, S, size=88):
    return G.steps(items, S, top=TOP, size=size)


def fase(n, a, b=None):
    if n == 1:
        return f'.p1{{animation:gone .4s ease {b} forwards}}' if b else ''
    return f'.p{n}{{opacity:0;animation:fade .35s ease {a} forwards' + (f',gone .4s ease {b} forwards' if b else '') + '}'


def tag(html, A, t, extra=''):
    return f'<div class="tag pop" style="animation-delay:{A(t)};{extra}">{html}</div>'


def em(e, top='50%', size=None):
    return f'<div class="em" style="top:{top}{";font-size:" + str(size) + "px" if size else ""}">{e}</div>'


# ───────── 0:00 · #01 FBI detiene a un ingeniero de OpenAI por esconder un micrófono
S = 0.0; A = G.at(S)
lo1, hi1 = fc('a', BX, BY, BW, BH, BK, 4, A(0.2),
              f"""<div class="t">Micrófono escondido</div><div class="s pop" style="animation-delay:{A(3.9)}">en la sala de ejecutivos de OpenAI</div>
{meta(('user', 'un <b>ingeniero</b>', A(1.0)), ('chat', 'plan hecho con un <b>chatbot</b>', A(9.1)))}
{boton('Según Wired', A(7.2), 'chat')}""",
              hi_in=tag(f'{G.logo("openai", "#fff")}OpenAI', A, 1.8) + f'<div class="off" style="position:absolute;right:54px;top:470px"><span class="pill bad stamp" style="font-size:40px;padding:16px 32px;animation-delay:{A(4.9)}">🔴 REC</span></div>')
lo2a, hi2a = fc('b', LX, 620, SW, 820, SK, 'gris', A(12.2), '<div class="t">El aparato</div><div class="s">grabadora USB de $14, escondida en papel de baño</div>', phh=440,
                lo_in=em('🎙️'))
lo2b, hi2b = fc('a', RX, 620, SW, 820, SK, 2, A(17.0), '<div class="t">FBI</div><div class="s">ya arrestó al empleado</div>', fav='', lo_in=em('🚔', '40%'))
escena('e00-espia', S, 19.4, 4, fase(1, 0, A(11.6)) + fase(2, A(11.7)),
       f"""<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>
<div class="p2 lo">{lo2a}{lo2b}</div><div class="p2">{st([('OpenAI lo <em>encontró</em>', 11.8, None)], S, 92)}{hi2a}{hi2b}</div>""",
LIB + r"""const mc=R.mic(300);R.scene.add(mc);
return t=>{const a=R.eb(R.k(t,.4,.9)),o=R.eo(R.k(t,11.3,.4));mc.visible=t<11.8;mc.scale.setScalar(Math.max(.001,a*(1-o)));
 R.at(mc,540,820+10*Math.sin(t*1.5),2);mc.rotation.set(.15+.06*Math.sin(t*1.1),(1-a)*3+.5*Math.sin(t*.8),.12*Math.sin(t*.9));
 mc.userData.led.material.emissiveIntensity=t>4.9?(Math.sin(t*8)>0?2:.2):.2}""")

# ───────── 0:19 · #01 (parte 2): Kash Patel y «superinteligencia» → el riesgo puede estar en la misma sala
S = 19.4; A = G.at(S)
lo1, hi1 = fc('b', BX, BY, BW, BH, BK, 2, A(19.5),
              f"""<div class="t pop" style="animation-delay:{A(26.9)}">«Superinteligencia»</div><div class="s pop" style="animation-delay:{A(23.4)}">lo que quería grabar, según el FBI</div>
{meta(('user', '<b>Kash Patel</b>', A(19.7)), ('scale', 'director del <b>FBI</b>', A(20.5)))}
{boton('Prioridad de contrainteligencia', A(27.6), 'lock')}""", phh=700)
lo2a, hi2a = fc('a', LX, 640, SW, 780, SK, 'gris', A(31.4), '<div class="t">Afuera</div><div class="s">ataques y hackers</div>', fav='', lo_in=em('🌐', '40%'))
lo2b, hi2b = fc('b', RX, 640, SW, 780, SK, 4, A(33.2), f'<div class="t">Adentro</div><div class="s">en la misma sala que tú</div>{boton("Ojo", A(34.4), heart=A(35.3))}', phh=420,
                lo_in=em('👀'))
escena('e01-patel', S, 36.5, 4, fase(1, 0, A(28.7)) + fase(2, A(28.8)),
       f"""<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>
<div class="p2 lo">{lo2a}{lo2b}</div><div class="p2">{st([('¿Trabajas en <em>tecnología</em>?', 28.9, 31.2), ('El riesgo no siempre<br>viene de <em>afuera</em>', 31.3, None)], S, 86)}{hi2a}{hi2b}</div>""",
LIB + r"""const bd=R.badge(200);R.scene.add(bd);
return t=>{const a=R.eb(R.k(t,19.8,.9)),o=R.eo(R.k(t,28.4,.4));bd.visible=t<28.9;bd.scale.setScalar(Math.max(.001,a*(1-o)));
 R.at(bd,540,790,2);bd.rotation.set(.15+.05*Math.sin(t*1.2),(1-a)*3+.5*Math.sin(t*.8),.05*Math.sin(t))}""")

# ───────── 0:36 · #02 Netflix despide a ~1,000 personas → áreas → ten tu portafolio al día
S = 36.5; A = G.at(S)
lo1, hi1 = fc('a', BX, BY, BW, BH, BK, 1, A(36.7),
              f"""<div class="t">~<span id="nf">0</span> despidos</div><div class="s pop" style="animation-delay:{A(41.0)}">alrededor del 6 % de su plantilla</div>
{meta(('cal', 'la mayor ronda desde <b>2022</b>', A(43.9)))}
{boton('Antes de su reporte del 20 oct', A(44.6), 'trend')}""",
              hi_in=tag(f'{G.logo("netflix", "#fff")}Netflix', A, 37.0) + f'<div class="off" style="position:absolute;left:54px;top:470px"><span class="pill bad stamp" style="font-size:46px;padding:18px 36px;animation-delay:{A(41.9)}">−6 %</span></div>')
AREAS = [('🧩', 'Producto', 1, 48.0), ('💻', 'Tecnología', 2, 48.8), ('⚖️', 'Legal', 'amb', 49.7), ('🧑‍💼', 'Recursos humanos', 'pass', 50.2)]
lo2 = hi2 = ''
for i, (e, t, p, t0) in enumerate(AREAS):
    l, h = fc('b', LX if i % 2 == 0 else RX, 600 + (i // 2) * 600, SW, 560, 1.3, p, A(t0), f'<div class="t">{t}</div><div class="s">área afectada</div>', phh=360, lo_in=em(e))
    lo2 += l; hi2 += h
lo3, hi3 = fc('b', BX, 600, BW, 1160, BK, 1, A(52.0),
              f"""<div class="t">Tu portafolio</div><div class="s pop" style="animation-delay:{A(55.0)}">siempre al día</div>
{meta(('folder', 'proyectos <b>recientes</b>', A(54.3)), ('user', 'perfil <b>actualizado</b>', A(55.4)))}
{boton('Ni las que crecen', A(56.4), 'trend', heart='')}""", phh=560)
escena('e02-netflix', S, 58.9, 1, fase(1, 0, A(46.2)) + fase(2, A(46.3), A(51.8)) + fase(3, A(51.9)),
       f"""<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>
<div class="p2 lo">{lo2}</div><div class="p2">{st([('¿A quién le <em>tocó</em>?', 46.4, None)], S, 92)}{hi2}</div>
<div class="p3 lo">{lo3}</div><div class="p3">{st([('Ten tu <em>portafolio</em><br>al día', 52.0, None)], S, 86)}{hi3}</div>""",
LIB + "const NF=" + js(G.svgpath('netflix')) + r""";
const nf=R.shape(NF,300,4,R.gloss('#e50914',{emissive:'#b00610',emissiveIntensity:.3,roughness:.14}));R.scene.add(nf);const cs=R.case(300,'#7a3b1f');R.scene.add(cs);
return t=>{const a=R.eb(R.k(t,37.0,.9)),o=R.eo(R.k(t,45.9,.4)),b=R.eb(R.k(t,52.3,.9));
 nf.visible=t<46.4;nf.scale.setScalar(Math.max(.001,a*(1-o)));R.at(nf,540,820,2);nf.rotation.set(.15+.05*Math.sin(t),(1-a)*3+.5*Math.sin(t*.8),0);
 cs.visible=t>52.2;cs.scale.setScalar(Math.max(.001,b));R.at(cs,540,890,2);cs.rotation.set(.2+.05*Math.sin(t*1.2),(1-b)*3-.4+.3*Math.sin(t*.9),0)}""",
f"""window.__cnt=t=>{{t+={S};const e=1-Math.pow(1-Math.min(1,Math.max(0,(t-38.8)/1.3)),3);document.getElementById('nf').textContent=Math.round(1000*e).toLocaleString('en-US')}}""")

# ───────── 0:59 · #03 NVIDIA RTX Spark → Adobe y Microsoft se ajustan
S = 58.9; A = G.at(S)
lo1, hi1 = fc('a', BX, BY, BW, BH, BK, 3, A(59.1),
              f"""<div class="t">NVIDIA RTX Spark</div><div class="s pop" style="animation-delay:{A(63.0)}">laptops con IA de Microsoft y NVIDIA</div>
{meta(('cal', 'ya <b>a la venta</b>', A(60.9)), ('tag', 'desde <b>$2,599</b>', A(64.6)))}
{boton('Hasta 128 GB de memoria', A(65.9), 'star')}""",
              hi_in=tag(f'{G.logo("nvidia", "#fff")}NVIDIA', A, 59.4) + tag(f'{G.logo("microsoft", "#fff")}Microsoft', A, 66.5, 'left:auto;right:53px'))
APPS = [('Ps', 'Photoshop', 'rehecho para IA local', 2, 69.4), ('Pr', 'Premiere', 'IA 2× más rápida', 0, 70.2), ('Sb', 'Substance', 'muy pronto', 1, 70.85),
        (G.logo('microsoft', '#fff', 120), 'Windows', 'ajustado para ellas', 4, 72.7)]
lo2 = hi2 = ''
for i, (e, t, s, p, t0) in enumerate(APPS):
    l, h = fc('b', LX if i % 2 == 0 else RX, 600 + (i // 2) * 600, SW, 560, 1.3, p, A(t0), f'<div class="t">{t}</div><div class="s">{s}</div>', phh=360,
              lo_in=(f'<div class="em" style="font-size:120px;font-weight:800;letter-spacing:-.05em;color:#fff">{e}</div>' if len(e) == 2 else f'<div class="lg">{e}</div>'))
    lo2 += l; hi2 += h
escena('e03-spark', S, 76.0, 3, fase(1, 0, A(67.9)) + fase(2, A(68.0)),
       f"""<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>
<div class="p2 lo">{lo2}</div><div class="p2">{st([('Adobe y Microsoft<br>se <em>ajustan</em>', 68.1, None)], S, 86)}{hi2}</div>""",
LIB + r"""const lp=R.laptop(440,'#76b900');R.scene.add(lp);
return t=>{const a=R.eb(R.k(t,59.4,.9)),op=R.eio(R.k(t,60.6,1.0)),o=R.eo(R.k(t,67.6,.4));lp.visible=t<68.1;lp.scale.setScalar(Math.max(.001,a*(1-o)));
 R.at(lp,540,920,1);lp.rotation.set(.35+.05*Math.sin(t*1.1),(1-a)*3-.5+.3*Math.sin(t*.7),0);lp.userData.lid.rotation.x=-(1-op)*1.5+.25;
 lp.userData.pn.material.emissiveIntensity=.2+1.2*op}""")

# ───────── 1:16 · #03 (parte 2): ASUS ProArt en España, IA local → menos APIs de pago
S = 76.0; A = G.at(S)
lo1, hi1 = fc('b', BX, BY, BW, BH, BK, 3, A(76.2),
              f"""<div class="t">ASUS ProArt</div><div class="s pop" style="animation-delay:{A(79.3)}">ya en España, con IA local</div>
{meta(('tag', 'desde <b>3.299 €</b>', A(79.6)), ('lock', 'IA <b>en tu equipo</b>', A(80.4)))}
{boton('Sin pagar tokens', A(81.3), 'check', heart='')}""", phh=700)
lo2a, hi2a = fc('a', LX, 640, SW, 800, SK, 'gris', A(83.4), f'<div class="t">APIs de pago</div><div class="s">pagas por cada token</div>{boton("$ / token", A(84.2))}', fav='',
                lo_in=em('💸', '40%'))
lo2b, hi2b = fc('b', RX, 640, SW, 800, SK, 3, A(84.4), f'<div class="t">IA local</div><div class="s">en tu propia laptop</div>{boton("Gratis", A(87.6), "check", heart=A(88.6))}', phh=430,
                lo_in=em('💻'))
escena('e04-proart', S, 90.3, 3, fase(1, 0, A(82.7)) + fase(2, A(82.8)),
       f"""<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>
<div class="p2 lo">{lo2a}{lo2b}</div><div class="p2">{st([('¿Programas o editas<br>en <em>Windows</em>?', 82.9, 86.1), ('Depende menos de<br>las <em>APIs de pago</em>', 86.2, None)], S, 86)}{hi2a}{hi2b}
 <div class="vs stamp" style="left:540px;top:1040px;--r:-8deg;animation-delay:{A(86.4)}">VS</div></div>""",
LIB + r"""const lp=R.laptop(420,'#4fd2ff');R.scene.add(lp);
return t=>{const a=R.eb(R.k(t,76.4,.9)),o=R.eo(R.k(t,82.4,.4));lp.visible=t<82.9;lp.scale.setScalar(Math.max(.001,a*(1-o)));
 R.at(lp,540,830,1);lp.rotation.set(.35+.05*Math.sin(t*1.1),(1-a)*3+.5+.3*Math.sin(t*.7),0);lp.userData.lid.rotation.x=.25;lp.userData.pn.material.emissiveIntensity=1.1}""")

# ───────── 1:30 · #04 Apple: preventa del iPhone Duo → A20 Pro en Geekbench
S = 90.3; A = G.at(S)
lo1, hi1 = fc('a', BX, BY, BW, BH, BK, 2, A(90.5),
              f"""<div class="t">iPhone Duo</div><div class="s pop" style="animation-delay:{A(94.2)}">su primer plegable</div>
{meta(('cal', 'preventa: <b>16 oct</b>', A(95.6)), ('tag', 'desde <b>$1,999</b>', A(96.0)))}
{boton('Llega el 23 de octubre', A(96.4), 'clock')}""",
              fav='', hi_in=tag(f'{G.logo("apple", "#fff")}Apple', A, 90.9))
lo2, hi2 = fc('b', BX, 600, BW, 1160, BK, 0, A(97.4),
              f"""<div class="t">A20 Pro</div><div class="s pop" style="animation-delay:{A(98.0)}">ya apareció en Geekbench</div>
{meta(('star', '<b id="sc">0</b> un núcleo', A(98.6)), ('star', '<b>11,067</b> multinúcleo', A(99.4)))}
{boton('El mismo chip del iPhone 18 Pro', A(101.6), 'check')}""", phh=560)
escena('e05-apple', S, 103.4, 2, fase(1, 0, A(97.1)) + fase(2, A(97.2)),
       f"""<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>
<div class="p2 lo">{lo2}</div><div class="p2">{st([('Y en <em>Geekbench</em>…', 97.3, None)], S, 92)}{hi2}</div>""",
LIB + r"""const fd=R.fold(500);R.scene.add(fd);const ch=R.chip(230);R.scene.add(ch);
return t=>{const a=R.eb(R.k(t,90.8,.9)),op=R.eio(R.k(t,94.4,1.2)),o=R.eo(R.k(t,96.8,.4)),b=R.eb(R.k(t,97.6,.9));
 fd.visible=t<97.3;fd.scale.setScalar(Math.max(.001,a*(1-o)));R.at(fd,540,800,1);fd.rotation.set(.18+.05*Math.sin(t),(1-a)*3-.45+.25*Math.sin(t*.8),.06);
 fd.userData.L.rotation.y=(1-op)*1.25;fd.userData.Rt.rotation.y=-(1-op)*1.25;
 ch.visible=t>97.4;ch.scale.setScalar(Math.max(.001,b));R.at(ch,540,860,1);ch.rotation.set(.55+.08*Math.sin(t*1.4),.4*Math.sin(t*.8),0);ch.children[2].material.emissiveIntensity=.35+.8*R.k(t,98.6,1)}""",
f"""window.__cnt=t=>{{t+={S};const e=1-Math.pow(1-Math.min(1,Math.max(0,(t-98.6)/1.2)),3);document.getElementById('sc').textContent=Math.round(3986*e).toLocaleString('en-US')}}""")

# ───────── 1:43 · #04 (parte 2): Gurman: evento el 28 de octubre, MacBook Pro OLED táctiles
S = 103.4; A = G.at(S)
lo1, hi1 = fc('a', BX, BY, BW, BH, BK, 0, A(103.6),
              f"""<div class="t">MacBook Pro táctil</div><div class="s pop" style="animation-delay:{A(110.7)}">con pantalla OLED</div>
{meta(('cal', 'presentación: <b>28 oct</b>', A(108.0)), ('user', 'invitó a <b>medios</b>', A(106.2)))}
{boton('Según Mark Gurman', A(104.7), 'chat')}""",
              fav=A(111.2), hi_in=tag(f'{G.logo("apple", "#fff")}Apple', A, 105.4))
escena('e06-macbook', S, 112.2, 0, '', f'<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>',
LIB + r"""const lp=R.laptop(460,'#a78bfa');R.scene.add(lp);const fg=R.rbox(40,60,40,18,R.gloss('#ffd9cc',{roughness:.4}));R.scene.add(fg);
return t=>{const a=R.eb(R.k(t,103.9,.9)),op=R.eio(R.k(t,105.0,1.0)),tap=R.k(t,110.8,.5);lp.scale.setScalar(Math.max(.001,a));
 R.at(lp,540,880,1);lp.rotation.set(.3+.04*Math.sin(t*1.1),(1-a)*3-.35+.25*Math.sin(t*.7),0);lp.userData.lid.rotation.x=-(1-op)*1.5+.2;
 lp.userData.pn.material.emissiveIntensity=.2+1.0*op+(tap>0&&tap<1?1.5*Math.sin(Math.PI*tap):0);
 fg.visible=t>110.4&&t<111.6;R.at(fg,560,760+40*(1-Math.sin(Math.PI*Math.min(1,R.k(t,110.4,1.2)))),6)}""")

# ───────── 1:52 · cierre: ¿cambiar tu Mac ya o esperar? (arriba entra «Sígueme»)
S = 112.2; A = G.at(S)
lo1a, hi1a = fc('b', LX, 640, SW, 820, SK, 'gris', A(113.6), f'<div class="t">Cambiarla ya</div><div class="s">con lo que hay hoy</div>{boton("Ahora", A(114.4), heart="")}', phh=440,
                lo_in=em('💻'))
lo1b, hi1b = fc('a', RX, 640, SW, 820, SK, 0, A(115.4), f'<div class="t">Esperar al 28</div><div class="s">a ver qué sale ese día</div>{boton("Esperar", A(116.6), tap=A(117.9))}',
                fav=A(118.2), lo_in=em('⏳', '40%'))
SEG_INI = 120.9
escena('e07-cierre', S, FIN, 0, fase(1, 0, A(120.7)),
       f"""<div class="p1 lo">{lo1a}{lo1b}</div><div class="p1">{st([('¿Cambiar tu <em>Mac</em>?', 112.3, 115.2), ('Yo me <em>esperaría</em>', 115.3, None)], S, 92)}{hi1a}{hi1b}
 <div class="vs stamp" style="left:540px;top:1050px;--r:6deg;font-size:44px;animation-delay:{A(116.2)}">¿o?</div></div>""",
LIB + r"""const tx=R.text('EL LOG',140,60,R.iri('#b9a2ff',{metalness:.85,roughness:.14,opacity:1,transparent:false,iridescence:1}));R.scene.add(tx);
return t=>{const c=R.eb(R.k(t,120.9,.8));tx.visible=t>120.8;tx.scale.setScalar(Math.max(.001,c));R.at(tx,540,1450+(1-c)*150);tx.rotation.set(.18+.05*Math.sin(t*2),(1-c)*1.8+.22*Math.sin(t*1.5),0)}""",
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
.cm{display:flex;gap:18px;align-items:center;margin-top:20px;padding:20px 26px;border-radius:36px;background:linear-gradient(180deg,rgba(255,255,255,.1),rgba(255,255,255,.03));animation:pop .45s cubic-bezier(.22,1.3,.36,1) 1.6s both}
.cm .mini{background:linear-gradient(160deg,#e9e0ff,#a78bfa)}.cm .t{font-size:28px;font-weight:600}
""", """<div class="tt"><div class="av">A</div><div><div class="nm">Armando</div><div class="sub">El Log · cada semana</div></div></div>
<div class="btn"><span class="b1">Seguir</span><span class="b2">Siguiendo ✓</span></div>
<div class="q pop" style="animation-delay:.4s"><span class="pill on">💻 ¿Una MacBook para programar?</span></div>
<div class="cm"><div class="mini">💬</div><div><div class="sub" style="font-size:21px">Tú · ahora</div><div class="t"><span class="type" style="--td:1.0s;--n:20;animation-delay:1.8s">Si es táctil, sí 👀</span></div></div></div>""",
round(FIN - SEG_INI, 2), pal='ia', top=380,
js3d=LIB + r"""const lp=R.laptop(170,'#a78bfa');R.scene.add(lp);
return t=>{const a=R.IN(t),o=R.OUT(t);lp.scale.setScalar(Math.max(.001,a*(1-o)));R.at(lp,870,450-o*80,4);lp.rotation.set(.35,-.45+.5*Math.sin(t*1.2),0);lp.userData.lid.rotation.x=.2;lp.userData.pn.material.emissiveIntensity=1}""")

PIEZAS.append(('seguir', SEG_INI, FIN, SEGUIR))
PIEZAS.append(('cinta', 0.0, FIN, D.cinta()))  # al final: queda encima de todo
PRE = 'ell5-'

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
        rel = os.environ.get('REL', 'noticias/5/animaciones')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
