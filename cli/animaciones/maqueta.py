"""Estilo «Maqueta»: la historia ocurre en un diorama 3D en miniatura (maqueta de arquitectura / juguete) que la cámara
isométrica recorre. Low-poly de sombreado plano, colores sobrios, sombras suaves y desenfoque de tilt-shift arriba y abajo.
Las piezas crecen desde el piso de la maqueta y se hunden al salir; los textos son letreros físicos dentro del diorama
(maqueta.js: M.letrero, M.pintura), placas limpias en pantalla (placa) o etiquetas con línea guía clavadas a un punto 3D (pin).

Continuidad: el mundo y la cámara dependen del tiempo GLOBAL (segundos del video final). Cada página construye el diorama
completo y renderiza solo su tramo, así que el corte entre páginas es invisible y la «transición» es el travelling de la
cámara a otra parte de la maqueta. Nada se desvanece: las placas entran subiendo desde su base y salen hundiéndose.

    page(mundo_js, capas, S0, dur)  → HTML opaco 1080×1920 (contrato __seek / __listo de capturar.ts)
    placa(t0, t1, x, y, w, html)     → placa en pantalla       pin(t0, t1, p, html) → etiqueta con línea a un punto 3D
    N(keys)                          → contador animado (keys = [[t, valor], [t, valor, dur], …])
    subtitulos(G, dur)               → capa transparente de subtítulos (grupos de cli/subtitulos.py)
"""
import html as _html
import json, os

AQUI = os.path.dirname(os.path.abspath(__file__))
THREE = 'https://cdn.jsdelivr.net/npm/three@0.170.0'
RUNTIME = open(os.path.join(AQUI, 'maqueta.js')).read()
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Manrope:wght@600;800&display=block" rel="stylesheet">')
PR = 1.5  # densidad de píxeles del 3D: 1.5 se ve nítido a 1080 y cuesta la mitad que 2

TINTA, ROJO, VERDE, OCRE, PIZARRA, HUESO = '#22252b', '#d9483b', '#3f8f5a', '#d9a441', '#4b6a88', '#f6f3ec'

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:transparent;font-family:Manrope,sans-serif;color:#22252b;-webkit-font-smoothing:antialiased;font-synthesis:none}
.estudio{position:absolute;inset:0;overflow:hidden;background:radial-gradient(1300px 1700px at 50% 42%,#ece7de,#c9c2b6 70%,#b3ab9e)}
#c3{position:absolute;inset:0;z-index:2}
/* tilt-shift: bandas de desenfoque creciente arriba y abajo (el centro queda nítido) */
.ts{position:absolute;left:0;right:0;z-index:4;pointer-events:none}
.ts.a1{top:0;height:560px;backdrop-filter:blur(2.5px);-webkit-mask-image:linear-gradient(#000 40%,transparent)}
.ts.a2{top:0;height:330px;backdrop-filter:blur(6px);-webkit-mask-image:linear-gradient(#000 35%,transparent)}
.ts.b1{bottom:0;height:520px;backdrop-filter:blur(2.5px);-webkit-mask-image:linear-gradient(transparent,#000 60%)}
.ts.b2{bottom:0;height:300px;backdrop-filter:blur(6px);-webkit-mask-image:linear-gradient(transparent,#000 65%)}
.vin{position:absolute;inset:0;z-index:5;pointer-events:none;background:radial-gradient(1200px 1500px at 50% 45%,transparent 60%,rgba(60,50,40,.22))}
/* capa de texto */
.cp{position:absolute;z-index:10;visibility:hidden;will-change:transform,clip-path}
.placa{background:#f6f3ec;border-radius:10px;padding:26px 34px 28px;border:3px solid #22252b;
  box-shadow:0 10px 0 #22252b,0 26px 40px rgba(40,30,20,.22)}
.placa .et{font:800 26px/1 Manrope;letter-spacing:.16em;text-transform:uppercase;display:flex;align-items:center;gap:12px;color:#5a5d63}
.placa .et:before{content:'';width:18px;height:18px;background:var(--ac,#d9483b);display:inline-block}
.placa .gr{font:700 104px/1 'Space Grotesk';letter-spacing:-.03em;margin-top:14px}
.placa .md{font:700 62px/1.04 'Space Grotesk';letter-spacing:-.02em;margin-top:12px}
.placa .ch{font:600 34px/1.25 Manrope;margin-top:12px;color:#3c3f45}
.placa .cod{font:500 40px/1.3 'Space Grotesk';background:#22252b;color:#f6f3ec;border-radius:6px;padding:14px 20px;margin-top:14px}
.placa.osc{background:#22252b;color:#f6f3ec;border-color:#22252b;box-shadow:0 10px 0 #0e0f12,0 26px 40px rgba(40,30,20,.3)}
.placa.osc .et,.placa.osc .ch{color:#b9bcc2}
.ac{color:var(--ac,#d9483b)}
/* pin: punto en la maqueta + línea guía + etiqueta */
.pin{position:absolute;z-index:9;left:0;top:0;width:0;height:0;visibility:hidden}
.pin .pt{position:absolute;left:-13px;top:-13px;width:26px;height:26px;border-radius:50%;background:#f6f3ec;border:6px solid var(--ac,#22252b)}
.pin .ln{position:absolute;left:0;top:-2px;height:4px;background:#22252b;transform-origin:0 50%}
.pin .tx{position:absolute;white-space:nowrap;background:#22252b;color:#f6f3ec;font:700 36px/1 'Space Grotesk';padding:14px 20px;border-radius:8px;transform-origin:0 100%}
.pin .tx small{display:block;font:800 20px/1 Manrope;letter-spacing:.14em;text-transform:uppercase;color:#b9bcc2;margin-bottom:8px}
/* marca de la serie: etiqueta de lote de maqueta */
.marca{position:absolute;z-index:11;left:56px;top:92px;display:flex;align-items:stretch;border:3px solid #22252b;border-radius:8px;overflow:hidden;
  font:800 24px/1 Manrope;letter-spacing:.2em;box-shadow:0 6px 0 #22252b}
.marca b{background:#22252b;color:#f6f3ec;padding:12px 14px 10px}.marca i{font-style:normal;background:#f6f3ec;padding:12px 14px 10px}
"""

JS = r"""
const _eo=p=>1-Math.pow(1-p,3),_eio=p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2,_k=(t,a,d)=>Math.min(1,Math.max(0,(t-a)/d));
const _eb=p=>{const c=1.9,c3=c+1;return 1+c3*Math.pow(p-1,3)+c*Math.pow(p-1,2)};
const _v=(k,t)=>{let v=k[0][1];for(const [a,b,d] of k.slice(1)){const p=_k(t,a,d||.8);v=v+(b-v)*_eio(p)}return v};
const _f=(v,f)=>f==='c'?Math.round(v).toLocaleString('es-MX'):f==='1'?v.toFixed(1):Math.round(v);
const _N=[...document.querySelectorAll('[data-n]')].map(e=>[e,JSON.parse(e.dataset.n)]);
const _CP=[...document.querySelectorAll('.cp')].map(e=>[e,+e.dataset.a,+e.dataset.b]);
const _PIN=[...document.querySelectorAll('.pin')].map(e=>[e,+e.dataset.a,+e.dataset.b,JSON.parse(e.dataset.p),+e.dataset.dx,+e.dataset.dy]);
const _capas=t=>{
 for(const [e,k] of _N)e.textContent=(e.dataset.pre||'')+_f(_v(k,t),e.dataset.f)+(e.dataset.suf||'');
 // placas: suben desde su base al entrar y se hunden al salir
 for(const [e,a,b] of _CP){if(t<a||t>b+.4){e.style.visibility='hidden';continue}e.style.visibility='visible';
  const pi=_eo(_k(t,a,.42)),po=_eio(_k(t,b,.36)),q=1-pi+po;
  e.style.clipPath=`inset(-40px -60px calc(${q*100}% - ${40*(1-q)}px) -60px)`;e.style.transform=`translateY(${q*100}%) scale(${1+(.06*(1-_eb(Math.min(1,pi*1.2))))})`}
 for(const [e,a,b,p,dx,dy] of _PIN){if(t<a||t>b+.4||!window.__proy){e.style.visibility='hidden';continue}e.style.visibility='visible';
  const [x,y]=window.__proy(p);e.style.transform=`translate(${x}px,${y}px)`;
  const pt=e.children[0],ln=e.children[1],tx=e.children[2];
  // la etiqueta no sale de la zona segura (x 50–930, y 160–1300); la línea va a su esquina inferior izquierda
  const tw=tx.offsetWidth,th=tx.offsetHeight;let lx=Math.min(930-tw,Math.max(50,x+dx))-x,ly=Math.min(1300,Math.max(160+th,y+dy))-y;
  const ex=Math.min(Math.max(0,-lx),tw)+lx,L=Math.hypot(ex,ly);
  const pi=_k(t,a,.5),po=_eio(_k(t,b,.35)),pl=_eo(_k(pi,.15,.5))*(1-po);
  pt.style.transform=`scale(${Math.max(0,_eb(Math.min(1,pi/.4)))*(1-po)})`;
  ln.style.width=L+'px';ln.style.transform=`rotate(${Math.atan2(ly,ex)}rad) scaleX(${pl})`;
  const ps=_eb(_k(pi,.5,.5))*(1-po);tx.style.left=lx+'px';tx.style.top=(ly-th)+'px';
  tx.style.transform=`scale(${Math.max(0,ps)})`;}
};
window.__seek=s=>{const t=S0+s;window.__u3&&window.__u3(t);_capas(t)};
window.__listo=Promise.all(['700 100px "Space Grotesk"','800 100px Manrope','600 100px Manrope'].map(f=>document.fonts.load(f))).then(()=>document.fonts.ready)
 .then(()=>{const m=['700 100px "Space Grotesk"','800 100px Manrope'].filter(f=>!document.fonts.check(f));if(m.length)throw new Error('faltan fuentes: '+m)}).then(()=>window.__c3).then(()=>window.__seek(0));
"""


def placa(t0, t1, x, y, w, html, cls='', ac=ROJO, extra=''):
    """Placa de texto en pantalla (x, y = esquina superior izquierda en px). html usa .et (etiqueta), .gr/.md (cifra/titular), .ch (texto), .cod."""
    return (f'<div class="cp placa {cls}" data-a="{t0:.2f}" data-b="{t1:.2f}" '
            f'style="left:{x}px;top:{y}px;width:{w}px;--ac:{ac};{extra}">{html}</div>')


def pin(t0, t1, p, html, dx=110, dy=-120, ac=TINTA):
    """Etiqueta con línea guía clavada al punto 3D p = [x, y, z] (se reproyecta en cada cuadro, sigue a la cámara)."""
    return (f'<div class="pin" data-a="{t0:.2f}" data-b="{t1:.2f}" data-p="{json.dumps(p)}" data-dx="{dx}" data-dy="{dy}" style="--ac:{ac}">'
            f'<i class="pt"></i><i class="ln"></i><div class="tx">{html}</div></div>')


def et(txt):
    return f'<div class="et">{txt}</div>'


def N(keys, f='', suf='', pre=''):
    return (f"<b data-n='{json.dumps([list(k) for k in keys])}'" + (f' data-f="{f}"' if f else '') + (f' data-suf="{suf}"' if suf else '')
            + (f' data-pre="{pre}"' if pre else '') + ' style="font-weight:inherit">0</b>')


def page(mundo, capas, S0, dur, marca=('ARCHIVO', '#01'), css=''):
    """Página opaca: diorama 3D (mundo = cuerpo JS async (M, THREE) → update(t)) + tilt-shift + capa de placas/pins."""
    rt = RUNTIME.replace('__MUNDO__', mundo)
    tres = (f'<script>window.MAQ={{S0:{S0},PR:{PR}}};window.__c3=new Promise(r=>window.__c3ok=r);</script>'
            f'<script type="importmap">{{"imports":{{"three":"{THREE}/build/three.module.js","three/addons/":"{THREE}/examples/jsm/"}}}}</script>'
            f'<script type="module">{rt}</script>')
    mc = f'<div class="marca"><b>{marca[0]}</b><i>{marca[1]}</i></div>' if marca else ''
    return (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{CSS}{css}</style>{tres}</head><body>'
            f'<div class="estudio"><div id="c3"></div><i class="ts a1"></i><i class="ts a2"></i><i class="ts b1"></i><i class="ts b2"></i>'
            f'<i class="vin"></i>{mc}{"".join(capas)}</div><script>const S0={S0};{JS}</script></body></html>')


def subtitulos(G, dur, ocultar=(), top=1352):
    """Subtítulos como placa limpia: tarjeta hueso con borde de tinta; la palabra activa lleva un bloque de color debajo.
    Cada grupo entra subiendo desde su base (sin desvanecido). ocultar = [[a, b]] tramos sin subtítulos."""
    data = json.dumps([dict(i=round(g['ini'], 2), f=round(g['fin'], 2), w=[[_html.escape(w), round(a, 2), round(b, 2)] for w, a, b in g['w']]) for g in G],
                      ensure_ascii=False)
    css = ("*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1920px;overflow:hidden;background:transparent}"
           f"#s{{position:absolute;left:70px;right:150px;top:{top}px;height:150px;display:flex;align-items:flex-end;justify-content:center}}"
           "#s .l{display:inline-block;background:#f6f3ec;border:3px solid #22252b;border-radius:10px;padding:14px 26px 18px;box-shadow:0 8px 0 #22252b;"
           "font:700 62px/1.08 'Space Grotesk',sans-serif;letter-spacing:-.015em;color:#22252b;text-align:center;transform-origin:50% 100%}"
           "#s i{font-style:normal;padding:0 .06em;background:linear-gradient(transparent 72%,var(--c,transparent) 72%)}#s i.on{--c:#e8b84a}")
    js = (f"const G={data},O={json.dumps(list(ocultar))};const el=document.getElementById('s');"
          "const eb=p=>{const c=1.9,c3=c+1;return 1+c3*Math.pow(p-1,3)+c*Math.pow(p-1,2)};"
          "window.__seek=s=>{if(O.some(([a,b])=>s>=a&&s<b)){el.innerHTML='';return}"
          "const k=G.findIndex(g=>s>=g.i&&s<g.f);if(k<0){el.innerHTML='';return}"
          "const g=G[k];let on=-1;g.w.forEach(([w,a],j)=>{if(s>=a-.05)on=j});"
          "const p=Math.min(1,(s-g.i)/.22);const sy=Math.max(.02,eb(p));"
          "el.innerHTML=`<span class=l style=\"transform:scaleY(${sy})\">`+g.w.map(([w],j)=>`<i class=\"${j===on?'on':''}\">${w}</i>`).join(' ')+'</span>'};"
          "window.__listo=document.fonts.load(\"700 62px 'Space Grotesk'\").then(()=>document.fonts.ready).then(()=>{if(!document.fonts.check(\"700 62px 'Space Grotesk'\"))throw new Error('falta Space Grotesk')});window.__seek(0);")
    return (f"<!doctype html><html><head><meta charset=utf-8><link href=\"https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&display=block\" rel=stylesheet>"
            f"<style>{css}</style></head><body><div id=s></div><script>{js}</script></body></html>")
