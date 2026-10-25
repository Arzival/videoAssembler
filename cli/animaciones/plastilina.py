"""Estilo «Plastilina»: claymation (contratendencia 2026 al contenido brilloso/hiperreal): todo parece modelado a mano en
plastilina — objetos 3D mates con huellas, colores pastel, rebotes que aplastan y estiran, letras gorditas y movimiento
de stop-motion a 12 cps con el ligero «temblor» de mano entre cuadros. Entre escenas, una mancha de plastilina del color
nuevo se aplasta desde un punto y cubre la pantalla.

Tiempos: segundos del video final; A(t) = retardo local. js3d = cuerpo JS (recibe C y THREE, devuelve update(t)).
"""
import json, re
import ellog_gloss as G

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Nunito:wght@600;800;900&display=block" rel="stylesheet">')
COLA = 0.7
CPS = 12
PAS = {'rosa': '#ffb3c7', 'durazno': '#ffc79a', 'menta': '#a8e6cf', 'cielo': '#9fd3ff', 'lila': '#c9b6ff', 'limon': '#fff09a',
       'rojo': '#ff6b6b', 'azul': '#5b8cff', 'verde': '#4cc38a', 'naranja': '#ff9f43', 'morado': '#9b6bff', 'cafe': '#a9745b', 'blanco': '#fff8ef', 'negro': '#3b3340'}
FONDOS = {'crema': ('#fff3e3', '#ffe0c2'), 'rosa': ('#ffe3ea', '#ffc6d3'), 'menta': ('#e2f7ee', '#bfead6'), 'cielo': ('#e1f1ff', '#bfdcff'),
          'lila': ('#efe8ff', '#d9cbff'), 'limon': ('#fffbe0', '#fff0a8'), 'noche': ('#3b3554', '#262138')}

BASE = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:transparent;font-family:'Fredoka',sans-serif;color:#3b3340;-webkit-font-smoothing:antialiased;font-synthesis:none}
.mesa{position:absolute;inset:0;overflow:hidden;background:radial-gradient(1200px 1500px at 50% 35%,var(--f1),var(--f2))}
.mesa:after{content:'';position:absolute;inset:0;pointer-events:none;z-index:70;opacity:.35;mix-blend-mode:multiply;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.7' numOctaves='2'/%3E%3CfeColorMatrix values='0 0 0 0 .4 0 0 0 0 .3 0 0 0 0 .3 0 0 0 .35 0'/%3E%3C/filter%3E%3Crect width='240' height='240' filter='url(%23n)'/%3E%3C/svg%3E");
  animation:boil .5s steps(1) infinite}
@keyframes boil{0%{transform:translate(0,0)}25%{transform:translate(-9px,5px)}50%{transform:translate(6px,-7px)}75%{transform:translate(-4px,-4px)}}
#c3{position:absolute;inset:0;z-index:14;pointer-events:none}
/* letras de plastilina: gorditas, con grosor y sombra suave; tiemblan como stop-motion */
.pl{position:absolute;left:60px;right:60px;z-index:20;font-weight:700;line-height:.98;letter-spacing:-.01em}
.pl .w{display:inline-block;margin-right:.2em;color:var(--c,#3b3340);
  text-shadow:0 .025em 0 var(--o,rgba(0,0,0,.25)),0 .05em 0 var(--o,rgba(0,0,0,.25)),0 .075em 0 var(--o,rgba(0,0,0,.25)),0 .14em .12em rgba(60,30,30,.25);
  animation:aplasta .55s steps(7) var(--d) both,tiembla .5s steps(1) var(--d) infinite}
.pl .w.x{animation:aplasta .55s steps(7) var(--d) both,tiembla .5s steps(1) var(--d) infinite,salta .45s steps(5) var(--x) forwards}
@keyframes aplasta{0%{transform:translateY(-1.4em) scale(.7,1.4);opacity:0}45%{transform:translateY(0) scale(1.35,.65);opacity:1}70%{transform:scale(.9,1.12)}100%{transform:none;opacity:1}}
@keyframes tiembla{0%{rotate:-.6deg}25%{rotate:.5deg;translate:1px 0}50%{rotate:-.3deg;translate:0 1px}75%{rotate:.6deg}}
@keyframes salta{40%{transform:scale(1.15,.85)}100%{transform:translateY(1.6em) scale(.2,.2);opacity:0}}
/* bloque de plastilina aplanada (tarjeta) */
.pz{position:absolute;z-index:16;border-radius:46px;padding:30px 36px;background:var(--b,#fff8ef);color:#3b3340;
  box-shadow:inset 0 -14px 0 rgba(0,0,0,.08),inset 0 10px 18px rgba(255,255,255,.55),0 18px 0 var(--o,rgba(0,0,0,.12)),0 30px 40px rgba(60,30,30,.22);
  animation:pzin .6s steps(7) var(--d) both,tiembla .5s steps(1) var(--d) infinite}
.pz.x{animation:pzin .6s steps(7) var(--d) both,tiembla .5s steps(1) var(--d) infinite,salta .45s steps(5) var(--x) forwards}
@keyframes pzin{0%{transform:scale(.2,.2) translateY(200px);opacity:0}40%{transform:scale(1.18,.82);opacity:1}65%{transform:scale(.94,1.06)}100%{transform:none;opacity:1}}
.pz .tt{font-size:44px;font-weight:700}.pz .sb{font-family:Nunito;font-weight:800;font-size:30px;opacity:.7}
.chip{display:inline-block;padding:10px 26px;border-radius:999px;font-weight:700;font-size:34px;background:var(--b,#ffb3c7);margin:6px 8px 0 0;
  box-shadow:inset 0 -6px 0 rgba(0,0,0,.1),0 8px 0 rgba(0,0,0,.08);animation:pzin .5s steps(6) var(--d) both}
.num{position:absolute;z-index:18;font-weight:700;line-height:.9;color:var(--c,#ff6b6b);
  text-shadow:0 .02em 0 rgba(0,0,0,.2),0 .04em 0 rgba(0,0,0,.2),0 .06em 0 rgba(0,0,0,.2),0 .1em .08em rgba(60,30,30,.25);animation:pzin .6s steps(7) var(--d) both}
.mono{font-family:Nunito;font-weight:900}
.ap{opacity:0;animation:apo .01s steps(1) var(--d) forwards}.ap.x{animation:apo .01s steps(1) var(--d) forwards,apc .01s steps(1) var(--x) forwards}
@keyframes apo{to{opacity:1}}@keyframes apc{to{opacity:0}}
"""

JS = """const _Q=1000/%d;window.__cps=1000/_Q;  // capturar.ts: los cuadros del mismo paso son idénticos
const _e=p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2;
const _v=(k,t)=>{let v=k[0][1];for(const [a,b,d] of k.slice(1)){const p=Math.min(1,Math.max(0,(t-a)/(d||.8)));v=v+(b-v)*_e(p)}return v};
const _f=(v,f)=>f==='c'?Math.round(v).toLocaleString('en-US'):f==='1'?v.toFixed(1):f==='p'?Math.round(v)+'%%':Math.round(v);
const _N=[...document.querySelectorAll('[data-n]')].map(e=>[e,JSON.parse(e.dataset.n)]);
window.__seek=s=>{const ms=Math.floor(s*1000/_Q+1e-6)*_Q;for(const a of document.getAnimations()){a.pause();a.currentTime=ms}
 const t=ms/1000+S0;for(const [e,k] of _N)e.textContent=(e.dataset.pre||'')+_f(_v(k,t),e.dataset.f)+(e.dataset.suf||'');window.__u3&&window.__u3(t)};
const _F=['700 100px Fredoka','900 100px Nunito'];
window.__listo=Promise.all(_F.map(f=>document.fonts.load(f))).then(()=>document.fonts.ready).then(()=>{const m=_F.filter(f=>!document.fonts.check(f));if(m.length)throw new Error('faltan fuentes: '+m)}).then(()=>window.__c3);
window.__seek(0);""" % CPS

RT3D = r"""
import * as THREE from 'three';
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';
import {SVGLoader} from 'three/addons/loaders/SVGLoader.js';
const el=document.getElementById('c3');
const ren=new THREE.WebGLRenderer({antialias:true,alpha:true,preserveDrawingBuffer:true});
ren.setPixelRatio(location.hash.includes("preview")?1:2);ren.setSize(1080,1920);ren.shadowMap.enabled=true;ren.shadowMap.type=THREE.PCFSoftShadowMap;ren.toneMapping=THREE.NeutralToneMapping;
el.appendChild(ren.domElement);ren.domElement.addEventListener('webglcontextlost',()=>{window.__perdido=true});
const scene=new THREE.Scene();
const cam=new THREE.PerspectiveCamera(30,1080/1920,1,200);cam.position.z=40;
const PX=1920/(2*40*Math.tan(15*Math.PI/180));
scene.add(new THREE.HemisphereLight('#fff6ee','#c9a9a0',1.7));
const sun=new THREE.DirectionalLight('#fff1e2',2.1);sun.position.set(-8,14,22);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);
Object.assign(sun.shadow.camera,{left:-20,right:20,top:34,bottom:-34,near:1,far:90});sun.shadow.radius=9;sun.shadow.bias=-.0006;scene.add(sun);
if(PISO){const piso=new THREE.Mesh(new THREE.PlaneGeometry(80,120),new THREE.ShadowMaterial({opacity:.2}));piso.receiveShadow=true;scene.add(piso)}
// huellas de plastilina: mapa de relieve con manchas y rayones suaves
const BUMP=(()=>{const c=document.createElement('canvas');c.width=c.height=512;const g=c.getContext('2d');g.fillStyle='#808080';g.fillRect(0,0,512,512);
 let sd=11;const rn=()=>(sd=(sd*16807)%2147483647)/2147483647;
 for(let i=0;i<260;i++){const x=rn()*512,y=rn()*512,r=8+rn()*40;const gr=g.createRadialGradient(x,y,0,x,y,r);const v=rn()<.5?100:150;
  gr.addColorStop(0,`rgba(${v},${v},${v},.35)`);gr.addColorStop(1,'rgba(128,128,128,0)');g.fillStyle=gr;g.beginPath();g.arc(x,y,r,0,7);g.fill()}
 g.strokeStyle='rgba(95,95,95,.25)';for(let i=0;i<70;i++){g.lineWidth=1+rn()*2;g.beginPath();const x=rn()*512,y=rn()*512;g.arc(x,y,6+rn()*16,rn()*6,rn()*6+1.5);g.stroke()}
 const t=new THREE.CanvasTexture(c);t.wrapS=t.wrapT=THREE.RepeatWrapping;return t})();
const C={THREE,scene,PX,
 u:p=>p/PX, at:(o,x,y,z=1.5)=>{o.position.set((x-540)/PX,(960-y)/PX,z);return o},
 k:(t,a,d)=>Math.min(1,Math.max(0,(t-a)/d)), eo:p=>1-Math.pow(1-p,3), eio:p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2,
 h:i=>{const x=Math.sin(i*12.9898+4.1)*43758.5453;return x-Math.floor(x)},
 barro:(c,o={})=>new THREE.MeshStandardMaterial({color:c,roughness:.78,metalness:0,bumpMap:BUMP,bumpScale:1.2,...o}),
 sombra:o=>{o.traverse(m=>{if(m.isMesh){m.castShadow=true;m.receiveShadow=true}});return o},
 bola:(r,c)=>C.sombra(new THREE.Mesh(new THREE.SphereGeometry(r/PX,48,32),C.barro(c))),
 capsula:(r,l,c)=>C.sombra(new THREE.Mesh(new THREE.CapsuleGeometry(r/PX,l/PX,12,32),C.barro(c))),
 caja:(w,h,d,c,r)=>C.sombra(new THREE.Mesh(new RoundedBoxGeometry(w/PX,h/PX,d/PX,10,Math.min(r??Math.min(w,h,d)*.32,Math.min(w,h,d)*.49)/PX),C.barro(c))),
 dona:(r,g,c)=>C.sombra(new THREE.Mesh(new THREE.TorusGeometry(r/PX,g/PX,28,64),C.barro(c))),
 cil:(r,h,c)=>C.sombra(new THREE.Mesh(new THREE.CylinderGeometry(r/PX,r/PX,h/PX,48),C.barro(c))),
 cono:(r,h,c)=>C.sombra(new THREE.Mesh(new THREE.ConeGeometry(r/PX,h/PX,40),C.barro(c))),
 // figura SVG (viewBox 24) modelada en plastilina: muy redondeada
 logo:(d,size,c,grosor=40)=>{const data=new SVGLoader().parse(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="${d}"/></svg>`);
  const shapes=data.paths.flatMap(p=>SVGLoader.createShapes(p));const g0=new THREE.ShapeGeometry(shapes);g0.computeBoundingBox();const bw=g0.boundingBox.max.x-g0.boundingBox.min.x;
  const k=bw/size;const g=new THREE.ExtrudeGeometry(shapes,{depth:grosor*k*.5,bevelEnabled:true,bevelThickness:grosor*k*.3,bevelSize:grosor*k*.18,bevelSegments:8,curveSegments:32});
  g.rotateX(Math.PI);g.center();const s=(size/PX)/bw;g.scale(s,s,s);return C.sombra(new THREE.Mesh(g,C.barro(c)))},
 grupo:()=>new THREE.Group(),
 // cae desde arriba y se aplasta al tocar (squash & stretch). Devuelve progreso.
 cae:(o,t,t0,y0=500,d=.6)=>{const p=C.k(t,t0,d);o.visible=t>=t0;const b=p<.55?p/.55:1;const yy=(1-b*b)*y0/PX;
  let sx=1,sy=1;if(p<.55){sy=1.25;sx=.82}else{const q=(p-.55)/.45;const w=Math.sin(q*Math.PI*2.2)*Math.exp(-q*3);sy=1-.38*w;sx=1+.3*w}
  o.userData.dy=yy;o.userData.sq=[sx,sy];return p},
 // brota de la mesa (escala desde 0 con rebote gelatinoso)
 brota:(o,t,t0,d=.6)=>{const p=C.k(t,t0,d);o.visible=t>=t0;const w=p<1?1+Math.sin(p*Math.PI*2.4)*(1-p)*.5:1;const s=Math.max(.001,Math.min(1,p*1.6))*w;o.userData.sq=[s,s*(2-w)];return p},
 // se aplasta y desaparece (sale)
 aplasta:(o,t,t0,d=.4)=>{if(t<t0)return 0;const p=C.k(t,t0,d);const s=o.userData.sq||[1,1];o.userData.sq=[s[0]*(1+p*.8),s[1]*Math.max(.02,1-p)];if(p>=1)o.visible=false;return p},
 // aplica dy/sq y el temblor de stop-motion (cambia en cada cuadro de 12 cps)
 pon:(o,x,y,z=1.5,t=0,i=0,base=1)=>{C.at(o,x,y,z);o.position.y+=o.userData.dy||0;const s=o.userData.sq||[1,1];o.scale.set(base*s[0],base*s[1],base*s[0]);
  const f=Math.floor(t*12),jz=(C.h(f*7+i)-.5)*.035;if(o.userData.rz!=null&&Math.abs(o.rotation.z-o.userData.rz)<1e-9)o.rotation.z-=o.userData.jz||0;
  o.rotation.z+=jz;o.userData.jz=jz;o.userData.rz=o.rotation.z;o.position.x+=(C.h(f*13+i)-.5)*.04;o.userData.dy=0;o.userData.sq=[1,1]},
};
"""


def at(start):
    return lambda t: f'{max(0.0, t - start):.2f}s'


def letras(lineas, A, t, top=300, size=120, sale=None, color=None, step=.07, align='left', extra=''):
    """Palabras que caen y se aplastan. *palabra* = color de acento (var(--ac)); [palabra|#color] = color propio."""
    html, k = '', 0
    lineas = [re.sub(r'\*([^*]+?)\*', lambda m_: ' '.join(f'*{w}*' for w in m_.group(1).split(' ')), ln) for ln in lineas]
    for ln in lineas:
        ws = []
        for w in ln.split(' '):
            c = ''
            m = re.match(r'^\*(.+)\*(.*)$', w)
            if m:
                w = m.group(1) + m.group(2); c = 'var(--ac,#ff6b6b)'
            m = re.match(r'^\[(.+)\|(#[0-9a-fA-F]{3,6})\](.*)$', w)
            if m:
                w = m.group(1) + m.group(3); c = m.group(2)
            st = f'--d:{A(t + k * step)};' + (f'--c:{c};' if c else '')
            cls = 'w'
            if sale is not None:
                cls += ' x'; st += f'--x:{A(sale + k * .03)};'
            ws.append(f'<span class="{cls}" style="{st}">{w}</span>')
            k += 1
        html += '<div>' + ''.join(ws) + '</div>'
    col = f'--c:{color};' if color else ''
    return f'<div class="pl" style="top:{top}px;font-size:{size}px;text-align:{align};{col}{extra}">{html}</div>'


def bloque(x, y, w, html, A, t, sale=None, color='#fff8ef', extra=''):
    st = f'left:{x}px;top:{y}px;width:{w}px;--d:{A(t)};--b:{color};{extra}'
    cls = 'pz'
    if sale is not None:
        cls += ' x'; st += f'--x:{A(sale)};'
    return f'<div class="{cls}" style="{st}">{html}</div>'


def chip(txt, A, t, color='#ffb3c7'):
    return f'<span class="chip" style="--d:{A(t)};--b:{color}">{txt}</span>'


def N(keys, f='', suf='', pre=''):
    return (f"<b data-n='{json.dumps([list(k) for k in keys])}'" + (f' data-f="{f}"' if f else '') + (f' data-suf="{suf}"' if suf else '')
            + (f' data-pre="{pre}"' if pre else '') + ' style="font-weight:inherit">0</b>')


def numero(html, x, y, size, A, t, color='#ff6b6b'):
    return f'<div class="num" style="left:{x}px;top:{y}px;font-size:{size}px;--d:{A(t)};--c:{color}">{html}</div>'


def ap(html, A, t, sale=None):
    cls, st = 'ap', f'--d:{A(t)};'
    if sale is not None:
        cls += ' x'; st += f'--x:{A(sale)};'
    return f'<div class="{cls}" style="{st}">{html}</div>'


def page(css, body, dur, S0=0.0, fondo='crema', entra=(540, 1300), ac='#ff6b6b', js3d=None, transparente=False):
    """Escena. entra = punto desde donde la mancha de plastilina del fondo nuevo se aplasta y cubre (o None)."""
    f1, f2 = FONDOS[fondo]
    tres = ''
    if js3d:
        body = '<div id="c3"></div>' + body
        tres = (f'<script>window.__c3=new Promise(r=>window.__c3ok=r);</script><script type="importmap">{{"imports":{{"three":"{G.THREE}/build/three.module.js",'
                f'"three/addons/":"{G.THREE}/examples/jsm/"}}}}</script><script type="module">{RT3D.replace("PISO", "false" if transparente else "true")}\n'
                f'const update=await (async(C,THREE)=>{{{js3d}}})(C,THREE);window.__u3=t=>{{if(window.__perdido||ren.getContext().isContextLost())throw new Error("contexto WebGL perdido");'
                f'update(t);ren.render(scene,cam)}};window.__u3({S0});window.__c3ok();</script>')
    if transparente:
        inner = f'<div style="position:absolute;inset:0;--ac:{ac}">{body}</div>'
    else:
        if entra:
            x, y = entra
            # mancha: círculo con borde ondulado que crece a pasos con un rebote
            css += (f'@keyframes mancha{{0%{{clip-path:circle(0px at {x}px {y}px)}}55%{{clip-path:circle(1700px at {x}px {y}px)}}75%{{clip-path:circle(1500px at {x}px {y}px)}}'
                    f'100%{{clip-path:circle(2400px at {x}px {y}px)}}}}.mesa{{animation:mancha .65s steps(8) both}}')
        inner = f'<div class="mesa" style="--f1:{f1};--f2:{f2};--ac:{ac}">{body}</div>'
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{BASE}{css}</style>{tres}</head><body>{inner}
<script>const S0={S0};{JS}</script></body></html>"""
