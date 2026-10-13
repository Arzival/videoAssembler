"""El Log #02 · prueba de la dirección «gloss» (composiciones nuevas + capa 3D con three.js).
Mismos tiempos que ellog-02.py (voz recortada de noticias/2). Necesita internet al capturar (three.js y fuentes por CDN).
Uso: SALIDA=noticias/2/animaciones-gloss2 REL=noticias/2/animaciones-gloss2 python3 ejemplos/ellog-02-gloss.py [ids…]   (SOLO_HTML=1 para revisar)
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import ellog_gloss as G
from ellog_gloss import js

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.getcwd()))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
FIN = 125.08

ENTRADAS = ['Anthropic apaga el internet', 'Nadella · freno de emergencia', 'Intel y AMD · vuelve la DDR4', 'Microsoft · Maia 300']
MS = ('<svg viewBox="0 0 24 24"{st}><rect x="1" y="1" width="10.5" height="10.5" fill="#f25022"/><rect x="12.5" y="1" width="10.5" height="10.5" fill="#7fba00"/>'
      '<rect x="1" y="12.5" width="10.5" height="10.5" fill="#00a4ef"/><rect x="12.5" y="12.5" width="10.5" height="10.5" fill="#ffb900"/></svg>')
def ms(size=None):
    return MS.format(st=f' style="width:{size}px;height:{size}px"' if size else '')

SHIELD = 'M12 1.5 3.5 4.8v6.1c0 5.3 3.6 10 8.5 11.6 4.9-1.6 8.5-6.3 8.5-11.6V4.8z'
TICKET = """-webkit-mask:radial-gradient(circle 30px at 0 var(--ny,72%),#0000 97%,#000) left/51% 100% no-repeat,
  radial-gradient(circle 30px at 100% var(--ny,72%),#0000 97%,#000) right/51% 100% no-repeat"""

PIEZAS = []


def escena(pid, start, end, n, css, body, js3d=None, script='', sigue=True):
    if sigue:
        end += 0.45
    PIEZAS.append((pid, start, end, G.page(css, body, end - start, script, n=n, js3d=js3d, salida=not sigue, t0=start)))


# ───────── 0:00 · gancho
S = 0.0; A = G.at(S)
escena('e00-gancho', S, 9.3, 0, f"""
.tag{{position:absolute;left:0;right:0;top:150px;text-align:center;z-index:9}}
.pA{{animation:gone .4s ease {A(3.9)} forwards}}
.card{{position:absolute;left:70px;right:70px;top:760px;height:560px;border-radius:60px;
  background:linear-gradient(160deg,#ffb59c -30%,#e8603f 25%,#7a2117 85%);box-shadow:inset 0 2px 0 rgba(255,255,255,.5),0 60px 140px rgba(232,96,63,.4);
  animation:rise .7s cubic-bezier(.22,1.1,.36,1) .05s both,gone .4s ease {A(3.9)} forwards}}
.card:before{{content:'';position:absolute;right:-40px;top:-60px;width:420px;height:420px;border-radius:50%;filter:blur(40px);animation:siren .5s steps(1) 1s infinite}}
@keyframes siren{{0%{{background:rgba(255,40,60,.7)}}50%{{background:rgba(60,120,255,.7)}}}}
.card .tx{{position:absolute;left:56px;right:56px;bottom:60px;font-size:62px;font-weight:800;letter-spacing:-.04em;line-height:1.05;z-index:9}}
.card .tx b{{color:#ffe7dd}}
.fk{{position:absolute;left:56px;top:250px;z-index:9;font-size:34px;--r:-7deg;animation-delay:{A(2.6)}}}
.pB{{opacity:0;animation:fade .3s ease {A(4.15)} forwards}}
.beamB{{left:280px;top:560px;opacity:0;animation:fade .6s ease {A(4.4)} forwards}}
.no{{position:absolute;left:0;right:0;top:1120px;text-align:center;font-size:150px;font-weight:800;letter-spacing:-.06em;z-index:9;animation:pop .6s cubic-bezier(.22,1.35,.36,1) {A(5.0)} both}}
.no em{{font-style:normal;background:linear-gradient(180deg,#f1fbc9,#c6e64a);-webkit-background-clip:text;background-clip:text;color:transparent}}
.tr{{position:absolute;left:0;right:0;top:1340px;text-align:center;z-index:9}}.tr .pill{{font-size:34px;--r:-4deg}}
.hey{{position:absolute;left:0;right:0;top:1600px;text-align:center;z-index:9;animation:pop .5s cubic-bezier(.22,1.35,.36,1) {A(7.7)} both}}.hey .pill{{font-size:34px}}
""", f"""<div class="tag"><span class="pill fade">✦ Esta semana en El Log</span></div>
<div class="card"><div class="tx">Una IA de <b>Anthropic</b><br>le escribió a la <b>policía</b> 🚓</div></div><div class="pA"><span class="pill bad fk stamp">✕ TIP FALSO</span></div>
<div class="pB"><div class="beam beamB"></div><div class="no">¡No la <em>tires</em>!</div>
 <div class="tr"><span class="pill bad stamp" style="animation-delay:{A(6.0)}">🗑️ tu RAM DDR4 ✕</span></div></div>
<div class="hey"><span class="pill on">Ahorita te explico por qué →</span></div>""",
"const {THREE}=R;const CL=" + js(G.svgpath('claude')) + r""";
const cl=R.shape(CL,400,3,R.gloss('#f08a66',{emissive:'#a8381a',emissiveIntensity:.3}));R.scene.add(cl);
const st=R.star(5,120,56,34,R.metal('#f5c451',{roughness:.18}));R.at(st,880,780,4);R.scene.add(st);
const ram=R.ram(840);R.scene.add(ram);
return t=>{
 const a=R.eb(R.k(t,.15,.8)),out=R.eo(R.k(t,3.85,.45));
 cl.scale.setScalar(Math.max(.001,a*(1-out)));R.at(cl,540,620-out*300,3);cl.rotation.set(.25*Math.sin(t*1.3),-1.4*(1-a)+.45*Math.sin(t*1.1),.1+t*.25);
 const b=R.eb(R.k(t,1.0,.6));st.scale.setScalar(Math.max(.001,b*(1-out)));st.rotation.set(.3,Math.sin(t*2)*.6,-.2+t*.3);
 const c=R.eb(R.k(t,4.2,.9));ram.visible=t>4.1;ram.scale.setScalar(Math.max(.001,c));R.at(ram,540,800+(1-c)*500+Math.sin(t*1.6)*12);
 ram.rotation.set(.38+Math.sin(t)*.08,(1-c)*3.3+Math.sin(t*.9)*.35,-.08);
}""")

# ───────── 0:09 · intro
S = 9.3; A = G.at(S)
COLS = [G.PALETAS[k][2] for k in (1, 2, 3, 4)]
filas = ''.join(f'<div class="row glass pop" style="animation-delay:{1.5 + k * .2:.2f}s"><span class="nn" style="background:{c}">{k + 1:02d}</span>{t}</div>'
                for k, (t, c) in enumerate(zip(ENTRADAS, COLS)))
escena('e01-intro', S, 12.0, 0, """
.beam{left:280px;top:260px}
.sem{position:absolute;left:0;right:0;top:700px;text-align:center;z-index:9;animation:pop .5s cubic-bezier(.22,1.35,.36,1) .6s both}.sem .pill{font-size:30px}
.list{position:absolute;left:90px;right:90px;top:840px;display:grid;gap:20px;z-index:9}
.row{display:flex;align-items:center;gap:26px;padding:26px 34px;border-radius:999px;font-size:35px;font-weight:700}
.nn{width:66px;height:66px;border-radius:50%;color:#111;display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:800;flex-shrink:0;
  box-shadow:inset 0 2px 0 rgba(255,255,255,.6),0 0 30px rgba(255,255,255,.15)}
""", f'<div class="beam"></div><div class="sem"><span class="pill">🗓️ semana del 6 al 12 de octubre</span></div><div class="list">{filas}</div>',
r"""const tx=R.text('EL LOG',165,70,R.iri('#b9a2ff',{metalness:.85,roughness:.14,opacity:1,transparent:false,iridescence:1}));R.scene.add(tx);
return t=>{const a=R.eb(R.k(t,9.35,.75));tx.scale.setScalar(Math.max(.001,a));R.at(tx,540,500+(1-a)*200);tx.rotation.set(.18+.05*Math.sin(t*2),(1-a)*-1.8+.22*Math.sin(t*1.5),0)}""")

# ───────── 0:12 · #01 Anthropic (internet apagado → tip falso → 72 días)
S = 12.0; A = G.at(S)
evals = ''.join(f'<span class="ev" style="animation-delay:{A(14.2 + k * .12)},{A(14.8 + k * .12)}">eval-{k + 1:02d}</span>' for k in range(8))
escena('e02-anthropic', S, 31.6, 1, f"""
.p1{{animation:gone .4s ease {A(21.3)} forwards}}
.beam{{left:280px;top:430px;animation:beamOff .5s ease {A(12.95)} forwards}}@keyframes beamOff{{to{{opacity:.2}}}}
.tog{{position:absolute;left:100px;right:100px;top:1010px;padding:34px 40px;display:flex;align-items:center;gap:24px;font-size:40px;font-weight:800;animation:rise .7s cubic-bezier(.22,1.1,.36,1) {A(12.3)} both}}
.tog small{{display:block;font-size:24px;font-weight:600;color:rgba(255,255,255,.55);margin-top:4px}}.tog small b{{color:#ff6b7a;opacity:0;animation:fade .3s ease {A(13.2)} forwards}}
.sw{{margin-left:auto;width:150px;height:84px;border-radius:42px;background:linear-gradient(180deg,#ffd9cc,#ff8a6b);position:relative;box-shadow:inset 0 2px 0 rgba(255,255,255,.6),0 0 40px rgba(255,138,107,.6);
  animation:swOff .35s ease {A(12.9)} forwards}}
.sw:after{{content:'';position:absolute;top:8px;left:74px;width:68px;height:68px;border-radius:50%;background:#fff;box-shadow:0 6px 16px rgba(0,0,0,.3);animation:knob .35s ease {A(12.9)} forwards}}
@keyframes swOff{{to{{background:linear-gradient(180deg,#4a4550,#2a2730);box-shadow:inset 0 2px 0 rgba(255,255,255,.15)}}}}@keyframes knob{{to{{left:8px}}}}
.evs{{position:absolute;left:100px;right:100px;top:1230px;display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}
.ev{{padding:20px 0;text-align:center;border-radius:999px;font-size:24px;font-weight:700;background:linear-gradient(180deg,rgba(255,255,255,.16),rgba(255,255,255,.06));
  box-shadow:inset 0 1.5px 0 rgba(255,255,255,.25);animation:pop .4s ease both,evOff .3s ease forwards}}
@keyframes evOff{{to{{background:linear-gradient(180deg,#ff9aa5,#ff4d5e);color:#2a0308;box-shadow:inset 0 2px 0 rgba(255,255,255,.5),0 10px 30px rgba(255,77,94,.35)}}}}
.rep{{position:absolute;left:150px;right:150px;top:1450px;padding:36px 42px 40px;border-radius:40px;background:#f6f2ee;color:#151318;--ny:62%;{TICKET};
  box-shadow:0 40px 90px rgba(0,0,0,.5);animation:rise .7s cubic-bezier(.22,1.1,.36,1) {A(17.9)} both;z-index:9}}
.rep h4{{font-size:32px;font-weight:800}}.rep .sep{{border-top:3px dashed #d8d1c9;margin:22px 0}}
.rep .w{{display:inline-block;padding:12px 22px;border-radius:999px;background:linear-gradient(180deg,#ff9aa5,#ff4d5e);color:#2a0308;font-size:26px;font-weight:800}}
.p2{{opacity:0;animation:fade .35s ease {A(21.6)} forwards,gone .4s ease {A(27.6)} forwards}}
.form{{position:absolute;left:80px;right:80px;top:600px;padding:44px;opacity:0;animation:rise .7s cubic-bezier(.22,1.1,.36,1) {A(21.7)} forwards,gone .4s ease {A(27.6)} forwards}}
.form .bar{{display:inline-flex;font-size:26px;margin-bottom:26px}}
.form .lb{{font-size:22px;color:rgba(255,255,255,.5);font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin:20px 0 10px}}
.form .in{{padding:22px 26px;border-radius:26px;background:rgba(0,0,0,.28);box-shadow:inset 0 2px 8px rgba(0,0,0,.3);font-size:30px;font-weight:600}}
.form .ta{{min-height:150px;font-size:28px}}
.send{{margin-top:30px;font-size:30px;padding:20px 40px;animation:press .25s ease {A(24.1)} 2 alternate}}@keyframes press{{to{{transform:scale(.9)}}}}
.ok{{position:absolute;left:110px;top:560px;z-index:9;font-size:32px;--r:-6deg;animation-delay:{A(24.4)}}}
.who{{position:absolute;left:60px;right:60px;top:1330px;display:flex;justify-content:center;gap:18px;flex-wrap:wrap;z-index:9}}
.p3{{opacity:0;animation:fade .35s ease {A(27.8)} forwards}}
.hc{{position:absolute;left:70px;right:70px;top:520px;height:620px;padding:60px;animation:rise .7s cubic-bezier(.22,1.1,.36,1) {A(27.9)} both}}
.hc .lbl{{color:rgba(42,12,5,.7);font-size:30px;font-weight:700}}
.hc .num{{font-size:330px;color:#2a0c05;margin-top:30px}}.hc .num small{{font-size:70px;letter-spacing:-.03em;opacity:.55}}
.hc .bt{{position:absolute;left:60px;bottom:56px;font-size:32px;font-weight:700;color:#2a0c05}}
.tl{{position:absolute;left:70px;right:70px;top:1190px;padding:40px 50px}}
.tl .trk{{position:relative;height:18px;border-radius:9px;background:rgba(255,255,255,.12);margin:16px 20px 70px}}
.tl .fill{{position:absolute;inset:0;border-radius:9px;background:linear-gradient(90deg,#ff4d5e,#ffb340);transform-origin:left;animation:grow 1.6s ease {A(28.6)} both;box-shadow:0 0 20px rgba(255,120,80,.6)}}
@keyframes grow{{from{{transform:scaleX(0)}}}}
.tl .pt{{position:absolute;top:-12px;width:42px;height:42px;border-radius:50%;margin-left:-21px;background:#fff;box-shadow:0 0 0 8px rgba(255,255,255,.15)}}
.tl .lb2{{position:absolute;top:50px;transform:translateX(-50%);font-size:28px;font-weight:800;white-space:nowrap;text-align:center}}.tl .lb2 small{{display:block;font-size:22px;color:rgba(255,255,255,.55);font-weight:600}}
.ppd{{position:absolute;left:0;right:0;top:1500px;text-align:center;z-index:9;animation:pop .5s cubic-bezier(.22,1.35,.36,1) {A(30.2)} both}}.ppd .pill{{font-size:32px}}
""", f"""{G.header(1, G.logo('anthropic'), 'Anthropic')}
<div class="p1">
 {G.steps([('Apagó el <em>internet</em>', 12.4, 17.4), ('Acciones <em class="red">no intencionadas</em>', 17.5, None)], S, top=280, size=86)}
 <div class="beam"></div>
 <div class="tog glass"><div>Internet en vivo<small>evaluaciones de agentes · <b>APAGADO</b></small></div><div class="sw"></div></div>
 <div class="evs">{evals}</div>
 <div class="rep"><h4>📄 Informe de incidentes · Anthropic</h4><div class="sep"></div><span class="w">⚠ acciones no intencionadas de sus modelos</span></div>
</div>
<div class="form glass"><span class="pill bar">🚓 Policía de Filadelfia · casos sin resolver</span>
  <div class="lb">Caso</div><div class="in">Homicidio sin resolver</div>
  <div class="lb">Información</div><div class="in ta"><span class="type" style="--n:28;--td:1.6s;animation-delay:{A(22.4)}">Tengo datos sobre el caso…</span></div>
  <span class="pill on send">Enviar tip →</span></div>
<div class="p2">
 {G.steps([('Un <em class="red">tip falso</em> a la policía', 21.8, None)], S, top=280, size=84)}
 <span class="pill bad ok stamp">ENVIADO ✓</span>
 <div class="who"><span class="pill pop" style="animation-delay:{A(23.0)}">{G.logo('claude', '#ffb38f')} Claude Haiku 4.5</span>
  <span class="pill pop" style="animation-delay:{A(25.5)}">📍 Filadelfia</span><span class="pill pop" style="animation-delay:{A(26.5)}">📅 18 de julio</span></div>
</div>
<div class="p3">
 {G.steps([('Lo detectaron <em>2 meses</em> después', 28.0, None)], S, top=280, size=80)}
 <div class="hc hero"><div class="lbl">Tiempo sin que nadie lo notara</div><div class="num"><span id="dd">0</span><small> días</small></div>
  <div class="bt">18 jul → 28 sep</div></div>
 <div class="tl glass"><div class="trk"><div class="fill"></div>
  <span class="pt" style="left:0"></span><span class="lb2" style="left:0">18 jul<small>tip enviado</small></span>
  <span class="pt" style="left:100%;opacity:0;animation:fade .3s ease {A(30.1)} forwards"></span><span class="lb2" style="left:100%;opacity:0;animation:fade .3s ease {A(30.1)} forwards">28 sep<small>lo descubren</small></span></div></div>
 <div class="ppd"><span class="pill light">🚓 La policía lo llamó «inaceptable»</span></div>
</div>""",
r"""const {THREE}=R;
const globe=R.group();const sp=new THREE.Mesh(new THREE.SphereGeometry(R.u(200),64,48),R.gloss('#ff8a6b',{emissive:'#ff4a20',emissiveIntensity:.55,roughness:.28}));globe.add(sp);
const wf=new THREE.Mesh(new THREE.IcosahedronGeometry(R.u(212),3),new THREE.MeshBasicMaterial({color:'#ffe2d6',wireframe:true,transparent:true,opacity:.35}));globe.add(wf);
const ring=new THREE.Mesh(new THREE.TorusGeometry(R.u(300),R.u(11),24,160),R.iri('#ffffff'));ring.rotation.set(1.25,.2,0);globe.add(ring);
R.scene.add(globe);
const on=new THREE.Color('#ff8a6b'),off=new THREE.Color('#3b3742');
const star=R.star(5,150,68,40,R.metal('#f5c451',{roughness:.16}));R.scene.add(star);
return t=>{
 const a=R.eb(R.k(t,12.15,.8)),o=R.eo(R.k(t,12.95,.5)),x=R.eo(R.k(t,21.2,.45));
 globe.visible=t<21.8;globe.scale.setScalar(Math.max(.001,a*(1-x)));R.at(globe,540,690+o*30-x*400);globe.rotation.y=t*.5;wf.rotation.y=-t*.25;
 sp.material.color.copy(on).lerp(off,o);sp.material.emissiveIntensity=.55*(1-o);wf.material.opacity=.35-.22*o;
 const s=R.eb(R.k(t,21.85,.75)),sx=R.eo(R.k(t,27.5,.4));star.visible=t>21.8&&t<28.1;star.scale.setScalar(Math.max(.001,s*(1-sx)));
 R.at(star,850,590,4);star.rotation.set(.25+.1*Math.sin(t*1.5),(1-s)*4+.5*Math.sin(t*1.1),.15);
}""",
f"""window.__cnt=t=>{{t+={S};const p=Math.min(1,Math.max(0,(t-28.6)/1.6));document.getElementById('dd').textContent=Math.round(72*(1-Math.pow(1-p,3)))}}""")

# ───────── 0:31 · #01 (parte 2): 20 visas + qué hacer si usas agentes
S = 31.6; A = G.at(S)
escena('e03-visas', S, 49.75, 1, f"""
.p1{{animation:gone .4s ease {A(40.3)} forwards}}
.src{{position:absolute;left:0;right:0;top:280px;display:flex;justify-content:center;gap:16px;z-index:9}}.src .pill svg{{width:34px;height:34px}}
.cnt{{position:absolute;left:0;right:0;top:400px;text-align:center;z-index:9}}
.cnt .num{{font-size:280px;background:linear-gradient(180deg,#fff 20%,#ffd9cc 60%,#ff8a6b);-webkit-background-clip:text;background-clip:text;color:transparent}}
.cnt .lbl{{font-size:36px;font-weight:700;color:rgba(255,255,255,.75);margin-top:6px}}
.beam{{left:280px;top:820px}}
.inc{{position:absolute;left:0;right:0;top:1040px;text-align:center;z-index:9}}.inc .pill{{font-size:56px;padding:22px 46px;--r:-8deg;animation-delay:{A(39.2)}}}
.dep{{position:absolute;left:0;right:0;top:1500px;display:flex;justify-content:center;gap:16px;z-index:9}}
.p2{{opacity:0;animation:fade .35s ease {A(40.5)} forwards}}
.chk{{position:absolute;left:90px;right:90px;top:900px;display:grid;gap:22px;z-index:9}}
.it{{display:flex;align-items:center;gap:26px;padding:30px 34px;border-radius:999px;font-size:44px;font-weight:800;animation:pop .55s cubic-bezier(.22,1.35,.36,1) both}}
.it .e{{font-size:56px;width:70px;text-align:center}}
.it .ck{{margin-left:auto;width:76px;height:76px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:40px;font-weight:900;
  background:rgba(255,255,255,.1);color:transparent;animation:ckOn .4s cubic-bezier(.22,1.6,.36,1) both}}
@keyframes ckOn{{from{{transform:scale(.5)}}to{{background:linear-gradient(160deg,#ffd9cc,#ff8a6b);color:#2a0c05;box-shadow:inset 0 2px 0 rgba(255,255,255,.6),0 0 30px rgba(255,138,107,.6);transform:none}}}}
.nope{{position:absolute;left:0;right:0;top:1500px;text-align:center;z-index:9;animation:pop .5s cubic-bezier(.22,1.5,.36,1) {A(46.3)} both}}.nope .pill{{font-size:36px}}.nope svg{{width:36px;height:36px}}
""", f"""{G.header(1, G.logo('anthropic'), 'Anthropic')}
<div class="p1">
 <div class="src"><span class="pill pop" style="animation-delay:{A(32.0)}">{G.logo('newyorktimes', '#fff')} The New York Times</span><span class="pill pop" style="animation-delay:{A(33.4)}">✍️ vía Simon Willison</span></div>
 <div class="cnt fade" style="animation-delay:{A(35.6)}"><div class="num" id="vn">0</div><div class="lbl">solicitudes de visa 🇺🇸</div></div>
 <div class="beam"></div>
 <div class="inc"><span class="pill bad stamp">INCOMPLETAS</span></div>
 <div class="dep"><span class="pill pop" style="animation-delay:{A(38.9)}">🏛️ Departamento de Estado</span><span class="pill light pop" style="animation-delay:{A(39.4)}">ninguna se procesó</span></div>
</div>
<div class="p2">
 {G.steps([('¿Usas <em>agentes</em>?', 40.7, None)], S, top=280, size=104)}
 <div class="chk">
  <div class="it glass" style="animation-delay:{A(43.3)}"><span class="e">🧱</span>Aislamiento<span class="ck" style="animation-delay:{A(44.5)}">✓</span></div>
  <div class="it glass" style="animation-delay:{A(45.3)}"><span class="e">🔑</span>Permisos<span class="ck" style="animation-delay:{A(45.8)}">✓</span></div>
  <div class="it glass" style="animation-delay:{A(48.0)}"><span class="e">👀</span>Supervisa tus modelos<span class="ck" style="animation-delay:{A(49.0)}">✓</span></div></div>
 <div class="nope"><span class="pill light">y no seas como {G.logo('anthropic', '#151318')} Anthropic 😅</span></div>
</div>""",
"const {THREE}=R;const SH=" + js(SHIELD) + r""";
const P=[];const em=R.metal('#e9c05a',{roughness:.22});const cov=R.gloss('#1e3170',{roughness:.4,clearcoat:.8});
let seed=11;const rnd=()=>{seed=(seed*16807)%2147483647;return seed/2147483647};
for(let k=0;k<20;k++){const g=R.group();g.add(R.rbox(240,330,16,16,cov));
 const e=new THREE.Mesh(new THREE.TorusGeometry(R.u(46),R.u(6),16,48),em);e.position.set(0,R.u(35),R.u(9));g.add(e);
 const e2=new THREE.Mesh(new THREE.CircleGeometry(R.u(22),32),em);e2.position.set(0,R.u(35),R.u(9));g.add(e2);
 const b=R.rbox(130,12,4,4,em);b.position.set(0,R.u(-80),R.u(9));g.add(b);const b2=R.rbox(90,10,4,4,em);b2.position.set(0,R.u(-110),R.u(9));g.add(b2);
 g.userData={x:540+(rnd()-.5)*460,y:1180+(rnd()-.5)*200,r:(rnd()-.5)*.9,t:35.9+k*.09,z:k*.08};R.scene.add(g);P.push(g)}
const sh=R.shape(SH,330,5,R.gloss('#e8603f',{emissive:'#ff5a3a',emissiveIntensity:0,roughness:.18}));R.scene.add(sh);
return t=>{
 const x=R.eo(R.k(t,40.2,.5));
 for(const g of P){const d=g.userData,e=R.eb(R.k(t,d.t,.55));g.visible=t>=d.t&&t<40.8;
  R.at(g,d.x,d.y-(1-e)*900+x*900,d.z);g.rotation.set(.2-.5*(1-e),(1-e)*1.4,d.r*e)}
 const s=R.eb(R.k(t,40.85,.75));sh.visible=t>40.8;sh.scale.setScalar(Math.max(.001,s));R.at(sh,540,630,2);sh.rotation.set(.18+.08*Math.sin(t),(1-s)*3+.55*Math.sin(t*1.2),.05);
 sh.material.emissiveIntensity=(R.k(t,44.5,.4)+R.k(t,45.8,.4)+R.k(t,49.0,.4))/3*.45;
}""",
f"""window.__cnt=t=>{{t+={S};document.getElementById('vn').textContent=Math.max(0,Math.min(20,Math.floor((t-35.9)/.09)+1))}}""")

# ───────── 0:50 · #02 Nadella
S = 49.75; A = G.at(S)
words = ''.join(f'<span class="w" style="animation-delay:{A(53.2 + k * .2)}">{w} </span>' for k, w in enumerate('Asume que todos los modelos de IA están comprometidos.'.split()))
escena('e04-nadella', S, 72.8, 2, f"""
.p1{{animation:gone .4s ease {A(56.7)} forwards}}
.tw{{position:absolute;left:70px;right:70px;top:500px;height:740px;padding:60px 56px;animation:rise .7s cubic-bezier(.22,1.1,.36,1) {A(50.0)} both,gone .4s ease {A(56.7)} forwards;
  background:linear-gradient(165deg,#9cc2ff -20%,#3b6fd8 25%,#173077 70%,#0b1638);box-shadow:inset 0 2px 0 rgba(255,255,255,.5),0 60px 140px rgba(59,111,216,.45)}}
.tw .who{{display:flex;align-items:center;gap:22px}}
.tw .av{{width:110px;height:110px;border-radius:50%;background:linear-gradient(160deg,#fff,#c9d8f5);color:#173077;display:flex;align-items:center;justify-content:center;font-size:42px;font-weight:800;
  box-shadow:inset 0 -4px 0 rgba(0,0,0,.1),0 10px 30px rgba(0,0,0,.3)}}
.tw .nm{{font-size:38px;font-weight:800}}.tw .nm small{{display:block;font-size:27px;font-weight:600;color:rgba(255,255,255,.65)}}
.tw .tx{{font-size:66px;font-weight:800;letter-spacing:-.035em;line-height:1.08;margin-top:50px}}.tw .w{{opacity:0;animation:fade .25s ease forwards}}
.tw .ft{{position:absolute;left:56px;bottom:50px;display:flex;gap:14px}}.tw .ft .pill{{font-size:24px;padding:12px 22px}}.tw .ft svg{{width:26px;height:26px}}
.ceo{{position:absolute;left:0;right:0;top:1310px;text-align:center;z-index:9}}.ceo .pill{{font-size:32px}}
.p2{{opacity:0;animation:fade .35s ease {A(57.0)} forwards,gone .4s ease {A(65.1)} forwards}}
.beam{{left:280px;top:560px}}
.flow{{position:absolute;left:0;right:0;top:1180px;display:flex;justify-content:center;gap:18px;z-index:9}}.flow .pill{{font-size:34px}}
.acc{{position:absolute;left:0;right:0;top:1350px;text-align:center;z-index:9}}.acc .pill{{font-size:40px;padding:20px 40px;--r:-5deg;animation-delay:{A(62.8)}}}
.p3{{opacity:0;animation:fade .35s ease {A(65.3)} forwards}}
.arq{{position:absolute;left:70px;right:70px;top:440px;display:grid;grid-template-columns:1fr 1fr;gap:20px;z-index:9}}
.ly{{padding:34px 30px;text-align:left;animation:pop .5s cubic-bezier(.22,1.35,.36,1) both}}
.ly .e{{width:84px;height:84px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:44px;background:linear-gradient(160deg,#dbe8ff,#6ea8ff);box-shadow:inset 0 2px 0 #fff,0 0 30px rgba(110,168,255,.5)}}
.ly b{{display:block;font-size:36px;margin-top:22px}}.ly span{{font-size:24px;color:rgba(255,255,255,.6);font-weight:600}}
.log{{grid-column:1/3;padding:26px 34px;font-size:26px;font-weight:600;line-height:1.75;animation:pop .5s ease {A(68.0)} both}}
.log .r{{display:flex;justify-content:space-between}}.log .t{{color:rgba(255,255,255,.45);font-variant-numeric:tabular-nums;margin-right:18px}}
.paused{{position:absolute;left:0;right:0;top:1580px;text-align:center;z-index:9;opacity:0;animation:pop .45s cubic-bezier(.22,1.35,.36,1) {A(71.2)} forwards}}.paused .pill{{font-size:32px}}
""", f"""{G.header(2, ms(), 'Microsoft')}
<div class="tw"><div class="who"><div class="av">SN</div><div class="nm">Satya Nadella<small>CEO de Microsoft</small></div></div>
  <div class="tx">“{words}”</div>
  <div class="ft"><span class="pill">{G.logo('x', '#fff')} @satyanadella</span><span class="pill">10 oct 2026</span></div></div>
<div class="p1">
 {G.steps([('Satya <em>Nadella</em>', 50.0, None)], S, top=280, size=96)}
 <div class="ceo"><span class="pill pop" style="animation-delay:{A(51.0)}">{ms(32)} el jefe de Microsoft</span></div>
</div>
<div class="p2">
 {G.steps([('Ya no son <em>cajas negras</em>', 57.4, None)], S, top=280, size=86)}
 <div class="beam"></div>
 <div class="flow"><span class="pill pop" style="animation-delay:{A(60.8)}">💬 consejos</span><span class="pill on pop" style="animation-delay:{A(61.4)}">⚡ acciones</span></div>
 <div class="acc"><span class="pill bad stamp">ACEPTADO SIN REVISAR ✕</span></div>
</div>
<div class="p3">
 {G.steps([('Arquitectura de <em>confianza</em>', 65.6, 69.9), ('Freno de <em class="red">emergencia</em>', 70.0, None)], S, top=280, size=82)}
 <div class="arq"><div class="ly glass" style="animation-delay:{A(66.4)}"><div class="e">🧠</div><b>Modelo</b><span>contenido desde el inicio</span></div>
  <div class="ly glass" style="animation-delay:{A(66.8)}"><div class="e">⚙️</div><b>Orquestación</b><span>separada del modelo</span></div>
  <div class="log glass"><div class="r"><span><span class="t">12:04:11</span>abrir_navegador</span><span class="g">✓</span></div>
   <div class="r"><span><span class="t">12:04:13</span>enviar_formulario</span><span class="red">⏸ requiere humano</span></div></div></div>
 <div class="paused"><span class="pill bad">● modelo en pausa a mitad de la tarea</span></div>
</div>""",
r"""const {THREE}=R;
const knot=new THREE.Mesh(new THREE.TorusKnotGeometry(R.u(120),R.u(44),240,40,2,3),R.iri('#cfe0ff',{opacity:1,transparent:false,metalness:.5}));R.scene.add(knot);
const bm=new THREE.MeshPhysicalMaterial({color:'#07080b',roughness:.12,metalness:.3,clearcoat:1,transparent:true,opacity:1});
const box=R.rbox(400,400,400,46,bm);R.scene.add(box);
const core=new THREE.Mesh(new THREE.IcosahedronGeometry(R.u(115),1),R.gloss('#6ea8ff',{emissive:'#3d7bff',emissiveIntensity:1.3,flatShading:true}));box.add(core);
const blk=new THREE.Color('#07080b'),clr=new THREE.Color('#a9c8ff');
const btn=R.group();btn.add(new THREE.Mesh(new THREE.CylinderGeometry(R.u(240),R.u(262),R.u(80),96),R.gloss('#16161b',{roughness:.3})));
const ring=new THREE.Mesh(new THREE.TorusGeometry(R.u(212),R.u(20),24,96),R.gloss('#ffcc00',{roughness:.25}));ring.rotation.x=Math.PI/2;ring.position.y=R.u(42);btn.add(ring);
const dome=new THREE.Mesh(new THREE.SphereGeometry(R.u(188),64,32,0,Math.PI*2,0,Math.PI/2),R.gloss('#ff2a2a',{emissive:'#ff0000',emissiveIntensity:.15,roughness:.12}));dome.position.y=R.u(38);dome.scale.y=.62;btn.add(dome);
btn.rotation.x=.62;R.scene.add(btn);
const glow=new THREE.PointLight('#ff3030',0,50);R.scene.add(glow);R.at(glow,540,1150,8);
return t=>{
 const a=R.eb(R.k(t,50.3,.9)),ax=R.eo(R.k(t,56.6,.4));knot.visible=t<57.1;knot.scale.setScalar(Math.max(.001,a*(1-ax)));R.at(knot,900,610,3);knot.rotation.set(t*.3,t*.45,.2);
 const b=R.eb(R.k(t,58.9,.75)),bx=R.eo(R.k(t,65.0,.4)),cl=R.eio(R.k(t,59.7,1.0));box.visible=t>58.8&&t<65.5;box.scale.setScalar(Math.max(.001,b*(1-bx)));R.at(box,540,800);
 box.rotation.set(.5+.1*Math.sin(t),t*.45+.6,0);bm.opacity=1-.8*cl;bm.color.copy(blk).lerp(clr,cl);core.scale.setScalar(Math.max(.001,cl));core.rotation.set(t,t*1.3,0);
 const c=R.eb(R.k(t,70.0,.75)),press=Math.sin(Math.PI*R.k(t,70.9,.3));btn.visible=t>69.9;btn.scale.setScalar(Math.max(.001,c));R.at(btn,540,1250);dome.position.y=R.u(38-44*press);
 const pulse=t>71.2?(.5+.5*Math.sin((t-71.2)*8)):0;dome.material.emissiveIntensity=.15+1.3*pulse;glow.intensity=pulse*500;
}""")

# ───────── 1:13 · #03 Intel y AMD vuelven a la DDR4
S = 72.8; A = G.at(S)
escena('e05-ddr4', S, 93.95, 3, f"""
.p1{{animation:gone .4s ease {A(87.1)} forwards}}
.ch{{position:absolute;left:90px;right:90px;top:470px;height:560px;padding:40px 50px;animation:rise .7s cubic-bezier(.22,1.1,.36,1) {A(74.1)} both,gone .4s ease {A(76.5)} forwards}}
.ch .lbl{{font-size:26px}}
.bars{{position:absolute;left:50px;right:50px;bottom:40px;height:400px;display:flex;justify-content:center;align-items:flex-end;gap:110px}}
.bar{{width:190px;position:relative;text-align:center}}
.bar i{{display:block;border-radius:30px;transform-origin:bottom;animation:up 1s cubic-bezier(.22,1.1,.36,1) both}}@keyframes up{{from{{transform:scaleY(0)}}}}
.bar b{{position:absolute;left:50%;transform:translateX(-50%);white-space:nowrap;font-size:40px;padding:12px 26px;border-radius:999px;opacity:0;animation:fade .3s ease forwards}}
.bar span{{display:block;margin-top:14px;font-size:30px;font-weight:800}}
.hot{{font-size:56px;position:absolute;right:50px;top:30px;animation:pop .5s cubic-bezier(.22,1.6,.36,1) {A(75.6)} both}}
.beam{{left:280px;top:380px;opacity:0;animation:fade .6s ease {A(77.0)} forwards}}
.cpuL{{position:absolute;top:1250px;width:300px;text-align:center;z-index:9}}.cpuL .lbl{{font-size:26px}}
.sup{{position:absolute;left:0;right:0;top:1340px;text-align:center;z-index:9}}.sup .pill{{font-size:36px;padding:20px 40px}}
.sts{{position:absolute;left:70px;right:70px;top:1480px;display:grid;grid-template-columns:1fr 1fr;gap:20px;z-index:9}}
.stc{{padding:30px 34px;border-radius:40px;animation:pop .55s cubic-bezier(.22,1.35,.36,1) both}}.stc .lbl{{font-size:24px}}
.stc .num{{font-size:84px;margin-top:10px}}.stc .num.s{{font-size:46px;letter-spacing:-.03em;line-height:1.1;margin-top:18px}}
.p2{{opacity:0;animation:fade .35s ease {A(87.3)} forwards}}
.trash{{position:absolute;left:50%;top:1290px;width:220px;height:220px;margin-left:-110px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:110px;
  animation:pop .5s cubic-bezier(.22,1.35,.36,1) {A(87.5)} both,gone .4s ease {A(89.7)} forwards}}
.save{{position:absolute;left:0;right:0;top:1200px;text-align:center;z-index:9;animation:pop .6s cubic-bezier(.22,1.5,.36,1) {A(91.6)} both}}
.save .pill{{font-size:76px;padding:30px 64px}}.save .lbl{{margin-top:26px;font-size:30px}}
""", f"""{G.header(3, G.logo('intel', '#fff'), 'Intel + AMD')}
<div class="p1">
 {G.steps([('La RAM está <em class="red">carísima</em>', 73.4, 76.7), ('Vuelve la <em>DDR4</em>', 76.8, None)], S, top=280, size=92)}
 <div class="ch glass"><div class="lbl">Kit de 32 GB · precio aprox.</div><span class="hot">🔥</span>
  <div class="bars"><div class="bar"><b class="pill bad" style="top:-80px;animation-delay:{A(75.3)}">$480</b><i style="height:300px;background:linear-gradient(180deg,#ffb0a0,#ff4d5e);box-shadow:0 0 50px rgba(255,77,94,.5);animation-delay:{A(74.6)}"></i><span>DDR5</span></div>
   <div class="bar"><b class="pill on" style="top:90px;animation-delay:{A(75.6)}">$210</b><i style="height:130px;background:linear-gradient(180deg,#f1fbc9,#c6e64a);box-shadow:0 0 50px rgba(198,230,74,.5);animation-delay:{A(74.9)}"></i><span>DDR4</span></div></div></div>
 <div class="beam"></div>
 <div class="sup"><span class="pill on pop" style="animation-delay:{A(81.4)}">✓ con soporte para DDR4</span></div>
 <div class="sts"><div class="stc glass" style="animation-delay:{A(84.2)}"><div class="lbl">Memoria</div><div class="num s">⏮ generación anterior</div></div>
  <div class="stc glass" style="animation-delay:{A(85.9)}"><div class="lbl">Precio por GB</div><div class="num g">−56<span class="d">%</span></div></div></div>
</div>
<div class="trash glass">🗑️</div>
<div class="p2">
 {G.steps([('<em>No</em> tires tu DDR4', 89.6, None)], S, top=280, size=104)}
 <div class="save"><span class="pill on">+ una lanita 💸</span><div class="lbl">al armar o actualizar tu PC (y tu homelab)</div></div>
</div>""",
"const {THREE}=R;const INTEL=" + js(G.svgpath('intel')) + ";const AMD=" + js(G.svgpath('amd')) + r""";
const ram=R.ram(760);R.scene.add(ram);
const cpu=(lg,col)=>{const g=R.chip(290,'#c9ccd3','#1a1d22','#c6e64a');const l=R.shape(lg,170,1,R.gloss(col,{roughness:.2}),.15);l.position.z=R.u(44);g.add(l);R.scene.add(g);return g};
const ci=cpu(INTEL,'#2f8fff'),ca=cpu(AMD,'#f2f2f2');
const coins=[];const gm=R.metal('#f3c64f',{roughness:.18});for(let i=0;i<12;i++){const c=R.coin(52,gm);c.userData={a:i/12*Math.PI*2+.3,s:.75+((i*37)%10)/14};R.scene.add(c);coins.push(c)}
return t=>{
 const a=R.eb(R.k(t,76.9,.85));ram.visible=t>76.8;
 const d=R.k(t,88.0,1.6),drop=d>0&&d<1?Math.sin(Math.PI*d):0,m=R.eio(R.k(t,87.2,.6));
 ram.scale.setScalar(Math.max(.001,a*R.mix(1,1.12,m)));
 R.at(ram,540,R.mix(640,780,m)+drop*480+Math.sin(t*1.5)*10);ram.rotation.set(.32+Math.sin(t*.8)*.08+drop*1.1,(1-a)*3.14+Math.sin(t*.7)*.4,-.06+drop*.7);
 for(const [g,t0,x] of [[ci,77.2,300],[ca,77.7,780]]){const p=R.eb(R.k(t,t0,.75)),o=R.eo(R.k(t,87.0,.4));g.visible=t>t0&&t<87.5;g.scale.setScalar(Math.max(.001,p*(1-o)));
  R.at(g,x,1070);g.rotation.set(-.55+.08*Math.sin(t+t0),.3*Math.sin(t*.8+t0),0)}
 for(const c of coins){const p=R.k(t,91.6,1.6),e=R.eo(p),u=c.userData;c.visible=t>91.55;const r=e*8*u.s;
  c.position.set(Math.cos(u.a)*r,(960-780)/R.PX+Math.sin(u.a)*r*1.1-p*p*4,2);c.rotation.set(t*3*u.s,t*2,0);c.scale.setScalar(Math.max(.001,R.eb(R.k(t,91.6,.35))))}
}""")

# ───────── 1:34 · #04 Microsoft Maia 300
S = 93.95; A = G.at(S)
escena('e06-maia', S, 118.6, 4, f"""
.beam{{left:280px;top:520px;animation:bm .7s cubic-bezier(.6,0,.2,1) {A(99.6)} forwards}}@keyframes bm{{to{{transform:translateY(-200px) scale(.6)}}}}
.gen{{position:absolute;left:60px;right:60px;top:1230px;display:flex;justify-content:center;gap:16px;flex-wrap:wrap;z-index:9;animation:gone .4s ease {A(99.4)} forwards}}.gen .pill{{font-size:32px}}
.p2{{opacity:0;animation:fade .35s ease {A(99.8)} forwards,gone .4s ease {A(104.3)} forwards}}
.inf{{position:absolute;left:0;right:0;top:850px;text-align:center;z-index:9}}.inf .pill{{font-size:34px}}
.svc{{position:absolute;left:70px;right:70px;top:990px;display:grid;grid-template-columns:repeat(3,1fr);gap:20px;z-index:9}}
.sv{{padding:40px 20px;text-align:center;font-size:30px;font-weight:800;animation:pop .5s cubic-bezier(.22,1.35,.36,1) both}}
.sv .e{{width:100px;height:100px;margin:0 auto 18px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:50px;background:rgba(255,255,255,.1);box-shadow:inset 0 2px 0 rgba(255,255,255,.3)}}
.sv .e svg{{width:56px;height:56px}}
.p3{{opacity:0;animation:fade .35s ease {A(104.6)} forwards,gone .4s ease {A(112.8)} forwards}}
.big{{position:absolute;left:70px;right:70px;top:850px;display:grid;grid-template-columns:1fr 1fr;gap:20px;z-index:9}}
.kp{{padding:40px 36px;animation:pop .5s cubic-bezier(.22,1.35,.36,1) both}}.kp .num{{font-size:150px;margin:16px 0 10px}}.kp .lbl{{font-size:26px}}
.kp.hero .num,.kp.hero .lbl{{color:var(--ink)}}
.dep{{position:absolute;left:70px;right:70px;top:1220px;padding:40px 44px;z-index:9;animation:pop .5s ease {A(109.4)} both}}
.dep .r{{display:flex;justify-content:space-between;align-items:center;font-size:32px;font-weight:800;margin-bottom:22px}}.dep .r svg{{width:56px;height:56px}}
.dep .trk{{height:50px;border-radius:25px;background:rgba(255,255,255,.08);overflow:hidden}}
.dep .trk i{{display:block;height:100%;width:92%;border-radius:25px;background:linear-gradient(90deg,#76b900,#b6f03a);box-shadow:0 0 30px rgba(118,185,0,.5);transform-origin:left;animation:shrink 1.4s ease {A(110.6)} both}}
@keyframes shrink{{to{{transform:scaleX(.42)}}}}
.dep .ms{{display:flex;align-items:center;gap:14px;margin-top:24px;font-size:28px;font-weight:700;opacity:0;animation:fade .3s ease {A(111.6)} forwards}}
.p4{{opacity:0;animation:fade .35s ease {A(113.0)} forwards}}
.az{{position:absolute;left:90px;right:90px;top:850px;padding:44px 50px 50px;border-radius:44px;background:#f6f2ee;color:#151318;--ny:30%;{TICKET};
  box-shadow:0 40px 90px rgba(0,0,0,.5);z-index:9;animation:rise .7s cubic-bezier(.22,1.1,.36,1) {A(113.3)} both}}
.az .h{{display:flex;align-items:center;gap:18px;font-size:36px;font-weight:800}}.az .h svg{{width:60px;height:60px}}
.az .sep{{border-top:3px dashed #d8d1c9;margin:34px 0 14px}}
.az .ln{{display:flex;justify-content:space-between;align-items:center;padding:22px 0;font-size:34px;font-weight:700}}
.az .ln b{{width:76px;height:76px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:38px;color:#032231;background:linear-gradient(160deg,#d3f4ff,#4fd2ff)}}
.when{{position:absolute;left:0;right:0;top:1400px;text-align:center;z-index:9}}.when .pill{{font-size:34px}}
""", f"""{G.header(4, ms(), 'Microsoft')}
{G.steps([('Microsoft <em>Maia 300</em>', 94.2, 104.4), ('Más <em>barato</em> y <em>eficiente</em>', 104.5, 112.9), ('¿Usas <em>Azure</em>?', 113.0, None)], S, top=280, size=86)}
<div class="beam"></div>
<div class="gen"><span class="pill pop" style="animation-delay:{A(97.2)}">3ª generación</span><span class="pill pop" style="animation-delay:{A(97.7)}">TSMC 2 nm</span>
 <span class="pill pop" style="animation-delay:{A(98.2)}">8× HBM4</span><span class="pill on pop" style="animation-delay:{A(98.8)}">🧠 para IA</span></div>
<div class="p2"><div class="inf"><span class="pill on pop" style="animation-delay:{A(101.6)}">⚡ su chip principal de inferencia</span></div>
 <div class="svc"><div class="sv glass" style="animation-delay:{A(102.8)}"><div class="e">✦</div>Copilot</div>
  <div class="sv glass" style="animation-delay:{A(103.1)}"><div class="e">{G.logo('microsoftazure', '#4fd2ff')}</div>Azure</div>
  <div class="sv glass" style="animation-delay:{A(103.4)}"><div class="e">🧩</div>Servicios</div></div></div>
<div class="p3"><div class="big">
 <div class="kp hero" style="animation-delay:{A(105.4)}"><div class="lbl">Tokens por rack</div><div class="num" id="k1">1×</div></div>
 <div class="kp glass" style="animation-delay:{A(107.4)}"><div class="lbl">Eficiencia por megawatt</div><div class="num g" id="k2">+0%</div></div></div>
 <div class="dep glass"><div class="r"><span>Dependencia de <span style="color:#9be22e">NVIDIA</span></span>{G.logo('nvidia', '#76b900')}</div><div class="trk"><i></i></div>
  <div class="ms">{ms(32)} más chips propios = <span class="g">menos GPUs de NVIDIA</span></div></div></div>
<div class="p4"><div class="az"><div class="h">{G.logo('microsoftazure', '#0089d6')}Azure · lo que puede cambiar</div><div class="sep"></div>
 <div class="ln pop" style="animation-delay:{A(115.5)}"><span>💵 Lo que pagas</span><b>↓</b></div>
 <div class="ln pop" style="animation-delay:{A(117.2)}"><span>📦 Lo que tienes disponible</span><b>↑</b></div></div>
 <div class="when"><span class="pill pop" style="animation-delay:{A(114.2)}">📅 en producción desde 2027</span></div></div>""",
r"""const {THREE}=R;
const chip=R.chip(500,'#2a3446','#0b2a40','#4fd2ff');
const tx=R.text('MAIA',64,12,R.metal('#eaf8ff',{roughness:.12}));tx.position.set(0,R.u(16),R.u(62));chip.add(tx);
const t3=R.text('300',40,8,R.gloss('#4fd2ff',{emissive:'#4fd2ff',emissiveIntensity:.8}));t3.position.set(0,R.u(-52),R.u(60));chip.add(t3);
R.scene.add(chip);
const ring=new THREE.Mesh(new THREE.TorusGeometry(R.u(430),R.u(7),16,200),R.iri('#c8f2ff',{opacity:1,transparent:false}));R.scene.add(ring);
const ring2=new THREE.Mesh(new THREE.TorusGeometry(R.u(500),R.u(4),16,200),R.iri('#ffffff',{opacity:.7}));R.scene.add(ring2);
return t=>{
 const a=R.eb(R.k(t,94.6,.85)),m=R.eio(R.k(t,99.6,.7));const y=R.mix(780,560,m),s=R.mix(1,.56,m)*a;
 chip.scale.setScalar(Math.max(.001,s));R.at(chip,540,y);chip.rotation.set(-.32+.08*Math.sin(t*.9),.38*Math.sin(t*.6)+(1-a)*2.6,.04);
 for(const [r,o] of [[ring,0],[ring2,1]]){r.scale.setScalar(Math.max(.001,s));R.at(r,540,y,-3);r.rotation.set(1.2+o*.15,o*.3,t*(.35+o*.2))}
}""",
f"""window.__cnt=t=>{{t+={S};const e=(s,d)=>1-Math.pow(1-Math.min(1,Math.max(0,(t-s)/d)),3);
document.getElementById('k1').innerHTML=(1+6*e(105.8,1.2)).toFixed(0)+'<span class="d">×</span>';document.getElementById('k2').innerHTML='+'+Math.round(40*e(107.8,1.2))+'<span class="d">%</span>'}}""")

# ───────── 1:59 · cierre (arriba queda la tarjeta «Sígueme»)
S = 118.6
filas = ''.join(f'<div class="row glass pop" style="animation-delay:{.3 + k * .2:.2f}s"><span class="ck" style="background:{c};box-shadow:inset 0 2px 0 rgba(255,255,255,.6),0 0 26px {c}">✓</span>{t}</div>'
                for k, (t, c) in enumerate(zip(ENTRADAS, COLS)))
escena('e07-cierre', S, FIN, 0, """
.list{position:absolute;left:90px;right:90px;top:690px;display:grid;gap:18px;z-index:9}
.row{display:flex;align-items:center;gap:24px;padding:24px 32px;border-radius:999px;font-size:32px;font-weight:700}
.ck{width:56px;height:56px;border-radius:50%;color:#111;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:800;flex-shrink:0}
.beam{left:280px;top:1180px}
.q{position:absolute;left:0;right:0;top:1600px;text-align:center;z-index:9;animation:pop .5s cubic-bezier(.22,1.35,.36,1) 2.3s both}.q .pill{font-size:38px}
""", f'<div class="list">{filas}</div><div class="beam"></div><div class="q"><span class="pill on">💬 ¿Cuál te sorprendió más?</span></div>',
r"""const tx=R.text('EL LOG',150,64,R.iri('#b9a2ff',{metalness:.85,roughness:.14,opacity:1,transparent:false,iridescence:1}));R.scene.add(tx);
return t=>{const a=R.eb(R.k(t,120.2,.75));tx.visible=t>120.1;tx.scale.setScalar(Math.max(.001,a));R.at(tx,540,1420+(1-a)*150);tx.rotation.set(.18+.05*Math.sin(t*2),(1-a)*1.8+.22*Math.sin(t*1.5),0)}""",
sigue=False)

SIGUEME = ('seguir', 118.7, FIN)
# prefijo único: el editor web empareja archivos por nombre y si no, toma los e00-….webm de otras semanas
PRE = 'gloss-'

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
        rel = os.environ.get('REL', 'noticias/2/animaciones-gloss2')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        ovs.append({'file': f'{rel}/{PRE}{SIGUEME[0]}.webm', 'start': SIGUEME[1], 'end': SIGUEME[2], 'trimIn': 0, 'scale': 1, 'position': 'center'})
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
