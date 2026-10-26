"""Estilo «Cinta VHS»: noticiero de los 90 grabado en casete. Todo es la señal de una cinta reproducida: scanlines, ruido,
viñeta, aberración cromática, OSD de videocasetera (▶ PLAY, ◀◀ REW, ▶▶ FF, ❚❚ PAUSE, ● REC, contador y fechador de cámara)
y grafismo de noticiero noventero (cintillo azul con biselado, «ÚLTIMA HORA», logo de canal, ticker, gráficas en pantalla).
Entre escenas no hay fundido: la cinta pierde el tracking (franjas de ruido, la imagen se tuerce y salta) y entra la siguiente.

Todo se calcula en __seek a partir del tiempo (sin animaciones CSS/WAAPI), así que las capturas en paralelo no pierden piezas.
Tiempos: segundos del video final. Cada página fija su inicio con nueva(S0); los ayudantes convierten a tiempo local.
"""
import html as H
import json

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo+Narrow:wght@500;700'
         '&family=VT323&display=block" rel="stylesheet">')
CPS = 30
_S0 = [0.0]

AZUL = '#1b2fd0'      # pantalla azul de videocasetera
ORO = '#ffcf3a'
ROJO = '#ff2a3d'
AMBAR = '#ffb02e'
CIAN = '#46e6ff'

BASE = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#000;color:#fff;-webkit-font-smoothing:antialiased;font-synthesis:none}
.tv{position:absolute;inset:0;overflow:hidden;background:var(--fondo)}
#scn{position:absolute;inset:0;--ca:3px}
.el{position:absolute;visibility:hidden}
.ca{text-shadow:calc(var(--ca)*-1) 0 rgba(255,30,70,.65),var(--ca) 0 rgba(40,220,255,.6),0 4px 0 rgba(0,0,0,.45)}
.tt{white-space:nowrap;font-family:'Archivo Black',sans-serif;text-transform:uppercase;line-height:.95;letter-spacing:-.01em}
.nr{font-family:'Archivo Narrow',sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:.02em}
.vt{font-family:'VT323',monospace;line-height:.95}
/* caja de noticiero: degradado + biselado */
.cj{padding:22px 34px;background:linear-gradient(180deg,var(--c1,#2f57ff),var(--c2,#0b1c86));border:3px solid rgba(255,255,255,.55);
  box-shadow:inset 0 3px 0 rgba(255,255,255,.45),inset 0 -5px 0 rgba(0,0,0,.35),0 10px 0 rgba(0,0,0,.4),0 18px 40px rgba(0,0,0,.5)}
.oro{background:linear-gradient(180deg,#fff2a6,#ffcf3a 45%,#c98a00);color:#2a1600;text-shadow:0 2px 0 rgba(255,255,255,.5)}
.rojo{--c1:#ff5161;--c2:#a3000f}
.amb{color:var(--amb,#ffb02e);text-shadow:0 0 14px rgba(255,160,40,.55)}
/* pantalla CRT dentro del cuadro */
.crt{background:radial-gradient(120% 120% at 50% 40%,#2a1a06,#0d0700 70%);border-radius:34px;border:14px solid #2b2b33;
  box-shadow:inset 0 0 60px rgba(0,0,0,.9),0 0 0 6px #111,0 24px 50px rgba(0,0,0,.6);overflow:hidden}
.crt:after{content:'';position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,.35) 0 2px,transparent 2px 5px);pointer-events:none}
/* rack de servidor lo-fi */
.rk{background:linear-gradient(180deg,#3a3f52,#1c1f2b);border:3px solid #6a7090;border-radius:8px;box-shadow:inset 0 2px 0 rgba(255,255,255,.25),0 10px 0 rgba(0,0,0,.45)}
.rk .u{height:30px;margin:10px 12px;background:#10121a;border:2px solid #4b5170;display:flex;align-items:center;gap:8px;padding:0 10px}
.led{width:12px;height:12px;border-radius:50%;background:#2c3a2c}
.led.on{background:#69ff7d;box-shadow:0 0 10px #69ff7d}
.led.r.on{background:#ff3347;box-shadow:0 0 12px #ff3347}
.led.a.on{background:#ffb02e;box-shadow:0 0 10px #ffb02e}
/* interruptor */
.sw{width:170px;height:280px;border-radius:26px;background:linear-gradient(180deg,#d9dbe4,#8b8f9e);border:4px solid #f4f5fa;
  box-shadow:inset 0 -8px 0 rgba(0,0,0,.25),0 14px 0 rgba(0,0,0,.45)}
.sw .pal{position:absolute;left:45px;width:80px;height:120px;border-radius:14px;background:linear-gradient(180deg,#30344a,#0e1020);border:3px solid #000}
/* overlays de la cinta */
#nz{position:absolute;inset:0;width:1080px;height:1920px;pointer-events:none;z-index:80}
.scan{position:absolute;inset:0;z-index:81;pointer-events:none;background:repeating-linear-gradient(0deg,rgba(0,0,0,.22) 0 2px,rgba(255,255,255,.03) 2px 3px,transparent 3px 6px)}
.vig{position:absolute;inset:0;z-index:82;pointer-events:none;background:radial-gradient(130% 95% at 50% 50%,transparent 55%,rgba(0,0,0,.55) 100%)}
#osd{position:absolute;inset:0;z-index:90;pointer-events:none;font-family:'VT323',monospace;color:#fff;
  text-shadow:3px 3px 0 rgba(0,0,0,.75),-2px 0 0 rgba(255,40,80,.45),2px 0 0 rgba(40,220,255,.45)}
#osd .m{position:absolute;left:70px;top:70px;font-size:82px}
#osd .sp{position:absolute;left:74px;top:150px;font-size:56px}
#osd .cnt{position:absolute;right:140px;top:70px;font-size:76px;text-align:right}
#osd .rl{position:absolute;left:74px;top:204px;font-size:56px}
.bug{position:absolute;right:140px;top:160px;z-index:89;display:flex;align-items:stretch;transform:skewX(-8deg);
  box-shadow:0 6px 0 rgba(0,0,0,.45),0 0 0 3px rgba(255,255,255,.7)}
.bug b{font-family:'Archivo Black';font-weight:400;font-size:34px;padding:6px 14px;letter-spacing:.04em}
.bug i{font-style:normal;font-family:'Archivo Black';font-size:34px;padding:6px 12px;background:#e0001b;color:#fff}
"""

JS = r"""
const CPS=__CPS__,_Q=1000/CPS;window.__cps=CPS;
const _h=i=>{const x=Math.sin(i*12.9898+78.233)*43758.5453;return x-Math.floor(x)};
const _c=v=>Math.min(1,Math.max(0,v)),_eo=p=>1-Math.pow(1-p,3),_ei=p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2;
const _v=(k,t)=>{let v=k[0][1];for(const [a,b,d] of k.slice(1)){const p=_c((t-a)/(d||.8));v=v+(b-v)*_ei(p)}return v};
const _hora=s=>{s=Math.round(s);let h=Math.floor(s/3600)%%24,m=Math.floor(s/60)%%60,x=s%%60;const ap=h<12?'AM':'PM';h=h%%12||12;
 return `${h}:${String(m).padStart(2,'0')}:${String(x).padStart(2,'0')} ${ap}`};
const _f=(v,f)=>f==='m'?'$'+Math.round(v).toLocaleString('en-US'):f==='c'?Math.round(v).toLocaleString('en-US'):f==='h'?_hora(v)
 :f==='ms'?String(Math.floor(v/60)).padStart(2,'0')+':'+String(Math.floor(v%%60)).padStart(2,'0'):f==='1'?v.toFixed(1):String(Math.round(v));
const _dec=h=>{const d=document.createElement('textarea');d.innerHTML=h.replace(/<br\s*\/?>/g,'\n');return d.value};
const scn=document.getElementById('scn');
const E=[...document.querySelectorAll('[data-i]')].map(e=>({e,i:+e.dataset.i,o:e.dataset.o!==undefined?+e.dataset.o:1e9,fx:e.dataset.fx||'cut',
 d:+(e.dataset.d||.3),r:+(e.dataset.r||24),sk:+(e.dataset.sk||0),txt:e.dataset.fx==='type'?_dec(e.innerHTML):null,base:e.style.transform||'',pa:e.parentElement.closest('[data-i]')}));
const N=[...document.querySelectorAll('[data-n]')].map(e=>[e,JSON.parse(e.dataset.n)]);
const MQ=[...document.querySelectorAll('[data-mq]')].map(e=>[e,+e.dataset.mq]);
const DR=[...document.querySelectorAll('[data-dr]')].map(e=>{const [a,d]=e.dataset.dr.split(',').map(Number);const L=e.getTotalLength();e.style.strokeDasharray=L;return [e,a,d,L]});
const LD=[...document.querySelectorAll('[data-bk]')].map(e=>{const [p,s,a,b]=e.dataset.bk.split(',').map(Number);return [e,p,s,a??-1e9,b??1e9]});
const RT=[...document.querySelectorAll('[data-rot]')].map(e=>[e,+e.dataset.rot]);
const PR=[...document.querySelectorAll('[data-pr]')].map(e=>[e,JSON.parse(e.dataset.pr)]);
const nz=document.getElementById('nz'),g=nz.getContext('2d');const NW=270,NH=480;const ns=document.createElement('canvas');ns.width=NW;ns.height=NH;
const ng=ns.getContext('2d'),nd=ng.createImageData(NW,NH);
const osd=document.getElementById('osd');const om=osd&&osd.querySelector('.m'),oc=osd&&osd.querySelector('.cnt'),od=osd&&osd.querySelector('.sp'),orl=osd&&osd.querySelector('.rl');
// modo de la cinta en el segundo T del video
const modo=T=>{let m='PLAY';for(const [a,x] of MODOS)if(T>=a)m=x;return m};
const VEL={PLAY:1,REW:-9,FF:9,PAUSE:0,REC:1,STOP:0,EJECT:0};
const contador=T=>{let c=0,t=0;for(let k=0;k<MODOS.length;k++){const [a,m]=MODOS[k];const b=k+1<MODOS.length?MODOS[k+1][0]:1e9;if(T<=a)break;c+=(Math.min(T,b)-a)*VEL[m]}return Math.max(0,c+CONT0)};
const fecha=T=>{let f=FECHAS[0][1];for(const [a,x] of FECHAS)if(T>=a)f=x;return f};
window.__seek=s=>{const ms=Math.floor(s*1000/_Q+1e-6)*_Q;const t=ms/1000,T=t+S0,fr=Math.round(T*CPS);
 for(const x of E){const on=t>=x.i&&t<x.o&&(!x.pa||x.pa._on);x.e._on=on;x.e.style.visibility=on?'visible':'hidden';if(!on)continue;const p=_c((t-x.i)/x.d),q=_eo(p);let tr=x.base,cp='';
  switch(x.fx){case 'wipe':cp=`inset(0 ${(100-100*q).toFixed(2)}% 0 0)`;break;case 'wipeu':cp=`inset(${(100-100*q).toFixed(2)}% 0 0 0)`;break;
   case 'slide':tr+=` translateX(${(-1150*(1-q)).toFixed(1)}px)`;break;case 'slider':tr+=` translateX(${(1150*(1-q)).toFixed(1)}px)`;break;
   case 'pop':tr+=` scale(${(1+.45*(1-q)).toFixed(3)})`;break;case 'zoom':tr+=` scale(${Math.max(.001,q).toFixed(3)})`;break;
   case 'flip':tr+=` perspective(900px) rotateX(${(90*(1-q)).toFixed(1)}deg)`;break;
   case 'blink':x.e.style.visibility=Math.floor((t-x.i)*2.5)%%2?'hidden':'visible';break;
   case 'type':{const tx=x.txt,k=Math.min(tx.length,Math.floor((t-x.i)*x.r));
     x.e.innerHTML=H(tx.slice(0,k)).replace(/\n/g,'<br>')+(k<tx.length?'<span style="opacity:.9">█</span>':'');break}}
  if(x.sk)tr+=` translate(${((_h(fr*3+x.i)-.5)*x.sk).toFixed(1)}px,${((_h(fr*7+x.i)-.5)*x.sk).toFixed(1)}px)`;
  x.e.style.transform=tr;x.e.style.clipPath=cp}
 for(const [e,k] of N)e.textContent=(e.dataset.pre||'')+_f(_v(k,T),e.dataset.f)+(e.dataset.suf||'');
 for(const [e,v] of MQ){const w=e.scrollWidth/2;e.style.transform=`translateX(${(-((t*v)%%w)).toFixed(1)}px)`}
 for(const [e,a,d,L] of DR)e.style.strokeDashoffset=(L*(1-_eo(_c((t-a)/d)))).toFixed(1);
 for(const [e,p,s,a,b] of LD)e.classList.toggle('on',t>=a&&t<b&&_h(Math.floor(t/p)*31+s)>.35);
 for(const [e,v] of RT)e.style.transform=`rotate(${(t*v).toFixed(2)}deg)`;
 for(const [e,k] of PR)e.style.width=(_c(_v(k,T))*100).toFixed(2)+'%%';
 // tracking: franjas, torcido y saltos
 let a=0;for(const [g0,d,amp] of GL){if(t>=g0&&t<g0+d)a=Math.max(a,amp*Math.sin(Math.PI*_c((t-g0)/d)))}
 const m=modo(T),busca=m==='REW'||m==='FF',pausa=m==='PAUSE';
 let dx=(_h(fr)-.5)*1.6,dy=0,sk=0;if(a>0){dx+=(_h(fr*5+1)-.5)*140*a;sk=(_h(fr*5+2)-.5)*10*a;dy=(_h(fr*5+3)-.5)*90*a}
 if(busca){dx+=(_h(fr*9)-.5)*10;dy+=(_h(fr*9+1)-.5)*8}if(pausa)dy+=(fr%%2)*3;
 scn.style.transform=`translate(${dx.toFixed(1)}px,${dy.toFixed(1)}px) skewX(${sk.toFixed(2)}deg)`;scn.style.setProperty('--ca',(3+a*16+(busca?6:0)).toFixed(1)+'px');
 // ruido fino de la cinta
 const D=nd.data;let sd=fr*977+13;for(let i=0;i<D.length;i+=4){sd=(sd*16807)%%2147483647;const v=sd%%256;D[i]=D[i+1]=D[i+2]=v;D[i+3]=(sd>>9)%%40+(a>0?40*a:0)}
 ng.putImageData(nd,0,0);g.clearRect(0,0,1080,1920);g.globalAlpha=.55;g.drawImage(ns,0,0,1080,1920);g.globalAlpha=1;
 const banda=(y,h,al)=>{for(let k=0;k<h;k+=3){g.fillStyle=`rgba(255,255,255,${(al*_h(fr*11+y+k)).toFixed(3)})`;const x0=_h(fr+k+y)*200-100;g.fillRect(x0,y+k,1080,2)}};
 if(a>0)for(let k=0;k<7;k++)banda(Math.floor(_h(fr*3+k)*1900),10+Math.floor(_h(fr*3+k+50)*70*a),.85*a);
 if(busca)for(let k=0;k<3;k++)banda(Math.floor(((T*(m==='REW'?-900:900))%%1920+1920+k*640)%%1920),46,.8);
 if(pausa)banda(1300+Math.floor(_h(fr)*8),22,.6);
 banda(1872,48,.55);  // conmutación de cabezas abajo
 if(osd){const ic={PLAY:'▶ PLAY',REW:'◀◀ REW',FF:'▶▶ FF',PAUSE:'❚❚ PAUSE',REC:'● REC',STOP:'■ STOP',EJECT:'⏏ EJECT'}[m];
  om.textContent=ic;om.style.color=m==='REC'?'#ff3347':'#fff';om.style.visibility=(m==='PAUSE'||m==='REC')&&Math.floor(T*2.5)%%2?'hidden':'visible';
  const c=contador(T);oc.textContent=Math.floor(c/3600)+':'+String(Math.floor(c/60)%%60).padStart(2,'0')+':'+String(Math.floor(c)%%60).padStart(2,'0');
  od.textContent='SP  '+fecha(T);if(orl){let r='';for(const [a,b,ini,fin] of RELOJ)if(T>=a&&T<b+60)r=_hora(ini+(fin-ini)*_ei(_c((T-a)/(b-a))));orl.textContent=r}}
};
function H(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
const _F=['400 80px VT323','400 80px "Archivo Black"','700 80px "Archivo Narrow"'];
window.__listo=Promise.all(_F.map(f=>document.fonts.load(f))).then(()=>document.fonts.ready).then(()=>{const m=_F.filter(f=>!document.fonts.check(f));if(m.length)throw new Error('faltan fuentes: '+m)});
window.__seek(0);""".replace('%%', '%').replace('__CPS__', str(CPS))


def nueva(S0):
    """Empieza una página que arranca en el segundo S0 del video final."""
    _S0[0] = S0


def L(t):
    return round(t - _S0[0], 3)


def el(html, x, y, i, o=None, fx='cut', d=.3, w=None, h=None, cls='', st='', r=None, sk=0, extra=''):
    """Pieza posicionada. fx: cut|wipe|wipeu|slide|slider|pop|zoom|flip|blink|type (r = letras/s). sk = temblor (px)."""
    a = f'data-i="{L(i)}" data-fx="{fx}" data-d="{d}"' + (f' data-o="{L(o)}"' if o is not None else '')
    a += (f' data-r="{r}"' if r else '') + (f' data-sk="{sk}"' if sk else '')
    s = f'left:{x}px;top:{y}px;' + (f'width:{w}px;' if w else '') + (f'height:{h}px;' if h else '') + st
    return f'<div class="el {cls}" {a} {extra} style="{s}">{html}</div>'


def tt(txt, x, y, size, i, o=None, color='#fff', fx='pop', d=.25, w=None, cls='', st='', sk=0):
    """Titular de noticiero: Archivo Black en mayúsculas con aberración cromática."""
    return el(txt, x, y, i, o, fx, d, w, cls=f'tt ca {cls}', st=f'font-size:{size}px;color:{color};{"white-space:normal;" if w else ""}{st}', sk=sk)


def nr(txt, x, y, size, i, o=None, color='#fff', fx='wipe', d=.3, w=None, cls='', st=''):
    return el(txt, x, y, i, o, fx, d, w, cls=f'nr ca {cls}', st=f'font-size:{size}px;color:{color};{st}')


def vt(txt, x, y, size, i, o=None, color='#fff', fx='type', r=26, w=None, cls='', st=''):
    """Texto de terminal/OSD en VT323; fx='type' lo teclea (r letras por segundo). Usa <br> para saltos."""
    return el(txt, x, y, i, o, fx, .3, w, cls=f'vt {cls}', st=f'font-size:{size}px;color:{color};{st}', r=r)


def num(keys, x, y, size, i, o=None, f='c', color='#fff', pre='', suf='', fx='pop', cls='tt ca', st=''):
    """Cifra que corre: keys = [[t, v], [t, v, dur], …] con t en segundos del video final."""
    k = json.dumps(keys)
    return el(f'<span data-n=\'{k}\' data-f="{f}" data-pre="{H.escape(pre)}" data-suf="{H.escape(suf)}">{pre}0{suf}</span>',
              x, y, i, o, fx, .25, cls=cls, st=f'font-size:{size}px;color:{color};white-space:nowrap;{st}')


def caja(html, x, y, i, o=None, w=None, fx='flip', d=.35, cls='', st=''):
    return el(html, x, y, i, o, fx, d, w, cls=f'cj {cls}', st=st)


def urgente(i, o=None, x=70, y=310, txt='ÚLTIMA HORA'):
    """Etiqueta roja que parpadea su punto."""
    return el(f'<span class="led r" data-bk=".4,1" style="display:inline-block;margin-right:16px;vertical-align:middle;width:22px;height:22px"></span>{txt}',
              x, y, i, o, 'wipe', .25, cls='cj rojo nr', st='font-size:48px;padding:12px 26px')


def cintillo(tag, titulo, i, o=None, y=1140, tagc='oro'):
    """Cintillo inferior (lower third): etiqueta + barra azul biselada; entra deslizándose."""
    return el(f'<div class="nr {tagc}" style="display:inline-block;font-size:34px;padding:8px 20px;margin-left:30px">{tag}</div>'
              f'<div class="cj tt" style="font-size:50px;padding:18px 34px;line-height:1.02;white-space:normal">{titulo}</div>',
              40, y, i, o, 'slide', .35, w=880)


def ticker(texto, y, i, o=None, vel=260, color='#fff', fondo='#0a0f3a'):
    """Barra de cotizaciones que corre a la izquierda (texto se duplica para el bucle)."""
    t = f'<span style="padding-right:60px">{texto}</span>'
    return el(f'<div data-mq="{vel}" style="white-space:nowrap;display:inline-block">{t}{t}</div>', 0, y, i, o, 'wipe', .3, w=1080,
              cls='vt', st=f'font-size:54px;color:{color};background:{fondo};padding:8px 0;overflow:hidden;border-top:3px solid {ORO};border-bottom:3px solid {ORO}')


def grafica(puntos, x, y, w, h, i, o=None, d=1.2, color=ROJO, grosor=8, rejilla=True):
    """Gráfica de línea en pantalla de tele: puntos 0..1 (y=1 arriba); se dibuja en d segundos."""
    n = len(puntos) - 1
    pts = ' '.join(f'{w * k / n:.1f},{h - h * v:.1f}' for k, v in enumerate(puntos))
    rej = ''.join(f'<line x1="0" x2="{w}" y1="{h * k / 4:.0f}" y2="{h * k / 4:.0f}" stroke="rgba(255,255,255,.18)" stroke-width="2"/>' for k in range(5)) if rejilla else ''
    svg = (f'<svg width="{w}" height="{h}" style="overflow:visible">{rej}<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{grosor}" '
           f'stroke-linejoin="round" stroke-linecap="round" data-dr="{L(i)},{d}" style="filter:drop-shadow(0 0 10px {color})"/></svg>')
    return el(svg, x, y, i, o, 'cut')


def rack(x, y, i, o=None, w=220, u=5, nombre='', leds='', fx='zoom', estado=None, sk=0):
    """Servidor lo-fi: u unidades con luces que parpadean. estado = html bajo el rack (versión, palomita…)."""
    filas = ''.join(f'<div class="u"><span class="led {leds}" data-bk=".{3 + k % 4},{k * 7 + int(x)}"></span>'
                    f'<span class="led a" data-bk=".{5 + k % 3},{k * 3 + int(y)}"></span>'
                    f'<span style="flex:1;height:6px;background:#2a2f44"></span></div>' for k in range(u))
    pie = f'<div class="vt" style="font-size:40px;text-align:center;margin-top:8px">{nombre}</div>' if nombre else ''
    return el(f'<div class="rk" style="width:{w}px;padding:6px 0">{filas}</div>{pie}{estado or ""}', x, y, i, o, fx, .3, sk=sk)


def interruptor(x, y, i, o=None, on_t=None, etiqueta='FLAG', fx='zoom'):
    """Interruptor de pared; on_t = segundo (video final) en que se prende (la palanca baja→sube)."""
    ab = 'top:130px'
    pal = (f'<div class="pal" style="{ab}"></div>' if on_t is None else
           f'<div class="pal el" data-i="{L(i)}" data-o="{L(on_t)}" style="top:130px;visibility:visible"></div>'
           f'<div class="pal el" data-i="{L(on_t)}" style="top:30px;background:linear-gradient(180deg,#ff5161,#a3000f)"></div>')
    luz = '' if on_t is None else f'<div class="el vt" data-i="{L(on_t)}" style="left:0;width:170px;top:-80px;text-align:center;font-size:60px;color:{ROJO};text-shadow:0 0 18px {ROJO}">ON</div>'
    return el(f'<div class="sw" style="position:relative">{pal}{luz}</div><div class="vt" style="font-size:44px;text-align:center;width:170px;margin-top:14px">{etiqueta}</div>',
              x, y, i, o, fx, .3)


def cassette(x, y, i, o=None, etiqueta='', fx='zoom', w=620, extra=''):
    """Casete VHS visto de frente con su etiqueta (extra = html encima de la etiqueta)."""
    hw = int(w * .56)
    return el(f'<div style="position:relative;width:{w}px;height:{hw}px;background:linear-gradient(180deg,#26262c,#0c0c10);border-radius:18px;'
              f'border:4px solid #3b3b44;box-shadow:inset 0 3px 0 rgba(255,255,255,.18),0 16px 0 rgba(0,0,0,.5)">'
              f'<div style="position:absolute;left:8%;right:8%;top:9%;height:40%;background:#f4efe2;border-radius:6px;color:#1a1a1a;'
              f'font-family:\'Archivo Narrow\';font-weight:700;font-size:{int(w * .068)}px;padding:10px 18px;line-height:1.05;transform:rotate(-.6deg)">{etiqueta}{extra}</div>'
              f'<div style="position:absolute;left:22%;right:22%;bottom:10%;height:30%;background:#000;border-radius:10px;border:3px solid #444;'
              f'display:flex;justify-content:space-around;align-items:center">'
              f'<div data-rot="-160" style="width:{int(w * .13)}px;height:{int(w * .13)}px;border-radius:50%;background:repeating-conic-gradient(#ddd 0 20deg,#555 20deg 60deg)"></div>'
              f'<div data-rot="-160" style="width:{int(w * .13)}px;height:{int(w * .13)}px;border-radius:50%;background:repeating-conic-gradient(#ddd 0 20deg,#555 20deg 60deg)"></div>'
              f'</div></div>', x, y, i, o, fx, .3)


def barra(keys, x, y, w, i, o=None, color=CIAN, alto=40, fx='cut', etiqueta=''):
    """Barra de progreso; keys = [[t, 0..1], [t, 0..1, dur]…] en segundos del video final."""
    return el(f'<div style="width:{w}px;height:{alto}px;border:3px solid #fff;padding:4px;background:#000">'
              f'<div data-pr=\'{json.dumps(keys)}\' style="height:100%;width:0;background:repeating-linear-gradient(90deg,{color} 0 18px,transparent 18px 24px)"></div></div>{etiqueta}',
              x, y, i, o, fx, .25)


def bug(n='01'):
    return f'<div class="bug"><b class="oro">ARCHIVO</b><i>{n}</i></div>'


def page(body, dur, S0, fondo='radial-gradient(130% 80% at 50% 30%,#1b3bbf,#06103f 70%,#020414)', glitches=(), modos=(('0', 'PLAY'),),
         fechas=((0, ''),), reloj=(), cont0=0, osd=True, canal=True, entra=True, sale=True):
    """Página opaca de la cinta. glitches = [(t, dur, amp)] en segundos del video final; se agregan solos el de entrada y el de salida.
    modos = [(t, 'PLAY'|'REW'|'FF'|'PAUSE'|'REC'|'STOP'|'EJECT')], fechas = [(t, 'AGO. 01 2012')], reloj = [(t0, t1, seg0, seg1)] (hora del día)."""
    gl = [(round(t - S0, 3), d, a) for t, d, a in glitches]
    if entra:
        gl.append((0, .28, 1))
    if sale:
        gl.append((round(dur - .2, 3), .2, 1))
    osd_html = ('<div id="osd"><div class="m"></div><div class="sp"></div><div class="cnt"></div><div class="rl"></div></div>' if osd else '')
    cfg = (f'const S0={S0},GL={json.dumps(gl)},MODOS={json.dumps([[float(a), m] for a, m in modos])},FECHAS={json.dumps([[float(a), f] for a, f in fechas])},'
           f'RELOJ={json.dumps([list(r) for r in reloj])},CONT0={cont0};')
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{BASE}</style></head><body>
<div class="tv" style="--fondo:{fondo}"><div id="scn">{body}</div>{bug() if canal else ''}<canvas id="nz" width="1080" height="1920"></canvas>
<div class="scan"></div><div class="vig"></div>{osd_html}</div>
<script>{cfg}{JS}</script></body></html>"""


def subtitulos(G, dur, ocultar=()):
    """Capa transparente de subtítulos tipo closed caption: blanco monoespaciado sobre caja negra; palabra activa en amarillo."""
    data = json.dumps([dict(i=round(g['ini'], 2), f=round(g['fin'], 2), w=[[H.escape(w), round(a, 2), round(b, 2)] for w, a, b in g['w']]) for g in G],
                      ensure_ascii=False)
    css = ("*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1920px;overflow:hidden;background:transparent}"
           "#s{position:absolute;left:70px;right:140px;top:1340px;height:180px;display:flex;align-items:center;justify-content:center;text-align:center}"
           "#s span.l{display:inline;font-family:'VT323',monospace;font-size:84px;line-height:1.18;color:#fff;background:#000;padding:2px 16px;"
           "box-decoration-break:clone;-webkit-box-decoration-break:clone;text-transform:uppercase}"
           "#s i{font-style:normal}#s i.on{color:#ffe14a}")
    js = (f"const G={data},O={json.dumps([list(r) for r in ocultar])};const el=document.getElementById('s');window.__cps=10;"
          "window.__seek=s=>{s=Math.floor(s*10+1e-6)/10;if(O.some(([a,b])=>s>=a&&s<b)){el.innerHTML='';return}"
          "const k=G.findIndex(g=>s>=g.i&&s<g.f);if(k<0){el.innerHTML='';return}"
          "const g=G[k];let on=-1;g.w.forEach(([w,a],j)=>{if(s>=a-.05)on=j});"
          "el.innerHTML='<span class=l>'+g.w.map(([w],j)=>`<i class=\"${j===on?'on':''}\">${w}</i>`).join(' ')+'</span>'};"
          "window.__listo=document.fonts.load('400 80px VT323').then(()=>document.fonts.ready).then(()=>{if(!document.fonts.check('400 80px VT323'))throw new Error('falta VT323')});"
          "window.__seek(0);")
    return (f"<!doctype html><html><head><meta charset=utf-8>{FONTS}<style>{css}</style></head><body><div id=s></div><script>{js}</script></body></html>")
