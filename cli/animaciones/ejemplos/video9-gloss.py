"""Video 9 · Datafront (bóveda de referencias de diseño → prompts) en estilo «gloss 2»: tarjetas de vidrio sobre la
cámara + escenas a pantalla completa con 3D. Reutiliza las piezas 3D del video 8 (servidor, campana, etiqueta…).
Uso: SALIDA=videos/9/animaciones REL=videos/9/animaciones python3 ejemplos/video9-gloss.py [ids…]   (SOLO_HTML=1 para revisar)
Los archivos salen con prefijo «g9-» (el editor web empareja por nombre).
"""
import importlib.util, json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import ellog_gloss as G
from ellog_gloss import js

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('v8', os.path.join(HERE, 'video8-gloss.py'))
V8 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(V8)

CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.getcwd()))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
PRE = 'g9-'
FIN = 145.67
G.PALETAS.setdefault('gris', ('#24262d', '#0b0b0e', '#8d96a8', '#e6e9ef', '141,150,168', '#111318'))


def d(s):
    return f'style="animation-delay:{s}s"'


def lg(n, c='#fff', s=None):
    return G.logo(n, c, s)


# piezas 3D: las del video 8 + destello de 4 puntas, marco de imagen y moneda
LIB = V8.LIB + r"""
R.spark=(r,col)=>R.star(4,r,r*.28,r*.35,R.iri(col,{metalness:.5,roughness:.1,opacity:1,transparent:false,emissive:col,emissiveIntensity:.15}));
R.frame=(w,col)=>{const G=R.group(),h=w*.78;G.add(R.rbox(w,h,w*.08,w*.08,R.gloss('#f6f4fb',{roughness:.25})));
 const p=R.rbox(w*.84,h*.8,w*.02,w*.05,R.gloss(col,{emissive:col,emissiveIntensity:.25,roughness:.2}));p.position.z=R.u(w*.045);G.add(p);
 const sun=new THREE.Mesh(new THREE.SphereGeometry(R.u(w*.08),24,16),R.gloss('#fff3c4',{emissive:'#ffd36b',emissiveIntensity:.6}));sun.position.set(R.u(w*.22),R.u(h*.18),R.u(w*.07));G.add(sun);
 const m=new THREE.Mesh(new THREE.ConeGeometry(R.u(w*.22),R.u(h*.36),4),R.gloss('#ffffff',{roughness:.3,transparent:true,opacity:.85}));m.position.set(R.u(-w*.12),R.u(-h*.12),R.u(w*.06));m.rotation.y=Math.PI/4;G.add(m);return G};
R.money=(r)=>{const G=R.coin(r,R.metal('#ffcf4d',{roughness:.18}));const tx=R.text('$',r*1.1,r*.12,R.metal('#fff4d0',{roughness:.12}));tx.position.z=R.u(r*.1);G.add(tx);return G};
"""

TARJETAS = {}   # id → (inicio, duración, paleta, css, body, js3d[, script][, top])
ESCENAS = {}

# 0:00 · «cada diseño que me gusta de Dribbble… me lo vuelve un prompt listo para mis IAs»
P1 = 'Tarjeta oscura, radio 16 px, violeta #7c5cd6, pestañas y bloque de comando…'
TARJETAS['c01-prompt'] = (0.2, 7.2, 'ia', f"""
.flow{{display:flex;align-items:center;gap:18px}}
.img{{width:150px;height:150px;border-radius:30px;flex-shrink:0;background:linear-gradient(160deg,#2a2233,#0d0b10);box-shadow:inset 0 0 0 2px rgba(255,255,255,.12);position:relative;overflow:hidden}}
.img:before{{content:'';position:absolute;left:14px;right:14px;top:16px;height:60px;border-radius:14px;background:radial-gradient(70% 90% at 50% 0%,#a78bfa,#2a2233)}}
.img:after{{content:'';position:absolute;left:14px;right:40px;bottom:22px;height:14px;border-radius:7px;background:linear-gradient(90deg,#7b2fd0,#d9c8f0)}}
.ar{{font-size:44px;color:rgba(255,255,255,.4)}}
.pr{{flex:1;padding:22px 24px;border-radius:30px;background:rgba(0,0,0,.35);box-shadow:inset 0 2px 10px rgba(0,0,0,.3);font-size:23px;line-height:1.35;color:rgba(255,255,255,.85);min-height:150px}}
.pr b{{display:block;font-size:20px;color:var(--ac);letter-spacing:.06em;text-transform:uppercase;margin-bottom:6px}}
.ias{{display:flex;gap:14px;margin-top:24px}}.ias .pill{{font-size:24px}}.ias svg{{width:30px;height:30px}}
""", f"""<div class="hd" style="padding-right:200px"><div class="ic">🎨</div><div class="app">Diseño → prompt<small>de Dribbble a tus IAs</small></div></div>
<div class="flow"><div class="img pop" {d(.4)}></div><span class="ar fade" {d(1.6)}>→</span>
 <div class="pr pop" {d(1.8)}><b>prompt listo</b><span class="type" style="--td:1.6s;--n:44;animation-delay:2.3s;font-family:inherit;white-space:normal">{P1}</span></div></div>
<div class="ias"><span class="pill pop" {d(5.0)}>{lg('claude', '#ffb38f')}Claude</span><span class="pill pop" {d(5.3)}>{lg('openai')}ChatGPT</span><span class="pill pop" {d(5.6)}>{lg('googlegemini', '#8ab4ff')}Gemini</span></div>""",
LIB + r"""const sp=R.spark(120,'#c9b6ff');R.scene.add(sp);
return t=>{const a=R.IN(t),o=R.OUT(t),p=Math.sin(Math.PI*R.k(t,3.0,.6));sp.scale.setScalar(Math.max(.001,a*(1-o)*(1+.15*p)));R.at(sp,860,290-o*80,4);
 sp.rotation.set(.15,.4*Math.sin(t*1.1),t*.5)}""")

# 0:14 · «se llama Datafront: entro a Dribbble, copio el diseño, cargo la imagen»
TARJETAS['c02-datafront'] = (14.2, 10.6, 'ia', """
.steps .row .num2{width:56px;height:56px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:800;
  background:rgba(255,255,255,.1);animation:lit .35s ease forwards}
@keyframes lit{to{background:linear-gradient(160deg,#e9e0ff,#a78bfa);color:#160b33;box-shadow:0 0 26px rgba(167,139,250,.6)}}
.logo2{font-size:40px;font-weight:800;letter-spacing:-.04em}.logo2 i{font-style:normal;color:var(--ac)}
""", f"""<div class="hd" style="padding-right:200px"><div class="ic">◆</div><div class="app"><span class="logo2">datafront<i>.</i></span><small>tu bóveda de referencias</small></div></div>
<div class="steps">
 <div class="row pop" {d(3.0)}><span class="num2" style="animation-delay:3.2s">1</span><div class="info"><div class="n">Entro a Dribbble</div><div class="sub">busco un diseño que me guste</div></div><span class="pill">🏀</span></div>
 <div class="row pop" {d(5.9)}><span class="num2" style="animation-delay:6.1s">2</span><div class="info"><div class="n">Lo copio</div><div class="sub">la imagen, tal cual</div></div><span class="pill">⌘C</span></div>
 <div class="row pop" {d(9.0)}><span class="num2" style="animation-delay:9.2s">3</span><div class="info"><div class="n">Cargo la imagen</div><div class="sub">en Datafront</div></div><span class="pill on">⌘V</span></div>
</div>""",
LIB + r"""const fr=R.frame(190,'#a78bfa');R.scene.add(fr);const hop=[3.2,6.1,9.2];
return t=>{const a=R.IN(t),o=R.OUT(t);let h=0;hop.forEach(x=>{h+=Math.sin(Math.PI*R.k(t,x,.45))});
 fr.scale.setScalar(Math.max(.001,a*(1-o)));R.at(fr,860,300-h*30-o*80,4);fr.rotation.set(.2,-.4+.3*Math.sin(t*1.1),-.1+.06*Math.sin(t*1.6))}""")

# 0:25 · «una vez que la cargo, en automático empieza a procesarse»
TARJETAS['c03-proceso'] = (25.4, 4.4, 'ia', """
.bar{height:26px;border-radius:13px;background:rgba(255,255,255,.08);overflow:hidden;margin-top:6px}
.bar i{display:block;height:100%;border-radius:13px;background:linear-gradient(90deg,#7b2fd0,#d9c8f0);transform-origin:left;transform:scaleX(.04);animation:go 3s cubic-bezier(.45,0,.2,1) .6s forwards;box-shadow:0 0 24px rgba(167,139,250,.6)}
@keyframes go{to{transform:scaleX(.82)}}
.st2{display:flex;justify-content:space-between;margin-top:14px;font-size:24px;color:rgba(255,255,255,.6);font-weight:600}
""", """<div class="hd" style="padding-right:200px"><div class="ic">⚙️</div><div class="app">Procesando…<small>en automático</small></div><span class="pill on pop" style="animation-delay:.2s">🖼️ imagen cargada</span></div>
<div class="bar"><i></i></div><div class="st2"><span>analizando con IA</span><span class="dot"></span></div>""",
LIB + r"""const ch=R.chip(150);R.scene.add(ch);
return t=>{const a=R.IN(t),o=R.OUT(t);ch.scale.setScalar(Math.max(.001,a*(1-o)));R.at(ch,880,300-o*80,4);ch.rotation.set(.5+.08*Math.sin(t*2),t*1.2,0)}""")

# 0:44 · «entro, selecciono uno, copio la descripción como prompt y se lo paso a la IA»
REFS = [('🗺️', 'Ruta a pie con progreso', 'viajes · oscuro'), ('🧩', 'Catálogo de modelos IA', 'ia · técnico'), ('🏙️', 'Tarjetas de destino', 'viajes · claro')]
rows = ''.join(f'<div class="row pop r{k}" {d(.6 + k * .25)}><div class="mini" style="background:linear-gradient(160deg,#2a2233,#0d0b10)">{e}</div>'
               f'<div class="info"><div class="n">{n}</div><div class="sub">{s}</div></div></div>' for k, (e, n, s) in enumerate(REFS))
TARJETAS['c04-copiar'] = (44.1, 13.6, 'ia', """
.r1{animation:pop .5s cubic-bezier(.22,1.35,.36,1) .85s both,sel .3s ease 4.6s forwards}
@keyframes sel{to{background:linear-gradient(180deg,rgba(167,139,250,.38),rgba(167,139,250,.12));box-shadow:inset 0 0 0 2px #a78bfa,0 0 40px rgba(167,139,250,.35)}}
.cp{position:relative;margin-top:22px;height:84px}
.cp span{position:absolute;inset:0;border-radius:999px;display:flex;align-items:center;justify-content:center;gap:12px;font-size:32px;font-weight:800}
.cp .a{background:linear-gradient(180deg,#e9e0ff,#a78bfa);color:#160b33;box-shadow:inset 0 2px 0 #fff,0 18px 40px rgba(167,139,250,.4);animation:pop .45s ease 5.4s both,tap .25s ease 6.0s,off .2s ease 6.2s forwards}
.cp .b{background:linear-gradient(180deg,#c9f8dc,#3ee08a);color:#032412;opacity:0;animation:fade .25s ease 6.2s forwards}
@keyframes tap{50%{transform:scale(.93)}}
.ia{display:flex;gap:16px;align-items:center;margin-top:20px;padding:20px 24px;border-radius:32px;background:rgba(0,0,0,.3);animation:pop .45s cubic-bezier(.22,1.35,.36,1) 9.6s both}
.ia .t{font-size:26px;font-weight:600}.ia svg{width:44px;height:44px;flex-shrink:0}
""", f"""<div class="hd" style="padding-right:200px"><div class="ic">◆</div><div class="app">Mis referencias<small>datafront · 29 guardadas</small></div></div>
{rows}
<div class="cp"><span class="a">📋 Copiar prompt</span><span class="b">✓ Copiado</span></div>
<div class="ia">{lg('claude', '#ffb38f')}<div class="t"><span class="type" style="--td:1.4s;--n:30;animation-delay:10.0s;font-family:inherit">Usa esta referencia de diseño…</span></div></div>""",
LIB + r"""const sp=R.spark(100,'#c9b6ff');R.scene.add(sp);
return t=>{const a=R.IN(t),o=R.OUT(t),p=Math.sin(Math.PI*R.k(t,6.0,.5));sp.scale.setScalar(Math.max(.001,a*(1-o)*(1+.25*p)));R.at(sp,880,280-o*80,4);sp.rotation.set(.15,.4*Math.sin(t),t*.6)}""")

# 1:16 · «aquí el análisis se hace una sola vez, queda guardado; es texto: lo edito y lo combino en un solo prompt»
TARJETAS['c05-texto'] = (75.9, 13.5, 'fin', """
.row .pill{font-size:23px}
.mix{display:flex;align-items:center;gap:14px;margin-top:22px}
.mix .pc{padding:16px 22px;border-radius:24px;font-size:24px;font-weight:700;background:rgba(255,255,255,.1);animation:pop .45s ease both}
.mix .pc.a{animation:pop .45s ease 9.9s both,mergeA .6s cubic-bezier(.5,0,.2,1) 11.4s forwards}.mix .pc.b{animation:pop .45s ease 10.3s both,mergeB .6s cubic-bezier(.5,0,.2,1) 11.4s forwards}
@keyframes mergeA{to{transform:translateX(120px) scale(.6);opacity:0}}@keyframes mergeB{to{transform:translateX(-60px) scale(.6);opacity:0}}
.mix .one{margin-left:auto;opacity:0;animation:stamp .45s cubic-bezier(.22,1.6,.36,1) 12.0s forwards;--r:-3deg}
@keyframes stamp{from{opacity:0;transform:scale(2.2) rotate(var(--r))}to{opacity:1;transform:rotate(var(--r))}}
""", f"""<div class="hd" style="padding-right:200px"><div class="ic">💾</div><div class="app">Análisis guardado<small>se hace una sola vez</small></div></div>
<div class="row pop" {d(.4)}><div class="mini" style="background:linear-gradient(160deg,#c9f8dc,#3ee08a)">1×</div><div class="info"><div class="n">Se analiza una vez</div><div class="sub">siempre se lee igual</div></div><span class="pill ok">✓</span></div>
<div class="row pop" {d(2.4)}><div class="mini" style="background:linear-gradient(160deg,#c9f8dc,#3ee08a)">🗂️</div><div class="info"><div class="n">Guardado y clasificado</div><div class="sub">sin buscar entre mil capturas</div></div><span class="pill ok">✓</span></div>
<div class="mix"><span class="pc a">📝 Ruta a pie</span><span class="pc b">📝 Catálogo</span><span class="pill on one">✨ un solo prompt</span></div>""",
LIB + r"""const db=R.db(140,'#3ee08a');R.scene.add(db);const lit=[.4,2.4,12.0];
return t=>{const a=R.IN(t),o=R.OUT(t);db.scale.setScalar(Math.max(.001,a*(1-o)));R.at(db,880,290-o*80,4);db.rotation.set(.35+.05*Math.sin(t),t*.6,0);
 db.userData.rings.forEach((r,i)=>r.material.emissiveIntensity=.2+1.6*R.eo(R.k(t,lit[i],.4)))}""")

# 1:46 · «si tienes alguna página de diseños, de pago o no, déjamelo en un comentario»
TARJETAS['c06-paginas'] = (106.0, 9.0, 'amb', """
.cm{display:flex;gap:18px;align-items:center;padding:22px 26px;border-radius:36px;background:rgba(0,0,0,.3);margin-top:6px}
.cm .t{font-size:28px;font-weight:600}.chips{display:flex;gap:12px;margin-top:20px}.chips .pill{font-size:25px}
.send{margin-left:auto;width:72px;height:72px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:32px;
  background:linear-gradient(160deg,#ffe6c2,#ffb340);color:#2a1603;animation:pop .4s ease 7.6s both,tap .25s ease 8.1s}
@keyframes tap{50%{transform:scale(.88)}}
""", f"""<div class="hd" style="padding-right:200px"><div class="ic">💬</div><div class="app">¿Conoces una página?<small>de diseños para inspirarme</small></div></div>
<div class="cm"><div class="mini" style="background:linear-gradient(160deg,#ffe6c2,#ffb340)">🙋</div><div><div class="sub" style="font-size:21px">Tú · ahora</div>
 <div class="t"><span class="type" style="--td:1.6s;--n:28;animation-delay:1.0s;font-family:inherit">Te recomiendo esta página…</span></div></div><span class="send">➤</span></div>
<div class="chips"><span class="pill pop" {d(5.2)}>💳 de pago ✓</span><span class="pill pop" {d(5.9)}>🆓 gratis ✓</span><span class="pill on pop" {d(7.4)}>déjamela 👇</span></div>""",
LIB + r"""const b=R.bell(100,'#ffc83d');R.scene.add(b);
return t=>{const a=R.IN(t),o=R.OUT(t),p=R.k(t,8.1,1.0),sw=p>0&&p<1?Math.sin(p*Math.PI*6)*(1-p)*.55:0;
 b.scale.setScalar(Math.max(.001,a*(1-o)));R.at(b,870,270-o*80,4);b.rotation.set(.2,-.3+.25*Math.sin(t),sw)}""")

# 2:11 · «si siempre terminas guardando capturas que nunca abres, conviértelas en algo que tu IA sí use»
TARJETAS['c07-capturas'] = (130.8, 8.5, 'ia', """
.old{animation:pop .5s cubic-bezier(.22,1.35,.36,1) .3s both,old .4s ease 3.9s forwards}@keyframes old{to{opacity:.4;filter:grayscale(1)}}
.amt{font-size:40px}
""", f"""<div class="hd" style="padding-right:200px"><div class="ic">📸</div><div class="app">Tus capturas<small>¿cuándo las abriste?</small></div></div>
<div class="row old"><div class="mini" style="background:rgba(255,255,255,.12)">🗃️</div><div class="info"><div class="n">Carpeta de capturas</div><div class="sub">nunca la vuelves a abrir</div></div><div class="amt red" id="cnt">0</div></div>
<div class="row pop" {d(4.4)}><div class="mini" style="background:linear-gradient(160deg,#e9e0ff,#a78bfa)">✨</div><div class="info"><div class="n">Prompts listos</div><div class="sub">tu IA sí los ocupa</div></div><span class="pill on">listos</span></div>""",
LIB + r"""const sp=R.spark(100,'#c9b6ff');R.scene.add(sp);
return t=>{const a=R.eb(R.k(t,4.4,.7)),o=R.OUT(t);sp.visible=t>4.3;sp.scale.setScalar(Math.max(.001,a*(1-o)));R.at(sp,880,290-o*80,4);sp.rotation.set(.15,.4*Math.sin(t),t*.6)}""",
"""window.__cnt=t=>{const p=Math.min(1,Math.max(0,(t-.6)/2.4)),e=1-Math.pow(1-p,3);document.getElementById('cnt').textContent=Math.round(347*e)}""")

# 2:19 · Sígueme + «¿tú cómo guardas tus referencias de diseño?»
TARJETAS['seguir'] = (139.4, round(FIN - 139.4, 2), 'ia', """
.tt{display:flex;align-items:center;gap:24px;padding-right:170px}
.av{width:120px;height:120px;border-radius:50%;background:linear-gradient(160deg,#e9e0ff,#a78bfa);display:flex;align-items:center;justify-content:center;font-size:56px;font-weight:800;color:#160b33;
  box-shadow:inset 0 3px 0 rgba(255,255,255,.6),0 0 0 6px rgba(255,255,255,.12),0 0 40px rgba(167,139,250,.45)}
.nm{font-size:44px;font-weight:800;letter-spacing:-.03em}
.btn{position:relative;margin-top:30px;height:96px}
.btn span{position:absolute;inset:0;border-radius:999px;display:flex;align-items:center;justify-content:center;font-size:36px;font-weight:800}
.b1{background:linear-gradient(180deg,#e9e0ff,#a78bfa);color:#160b33;box-shadow:inset 0 2px 0 #fff,0 20px 50px rgba(167,139,250,.4);animation:tap .22s ease 1.0s,off .2s ease 1.17s forwards}
.b2{background:linear-gradient(180deg,rgba(255,255,255,.18),rgba(255,255,255,.07));opacity:0;animation:fade .25s ease 1.17s forwards}
@keyframes tap{50%{transform:scale(.92)}}
.q{margin-top:22px;text-align:center}.q .pill{font-size:28px}
.cm{display:flex;gap:18px;align-items:center;margin-top:20px;padding:20px 26px;border-radius:36px;background:linear-gradient(180deg,rgba(255,255,255,.1),rgba(255,255,255,.03));animation:pop .45s cubic-bezier(.22,1.3,.36,1) 2.6s both}
.cm .mini{background:linear-gradient(160deg,#e9e0ff,#a78bfa)}.cm .t{font-size:28px;font-weight:600}
""", """<div class="tt"><div class="av">A</div><div><div class="nm">Armando</div><div class="sub">IA · homelab · código</div></div></div>
<div class="btn"><span class="b1">Seguir</span><span class="b2">Siguiendo ✓</span></div>
<div class="q pop" style="animation-delay:.5s"><span class="pill on">🎨 ¿Cómo guardas tus referencias de diseño?</span></div>
<div class="cm"><div class="mini">💬</div><div><div class="sub" style="font-size:21px">Tú · ahora</div><div class="t"><span class="type" style="--td:1.4s;--n:30;animation-delay:2.9s">En una carpeta que nunca abro 😅</span></div></div></div>""",
LIB + r"""const sp=R.spark(90,'#c9b6ff');R.scene.add(sp);
return t=>{const a=R.IN(t),o=R.OUT(t);sp.scale.setScalar(Math.max(.001,a*(1-o)));R.at(sp,870,450-o*80,4);sp.rotation.set(.15,-.45+.5*Math.sin(t*1.2),t*.5)}""", 380)


# ───────── escenas a pantalla completa (tiempos locales) ─────────
def st(items, size=86, top=300):
    return G.steps(items, 0, top=top, size=size)


# 0:07 · «gracias a esta app le estoy cambiando los diseños a las animaciones de mi editor» (Destino → Catálogo → Trayecto)
ESCENAS['s1-editor'] = (7.5, 6.6, 0, """
.mk{position:absolute;width:300px;height:420px;top:760px;z-index:9;animation:pop .6s cubic-bezier(.22,1.35,.36,1) both}
.mk.a{left:60px;--r:-6deg;transform:rotate(-6deg)}.mk.b{left:390px;top:720px}.mk.c{left:720px;--r:6deg}
.mk .in{position:absolute;inset:0;border-radius:40px;overflow:hidden;transform:rotate(var(--r,0deg));box-shadow:0 40px 90px rgba(0,0,0,.55)}
.mk.a .in{background:#fff;padding:12px}.mk.a .ph{height:100%;border-radius:30px;background:radial-gradient(120% 75% at 50% 16%,#dbe8ff,#6ea8ff 30%,#0c1a45 72%)}
.mk.a .ph:after{content:'';position:absolute;left:40px;right:40px;bottom:44px;height:46px;border-radius:999px;background:#fff}
.mk.b .in{background:#0b0b0c;box-shadow:inset 0 0 0 2px rgba(255,255,255,.08),0 40px 90px rgba(0,0,0,.55);padding:14px}
.mk.b .ph{height:58%;border-radius:20px;background:radial-gradient(120% 75% at 50% 16%,#ffe6c2,#ffb340 30%,#2a1806 80%)}
.mk.b .l{height:16px;border-radius:4px;background:#2a2a2e;margin:16px 6px 0}.mk.b .tg{display:flex;gap:8px;margin:14px 6px 0}.mk.b .tg i{width:50px;height:22px;border-radius:5px;background:rgba(124,92,214,.4)}
.mk.c .in{background:radial-gradient(60% 50% at 50% 0%,rgba(167,139,250,.6),transparent 75%),#0d0b10;box-shadow:inset 0 0 0 2px rgba(255,255,255,.15),0 40px 90px rgba(0,0,0,.55);padding:26px 22px}
.mk.c .v{font-size:40px;font-weight:300;color:#d9c8f0;margin-top:70px}.mk.c .br{height:20px;border-radius:10px;background:#2a2233;margin-top:30px;overflow:hidden}
.mk.c .br i{display:block;height:100%;width:45%;border-radius:10px;background:linear-gradient(90deg,#7b2fd0,#d9c8f0)}
.nm{position:absolute;left:0;right:0;bottom:-70px;text-align:center;font-size:30px;font-weight:800;transform:rotate(var(--r,0deg))}
.ed{position:absolute;left:0;right:0;top:1360px;text-align:center;z-index:9}.ed .pill{font-size:36px;padding:20px 40px}
""", f"""{st([('Gracias a <em>esta app</em>…', .1, 2.3), ('…cambio el <em>diseño</em><br>de mis animaciones', 2.4, None)])}
<div class="mk a" style="animation-delay:2.3s"><div class="in"><div class="ph"></div></div><div class="nm">Destino</div></div>
<div class="mk b" style="animation-delay:3.1s"><div class="in"><div class="ph"></div><div class="l"></div><div class="l" style="width:70%"></div><div class="tg"><i></i><i></i><i style="background:rgba(58,167,201,.45)"></i></div></div><div class="nm">Catálogo</div></div>
<div class="mk c" style="animation-delay:4.0s"><div class="in"><div class="v">~40 min</div><div class="br"><i></i></div></div><div class="nm">Trayecto</div></div>
<div class="ed"><span class="pill on pop" style="animation-delay:5.0s">🎬 en mi propio editor de video</span></div>""",
LIB + r"""const sp=R.spark(150,'#c9b6ff');R.scene.add(sp);
return t=>{const a=R.eb(R.k(t,.2,.9));sp.scale.setScalar(Math.max(.001,a));R.at(sp,540,1600+15*Math.sin(t*1.5),2);sp.rotation.set(.15,.5*Math.sin(t*.9),t*.7)}""")

# 0:30 · «manda la imagen junto con un prompt a la IA y extrae colores, estilo y categoría → bien clasificado»
SW = ['#0b0b0c', '#1a1a1c', '#f4f4f5', '#7c5cd6', '#3aa7c9']
sws = ''.join(f'<i style="background:{c};animation-delay:{8.4 + k * .12:.2f}s"></i>' for k, c in enumerate(SW))
ESCENAS['s2-analisis'] = (29.7, 13.9, 'ia', """
.in2{position:absolute;left:80px;right:80px;top:560px;display:flex;align-items:center;justify-content:space-between;z-index:9}
.chipimg{width:250px;height:250px;border-radius:44px;background:linear-gradient(160deg,#2a2233,#0d0b10);box-shadow:inset 0 0 0 3px rgba(255,255,255,.14),0 30px 70px rgba(0,0,0,.5);
  position:relative;animation:pop .6s cubic-bezier(.22,1.35,.36,1) .3s both,flyR .8s cubic-bezier(.5,0,.2,1) 2.4s forwards}
.chipimg:before{content:'';position:absolute;left:22px;right:22px;top:24px;height:100px;border-radius:20px;background:radial-gradient(70% 90% at 50% 0%,#a78bfa,#2a2233)}
.chipimg:after{content:'';position:absolute;left:22px;right:70px;bottom:38px;height:22px;border-radius:11px;background:linear-gradient(90deg,#7b2fd0,#d9c8f0)}
.chipp{padding:26px 30px;border-radius:36px;font-size:30px;font-weight:700;animation:pop .6s cubic-bezier(.22,1.35,.36,1) 1.6s both,flyL .8s cubic-bezier(.5,0,.2,1) 2.4s forwards}
@keyframes flyR{to{transform:translate(290px,330px) scale(.3);opacity:0}}@keyframes flyL{to{transform:translate(-280px,330px) scale(.3);opacity:0}}
.res{position:absolute;left:80px;right:80px;top:1180px;display:grid;gap:20px;z-index:9}
.o{display:flex;align-items:center;gap:24px;padding:28px 34px;animation:pop .55s cubic-bezier(.22,1.35,.36,1) both}
.o .k{font-size:26px;font-weight:700;color:rgba(255,255,255,.55);width:200px}.o .v{font-size:36px;font-weight:800}
.sw{display:flex;gap:12px}.sw i{width:56px;height:56px;border-radius:16px;box-shadow:inset 0 0 0 2px rgba(255,255,255,.2);animation:pop .4s ease both}
.ok{position:absolute;left:0;right:0;top:1700px;text-align:center;z-index:9}.ok .pill{font-size:40px;padding:20px 42px;--r:-4deg}
""", f"""{st([('Imagen + <em>prompt</em> → IA', .2, 4.9), ('Extrae <em>todo</em> el diseño', 5.0, None)])}
<div class="in2"><div class="chipimg"></div><div class="chipp glass">📝 prompt de análisis</div></div>
<div class="res">
 <div class="o glass" style="animation-delay:8.3s"><span class="k">Colores</span><div class="sw">{sws}</div></div>
 <div class="o glass" style="animation-delay:9.0s"><span class="k">Estilo</span><span class="v">oscuro · minimalista</span></div>
 <div class="o glass" style="animation-delay:10.7s"><span class="k">Categoría</span><span class="v">ia · detalle</span></div>
</div>
<div class="ok"><span class="pill on stamp" style="animation-delay:12.4s">🗂️ bien clasificado</span></div>""",
LIB + r"""const ch=R.chip(260);R.scene.add(ch);
return t=>{const a=R.eb(R.k(t,2.6,.8)),g=Math.sin(Math.PI*R.k(t,3.2,1.2));ch.scale.setScalar(Math.max(.001,a*(1+.08*g)));R.at(ch,540,960,0);
 ch.rotation.set(.55+.08*Math.sin(t*1.4),.4*Math.sin(t*.8),0);ch.children[2].material.emissiveIntensity=.35+1.2*g}""")

# 0:58 · «más fácil guardar las imágenes… sí funciona, pero cada vez la IA la vuelve a interpretar distinto»
LECT = [('«oscuro, violeta, técnico»', 10.4), ('«negro con morado, minimal»', 11.4), ('«tema dark, acentos azules»', 12.5)]
lect = ''.join(f'<div class="le glass" style="animation-delay:{t0}s"><span class="n2">#{k + 1}</span>{x}</div>' for k, (x, t0) in enumerate(LECT))
ESCENAS['s3-imagenes'] = (58.3, 17.5, 'gris', """
.p1{animation:gone .4s ease 8.6s forwards}
.fold{position:absolute;left:0;right:0;top:720px;display:flex;justify-content:center;gap:20px;z-index:9}
.ph2{width:200px;height:250px;border-radius:30px;background:linear-gradient(160deg,#3a3d48,#15161c);box-shadow:inset 0 0 0 2px rgba(255,255,255,.12),0 30px 60px rgba(0,0,0,.5);animation:pop .5s cubic-bezier(.22,1.35,.36,1) both;font-size:80px;display:flex;align-items:center;justify-content:center}
.wk{position:absolute;left:0;right:0;top:1120px;text-align:center;z-index:9}.wk .pill{font-size:38px;padding:20px 40px}
.p2{opacity:0;animation:fade .35s ease 8.75s forwards}
.les{position:absolute;left:90px;right:90px;top:980px;display:grid;gap:20px;z-index:9}
.le{display:flex;align-items:center;gap:22px;padding:28px 34px;font-size:34px;font-weight:700;animation:pop .5s cubic-bezier(.22,1.35,.36,1) both}
.le .n2{width:64px;height:64px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:800;background:rgba(255,255,255,.12)}
.ne{position:absolute;left:0;right:0;top:1520px;text-align:center;z-index:9}.ne .pill{font-size:40px;padding:20px 42px;--r:-4deg}
""", f"""<div class="p1">{st([('«Más fácil guardar<br>las <em>imágenes</em>»', .1, None)])}
 <div class="fold"><div class="ph2" style="animation-delay:3.4s">🖼️</div><div class="ph2" style="animation-delay:3.7s">🖼️</div><div class="ph2" style="animation-delay:4.0s">🖼️</div></div>
 <div class="wk"><span class="pill pop" style="animation-delay:7.0s">👍 sí, también funciona</span></div></div>
<div class="p2">{st([('Pero la IA la <em>reinterpreta</em><br>cada vez', 8.8, None)])}
 <div class="les">{lect}</div>
 <div class="ne"><span class="pill bad stamp" style="animation-delay:15.0s">🎲 nunca igual</span></div></div>""",
LIB + r"""const fr=R.frame(260,'#8d96a8');R.scene.add(fr);
return t=>{const a=R.eb(R.k(t,.4,.8)),m=R.eio(R.k(t,8.4,.8)),sp=R.k(t,10.2,4.5);fr.scale.setScalar(Math.max(.001,a*R.mix(1,.75,m)));
 R.at(fr,540,R.mix(1560,700,m),2);fr.rotation.set(.15+.05*Math.sin(t),R.mix(-.4+.3*Math.sin(t*.9),t*2.2,sp>0?Math.min(1,sp*3):0),0)}""")

# 1:30 · «estos diseños son el trabajo de alguien: estoy dispuesto a pagar Pro o por imagen; solo como referencia»
ESCENAS['s4-creditos'] = (90.3, 14.6, 'amb', """
.qt{position:absolute;left:80px;right:80px;top:560px;padding:60px 56px;z-index:9;animation:rise .7s cubic-bezier(.22,1.1,.36,1) .2s both}
.qt .tx{font-size:70px;font-weight:800;letter-spacing:-.035em;line-height:1.08;color:var(--ink)}
.qt .by{margin-top:22px;font-size:30px;font-weight:700;color:var(--ink);opacity:.7}
.pay{position:absolute;left:80px;right:80px;top:1060px;display:grid;grid-template-columns:1fr 1fr;gap:20px;z-index:9}
.py{padding:36px 30px;text-align:center;animation:pop .55s cubic-bezier(.22,1.35,.36,1) both}.py .e{font-size:60px}.py b{display:block;font-size:38px;margin-top:10px}.py .lbl{font-size:24px;margin-top:6px}
.ok{position:absolute;left:0;right:0;top:1400px;text-align:center;z-index:9}.ok .pill{font-size:36px;padding:20px 40px}
.ref{position:absolute;left:0;right:0;top:1540px;text-align:center;z-index:9}.ref .pill{font-size:40px;padding:22px 44px;--r:-3deg}
""", """<div class="qt hero"><div class="tx">Estos diseños son el trabajo de <em style="font-style:normal;text-decoration:underline;text-decoration-thickness:8px">alguien</em>.</div><div class="by">— y hay que respetarlo</div></div>
<div class="pay"><div class="py glass" style="animation-delay:6.6s"><div class="e">⭐</div><b>Cuenta Pro</b><div class="lbl">pagar la suscripción</div></div>
 <div class="py glass" style="animation-delay:8.6s"><div class="e">🖼️</div><b>Por imagen</b><div class="lbl">pagar cada diseño</div></div></div>
<div class="ok"><span class="pill pop" style="animation-delay:10.4s">🤝 sin perjudicar a ningún creador</span></div>
<div class="ref"><span class="pill on stamp" style="animation-delay:13.4s">📌 solo como referencia</span></div>""",
LIB + r"""const mn=R.money(110);R.scene.add(mn);
return t=>{const a=R.eb(R.k(t,4.4,.8)),f=R.k(t,6.4,3);mn.scale.setScalar(Math.max(.001,a));R.at(mn,860,520,5);mn.rotation.set(.3,t*2.2,.1)}""")

# 1:55 · «siguiente paso: que mi homelab busque referencias solo; yo solo apruebo o descarto… todavía no está listo»
CAND = [('🗺️', 'Panel de clima'), ('🧩', 'Dashboard cripto'), ('🏙️', 'Checkout móvil')]
cand = ''.join(f'<div class="cd glass" style="animation-delay:{4.6 + k * .5:.1f}s"><span class="e">{e}</span><span class="n3">{n}</span>'
               + (f'<span class="ok2" style="animation-delay:{9.4 + k * .5:.2f}s">✓</span></div>' if k != 1 else f'<span class="no2" style="animation-delay:{9.4 + k * .5:.2f}s">✕</span></div>') for k, (e, n) in enumerate(CAND))
ESCENAS['s5-homelab'] = (115.3, 14.9, 'fin', """
.cds{position:absolute;left:90px;right:90px;top:1060px;display:grid;gap:18px;z-index:9}
.cd{display:flex;align-items:center;gap:22px;padding:22px 30px;font-size:34px;font-weight:700;animation:pop .5s cubic-bezier(.22,1.35,.36,1) both}
.cd .e{font-size:46px}.cd .n3{flex:1}
.cd .ok2,.cd .no2{width:70px;height:70px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:34px;font-weight:800;opacity:0;animation:pop .35s cubic-bezier(.22,1.6,.36,1) forwards}
.cd .ok2{background:linear-gradient(160deg,#c9f8dc,#3ee08a);color:#032412}.cd .no2{background:linear-gradient(160deg,#ffd0d6,#ff4d5e);color:#2a0308}
.wip{position:absolute;left:0;right:0;top:1600px;text-align:center;z-index:9}.wip .pill{font-size:42px;padding:22px 44px;--r:-4deg}
""", f"""{st([('El siguiente paso', .2, 2.6), ('Mi <em>homelab</em> las busca solo', 2.7, 7.4), ('Yo solo <em>apruebo</em><br>o descarto', 7.5, None)])}
<div class="cds">{cand}</div>
<div class="wip"><span class="pill bad stamp" style="animation-delay:12.9s">🚧 todavía no está listo</span></div>""",
LIB + r"""const sv=R.server(200,'#3ee08a');R.scene.add(sv);const mg=R.mag(70);R.scene.add(mg);
return t=>{const a=R.eb(R.k(t,1.2,.8)),m=R.eb(R.k(t,4.0,.6));sv.scale.setScalar(Math.max(.001,a));R.at(sv,540,760);sv.rotation.set(.25,-.5+.2*Math.sin(t*.8),0);R.blink(sv,t);
 mg.visible=t>3.9&&t<12.6;mg.scale.setScalar(Math.max(.001,m*(1-R.eo(R.k(t,12.2,.4)))));R.at(mg,760+90*Math.sin(t*1.8),700+60*Math.cos(t*1.8),6);mg.rotation.set(.2,.3*Math.sin(t),0)}""")


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
            print('html', path); continue
        r = subprocess.run(['node', CAP, path, str(dur), f'{OUT}/{PRE}{kid}.webm'], capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr[-600:], flush=True)
    if not solo:
        rel = os.environ.get('REL', 'videos/9/animaciones')
        ov = [{'file': f'{rel}/{PRE}{k}.webm', 'start': v[1][0], 'end': round(v[1][0] + v[1][1], 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for k, v in todo.items()]
        json.dump(sorted(ov, key=lambda o: o['start']), open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
