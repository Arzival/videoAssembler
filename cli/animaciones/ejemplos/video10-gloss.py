"""Video 10 · la Legion 5 llega al homelab (devlog) en estilo «gloss 2»: tarjetas de vidrio sobre la cámara + una escena
a pantalla completa (respaldo mutuo ZenBook ⇄ Legion). Reutiliza las piezas 3D del video 9 y suma laptop y tarjeta gráfica.
Tiempos = timeline final (voz de videos/10 con cortes, 115.62 s).
Uso: SALIDA=videos/10/animaciones REL=videos/10/animaciones python3 ejemplos/video10-gloss.py [ids…]   (SOLO_HTML=1 para revisar)
Los archivos salen con prefijo «g10-» (el editor web empareja por nombre).
"""
import importlib.util, json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import ellog_gloss as G
from ellog_gloss import js

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('v9', os.path.join(HERE, 'video9-gloss.py'))
V9 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(V9)
d, lg = V9.d, V9.lg

CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.getcwd()))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
PRE = 'g10-'
FIN = 115.62

# piezas 3D nuevas: laptop (tapa con pantalla encendida) y tarjeta gráfica con dos ventiladores
LIB = V9.LIB + r"""
R.laptop=(w,body='#22252d',scr='#6ea8ff')=>{const G=R.group(),bm=R.metal(body,{roughness:.25}),dp=w*.68;
 const base=R.rbox(w,w*.05,dp,w*.025,bm);G.add(base);
 const kb=R.rbox(w*.86,w*.012,dp*.5,w*.006,R.gloss('#0d0f12',{roughness:.5}));kb.position.set(0,R.u(w*.028),R.u(-dp*.08));G.add(kb);
 const lid=R.group();lid.position.set(0,R.u(w*.025),R.u(-dp/2));G.add(lid);
 const sh=R.rbox(w,w*.64,w*.03,w*.025,bm);sh.position.set(0,R.u(w*.32),0);lid.add(sh);
 const sm=R.gloss(scr,{emissive:scr,emissiveIntensity:.55,roughness:.2});const sc=R.rbox(w*.9,w*.55,w*.01,w*.012,sm);sc.position.set(0,R.u(w*.33),R.u(w*.018));lid.add(sc);
 lid.rotation.x=-.28;G.userData.lid=lid;G.userData.sm=sm;return G};
R.gpu=(w,acc='#3ee08a')=>{const G=R.group();G.add(R.rbox(w,w*.42,w*.09,w*.03,R.metal('#2a2e38',{roughness:.3})));
 const st=R.rbox(w*.9,w*.025,w*.02,w*.01,R.gloss(acc,{emissive:acc,emissiveIntensity:.9}));st.position.set(0,R.u(-w*.17),R.u(w*.05));G.add(st);const fans=[];
 for(const x of [-.23,.23]){const f=R.group();f.position.set(R.u(w*x),R.u(w*.02),R.u(w*.05));G.add(f);
  f.add(new THREE.Mesh(new THREE.TorusGeometry(R.u(w*.15),R.u(w*.014),12,48),R.metal('#c9d2de',{roughness:.2})));
  for(let i=0;i<7;i++){const b=R.rbox(w*.13,w*.04,w*.008,w*.006,R.gloss('#14161c',{roughness:.4}));b.rotation.z=i*Math.PI*2/7;b.position.set(R.u(w*.06*Math.cos(i*Math.PI*2/7)),R.u(w*.06*Math.sin(i*Math.PI*2/7)),0);f.add(b)}
  const hub=new THREE.Mesh(new THREE.CylinderGeometry(R.u(w*.035),R.u(w*.035),R.u(w*.02),24),R.metal('#e8ecf3'));hub.rotation.x=Math.PI/2;f.add(hub);fans.push(f)}
 G.userData.fans=fans;return G};
"""

TARJETAS = {}   # id → (inicio, duración, paleta, css, body, js3d[, script][, top])
ESCENAS = {}

# 0:00 · «esta laptop me costó $9,000 pesos usada y va a ser el músculo de mi homelab»
TARJETAS['c01-precio'] = (0.2, 4.1, 'fin', """
.pr2{display:flex;align-items:baseline;gap:14px;margin-top:6px}
.pr2 .v{font-size:110px;font-weight:800;letter-spacing:-.05em;line-height:1}.pr2 .mx{font-size:34px;font-weight:800;color:var(--ac)}
.tags{display:flex;gap:14px;margin-top:22px}.tags .pill{font-size:28px}
""", f"""<div class="hd" style="padding-right:200px"><div class="ic">💻</div><div class="app">Mi nueva laptop<small>para el homelab</small></div></div>
<div class="pr2 pop" {d(.5)}><span class="v">$<span id="cnt">0</span></span><span class="mx">MXN</span></div>
<div class="tags"><span class="pill pop" {d(1.8)}>♻️ usada</span><span class="pill on pop" {d(2.6)}>💪 el músculo de mi homelab</span></div>""",
LIB + r"""const mn=R.money(105);R.scene.add(mn);
return t=>{const a=R.IN(t),o=R.OUT(t),p=Math.sin(Math.PI*R.k(t,1.4,.5));mn.scale.setScalar(Math.max(.001,a*(1-o)*(1+.12*p)));R.at(mn,870,300-o*80,4);
 mn.rotation.set(.25,t*2.0,.1)}""",
"""window.__cnt=t=>{const p=Math.min(1,Math.max(0,(t-.7)/.9)),e=1-Math.pow(1-p,3);document.getElementById('cnt').textContent=Math.round(9000*e).toLocaleString('en-US')}""")

# 0:08 · «trae un Ryzen 7 de 8 núcleos y 16 hilos, 16 GB de RAM que puedo expandir… y lo más importante: una 3050 Ti de 4 GB»
TARJETAS['c02-specs'] = (8.3, 15.0, 'tg', """
.steps .row .tg2{font-size:24px;font-weight:800;letter-spacing:.06em;padding:8px 14px;border-radius:12px;background:rgba(255,255,255,.1)}
.steps .row.gpu{box-shadow:inset 0 0 0 2px var(--ac),0 0 40px rgba(79,180,255,.35)}
.steps .row.gpu .tg2{background:linear-gradient(160deg,#d6ecff,#4fb4ff);color:#04203a}
.stamp{animation-fill-mode:both}.imp{display:flex;justify-content:flex-end;margin-top:14px}.imp .pill{font-size:26px;--r:-3deg}
""", f"""<div class="hd" style="padding-right:200px"><div class="ic">🎮</div><div class="app">Lenovo Legion 5<small>la encontré en Marketplace</small></div></div>
<div class="steps">
 <div class="row pop" {d(.7)}><div class="info"><div class="n">Ryzen 7</div><div class="sub">8 núcleos · 16 hilos</div></div><span class="tg2">CPU</span></div>
 <div class="row pop" {d(4.9)}><div class="info"><div class="n">16 GB de RAM</div><div class="sub">y se puede expandir</div></div><span class="tg2">RAM</span></div>
 <div class="row gpu pop" {d(12.5)}><div class="info"><div class="n">RTX 3050 Ti</div><div class="sub">4 GB de memoria</div></div><span class="tg2">GPU</span></div>
</div>
<div class="imp"><span class="pill on stamp" {d(10.6)}>⭐ lo más importante</span></div>""",
LIB + r"""const ch=R.chip(150);R.scene.add(ch);const gp=R.gpu(230,'#4fb4ff');R.scene.add(gp);const F=gp.userData.fans;
return t=>{const a=R.IN(t),o=R.OUT(t),m=R.eo(R.k(t,10.4,.4)),b=R.eb(R.k(t,10.6,.8));
 ch.visible=t<10.9;ch.scale.setScalar(Math.max(.001,a*(1-m)));R.at(ch,860,290,4);ch.rotation.set(.5+.05*Math.sin(t*1.3),.4*Math.sin(t*.9),0);ch.children[2].material.emissiveIntensity=.35+.4*Math.abs(Math.sin(t*2));
 gp.visible=t>10.5;gp.scale.setScalar(Math.max(.001,b*(1-o)));R.at(gp,850,300-o*80,4);gp.rotation.set(.25+.05*Math.sin(t*1.2),-.45+.3*Math.sin(t*.8),0);
 F.forEach(f=>f.rotation.z=-t*(t>12.5?14:4))}""")

# 0:33 · «primero las capturas de mis redes y los precios que rastreo de Mercado Libre y Amazon; ahorita lo hace la ZenBook»
TARJETAS['c03-tareas'] = (33.0, 10.6, 'amb', """
.who2{display:flex;align-items:center;justify-content:center;gap:16px;margin-top:20px}.who2 .pill{font-size:28px}.who2 .ar{font-size:36px;color:rgba(255,255,255,.45)}
.lgs{display:flex;gap:10px}.lgs .pill{font-size:22px;padding:8px 14px}.lgs svg{width:26px;height:26px}
""", f"""<div class="hd" style="padding-right:200px"><div class="ic">🏋️</div><div class="app">Trabajo pesado<small>se lo paso a la Legion</small></div></div>
<div class="steps">
 <div class="row pop" {d(1.8)}><span class="num">📸</span><div class="info"><div class="n">Capturas</div><div class="sub">de mis redes sociales</div></div></div>
 <div class="row pop" {d(3.9)}><span class="num">🏷️</span><div class="info"><div class="n">Precios que rastreo</div><div class="sub">bajadas y descuentos</div></div>
  <div class="lgs"><span class="pill pop" {d(5.8)}>🤝 Mercado Libre</span><span class="pill pop" {d(6.8)}>{lg('amazon')}Amazon</span></div></div>
</div>
<div class="who2"><span class="pill pop" {d(7.6)}>💻 hoy: ZenBook</span><span class="ar fade" {d(8.6)}>→</span><span class="pill on pop" {d(8.9)}>🎮 Legion</span></div>""",
LIB + r"""const tg=R.tag(190,'#ffb340');R.scene.add(tg);
return t=>{const a=R.IN(t),o=R.OUT(t),h=Math.sin(Math.PI*R.k(t,3.9,.5));tg.scale.setScalar(Math.max(.001,a*(1-o)*(1+.12*h)));R.at(tg,860,290-o*80,4);
 tg.rotation.set(.2,-.45+.35*Math.sin(t*1.1),-.15+.08*Math.sin(t*1.6))}""")

# 0:59 · «la ZenBook lo hace 9 veces más lento que mi Mac → combinar las 3 laptops para que rendericen más rápido»
TARJETAS['c04-render'] = (58.9, 10.6, 'ia', """
.bars{display:grid;gap:18px;margin-top:6px}
.bw{display:grid;grid-template-columns:200px 1fr 170px;align-items:center;gap:18px;font-size:30px;font-weight:700;animation:pop .45s cubic-bezier(.22,1.35,.36,1) both}
.bw .tr2{height:26px;border-radius:13px;background:rgba(255,255,255,.08);overflow:hidden}
.bw .tr2 i{display:block;height:100%;width:0;border-radius:13px;background:linear-gradient(90deg,#a78bfa,#e9e0ff);animation:grow 1s cubic-bezier(.22,1,.36,1) both}
.bw.bad .tr2 i{background:linear-gradient(90deg,#ff4d5e,#ffb3b3)}.bw .x{font-size:28px;text-align:right;color:rgba(255,255,255,.7)}.bw.bad .x{color:#ff8a8a}
@keyframes grow{to{width:var(--w)}}
.stamp{animation-fill-mode:both}.tog{display:flex;justify-content:center;margin-top:24px}.tog .pill{font-size:30px;padding:16px 30px}
""", f"""<div class="hd" style="padding-right:200px"><div class="ic">🧊</div><div class="app">Animaciones 3D<small>las de todos mis videos</small></div></div>
<div class="bars">
 <div class="bw" {d(.5)}><span>🍎 Mac</span><div class="tr2"><i style="--w:11%;animation-delay:.8s"></i></div><span class="x">1×</span></div>
 <div class="bw bad" {d(2.0)}><span>💻 ZenBook</span><div class="tr2"><i style="--w:100%;animation-delay:2.3s"></i></div><span class="x">9× lento</span></div>
 <div class="bw" {d(5.6)}><span>🎮 Legion</span><div class="tr2"><i style="--w:20%;animation-delay:5.9s;background:linear-gradient(90deg,#3ee08a,#d2fbe4)"></i></div><span class="x">GPU ⚡</span></div>
</div>
<div class="tog"><span class="pill on stamp" {d(7.4)}>🤝 las 3 juntas → más rápido</span></div>""",
LIB + r"""const lp=R.laptop(190,'#2a2e38','#a78bfa');R.scene.add(lp);
return t=>{const a=R.IN(t),o=R.OUT(t),p=Math.sin(Math.PI*R.k(t,7.4,.5));lp.scale.setScalar(Math.max(.001,a*(1-o)*(1+.1*p)));R.at(lp,860,320-o*80,4);
 lp.rotation.set(.35+.05*Math.sin(t*1.2),-.5+.35*Math.sin(t*.8),0);lp.userData.sm.emissiveIntensity=.45+.35*Math.abs(Math.sin(t*2.5))}""")

# 0:44 · «después tendría que pasar todos los videos a texto, porque los estoy ocupando para un análisis»
TARJETAS['c05-texto'] = (43.9, 5.9, 'tg', """
.flow{display:flex;align-items:center;gap:16px;margin-top:6px}.flow .pill{font-size:28px}.flow .ar{font-size:40px;color:rgba(255,255,255,.4)}
.tx2{margin-top:20px;padding:22px 26px;border-radius:28px;background:rgba(0,0,0,.35);box-shadow:inset 0 2px 10px rgba(0,0,0,.3);font-size:28px;line-height:1.35;color:rgba(255,255,255,.85);min-height:84px}
.tx2 b{display:block;font-size:20px;color:var(--ac);letter-spacing:.06em;text-transform:uppercase;margin-bottom:6px}
.an{display:flex;justify-content:flex-end;margin-top:16px}.an .pill{font-size:28px;--r:-3deg}.stamp{animation-fill-mode:both}
""", f"""<div class="hd" style="padding-right:200px"><div class="ic">🎙️</div><div class="app">Videos → texto<small>todos, para un análisis</small></div></div>
<div class="flow"><span class="pill pop" {d(.5)}>🎬 mis videos</span><span class="ar fade" {d(1.2)}>→</span><span class="pill on pop" {d(1.4)}>📝 transcripción</span></div>
<div class="tx2 pop" {d(1.9)}><b>texto</b><span class="type" style="--td:1.6s;--n:38;animation-delay:2.3s;font-family:inherit;white-space:normal">«Esta laptop me costó 9,000 pesos…»</span></div>
<div class="an"><span class="pill on stamp" {d(4.6)}>🔬 para un análisis</span></div>""",
LIB + r"""const sp=R.spark(100,'#4fb4ff');R.scene.add(sp);
return t=>{const a=R.IN(t),o=R.OUT(t),p=Math.sin(Math.PI*R.k(t,4.6,.5));sp.scale.setScalar(Math.max(.001,a*(1-o)*(1+.15*p)));R.at(sp,870,290-o*80,4);sp.rotation.set(.15,.4*Math.sin(t*1.1),t*.6)}""")

# 1:29 · «como las bases de datos van a estar copiadas al segundo, el paso de una a otra va a ser muy rápido y muy simple»
TARJETAS['c06-replica'] = (88.57, 8.8, 'fin', """
.rp{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:16px;margin-top:6px}
.db2{padding:22px 20px;border-radius:28px;background:rgba(255,255,255,.07);text-align:center;animation:pop .45s cubic-bezier(.22,1.35,.36,1) both}
.db2 .e{font-size:48px}.db2 .n{font-size:30px;font-weight:800;margin-top:6px}.db2 .s{font-size:22px;color:rgba(255,255,255,.6)}
.sy{font-size:44px;color:var(--ac);animation:spin2 1s linear infinite}@keyframes spin2{to{transform:rotate(360deg)}}
.lat{display:flex;justify-content:center;margin-top:20px}.lat .pill{font-size:28px;font-variant-numeric:tabular-nums}
.ok3{display:flex;justify-content:flex-end;margin-top:14px}.ok3 .pill{font-size:28px;--r:-3deg}.stamp{animation-fill-mode:both}
""", f"""<div class="hd" style="padding-right:200px"><div class="ic">🗄️</div><div class="app">Bases de datos<small>copiadas al segundo</small></div></div>
<div class="rp"><div class="db2" {d(.5)}><div class="e">💻</div><div class="n">ZenBook</div><div class="s">base de datos</div></div>
 <span class="sy fade" {d(1.2)}>⇄</span>
 <div class="db2" {d(.9)}><div class="e">🎮</div><div class="n">Legion</div><div class="s">copia exacta</div></div></div>
<div class="lat"><span class="pill pop" {d(2.6)}>⏱️ última copia: hace <b id="cnt">0.0</b> s</span></div>
<div class="ok3"><span class="pill on stamp" {d(6.6)}>⚡ cambio rápido y simple</span></div>""",
LIB + r"""const db=R.db(120,'#3ee08a');R.scene.add(db);
return t=>{const a=R.IN(t),o=R.OUT(t);db.scale.setScalar(Math.max(.001,a*(1-o)));R.at(db,870,290-o*80,4);db.rotation.set(.3,t*1.2,0)}""",
"""window.__cnt=t=>{document.getElementById('cnt').textContent=((t*1.0)%1).toFixed(1)}""")

# 1:49 · Sígueme + «¿tú qué le pondrías a hacer a una segunda computadora en tu casa?»
_q, _r = '🖥️ ¿Qué le pondrías a una 2.ª compu?', 'Un servidor de Minecraft 😅'
TARJETAS['seguir'] = (108.37, round(FIN - 108.37, 2), 'ia', V9.TARJETAS['seguir'][3],
                      V9.TARJETAS['seguir'][4].replace('🎨 ¿Cómo guardas tus referencias de diseño?', _q)
                      .replace('--n:30;', f'--n:{len(_r) + 1};').replace('En una carpeta que nunca abro 😅', _r),
LIB + r"""const lp=R.laptop(120,'#22252d','#c86bff');R.scene.add(lp);
return t=>{const a=R.IN(t),o=R.OUT(t);lp.scale.setScalar(Math.max(.001,a*(1-o)));R.at(lp,870,470-o*80,4);lp.rotation.set(.35,-.45+.5*Math.sin(t*1.2),0)}""", 380)
assert _q in TARJETAS['seguir'][4] and _r in TARJETAS['seguir'][4]


# ───────── escena a pantalla completa (tiempos locales) ─────────
def st(items, size=86, top=300):
    return G.steps(items, 0, top=top, size=size)


# 1:10 · «van a ser respaldo una de la otra: si se cae la ZenBook, la Legion toma el control (base de datos, servicios, hub) y me avisa
#        por Telegram; si se cae la Legion, la ZenBook vuelve a hacer todo»
SERV = [('🗄️', 'Base de datos', 9.8), ('⚙️', 'Servicios', 10.7), ('🧭', 'Mi hub', 11.4)]
serv = ''.join(f'<div class="sv glass" style="animation-delay:{t0}s"><span class="e">{e}</span><span class="n3">{n}</span>'
               f'<span class="en"><b class="z1">ZenBook</b><b class="lg2">Legion</b><b class="z2">ZenBook</b></span></div>' for e, n, t0 in SERV)
ESCENAS['s1-respaldo'] = (69.5, 19.1, 'fin', """
.mq{position:absolute;top:600px;width:400px;padding:30px 30px 26px;z-index:9;text-align:center;animation:pop .6s cubic-bezier(.22,1.35,.36,1) both}
.mq.zb{left:80px}.mq.lg{right:80px}
.mq .nm2{font-size:44px;font-weight:800;letter-spacing:-.03em}.mq .rol{font-size:24px;color:rgba(255,255,255,.6);margin-top:4px}
.mq .stt{margin-top:18px;height:52px;position:relative}.mq .stt span{position:absolute;left:0;right:0;margin:auto;width:max-content;font-size:26px;opacity:0}
.mq .stt .up{opacity:1}
.sync{position:absolute;left:0;right:0;top:680px;text-align:center;font-size:60px;z-index:9;color:rgba(255,255,255,.55);animation:fade .4s ease 1.6s both}
.svs{position:absolute;left:90px;right:90px;top:960px;display:grid;gap:16px;z-index:9}
.sv{display:flex;align-items:center;gap:22px;padding:22px 30px;font-size:34px;font-weight:700;animation:pop .5s cubic-bezier(.22,1.35,.36,1) both}
.sv .e{font-size:44px}.sv .n3{flex:1}.sv .en{position:relative;width:190px;height:50px}
.sv .en b{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;border-radius:25px;font-size:24px;opacity:0}
.sv .en .z1{background:rgba(255,255,255,.12);animation:fade .3s ease 0s forwards,gone .3s ease 6.2s forwards}
.sv .en .lg2{background:linear-gradient(160deg,#c9f8dc,#3ee08a);color:#032412;animation:fade .3s ease 6.4s forwards,gone .3s ease 15.6s forwards}
.sv .en .z2{background:linear-gradient(160deg,#c9f8dc,#3ee08a);color:#032412;animation:fade .3s ease 15.8s forwards}
.tgm{position:absolute;left:90px;right:90px;top:1330px;display:flex;align-items:center;gap:22px;padding:24px 30px;z-index:9;animation:pop .55s cubic-bezier(.22,1.35,.36,1) 13.0s both,gone .4s ease 14.3s forwards}
.tgm .ic2{width:72px;height:72px;border-radius:20px;background:linear-gradient(160deg,#d6ecff,#4fb4ff);display:flex;align-items:center;justify-content:center;flex-shrink:0}.tgm .ic2 svg{width:44px;height:44px}
.tgm .t1{font-size:24px;color:rgba(255,255,255,.6)}.tgm .t2{font-size:30px;font-weight:700}
.bk{position:absolute;left:0;right:0;top:1360px;text-align:center;z-index:9}.bk .pill{font-size:38px;padding:20px 40px;--r:-3deg}
""", f"""{st([('Respaldo <em>mutuo</em>', .1, 4.9), ('Si se cae la <em>ZenBook</em>…', 5.0, 14.4), ('…y si cae la <em>Legion</em>', 14.5, None)])}
<div class="mq glass zb" style="animation-delay:.4s"><div class="nm2">ZenBook</div><div class="rol">hoy hace todo</div>
 <div class="stt"><span class="pill ok up" style="animation:gone .2s ease 5.2s forwards">● en línea</span><span class="pill bad" style="animation:fade .2s ease 5.3s forwards,gone .2s ease 14.6s forwards">✕ caída</span><span class="pill" style="animation:fade .2s ease 14.7s forwards">● respaldo</span></div></div>
<div class="sync">⇄</div>
<div class="mq glass lg" style="animation-delay:.9s"><div class="nm2">Legion</div><div class="rol">la nueva</div>
 <div class="stt"><span class="pill up" style="animation:gone .2s ease 6.2s forwards">● respaldo</span><span class="pill ok" style="animation:fade .2s ease 6.3s forwards,gone .2s ease 14.6s forwards">⚡ tomó el control</span><span class="pill bad" style="animation:fade .2s ease 14.7s forwards">✕ caída</span></div></div>
<div class="svs">{serv}</div>
<div class="tgm glass"><div class="ic2">{lg('telegram', '#04203a')}</div><div><div class="t1">Telegram · ahora</div><div class="t2">La ZenBook se cayó · la Legion tomó el control</div></div></div>
<div class="bk"><span class="pill on stamp" style="animation-delay:16.4s">🔁 la ZenBook vuelve a hacer todo</span></div>""",
LIB + r"""const zb=R.laptop(260,'#b9c0cc','#6ea8ff'),lg=R.laptop(260,'#1b1e26','#c86bff');R.scene.add(zb);R.scene.add(lg);
const SB='#6ea8ff',SL='#c86bff',RED='#ff2a3a';
return t=>{const a=R.eb(R.k(t,.4,.8)),b=R.eb(R.k(t,.9,.8));
 const zd=t>5.2&&t<14.6,ld=t>14.6,sz=zd?R.k(t,5.2,.5):(t>14.6?1-R.k(t,14.6,.5):0),sl=ld?R.k(t,14.6,.5):0;
 zb.scale.setScalar(Math.max(.001,a));lg.scale.setScalar(Math.max(.001,b));
 R.at(zb,290+(sz>0&&sz<1?Math.sin(t*40)*8:0),1640+10*Math.sin(t*1.3)+sz*40,2);R.at(lg,790+(sl>0&&sl<1?Math.sin(t*40)*8:0),1640+10*Math.sin(t*1.5)+sl*40,2);
 zb.rotation.set(.35,.35+.12*Math.sin(t*.8),-.25*sz);lg.rotation.set(.35,-.35+.12*Math.sin(t*.9),.25*sl);
 zb.userData.lid.rotation.x=-.28+.9*sz;lg.userData.lid.rotation.x=-.28+.9*sl;
 zb.userData.sm.color.set(zd?RED:SB);zb.userData.sm.emissive.set(zd?RED:SB);lg.userData.sm.color.set(ld?RED:SL);lg.userData.sm.emissive.set(ld?RED:SL);
 const on=t>6.3&&t<14.6;lg.userData.sm.emissiveIntensity=on?.6+.5*Math.abs(Math.sin(t*4)):.55}""")


if __name__ == '__main__':
    solo = set(sys.argv[1:])
    todo = {**{k: ('T', v) for k, v in TARJETAS.items()}, **{k: ('E', v) for k, v in ESCENAS.items()}}
    for kid, (kind, (ini, dur, pal, css, body, js3d, *extra)) in todo.items():
        if solo and kid not in solo:
            continue
        sc = next((x for x in extra if isinstance(x, str)), '')
        top = next((x for x in extra if isinstance(x, int)), 200)
        html = G.tarjeta(css, body, dur, sc, pal=pal, js3d=js3d, top=top) if kind == 'T' else G.page(css, body, dur, sc, n=pal, js3d=js3d)
        path = f'{WORK}/{kid}.html'
        open(path, 'w').write(html)
        if os.environ.get('SOLO_HTML'):
            print('html', path, dur); continue
        r = subprocess.run(['node', CAP, path, str(dur), f'{OUT}/{PRE}{kid}.webm'], capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr[-600:], flush=True)
    if not solo:
        rel = os.environ.get('REL', 'videos/10/animaciones')
        ov = [{'file': f'{rel}/{PRE}{k}.webm', 'start': v[1][0], 'end': round(v[1][0] + v[1][1], 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for k, v in todo.items()]
        json.dump(sorted(ov, key=lambda o: o['start']), open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
