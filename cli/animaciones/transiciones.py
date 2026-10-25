"""Transiciones sin desvanecidos y 3D «limpio» para el estilo gloss (ellog_gloss.page / tarjeta).

Se activa con la variable TRANS (sin ella todo sale como siempre):
  desliz   — como hacer scroll: la escena nueva sube como una hoja y la anterior se va arriba con parallax;
             las piezas llegan escalonadas y se acomodan; las fases internas pasan como carrusel.
  ensamble — las piezas se compactan hacia una píldora al centro, la píldora se expande y forma la escena
             nueva, y de ahí salen disparadas a su lugar; las fases internas se compactan y se vuelven a armar.
En ambas, las piezas del 3D también se arman al entrar y se desarman al salir, y el 3D usa luz de estudio,
materiales satinados, bordes redondeados y supermuestreo.
Las piezas son los hijos de cada capa .pN (y lo suelto de .scene); las fases se leen de sus animaciones fade/gone.
"""
import json, os

TRANS = os.environ.get('TRANS', '')
COLA = 0.9 if TRANS else 0.45          # cuánto se queda una escena debajo de la siguiente
FOCO = (540, 960, 520, 116)            # píldora central (x, y, ancho, alto) donde se compacta todo en «ensamble»


def runtime(rt):
    """RUNTIME de three.js con la luz y los materiales nuevos + el gancho R.fx de las transiciones."""
    if not TRANS:
        return rt
    cambios = [
        ("ren.setPixelRatio(1);ren.setSize(1080,1920);ren.toneMapping=THREE.ACESFilmicToneMapping;ren.toneMappingExposure=1.05;",
         "ren.setPixelRatio(2);ren.setSize(1080,1920);ren.toneMapping=THREE.NeutralToneMapping;ren.toneMappingExposure=1.0;"),
        ("scene.environment=new THREE.PMREMGenerator(ren).fromScene(new RoomEnvironment(),0.03).texture;",
         "scene.environment=new THREE.PMREMGenerator(ren).fromScene(_estudio(),0.02).texture;"),
        ("const key=new THREE.DirectionalLight('#ffffff',1.6);key.position.set(-6,10,12);scene.add(key);",
         "const key=new THREE.DirectionalLight('#ffffff',1.1);key.position.set(-6,12,14);scene.add(key);"
         "scene.add(new THREE.HemisphereLight('#ffffff','#1a1824',.55));"),
        ("const rim=new THREE.PointLight(AC,260,60);", "const rim=new THREE.PointLight(AC,170,60);"),
        ("gloss:(c,o={})=>new THREE.MeshPhysicalMaterial({color:c,roughness:.22,metalness:.05,clearcoat:1,clearcoatRoughness:.06,...o}),",
         "gloss:(c,o={})=>new THREE.MeshPhysicalMaterial({color:c,roughness:.36,metalness:0,clearcoat:.45,clearcoatRoughness:.16,specularIntensity:.65,...o,"
         "roughness:Math.max(.3,o.roughness??.36)}),"),
        ("metal:(c,o={})=>new THREE.MeshPhysicalMaterial({color:c,roughness:.18,metalness:1,...o}),",
         "metal:(c,o={})=>new THREE.MeshPhysicalMaterial({color:c,roughness:.26,metalness:1,...o,roughness:Math.max(.24,o.roughness??.26)}),"),
        ("iridescence:1,iridescenceIOR:1.35", "iridescence:.65,iridescenceIOR:1.3"),
        ("rbox:(w,h,d,r,m)=>new THREE.Mesh(new RoundedBoxGeometry(w/PX,h/PX,d/PX,6,r/PX),m),",
         "rbox:(w,h,d,r,m)=>{const mn=Math.min(w,h,d);r=Math.min(Math.max(r,mn*.3),mn*.48);return new THREE.Mesh(new RoundedBoxGeometry(w/PX,h/PX,d/PX,8,r/PX),m)},"),
        ("bevelThickness:bevel,bevelSize:bevel*.5,bevelSegments:4,curveSegments:24",
         "bevelThickness:bevel*1.2,bevelSize:bevel*.6,bevelSegments:10,curveSegments:48"),
        ("curveSegments:16,bevelEnabled:true,bevelThickness:depth/PX*.25,bevelSize:size/PX*.03,bevelSegments:5",
         "curveSegments:24,bevelEnabled:true,bevelThickness:depth/PX*.3,bevelSize:size/PX*.035,bevelSegments:10"),
        ("bevelThickness:.12,bevelSize:.1,bevelSegments:4", "bevelThickness:.16,bevelSize:.12,bevelSegments:10"),
    ]
    for a, b in cambios:
        assert a in rt, a[:50]
        rt = rt.replace(a, b)
    estudio = r"""
// estudio fotográfico: fondo oscuro + softbox arriba + tiras laterales (reflejos limpios en vez de un cuarto)
function _estudio(){const s=new THREE.Scene();s.background=new THREE.Color('#3a3a46');
 const L=(w,h,k,x,y,z,c='#ffffff')=>{const m=new THREE.Mesh(new THREE.PlaneGeometry(w,h),new THREE.MeshBasicMaterial({color:new THREE.Color(c).multiplyScalar(k),side:THREE.DoubleSide}));
  m.position.set(x,y,z);m.lookAt(0,0,0);s.add(m)};
 L(34,26,3.6,0,24,8);L(8,34,2.8,-22,2,10);L(8,34,2.0,22,0,9);L(44,10,.8,0,-20,10,'#dfe3ff');L(30,30,.7,0,4,-26);L(26,16,1.1,4,8,30);return s}
"""
    i = rt.index('const el=document.getElementById')
    rt = rt[:i] + estudio + rt[i:]
    return rt + r"""
// ── transiciones: las partes del 3D se arman al entrar y se desarman al salir (desplazamientos que se quitan antes de cada update)
{const TR=window.__TR||{},_sv=[],V=THREE.Vector3;
 const _k=(t,a,d)=>Math.min(1,Math.max(0,(t-a)/d)),_h=i=>{const x=Math.sin(i*12.9898+4.1)*43758.5453;return x-Math.floor(x)};
 const FW=TR.F?new V((TR.F[0]-540)/PX,(960-TR.F[1])/PX,0):new V();
 R.fx0=()=>{for(const [o,p,r,s] of _sv){o.position.copy(p);o.rotation.copy(r);o.scale.copy(s)}_sv.length=0};
 R.fx=t=>{if(!TR.m)return;const D=TR.m==='desliz',S=TR.k==='card'?-1:1;
  const enter=t<2.2,leave=TR.T0!=null&&t>TR.T0-.45;if(!enter&&!leave)return;
  scene.updateMatrixWorld(true);let j=0;
  for(const o of scene.children){if(o.isLight||!o.visible||o.scale.x<.002)continue;
   const parts=o.children.length>1?o.children:[o];
   parts.forEach((p,i)=>{j++;const r1=_h(j),r2=_h(j+.37),r3=_h(j+.71);
    const qi=D?R.eb(_k(t,.12+i*.035,.9)):R.eb(_k(t,.45+i*.03,.85)),ei=1-qi;
    const qo=TR.T0==null?0:D?R.eio(_k(t,TR.T0+i*.02,.75)):Math.pow(_k(t,TR.T0-.4+i*.02,.5),2.2);
    if(ei<=.0005&&qo<=.0005)return;
    _sv.push([p,p.position.clone(),p.rotation.clone(),p.scale.clone()]);
    const w=p.getWorldPosition(new V()),d=new V();let sc=1;
    if(D){d.y+=S*(-ei*(7+r1*5))+qo*(9+r1*6);d.x+=ei*(r2-.5)*6+qo*(r2-.5)*4;p.rotation.x+=(ei+qo)*(r3-.5)*2.2;p.rotation.y+=(ei-qo)*(r1-.5)*2.4}
    else{d.copy(FW).sub(w).multiplyScalar(Math.max(ei,qo));sc=1-.85*ei-.92*qo;p.rotation.z+=(ei-qo)*(r3-.5)*3;p.rotation.y+=ei*(r2-.5)*2}
    const tgt=p.parent.worldToLocal(w.clone().add(d));p.position.copy(tgt);p.scale.multiplyScalar(Math.max(.001,sc))})}}}
"""


CSS = """
@keyframes sIn{from{}to{}}@keyframes sOut{from{}to{}}@keyframes cardIn{from{}to{}}@keyframes cIn{from{}to{}}@keyframes cOut{from{}to{}}
@keyframes dkIn{from{transform:translateX(-50%)}to{transform:translateX(-50%)}}
@keyframes stIn{from{opacity:1;clip-path:inset(0 -12% 100% -12%);transform:translateY(60px)}to{opacity:1;clip-path:inset(-25% -12% -35% -12%);transform:none}}
@keyframes stOut{from{opacity:1;clip-path:inset(-25% -12% -35% -12%);transform:none}to{opacity:1;clip-path:inset(100% -12% -35% -12%);transform:translateY(-60px)}}
.scrim{position:absolute;inset:0;background:#000;opacity:0;z-index:60;pointer-events:none}
.ring{position:absolute;z-index:61;pointer-events:none;border:3px solid rgba(255,255,255,.75);box-shadow:inset 0 0 40px rgba(var(--acr),.8),inset 0 0 0 1px rgba(255,255,255,.3)}
"""

JS = r"""
(()=>{const C=window.__TR,W=1080,H=1920,DZ=C.m==='desliz';
const EIO='cubic-bezier(.65,0,.35,1)',EIN='cubic-bezier(.6,0,.8,.3)',SPR='cubic-bezier(.2,1.12,.3,1)',SPR2='cubic-bezier(.2,1.04,.3,1)',SPR3='cubic-bezier(.3,1.08,.4,1)',EIN2='cubic-bezier(.5,0,.75,0)';
// en pausa y persistentes desde que nacen: si corrieran en tiempo real, el navegador descarta las que terminan antes de la captura
const fija=x=>{x.pause();x.currentTime=0;x.persist();return x};
const an=(el,kf,d,dur,ease,fill)=>fija(el.animate(kf,{delay:Math.max(0,d)*1000,duration:dur*1000,easing:ease,fill}));
const hide=(el,a,b)=>fija(el.animate([{visibility:'hidden'},{visibility:'hidden'}],{delay:a*1000,duration:(b-a)*1000,fill:'none'}));
const R=el=>el.getBoundingClientRect(),area=r=>r.width*r.height;
const SKIP='script,style,link,.bg1,.bg2,.grain,#g3,.scrim,.ring';
const piezas=(layer,suelta)=>{const out=[];for(const el of layer.children){if(el.matches(SKIP))continue;const r=R(el);
  if(area(r)>W*H*(suelta?.45:.8)){if(!suelta&&el.children.length)out.push(...piezas(el,false));continue}
  if(area(r)<4&&!el.children.length)continue;out.push(el)}return out};
const filas=el=>el.matches('.tr,.card')?[...el.children]:el.matches('.cc.hi')?[...(el.querySelector('.cb')?.children||[])]:[];
const ctr=r=>[r.left+r.width/2,r.top+r.height/2];
// entrada/salida de un grupo de piezas en el tiempo t; f = foco [x,y] para «ensamble»
function entra(ps,t,f,lado){for(const p of ps){const r=R(p),[cx,cy]=ctr(r),fl=filas(p);
  if(DZ){const k=r.top/H;
   if(lado){an(p,[{translate:'1140px 0'},{translate:'0 0'}],t+k*.12,.8,SPR2,'backwards');
    fl.forEach((e,i)=>an(e,[{translate:`${140+i*46}px 0`},{translate:'0 0'}],t+k*.12+.06+i*.04,.75,SPR2,'backwards'))}
   else{an(p,[{translate:`0 ${260+r.top*.32}px`},{translate:'0 0'}],t+.1+k*.22,.9,SPR2,'backwards');
    fl.forEach((e,i)=>an(e,[{translate:`0 ${60+i*22}px`},{translate:'0 0'}],t+.2+k*.22+i*.045,.75,SPR2,'backwards'))}}
  else{const dx=f[0]-cx,dy=f[1]-cy,ds=Math.hypot(dx,dy)/1100;
   const t1=t+(lado?.22:.38)+ds*.24;
   an(p,[{translate:`${dx}px ${dy}px`,scale:.12},{translate:'0px 0px',scale:1}],t1,.85,SPR3,'backwards');
   fl.forEach((e,i)=>{const q=R(e),[ex,ey]=ctr(q);an(e,[{translate:`${(cx-ex)*.85}px ${(cy-ey)*.85}px`,scale:.4},{translate:'0px 0px',scale:1}],t1+.16+i*.045,.7,SPR3,'backwards')})}}}
function sale(ps,t,f,lado){for(const p of ps){const r=R(p),[cx,cy]=ctr(r),fl=filas(p);
  if(DZ){const k=r.top/H;
   if(lado)an(p,[{translate:'0 0'},{translate:'-1140px 0'}],t+k*.12,.62,EIO,'forwards');
   else an(p,[{translate:'0 0'},{translate:`0 ${-(170+(H-r.top)*.2)}px`}],t+k*.1,.78,EIO,'forwards')}
  else{const dx=f[0]-cx,dy=f[1]-cy,ds=Math.hypot(dx,dy)/1100;
   const t1=t-(lado?.15:.4);
   fl.forEach((e,i)=>{const q=R(e),[ex,ey]=ctr(q);an(e,[{translate:'0px 0px',scale:1},{translate:`${(cx-ex)*.85}px ${(cy-ey)*.85}px`,scale:.4}],t1+(fl.length-i)*.025,.36,EIN2,'forwards')});
   an(p,[{translate:'0px 0px',scale:1},{translate:`${dx}px ${dy}px`,scale:.08}],t1+.12+(1-Math.min(1,ds))*.12,.48,EIN2,'forwards')}}}
function arma(){
 const F=C.F,pill=(x,y,w,h,el)=>{const b=R(el);return `inset(${y-h/2-b.top}px ${b.right-x-w/2}px ${b.bottom-y-h/2}px ${x-w/2-b.left}px round ${h/2}px)`};
 if(C.k==='card'){const wr=document.querySelector('.wrap'),cd=wr.querySelector('.card'),r=R(wr),fl=[...cd.children],T0=C.T0;
  if(DZ){const up=-(r.bottom+80);
   an(wr,[{translate:`0 ${up}px`},{translate:'0 0'}],0,.85,SPR2,'backwards');
   fl.forEach((e,i)=>an(e,[{translate:`0 ${-(40+i*16)}px`},{translate:'0 0'}],.14+i*.05,.7,SPR2,'backwards'));
   fl.forEach((e,i)=>an(e,[{translate:'0 0'},{translate:`0 ${-(30+(fl.length-i)*14)}px`}],T0+(fl.length-i)*.03,.4,EIN,'forwards'));
   an(wr,[{translate:'0 0'},{translate:`0 ${up}px`}],T0+.12,.6,EIO,'forwards')}
  else{const hd=R(fl[0]),f=[r.left+r.width/2,hd.top+hd.height/2],cp=pill(f[0],f[1],300,96,cd),full='inset(-160px -160px -160px -160px round 216px)';
   an(cd,[{clipPath:cp,scale:.94},{clipPath:full,scale:1}],.06,.75,'cubic-bezier(.7,0,.2,1)','backwards');
   fl.forEach((e,i)=>{const q=R(e),[ex,ey]=ctr(q);an(e,[{translate:`${(f[0]-ex)*.8}px ${(f[1]-ey)*.8}px`,scale:.3},{translate:'0px 0px',scale:1}],.3+i*.05,.75,SPR,'backwards')});
   fl.forEach((e,i)=>{const q=R(e),[ex,ey]=ctr(q);an(e,[{translate:'0px 0px',scale:1},{translate:`${(f[0]-ex)*.8}px ${(f[1]-ey)*.8}px`,scale:.3}],T0+(fl.length-i)*.03,.42,EIN,'forwards')});
   an(cd,[{clipPath:full,scale:1},{clipPath:cp,scale:.94}],T0+.18,.42,'cubic-bezier(.7,0,.2,1)','forwards');
   an(wr,[{scale:1,translate:'0 0'},{scale:.001,translate:'0 -40px'}],T0+.58,.17,EIN,'forwards')}
  return}
 const root=document.querySelector('.scene');
 const capas=[...root.children].filter(e=>[...e.classList].some(c=>/^p\d$/.test(c)));
 const fases=capas.map(el=>{let a=null,b=null;for(const x of el.getAnimations()){const d=x.effect.getTiming().delay/1000;
   if(x.animationName==='fade')a=d;else if(x.animationName==='gone')b=d}return{el,a,b,ps:piezas(el,false)}});
 for(const f of fases)if(f.a!=null||f.b!=null){f.el.style.animation='none';f.el.style.opacity='1'}
 const sueltas=piezas(root,true).filter(e=>!capas.includes(e));
 const foco=ps=>{const c=ps.find(p=>p.matches('.tr,.cc.hi'));if(!c)return[F[0],F[1]];const[x,y]=ctr(R(c));return[x,Math.min(y,R(c).top+260)]};
 // fases internas (cambio de tarjeta dentro de la misma escena)
 for(const f of fases){const fc=foco(f.ps);
  if(f.a!=null&&f.a>.05){hide(f.el,0,f.a);entra(f.ps,f.a,fc,true)}
  if(f.b!=null){sale(f.ps,f.b,fc,true);hide(f.el,f.b+.9,1e5)}}
 // la escena entra
 const inicio=fases.filter(f=>f.a==null||f.a<=.05).flatMap(f=>f.ps).concat(sueltas);
 if(DZ)an(root,[{translate:'0 1920px',borderRadius:'90px'},{translate:'0 0',borderRadius:'0px'}],0,.8,EIO,'backwards');
 else{const K=[[60,60,.0],[F[2],F[3],.22],[W,H,1]],ez='cubic-bezier(.6,0,.2,1)',rg=document.createElement('div');
  an(root,K.map(([w,h,o],i)=>({clipPath:i==2?'inset(0px 0px 0px 0px round 0px)':pill(F[0],F[1],w,h,root),offset:o})),0,1.0,ez,'backwards');
  rg.className='ring';root.appendChild(rg);
  an(rg,K.map(([w,h,o],i)=>({left:`${F[0]-w/2}px`,top:`${F[1]-h/2}px`,width:`${w}px`,height:`${h}px`,borderRadius:i==2?'0px':`${h/2}px`,borderColor:i==2?'rgba(255,255,255,0)':'rgba(255,255,255,.75)',offset:o})),0,1.0,ez,'both')}
 entra(inicio,0,F,false);
 // la escena sale (al final queda lo que siga visible)
 if(C.T0!=null){const fin=fases.filter(f=>f.b==null).flatMap(f=>f.ps).concat(sueltas),T0=C.T0;
  sale(fin,T0,F,false);
  if(C.cubre){if(DZ){an(root,[{translate:'0 0',scale:1},{translate:'0 -30%',scale:.94}],T0,.85,EIO,'forwards');
    const s=document.createElement('div');s.className='scrim';root.appendChild(s);an(s,[{opacity:0},{opacity:.55}],T0,.8,'ease-in','forwards')}}
  else if(DZ)an(root,[{translate:'0 0',borderRadius:'0px'},{translate:'0 -105%',borderRadius:'90px'}],T0+.1,.75,'cubic-bezier(.7,0,.3,1)','forwards');
  else an(root,[{clipPath:'inset(0px 0px 0px 0px round 0px)',offset:0},{clipPath:pill(F[0],F[1],F[2],F[3],root),offset:.8},{clipPath:pill(F[0],F[1],2,2,root),offset:1}],T0+.25,.6,'cubic-bezier(.7,0,.3,1)','forwards')}}
const prev=window.__listo;window.__listo=Promise.all([prev,document.fonts.ready.then(arma)]);
})();
"""


def cfg(dur, kind, salida, cubre=None):
    """Configuración de la página: kind 'page' | 'card'; T0 = cuándo empieza a salir (segundos locales)."""
    if kind == 'card':
        T0 = dur - 0.8
    elif salida:
        T0 = dur - 0.85
    else:
        T0 = dur - COLA
    return {'m': TRANS, 'k': kind, 'D': dur, 'T0': round(T0, 3), 'cubre': (not salida) if cubre is None else cubre, 'F': list(FOCO)}


def head(c):
    """<script> para el <head>: deja la configuración antes de que corra el módulo 3D."""
    return f'<script>window.__TR={json.dumps(c)};</script>' if TRANS else ''


def tail():
    return f'<script>{JS}</script>' if TRANS else ''
