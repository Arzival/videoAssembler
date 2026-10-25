// Sombras: runtime de las páginas de terror (siluetas articuladas sobre fondos de shader).
// Cada página define window.ESC = {gl: 'modo', q: .5, draw(t, X)}; aquí se arma el lienzo 2D,
// el fondo WebGL (uber-shader), las figuras con contraluz y el post (grano, viñeta, interferencia).
const W = 1080, H = 1920
const cv = document.getElementById("c")
let X = cv.getContext("2d")
const R = (a, b, t) => Math.min(1, Math.max(0, (t - a) / (b - a)))       // rampa 0..1 entre a y b
const E = p => p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2  // easeInOutCubic
const EO = p => 1 - Math.pow(1 - p, 3)
const L = (a, b, p) => a + (b - a) * p
const D = Math.PI / 180
function hash(n) { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s) }
function ruido(x) { const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f); return L(hash(i), hash(i + 1), u) * 2 - 1 }

// ---------- fondo WebGL ----------
const GLSL = `precision highp float;
uniform vec2 uR; uniform float uT; uniform int uM;
uniform vec4 uA; uniform vec4 uB; uniform vec4 uC; uniform vec4 uD;
float h21(vec2 p){p=fract(p*vec2(123.34,456.21));p+=dot(p,p+45.32);return fract(p.x*p.y);}
float n2(vec2 p){vec2 i=floor(p),f=fract(p);vec2 u=f*f*(3.-2.*f);
 return mix(mix(h21(i),h21(i+vec2(1,0)),u.x),mix(h21(i+vec2(0,1)),h21(i+vec2(1,1)),u.x),u.y);}
float fbm(vec2 p){float v=0.,a=.5;mat2 m=mat2(1.6,1.2,-1.2,1.6);for(int i=0;i<6;i++){v+=a*n2(p);p=m*p;a*=.5;}return v;}
float fbm3(vec2 p){float v=0.,a=.5;mat2 m=mat2(1.6,1.2,-1.2,1.6);for(int i=0;i<3;i++){v+=a*n2(p);p=m*p;a*=.5;}return v;}
vec3 estrellas(vec2 p){vec3 c=vec3(0);for(int k=0;k<3;k++){float s=120.+float(k)*90.;vec2 g=p*s;vec2 i=floor(g),f=fract(g)-.5;
 float r=h21(i+float(k)*7.);if(r>.985){vec2 o=vec2(h21(i+3.),h21(i+5.))-.5;float d=length(f-o*.6);float tw=.6+.4*sin(uT*(1.+r*3.)+r*40.);
 c+=vec3(.8,.85,1.)*smoothstep(.16,0.,d)*tw*(.7+.9*fract(r*97.));}}
 float neb=fbm(p*2.3+vec2(0,uT*.01));c+=vec3(.10,.03,.06)*pow(neb,3.)*1.6;return c;}
// paleta de Júpiter por latitud con turbulencia
vec3 jupCol(vec2 q,float t){float y=q.y;
 float w=fbm(vec2(q.x*2.2+t*.03,y*9.))*.18;float b=y*7.+w*3.5+fbm(q*vec2(3.,14.)+t*.02)*.6;
 vec3 c1=vec3(.93,.80,.62),c2=vec3(.70,.42,.24),c3=vec3(.98,.92,.80),c4=vec3(.52,.28,.17);
 float s=sin(b*3.1)*.5+.5,s2=sin(b*1.3+1.)*.5+.5;vec3 c=mix(mix(c1,c2,s),mix(c3,c4,s),s2*.6);
 c*=.85+.3*fbm(q*vec2(6.,30.)+vec2(t*.05,0));return c;}
// mancha / ojo: centro m, radio rx, ry; abre = 0..1 (párpados), pup = 0..1
vec3 manchaOjo(vec2 q,vec3 base,vec2 m,vec2 rr,float abre,float pup,float t,out float k){
 vec2 d=(q-m)/rr;float r=length(d);float an=atan(d.y,d.x);
 // remolino
 float sw=an+.9/(r+.3)+t*.06*smoothstep(1.2,0.,r);vec2 sp=vec2(cos(sw),sin(sw))*r;
 float f=fbm(sp*3.+vec2(t*.02));vec3 rojo=mix(vec3(.62,.18,.08),vec3(.92,.45,.22),f);
 rojo=mix(rojo,vec3(.35,.07,.04),smoothstep(.2,.95,r)*.3);
 k=smoothstep(1.15,.85,r+ (f-.5)*.25);vec3 c=mix(base,rojo,k);
 if(abre>0.){
  // párpados: ojo almendrado dentro de la mancha
  float ax=d.x/.95,ay=d.y/(.62*abre+.001);float lid=1.-(ax*ax+ay*ay*(1.+ax*ax*1.6));
  float dentro=smoothstep(0.,.06,lid);
  vec2 g=d-uD.xy*.25;float rr2=length(g/vec2(1.,1.));float ir=.52;
  float fib=fbm(vec2(atan(g.y,g.x)*6.,rr2*14.)+t*.05);
  vec3 iris=mix(vec3(1.,.72,.18),vec3(.85,.25,.02),smoothstep(.0,ir,rr2));iris*=.6+.8*fib;
  iris+=vec3(1.,.85,.4)*smoothstep(.25,0.,rr2)*.6;
  float pw=mix(.05,.30,pup),ph=mix(.40,.46,pup);float pupila=smoothstep(1.05,.95,length(g/vec2(pw,ph)));
  pupila*=smoothstep(.06,.3,abre);
  vec3 esc=mix(vec3(.10,.02,.01),vec3(.35,.10,.04),smoothstep(.9,.2,length(d)));
  vec3 ojo=mix(esc,iris,smoothstep(ir+.03,ir-.02,rr2));ojo=mix(ojo,vec3(0),pupila);
  ojo*=.55+.45*smoothstep(0.,.35,lid);
  c=mix(c,ojo,dentro);
  c=mix(c,vec3(.05,.01,.0),smoothstep(.0,.05,lid)*smoothstep(.12,.02,lid)*.7);
 }
 return c;}
vec3 planeta(vec2 p,vec2 cen,float rad,float t,float abre,float pup,out float a){
 vec2 q=(p-cen)/rad;float r=length(q);a=smoothstep(1.,.995,r);if(a<=0.)return vec3(0);
 float z=sqrt(max(0.,1.-r*r));vec2 s=vec2(asin(clamp(q.x/max(sqrt(1.-q.y*q.y),.0001),-1.,1.))/1.5708,q.y);
 s.x+=t*.004;vec3 c=jupCol(s,t);float k;
 c=manchaOjo(s,c,vec2(.18+t*.004,.36),vec2(.20,.11),abre,pup,t,k);
 float luz=clamp(dot(normalize(vec3(q.x,-q.y,z)),normalize(vec3(-.55,.25,.8))),0.,1.);
 c*=pow(luz,.8)*1.15+.02;c=mix(c,c*vec3(.9,.6,.5),pow(1.-z,2.));
 return c;}
vec3 nubes(vec2 p,float t){ // dentro de la atmósfera: capas que suben (descenso)
 float y=p.y+uA.x;vec3 c=vec3(0);float prof=uA.y;
 for(int i=0;i<4;i++){float fi=float(i);float sc=1.4+fi*.9;
  vec2 q=vec2(p.x*sc+fi*3.1+t*.02*(fi+1.),y*sc*1.6+fi*1.7);
  float wq=fbm3(q*.7+t*.03);float f=fbm(q+vec2(wq*1.6,t*.04));
  vec3 col=mix(vec3(.55,.24,.10),vec3(.98,.70,.42),f)*mix(1.,.25,prof);col=mix(col,vec3(.30,.07,.05),fi*.15+prof*.4);
  float dens=smoothstep(.35,.75,f+.1*sin(fi+t*.1));c=mix(c,col*(.5+.6*f),dens*(.55+fi*.1));}
 // sombra colosal: uB = (x,y,largo,alto) ; uB.w>0
 if(uB.z>0.){vec2 d=(p-uB.xy)/uB.zw;float m=fbm3(p*2.+t*.05)*.35;float s=smoothstep(1.,.3,length(d)+m);
  c*=1.-s*.82;}
 // cristales de amoníaco
 vec2 g=p*vec2(40.,40.)+vec2(0,uA.x*40.);vec2 i=floor(g);float r=h21(i);
 if(r>.992){vec2 f=fract(g)-.5;float tw=pow(.5+.5*sin(t*3.+r*90.),6.);c+=vec3(.9,.95,1.)*smoothstep(.12,0.,length(f))*tw*uA.z;}
 return c;}
void main(){vec2 uv=gl_FragCoord.xy/uR;vec2 p=(gl_FragCoord.xy-.5*uR)/uR.y;p.y=-p.y;float t=uT;vec3 c=vec3(0);
 if(uM==0){c=estrellas(p*uA.z+uA.xy);}
 else if(uM==1){c=estrellas(p+uA.xy*.2);float a;vec3 pl=planeta(p,uA.xy,uA.z,t,uB.x,uB.y,a);
  // halo atmosférico
  float r=length((p-uA.xy)/uA.z);c+=vec3(.9,.5,.25)*smoothstep(1.25,1.,r)*smoothstep(.98,1.02,r)*.25;
  c=mix(c,pl,a);}
 else if(uM==2){c=nubes(p,t);}
 else if(uM==3){ // ojo de cerca dentro de la tormenta
  vec2 q=p*uA.z+uA.xy;float a=atan(q.y,q.x),r=length(q);float sw=a+1.6/(r+.4)+t*.04;
  vec2 sp=vec2(cos(sw),sin(sw))*r;float f=fbm(sp*2.2+t*.03);vec3 base=mix(vec3(.45,.12,.05),vec3(.95,.55,.28),f);
  base*=.55+.6*fbm(sp*6.);float k;c=manchaOjo(q,base,vec2(0),vec2(.62,.62),uB.x,uB.y,t,k);c=mix(base,c,k);
  c*=1.-smoothstep(.4,1.4,length(p))*.55;}
 else if(uM==4){ // niebla roja
  float f=fbm(p*1.6+vec2(t*.05,-t*.02));float g=fbm(p*3.+vec2(-t*.04,t*.03)+f);
  c=mix(vec3(.10,.01,.01),vec3(.62,.10,.06),g)*(.5+.7*f);c+=vec3(.5,.08,.04)*smoothstep(.6,-.2,p.y)*.35;}
 else if(uM==5){ // cosmos: espirales que colapsan a un punto (uA.x = 0..1 colapso)
  float z=mix(1.,.02,uA.x);vec2 q=p/z;vec3 s=vec3(0);
  for(int i=0;i<7;i++){float fi=float(i);vec2 cg=vec2(h21(vec2(fi,1.))-.5,h21(vec2(fi,2.))-.5)*vec2(.55,.95)*(1.-uA.x*.5);
   vec2 d=(q-cg)*(3.+fi*.6);float r=length(d),a=atan(d.y,d.x);float arms=.5+.5*sin(a*2.-log(r+.001)*4.+t*.3+fi);
   s+=vec3(.95,.55,.45)*exp(-r*2.)*(.25+.75*arms)*1.1+vec3(1.,.9,.8)*exp(-r*14.)*1.2;}
  c=estrellas(q*.5)+s;float core=exp(-length(p)/(.004+uA.y*.3));c+=vec3(1.,.85,.6)*core*uA.y*2.;
  c*=1.-uA.w;}
 gl_FragColor=vec4(c,1.);}`

const G = {}
function glInit(q) {
  const c = document.createElement('canvas'); c.width = Math.round(W * q); c.height = Math.round(H * q)
  const gl = c.getContext('webgl', { preserveDrawingBuffer: true, antialias: false })
  c.addEventListener('webglcontextlost', () => { window.__perdido = true })
  const sh = (ty, src) => { const s = gl.createShader(ty); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s)); return s }
  const pr = gl.createProgram()
  gl.attachShader(pr, sh(gl.VERTEX_SHADER, 'attribute vec2 a;void main(){gl_Position=vec4(a,0,1);}'))
  gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, GLSL)); gl.linkProgram(pr); gl.useProgram(pr)
  const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b)
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW)
  const loc = gl.getAttribLocation(pr, 'a'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0)
  const u = {}; for (const n of ['uR', 'uT', 'uM', 'uA', 'uB', 'uC', 'uD']) u[n] = gl.getUniformLocation(pr, n)
  Object.assign(G, { c, gl, u })
}
const MODOS = { estrellas: 0, planeta: 1, nubes: 2, ojo: 3, niebla: 4, cosmos: 5 }
// pinta el fondo y devuelve el canvas (para drawImage, también como textura dentro de siluetas)
function fondo(modo, t, o = {}) {
  const { gl, u, c } = G
  if (window.__perdido || gl.isContextLost()) throw new Error('contexto WebGL perdido')
  gl.viewport(0, 0, c.width, c.height)
  gl.uniform2f(u.uR, c.width, c.height); gl.uniform1f(u.uT, t); gl.uniform1i(u.uM, MODOS[modo])
  for (const k of ['A', 'B', 'C', 'D']) gl.uniform4fv(u['u' + k], o[k] || [0, 0, 1, 0])
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4)
  return c
}
function pintaFondo(modo, t, o, cam) {
  const c = fondo(modo, t, o)
  X.save(); camara(cam); X.drawImage(c, 0, 0, W, H); X.restore()
}
// cámara: {s: escala, x, y} alrededor del centro
function camara(k) {
  if (!k) return
  const s = k.s || 1
  X.translate(W / 2 + (k.x || 0), H / 2 + (k.y || 0)); X.rotate((k.r || 0) * D); X.scale(s, s); X.translate(-W / 2, -H / 2)
}

// ---------- figuras ----------
// pose: ángulos en grados. t torso (+ adelante), h cabeza, bi/bd brazo izq/der (0 = colgando, + adelante),
// ci/cd codo (+ dobla hacia adelante), pi/pd muslo, ri/rd rodilla (+ dobla hacia atrás)
const POSES = {
  pie: { t: 0, h: 0, bi: -6, ci: 10, bd: 8, cd: 12, pi: 2, ri: 2, pd: -3, rd: 3 },
  firme: { t: 0, h: 0, bi: -3, ci: 4, bd: 3, cd: 4, pi: 2, ri: 0, pd: -2, rd: 0 },
  habla: { t: 6, h: 8, bi: 10, ci: 80, bd: 22, cd: 150, pi: 3, ri: 4, pd: -4, rd: 5 },
  mira: { t: -4, h: -12, bi: -8, ci: 14, bd: 6, cd: 18, pi: 3, ri: 3, pd: -3, rd: 3 },
  consola: { t: 22, h: 10, bi: 50, ci: 40, bd: 62, cd: 30, pi: 6, ri: 6, pd: -4, rd: 8 },
  sentado: { t: -6, h: 6, bi: 40, ci: 50, bd: 55, cd: 40, pi: 88, ri: 85, pd: 84, rd: 80 },
  vidrio: { t: 10, h: -8, bi: 20, ci: 30, bd: 95, cd: 15, pi: 4, ri: 5, pd: -6, rd: 6 },
  arranca: { t: -10, h: -25, bi: 150, ci: 40, bd: 140, cd: 55, pi: 8, ri: 10, pd: -10, rd: 12 },
  grita: { t: -18, h: -35, bi: 130, ci: 30, bd: -40, cd: 20, pi: 12, ri: 10, pd: -14, rd: 14 },
  rodillas: { t: 6, h: 14, bi: 14, ci: 30, bd: 22, cd: 40, pi: 4, ri: 92, pd: 8, rd: 96 },
  llora: { t: 14, h: 34, bi: 48, ci: 140, bd: 56, cd: 145, pi: 4, ri: 94, pd: 8, rd: 98 },
  penitencia: { t: 10, h: 42, bi: 40, ci: 100, bd: 46, cd: 104, pi: 4, ri: 94, pd: 8, rd: 98 },
  corre: { t: 18, h: 4, bi: -40, ci: 70, bd: 50, cd: 70, pi: 40, ri: 70, pd: -30, rd: 30 },
  jala: { t: -14, h: 0, bi: 70, ci: 10, bd: 60, cd: 20, pi: 20, ri: 12, pd: -25, rd: 18 },
  cabizbajo: { t: 14, h: 40, bi: 25, ci: 95, bd: 30, cd: 100, pi: 3, ri: 4, pd: -3, rd: 4 },
  flota: { t: 4, h: -6, bi: 35, ci: 30, bd: 20, cd: 40, pi: 12, ri: 30, pd: -8, rd: 45 },
  manos: { t: 4, h: -4, bi: 75, ci: 75, bd: 70, cd: 70, pi: 2, ri: 2, pd: -3, rd: 3 },
}
function mezcla(a, b, p) { const o = {}; for (const k in a) o[k] = L(a[k], b[k] ?? a[k], p); return o }
// secuencia de poses: [[t, 'pose' | {…}], …] con transición de dur s
function seq(keys, t, dur = .45) {
  const pz = k => typeof k === 'string' ? POSES[k] : { ...POSES.pie, ...k }
  let p = pz(keys[0][1])
  for (let i = 1; i < keys.length; i++) {
    const [ti, k] = keys[i]; if (t < ti) break
    p = mezcla(p, pz(k), E(R(ti, ti + (keys[i][2] || dur), t)))
  }
  return p
}
function caminar(t, vel = 1, amp = 1) {
  const f = t * 2.2 * vel * Math.PI, s = Math.sin(f), c = Math.cos(f)
  return { t: 6, h: 2, bi: -26 * s * amp, ci: 18, bd: 26 * s * amp, cd: 18, pi: 26 * s * amp, ri: Math.max(0, -c) * 40 * amp + 4, pd: -26 * s * amp, rd: Math.max(0, c) * 40 * amp + 4, bob: Math.abs(c) * 8 * amp }
}
// tipos de cuerpo (px a escala 1)
const CUERPOS = {
  astro: { tor: 150, ancho: 112, cuello: 18, cab: 60, brazo: [86, 80], gb: [40, 36], pie: [102, 98], gp: [50, 44], mano: 22, mochila: true, casco: true },
  persona: { tor: 150, ancho: 70, cuello: 26, cab: 36, brazo: [82, 78], gb: [24, 20], pie: [104, 100], gp: [30, 26], mano: 13, pelo: 0 },
  mujer: { tor: 142, ancho: 62, cuello: 26, cab: 34, brazo: [80, 76], gb: [20, 17], pie: [102, 98], gp: [26, 22], mano: 12, pelo: 1, falda: 1 },
  nina: { tor: 95, ancho: 50, cuello: 16, cab: 30, brazo: [56, 52], gb: [16, 14], pie: [70, 66], gp: [20, 18], mano: 10, pelo: 2, falda: 1 },
}
// devuelve los puntos del esqueleto
function esqueleto(f) {
  const C = CUERPOS[f.tipo || 'astro'], s = f.s || 1, dir = f.dir || 1, p = f.pose
  const v = (a, l) => [Math.sin(a * D) * dir * l * s, Math.cos(a * D) * l * s]
  const cad = [f.x, f.y - (p.bob || 0) * s]
  const hip = cad
  const [tx, ty] = v(p.t, C.tor), cuello = [hip[0] + tx, hip[1] - ty]
  const hombro = [L(hip[0], cuello[0], .86), L(hip[1], cuello[1], .86)]
  const ha = p.t + p.h, [hx, hy] = v(ha, C.cuello + C.cab * .9), cab = [cuello[0] + hx, cuello[1] - hy]
  const ext = (o, a1, c1, l) => { const [x1, y1] = v(a1, l[0]), m = [o[0] + x1, o[1] + y1], [x2, y2] = v(a1 + c1, l[1]); return [m, [m[0] + x2, m[1] + y2]] }
  const [codI, manI] = ext(hombro, p.bi + p.t * .3, p.ci, C.brazo), [codD, manD] = ext(hombro, p.bd + p.t * .3, p.cd, C.brazo)
  const [rodI, pieI] = ext(hip, p.pi, -p.ri, C.pie), [rodD, pieD] = ext(hip, p.pd, -p.rd, C.pie)
  return { C, s, dir, hip, cuello, hombro, cab, codI, manI, codD, manD, rodI, pieI, rodD, pieD, ha }
}
function capsula(a, b, w) { X.lineWidth = w; X.beginPath(); X.moveTo(a[0], a[1]); X.lineTo(b[0], b[1]); X.stroke() }
function circ(p, r) { X.beginPath(); X.arc(p[0], p[1], r, 0, 7); X.fill() }
// trazo de toda la figura en el color actual; lados: 'atras' | 'frente' | 'todo'
function cuerpo(k, f, lado = 'todo') {
  const { C, s, dir } = k
  X.lineCap = 'round'; X.lineJoin = 'round'
  const brazoI = () => { capsula(k.hombro, k.codI, C.gb[0] * s); capsula(k.codI, k.manI, C.gb[1] * s); circ(k.manI, C.mano * s) }
  const brazoD = () => { capsula(k.hombro, k.codD, C.gb[0] * s); capsula(k.codD, k.manD, C.gb[1] * s); circ(k.manD, C.mano * s) }
  const pierna = (r, p) => { capsula(k.hip, r, C.gp[0] * s); capsula(r, p, C.gp[1] * s); X.save(); X.translate(p[0], p[1]); X.scale(dir, 1); X.beginPath(); X.ellipse(10 * s, 4 * s, C.gp[1] * .75 * s, C.gp[1] * .4 * s, 0, 0, 7); X.fill(); X.restore() }
  if (lado !== 'frente') { brazoI(); pierna(k.rodI, k.pieI) }
  if (lado === 'atras') return
  // torso
  capsula(k.hip, k.cuello, C.ancho * s)
  if (C.falda) { X.beginPath(); const h = k.hip, w = C.ancho * s; X.moveTo(h[0] - w * .45, h[1] - 30 * s); X.lineTo(h[0] + w * .45, h[1] - 30 * s); X.lineTo(h[0] + w * 1.0, h[1] + 70 * s); X.lineTo(h[0] - w * 1.0, h[1] + 70 * s); X.fill() }
  if (C.mochila) {
    X.save(); X.translate(L(k.hip[0], k.cuello[0], .55), L(k.hip[1], k.cuello[1], .55)); X.rotate(Math.atan2(k.cuello[0] - k.hip[0], k.hip[1] - k.cuello[1]))
    X.beginPath(); X.roundRect((-dir * 70 - 40) * s, -80 * s, 80 * s, 150 * s, 18 * s); X.fill(); X.restore()
  }
  pierna(k.rodD, k.pieD)
  capsula(k.cuello, k.cab, C.cuello * 1.6 * s)
  if (C.casco && !f.sinCasco) {
    circ(k.cab, C.cab * s)
    X.save(); X.translate(k.cab[0], k.cab[1]); X.rotate(k.ha * D * dir); X.beginPath(); X.ellipse(dir * 34 * s, 8 * s, 34 * s, 40 * s, 0, 0, 7); X.fill(); X.restore()
  } else {
    // cabeza de perfil: cráneo + nariz + mentón
    const r = (C.casco ? 38 : C.cab) * s
    X.save(); X.translate(k.cab[0], k.cab[1]); X.rotate(k.ha * D * dir); X.scale(dir, 1)
    X.beginPath(); X.ellipse(0, 0, r * .92, r, 0, 0, 7); X.fill()
    X.beginPath(); X.moveTo(r * .7, -r * .2); X.lineTo(r * 1.12, r * .22); X.lineTo(r * .78, r * .35); X.quadraticCurveTo(r * .9, r * .8, r * .3, r * 1.05); X.lineTo(-r * .2, r * .6); X.fill()
    const pelo = C.pelo
    if (pelo === 1) { X.beginPath(); X.moveTo(r * .3, -r * 1.0); X.quadraticCurveTo(-r * 1.6, -r * 1.1, -r * 1.3, r * 2.4); X.lineTo(-r * .2, r * 2.0); X.quadraticCurveTo(-r * .5, 0, r * .4, -r * .7); X.fill() }
    if (pelo === 2) { X.beginPath(); X.ellipse(-r * 1.0, r * .2, r * .35, r * .9, .3, 0, 7); X.fill() }
    if (f.coleta) { X.beginPath(); X.ellipse(-r * 1.05, r * .1, r * .3, r * .8, .5 + Math.sin(f.coleta) * .1, 0, 7); X.fill() }
    X.restore()
    if (C.casco) { // astronauta sin casco: cuello del traje
      X.beginPath(); X.ellipse(k.cuello[0], k.cuello[1] - 4 * s, 42 * s, 18 * s, 0, 0, 7); X.fill()
    }
  }
  if (lado === 'todo') brazoD()
  if (lado === 'frente') brazoD()
}
// figura con contraluz: borde de luz en el lado de `luz` (vector) y glow
function apoya(f) {
  if (f.suelo == null) return f
  const k = esqueleto({ ...f, y: 0 }), g = k.C.gp[1] * k.s * .5
  f.y = f.suelo - Math.max(k.pieI[1], k.pieD[1], k.rodI[1], k.rodD[1]) - g
  return f
}
function figura(f) {
  apoya(f)
  const k = esqueleto(f), luz = f.luz || [1, -.3], borde = f.borde ?? 4, col = f.rim || 'rgba(255,170,90,.95)'
  X.save()
  if (f.alfa != null) X.globalAlpha = f.alfa
  if (borde > 0) {
    X.save(); X.translate(luz[0] * borde, luz[1] * borde)
    X.shadowColor = col; X.shadowBlur = (f.glow ?? 18)
    X.fillStyle = X.strokeStyle = col; cuerpo(k, f); X.restore()
  }
  X.fillStyle = X.strokeStyle = f.color || '#050304'; cuerpo(k, f)
  if (k.C.casco && !f.sinCasco && f.visor !== false) visor(k, f)
  X.restore()
  return k
}
// reflejo del visor (franja) y gancho para pintar dentro (f.enVisor(ctx, k))
function visor(k, f) {
  const { s, dir } = k
  X.save(); X.translate(k.cab[0], k.cab[1]); X.rotate(k.ha * D * dir)
  X.beginPath(); X.ellipse(dir * 34 * s, 8 * s, 30 * s, 36 * s, 0, 0, 7); X.clip()
  const g = X.createLinearGradient(dir * 10 * s, -30 * s, dir * 60 * s, 40 * s)
  g.addColorStop(0, f.visorA || 'rgba(255,150,80,.0)'); g.addColorStop(.5, f.visorB || 'rgba(255,170,100,.22)'); g.addColorStop(1, 'rgba(0,0,0,0)')
  X.fillStyle = g; X.fillRect(-80 * s, -80 * s, 160 * s, 160 * s)
  if (f.enVisor) f.enVisor(X, s, dir)
  X.restore()
}
// silueta usada como máscara: pinta `img` (canvas) sólo dentro del cuerpo
function figuraRelleno(f, img, cam) {
  apoya(f)
  const k = esqueleto(f)
  const m = maskCanvas(); const mx = m.getContext('2d')
  mx.setTransform(1, 0, 0, 1, 0, 0); mx.clearRect(0, 0, W, H)
  const prev = X; Xswap(mx); mx.fillStyle = mx.strokeStyle = '#fff'; cuerpo(k, f); Xswap(prev)
  mx.globalCompositeOperation = 'source-in'; mx.save(); if (cam) { const c0 = X; Xswap(mx); camara(cam); Xswap(c0) } mx.drawImage(img, 0, 0, W, H); mx.restore(); mx.globalCompositeOperation = 'source-over'
  X.save(); if (f.alfa != null) X.globalAlpha = f.alfa; X.drawImage(m, 0, 0); X.restore()
  return k
}
let _mask
function maskCanvas() { if (!_mask) { _mask = document.createElement('canvas'); _mask.width = W; _mask.height = H } return _mask }
// permite reutilizar cuerpo() en otro contexto
let Xreal = X
function Xswap(c) { X = c }

// ---------- props (siluetas) ----------
function rect(x, y, w, h, r = 0) { X.beginPath(); X.roundRect(x, y, w, h, r); X.fill() }
function texto(t, x, y, px, col, o = {}) {
  X.save(); X.font = `${o.peso || 400} ${px}px ${o.fam || '"Share Tech Mono"'}`; X.fillStyle = col; X.textAlign = o.al || 'center'; X.textBaseline = 'middle'
  if (o.esp) X.letterSpacing = o.esp + 'px'
  if (o.glow) { X.shadowColor = col; X.shadowBlur = o.glow }
  X.fillText(t, x, y); X.restore()
}
// módulo Kraken-1: cápsula alargada con aletas y patas (tentáculos)
function kraken(x, y, s, ang = 0, o = {}) {
  X.save(); X.translate(x, y); X.rotate(ang * D); X.scale(s, s)
  const c = o.color || '#060405'
  const forma = () => {
    X.beginPath(); X.moveTo(0, -210); X.bezierCurveTo(70, -200, 95, -110, 95, -10); X.lineTo(110, 90); X.lineTo(-110, 90); X.lineTo(-95, -10); X.bezierCurveTo(-95, -110, -70, -200, 0, -210); X.fill()
    rect(-60, 90, 120, 34, 6)
    X.lineWidth = 16; X.lineCap = 'round'
    for (const sx of [-1, 1]) {
      X.beginPath(); X.moveTo(sx * 90, 60); X.quadraticCurveTo(sx * 170, 110, sx * 150 + Math.sin((o.t || 0) * 2 + sx) * 8, 210); X.stroke()
      X.beginPath(); X.moveTo(sx * 40, 110); X.quadraticCurveTo(sx * 70, 190, sx * 50 + Math.sin((o.t || 0) * 2.4 + sx) * 6, 260); X.stroke()
      X.beginPath(); X.moveTo(sx * 92, -30); X.lineTo(sx * 150, 20); X.lineTo(sx * 98, 40); X.fill()
    }
    X.lineWidth = 6; X.beginPath(); X.moveTo(0, -210); X.lineTo(0, -270); X.stroke(); circ([0, -274], 8)
  }
  X.save(); X.translate(o.luz ? o.luz[0] * 5 : 4, o.luz ? o.luz[1] * 5 : -2); X.fillStyle = X.strokeStyle = o.rim || 'rgba(255,170,90,.9)'; X.shadowColor = X.fillStyle; X.shadowBlur = 20; forma(); X.restore()
  X.fillStyle = X.strokeStyle = c; forma()
  // ventanillas encendidas
  const vl = o.ventanas ?? 1
  if (vl > 0) { X.fillStyle = `rgba(255,190,120,${.85 * vl})`; X.shadowColor = '#ffb070'; X.shadowBlur = 14; for (const yy of [-120, -70]) { X.beginPath(); X.ellipse(0, yy, 18, 14, 0, 0, 7); X.fill() } X.shadowBlur = 0 }
  if (o.letrero) { X.save(); X.rotate(-Math.PI / 2); texto('KRAKEN-1', 10, 48, 30, 'rgba(255,190,140,.75)', { esp: 4 }); X.restore() }
  if (o.fuego) { // escudo térmico / propulsor
    const g = X.createRadialGradient(0, 130, 10, 0, 160, 160 * o.fuego); g.addColorStop(0, 'rgba(255,240,200,.95)'); g.addColorStop(.3, 'rgba(255,140,50,.7)'); g.addColorStop(1, 'rgba(255,60,10,0)')
    X.fillStyle = g; X.beginPath(); X.ellipse(0, 150, 150 * o.fuego, 120 + 90 * o.fuego, 0, 0, 7); X.fill()
  }
  if (o.plasma) {
    X.globalCompositeOperation = 'lighter'
    for (let i = 0; i < 14; i++) { const a = -Math.PI / 2 + (i / 13 - .5) * 2.4; const l = 160 + 120 * hash(i + Math.floor((o.t || 0) * 12)); X.strokeStyle = `rgba(255,${120 + i * 6},60,${.35 * o.plasma})`; X.lineWidth = 10; X.beginPath(); X.moveTo(Math.cos(a) * 100, -40 + Math.sin(a) * 140); X.lineTo(Math.cos(a) * (100 + l), -40 + Math.sin(a) * (140 + l)); X.stroke() }
    X.globalCompositeOperation = 'source-over'
  }
  X.restore()
}
// estación orbital: anillo + módulos + paneles
function estacion(x, y, s, giro, o = {}) {
  X.save(); X.translate(x, y); X.scale(s, s)
  const forma = () => {
    X.save(); X.scale(1, .32); X.lineWidth = 34; X.beginPath(); X.arc(0, 0, 300, 0, 7); X.stroke(); X.restore()
    for (let i = 0; i < 6; i++) { const a = giro + i * Math.PI / 3; X.lineWidth = 12; X.beginPath(); X.moveTo(0, 0); X.lineTo(Math.cos(a) * 300, Math.sin(a) * 96); X.stroke() }
    rect(-60, -170, 120, 340, 30)
    rect(-40, -260, 80, 100, 14)
    for (const sx of [-1, 1]) { rect(sx > 0 ? 330 : -560, -40, 230, 80, 4); X.lineWidth = 10; X.beginPath(); X.moveTo(sx * 300, 0); X.lineTo(sx * 340, 0); X.stroke() }
    X.lineWidth = 6; X.beginPath(); X.moveTo(0, -260); X.lineTo(0, -340); X.stroke()
  }
  X.save(); X.translate(-5, -4); X.fillStyle = X.strokeStyle = o.rim || 'rgba(255,190,130,.9)'; X.shadowColor = X.fillStyle; X.shadowBlur = 16; forma(); X.restore()
  X.fillStyle = X.strokeStyle = '#060405'; forma()
  // paneles con rejilla
  X.strokeStyle = 'rgba(255,170,110,.18)'; X.lineWidth = 3
  for (const sx of [330, -560]) for (let i = 1; i < 6; i++) { X.beginPath(); X.moveTo(sx + i * 38, -40); X.lineTo(sx + i * 38, 40); X.stroke() }
  X.fillStyle = 'rgba(255,200,140,.9)'; X.shadowColor = '#ffb070'; X.shadowBlur = 10
  for (let i = 0; i < 5; i++) { X.beginPath(); X.arc(0, -130 + i * 60, 7, 0, 7); X.fill() }
  if (hash(Math.floor((o.t || 0) * 1.5)) > .4) { X.fillStyle = '#ff4030'; X.shadowColor = '#ff4030'; X.beginPath(); X.arc(0, -342, 9, 0, 7); X.fill() }
  X.shadowBlur = 0
  if (o.letrero) { texto(o.letrero, 0, 230, 44, 'rgba(255,200,150,.8)', { esp: 10 }) }
  X.restore()
}
function sonda(x, y, s, t, o = {}) {
  X.save(); X.translate(x, y); X.scale(s, s); X.rotate(Math.sin(t * .8 + x) * .15)
  X.fillStyle = X.strokeStyle = '#060405'; X.lineWidth = 6
  X.beginPath(); X.moveTo(0, -40); X.lineTo(26, 0); X.lineTo(0, 40); X.lineTo(-26, 0); X.fill()
  X.beginPath(); X.moveTo(0, -40); X.lineTo(0, -80); X.stroke(); X.beginPath(); X.moveTo(-26, 0); X.lineTo(-60, -20); X.moveTo(26, 0); X.lineTo(60, -20); X.stroke()
  const on = (t * 1.3 + (o.fase || 0)) % 1 < .18
  if (on) { X.fillStyle = '#ff3a2a'; X.shadowColor = '#ff3a2a'; X.shadowBlur = 24; X.beginPath(); X.arc(0, -84, 8, 0, 7); X.fill() }
  X.restore()
}
// ciudad para escala
function ciudad(y0, s, alfa = 1, sem = 3) {
  X.save(); X.globalAlpha = alfa
  let x = -40, i = 0
  while (x < W + 40) {
    const w = (50 + hash(i * 3 + sem) * 90) * s, h = (120 + hash(i * 7 + sem) * 420 * (1 - Math.abs(x - W / 2) / W)) * s
    X.fillStyle = '#060304'; X.fillRect(x, y0 - h, w + 1, h + 400)
    if (hash(i + sem) > .7) { X.fillRect(x + w / 2 - 3, y0 - h - 60 * s, 6, 60 * s) }
    X.fillStyle = 'rgba(255,180,100,.35)'
    for (let yy = y0 - h + 20 * s; yy < y0 - 10; yy += 26 * s) for (let xx = x + 10 * s; xx < x + w - 10 * s; xx += 20 * s) if (hash(xx * .37 + yy * 1.3) > .78) X.fillRect(xx, yy, 6 * s, 9 * s)
    x += w + 6 * s; i++
  }
  X.restore()
}

// ---------- post ----------
const GR = []
function granoInit() {
  for (let n = 0; n < 8; n++) {
    const c = document.createElement('canvas'); c.width = 540; c.height = 960; const x = c.getContext('2d'), d = x.createImageData(540, 960)
    let s = 9301 + n * 49297
    for (let i = 0; i < d.data.length; i += 4) { s = (s * 1103515245 + 12345) & 0x7fffffff; const v = (s >> 16) & 255; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 255 }
    x.putImageData(d, 0, 0); GR.push(c)
  }
}
let _tmp
function tmpCanvas() { if (!_tmp) { _tmp = document.createElement('canvas'); _tmp.width = W; _tmp.height = H } return _tmp }
// interferencia: fuerza 0..1 (desplaza franjas, separa canales, nieve)
function interferencia(t, k) {
  if (k <= 0) return
  const tc = tmpCanvas(), tx = tc.getContext('2d'); tx.clearRect(0, 0, W, H); tx.drawImage(cv, 0, 0)
  const fr = Math.floor(t * 30)
  for (let i = 0; i < 22 * k; i++) {
    const y = hash(fr * 13 + i) * H, h = 8 + hash(fr * 7 + i * 3) * 120 * k, dx = (hash(fr + i * 11) - .5) * 260 * k
    X.drawImage(tc, 0, y, W, h, dx, y, W, h)
  }
  X.save(); X.globalCompositeOperation = 'lighter'; X.globalAlpha = .35 * k; X.drawImage(tc, 10 * k, 0); X.restore()
  X.save(); X.globalAlpha = Math.min(.62, k * .62); X.globalCompositeOperation = 'source-over'; X.imageSmoothingEnabled = false
  X.drawImage(GR[fr % GR.length], 0, 0, W, H); X.restore()
}
function post(t, o = {}) {
  const fr = Math.floor(t * 30)
  // viñeta
  const g = X.createRadialGradient(W / 2, H / 2, H * .25, W / 2, H / 2, H * .72); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, `rgba(0,0,0,${o.vig ?? .78})`)
  X.fillStyle = g; X.fillRect(0, 0, W, H)
  // parpadeo de luz
  const fl = o.parpadeo ? Math.max(0, ruido(t * 9) * o.parpadeo) : 0
  if (fl > 0) { X.fillStyle = `rgba(0,0,0,${fl})`; X.fillRect(0, 0, W, H) }
  // grano
  X.save(); X.globalCompositeOperation = 'overlay'; X.globalAlpha = o.grano ?? .16; X.drawImage(GR[fr % GR.length], 0, 0, W, H); X.restore()
  // líneas de barrido tenues
  if (o.lineas) { X.fillStyle = `rgba(0,0,0,${o.lineas})`; for (let y = (fr * 3) % 6; y < H; y += 6) X.fillRect(0, y, W, 2) }
  interferencia(t, o.ruido || 0)
  if (o.negro) { X.fillStyle = `rgba(0,0,0,${o.negro})`; X.fillRect(0, 0, W, H) }
}
// estallido de interferencia en los cortes: devuelve 0..1
function corte(t, t0, d = .22) { const p = (t - t0) / d; return p >= 0 && p < 1 ? (1 - p) * .9 : 0 }

// ---------- arranque ----------
const _F = ['40px "Share Tech Mono"']
window.__listo = Promise.all(_F.map(f => document.fonts.load(f))).then(() => document.fonts.ready).then(() => {
  const m = _F.filter(f => !document.fonts.check(f)); if (m.length) throw new Error('faltan fuentes: ' + m)
  granoInit(); glInit(window.ESC.q || .5); window.__seek(0)
})
window.__seek = s => {
  if (!G.gl) return
  X = Xreal; X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = 1; X.globalCompositeOperation = 'source-over'; X.fillStyle = '#000'; X.fillRect(0, 0, W, H)
  window.ESC.draw(s)
}

// ---------- escenarios ----------
// interior de la nave: muro, paneles, ventanilla redonda (vista = canvas o null), alarma roja, consola
function cabina(t, o = {}) {
  const g = X.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#120809'); g.addColorStop(.6, '#0b0506'); g.addColorStop(1, '#050203')
  X.fillStyle = g; X.fillRect(-200, -200, W + 400, H + 400)
  X.strokeStyle = 'rgba(255,140,100,.07)'; X.lineWidth = 4
  for (const [x, y, w, h] of [[-40, 120, 520, 700], [520, 120, 600, 420], [520, 580, 600, 520], [-40, 860, 520, 600], [-40, 1500, 1160, 500]]) { X.beginPath(); X.roundRect(x, y, w, h, 24); X.stroke() }
  X.fillStyle = 'rgba(255,140,100,.08)'
  for (let i = 0; i < 18; i++) { X.beginPath(); X.arc(20 + (i % 9) * 130, i < 9 ? 140 : 1480, 5, 0, 7); X.fill() }
  if (o.ojo) {
    const [x, y, r] = o.ojo
    X.save(); X.beginPath(); X.arc(x, y, r, 0, 7); X.clip()
    if (o.vista) X.drawImage(o.vista, x - r * 1.9, y - r * 1.9 * H / W * .5, r * 3.8, r * 3.8 * H / W * .5)
    else { X.fillStyle = '#000'; X.fill() }
    const v = X.createRadialGradient(x, y, r * .5, x, y, r); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,.7)'); X.fillStyle = v; X.fillRect(x - r, y - r, r * 2, r * 2)
    X.restore()
    X.strokeStyle = '#1a0d0d'; X.lineWidth = r * .16; X.beginPath(); X.arc(x, y, r * 1.06, 0, 7); X.stroke()
    X.strokeStyle = 'rgba(255,160,110,.18)'; X.lineWidth = 3; X.beginPath(); X.arc(x, y, r * .99, 0, 7); X.stroke()
    X.fillStyle = 'rgba(255,150,100,.15)'; for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2; X.beginPath(); X.arc(x + Math.cos(a) * r * 1.06, y + Math.sin(a) * r * 1.06, 6, 0, 7); X.fill() }
  }
  if (o.consola !== false) {
    const cy = o.consolaY || 1560
    X.fillStyle = '#0a0506'; X.fillRect(-200, cy, W + 400, 600)
    X.fillStyle = 'rgba(255,140,90,.14)'; X.fillRect(-200, cy, W + 400, 4)
    for (let i = 0; i < 6; i++) {
      const x = 40 + i * 175, on = .5 + .5 * Math.sin(t * 2 + i * 1.7)
      X.fillStyle = `rgba(255,${120 + i * 15},70,${.10 + on * .12})`; X.fillRect(x, cy + 40, 130, 70)
      X.fillStyle = `rgba(255,90,60,${hash(Math.floor(t * 3) + i) > .5 ? .8 : .15})`; X.beginPath(); X.arc(x + 20, cy + 150, 8, 0, 7); X.fill()
    }
  }
  if (o.alarma) {
    const p = .5 + .5 * Math.sin(t * 5.2), a = o.alarma * p
    const r = X.createRadialGradient(o.alarmaX ?? 160, -60, 40, o.alarmaX ?? 160, -60, 1500); r.addColorStop(0, `rgba(255,40,30,${.55 * a})`); r.addColorStop(1, 'rgba(255,0,0,0)')
    X.fillStyle = r; X.fillRect(-200, -200, W + 400, H + 400)
  }
}
// pantalla de la nave con contenido (fn dibuja en coordenadas locales w×h)
function pantalla(x, y, w, h, t, fn, o = {}) {
  X.save(); X.translate(x, y)
  X.fillStyle = '#0d0707'; X.beginPath(); X.roundRect(-18, -18, w + 36, h + 36, 18); X.fill()
  X.beginPath(); X.rect(0, 0, w, h); X.clip(); X.fillStyle = '#020101'; X.fillRect(0, 0, w, h)
  fn(w, h)
  X.fillStyle = 'rgba(0,0,0,.25)'; for (let yy = 0; yy < h; yy += 5) X.fillRect(0, yy, w, 2)
  const g = X.createRadialGradient(w / 2, h / 2, 10, w / 2, h / 2, Math.max(w, h) * .7); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(0,0,0,.55)'); X.fillStyle = g; X.fillRect(0, 0, w, h)
  X.restore()
  if (o.brillo) { // la pantalla ilumina el cuarto
    const g2 = X.createRadialGradient(x + w / 2, y + h / 2, 50, x + w / 2, y + h / 2, 1200); g2.addColorStop(0, `rgba(255,140,60,${.22 * o.brillo})`); g2.addColorStop(1, 'rgba(255,100,40,0)')
    X.fillStyle = g2; X.fillRect(-200, -200, W + 400, H + 400)
  }
}
// ojo dibujado en 2D (para reflejos, pantallas pequeñas y destellos)
function ojo2d(x, y, r, abre, pup = .2, o = {}) {
  X.save(); X.translate(x, y)
  X.beginPath(); X.moveTo(-r, 0); X.quadraticCurveTo(0, -r * 1.1 * abre, r, 0); X.quadraticCurveTo(0, r * 1.1 * abre, -r, 0); X.closePath(); X.clip()
  const g = X.createRadialGradient(0, 0, 0, 0, 0, r * .6); g.addColorStop(0, o.c0 || '#ffd27a'); g.addColorStop(.6, o.c1 || '#e0560f'); g.addColorStop(1, o.c2 || '#5a1406')
  X.fillStyle = '#2a0805'; X.fillRect(-r, -r, r * 2, r * 2); X.fillStyle = g; X.beginPath(); X.arc(o.gx || 0, 0, r * .6, 0, 7); X.fill()
  X.fillStyle = '#000'; X.beginPath(); X.ellipse(o.gx || 0, 0, r * (.05 + .2 * pup), r * .5, 0, 0, 7); X.fill()
  X.restore()
}

// ---------- más piezas ----------
// glifo de un idioma desconocido (trazos deterministas por semilla)
function glifo(x, y, sz, seed, col, o = {}) {
  X.save(); X.translate(x, y); X.rotate((o.rot || 0)); X.strokeStyle = col; X.lineWidth = o.grosor || sz * .09; X.lineCap = 'round'
  if (o.glow) { X.shadowColor = col; X.shadowBlur = o.glow }
  const n = 2 + Math.floor(hash(seed) * 3)
  X.beginPath()
  for (let i = 0; i < n; i++) {
    const a = hash(seed * 3 + i), b = hash(seed * 5 + i * 7), c = hash(seed * 11 + i * 3)
    if (a < .35) { X.moveTo((b - .5) * sz, -sz * .5); X.quadraticCurveTo((c - .5) * sz * 1.4, 0, (b - .5) * sz * .6, sz * .5) }
    else if (a < .6) { X.moveTo(-sz * .45, (b - .5) * sz); X.lineTo(sz * .45, (c - .5) * sz) }
    else if (a < .8) { X.moveTo((b - .5) * sz * .6 + sz * .18, (c - .5) * sz * .6); X.arc((b - .5) * sz * .6, (c - .5) * sz * .6, sz * .18, 0, 6.3) }
    else { X.moveTo(0, -sz * .5); X.lineTo((b - .5) * sz, sz * .1); X.lineTo((c - .5) * sz, sz * .5) }
  }
  X.stroke(); X.restore()
}
// puntos del cuerpo (para disolver en partículas)
function puntosCuerpo(k, n, seed = 1) {
  const seg = [[k.hip, k.cuello, k.C.ancho], [k.cuello, k.cab, k.C.cab * 1.6], [k.hombro, k.codI, k.C.gb[0]], [k.codI, k.manI, k.C.gb[1]], [k.hombro, k.codD, k.C.gb[0]], [k.codD, k.manD, k.C.gb[1]],
    [k.hip, k.rodI, k.C.gp[0]], [k.rodI, k.pieI, k.C.gp[1]], [k.hip, k.rodD, k.C.gp[0]], [k.rodD, k.pieD, k.C.gp[1]]]
  const out = []
  for (let i = 0; i < n; i++) {
    const sg = seg[Math.floor(hash(seed + i * 1.3) * seg.length)], u = hash(seed + i * 2.7), v = hash(seed + i * 4.1) - .5
    const [a, b, w] = sg, dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1
    out.push([a[0] + dx * u - dy / l * v * w * k.s, a[1] + dy * u + dx / l * v * w * k.s, hash(seed + i * 9.1)])
  }
  return out
}
// figura que se disuelve hacia arriba: p 0..1
function disuelve(f, p, o = {}) {
  apoya(f); const k = esqueleto(f)
  if (p < 1) {
    X.save(); X.globalAlpha = 1 - E(Math.min(1, p * 1.4)); figura(f); X.restore()
  }
  if (p > 0) {
    const pts = puntosCuerpo(k, o.n || 420, o.seed || 3)
    X.save()
    for (const [x, y, r] of pts) {
      const q = Math.max(0, Math.min(1, (p - r * .5) * 2))
      if (q <= 0 || q >= 1) { if (q <= 0 && p < .5) continue; if (q >= 1) continue }
      const dy = -E(q) * (300 + r * 500), dx = ruido(r * 50 + q * 3) * 120 * q
      X.fillStyle = `rgba(${o.col || '255,120,90'},${(1 - q) * .9})`; const z = 3 + r * 6
      X.fillRect(x + dx, y + dy, z, z)
    }
    X.restore()
  }
}
// hipercubo (forma imposible) girando
function tesseract(x, y, sz, t, col) {
  const V = []; for (let i = 0; i < 16; i++) V.push([(i & 1) * 2 - 1, (i >> 1 & 1) * 2 - 1, (i >> 2 & 1) * 2 - 1, (i >> 3 & 1) * 2 - 1])
  const a = t * .7, b = t * .45, P = V.map(([px, py, pz, pw]) => {
    let x1 = px * Math.cos(a) - pw * Math.sin(a), w1 = px * Math.sin(a) + pw * Math.cos(a)
    let y1 = py * Math.cos(b) - pz * Math.sin(b), z1 = py * Math.sin(b) + pz * Math.cos(b)
    const k = 1 / (2.6 - w1), x2 = x1 * k, y2 = y1 * k, z2 = z1 * k
    const k2 = 1 / (3 - z2 * .8); return [x + x2 * k2 * sz * 3, y + y2 * k2 * sz * 3]
  })
  X.save(); X.strokeStyle = col; X.lineWidth = 3; X.shadowColor = col; X.shadowBlur = 14; X.beginPath()
  for (let i = 0; i < 16; i++) for (let j = 0; j < 4; j++) { const n = i ^ (1 << j); if (n > i) { X.moveTo(P[i][0], P[i][1]); X.lineTo(P[n][0], P[n][1]) } }
  X.stroke(); X.restore()
}
// luna helada (Europa)
function europa(x, y, r, t) {
  const g = X.createRadialGradient(x - r * .4, y - r * .4, r * .1, x, y, r); g.addColorStop(0, '#f2ead8'); g.addColorStop(.7, '#b9a58a'); g.addColorStop(1, '#3a2e26')
  X.fillStyle = g; X.beginPath(); X.arc(x, y, r, 0, 7); X.fill()
  X.save(); X.beginPath(); X.arc(x, y, r, 0, 7); X.clip(); X.strokeStyle = 'rgba(120,60,40,.45)'; X.lineWidth = r * .012
  for (let i = 0; i < 26; i++) { X.beginPath(); const a = hash(i) * 7, b = hash(i + 50) * 7; X.moveTo(x + Math.cos(a) * r * 1.2, y + Math.sin(a) * r * 1.2); X.quadraticCurveTo(x + (hash(i + 9) - .5) * r, y + (hash(i + 19) - .5) * r, x + Math.cos(b) * r * 1.2, y + Math.sin(b) * r * 1.2); X.stroke() }
  const s = X.createLinearGradient(x - r, y - r, x + r * .6, y + r * .6); s.addColorStop(0, 'rgba(0,0,0,0)'); s.addColorStop(.55, 'rgba(0,0,0,.2)'); s.addColorStop(1, 'rgba(0,0,0,.9)'); X.fillStyle = s; X.fillRect(x - r, y - r, r * 2, r * 2)
  X.restore()
}
// anillos de señal que se expanden desde (x,y)
function pings(x, y, t, o = {}) {
  const per = o.per || 1.2, n = o.n || 4, max = o.max || 600
  X.save(); X.lineWidth = o.grosor || 4
  for (let i = 0; i < n; i++) {
    const ph = ((t / per) + i / n) % 1, r = ph * max
    X.strokeStyle = `rgba(${o.col || '255,90,70'},${(1 - ph) * (o.alfa ?? .8)})`; X.beginPath()
    if (o.arco) X.arc(x, y, r, o.arco[0], o.arco[1]); else X.arc(x, y, r, 0, 7)
    X.stroke()
  }
  X.restore()
}
// guante grande (mano en primer plano) desde el borde: b = base del brazo, p = centro de la palma
function formaGuante(b, p, s, o) {
  const a = Math.atan2(p[1] - b[1], p[0] - b[0]), ux = Math.cos(a), uy = Math.sin(a), vx = -uy, vy = ux
  const P = (u, v) => [p[0] + ux * u * s + vx * v * s, p[1] + uy * u * s + vy * v * s]
  capsula(b, P(-40, 0), 118 * s)
  X.beginPath(); X.ellipse(p[0], p[1], 92 * s, 82 * s, a, 0, 7); X.fill()
  const ab = o.abierta ?? 0, dedos = [[-48, 92, -.16], [-16, 108, -.05], [16, 104, .05], [46, 84, .15]]
  dedos.forEach(([v, l, ang], i) => {
    const curl = o.senala && i !== 1 ? .45 : 1, sp = ang * (1 + ab * 1.6)
    const r0 = P(70, v), dx = Math.cos(a + sp), dy = Math.sin(a + sp)
    capsula(r0, [r0[0] + dx * l * curl * s, r0[1] + dy * l * curl * s], 34 * s)
  })
  const ta = a - (.9 + ab * .4) * (o.dir || 1), t0 = P(10, -70 * (o.dir || 1))
  capsula(t0, [t0[0] + Math.cos(ta) * 82 * s, t0[1] + Math.sin(ta) * 82 * s], 38 * s)
}
function guante(b, p, s = 1, o = {}) {
  X.save(); X.lineCap = 'round'
  X.save(); X.translate(3, -4); X.fillStyle = X.strokeStyle = o.rim || 'rgba(255,150,80,.9)'; X.shadowColor = X.fillStyle; X.shadowBlur = 16; formaGuante(b, p, s, o); X.restore()
  X.fillStyle = X.strokeStyle = '#050304'; formaGuante(b, p, s, o)
  if (o.dentro) { // pinta algo sólo dentro del guante
    const m = maskCanvas(), mx = m.getContext('2d'); mx.setTransform(1, 0, 0, 1, 0, 0); mx.clearRect(0, 0, W, H)
    const prev = X; Xswap(mx); mx.lineCap = 'round'; mx.fillStyle = mx.strokeStyle = '#fff'; formaGuante(b, p, s, o); mx.globalCompositeOperation = 'source-atop'; o.dentro(); mx.globalCompositeOperation = 'source-over'; Xswap(prev)
    X.drawImage(m, 0, 0)
  }
  X.restore()
}
// leyenda tipo registro (nombre en pantalla)
function etiqueta(t, txt, x, y, t0, o = {}) {
  const n = Math.floor(Math.max(0, Math.min(txt.length, (t - t0) * 22)))
  if (n <= 0) return
  texto(txt.slice(0, n) + (Math.floor(t * 3) % 2 && n < txt.length ? '_' : ''), x, y, o.px || 40, o.col || 'rgba(255,215,190,.9)', { al: o.al || 'left', esp: 6, glow: 8 })
}
