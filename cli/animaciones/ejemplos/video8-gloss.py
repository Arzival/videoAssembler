"""Video 8 · vigía de precios (Mercado Libre / Amazon) en estilo «gloss 2»: tarjetas de vidrio con objetos 3D + escenas 3D.
Uso: SALIDA=videos/8/animaciones REL=videos/8/animaciones python3 ejemplos/video8-gloss.py [ids…]   (SOLO_HTML=1 para revisar)
Los archivos salen con prefijo «gloss-» (el editor web empareja por nombre).
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import ellog_gloss as G
from ellog_gloss import js

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.getcwd()))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
PRE = 'gloss-'

def d(s):
    return f'style="animation-delay:{s}s"'

TG = G.svgpath('telegram')
AMZ = G.svgpath('amazon')
TG_SVG = f'<svg viewBox="0 0 24 24"><path fill="currentColor" d="{TG}"/></svg>'
AMZ_SVG = f'<svg viewBox="0 0 24 24" style="width:40px;height:40px"><path fill="currentColor" d="{AMZ}"/></svg>'
HEART = 'M12 21.4 10.6 20C5.4 15.4 2 12.3 2 8.5 2 5.4 4.4 3 7.5 3c1.7 0 3.4.8 4.5 2.1C13.1 3.8 14.8 3 16.5 3 19.6 3 22 5.4 22 8.5c0 3.8-3.4 6.9-8.6 11.5z'
ML = '<div class="mini" style="background:linear-gradient(160deg,#fff6c2,#ffe14d);color:#2d3277;font-size:30px">🤝</div>'
AZ = f'<div class="mini" style="background:linear-gradient(160deg,#3a4150,#141821);color:#ff9900">{AMZ_SVG}</div>'

# piezas 3D reutilizables (JS): servidor, teléfono, etiqueta de precio, lupa, campana, reloj, carrito, base de datos, flecha de recarga
LIB = r"""const {THREE}=R;
R.server=(w,led='#3ee08a')=>{const G=R.group();const bm=R.gloss('#1d2230',{roughness:.3});const lm=R.gloss(led,{emissive:led,emissiveIntensity:1});const L=[];
 for(let i=0;i<3;i++){const u=R.rbox(w,w*.3,w*.8,w*.06,bm);u.position.y=R.u((i-1)*w*.34);G.add(u);
  for(let j=0;j<3;j++){const l=new THREE.Mesh(new THREE.SphereGeometry(R.u(w*.03),16,12),lm.clone());l.position.set(R.u(-w*.36+j*w*.09),u.position.y,R.u(w*.41));G.add(l);L.push(l)}
  const s=R.rbox(w*.42,w*.05,4,2,R.metal('#9aa3b5'));s.position.set(R.u(w*.18),u.position.y,R.u(w*.4));G.add(s)}
 G.userData.leds=L;return G};
R.blink=(G,t)=>G.userData.leds.forEach((l,i)=>l.material.emissiveIntensity=.4+.8*(Math.sin(t*6+i*1.7)>0?1:0));
R.phone=(h,col='#15161c')=>{const G=R.group();G.add(R.rbox(h*.49,h,h*.07,h*.08,R.gloss(col,{roughness:.18})));
 const sc=R.rbox(h*.44,h*.94,4,h*.065,R.gloss('#0a0c14',{emissive:R.AC,emissiveIntensity:.07,roughness:.1}));sc.position.z=R.u(h*.036);G.add(sc);
 const isl=R.rbox(h*.13,h*.035,4,h*.017,R.gloss('#000'));isl.position.set(0,R.u(h*.42),R.u(h*.04));G.add(isl);return G};
// etiqueta de precio con ojillo y «$»
R.tag=(w,col)=>{const h=w*.56,x0=-w/2,xs=x0+h*.42,P=v=>v/R.PX;const s=new THREE.Shape();
 s.moveTo(P(x0),0);s.lineTo(P(xs),P(h/2));s.lineTo(P(w/2-h*.12),P(h/2));s.quadraticCurveTo(P(w/2),P(h/2),P(w/2),P(h/2-h*.12));
 s.lineTo(P(w/2),P(-h/2+h*.12));s.quadraticCurveTo(P(w/2),P(-h/2),P(w/2-h*.12),P(-h/2));s.lineTo(P(xs),P(-h/2));s.lineTo(P(x0),0);
 const hole=new THREE.Path();hole.absarc(P(xs-h*.02),0,P(h*.13),0,Math.PI*2,true);s.holes.push(hole);
 const g=new THREE.ExtrudeGeometry(s,{depth:P(w*.09),bevelEnabled:true,bevelThickness:P(w*.03),bevelSize:P(w*.025),bevelSegments:5,curveSegments:24});g.center();
 const G=R.group();G.add(new THREE.Mesh(g,R.gloss(col,{roughness:.16})));const tx=R.text('$',h*.62,w*.05,R.metal('#fff4d0',{roughness:.12}));tx.position.set(R.u(w*.12),0,R.u(w*.09));G.add(tx);return G};
R.mag=r=>{const G=R.group();const ring=new THREE.Mesh(new THREE.TorusGeometry(R.u(r),R.u(r*.16),24,72),R.metal('#e8ecf3',{roughness:.12}));G.add(ring);
 const lens=new THREE.Mesh(new THREE.CircleGeometry(R.u(r),64),R.glass('#cfe9ff',{opacity:.35}));G.add(lens);
 const hd=new THREE.Mesh(new THREE.CylinderGeometry(R.u(r*.17),R.u(r*.2),R.u(r*1.3),32),R.gloss('#1b1e26',{roughness:.25}));hd.position.set(R.u(r*1.2),R.u(-r*1.2),0);hd.rotation.z=Math.PI/4;G.add(hd);return G};
R.bell=(r,col)=>{const pts=[[0,1.05],[.16,1.0],[.3,.86],[.42,.5],[.5,.1],[.66,-.12],[.8,-.22],[.8,-.3],[0,-.3]].map(([x,y])=>new THREE.Vector2(R.u(r*x),R.u(r*y)));
 const G=R.group();const b=new THREE.Mesh(new THREE.LatheGeometry(pts,64),R.gloss(col,{roughness:.16,metalness:.3}));G.add(b);
 const cl=new THREE.Mesh(new THREE.SphereGeometry(R.u(r*.17),32,24),R.metal('#fff4d0'));cl.position.y=R.u(-r*.42);G.add(cl);
 const top=new THREE.Mesh(new THREE.TorusGeometry(R.u(r*.13),R.u(r*.05),16,40),R.metal('#fff4d0'));top.position.y=R.u(r*1.12);G.add(top);return G};
R.clock=(r,col)=>{const G=R.group();const body=new THREE.Mesh(new THREE.CylinderGeometry(R.u(r),R.u(r),R.u(r*.4),64),R.gloss(col,{roughness:.2}));body.rotation.x=Math.PI/2;G.add(body);
 const face=new THREE.Mesh(new THREE.CircleGeometry(R.u(r*.82),64),R.gloss('#fff8ec',{roughness:.4}));face.position.z=R.u(r*.21);G.add(face);
 const ring=new THREE.Mesh(new THREE.TorusGeometry(R.u(r),R.u(r*.1),24,80),R.metal('#e8ecf3',{roughness:.12}));ring.position.z=R.u(r*.12);G.add(ring);
 for(let i=0;i<12;i++){const m=R.rbox(r*.05,i%3?r*.08:r*.16,4,2,R.gloss('#1a1420'));const a=i/12*Math.PI*2;m.position.set(Math.sin(a)*R.u(r*.68),Math.cos(a)*R.u(r*.68),R.u(r*.23));m.rotation.z=-a;G.add(m)}
 const hh=R.rbox(r*.09,r*.42,6,3,R.gloss('#1a1420'));hh.geometry.translate(0,R.u(r*.18),0);hh.position.z=R.u(r*.26);G.add(hh);
 const mh=R.rbox(r*.06,r*.62,6,3,R.gloss(R.AC,{emissive:R.AC,emissiveIntensity:.3}));mh.geometry.translate(0,R.u(r*.28),0);mh.position.z=R.u(r*.29);G.add(mh);
 const pin=new THREE.Mesh(new THREE.SphereGeometry(R.u(r*.08),24,16),R.metal('#e8ecf3'));pin.position.z=R.u(r*.31);G.add(pin);G.userData={hh,mh};return G};
R.cart=(w,col)=>{const G=R.group();const P=v=>v/R.PX;const h=w*.55;const s=new THREE.Shape();s.moveTo(P(-w/2),P(h/2));s.lineTo(P(w/2),P(h/2));s.lineTo(P(w*.38),P(-h/2));s.lineTo(P(-w*.4),P(-h/2));s.lineTo(P(-w/2),P(h/2));
 const ho=new THREE.Shape();const g=new THREE.ExtrudeGeometry(s,{depth:P(w*.5),bevelEnabled:true,bevelThickness:P(w*.03),bevelSize:P(w*.03),bevelSegments:4});g.center();
 const bk=new THREE.Mesh(g,R.gloss(col,{roughness:.18}));G.add(bk);
 const mm=R.metal('#e8ecf3',{roughness:.12});const bar=new THREE.Mesh(new THREE.CylinderGeometry(P(w*.035),P(w*.035),P(w*.36),24),mm);bar.position.set(P(-w*.6),P(h*.62),0);bar.rotation.z=-.5;G.add(bar);
 const grip=new THREE.Mesh(new THREE.CylinderGeometry(P(w*.05),P(w*.05),P(w*.55),24),R.gloss('#1b1e26'));grip.rotation.x=Math.PI/2;grip.position.set(P(-w*.7),P(h*.78),0);G.add(grip);
 const wm=R.gloss('#1b1e26',{roughness:.3});[[-.3,-.24],[-.3,.24],[.28,-.24],[.28,.24]].forEach(([x,z])=>{const wh=new THREE.Mesh(new THREE.CylinderGeometry(P(w*.08),P(w*.08),P(w*.06),32),wm);wh.rotation.x=Math.PI/2;wh.position.set(P(w*x),P(-h*.72),P(w*z));G.add(wh)});
 const box=R.rbox(w*.42,w*.36,w*.32,w*.04,R.gloss('#ffe14d',{roughness:.2}));box.position.set(P(-w*.02),P(h*.55),0);box.rotation.z=.12;G.add(box);
 const rib=R.rbox(w*.08,w*.37,w*.33,w*.02,R.gloss('#ff4d5e'));rib.position.copy(box.position);rib.rotation.z=.12;G.add(rib);G.userData={box,rib};return G};
R.db=(w,col)=>{const G=R.group();const m=R.gloss(col,{roughness:.2,metalness:.2});const L=[];
 for(let i=0;i<3;i++){const c=new THREE.Mesh(new THREE.CylinderGeometry(R.u(w/2),R.u(w/2),R.u(w*.24),64),m);c.position.y=R.u((i-1)*w*.3);G.add(c);
  const l=new THREE.Mesh(new THREE.TorusGeometry(R.u(w/2),R.u(w*.025),12,64),R.gloss('#ffffff',{emissive:R.AC,emissiveIntensity:.2}));l.rotation.x=Math.PI/2;l.position.y=c.position.y+R.u(w*.13);G.add(l);L.push(l)}
 G.userData.rings=L;return G};
R.refresh=(r,col)=>{const G=R.group();const m=R.gloss(col,{roughness:.18});const arc=new THREE.Mesh(new THREE.TorusGeometry(R.u(r),R.u(r*.2),24,72,Math.PI*1.55),m);G.add(arc);
 const head=new THREE.Mesh(new THREE.ConeGeometry(R.u(r*.42),R.u(r*.55),32),m);head.position.set(R.u(r),R.u(-r*.05),0);G.add(head);G.userData.m=m;return G};
"""

TARJETAS = {}  # id → (inicio, duración, paleta, css, body, js3d[, script])

# 0:00 · «tengo un servicio que vigila los precios de Mercado Libre y Amazon» (etiqueta + lupa 3D)
TARJETAS['c01-vigia'] = (0.2, 5.2, 'ml', """
.st{display:flex;align-items:center;gap:14px;margin-bottom:24px;font-size:30px;font-weight:700}
""", f"""<div class="hd" style="padding-right:200px"><div class="ic">🏷️</div><div class="app">Vigía de precios<small>homelab · 24/7</small></div></div>
<div class="st"><span class="dot"></span>vigilando 2 tiendas</div>
<div class="row pop" {d(2.9)}>{ML}<div class="info"><div class="n">Mercado Libre</div><div class="sub">precios · existencias</div></div><span class="pill ok">● activo</span></div>
<div class="row pop" {d(4.3)}>{AZ}<div class="info"><div class="n">Amazon</div><div class="sub">precios · existencias</div></div><span class="pill ok">● activo</span></div>""",
LIB + r"""const tg=R.tag(250,'#ffe14d');R.scene.add(tg);const mg=R.mag(62);R.scene.add(mg);
return t=>{const a=R.IN(t),o=R.OUT(t);tg.scale.setScalar(Math.max(.001,a*(1-o)));R.at(tg,850,320-o*80,3);tg.rotation.set(.2,-.4+.3*Math.sin(t*1.1),-.25+.08*Math.sin(t*1.7));
 const m=R.eb(R.k(t,.9,.6));mg.scale.setScalar(Math.max(.001,m*(1-o)));R.at(mg,800+70*Math.sin(t*1.6),320+40*Math.cos(t*1.6)-o*80,9);mg.rotation.set(.2,.3*Math.sin(t),0)}""")

# 0:12 · alertas: bajó / se agotó / volvió (campana 3D que suena con cada aviso)
TARJETAS['c02-alertas'] = (12.5, 9.8, 'tg', """
.row .pill{font-size:23px}
.prod{display:flex;gap:18px;align-items:center;margin:0 0 22px;padding:18px 24px;border-radius:999px;background:rgba(0,0,0,.28);box-shadow:inset 0 2px 10px rgba(0,0,0,.3);font-size:27px;font-weight:700;margin-right:150px}
.prod .lnk{color:rgba(255,255,255,.55);font-weight:600;font-family:'JetBrains Mono',monospace;font-size:22px;margin-left:auto}
.ttl2{font-size:24px;color:rgba(255,255,255,.5);font-weight:800;text-transform:uppercase;letter-spacing:.08em;margin:0 0 14px 6px}
""", f"""<div class="hd" style="padding-right:200px"><div class="ic">{TG_SVG}</div><div class="app">PrecioBot<small>Telegram · avisos</small></div></div>
<div class="prod pop" {d(.2)}>📦 Tu producto<span class="lnk">cada 3 h</span></div>
<div class="row pop" {d(.3)}><div class="mini" style="background:linear-gradient(160deg,#c9f8dc,#3ee08a)">📉</div><div class="info"><div class="n">¡Bajó de precio!</div><div class="sub">$1,299 → <b class="green">$949</b></div></div><span class="pill ok">−27%</span></div>
<div class="row pop" {d(1.8)}><div class="mini" style="background:linear-gradient(160deg,#ffd0d6,#ff4d5e)">⛔</div><div class="info"><div class="n">Se agotó</div><div class="sub">sin existencias</div></div><span class="pill bad">agotado</span></div>
<div class="row pop" {d(5.4)}><div class="mini" style="background:linear-gradient(160deg,#d6ecff,#4fb4ff)">🔁</div><div class="info"><div class="n">¡Volvió a estar disponible!</div><div class="sub">ya puedes comprarlo</div></div><span class="pill ok">en stock</span></div>""",
LIB + r"""const b=R.bell(110,'#ffc83d');R.scene.add(b);const rings=[.3,1.8,5.4];
return t=>{const a=R.IN(t),o=R.OUT(t);let sw=0;rings.forEach(r=>{const p=R.k(t,r,1.0);if(p>0&&p<1)sw+=Math.sin(p*Math.PI*6)*(1-p)*.55});
 b.scale.setScalar(Math.max(.001,a*(1-o)));R.at(b,870,260-o*80,4);b.rotation.set(.2,-.3+.25*Math.sin(t),sw)}""")

# 0:25 · lo registra, lo guarda y lo revisa (sobre el teclado, debajo del chat de Telegram)
TARJETAS['c03-registro'] = (25.4, 7.9, 'tg', """
.wrap .card{padding:36px 40px}
.chain{display:flex;gap:14px;align-items:stretch}
.sp{flex:1;border-radius:32px;padding:22px 16px;text-align:center;background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(255,255,255,.03));box-shadow:inset 0 1.5px 0 rgba(255,255,255,.12);
  font-size:27px;font-weight:800;animation:pop .5s cubic-bezier(.22,1.35,.36,1) both,lit .35s ease forwards}
.sp .e{display:block;font-size:46px;margin-bottom:8px}.sp small{display:block;font-size:20px;color:rgba(255,255,255,.55);margin-top:4px;font-weight:600}
@keyframes lit{to{background:linear-gradient(180deg,rgba(79,180,255,.42),rgba(79,180,255,.14));box-shadow:inset 0 2px 0 rgba(255,255,255,.35),0 0 40px rgba(79,180,255,.3)}}
""", f"""<div class="hd" style="padding-right:200px;margin-bottom:22px"><div class="ic">🤖</div><div class="app">PrecioBot<small>producto nuevo</small></div><span class="pill ok pop" {d(.3)}>✓ link recibido</span></div>
<div class="chain">
 <div class="sp" style="animation-delay:1.2s,1.4s"><span class="e">📝</span>Registra<small>el producto</small></div>
 <div class="sp" style="animation-delay:2.7s,2.9s"><span class="e">💾</span>Guarda<small>precio actual</small></div>
 <div class="sp" style="animation-delay:5.2s,5.4s"><span class="e">⏱</span>Revisa<small>cada 3 horas</small></div>
</div>""",
LIB + r"""const db=R.db(150,'#4fb4ff');R.scene.add(db);const lit=[1.4,2.9,5.4];
return t=>{const a=R.IN(t),o=R.OUT(t);db.scale.setScalar(Math.max(.001,a*(1-o)));R.at(db,880,1300-o*80,4);db.rotation.set(.35+.05*Math.sin(t),t*.6,0);
 db.userData.rings.forEach((r,i)=>r.material.emissiveIntensity=.2+1.6*R.eo(R.k(t,lit[i],.4)))}""", 1290)

# 0:33 · ya no entro a revisar a cada rato (flecha de recarga 3D que gira sin parar → campana)
TARJETAS['c04-antes'] = (33.8, 7.2, 'ml', """
.k{font-size:22px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.45);margin:0 0 12px 8px}
.k+.row{margin-top:0}.row+.k{margin-top:24px}
.old{animation:pop .5s cubic-bezier(.22,1.35,.36,1) .5s both,old .4s ease 4.6s forwards}@keyframes old{to{opacity:.45;filter:grayscale(1)}}
.old .n{position:relative;display:inline-block}.old .n:after{content:'';position:absolute;left:-4px;right:-4px;top:52%;height:5px;border-radius:3px;background:#ff4d5e;transform:scaleX(0);transform-origin:left;animation:strike .35s ease 4.6s forwards}
@keyframes strike{to{transform:scaleX(1)}}
.amt{font-size:46px}
.chips{display:flex;gap:12px;margin-top:16px;padding-left:8px}.chips .pill{font-size:24px}
""", f"""<div class="hd" style="padding-right:200px"><div class="ic">🛒</div><div class="app">Revisar a mano<small>vs. que te avisen</small></div></div>
<div class="k fade" {d(.5)}>Antes</div>
<div class="row old"><div class="mini" style="background:rgba(255,255,255,.12)">🔄</div><div class="info"><div class="n">Entrar a revisar</div><div class="sub">a cada rato</div></div><div class="amt red" id="cnt">×0</div></div>
<div class="k fade" {d(4.8)}>Ahora</div>
<div class="row pop" {d(4.9)}><div class="mini" style="background:linear-gradient(160deg,#fff6c2,#ffe14d)">🔔</div><div class="info"><div class="n">Te avisa solo</div><div class="sub">tú ni te enteras</div></div><span class="pill on">0 revisiones</span></div>
<div class="chips"><span class="pill ok pop" {d(5.2)}>✓ ¿Disponible?</span><span class="pill ok pop" {d(6.1)}>✓ ¿Con descuento?</span></div>""",
LIB + r"""const rf=R.refresh(85,'#ff6b7a');R.scene.add(rf);const b=R.bell(100,'#ffe14d');R.scene.add(b);
return t=>{const a=R.IN(t),o=R.OUT(t),x=R.eo(R.k(t,4.5,.35)),bb=R.eb(R.k(t,4.8,.6));
 rf.visible=x<1;rf.scale.setScalar(Math.max(.001,a*(1-x)));R.at(rf,870,260,4);const sp=Math.min(t,4.5);rf.rotation.set(.2,-.3,-(sp*sp*1.6));
 b.visible=t>4.75;b.scale.setScalar(Math.max(.001,bb*(1-o)));R.at(b,870,260-o*80,4);const p=R.k(t,4.9,1.1);b.rotation.set(.2,-.3+.2*Math.sin(t),Math.sin(p*Math.PI*6)*(1-p)*.5)}""",
"""window.__cnt=t=>{const p=Math.min(1,Math.max(0,(t-1.0)/3.4));document.getElementById('cnt').textContent='×'+Math.round(p*p*23)}""")

# 0:56 · favoritos: agrego más y se borran los anteriores (corazón 3D que se apaga)
fav0 = [('🎧', 'Audífonos inalámbricos', '$1,299'), ('⌚', 'Smartwatch', '$2,499'), ('🎮', 'Control inalámbrico', '$1,149')]
fav1 = [('🔌', 'Cargador 65 W', '$549', 3.0), ('🧦', 'Calcetines x12', '$199', 3.4)]
fav_new = ''.join(f'<div class="fv grow" style="animation-delay:{t}s"><div class="row"><div class="mini" style="background:rgba(255,255,255,.12)">{e}</div><div class="info"><div class="n">{n}</div></div><div class="amt">{p}</div></div></div>' for e, n, p, t in reversed(fav1))
fav_dd = lambda k: f'style="--dd:{4.4 + (2 - k) * .35:.2f}s"' if k else ''
fav_old = ''.join(f'<div class="fv{" del" if k else ""}" {fav_dd(k)}><div class="row"><div class="mini" style="background:rgba(255,255,255,.12)">{e}</div><div class="info"><div class="n">{n}</div></div><div class="amt">{p}</div></div></div>' for k, (e, n, p) in enumerate(fav0))
TARJETAS['c05-favoritos'] = (56.6, 6.6, 'pass', """
.fv{overflow:hidden;max-height:120px;padding-bottom:12px}
.fv .row{margin:0}.amt{font-size:30px}
.grow{animation:grow .45s cubic-bezier(.22,1.2,.36,1) both}@keyframes grow{from{max-height:0;opacity:0;padding-bottom:0}to{max-height:120px;opacity:1}}
.del .row{animation:redd .3s ease var(--dd) forwards}@keyframes redd{to{background:linear-gradient(180deg,rgba(255,77,94,.35),rgba(255,77,94,.12));opacity:.7}}
.del{animation:shrink .4s ease calc(var(--dd) + .45s) forwards}@keyframes shrink{to{max-height:0;opacity:0;padding-bottom:0}}
.lost{margin-top:8px;text-align:center}
""", f"""<div class="hd" style="padding-right:200px"><div class="ic">♥</div><div class="app">Mis favoritos<small>lista llena</small></div></div>
{fav_new}{fav_old}
<div class="lost pop" {d(4.6)}><span class="pill bad">🗑 Se borraron los anteriores</span></div>""",
LIB + r"""const H=R.shape(HEART,190,5,R.gloss('#ff3d77',{emissive:'#ff1050',emissiveIntensity:.15,roughness:.15}));R.scene.add(H);
const grey=new THREE.Color('#5b5f6b'),pink=new THREE.Color('#ff3d77');
return t=>{const a=R.IN(t),o=R.OUT(t),g=R.eo(R.k(t,4.4,.8)),hit=Math.sin(Math.PI*R.k(t,4.4,.35));H.scale.setScalar(Math.max(.001,a*(1-o)*(1-.2*g)));
 R.at(H,870,260-o*80+g*30,4);H.rotation.set(.15+g*.4,-.4+.35*Math.sin(t*1.2),Math.sin(t*30)*.08*hit);H.material.color.lerpColors(pink,grey,g);H.material.emissiveIntensity=.15*(1-g)}""".replace('HEART', js(HEART)))

# 1:10 · Sígueme + «¿qué producto pondrías a vigilar?» (corazón 3D)
TARJETAS['seguir'] = (70.0, 6.72, 'ml', """
.tt{display:flex;align-items:center;gap:24px;padding-right:170px}
.av{width:120px;height:120px;border-radius:50%;background:linear-gradient(160deg,#fff6c2,#ffb340);display:flex;align-items:center;justify-content:center;font-size:56px;font-weight:800;color:#2a1603;
  box-shadow:inset 0 3px 0 rgba(255,255,255,.6),0 0 0 6px rgba(255,255,255,.12),0 0 40px rgba(255,225,77,.45)}
.nm{font-size:44px;font-weight:800;letter-spacing:-.03em}
.btn{position:relative;margin-top:30px;height:96px}
.btn span{position:absolute;inset:0;border-radius:999px;display:flex;align-items:center;justify-content:center;font-size:36px;font-weight:800}
.b1{background:linear-gradient(180deg,#fff6c2,#ffe14d);color:#2a2203;box-shadow:inset 0 2px 0 #fff,0 20px 50px rgba(255,225,77,.4);animation:tap .22s ease 1.0s,off .2s ease 1.17s forwards}
.b2{background:linear-gradient(180deg,rgba(255,255,255,.18),rgba(255,255,255,.07));opacity:0;animation:fade .25s ease 1.17s forwards}
@keyframes tap{50%{transform:scale(.92)}}
.acts{display:flex;gap:16px;margin-top:20px}
.act{flex:1;display:flex;align-items:center;justify-content:center;gap:12px;padding:20px;border-radius:999px;font-size:30px;font-weight:700;background:linear-gradient(180deg,rgba(255,255,255,.12),rgba(255,255,255,.04))}
.act.lk{animation:lk .3s ease 2.0s forwards}@keyframes lk{to{background:linear-gradient(180deg,#ffb0c6,#ff4d86);color:#2c0612}}
.cm{display:flex;gap:18px;align-items:center;margin-top:20px;padding:20px 26px;border-radius:36px;background:linear-gradient(180deg,rgba(255,255,255,.1),rgba(255,255,255,.03));animation:pop .45s cubic-bezier(.22,1.3,.36,1) 2.7s both}
.cm .mini{background:linear-gradient(160deg,#fff6c2,#ffe14d)}.cm .t{font-size:28px;font-weight:600}
.q{margin-top:20px;text-align:center}.q .pill{font-size:27px}
""", """<div class="tt"><div class="av">A</div><div><div class="nm">Armando</div><div class="sub">Homelab · IA · código</div></div></div>
<div class="btn"><span class="b1">Seguir</span><span class="b2">Siguiendo ✓</span></div>
<div class="acts"><div class="act lk"><span>❤️</span><span id="likes">1,203</span></div><div class="act">💬 <span id="coms">48</span></div><div class="act">↗️ Compartir</div></div>
<div class="q pop" style="animation-delay:.4s"><span class="pill on">🏷️ ¿Qué producto pondrías a vigilar?</span></div>
<div class="cm"><div class="mini">🛒</div><div><div class="sub" style="font-size:21px">Tú · ahora</div><div class="t"><span class="type" style="--td:1.5s;--n:24;animation-delay:3.0s">¡Una PS5 cuando baje! 🎮</span></div></div></div>""",
LIB + r"""const H=R.shape(HEART,210,5,R.gloss('#ff3d77',{emissive:'#ff1050',emissiveIntensity:.15,roughness:.15}));R.scene.add(H);
return t=>{const a=R.IN(t),o=R.OUT(t),b=Math.sin(Math.PI*R.k(t,2.0,.45));H.scale.setScalar(Math.max(.001,a*(1-o)*(1+.35*b)));R.at(H,870,270-o*80,4);
 H.rotation.set(.15,-.4+.35*Math.sin(t*1.2)+R.eo(R.k(t,2.0,.8))*Math.PI*2,0);H.material.emissiveIntensity=.15+.8*b}""".replace('HEART', js(HEART)),
"window.__cnt=t=>{document.getElementById('likes').textContent=t>=2.0?'1,204':'1,203';document.getElementById('coms').textContent=t>=2.7?'49':'48'}")


# ───────── escenas a pantalla completa (tiempos locales) ─────────
ESCENAS = {}  # id → (inicio, duración, paleta, css, body, js3d[, script])

# 0:05 · le mando el link → lo revisa cada 3 horas
ESCENAS['s1-link'] = (5.4, 7.2, 'ml', """
.lnk{position:absolute;left:0;right:0;top:640px;text-align:center;z-index:9;opacity:0;animation:pop .5s cubic-bezier(.22,1.35,.36,1) 1.8s forwards,off .3s ease 3.6s forwards}
.lnk .pill{font-size:30px;font-family:'JetBrains Mono',monospace;font-weight:700}
.lab{position:absolute;top:1130px;width:300px;text-align:center;font-size:32px;font-weight:800;z-index:9}
.hrs{position:absolute;left:60px;right:60px;top:1290px;display:flex;justify-content:center;gap:14px;flex-wrap:wrap;z-index:9}
.hrs .pill{font-size:30px;padding:16px 26px}
@keyframes off{to{opacity:0}}
""", f"""{G.steps([('Le mando el <em>link</em>', .2, 3.6), ('y lo revisa<br>cada <em>3 horas</em>', 3.7, None)], 0, top=170, size=96)}
<div class="lab" style="left:110px;animation:fade .4s ease .7s both,off .3s ease 3.6s forwards">📱 Yo</div>
<div class="lab" style="right:110px;animation:fade .4s ease 1.1s both,off .3s ease 3.6s forwards">🖥️ Homelab</div>
<div class="lnk"><span class="pill on">🔗 mercadolibre.com.mx/…</span></div>
<div class="hrs">{''.join(f'<span class="pill pop" style="animation-delay:{4.4 + k * .45:.2f}s">{h} <b class="g">✓</b></span>' for k, h in enumerate(['9:00', '12:00', '15:00', '18:00']))}</div>""",
LIB + r"""const ph=R.phone(360);R.scene.add(ph);const sv=R.server(230,'#ffe14d');R.scene.add(sv);
const tube=new THREE.Mesh(new THREE.CylinderGeometry(R.u(22),R.u(22),R.u(420),32,1,true),R.gloss('#ffe14d',{emissive:'#ffb800',emissiveIntensity:.5,transparent:true,opacity:.4,side:THREE.DoubleSide,depthWrite:false}));tube.rotation.z=Math.PI/2;R.scene.add(tube);
const pk=R.rbox(70,46,20,12,R.gloss('#fff6c2',{emissive:'#ffe14d',emissiveIntensity:1.2}));R.scene.add(pk);const ck=R.clock(190,'#ffe14d');R.scene.add(ck);
return t=>{const a=R.eb(R.k(t,.5,.7)),b=R.eb(R.k(t,.9,.7)),tu=R.eo(R.k(t,1.3,.6)),x=R.eio(R.k(t,3.5,.5)),c=R.eb(R.k(t,3.8,.7));
 ph.visible=sv.visible=x<1;ph.scale.setScalar(Math.max(.001,a*(1-x)));R.at(ph,260,890);ph.rotation.set(.1,.35+.12*Math.sin(t*.9),-.05);
 sv.scale.setScalar(Math.max(.001,b*(1-x)));R.at(sv,820,890);sv.rotation.set(.2,-.45+.12*Math.sin(t),0);R.blink(sv,t);
 tube.visible=tu>0&&x<1;tube.scale.set(1,Math.max(.001,tu*(1-x)),1);R.at(tube,540,890,-1);
 const m=R.eio(R.k(t,2.0,1.1));pk.visible=t>1.95&&t<3.15;R.at(pk,R.mix(330,750,m),890,1);pk.rotation.set(.3,t*3,0);
 ck.visible=t>3.75;ck.scale.setScalar(Math.max(.001,c));R.at(ck,540,900);ck.rotation.set(.15+.05*Math.sin(t),-.25+.3*Math.sin(t*.8),0);
 const sp=Math.max(0,t-3.9);ck.userData.mh.rotation.z=-sp*Math.PI*2*1.6;ck.userData.hh.rotation.z=-sp*Math.PI*2*1.6/4}""")

# 0:41 · grupos de ofertas: te mandan de todo (chat que no para; lo tuyo se pierde)
deals = [('🧦', 'Calcetines x12', '$89'), ('🍳', 'Sartén antiadherente', '$199'), ('🧴', 'Shampoo 1 L', '$75'), ('🪑', 'Silla gamer', '$1,890'),
         ('🔦', 'Linterna LED', '$129'), ('🧸', 'Peluche gigante', '$349'), ('🖨️', 'Impresora', '$1,299'), ('🥤', 'Termo 1.2 L', '$219'),
         ('⭐', 'Lo que TÚ buscabas', '$949'), ('🧹', 'Escoba eléctrica', '$899'), ('👟', 'Tenis running', '$1,099'), ('🧃', 'Jugos x24', '$159'),
         ('🪥', 'Cepillo eléctrico', '$399'), ('🧺', 'Canasta ropa', '$99'), ('🛞', 'Llanta 15"', '$1,450'), ('🍫', 'Chocolates x30', '$189'),
         ('🔋', 'Pilas AA x20', '$149'), ('🪴', 'Maceta grande', '$259'), ('🎒', 'Mochila', '$499'), ('🧼', 'Jabón x6', '$69'),
         ('📎', 'Clips x500', '$45'), ('🧯', 'Extintor', '$650'), ('🪞', 'Espejo', '$389'), ('🥫', 'Atún x10', '$210')]
feed = ''.join(f'<div class="msg{" mine" if "TÚ" in n else ""}"><span class="e">{e}</span><div class="info"><div class="n">{n}</div><div class="p">🔥 {p} · ver oferta</div></div></div>' for e, n, p in deals)
ESCENAS['s2-grupos'] = (41.2, 14.6, 'tg', """
.ph{position:absolute;left:50%;top:470px;width:600px;height:1000px;margin-left:-300px;border-radius:70px;z-index:9;overflow:hidden;animation:rise .7s cubic-bezier(.22,1.1,.36,1) .4s both;
  background:linear-gradient(180deg,#0f1b2b,#0a1019);box-shadow:inset 0 0 0 12px #23242c,inset 0 0 0 14px #5a5d6c,0 60px 140px rgba(0,0,0,.65),0 0 160px rgba(var(--acr),.3)}
.gh{position:absolute;left:0;right:0;top:0;z-index:3;padding:74px 44px 22px;border-radius:56px 56px 0 0;display:flex;gap:18px;align-items:center;
  background:linear-gradient(180deg,#1b2a40,#16233a);box-shadow:0 10px 30px rgba(0,0,0,.4)}
.gh .ic{width:70px;height:70px;border-radius:50%;background:linear-gradient(160deg,#ffd0bd,#ff6a3d);display:flex;align-items:center;justify-content:center;font-size:36px}
.gh b{display:block;font-size:30px}.gh small{font-size:21px;color:rgba(255,255,255,.55);font-weight:600}
.feed{position:absolute;left:30px;right:30px;top:200px;display:flex;flex-direction:column;gap:14px;
  animation:scr1 3.4s cubic-bezier(.45,0,.55,1) 2.6s both,scr2 6.4s cubic-bezier(.5,0,.9,.5) 7.4s forwards}
@keyframes scr1{from{transform:translateY(560px)}to{transform:translateY(-120px)}}
@keyframes scr2{from{transform:translateY(-120px)}to{transform:translateY(-2560px)}}
.msg{display:flex;gap:16px;align-items:center;padding:16px 20px;border-radius:28px 28px 28px 8px;background:linear-gradient(180deg,rgba(255,255,255,.13),rgba(255,255,255,.05));box-shadow:inset 0 1.5px 0 rgba(255,255,255,.15)}
.msg .e{font-size:44px;width:56px;text-align:center}.msg .n{font-size:27px;font-weight:700}.msg .p{font-size:21px;color:#ffb340;font-weight:700;margin-top:2px}
.msg.mine{background:linear-gradient(180deg,#d6ecff,#4fb4ff);color:#04203a;box-shadow:0 0 50px rgba(79,180,255,.6)}.msg.mine .p{color:#04203a}
.cnt{position:absolute;left:70px;top:400px;z-index:10;opacity:0;animation:pop .45s cubic-bezier(.22,1.35,.36,1) 6.6s forwards}
.cnt .pill{font-size:32px}
.lost{position:absolute;left:0;right:0;top:1560px;text-align:center;z-index:9;opacity:0;animation:pop .5s cubic-bezier(.22,1.35,.36,1) 12.0s forwards}
.lost .pill{font-size:32px;padding:20px 34px}
.fade2{position:absolute;left:14px;right:14px;bottom:14px;height:180px;z-index:3;border-radius:0 0 56px 56px;background:linear-gradient(0deg,#0a1019,transparent)}
""", f"""{G.steps([('Grupos de <em>ofertas</em>', .2, 6.4), ('te mandan<br><em class="red">de todo</em>', 6.5, 10.9), ('y tienes que<br>estar <em>revisándolos</em>', 11.0, None)], 0, top=150, size=92)}
<div class="ph"><div class="gh"><span class="ic">🔥</span><div><b>Ofertas MX 🇲🇽</b><small>48,213 miembros</small></div></div><div class="feed">{feed}</div><div class="fade2"></div></div>
<div class="cnt"><span class="pill bad" id="cnt">+0 mensajes</span></div>
<div class="lost"><span class="pill">😵 ¿Y lo que tú querías? …se perdió</span></div>""",
LIB + r"""const G=R.group();G.add(new THREE.Mesh(new THREE.SphereGeometry(R.u(105),64,48),R.gloss('#2f9bff',{roughness:.15})));
const pl=R.shape(TG,130,2.2,R.gloss('#ffffff',{roughness:.2}),.3);pl.position.set(R.u(-6),0,R.u(96));G.add(pl);R.scene.add(G);
const dots=[];for(let i=0;i<9;i++){const s=new THREE.Mesh(new THREE.SphereGeometry(R.u(22),24,16),R.gloss('#ff4d5e',{emissive:'#ff2040',emissiveIntensity:.5}));R.scene.add(s);dots.push(s)}
return t=>{const a=R.eb(R.k(t,.6,.8)),o=R.eo(R.k(t,R.D-.5,.42));G.scale.setScalar(Math.max(.001,a*(1-o)));R.at(G,900,640,6);
 const fast=R.k(t,6.6,6),shake=t>6.6?Math.sin(t*(30+fast*30))*.12*Math.min(1,fast*3):0;G.rotation.set(.15,-.35+.25*Math.sin(t*1.1),shake);
 dots.forEach((s,i)=>{const t0=6.6+i*.75,p=R.k(t,t0,1.6);s.visible=p>0&&p<1;const ang=i*2.4;s.scale.setScalar(Math.max(.001,Math.sin(p*Math.PI)));
  R.at(s,900+Math.cos(ang)*(140+p*120),640+Math.sin(ang)*(140+p*120),4)})}""".replace('TG', js(TG)),
"""window.__cnt=t=>{const p=Math.min(1,Math.max(0,(t-6.6)/7));document.getElementById('cnt').textContent='+'+Math.round(p*p*1284).toLocaleString('en-US')+' mensajes'}""")

# 1:03 · ¿algo en el carrito? no lo revises tú: que lo haga un servicio (carrito 3D + servidor)
ESCENAS['s3-carrito'] = (63.3, 6.7, 'fin', """
.price{position:absolute;left:0;right:0;top:1250px;text-align:center;z-index:9;animation:pop .5s cubic-bezier(.22,1.35,.36,1) .8s both}
.price .old{font-size:120px;font-weight:800;letter-spacing:-.05em;line-height:1;position:relative;display:inline-block;animation:dim .3s ease 4.2s forwards}
.price .old:after{content:'';position:absolute;left:-10px;right:-10px;top:50%;height:10px;border-radius:5px;background:#ff4d5e;transform:scaleX(0);transform-origin:left;animation:strike .3s ease 4.2s forwards}
@keyframes strike{to{transform:scaleX(1)}}@keyframes dim{to{opacity:.4;font-size:80px}}
.price .new{display:block;font-size:150px;font-weight:800;letter-spacing:-.05em;line-height:1.05;color:var(--ac);opacity:0;animation:stamp .45s cubic-bezier(.22,1.6,.36,1) 4.4s forwards;--r:-3deg}
.wait{margin-top:20px;animation:off .25s ease 4.1s forwards}.wait .pill{font-size:30px}
.ok{position:absolute;left:0;right:0;top:1660px;text-align:center;z-index:9;opacity:0;animation:pop .5s cubic-bezier(.22,1.35,.36,1) 4.8s forwards}.ok .pill{font-size:32px;padding:20px 34px}
@keyframes off{to{opacity:0}}
""", f"""{G.steps([('¿Algo en el<br><em>carrito</em>?', .2, 2.8), ('no lo revises <em class="red">tú</em>', 2.9, 3.8), ('que lo haga<br>un <em>servicio</em>', 3.9, None)], 0, top=150, size=96)}
<div class="price"><span class="old">$1,299</span><span class="new">$949</span><div class="wait"><span class="pill">⏳ esperando a que baje…</span></div></div>
<div class="ok"><span class="pill on">🔔 Te avisó tu homelab</span></div>""",
LIB + r"""const ct=R.cart(380,'#3ee08a');R.scene.add(ct);const sv=R.server(170,'#3ee08a');R.scene.add(sv);
const beam=new THREE.Mesh(new THREE.CylinderGeometry(R.u(10),R.u(10),R.u(300),24,1,true),R.gloss('#3ee08a',{emissive:'#3ee08a',emissiveIntensity:1,transparent:true,opacity:.6,depthWrite:false}));R.scene.add(beam);
return t=>{const a=R.eb(R.k(t,.3,.8)),s=R.eb(R.k(t,3.9,.6)),bm=R.eo(R.k(t,4.1,.4)),hop=Math.sin(Math.PI*R.k(t,4.4,.5));
 ct.scale.setScalar(Math.max(.001,a));R.at(ct,R.mix(560,470,s),860-hop*50);ct.rotation.set(.25+.04*Math.sin(t),-.5+.25*Math.sin(t*.8),.04*Math.sin(t*1.3));
 ct.userData.box.rotation.z=ct.userData.rib.rotation.z=.12+hop*.4;
 sv.visible=t>3.85;sv.scale.setScalar(Math.max(.001,s));R.at(sv,850,650);sv.rotation.set(.25,-.6+.15*Math.sin(t),0);R.blink(sv,t);
 beam.visible=bm>0;beam.scale.set(1,Math.max(.001,bm),1);R.at(beam,700,750,-1);beam.rotation.z=-1.0}""")


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
        rel = os.environ.get('REL', 'videos/8/animaciones')
        ov = [{'file': f'{rel}/{PRE}{k}.webm', 'start': v[1][0], 'end': round(v[1][0] + v[1][1], 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for k, v in todo.items()]
        json.dump(sorted(ov, key=lambda o: o['start']), open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
