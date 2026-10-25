"""El Log · dirección «gloss» (prueba): lienzo teñido por noticia, brillo radial, vidrio, píldoras sólidas
y una capa 3D real (three.js) con objetos brillosos que se salen de las tarjetas.

page(css, body, dur, script, n, js3d) — n = paleta de la noticia (0 = marca), js3d = cuerpo de una función
async (R, S) que arma la escena 3D con los helpers de R y devuelve update(t) (t = segundos del video final).
Los contadores en JS van en window.__cnt(t_local).
"""
import json, os, re
import ellog as _L
import transiciones as TRN

HERE = os.path.dirname(os.path.abspath(__file__))
logo, at, steps = _L.logo, _L.at, _L.steps
SANS = "'Plus Jakarta Sans',-apple-system,system-ui,sans-serif"
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800'
         '&family=JetBrains+Mono:wght@500;700&display=block" rel="stylesheet">')
THREE = 'https://cdn.jsdelivr.net/npm/three@0.170.0'
COLA = TRN.COLA  # cuánto se queda una escena debajo de la siguiente (más con TRANS)

# (lienzo, lienzo2, acento, acento claro, rgb acento, tinta sobre acento)
PALETAS = {
    0: ('#160d33', '#07060f', '#a78bfa', '#e9e0ff', '167,139,250', '#160b33'),
    1: ('#33100f', '#0e0606', '#ff8a6b', '#ffd9cc', '255,138,107', '#2a0c05'),
    2: ('#0c1a45', '#05070f', '#6ea8ff', '#dbe8ff', '110,168,255', '#06122e'),
    3: ('#171f08', '#070903', '#c6e64a', '#f1fbc9', '198,230,74', '#1a2203'),
    4: ('#062436', '#03090f', '#4fd2ff', '#d3f4ff', '79,210,255', '#032231'),
    # apps del homelab (video 7)
    'fin': ('#08261a', '#030a07', '#3ee08a', '#d2fbe4', '62,224,138', '#032412'),
    'pass': ('#2e0c1a', '#0d0408', '#ff5d86', '#ffd3df', '255,93,134', '#2c0612'),
    'tg': ('#07203a', '#030810', '#4fb4ff', '#d6ecff', '79,180,255', '#04203a'),
    'ia': ('#160d33', '#07060f', '#a78bfa', '#e9e0ff', '167,139,250', '#160b33'),
    'amb': ('#2a1806', '#0d0803', '#ffb340', '#ffe6c2', '255,179,64', '#2a1603'),
    # vigía de precios (video 8): amarillo Mercado Libre
    'ml': ('#2a2405', '#0c0a02', '#ffe14d', '#fff6c2', '255,225,77', '#2a2203'),
}


def svgpath(name):
    svg = open(os.path.join(HERE, 'logos', f'{name}.svg')).read()
    return re.search(r' d="([^"]+)"', svg).group(1)


BASE = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:transparent;font-family:""" + SANS + """;color:#fff;-webkit-font-smoothing:antialiased}
.scene{position:absolute;inset:0;overflow:hidden;background:radial-gradient(1300px 1150px at 50% 0%,var(--c1),var(--c2) 72%)}
.scene.in{animation:sIn .4s ease both}.scene.out{animation:sIn .4s ease both,sOut .4s ease var(--out) forwards}
@keyframes sIn{from{opacity:0;transform:scale(1.03)}to{opacity:1;transform:none}}
@keyframes sOut{to{opacity:0;transform:scale(.985)}}
.bg1{position:absolute;left:50%;top:-560px;width:1500px;height:1250px;margin-left:-750px;border-radius:50%;pointer-events:none;
  background:radial-gradient(closest-side,rgba(var(--acr),.5),rgba(var(--acr),.12) 55%,transparent);filter:blur(30px);animation:breathe 5s ease-in-out infinite alternate}
.bg2{position:absolute;left:-300px;bottom:-420px;width:1100px;height:900px;border-radius:50%;pointer-events:none;
  background:radial-gradient(closest-side,rgba(var(--acr),.18),transparent);filter:blur(40px)}
.grain{position:absolute;inset:0;pointer-events:none;opacity:.07;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)'/%3E%3C/svg%3E")}
@keyframes breathe{to{transform:translateY(70px) scale(1.1)}}
#g3{position:absolute;inset:0;z-index:5;pointer-events:none}
.p1,.p2,.p3,.p4,.pA,.pB{position:absolute;inset:0;z-index:9}
.z{position:relative;z-index:8}.top{z-index:9}
.L{position:absolute;inset:0}
.glass{border-radius:44px;background:linear-gradient(180deg,rgba(255,255,255,.14),rgba(255,255,255,.045));
  -webkit-backdrop-filter:blur(30px) saturate(1.5);backdrop-filter:blur(30px) saturate(1.5);
  box-shadow:inset 0 1.5px 0 rgba(255,255,255,.3),inset 0 0 0 1.5px rgba(255,255,255,.07),0 40px 90px rgba(0,0,0,.45)}
.solid{border-radius:44px;background:linear-gradient(180deg,#1d1b26,#121119);box-shadow:inset 0 1.5px 0 rgba(255,255,255,.12),0 40px 90px rgba(0,0,0,.5)}
.hero{border-radius:56px;overflow:visible;background:linear-gradient(160deg,var(--ac2) -40%,var(--ac) 10%,rgba(var(--acr),.35) 70%,rgba(0,0,0,.25));
  box-shadow:inset 0 2px 0 rgba(255,255,255,.55),inset 0 -40px 80px rgba(0,0,0,.25),0 50px 120px rgba(var(--acr),.35),0 30px 60px rgba(0,0,0,.4)}
.pill{display:inline-flex;align-items:center;gap:12px;padding:16px 28px;border-radius:999px;font-size:28px;font-weight:700;white-space:nowrap;
  background:linear-gradient(180deg,rgba(255,255,255,.18),rgba(255,255,255,.07));-webkit-backdrop-filter:blur(20px);backdrop-filter:blur(20px);
  box-shadow:inset 0 1.5px 0 rgba(255,255,255,.3),0 14px 34px rgba(0,0,0,.3)}
.pill svg{width:34px;height:34px}
.pill.on{background:linear-gradient(180deg,var(--ac2),var(--ac));color:var(--ink);box-shadow:inset 0 2px 0 rgba(255,255,255,.6),0 18px 40px rgba(var(--acr),.45)}
.pill.light{background:#f6f2ee;color:#151318;box-shadow:inset 0 -3px 0 rgba(0,0,0,.08),0 18px 40px rgba(0,0,0,.35)}
.pill.bad{background:linear-gradient(180deg,#ff9aa5,#ff4d5e);color:#2a0308;box-shadow:inset 0 2px 0 rgba(255,255,255,.5),0 18px 40px rgba(255,77,94,.45)}
.lbl{font-size:24px;font-weight:600;color:rgba(255,255,255,.55)}
.num{font-weight:800;letter-spacing:-.05em;line-height:.9;font-variant-numeric:tabular-nums}
.num .d{opacity:.38}
.g{color:var(--ac)}.dim{color:rgba(255,255,255,.55)}.red{color:#ff6b7a}
.ttl{position:absolute;left:60px;right:60px;text-align:center;font-weight:800;letter-spacing:-.045em;line-height:1.02;z-index:9}
.ttl em{font-style:normal;background:linear-gradient(180deg,var(--ac2) 5%,var(--ac) 85%);-webkit-background-clip:text;background-clip:text;color:transparent}
.ttl em.red{background:linear-gradient(180deg,#ffd6db,#ff5a6c);-webkit-background-clip:text;background-clip:text}
.beam{position:absolute;width:520px;height:520px;border-radius:50%;pointer-events:none;background:radial-gradient(closest-side,rgba(var(--acr),.55),rgba(var(--acr),.12) 60%,transparent);filter:blur(10px)}
.pop{animation:pop .6s cubic-bezier(.22,1.35,.36,1) both}
@keyframes pop{from{opacity:0;transform:translateY(46px) scale(.88)}to{opacity:1;transform:none}}
.rise{animation:rise .7s cubic-bezier(.22,1.1,.36,1) both}@keyframes rise{from{opacity:0;transform:translateY(160px)}to{opacity:1;transform:none}}
.fade{animation:fade .45s ease both}@keyframes fade{from{opacity:0}to{opacity:1}}
.gone{animation:gone .4s ease forwards}@keyframes gone{to{opacity:0;transform:translateY(-50px) scale(.95);filter:blur(10px)}}
.stamp{animation:stamp .45s cubic-bezier(.22,1.6,.36,1) both}@keyframes stamp{from{opacity:0;transform:scale(2.2) rotate(var(--r,-6deg))}to{opacity:1;transform:rotate(var(--r,-6deg))}}
@keyframes stIn{from{opacity:0;transform:translateY(34px) scale(.96);filter:blur(12px)}to{opacity:1;transform:none;filter:none}}
@keyframes stOut{to{opacity:0;transform:translateY(-34px);filter:blur(12px)}}
.type{display:inline-block;overflow:hidden;white-space:nowrap;vertical-align:bottom;font-family:'JetBrains Mono',monospace;animation:typ var(--td,1s) steps(var(--n,20)) both}
@keyframes typ{from{width:0}to{width:calc(var(--n,20) * 1ch)}}
/* encabezado de noticia */
.hd{position:absolute;left:60px;right:60px;top:108px;display:flex;align-items:center;gap:18px;z-index:9;animation:fade .4s ease .1s both}
.hd .n{width:78px;height:78px;border-radius:50%;background:linear-gradient(160deg,var(--ac2),var(--ac));color:var(--ink);display:flex;align-items:center;justify-content:center;
  font-size:30px;font-weight:800;box-shadow:inset 0 2px 0 rgba(255,255,255,.6),0 0 44px rgba(var(--acr),.6)}
.hd .pill{font-size:30px;padding:14px 28px 14px 18px}.hd .pill svg{width:42px;height:42px}
.hd .dots{margin-left:auto;display:flex;gap:10px}.hd .dots i{width:16px;height:16px;border-radius:8px;background:rgba(255,255,255,.18)}
.hd .dots i.on{width:48px;background:var(--ac);box-shadow:0 0 16px rgba(var(--acr),.7)}
"""

RUNTIME = r"""
import * as THREE from 'three';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';
import {SVGLoader} from 'three/addons/loaders/SVGLoader.js';
import {FontLoader} from 'three/addons/loaders/FontLoader.js';
import {TextGeometry} from 'three/addons/geometries/TextGeometry.js';
const el=document.getElementById('g3');
const ren=new THREE.WebGLRenderer({antialias:true,alpha:true,preserveDrawingBuffer:true});
ren.setPixelRatio(1);ren.setSize(1080,1920);ren.toneMapping=THREE.ACESFilmicToneMapping;ren.toneMappingExposure=1.05;el.appendChild(ren.domElement);
const scene=new THREE.Scene();scene.environment=new THREE.PMREMGenerator(ren).fromScene(new RoomEnvironment(),0.03).texture;
const cam=new THREE.PerspectiveCamera(30,1080/1920,1,200);cam.position.z=40;
const PX=1920/(2*40*Math.tan(15*Math.PI/180));
const key=new THREE.DirectionalLight('#ffffff',1.6);key.position.set(-6,10,12);scene.add(key);
const AC=getComputedStyle(document.querySelector('[data-root]')).getPropertyValue('--ac').trim()||'#a78bfa';
const rim=new THREE.PointLight(AC,260,60);rim.position.set(6,-8,8);scene.add(rim);
const R={THREE,scene,cam,PX,AC,
  u:p=>p/PX,
  at:(o,x,y,z=0)=>{o.position.set((x-540)/PX,(960-y)/PX,z);return o},
  k:(t,a,d)=>Math.min(1,Math.max(0,(t-a)/d)),
  eo:p=>1-Math.pow(1-p,3), eio:p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2,
  eb:p=>{const c=1.70158;return 1+(c+1)*Math.pow(p-1,3)+c*Math.pow(p-1,2)},
  mix:(a,b,p)=>a+(b-a)*p,
  gloss:(c,o={})=>new THREE.MeshPhysicalMaterial({color:c,roughness:.22,metalness:.05,clearcoat:1,clearcoatRoughness:.06,...o}),
  metal:(c,o={})=>new THREE.MeshPhysicalMaterial({color:c,roughness:.18,metalness:1,...o}),
  iri:(c='#ffffff',o={})=>new THREE.MeshPhysicalMaterial({color:c,roughness:.08,metalness:.2,clearcoat:1,iridescence:1,iridescenceIOR:1.35,iridescenceThicknessRange:[150,900],transparent:true,opacity:.92,...o}),
  glass:(c='#ffffff',o={})=>new THREE.MeshPhysicalMaterial({color:c,roughness:.04,metalness:0,clearcoat:1,transparent:true,opacity:.28,iridescence:.6,side:THREE.DoubleSide,envMapIntensity:2.2,depthWrite:false,...o}),
  rbox:(w,h,d,r,m)=>new THREE.Mesh(new RoundedBoxGeometry(w/PX,h/PX,d/PX,6,r/PX),m),
  group:()=>new THREE.Group(),
  // logo SVG (viewBox 24) extruido; size = ancho en px
  shape:(d,size,depth,m,bevel=.5)=>{const data=new SVGLoader().parse(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="${d}"/></svg>`);
    const shapes=data.paths.flatMap(p=>SVGLoader.createShapes(p));
    const g=new THREE.ExtrudeGeometry(shapes,{depth,bevelEnabled:true,bevelThickness:bevel,bevelSize:bevel*.5,bevelSegments:4,curveSegments:24});
    g.rotateX(Math.PI);g.center();g.computeBoundingBox();const s=(size/PX)/(g.boundingBox.max.x-g.boundingBox.min.x);g.scale(s,s,s);return new THREE.Mesh(g,m)},
  font:null,
  text:(str,size,depth,m)=>{const g=new TextGeometry(str,{font:R.font,size:size/PX,depth:depth/PX,curveSegments:16,bevelEnabled:true,bevelThickness:depth/PX*.25,bevelSize:size/PX*.03,bevelSegments:5});
    g.center();return new THREE.Mesh(g,m)},
  // estrella (placa de policía)
  star:(n,ro,ri,depth,m)=>{const s=new THREE.Shape();for(let i=0;i<n*2;i++){const r=i%2?ri:ro,a=i*Math.PI/n-Math.PI/2;const x=Math.cos(a)*r/PX,y=-Math.sin(a)*r/PX;i?s.lineTo(x,y):s.moveTo(x,y)}
    const g=new THREE.ExtrudeGeometry(s,{depth:depth/PX,bevelEnabled:true,bevelThickness:.12,bevelSize:.1,bevelSegments:4});g.center();return new THREE.Mesh(g,m)},
  // módulo de RAM
  ram:(w,col='#1f6b45')=>{const G=new THREE.Group(),h=w*.24;G.add(new THREE.Mesh(new RoundedBoxGeometry(w/PX,h/PX,10/PX,4,3/PX),R.gloss(col,{roughness:.35})));
    const cm=R.gloss('#0d0f12',{roughness:.3});for(let i=0;i<8;i++){const c=R.rbox(w*.095,h*.5,8,2,cm);c.position.set(((i-3.5)*w*.115)/PX,(h*.08)/PX,8/PX);G.add(c)}
    const gm=R.metal('#e2b74a',{roughness:.25});for(let i=0;i<34;i++){const p=new THREE.Mesh(new THREE.BoxGeometry(w*.018/PX,h*.16/PX,11/PX),gm);p.position.set(((i-16.5)*w*.027)/PX,(-h*.4)/PX,0);G.add(p)}
    const notch=R.rbox(w*.02,h*.2,12,1,R.gloss('#000'));notch.position.set(w*.08/PX,-h*.42/PX,0);G.add(notch);return G},
  // chip / CPU
  chip:(w,top='#2b3240',die='#123048',glow=AC)=>{const G=new THREE.Group();G.add(R.rbox(w,w,w*.08,w*.06,R.gloss('#1b1e24',{roughness:.4})));
    const lid=R.rbox(w*.78,w*.78,w*.06,w*.05,R.metal(top,{roughness:.22}));lid.position.z=w*.06/PX;G.add(lid);
    const d=R.rbox(w*.46,w*.46,w*.04,w*.03,R.gloss(die,{emissive:glow,emissiveIntensity:.35}));d.position.z=w*.1/PX;G.add(d);
    const pm=R.metal('#d9ae45');for(const sd of[0,1,2,3])for(let i=0;i<12;i++){const p=new THREE.Mesh(new THREE.BoxGeometry(w*.025/PX,w*.07/PX,w*.02/PX),pm);
      const o=((i-5.5)*w*.07)/PX,e=(w*.535)/PX;if(sd<2){p.position.set(o,sd?e:-e,0)}else{p.rotation.z=Math.PI/2;p.position.set(sd==2?e:-e,o,0)}G.add(p)}return G},
  coin:(r,m)=>{const c=new THREE.Mesh(new THREE.CylinderGeometry(r/PX,r/PX,r*.18/PX,64),m);c.rotation.x=Math.PI/2;const G=new THREE.Group();G.add(c);return G},
};
"""


def page(css, body, dur, script='', n=0, js3d=None, salida=True, t0=0.0):
    c1, c2, ac, ac2, acr, ink = PALETAS[n]
    cls = 'scene out' if salida else 'scene in'
    three = ''
    if js3d:
        three = f"""<script type="importmap">{{"imports":{{"three":"{THREE}/build/three.module.js","three/addons/":"{THREE}/examples/jsm/"}}}}</script>
<script type="module">{TRN.runtime(RUNTIME)}
R.D={dur};R.IN=t=>R.eb(R.k(t,.2,.75));R.OUT=t=>R.eo(R.k(t,R.D-.5,.42));
R.font=await new Promise(r=>new FontLoader().load('{THREE}/examples/fonts/helvetiker_bold.typeface.json',r));
const update=await (async(R)=>{{{js3d}}})(R);
const cnt=window.__seek;window.__seek=t=>{{cnt&&cnt(t);R.fx0&&R.fx0();update(t+{t0});R.fx&&R.fx(t);ren.render(scene,cam)}};window.__seek(0);window.__ok();
</script>"""
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}
<style>{BASE}{css}{TRN.CSS if TRN.TRANS else ''}</style>
<script>window.__listo=new Promise(r=>window.__ok=r);window.__seek=t=>window.__cnt&&window.__cnt(t);{'' if js3d else 'window.__ok();'}</script>
{TRN.head(TRN.cfg(dur, 'page', salida))}{three}</head><body><div class="{cls}" data-root style="--out:{dur - 0.4:.2f}s;--c1:{c1};--c2:{c2};--ac:{ac};--ac2:{ac2};--acr:{acr};--ink:{ink}">
<div class="bg1"></div><div class="bg2"></div>{'<div id="g3"></div>' if js3d else ''}{body}<div class="grain"></div></div>
<script>{script}</script>{TRN.tail()}</body></html>"""


def header(num, co_logo, co_name):
    dots = ''.join(f'<i class="{"on" if k + 1 == num else ""}"></i>' for k in range(4))
    return f'<div class="hd"><span class="n">{num:02d}</span><span class="pill">{co_logo}{co_name}</span><span class="dots">{dots}</span></div>'


def js(s):
    """Inserta un valor de Python como literal JS."""
    return json.dumps(s, ensure_ascii=False)


CARD = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:transparent;font-family:""" + SANS + """;color:#fff;-webkit-font-smoothing:antialiased}
#g3{position:absolute;inset:0;z-index:5;pointer-events:none}
.wrap{position:absolute;left:100px;width:880px;animation:cIn .75s cubic-bezier(.22,1.25,.36,1) both,cOut .45s cubic-bezier(.5,0,.75,0) var(--out) forwards}
@keyframes cIn{from{opacity:0;transform:translateY(-50px) scale(.9);filter:blur(12px)}to{opacity:1;transform:none;filter:none}}
@keyframes cOut{to{opacity:0;transform:translateY(-40px) scale(.94);filter:blur(10px)}}
.card{position:relative;border-radius:56px;padding:44px 46px;
  background:linear-gradient(165deg,rgba(var(--acr),.42) 0%,rgba(28,24,38,.92) 34%,rgba(13,12,19,.95) 100%);
  box-shadow:inset 0 2px 0 rgba(255,255,255,.38),inset 0 0 0 1.5px rgba(255,255,255,.08),0 50px 120px rgba(0,0,0,.6),0 0 110px rgba(var(--acr),.28)}
.card:before{content:'';position:absolute;left:-40px;top:-90px;width:520px;height:330px;border-radius:50%;pointer-events:none;background:radial-gradient(closest-side,rgba(255,255,255,.14),transparent);filter:blur(14px)}
.hd{display:flex;align-items:center;gap:22px;margin-bottom:30px;padding-right:var(--pr,0)}
.ic{width:84px;height:84px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:40px;font-weight:800;
  background:linear-gradient(160deg,var(--ac2),var(--ac));color:var(--ink);box-shadow:inset 0 2px 0 rgba(255,255,255,.6),0 0 36px rgba(var(--acr),.55)}
.ic svg{width:44px;height:44px}
.app{flex:1;font-size:30px;font-weight:800;letter-spacing:-.01em}.app small{display:block;font-size:23px;font-weight:600;color:rgba(255,255,255,.5);letter-spacing:0;margin-top:2px}
.pill{display:inline-flex;align-items:center;gap:10px;padding:12px 24px;border-radius:999px;font-size:24px;font-weight:700;white-space:nowrap;
  background:linear-gradient(180deg,rgba(255,255,255,.16),rgba(255,255,255,.06));box-shadow:inset 0 1.5px 0 rgba(255,255,255,.28)}
.pill.on{background:linear-gradient(180deg,var(--ac2),var(--ac));color:var(--ink);box-shadow:inset 0 2px 0 rgba(255,255,255,.6),0 12px 30px rgba(var(--acr),.4)}
.pill.ok{background:linear-gradient(180deg,#c9f8dc,#3ee08a);color:#032412;box-shadow:inset 0 2px 0 rgba(255,255,255,.6),0 10px 26px rgba(62,224,138,.35)}
.pill.bad{background:linear-gradient(180deg,#ffb0b9,#ff4d5e);color:#2a0308;box-shadow:inset 0 2px 0 rgba(255,255,255,.5),0 10px 26px rgba(255,77,94,.35)}
.sub{font-size:24px;color:rgba(255,255,255,.55);font-weight:600}
.ti{font-size:36px;font-weight:800;letter-spacing:-.02em}
.row{display:flex;gap:22px;align-items:center;padding:20px 24px;border-radius:32px;background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(255,255,255,.03));box-shadow:inset 0 1.5px 0 rgba(255,255,255,.12)}
.row+.row{margin-top:14px}
.mini{width:68px;height:68px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:34px;box-shadow:inset 0 2px 0 rgba(255,255,255,.35)}
.info{flex:1}.info .n{font-size:31px;font-weight:700}
.amt{font-size:34px;font-weight:800;text-align:right;font-variant-numeric:tabular-nums}
.num{font-weight:800;letter-spacing:-.05em;line-height:.95;font-variant-numeric:tabular-nums}.num .d{opacity:.4}
.g{color:var(--ac)}.green{color:#3ee08a}.red{color:#ff6b7a}.orange{color:#ffb340}
.dot{display:inline-block;width:14px;height:14px;border-radius:50%;background:#3ee08a;box-shadow:0 0 12px #3ee08a;animation:pulse 1.4s ease-in-out infinite}
@keyframes pulse{50%{box-shadow:0 0 0 8px rgba(62,224,138,0)}}
.pop{animation:pop .5s cubic-bezier(.22,1.35,.36,1) both}
@keyframes pop{from{opacity:0;transform:translateY(22px) scale(.94)}to{opacity:1;transform:none}}
.fade{animation:fade .35s ease both}@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes off{to{opacity:0}}
.type{display:inline-block;white-space:nowrap;clip-path:inset(0 100% 0 0);animation:type var(--td,1.4s) steps(var(--n,30),end) both}
@keyframes type{to{clip-path:inset(0 0 0 0)}}
.mono{font-family:'JetBrains Mono',monospace}
"""


def tarjeta(css, body, dur, script='', pal='fin', js3d=None, top=200, pr=0):
    """Tarjeta de vidrio sobre la cámara (fondo transparente); el 3D se ancla con R.at(o, x, y) en coordenadas de pantalla."""
    c1, c2, ac, ac2, acr, ink = PALETAS[pal]
    three = ''
    if js3d:
        three = f"""<script type="importmap">{{"imports":{{"three":"{THREE}/build/three.module.js","three/addons/":"{THREE}/examples/jsm/"}}}}</script>
<script type="module">{TRN.runtime(RUNTIME)}
R.D={dur};R.IN=t=>R.eb(R.k(t,.2,.75));R.OUT=t=>R.eo(R.k(t,R.D-.5,.42));
R.font=await new Promise(r=>new FontLoader().load('{THREE}/examples/fonts/helvetiker_bold.typeface.json',r));
const update=await (async(R)=>{{{js3d}}})(R);
const cnt=window.__seek;window.__seek=t=>{{cnt&&cnt(t);R.fx0&&R.fx0();update(t);R.fx&&R.fx(t);ren.render(scene,cam)}};window.__seek(0);window.__ok();
</script>"""
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}
<style>{CARD}{css}{TRN.CSS if TRN.TRANS else ''}</style>
<script>window.__listo=new Promise(r=>window.__ok=r);window.__seek=t=>window.__cnt&&window.__cnt(t);{'' if js3d else 'window.__ok();'}</script>
{TRN.head(dict(TRN.cfg(dur, 'card', True), F=[540, top + 86, 300, 96]))}{three}</head><body data-root style="--ac:{ac};--ac2:{ac2};--acr:{acr};--ink:{ink};--pr:{pr}px">
<div class="wrap" style="top:{top}px;--out:{dur - 0.45:.2f}s"><div class="card">{body}</div></div>{'<div id="g3"></div>' if js3d else ''}
<script>{script}</script>{TRN.tail()}</body></html>"""
