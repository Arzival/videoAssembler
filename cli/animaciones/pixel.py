"""Estilo «Pixel 16-bit»: escenas de videojuego retro dibujadas en una rejilla de píxeles reales.

Cada página es un <canvas> de 270×480 escalado ×4 (image-rendering: pixelated) a 1080×1920: un píxel del juego = 4 px del video.
Todo se dibuja con una función `draw(t)` determinista (t = segundos locales de la página), a 12 cps (__cps=12), sin WAAPI.
Paleta limitada tipo SNES (PAL), texto Press Start 2P umbralizado (sin antialias, a múltiplos de 8 px), sprites en arte de
caracteres (SPR) y ayudantes de juego: cajas de diálogo RPG, HUD, barras, monedas, menús con cursor, servidores, edificios.
Transición entre páginas: mosaico del SNES (los bloques crecen al salir y se encogen al entrar), nada de fundidos.

Uso desde un guion:
    import pixel as X
    html = X.page(draw_js, dur, mosaico=(True, True))        # escena opaca
    html = X.subtitulos(grupos, dur, ocultar=[[a, b]])       # capa transparente con caja de diálogo
draw_js es el cuerpo de una función JS `(t)=>{...}` que usa los ayudantes de RUNTIME (ver la lista abajo).
"""
import json

W, H, ESCALA, CPS = 270, 480, 4, 12
FUENTE = 'Press Start 2P'

PAL = {
    'k': '#0d0b1a', 'n': '#1b1f4b', 'N': '#262c6b', 'b': '#2e4fa8', 'c': '#4fa4e8', 'C': '#a6e3ff', 'w': '#f4f1e6',
    's': '#b8bccc', 'g': '#6b6f86', 'G': '#3c3f55', 'r': '#e23b3b', 'R': '#8a1c2b', 'o': '#f08a24', 'y': '#ffd23f',
    'Y': '#fff3a0', 'e': '#3cb44b', 'E': '#1f6e3a', 'l': '#9cf06a', 'p': '#8b4bd8', 'P': '#4a2a7a', 'm': '#f7a1c4',
    't': '#e8b48a', 'T': '#8f563b', 'q': '#d8cfae', 'Q': '#9d9474', 'u': '#5a3a22',
}

# Sprites en arte de caracteres: cada letra es un color de PAL, '.' = transparente.
SPR = {
    # corredor de bolsa (8×14) y su paso alterno
    'trader': ["..uuuu..", ".uttttu.", ".tkttkt.", ".tttttt.", "..tRRt..", "..nwwn..", ".nnrrnn.", "nnnrrnnn",
               "nnnrrnnn", "tnnnnnnt", ".nnnnnn.", ".nn..nn.", ".nn..nn.", ".kk..kk."],
    'trader2': ["..uuuu..", ".uttttu.", ".tkttkt.", ".tttttt.", "..tRRt..", "..nwwn..", ".nnrrnn.", "nnnrrnnn",
                "nnnrrnnn", "tnnnnnnt", ".nnnnnn.", "..nnnn..", ".nn..nn.", "kk....kk"],
    # programa viejo: computadora beige con cara (20×16), despierto y dormido
    'viejo': ["...QQQQQQQQQQQQQQ...", "..QqqqqqqqqqqqqqqQ..", "..QqkkkkkkkkkkkkqQ..", "..QqkrrkkkkkkrrkqQ..",
              "..QqkrrkkkkkkrrkqQ..", "..QqkkkkkkkkkkkkqQ..", "..QqkkwkwkwkwkkkqQ..", "..QqkkkkkkkkkkkkqQ..",
              "..QqqqqqqqqqqqqqqQ..", "..QqqqqqqqqgggqqqQ..", "...QQQQQQQQQQQQQQ...", ".QqqqqqqqqqqqqqqqqQ.",
              ".QqgggqqqqqqqqgggqQ.", ".QQQQQQQQQQQQQQQQQQ.", "..G..G..G..G..G..G..", ".G..G..G..G..G..G..."],
    'dormido': ["...QQQQQQQQQQQQQQ...", "..QqqqqqqqqqqqqqqQ..", "..QqkkkkkkkkkkkkqQ..", "..QqkkkkkkkkkkkkqQ..",
                "..QqkggkkkkkkggkqQ..", "..QqkkkkkkkkkkkkqQ..", "..QqkkkkggggkkkkqQ..", "..QqkkkkkkkkkkkkqQ..",
                "..QqqqqqqqqqqqqqqQ..", "..QqqqqqqqqgggqqqQ..", "...QQQQQQQQQQQQQQ...", ".QqqqqqqqqqqqqqqqqQ.",
                ".QqgggqqqqqqqqgggqQ.", ".QQQQQQQQQQQQQQQQQQ.", "....................", "...................."],
    # robot de despliegue automático (12×14)
    'robot': [".....yy.....", ".....kk.....", "..ssssssss..", ".sCCCCCCCCs.", ".sCkCCCCkCs.", ".sCCCCCCCCs.",
              ".sCCkkkkCCs.", "..ssssssss..", "...gssssg...", ".sgsssssgs..", "sg.ssssss.gs", "...ss..ss...",
              "...ss..ss...", "..kkk..kkk.."],
    # bote de basura (10×12)
    'basura': ["..gggggg..", "gggggggggg", "ssssssssss", ".sGsGsGsG.", ".sGsGsGsG.", ".sGsGsGsG.", ".sGsGsGsG.",
               ".sGsGsGsG.", ".sGsGsGsG.", ".sGsGsGsG.", "..ssssss..", "..........."],
    # corazón / vida (7×6)
    'vida': [".rr.rr.", "rrrrrrr", "rrrrrrr", ".rrrrr.", "..rrr..", "...r..."],
    # sol (9×9)
    'sol': ["....y....", ".y.yyy.y.", "..yyyyy..", ".yyYYYyy.", "yyyYYYyyy", ".yyYYYyy.", "..yyyyy..", ".y.yyy.y.", "....y...."],
}

RUNTIME = r"""
const W=%(W)d,H=%(H)d,CPS=%(CPS)d,FONT='%(FONT)s';
const cv=document.getElementById('c'),g=cv.getContext('2d');g.imageSmoothingEnabled=false;
const PAL=%(PAL)s,SPR=%(SPR)s;
const col=c=>PAL[c]||c;
const cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
const P=(t,a,b)=>cl((t-a)/(b-a));                         // progreso 0→1 entre a y b
const lerp=(a,b,x)=>a+(b-a)*x;
const E={o:x=>1-Math.pow(1-x,3),io:x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2,
  back:x=>{const c=1.9;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)},
  bote:x=>{const n=7.5625,d=2.75;if(x<1/d)return n*x*x;if(x<2/d)return n*(x-=1.5/d)*x+.75;if(x<2.5/d)return n*(x-=2.25/d)*x+.9375;return n*(x-=2.625/d)*x+.984375}};
const hs=n=>{const x=Math.sin(n*127.1+311.7)*43758.5453;return x-Math.floor(x)};   // azar determinista
const blink=(t,hz=2)=>Math.floor(t*hz*2)%%2===0;
// --- primitivas
function R(x,y,w,h,c){g.fillStyle=col(c);g.fillRect(Math.round(x),Math.round(y),Math.round(w),Math.round(h))}
function O(x,y,w,h,c,k=1){R(x,y,w,k,c);R(x,y+h-k,w,k,c);R(x,y,k,h,c);R(x+w-k,y,k,h,c)}
function L(x0,y0,x1,y1,c){x0=Math.round(x0);y0=Math.round(y0);x1=Math.round(x1);y1=Math.round(y1);
  const dx=Math.abs(x1-x0),dy=-Math.abs(y1-y0),sx=x0<x1?1:-1,sy=y0<y1?1:-1;let e=dx+dy;g.fillStyle=col(c);
  for(let i=0;i<999;i++){g.fillRect(x0,y0,1,1);if(x0===x1&&y0===y1)break;const e2=2*e;if(e2>=dy){e+=dy;x0+=sx}if(e2<=dx){e+=dx;y0+=sy}}}
function D(x,y,w,h,c1,c2){R(x,y,w,h,c1);g.fillStyle=col(c2);for(let j=0;j<h;j++)for(let i=(j%%2);i<w;i+=2)g.fillRect(x+i,y+j,1,1)}  // tramado 50 %%
function CIR(cx,cy,r,c){g.fillStyle=col(c);for(let j=-r;j<=r;j++){const w=Math.round(Math.sqrt(r*r-j*j));g.fillRect(Math.round(cx-w),Math.round(cy+j),2*w+1,1)}}
// cielo por franjas (degradado a bandas, como en el SNES)
function CIELO(cs,y0=0,y1=H){const n=cs.length,h=(y1-y0)/n;cs.forEach((c,i)=>R(0,y0+i*h,W,h+1,c));
  for(let i=0;i<n-1;i++){const y=Math.round(y0+(i+1)*h)-2;D(0,y,W,2,cs[i],cs[i+1])}}
// --- sprites: S(nombre,x,y,{s:escala,f:espejo,c:color único (silueta)})
function S(n,x,y,o={}){const rows=SPR[n],s=o.s||1;x=Math.round(x);y=Math.round(y);
  rows.forEach((r,j)=>{for(let i=0;i<r.length;i++){const ch=r[o.f?r.length-1-i:i];if(ch==='.')continue;
    g.fillStyle=col(o.c||(o.pal&&o.pal[ch])||ch);g.fillRect(x+i*s,y+j*s,s,s)}})}
const SW=n=>SPR[n][0].length,SH=n=>SPR[n].length;
// --- texto pixelado (umbral de alfa: nada de antialias)
const _tc=new Map(),ACC={'Á':['A','a'],'É':['E','a'],'Í':['I','a'],'Ó':['O','a'],'Ú':['U','a'],'Ñ':['N','t'],'Ü':['U','d']};
function _tb(str,z,c){const k=str+'|'+z+'|'+c;let b=_tc.get(k);if(b)return b;
  const m=document.createElement('canvas').getContext('2d');m.font=z+'px "'+FONT+'"';const w=Math.ceil(m.measureText(str).width)+2;
  const cvs=document.createElement('canvas');cvs.width=Math.max(1,w);cvs.height=Math.ceil(z*1.5);const x=cvs.getContext('2d');
  x.font=z+'px "'+FONT+'"';x.textBaseline='top';x.fillStyle=col(c);const top=Math.round(z*.25),u=z/8,ad=w>2?(w-2)/[...str].length:z;
  // la fuente no trae mayúsculas acentuadas: letra base + acento dibujado en píxeles
  x.fillText([...str].map(ch=>ACC[ch]?ACC[ch][0]:ch).join(''),0,top);
  [...str].forEach((ch,i)=>{const a=ACC[ch];if(!a)return;const x0=Math.round(i*ad),M=a[1];
    if(M==='a'){x.fillRect(x0+3*u,top-u,u,u);x.fillRect(x0+4*u,top-2*u,u,u)}
    else if(M==='t'){x.fillRect(x0+2*u,top-2*u,2*u,u);x.fillRect(x0+6*u,top-2*u,u,u);x.fillRect(x0+u,top-u,u,u);x.fillRect(x0+4*u,top-u,2*u,u)}
    else{x.fillRect(x0+2*u,top-2*u,u,u);x.fillRect(x0+5*u,top-2*u,u,u)}});
  const d=x.getImageData(0,0,cvs.width,cvs.height),a=d.data;for(let i=3;i<a.length;i+=4)a[i]=a[i]>100?255:0;x.putImageData(d,0,0);
  b={cv:cvs,w:w-2};_tc.set(k,b);return b}
function TW(str,z=8){return _tb(str,z,'w').w}
// TX(texto,x,y,{z:8|16|24…, c:color, a:'l'|'c'|'r', sh:sombra|null}) → ancho
function TX(str,x,y,o={}){str=String(str);if(!str)return 0;const z=o.z||8,b=_tb(str,z,o.c||'w');let X=Math.round(o.a==='c'?x-b.w/2:o.a==='r'?x-b.w:x),Y=Math.round(y-z*.25);
  if(o.sh!==null){const sb=_tb(str,z,o.sh||'k'),d=Math.max(1,z/8);g.drawImage(sb.cv,X+d,Y+d)}g.drawImage(b.cv,X,Y);return b.w}
// texto que se teclea: TY(texto,t,t0,cps)
const TY=(str,t,t0,v=28)=>t<t0?'':str.slice(0,Math.floor((t-t0)*v));
// caja de diálogo RPG (azul con doble borde)
function BOX(x,y,w,h,o={}){R(x-1,y-1,w+2,h+2,'k');R(x,y,w,h,o.b||'w');R(x+2,y+2,w-4,h-4,'k');
  const f=o.f||['N','n'];const hh=(h-6)/f.length;f.forEach((c,i)=>R(x+3,y+3+i*hh,w-6,hh+1,c));O(x+3,y+3,w-6,h-6,o.b2||'c')}
function BAR(x,y,w,h,v,c,o={}){R(x-1,y-1,w+2,h+2,'k');R(x,y,w,h,o.f||'G');R(x,y,Math.round(w*cl(v)),h,c);R(x,y,Math.round(w*cl(v)),1,o.hi||'w')}
// burbuja «!» sobre algo
function ALERTA(x,y,c='r'){R(x-4,y-11,9,11,'k');R(x-3,y-10,7,9,'w');R(x,y-9,1,4,c);R(x+1,y-9,1,4,c);R(x,y-4,2,2,c);R(x-1,y-1,3,2,'k');R(x,y-1,1,1,'w')}
// moneda (gira por pasos)
function MONEDA(x,y,t,k=0){const f=Math.floor(t*8+k)%%4,w=[6,4,2,4][f];x=Math.round(x-w/2);R(x,y,w,6,'o');R(x,y+1,w,4,'y');if(w>2)R(x+1,y+1,1,3,'Y')}
// sobre de correo
function SOBRE(x,y,c='w',ab=false){R(x,y,10,7,'k');R(x+1,y+1,8,5,c);L(x+1,y+1,x+5,y+4,'g');L(x+8,y+1,x+5,y+4,'g');if(ab){R(x+1,y-3,8,3,c);L(x+1,y-2,x+5,y-4,'g')}}
// servidor (16×28): estado 'ok'|'viejo'|'mal'|'off'|'nuevo'
function SERVIDOR(x,y,st,t,k=0){x=Math.round(x);y=Math.round(y);R(x,y,16,28,'k');R(x+1,y+1,14,26,st==='viejo'?'Q':'G');R(x+1,y+1,14,2,st==='viejo'?'q':'g');
  for(let i=0;i<5;i++){const yy=y+4+i*5;R(x+2,yy,12,4,'k');R(x+3,yy+1,6,2,st==='viejo'?'u':'g');
    const on=hs(k*13+i*7+Math.floor(t*6))>.4,lc=st==='ok'||st==='nuevo'?'l':st==='mal'?'r':st==='viejo'?'o':'G';R(x+11,yy+1,2,2,(st==='off'||!on)?'G':lc)}
  if(st==='viejo'){L(x-2,y-2,x+5,y+5,'s');L(x+3,y-2,x-2,y+3,'s')}}
// palanca ON/OFF (base 22×10): v 0 = OFF, 1 = ON
function PALANCA(x,y,v){x=Math.round(x);y=Math.round(y);R(x,y,24,10,'k');R(x+1,y+1,22,8,'g');R(x+1,y+1,22,2,'s');
  const a=lerp(-0.9,0.9,cl(v)),ex=x+12+Math.sin(a)*16,ey=y-Math.cos(a)*16;for(let d=-1;d<=1;d++)L(x+12+d,y+2,ex+d,ey,'s');CIR(ex,ey,3,v>.5?'r':'R');R(ex-1,ey-2,1,1,'w');
  TX('OFF',x+9,y+13,{c:v<.5?'w':'G',a:'r'});TX('ON',x+16,y+13,{c:v>.5?'l':'G'})}
// marco de juego + etiqueta de la serie (arriba a la izquierda)
function SERIE(){R(4,4,82,12,'k');R(5,5,80,10,'r');TX('ARCHIVO',7,6,{c:'w',sh:'R'});R(62,5,23,10,'y');TX('#01',63,6,{c:'k',sh:null})}
// HUD de dinero + reloj
function HUD(dinero,reloj,o={}){R(0,20,W,22,'k');R(0,41,W,1,'g');TX('$',4,27,{c:'y'});BAR(14,26,110,8,dinero,dinero>.3?'l':'r');
  TX(reloj,W-6,27,{c:o.rc||'w',a:'r'});const cx=W-56;CIR(cx,30,5,'w');CIR(cx,30,4,'k');R(cx,27,1,4,'w');R(cx,30,3,1,'w')}
// mosaico del SNES sobre todo el lienzo
const _m=document.createElement('canvas'),_mx=_m.getContext('2d');
function MOSAICO(b){b=Math.round(b);if(b<=1)return;const w=Math.ceil(W/b),h=Math.ceil(H/b);_m.width=w;_m.height=h;_mx.imageSmoothingEnabled=false;
  _mx.drawImage(cv,0,0,W,H,0,0,w,h);g.imageSmoothingEnabled=false;g.drawImage(_m,0,0,w,h,0,0,w*b,h*b)}
// sacudida de pantalla
const SAC=(t,a,b,amp=3)=>t>=a&&t<b?[Math.round((hs(Math.floor(t*12))-.5)*2*amp),Math.round((hs(Math.floor(t*12)+5)-.5)*2*amp)]:[0,0];
// dibujar a escala entera (bloques nítidos): ESC(x,y,2,()=>SERVIDOR(0,0,…))
function ESC(x,y,s,fn){g.save();g.translate(Math.round(x),Math.round(y));g.scale(s,s);fn();g.restore()}
// corte duro dentro de una página con un parpadeo de mosaico (2 cuadros)
let MZ=1;const CORTE=(t,tc)=>{const d=t-tc;if(d>=-.09&&d<.09)MZ=Math.max(MZ,8);else if(d>=-.17&&d<.17)MZ=Math.max(MZ,4)};
// escenario
function ESTRELLAS(t,n=40,y1=200){for(let i=0;i<n;i++){const x=Math.floor(hs(i)*W),y=Math.floor(hs(i+50)*y1);if(hs(i+Math.floor(t*3))>.25)R(x,y,1,1,hs(i+9)>.7?'Y':'s')}}
function SKYLINE(y,c,k=1,alto=60){let x=0,i=0;while(x<W){const w=12+Math.floor(hs(k*31+i)*20),h=20+Math.floor(hs(k*17+i)*alto);R(x,y-h,w,h,c);
  if(hs(k+i*3)>.5)R(x+w/2-1,y-h-6,2,6,c);x+=w+1;i++}}
function EDIFICIO(x,y,w,h,c,k=0,t=0,luz='y'){R(x,y,w,h,'k');R(x+1,y+1,w-2,h-1,c);for(let j=y+5;j<y+h-6;j+=7)for(let i=x+4;i<x+w-5;i+=6)
  R(i,j,3,4,hs(k+i*7+j*13+Math.floor(t/2))>.45?luz:'k')}
function BOLSA(x,y,t=0){R(x,y+22,120,6,'s');R(x+4,y+28,112,48,'q');for(let i=0;i<6;i++){R(x+10+i*18,y+30,8,44,'w');R(x+10+i*18,y+30,2,44,'s')}
  for(let j=0;j<22;j++){const w=Math.round(120*(j+1)/22);R(x+60-w/2,y+j,w,1,j%%3?'q':'w')}R(x,y+76,120,6,'s');R(x-6,y+82,132,4,'g');
  TX('BOLSA',x+60,y+12,{c:'k',a:'c',sh:null})}
function PISO(y,c1='G',c2='k'){R(0,y,W,H-y,c1);for(let j=y;j<H;j+=8)R(0,j,W,1,c2);for(let i=0;i<W;i+=16)R(i+((Math.floor((H-y)/8))%%2)*8,y,1,H-y,c2)}
// ventana con título (estilo menú de juego)
function VENTANA(x,y,w,h,tit,o={}){BOX(x,y,w,h,{f:o.f||['n'],b:o.b||'w',b2:o.b2||'c'});if(tit){R(x+6,y-5,TW(tit)+8,10,o.tc||'y');TX(tit,x+10,y-4,{c:'k',sh:null})}}
function CODIGO(x,y,w,n,t,k=0,cs=['l','c','s','m','y']){for(let i=0;i<n;i++){let xx=x+(hs(k+i)>.6?8:0)+(hs(k+i*5)>.85?16:0);const m=1+Math.floor(hs(k+i*3)*4);
  for(let j=0;j<m&&xx<x+w-6;j++){const ww=Math.min(x+w-xx,6+Math.floor(hs(k+i*11+j)*22));R(xx,y+i*7,ww,3,cs[Math.floor(hs(k+i+j*7)*cs.length)]);xx+=ww+4}}}
function CONFETI(t,t0,x,y,n=30){if(t<t0)return;const d=t-t0;for(let i=0;i<n;i++){const a=hs(i)*Math.PI*2,v=40+hs(i+3)*80;
  const px=x+Math.cos(a)*v*d,py=y+Math.sin(a)*v*d*.7+60*d*d;R(px,py,2,2,['r','y','l','c','m'][i%%5])}}
function CAMPANA(x,y,t,sw=0){const a=Math.sin(t*20)*sw;x=Math.round(x+a*4);R(x-2,y-4,4,3,'T');R(x-8,y,16,4,'y');R(x-10,y+4,20,10,'y');R(x-12,y+14,24,3,'o');R(x-8,y+2,3,10,'Y');CIR(x+a*3,y+19,2,'T')}
function BANDERA(x,y,t){for(let j=0;j<7;j++)for(let i=0;i<28;i++){const yy=y+j*3+Math.round(Math.sin(t*6+i*.4)*1.5);R(x+i,yy,1,3,j%%2?'w':'r')}
  for(let j=0;j<4;j++)for(let i=0;i<12;i++){const yy=y+j*3+Math.round(Math.sin(t*6+i*.4)*1.5);R(x+i,yy,1,3,'b')}
  for(let j=0;j<3;j++)for(let i=0;i<4;i++)R(x+1+i*3,y+1+j*3+Math.round(Math.sin(t*6+i*1.2)*1.5),1,1,'w');R(x-2,y-2,2,40,'s')}
"""

PAGINA = """<!doctype html><html><head><meta charset=utf-8>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=block" rel=stylesheet>
<style>html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:%(BG)s}
canvas{display:block;width:1080px;height:1920px;image-rendering:pixelated}</style></head>
<body><canvas id=c width=%(W)d height=%(H)d></canvas><script>
%(RUNTIME)s
const DUR=%(DUR).3f,MI=%(MI)s,MO=%(MO)s,TRANSP=%(TR)s,FONDO='%(FONDO)s';
%(EXTRA)s
const draw=(t)=>{%(DRAW)s};
function frame(t){g.setTransform(1,0,0,1,0,0);g.imageSmoothingEnabled=false;if(TRANSP)g.clearRect(0,0,W,H);else R(0,0,W,H,FONDO);
  MZ=1;draw(t);if(TRANSP)return;let b=MZ;if(MI&&t<.36)b=lerp(16,1,P(t,0,.34));if(MO&&t>DUR-.36)b=Math.max(b,lerp(1,16,P(t,DUR-.34,DUR-.02)));
  if(b>1.5)MOSAICO(b<3?2:b<6?4:b<10?8:16)}
window.__cps=CPS;
window.__seek=s=>{s=Math.floor(s*CPS+1e-6)/CPS;window.__t=s;frame(s)};
window.__listo=document.fonts.load('8px "'+FONT+'"').then(()=>document.fonts.ready).then(()=>{
  if(!document.fonts.check('8px "'+FONT+'"'))throw new Error('falta fuente '+FONT);_tc.clear();window.__seek(window.__t||0)});
window.__seek(0);
</script></body></html>"""


def runtime():
    return RUNTIME % dict(W=W, H=H, CPS=CPS, FONT=FUENTE, PAL=json.dumps(PAL), SPR=json.dumps(SPR))


def page(draw, dur, mosaico=(True, True), fondo='k', transparente=False, extra=''):
    """Página de 1080×1920 que dibuja `draw` (cuerpo JS de (t)=>{…}, t local) en el lienzo de 270×480."""
    return PAGINA % dict(BG='transparent' if transparente else PAL.get(fondo, fondo), W=W, H=H, RUNTIME=runtime(), DUR=dur,
                         MI=json.dumps(bool(mosaico[0])), MO=json.dumps(bool(mosaico[1])), TR=json.dumps(transparente),
                         FONDO=fondo, EXTRA=extra, DRAW=draw)


def subtitulos(G, dur, ocultar=(), y=333, z=16, ancho=15):
    """Capa transparente: caja de diálogo RPG abajo con el grupo actual (mayúsculas), palabra activa en amarillo.
    G = grupos de cli/subtitulos.py ([{ini, fin, w:[[palabra, a, b]]}]); `ocultar` = tramos [a, b] sin subtítulos.
    z = tamaño del texto en px del juego (16 → 64 px en el video); `ancho` = caracteres por renglón."""
    data = json.dumps([dict(i=round(g['ini'], 2), f=round(g['fin'], 2), w=[[w.upper(), round(a, 2), round(b, 2)] for w, a, b in g['w']]) for g in G],
                      ensure_ascii=False)
    draw = f"""const G={data},OC={json.dumps([list(o) for o in ocultar])};if(OC.some(([a,b])=>t>=a&&t<b))return;
const k=G.findIndex(q=>t>=q.i&&t<q.f);if(k<0)return;const q=G[k],z={z};
// renglones de máx {ancho} caracteres
const ln=[[]];let n=0;q.w.forEach((p,j)=>{{const l=p[0].length;if(n&&n+1+l>{ancho}){{ln.push([]);n=0}}ln[ln.length-1].push(j);n+=(n?1:0)+l}});
const h=ln.length*z*1.25+14,y0={y}+(48-h)/2;BOX(6,y0,W-12,h,{{f:['N','n']}});
let on=-1;q.w.forEach((p,j)=>{{if(t>=p[1]-.05)on=j}});
ln.forEach((r,i)=>{{const txt=r.map(j=>q.w[j][0]).join(' ');let x=W/2-TW(txt,z)/2;const yy=y0+8+i*z*1.25;
  r.forEach(j=>{{x+=TX(q.w[j][0],x,yy,{{z,c:j===on?'y':'w'}})+TW(' ',z)}})}});
if(blink(t,2))R(W-16,y0+h-6,5,2,'y');"""
    return page(draw, dur, mosaico=(False, False), transparente=True)
