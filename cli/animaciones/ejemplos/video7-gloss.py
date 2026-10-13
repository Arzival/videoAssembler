"""Video 7 · prueba de la dirección «gloss» (tarjetas de vidrio con objetos 3D + escenas 3D). Mismos tiempos que video7.py.
Uso: SALIDA=videos/7/animaciones-gloss2 REL=videos/7/animaciones-gloss2 python3 ejemplos/video7-gloss.py [ids…]   (SOLO_HTML=1 para revisar)
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

TG = ('M21.5 4.3 2.9 11.5c-1.1.4-1.1 1.1-.2 1.4l4.8 1.5 1.8 5.6c.2.6.4.8.9.8.4 0 .6-.2.9-.5l2.3-2.2 4.7 3.5c.9.5 1.5.2 1.7-.8l3.1-14.6c.3-1.3-.5-1.9-1.4-1.4z')
TG_SVG = f'<svg viewBox="0 0 24 24"><path fill="currentColor" d="{TG}"/></svg>'
TS_SVG = '<svg viewBox="0 0 24 24" fill="currentColor">' + ''.join(f'<circle cx="{x}" cy="{y}" r="2.4" opacity="{o}"/>' for x, y, o in
    [(4, 4, .35), (12, 4, .35), (20, 4, .35), (4, 12, 1), (12, 12, 1), (20, 12, 1), (4, 20, .35), (12, 20, 1), (20, 20, .35)]) + '</svg>'
CLAUDE = G.svgpath('claude')
HEART = 'M12 21.4 10.6 20C5.4 15.4 2 12.3 2 8.5 2 5.4 4.4 3 7.5 3c1.7 0 3.4.8 4.5 2.1C13.1 3.8 14.8 3 16.5 3 19.6 3 22 5.4 22 8.5c0 3.8-3.4 6.9-8.6 11.5z'

# piezas 3D reutilizables (JS): servidor, candado, engrane, teléfono, nodos
LIB = r"""const {THREE}=R;
R.server=(w,led='#3ee08a')=>{const G=R.group();const bm=R.gloss('#1d2230',{roughness:.3});const lm=R.gloss(led,{emissive:led,emissiveIntensity:1});const L=[];
 for(let i=0;i<3;i++){const u=R.rbox(w,w*.3,w*.8,w*.06,bm);u.position.y=R.u((i-1)*w*.34);G.add(u);
  for(let j=0;j<3;j++){const l=new THREE.Mesh(new THREE.SphereGeometry(R.u(w*.03),16,12),lm.clone());l.position.set(R.u(-w*.36+j*w*.09),u.position.y,R.u(w*.41));G.add(l);L.push(l)}
  const s=R.rbox(w*.42,w*.05,4,2,R.metal('#9aa3b5'));s.position.set(R.u(w*.18),u.position.y,R.u(w*.4));G.add(s)}
 G.userData.leds=L;return G};
R.lock=(w,col)=>{const G=R.group();const b=R.rbox(w,w*.8,w*.42,w*.16,R.gloss(col,{roughness:.2}));b.position.y=R.u(-w*.18);G.add(b);
 const sh=new THREE.Mesh(new THREE.TorusGeometry(R.u(w*.3),R.u(w*.075),24,64,Math.PI),R.metal('#e8ecf3',{roughness:.12}));sh.position.y=R.u(w*.2);G.add(sh);
 const legs=[-1,1].map(s=>{const l=new THREE.Mesh(new THREE.CylinderGeometry(R.u(w*.075),R.u(w*.075),R.u(w*.18),24),sh.material);l.position.set(R.u(s*w*.3),R.u(w*.11),0);G.add(l);return l});
 const kh=new THREE.Mesh(new THREE.CylinderGeometry(R.u(w*.07),R.u(w*.07),R.u(w*.05),24),R.gloss('#1a0a10'));kh.rotation.x=Math.PI/2;kh.position.set(0,R.u(-w*.14),R.u(w*.22));G.add(kh);
 G.userData={sh,legs};return G};
R.gear=(r,teeth,m)=>{const s=new THREE.Shape();const n=teeth*4;for(let i=0;i<=n;i++){const a=i/n*Math.PI*2,q=i%4;const rr=(q==1||q==2)?r:r*.78;const x=Math.cos(a)*rr/R.PX,y=Math.sin(a)*rr/R.PX;i?s.lineTo(x,y):s.moveTo(x,y)}
 const h=new THREE.Path();h.absarc(0,0,r*.3/R.PX,0,Math.PI*2,true);s.holes.push(h);
 const g=new THREE.ExtrudeGeometry(s,{depth:r*.35/R.PX,bevelEnabled:true,bevelThickness:.06,bevelSize:.05,bevelSegments:3});g.center();return new THREE.Mesh(g,m)};
R.phone=(h,col='#15161c')=>{const G=R.group();G.add(R.rbox(h*.49,h,h*.07,h*.08,R.gloss(col,{roughness:.18})));
 const sc=R.rbox(h*.44,h*.94,4,h*.065,R.gloss('#0a0c14',{emissive:R.AC,emissiveIntensity:.18,roughness:.1}));sc.position.z=R.u(h*.036);G.add(sc);
 const isl=R.rbox(h*.13,h*.035,4,h*.017,R.gloss('#000'));isl.position.set(0,R.u(h*.42),R.u(h*.04));G.add(isl);return G};
"""

TARJETAS = {}  # id → (inicio, duración, paleta, css, body, js3d, script)

# 0:00 · homelab 24/7 (servidor 3D en la esquina)
TARJETAS['c01-homelab'] = (0.3, 9.0, 'fin', """
.big24{font-size:46px;font-weight:800;letter-spacing:-.04em;color:var(--ac);margin-left:auto;margin-right:180px}
.st{display:flex;align-items:center;gap:14px;margin-bottom:22px}
.ph{margin-top:18px;display:flex;align-items:center;gap:16px;padding:20px 26px;border-radius:999px;font-size:30px;font-weight:700;
  background:linear-gradient(180deg,rgba(79,180,255,.3),rgba(79,180,255,.12));box-shadow:inset 0 2px 0 rgba(255,255,255,.3)}
.ph .pill{margin-left:auto}
""", f"""<div class="hd"><div class="ic">🖥️</div><div class="app">Homelab<small>ubuntu-server</small></div><div class="big24 pop" {d(3.5)}>24/7</div></div>
<div class="st ti"><span class="dot"></span>en línea</div>
<div class="row pop" {d(1.3)}><div class="mini" style="background:linear-gradient(160deg,#c9f8dc,#3ee08a)">💰</div><div class="info"><div class="n">Finanzas</div><div class="sub">:3000</div></div><span class="pill ok">● corriendo</span></div>
<div class="row pop" {d(1.6)}><div class="mini" style="background:linear-gradient(160deg,#ffd3df,#ff5d86)">🔐</div><div class="info"><div class="n">Contraseñas</div><div class="sub">:4000</div></div><span class="pill ok">● corriendo</span></div>
<div class="ph pop" {d(5.9)}>📱 También en mi teléfono<span class="pill ok">conectado ✓</span></div>""",
LIB + r"""const sv=R.server(230);R.scene.add(sv);
return t=>{const a=R.IN(t),o=R.OUT(t);sv.scale.setScalar(Math.max(.001,a*(1-o)));R.at(sv,880,250-o*80,4);sv.rotation.set(.25,-.5+.25*Math.sin(t*1.1),0);
 sv.userData.leds.forEach((l,i)=>l.material.emissiveIntensity=.4+.8*(Math.sin(t*6+i*1.7)>0?1:0))}""")

# 0:18 · ficha de Finanzas (insignia 3D con «$»)
TARJETAS['c02-finanzas'] = (18.4, 7.4, 'fin', """
.app-row{display:flex;gap:28px;align-items:center;padding-right:200px}
.nm{font-size:58px;font-weight:800;letter-spacing:-.04em}
.tags{display:flex;gap:14px;margin-top:30px;flex-wrap:wrap}.tags .pill{font-size:27px;padding:16px 26px}
.tag-cl{background:linear-gradient(180deg,#ffd0bd,#e8805d) !important;color:#2a0c05 !important}
""", f"""<div class="app-row"><div><div class="sub">App del homelab</div><div class="nm">Finanzas</div><div class="sub" style="font-size:28px">Básica y sencilla</div></div></div>
<div class="tags"><span class="pill tag-cl pop" {d(3.3)}>✦ Hecha por Claude</span><span class="pill pop" {d(4.9)}>🧱 Desde cero</span><span class="pill on pop" {d(5.9)}>🏠 Auto-hosteada</span></div>""",
LIB + r"""const G=R.group();G.add(R.rbox(250,250,90,70,R.gloss('#2ccf78',{roughness:.18})));
const tx=R.text('$',170,40,R.metal('#f5c84f',{roughness:.15}));tx.position.z=R.u(60);G.add(tx);R.scene.add(G);
const cl=R.shape(CLAUDE,120,3,R.gloss('#f08a66',{emissive:'#a8381a',emissiveIntensity:.3}));R.scene.add(cl);
return t=>{const a=R.IN(t),o=R.OUT(t);G.scale.setScalar(Math.max(.001,a*(1-o)));R.at(G,840,330-o*80,3);G.rotation.set(.2+.06*Math.sin(t*1.4),-.45+.3*Math.sin(t*.9),.05);
 const c=R.eb(R.k(t,3.3,.6));cl.visible=t>3.25;cl.scale.setScalar(Math.max(.001,c*(1-o)));R.at(cl,690,210-o*80,6);cl.rotation.set(.3,.4*Math.sin(t*1.3),t*.6)}""".replace('CLAUDE', js(CLAUDE)))

# 0:26 · movimientos (pila de monedas 3D que se va vaciando con cada gasto)
movs = [('🍔', 'Comida', 'hoy', '−$420', 6.0), ('⛽', 'Gasolina', 'ayer', '−$800', 6.35), ('📺', 'Suscripciones', 'lun', '−$219', 6.7)]
rows = ''.join(f'<div class="row pop" {d(t)}><div class="mini" style="background:linear-gradient(160deg,#ffd0d6,#ff6b7a)">{e}</div><div class="info"><div class="n">{n}</div><div class="sub">{w}</div></div><div class="amt red">{a}</div></div>' for e, n, w, a, t in movs)
TARJETAS['c03-movimientos'] = (26.3, 8.4, 'fin', """
.bal{margin:4px 0 26px;padding-right:200px}.bal .num{font-size:110px}
""", f"""<div class="hd"><div class="ic">💰</div><div class="app">Movimientos<small>octubre</small></div></div>
<div class="bal pop" {d(.5)}><div class="sub">Balance</div><div class="num" id="bal">$32,352</div></div>
<div class="row pop" {d(4.1)}><div class="mini" style="background:linear-gradient(160deg,#c9f8dc,#3ee08a)">💼</div><div class="info"><div class="n">Ingreso · Nómina</div><div class="sub">1 oct</div></div><div class="amt green">+$18,500</div></div>
{rows}""",
LIB + r"""const gm=R.metal('#f3c64f',{roughness:.16});const C=[];for(let i=0;i<5;i++){const c=R.coin(95,gm);c.rotation.x=1.15;R.scene.add(c);C.push(c)}
const out=[99,99,6.0,6.35,6.7];
return t=>{const a=R.IN(t),o=R.OUT(t);C.forEach((c,i)=>{const f=R.eo(R.k(t,out[4-i]||99,.6));c.visible=f<1;
 c.scale.setScalar(Math.max(.001,a*(1-o)));R.at(c,860+f*260,380-i*34-o*80+f*f*500,3);c.rotation.set(1.15+f*4,0,.15+f*3+Math.sin(t+i)*.05)})}""",
"""window.__cnt=t=>{const v=t<6.0?32352:t<6.35?31932:t<6.7?31132:30913;document.getElementById('bal').innerHTML='$'+v.toLocaleString('en-US')+'<span class="d">.00</span>'}""")

# 0:39 · bot de Telegram (avión de papel 3D)
TARJETAS['c04-telegram'] = (39.0, 8.2, 'tg', """
.chat{display:flex;flex-direction:column;gap:16px}
.me{align-self:flex-end;background:linear-gradient(180deg,#7cc6ff,#2f8fff);color:#04203a;font-weight:700;border-radius:36px 36px 10px 36px;padding:20px 28px;font-size:32px;box-shadow:inset 0 2px 0 rgba(255,255,255,.5)}
.bot{align-self:flex-start;display:flex;gap:16px;align-items:flex-end}
.bot .mini{background:linear-gradient(160deg,#c9f8dc,#3ee08a)}
.bb{background:linear-gradient(180deg,rgba(255,255,255,.14),rgba(255,255,255,.06));border-radius:36px 36px 36px 10px;padding:20px 28px;font-size:30px;box-shadow:inset 0 1.5px 0 rgba(255,255,255,.2)}
.bb .who{font-size:22px;font-weight:800;color:var(--ac);margin-bottom:6px}
.dots{display:flex;gap:10px;padding:8px 2px}.dots i{width:16px;height:16px;border-radius:50%;background:rgba(255,255,255,.6);animation:dt 1s ease-in-out infinite}
.dots i:nth-child(2){animation-delay:.15s}.dots i:nth-child(3){animation-delay:.3s}@keyframes dt{50%{transform:translateY(-8px);opacity:.3}}
.gone{animation:gone .25s ease forwards}@keyframes gone{to{opacity:0;height:0;padding:0;margin:0;overflow:hidden}}
.rec{display:flex;align-items:center;gap:16px;margin-top:22px;padding:20px 26px;border-radius:999px;font-size:28px;font-weight:700;
  background:linear-gradient(180deg,rgba(62,224,138,.3),rgba(62,224,138,.1));box-shadow:inset 0 2px 0 rgba(255,255,255,.25)}
""", f"""<div class="hd" style="padding-right:190px"><div class="ic">{TG_SVG}</div><div class="app">FinanzasBot<small>Telegram · ahora</small></div></div>
<div class="chat">
 <div class="me pop" {d(.7)}><span class="type" style="--td:1.1s;--n:22;animation-delay:.9s">Gasté $250 en tacos 🌮</span></div>
 <div class="bot pop" {d(3.0)}><div class="mini">💰</div>
  <div class="bb"><div class="who">FinanzasBot</div><div class="dots" style="animation:gone .2s ease 4.9s forwards"><i></i><i></i><i></i></div>
  <div class="pop" style="animation-delay:5.1s">✅ Registrado: <b>Comida −$250</b></div></div></div>
</div>
<div class="rec pop" {d(6.0)}>💰 Finanzas · nuevo movimiento <span class="pill bad" style="margin-left:auto">−$250</span></div>""",
LIB + r"""const G=R.group();G.add(new THREE.Mesh(new THREE.SphereGeometry(R.u(120),64,48),R.gloss('#2f9bff',{roughness:.15})));
const pl=R.shape(TG,150,2.2,R.gloss('#ffffff',{roughness:.2}),.3);pl.position.set(R.u(-8),0,R.u(108));G.add(pl);R.scene.add(G);
return t=>{const a=R.IN(t),o=R.OUT(t),hop=Math.sin(Math.PI*R.k(t,1.9,.5));G.scale.setScalar(Math.max(.001,a*(1-o)));
 R.at(G,870,250-o*80-hop*40,4);G.rotation.set(.15,-.35+.3*Math.sin(t*1.2)+hop*.6,hop*.3)}""".replace('TG', js(TG)))

# 1:02 · análisis con IA (dona 3D por categorías)
cats = [('Comida', 38, '#ffb340'), ('Transporte', 22, '#4fb4ff'), ('Suscripciones', 15, '#c084fc'), ('Otros', 25, '#9a98a8')]
bars = ''.join(f'<div class="cat pop{" hot" if k == 0 else ""}" style="animation-delay:{8.0 + k * .3:.1f}s"><div class="cl"><span><i style="background:{c}"></i>{n}</span><b>{p}%</b></div>'
               f'<div class="trk"><i style="width:{p * 2.2}%;background:{c};animation-delay:{8.15 + k * .3:.2f}s"></i></div></div>' for k, (n, p, c) in enumerate(cats))
TARJETAS['c05-analisis'] = (62.4, 17.9, 'ia', """
.prog{margin:0 0 20px;padding-right:220px}.prog .r{display:flex;justify-content:space-between;font-size:26px;font-weight:700;color:rgba(255,255,255,.65);margin-bottom:12px}
.prog .r b{font-size:40px;color:#fff}
.trk{height:22px;border-radius:11px;background:rgba(255,255,255,.1);overflow:hidden}
.trk i{display:block;height:100%;border-radius:11px;transform-origin:left;animation:fillL 1s ease both}@keyframes fillL{from{transform:scaleX(0)}}
.cat{padding:14px 20px;margin:0 -20px;border-radius:28px}.cat .cl{display:flex;justify-content:space-between;font-size:29px;font-weight:700;margin-bottom:10px}
.cat .cl i{display:inline-block;width:18px;height:18px;border-radius:50%;margin-right:14px}
.hot{animation:pop .45s cubic-bezier(.22,1.3,.36,1) 8.0s both,hot .5s ease 12.4s forwards}
@keyframes hot{to{background:linear-gradient(180deg,rgba(255,179,64,.28),rgba(255,179,64,.1));box-shadow:inset 0 2px 0 rgba(255,255,255,.25)}}
.warn{margin-left:14px;font-size:21px;padding:6px 16px;opacity:0;animation:fade .3s ease 12.6s forwards;background:linear-gradient(180deg,#ffe6c2,#ffb340);color:#2a1603}
.tip{display:flex;gap:18px;align-items:center;margin-top:22px;padding:24px 28px;border-radius:36px;font-size:29px;font-weight:600;line-height:1.3;
  background:linear-gradient(180deg,rgba(62,224,138,.28),rgba(62,224,138,.1));box-shadow:inset 0 2px 0 rgba(255,255,255,.25)}
""", f"""<div class="hd"><div class="ic">✦</div><div class="app">Análisis con IA<small>cada mes</small></div></div>
<div class="prog pop" {d(.4)}><div class="r"><span>Octubre · ingresos y gastos</span><b id="pc">0%</b></div><div class="trk"><i style="width:100%;background:linear-gradient(90deg,#e9e0ff,#a78bfa);animation-duration:2.6s;animation-delay:4.8s"></i></div></div>
{bars.replace('Comida</span>', 'Comida<span class="pill warn">⚠ aquí se te va</span></span>', 1)}
<div class="tip pop" {d(14.6)}><span style="font-size:40px">💡</span><span>Cocina 2 días más por semana y <b class="green">ahorra ~$1,200 al mes</b></span></div>""",
LIB + r"""const G=R.group();const segs=[[.38,'#ffb340'],[.22,'#4fb4ff'],[.15,'#c084fc'],[.25,'#9a98a8']];let a0=Math.PI/2;const S=[];
segs.forEach(([p,c],i)=>{const m=new THREE.Mesh(new THREE.TorusGeometry(R.u(115),R.u(46),32,96,p*Math.PI*2-.06),R.gloss(c,{roughness:.2}));m.rotation.z=a0;a0+=p*Math.PI*2;G.add(m);S.push(m)});
const core=new THREE.Mesh(new THREE.SphereGeometry(R.u(50),48,32),R.iri('#e9e0ff',{opacity:1,transparent:false,metalness:.6}));G.add(core);R.scene.add(G);
return t=>{const a=R.IN(t),o=R.OUT(t);G.scale.setScalar(Math.max(.001,a*(1-o)));R.at(G,860,250-o*80,3);G.rotation.set(-.55+.08*Math.sin(t),.3*Math.sin(t*.7),t*.25);
 S.forEach((m,i)=>{const r=R.eb(R.k(t,8.0+i*.3,.6));m.scale.setScalar(Math.max(.001,r));const h=i==0?R.eb(R.k(t,12.4,.5)):0;const mid=m.rotation.z+segs[i][0]*Math.PI;m.position.set(Math.cos(mid)*h*.5,Math.sin(mid)*h*.5,h*.4)})}""",
"""window.__cnt=t=>{const p=Math.min(1,Math.max(0,(t-4.8)/2.6));document.getElementById('pc').textContent=Math.round(p*100)+'%'}""")

# 1:20 · contraseñas (candado 3D que se abre con la palabra secreta)
accs = [('G', '#ea4335', 'Gmail', 'p4$Wq!9zLm'), ('A', '#ff9900', 'AWS', 'K7#vR2@xTe'), ('⌥', '#3b4350', 'GitHub', 'm9!Zc8&QwY')]
vault = ''.join(f'<div class="row pop" style="animation-delay:{6.6 + k * .25:.2f}s"><div class="mini" style="background:{c};font-size:30px;font-weight:800">{l}</div>'
                f'<div class="info"><div class="n">{n}</div></div><div class="pw mono"><span class="hid">••••••••••</span><span class="vis">{p}</span></div></div>' for k, (l, c, n, p) in enumerate(accs))
TARJETAS['c06-contrasenas'] = (80.5, 13.6, 'pass', """
.gen{display:flex;gap:16px;align-items:center;padding:22px 26px;border-radius:999px;font-size:32px;background:rgba(0,0,0,.3);box-shadow:inset 0 2px 10px rgba(0,0,0,.35);margin-right:170px}
.gen .lb{font-size:21px;font-weight:800;color:rgba(255,255,255,.5);text-transform:uppercase;letter-spacing:.08em}
.gen .pill{margin-left:auto;font-size:22px;padding:10px 18px}
.lock{display:flex;gap:16px;align-items:center;margin:18px 0 16px;padding:22px 28px;border-radius:999px;font-size:29px;font-weight:700;
  background:linear-gradient(180deg,rgba(255,93,134,.32),rgba(255,93,134,.12));box-shadow:inset 0 2px 0 rgba(255,255,255,.25);
  animation:pop .45s cubic-bezier(.22,1.3,.36,1) 6.3s both,unl .4s ease 11.4s forwards}
@keyframes unl{to{background:linear-gradient(180deg,rgba(62,224,138,.32),rgba(62,224,138,.12))}}
.lock .inp{margin-left:auto;font-size:34px;letter-spacing:.14em}
.pw{position:relative;font-size:28px;min-width:230px;text-align:right}
.pw .vis{position:absolute;right:0;top:0;opacity:0;animation:fade .3s ease 11.7s forwards;color:#3ee08a}
.pw .hid{animation:off .2s ease 11.6s forwards;color:rgba(255,255,255,.5)}
""", f"""<div class="hd" style="padding-right:190px"><div class="ic">🔐</div><div class="app">Contraseñas<small>homelab</small></div></div>
<div class="gen pop" {d(2.4)}><span class="lb">Generar</span><span class="type mono" style="--td:1.2s;--n:14;animation-delay:2.8s">Xq7!mZ@2vL#9pR</span><span class="pill ok pop" {d(3.9)}>✓</span></div>
<div class="lock">🔑 Palabra secreta<span class="inp"><span class="type" style="--td:1.3s;--n:8;animation-delay:8.3s">••••••••</span></span></div>
{vault}""",
LIB + r"""const L=R.lock(200,'#ff5d86');R.scene.add(L);
return t=>{const a=R.IN(t),o=R.OUT(t),u=R.eb(R.k(t,11.4,.6));L.scale.setScalar(Math.max(.001,a*(1-o)));R.at(L,870,250-o*80,4);
 L.rotation.set(.18,-.4+.3*Math.sin(t*1.1)-u*.3,0);const {sh,legs}=L.userData;sh.position.y=R.u(40+60*u);legs.forEach((l,i)=>l.position.y=R.u(22+60*u+(i==0?0:-30*u)));
 sh.rotation.y=u*.0;L.children[0].material.color.lerpColors(new THREE.Color('#ff5d86'),new THREE.Color('#3ee08a'),u)}""")

# 1:42 · backend yo / frontend Claude (engrane y asterisco 3D sobre cada columna)
TARJETAS['c07-stack'] = (102.1, 8.6, 'pass', """
.cols{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:150px}
.col{border-radius:44px;padding:110px 26px 34px;text-align:center;background:linear-gradient(180deg,rgba(255,255,255,.1),rgba(255,255,255,.03));box-shadow:inset 0 1.5px 0 rgba(255,255,255,.2)}
.col .k{font-size:23px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.5)}
.col .w{font-size:56px;font-weight:800;letter-spacing:-.04em;margin-top:6px}
.col.cl{background:linear-gradient(180deg,rgba(232,128,93,.4),rgba(232,128,93,.12));box-shadow:inset 0 2px 0 rgba(255,255,255,.3),0 0 60px rgba(232,128,93,.3)}
.hd{margin-bottom:0}
""", f"""<div class="hd"><div class="ic">🔐</div><div class="app">Contraseñas<small>cómo la hice</small></div></div>
<div class="cols"><div class="col pop" {d(2.0)}><div class="k">Backend</div><div class="w">Yo</div></div>
<div class="col cl pop" {d(4.4)}><div class="k">Frontend</div><div class="w">Claude</div></div></div>""",
LIB + r"""const gr=R.gear(110,10,R.metal('#c9ced8',{roughness:.2}));R.scene.add(gr);
const cl=R.shape(CLAUDE,230,3,R.gloss('#f08a66',{emissive:'#a8381a',emissiveIntensity:.3}));R.scene.add(cl);
return t=>{const o=R.OUT(t),g=R.eb(R.k(t,2.0,.7)),c=R.eb(R.k(t,4.4,.7));
 gr.visible=t>1.95;gr.scale.setScalar(Math.max(.001,g*(1-o)));R.at(gr,330,470-o*80,4);gr.rotation.set(.35,.25*Math.sin(t),t*1.2);
 cl.visible=t>4.35;cl.scale.setScalar(Math.max(.001,c*(1-o)));R.at(cl,750,470-o*80,4);cl.rotation.set(.25,(1-c)*3+.4*Math.sin(t*1.2),.2+t*.5)}""".replace('CLAUDE', js(CLAUDE)))

# 1:51 · spoiler 30 s (cronómetro 3D)
TARJETAS['c08-spoiler'] = (111.3, 16.8, 'tg', """
.chat{display:flex;flex-direction:column;gap:16px}
.me{align-self:flex-end;background:linear-gradient(180deg,#7cc6ff,#2f8fff);color:#04203a;font-weight:700;border-radius:36px 36px 10px 36px;padding:20px 28px;font-size:32px;box-shadow:inset 0 2px 0 rgba(255,255,255,.5)}
.bot{align-self:flex-start;display:flex;gap:16px;align-items:flex-end}
.bb{background:linear-gradient(180deg,rgba(255,255,255,.14),rgba(255,255,255,.06));border-radius:36px 36px 36px 10px;padding:20px 28px;font-size:30px;box-shadow:inset 0 1.5px 0 rgba(255,255,255,.2)}
.bb .who{font-size:22px;font-weight:800;color:var(--ac);margin-bottom:6px}
.spo{position:relative;display:inline-block;font-size:32px;margin-top:8px;padding:6px 12px;border-radius:12px}
.spo .txt{filter:blur(10px);opacity:.9}
.spo:after{content:'';position:absolute;inset:0;border-radius:12px;background-image:radial-gradient(rgba(255,255,255,.8) 1.2px,transparent 1.6px);background-size:8px 8px;animation:shim .6s steps(3) infinite}
@keyframes shim{50%{background-position:3px 4px}}
.msg{animation:pop .45s cubic-bezier(.22,1.3,.36,1) 4.8s both,poof .5s ease 14.9s forwards}@keyframes poof{to{opacity:0;filter:blur(12px);transform:scale(.9)}}
.timer{display:flex;align-items:center;gap:18px;margin-top:24px;font-size:27px;font-weight:700;color:rgba(255,255,255,.7)}
.timer .trk{flex:1;height:18px;border-radius:9px;background:rgba(255,255,255,.1);overflow:hidden}
.timer .trk i{display:block;height:100%;width:100%;background:linear-gradient(90deg,#ff4d5e,#ffb340);transform-origin:left;animation:drain 8.2s linear 6.6s both}
@keyframes drain{to{transform:scaleX(0)}}
.timer b{font-size:46px;font-weight:800;color:#fff;min-width:90px;text-align:right;font-variant-numeric:tabular-nums}
.del{position:absolute;left:46px;right:46px;bottom:120px;text-align:center;opacity:0;animation:fade .4s ease 15.3s forwards}
""", f"""<div class="hd" style="padding-right:190px"><div class="ic">{TG_SVG}</div><div class="app">ContraseñasBot<small>Telegram · ahora</small></div></div>
<div class="chat">
 <div class="me pop" {d(2.2)}>/pass gmail</div>
 <div class="bot msg"><div class="mini" style="background:linear-gradient(160deg,#ffd3df,#ff5d86)">🔐</div>
  <div class="bb"><div class="who">ContraseñasBot</div>Tu contraseña de Gmail:<br><span class="spo mono"><span class="txt">p4$Wq!9zLm</span></span></div></div>
</div>
<div class="del"><span class="pill bad">🗑 Mensaje eliminado</span></div>
<div class="timer pop" {d(6.6)}>⏱ Se borra en<div class="trk"><i></i></div><b id="sec">30s</b></div>""",
LIB + r"""const G=R.group();const body=new THREE.Mesh(new THREE.CylinderGeometry(R.u(115),R.u(115),R.u(50),64),R.gloss('#ff8a4c',{roughness:.2}));body.rotation.x=Math.PI/2;G.add(body);
const face=new THREE.Mesh(new THREE.CircleGeometry(R.u(92),64),R.gloss('#fff6ee',{roughness:.4}));face.position.z=R.u(26);G.add(face);
const ring=new THREE.Mesh(new THREE.TorusGeometry(R.u(115),R.u(14),24,80),R.metal('#e8ecf3',{roughness:.12}));ring.position.z=R.u(14);G.add(ring);
const btn=R.rbox(46,40,40,10,R.metal('#e8ecf3'));btn.position.y=R.u(140);G.add(btn);
const arc=new THREE.Mesh(new THREE.RingGeometry(R.u(40),R.u(86),64,1,Math.PI/2,Math.PI*2),R.gloss('#ff4d5e',{emissive:'#ff4d5e',emissiveIntensity:.4,side:THREE.DoubleSide}));arc.position.z=R.u(27);G.add(arc);
const hand=R.rbox(12,82,8,4,R.gloss('#1a1420'));hand.geometry.translate(0,R.u(36),0);hand.position.z=R.u(32);G.add(hand);R.scene.add(G);
return t=>{const a=R.IN(t),o=R.OUT(t),p=R.k(t,6.6,8.2),poof=R.eo(R.k(t,14.9,.5));G.scale.setScalar(Math.max(.001,a*(1-o)*(1-.25*poof)));R.at(G,880,250-o*80,4);
 G.rotation.set(.12,-.35+.25*Math.sin(t*1.1),Math.sin(t*20)*.03*(p>.75&&p<1?1:0));hand.rotation.z=-p*Math.PI*2;
 arc.geometry.dispose();arc.geometry=new THREE.RingGeometry(R.u(40),R.u(86),64,1,Math.PI/2,Math.max(.001,(1-p)*Math.PI*2))}""",
"""window.__cnt=t=>{const p=Math.min(1,Math.max(0,(t-6.6)/8.2));document.getElementById('sec').textContent=Math.ceil(30*(1-p))+'s'}""")

# 2:53 · red privada (nodos 3D conectados)
people = [('📱', 'iPhone de Armando', 'tú', .5), ('🖥️', 'homelab', 'servidor', .8), ('👩', 'Mamá', 'invitada', 2.9), ('👨', 'Hermano', 'invitado', 3.3)]
prow = ''.join(f'<div class="row pop" {d(t)}><div class="mini" style="background:rgba(255,255,255,.12)">{e}</div><div class="info"><div class="n">{n}</div><div class="sub">{s}</div></div>'
               f'<span class="pill ok fade" style="animation-delay:{5.7 + k * .15:.2f}s">✓ apps</span></div>' for k, (e, n, s, t) in enumerate(people))
TARJETAS['c09-red'] = (173.2, 8.0, 'tg', "", f"""<div class="hd" style="padding-right:190px"><div class="ic">{TS_SVG}</div><div class="app">Mi red privada<small>Tailscale · 4 equipos</small></div></div>{prow}""",
LIB + r"""const G=R.group();const pos=[[-1,.6],[1,.7],[-.8,-.8],[.9,-.6]];const cols=['#4fb4ff','#3ee08a','#ff8ab0','#ffb340'];const N=[];const T=[];
pos.forEach(([x,y],i)=>{const s=new THREE.Mesh(new THREE.SphereGeometry(R.u(34),40,30),R.gloss(cols[i],{emissive:cols[i],emissiveIntensity:.25}));s.position.set(R.u(x*85),R.u(y*85),0);G.add(s);N.push(s)});
const hub=new THREE.Mesh(new THREE.IcosahedronGeometry(R.u(40),1),R.iri('#d6ecff',{opacity:1,transparent:false,metalness:.6,flatShading:true}));G.add(hub);
N.forEach(n=>{const c=new THREE.CatmullRomCurve3([new THREE.Vector3(),n.position.clone()]);const tb=new THREE.Mesh(new THREE.TubeGeometry(c,8,R.u(6),10),R.glass('#d6ecff',{opacity:.6}));G.add(tb);T.push(tb)});
R.scene.add(G);const ts=[.5,.8,2.9,3.3];
return t=>{const a=R.IN(t),o=R.OUT(t);G.scale.setScalar(Math.max(.001,a*(1-o)));R.at(G,860,260-o*80,4);G.rotation.set(.3*Math.sin(t*.6),.5*Math.sin(t*.5),t*.15);
 N.forEach((n,i)=>{const p=R.eb(R.k(t,ts[i],.5));n.scale.setScalar(Math.max(.001,p));T[i].scale.setScalar(Math.max(.001,R.eo(R.k(t,ts[i]+.1,.4))))});hub.rotation.set(t,t*.7,0)}""")

# 3:01 · Sígueme (corazón 3D)
TARJETAS['seguir'] = (181.2, 8.37, 'ia', """
.tt{display:flex;align-items:center;gap:24px;padding-right:170px}
.av{width:120px;height:120px;border-radius:50%;background:linear-gradient(160deg,#e9e0ff,#7c3aed);display:flex;align-items:center;justify-content:center;font-size:56px;font-weight:800;color:#160b33;
  box-shadow:inset 0 3px 0 rgba(255,255,255,.6),0 0 0 6px rgba(255,255,255,.12),0 0 40px rgba(167,139,250,.5)}
.nm{font-size:44px;font-weight:800;letter-spacing:-.03em}
.btn{position:relative;margin-top:30px;height:96px}
.btn span{position:absolute;inset:0;border-radius:999px;display:flex;align-items:center;justify-content:center;font-size:36px;font-weight:800}
.b1{background:linear-gradient(180deg,#e9e0ff,#a78bfa);color:#160b33;box-shadow:inset 0 2px 0 #fff,0 20px 50px rgba(167,139,250,.45);animation:tap .22s ease 1.55s,off .2s ease 1.72s forwards}
.b2{background:linear-gradient(180deg,rgba(255,255,255,.18),rgba(255,255,255,.07));opacity:0;animation:fade .25s ease 1.72s forwards}
@keyframes tap{50%{transform:scale(.92)}}
.acts{display:flex;gap:16px;margin-top:20px}
.act{flex:1;display:flex;align-items:center;justify-content:center;gap:12px;padding:20px;border-radius:999px;font-size:30px;font-weight:700;background:linear-gradient(180deg,rgba(255,255,255,.12),rgba(255,255,255,.04))}
.act.lk{animation:lk .3s ease 3.15s forwards}@keyframes lk{to{background:linear-gradient(180deg,#ffb0c6,#ff4d86);color:#2c0612}}
.cm{display:flex;gap:18px;align-items:center;margin-top:20px;padding:20px 26px;border-radius:36px;background:linear-gradient(180deg,rgba(255,255,255,.1),rgba(255,255,255,.03));animation:pop .45s cubic-bezier(.22,1.3,.36,1) 4.8s both}
.cm .mini{background:linear-gradient(160deg,#ffe6c2,#ff5d86)}.cm .t{font-size:28px;font-weight:600}
""", """<div class="tt"><div class="av">A</div><div><div class="nm">Armando</div><div class="sub">Homelab · IA · código</div></div></div>
<div class="btn"><span class="b1">Seguir</span><span class="b2">Siguiendo ✓</span></div>
<div class="acts"><div class="act lk"><span>❤️</span><span id="likes">1,203</span></div><div class="act">💬 <span id="coms">48</span></div><div class="act">↗️ Compartir</div></div>
<div class="cm"><div class="mini"></div><div><div class="sub" style="font-size:21px">Tú · ahora</div><div class="t"><span class="type" style="--td:1.5s;--n:30;animation-delay:5.1s">¡Quiero ver más del homelab! 🔥</span></div></div></div>""",
LIB + r"""const H=R.shape(HEART,210,5,R.gloss('#ff3d77',{emissive:'#ff1050',emissiveIntensity:.15,roughness:.15}));R.scene.add(H);
return t=>{const a=R.IN(t),o=R.OUT(t),b=Math.sin(Math.PI*R.k(t,3.15,.45));H.scale.setScalar(Math.max(.001,a*(1-o)*(1+.35*b)));R.at(H,870,270-o*80,4);
 H.rotation.set(.15,-.4+.35*Math.sin(t*1.2)+R.eo(R.k(t,3.15,.8))*Math.PI*2,0);H.material.emissiveIntensity=.15+.8*b}""".replace('HEART', js(HEART)),
"window.__cnt=t=>{document.getElementById('likes').textContent=t>=3.15?'1,204':'1,203';document.getElementById('coms').textContent=t>=4.8?'49':'48'}")


# ───────── escenas a pantalla completa (tiempos locales) ─────────
ESCENAS = {}  # id → (inicio, duración, paleta, css, body, js3d)
PH = """
.ph{position:absolute;left:50%;width:500px;height:1010px;margin-left:-250px;border-radius:80px;background:#0b0c12;z-index:2;
  box-shadow:inset 0 0 0 12px #23242c,inset 0 0 0 14px #5a5d6c,0 0 0 2px rgba(255,255,255,.1),0 60px 140px rgba(0,0,0,.65),0 0 160px rgba(var(--acr),.3)}
.ph:before{content:'';position:absolute;left:50%;top:32px;width:140px;height:40px;margin-left:-70px;border-radius:20px;background:#000;z-index:5}
.scr{position:absolute;inset:14px;border-radius:66px;overflow:hidden}
"""

ESCENAS['s1-pwa'] = (50.8, 11.8, 'fin', PH + """
.ph{top:420px;animation:rise .7s cubic-bezier(.22,1.1,.36,1) .5s both}
.web{position:absolute;inset:0;background:linear-gradient(180deg,#0f1a16,#0a0f0d);padding:100px 28px 0}
.url{height:60px;border-radius:30px;background:rgba(255,255,255,.1);display:flex;align-items:center;justify-content:center;font-size:23px;color:rgba(255,255,255,.75)}
.wb{margin-top:28px;border-radius:40px;padding:30px;background:linear-gradient(160deg,#d2fbe4 -40%,#3ee08a 20%,#0a5a2b);box-shadow:inset 0 2px 0 rgba(255,255,255,.5)}
.wb .k{font-size:22px;color:rgba(3,36,18,.7);font-weight:700}.wb .v{font-size:56px;font-weight:800;letter-spacing:-.04em;color:#032412;margin-top:6px}
.wl{height:84px;border-radius:30px;background:rgba(255,255,255,.07);margin-top:18px}
.sheet{position:absolute;left:0;right:0;bottom:0;padding:30px 26px 56px;border-radius:44px 44px 0 0;background:linear-gradient(180deg,#2a2c36,#1d1f27);transform:translateY(100%);
  animation:shUp .45s cubic-bezier(.22,1.1,.36,1) 4.6s forwards,shDn .35s ease 6.5s forwards}
@keyframes shUp{to{transform:none}}@keyframes shDn{from{transform:none}to{transform:translateY(100%)}}
.opt{display:flex;align-items:center;gap:16px;padding:22px 24px;border-radius:999px;font-size:26px;font-weight:700;margin-top:10px;background:rgba(255,255,255,.07)}
.opt.add{background:linear-gradient(180deg,#d2fbe4,#3ee08a);color:#032412;animation:tap .25s ease 5.9s}@keyframes tap{50%{transform:scale(.94)}}
.home{position:absolute;inset:0;padding:120px 36px 0;background:radial-gradient(500px 500px at 30% 20%,#1f6b45,transparent),radial-gradient(500px 500px at 80% 90%,#0f3a5c,transparent),#0b1210;
  opacity:0;animation:fade .45s ease 6.8s forwards}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:34px 22px}
.ap{display:flex;flex-direction:column;align-items:center}.ap i{width:88px;height:88px;border-radius:26px;background:rgba(255,255,255,.12)}
.ap.new i{background:transparent}
.badge{position:absolute;left:0;right:0;top:1500px;text-align:center;z-index:9;opacity:0;animation:pop .5s cubic-bezier(.22,1.35,.36,1) 8.6s forwards}
.badge .pill{font-size:34px;padding:22px 40px}
""", f"""{G.steps([('Le pedí a <em>Claude</em>', .2, 2.9), ('que la hiciera <em>PWA</em>', 3.0, 4.6), ('<em>instalar</em> la web…', 4.7, 6.6), ('…como una <em>app</em><br>de mi teléfono', 6.7, None)], 0, top=150, size=88)}
<div class="ph"><div class="scr">
 <div class="web"><div class="url">🔒 finanzas.homelab</div><div class="wb"><div class="k">Balance</div><div class="v">$32,352</div></div><div class="wl"></div><div class="wl"></div><div class="wl"></div></div>
 <div class="sheet"><div class="opt">↗️ Compartir</div><div class="opt add">➕ Agregar a inicio</div><div class="opt">🔖 Marcador</div></div>
 <div class="home"><div class="grid">{''.join('<div class="ap"><i></i></div>' for _ in range(6))}<div class="ap new"><i></i></div>{''.join('<div class="ap"><i></i></div>' for _ in range(5))}</div></div>
</div></div>
<div class="badge"><span class="pill on">📲 Sin App Store · se abre como app</span></div>""",
LIB + r"""const cl=R.shape(CLAUDE,300,3,R.gloss('#f08a66',{emissive:'#a8381a',emissiveIntensity:.3}));R.scene.add(cl);
const ic=R.group();ic.add(R.rbox(200,200,70,56,R.gloss('#2ccf78',{roughness:.16})));const tx=R.text('$',130,34,R.metal('#f5c84f',{roughness:.14}));tx.position.z=R.u(46);ic.add(tx);R.scene.add(ic);
return t=>{const a=R.eb(R.k(t,.3,.8)),ax=R.eo(R.k(t,4.4,.5));cl.visible=t<5;cl.scale.setScalar(Math.max(.001,a*(1-ax)));R.at(cl,820,470-ax*200,6);cl.rotation.set(.3,.5*Math.sin(t*1.2),t*.5);
 // el ícono nace en la pantalla (fila 2, col 3) y se sale del teléfono hacia la cámara
 const b=R.eb(R.k(t,7.4,.6)),f=R.eio(R.k(t,8.3,1.0));ic.visible=t>7.35;ic.scale.setScalar(Math.max(.001,b*R.mix(.42,1.25,f)));
 R.at(ic,R.mix(636,540,f),R.mix(677,1000,f),R.mix(1,10,f));ic.rotation.set(R.mix(0,.25,f)+.05*Math.sin(t*2),R.mix(0,-.5,f)+.3*Math.sin(t*1.3)*f,0)}""".replace('CLAUDE', js(CLAUDE)))

ESCENAS['s2-tailscale'] = (145.3, 17.0, 'tg', """
.lockp{position:absolute;left:0;right:0;top:1010px;text-align:center;z-index:9;opacity:0;animation:pop .45s cubic-bezier(.22,1.35,.36,1) 3.2s forwards,off .3s ease 10.9s forwards}.lockp .pill{font-size:30px}
.places{position:absolute;left:60px;right:60px;top:1250px;display:flex;justify-content:center;gap:16px;flex-wrap:wrap;z-index:9;animation:off .3s ease 7.3s forwards}
.places .pill{font-size:32px;padding:18px 30px}
.x{position:absolute;left:0;right:0;top:1250px;text-align:center;z-index:9;opacity:0;animation:pop .45s ease 7.6s forwards,off .3s ease 10.8s forwards}
.x .pill{font-size:34px}.x s{text-decoration-color:#ff4d5e;text-decoration-thickness:5px}
.pocket{position:absolute;left:0;right:0;top:1560px;text-align:center;z-index:9;opacity:0;animation:pop .5s cubic-bezier(.22,1.35,.36,1) 11.6s forwards}.pocket .pill{font-size:32px;padding:20px 36px}
.lab{position:absolute;top:1110px;width:300px;text-align:center;font-size:32px;font-weight:800;z-index:9;animation:fade .4s ease both}
@keyframes off{to{opacity:0}}
""", f"""{G.steps([('<em>Tailscale</em>', .2, 1.7), ('funciona como una <em>VPN</em>', 1.8, 3.9), ('acceso desde<br><em>cualquier lugar</em>', 4.0, 7.4), ('sin estar en<br><em>la computadora</em>', 7.5, 10.9), ('siempre en el <em>bolsillo</em>', 11.0, None)], 0, top=150, size=92)}
<div class="lab" style="left:90px;animation-delay:.9s,0s;animation:fade .4s ease .9s both,off .3s ease 10.9s forwards">Teléfono</div>
<div class="lab" style="right:90px;animation:fade .4s ease 1.3s both,off .3s ease 10.9s forwards">Homelab</div>
<div class="lockp"><span class="pill">🔒 red privada · cifrada</span></div>
<div class="places">{''.join(f'<span class="pill pop" style="animation-delay:{4.4 + k * .3:.1f}s">{p}</span>' for k, p in enumerate(['☕ Café', '🏢 Oficina', '✈️ De viaje', '🚗 En la calle']))}</div>
<div class="x"><span class="pill bad">🖥️ <s>sentarme frente al homelab</s></span></div>
<div class="pocket"><span class="pill on">💰 Finanzas · 🔐 Contraseñas · y más…</span></div>""",
LIB + r"""const ph=R.phone(380);R.scene.add(ph);const sv=R.server(240,'#4fb4ff');R.scene.add(sv);
const dots=R.group();const dm=R.gloss('#ffffff',{roughness:.15}),dd=R.gloss('#5b6070',{roughness:.3});
[[0,0,0],[1,0,0],[2,0,0],[0,1,1],[1,1,1],[2,1,1],[0,2,0],[1,2,1],[2,2,0]].forEach(([x,y,on])=>{const s=new THREE.Mesh(new THREE.SphereGeometry(R.u(26),32,24),on?dm:dd);s.position.set(R.u((x-1)*70),R.u((1-y)*70),0);dots.add(s)});R.scene.add(dots);
const tube=new THREE.Mesh(new THREE.CylinderGeometry(R.u(26),R.u(26),R.u(460),32,1,true),R.gloss('#4fb4ff',{emissive:'#2f8fff',emissiveIntensity:.6,transparent:true,opacity:.45,side:THREE.DoubleSide,depthWrite:false}));tube.rotation.z=Math.PI/2;R.scene.add(tube);
const pk=[0,1,2,3].map(i=>{const p=new THREE.Mesh(new THREE.SphereGeometry(R.u(16),24,16),R.gloss('#ffffff',{emissive:'#bfe4ff',emissiveIntensity:2}));R.scene.add(p);return p});
return t=>{const a=R.eb(R.k(t,.6,.7)),b=R.eb(R.k(t,1.0,.7)),c=R.eb(R.k(t,1.6,.6)),tu=R.eo(R.k(t,2.0,.7)),m=R.eio(R.k(t,10.9,.9));
 ph.scale.setScalar(Math.max(.001,a*R.mix(1,1.55,m)));R.at(ph,R.mix(240,540,m),R.mix(870,980,m));ph.rotation.set(.1,R.mix(.35,0,m)+.12*Math.sin(t*.9),R.mix(-.05,0,m));
 sv.visible=m<.99;sv.scale.setScalar(Math.max(.001,b*(1-m)));R.at(sv,840,870);sv.rotation.set(.2,-.45+.12*Math.sin(t),0);
 sv.userData.leds.forEach((l,i)=>l.material.emissiveIntensity=.4+.8*(Math.sin(t*6+i*1.7)>0?1:0));
 dots.scale.setScalar(Math.max(.001,c*(1-m)));R.at(dots,540,640);dots.rotation.set(.2*Math.sin(t*.7),.3*Math.sin(t*.5),0);
 tube.visible=tu>0&&m<.95;tube.scale.set(1,Math.max(.001,tu*(1-m)),1);R.at(tube,540,870,-1);
 pk.forEach((p,i)=>{const u=((t-2.3)*.7+i/4)%1;p.visible=t>2.4&&m<.5;R.at(p,310+u*460,870,0)})}""")

pasos = [('💻', 'Una compu viejita', 3.3), ('🐧', 'Instala Ubuntu', 5.9), (TS_SVG, 'Instala Tailscale', 6.9), ('🚀', 'Tu propio servidor', 8.7)]
steps_html = ''.join(f'<div class="ps glass" style="animation-delay:{t}s"><span class="n">{k + 1}</span><span class="e">{e}</span>{n}</div>' for k, (e, n, t) in enumerate(pasos))
ESCENAS['s3-receta'] = (162.3, 10.8, 'amb', """
.list{position:absolute;left:90px;right:90px;top:980px;display:grid;gap:20px;z-index:9}
.ps{display:flex;align-items:center;gap:24px;padding:26px 34px;border-radius:999px;font-size:42px;font-weight:800;animation:pop .5s cubic-bezier(.22,1.35,.36,1) both}
.ps .n{width:66px;height:66px;border-radius:50%;background:linear-gradient(160deg,var(--ac2),var(--ac));color:var(--ink);font-size:30px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.ps .e{font-size:52px;width:64px;text-align:center;line-height:1}.ps .e svg{width:48px;height:48px;color:#fff}
.ps:last-child{background:linear-gradient(180deg,#ffe6c2,#ffb340);color:#2a1603;box-shadow:inset 0 2px 0 #fff,0 0 70px rgba(255,179,64,.45)}
.ps:last-child .n{background:#2a1603;color:#ffb340}
.beam{left:280px;top:420px}
""", f"""{G.steps([('¿Tienes una<br><em>compu viejita</em>?', .2, None)], 0, top=150, size=96)}<div class="beam"></div>
<div class="list">{steps_html}</div>""",
LIB + r"""const lp=R.group();const base=R.rbox(440,26,290,12,R.gloss('#b9bcc6',{roughness:.35,metalness:.4}));base.rotation.x=Math.PI/2;lp.add(base);
const kb=R.rbox(380,4,170,6,R.gloss('#2a2c33'));kb.rotation.x=Math.PI/2;kb.position.set(0,R.u(0),R.u(20));
const lid=R.group();const lb=R.rbox(440,290,22,12,R.gloss('#b9bcc6',{roughness:.35,metalness:.4}));lb.position.y=R.u(145);lid.add(lb);
const sc=R.rbox(400,250,4,8,R.gloss('#140c05',{emissive:'#ff8a1f',emissiveIntensity:0}));sc.position.set(0,R.u(145),R.u(12));lid.add(sc);lid.position.z=R.u(-140);lp.add(lid);R.scene.add(lp);
const rk=R.group();const bm=R.gloss('#f4f1ec',{roughness:.2});rk.add(new THREE.Mesh(new THREE.CylinderGeometry(R.u(60),R.u(60),R.u(200),48),bm));
const nose=new THREE.Mesh(new THREE.ConeGeometry(R.u(60),R.u(110),48),R.gloss('#ff5d3a',{roughness:.2}));nose.position.y=R.u(155);rk.add(nose);
const win=new THREE.Mesh(new THREE.SphereGeometry(R.u(26),32,24),R.glass('#9fd4ff',{opacity:.8}));win.position.set(0,R.u(40),R.u(54));rk.add(win);
for(let i=0;i<3;i++){const f=R.rbox(16,90,70,6,R.gloss('#ff5d3a'));const ang=i/3*Math.PI*2;f.position.set(Math.sin(ang)*R.u(66),R.u(-80),Math.cos(ang)*R.u(66));f.rotation.y=ang;rk.add(f)}
const fl=new THREE.Mesh(new THREE.ConeGeometry(R.u(46),R.u(160),32),new THREE.MeshBasicMaterial({color:'#ffb340',transparent:true,opacity:.9}));fl.rotation.x=Math.PI;fl.position.y=R.u(-180);rk.add(fl);
R.scene.add(rk);
return t=>{const a=R.eb(R.k(t,.4,.8)),on=R.eo(R.k(t,5.9,.8)),x=R.eo(R.k(t,8.5,.5));lp.visible=x<1;lp.scale.setScalar(Math.max(.001,a*(1-x)));R.at(lp,540,700);
 lp.rotation.set(.35+.05*Math.sin(t),-.35+.3*Math.sin(t*.7),0);lid.rotation.x=-R.mix(1.6,.15,R.eo(R.k(t,1.0,1.2)));sc.material.emissiveIntensity=on*.9;
 const r=R.eb(R.k(t,8.7,.6)),up=R.k(t,9.6,1.2);rk.visible=t>8.65;rk.scale.setScalar(Math.max(.001,r));R.at(rk,540,700-up*up*900);rk.rotation.set(.15,t*1.5,.12*Math.sin(t*3));
 fl.scale.set(1,.8+.4*Math.abs(Math.sin(t*20)),1)}""")


if __name__ == '__main__':
    solo = set(sys.argv[1:])
    todo = {**{k: ('T', v) for k, v in TARJETAS.items()}, **{k: ('E', v) for k, v in ESCENAS.items()}}
    for kid, (kind, (ini, dur, pal, css, body, js3d, *script)) in todo.items():
        if solo and kid not in solo:
            continue
        sc = script[0] if script else ''
        html = G.tarjeta(css, body, dur, sc, pal=pal, js3d=js3d) if kind == 'T' else G.page(css, body, dur, sc, n=pal, js3d=js3d)
        path = f'{WORK}/{kid}.html'
        open(path, 'w').write(html)
        if os.environ.get('SOLO_HTML'):
            print('html', path); continue
        r = subprocess.run(['node', CAP, path, str(dur), f'{OUT}/{PRE}{kid}.webm'], capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr[-600:], flush=True)
    if not solo:
        rel = os.environ.get('REL', 'videos/7/animaciones-gloss2')
        ov = [{'file': f'{rel}/{PRE}{k}.webm', 'start': v[1][0], 'end': round(v[1][0] + v[1][1], 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for k, v in todo.items()]
        json.dump(sorted(ov, key=lambda o: o['start']), open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
