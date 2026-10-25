"""Estilo «Bauhaus»: geométrico y plano. Primarios (rojo, amarillo, azul) + negro sobre crema, retícula visible,
tipografía geométrica (Jost, tipo Futura). Las formas puras (círculo, medio círculo, cuarto, cuadrado, triángulo, barra)
entran deslizándose y ENCAJAN en la retícula con un pequeño rebote; los textos se revelan con una barra de color que
barre y se retira. Entre escenas, un círculo gigante del color del siguiente capítulo crece desde una esquina.
Nada se desvanece ni lleva textura: bordes duros, color plano.

Tiempos: segundos del video final; A(t) = retardo local.
"""
import json, math

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600;700;800;900'
         '&family=JetBrains+Mono:wght@500;700&display=block" rel="stylesheet">')
COLA = 0.7
COL = {'crema': '#efe8da', 'rojo': '#e2352b', 'amarillo': '#f3c11b', 'azul': '#1f4fd6', 'negro': '#151515', 'blanco': '#faf7f0', 'gris': '#c9c2b4'}

BASE = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:transparent;font-family:'Jost',sans-serif;color:#151515;-webkit-font-smoothing:antialiased;font-synthesis:none}
.lz{position:absolute;inset:0;overflow:hidden;background:var(--fondo,#efe8da)}
.rj{position:absolute;inset:0;pointer-events:none;z-index:1;
  background-image:linear-gradient(var(--lin,rgba(21,21,21,.10)) 2px,transparent 2px),linear-gradient(90deg,var(--lin,rgba(21,21,21,.10)) 2px,transparent 2px);
  background-size:180px 180px;background-position:90px 60px}
.fm{position:absolute;z-index:5}
.fm.c{border-radius:50%}
.fm.sx{animation:entra var(--dur,.7s) cubic-bezier(.3,1.35,.45,1) var(--d) both}
.fm.sx.x{animation:entra var(--dur,.7s) cubic-bezier(.3,1.35,.45,1) var(--d) both,sale .5s cubic-bezier(.7,0,.9,.4) var(--x) forwards}
@keyframes entra{from{transform:translate(var(--fx,0),var(--fy,0)) rotate(var(--fr,0deg)) scale(var(--fs,1))}to{transform:none}}
@keyframes sale{to{transform:translate(var(--sx,0),var(--sy,0)) rotate(var(--sr,0deg)) scale(var(--ss,1))}}
.gira{animation:gira var(--gp,8s) linear infinite}@keyframes gira{to{transform:rotate(360deg)}}
/* texto: barra que barre y revela */
.tx{position:absolute;z-index:20;font-weight:800;line-height:.95;letter-spacing:-.025em}
.tx .ln{position:relative;display:block;width:max-content;max-width:100%;white-space:nowrap}
.tx .ln .t{display:inline-block;clip-path:inset(0 100% 0 0);animation:rev .01s steps(1) var(--m) forwards}
.tx .ln:after{content:'';position:absolute;left:-.08em;top:.06em;bottom:.02em;width:calc(100% + .16em);background:var(--bar,#151515);transform-origin:left;transform:scaleX(0);
  animation:bar .62s cubic-bezier(.7,0,.25,1) var(--d) forwards}
@keyframes bar{0%{transform:scaleX(0);transform-origin:left}49.9%{transform:scaleX(1);transform-origin:left}50%{transform:scaleX(1);transform-origin:right}100%{transform:scaleX(0);transform-origin:right}}
@keyframes rev{to{clip-path:inset(0 -10% 0 0)}}
.tx.x .ln{animation:txs .45s cubic-bezier(.7,0,.9,.4) var(--x) forwards}
@keyframes txs{to{clip-path:inset(0 0 0 100%)}}
.tx .ac{color:var(--ac,#e2352b)}.tx .hl{background:var(--hl,#f3c11b);padding:0 .08em}
.num{position:absolute;z-index:18;font-weight:900;line-height:.82;letter-spacing:-.05em;font-variant-numeric:tabular-nums}
.et{position:absolute;z-index:22;font-weight:700;font-size:34px;letter-spacing:.08em;text-transform:uppercase;padding:10px 22px;white-space:nowrap;background:#151515;color:#efe8da;
  clip-path:inset(0 100% 0 0);animation:rev .4s steps(8) var(--d) forwards}
.mono{font-family:'JetBrains Mono',monospace}
.ap{position:absolute;inset:0;z-index:12;pointer-events:none;opacity:0;animation:apo .01s steps(1) var(--d) forwards}.ap.x{animation:apo .01s steps(1) var(--d) forwards,apc .01s steps(1) var(--x) forwards}
@keyframes apo{to{opacity:1}}@keyframes apc{to{opacity:0}}
.lin{position:absolute;z-index:6;background:#151515;transform-origin:left center;transform:scaleX(0);animation:linea .6s cubic-bezier(.7,0,.25,1) var(--d) forwards}
@keyframes linea{to{transform:scaleX(1)}}
"""

JS = """const _e=p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2;
const _v=(k,t)=>{let v=k[0][1];for(const [a,b,d] of k.slice(1)){const p=Math.min(1,Math.max(0,(t-a)/(d||.8)));v=v+(b-v)*_e(p)}return v};
const _f=(v,f)=>f==='c'?Math.round(v).toLocaleString('en-US'):f==='1'?v.toFixed(1):f==='p'?Math.round(v)+'%':Math.round(v);
const _N=[...document.querySelectorAll('[data-n]')].map(e=>[e,JSON.parse(e.dataset.n)]);
window.__seek=s=>{const t=s+S0;for(const [e,k] of _N)e.textContent=(e.dataset.pre||'')+_f(_v(k,t),e.dataset.f)+(e.dataset.suf||'')};
const _F=['800 100px Jost','500 100px "JetBrains Mono"'];
window.__listo=Promise.all(_F.map(f=>document.fonts.load(f))).then(()=>document.fonts.ready).then(()=>{const m=_F.filter(f=>!document.fonts.check(f));if(m.length)throw new Error('faltan fuentes: '+m)});
window.__seek(0);"""


def at(start):
    return lambda t: f'{max(0.0, t - start):.2f}s'


DESDE = {'izq': ('-1300px', '0'), 'der': ('1300px', '0'), 'arriba': ('0', '-2100px'), 'abajo': ('0', '2100px')}


def forma(tipo, x, y, w, h, color, A, t, desde='izq', sale=None, hacia='izq', rot=0, gira=False, z=5, extra='', dur=.7, escala=False):
    """tipo: c (círculo) | sq | medio (media luna: rot 0 = plana abajo) | cuarto | tri | barra | anillo.
    Entra deslizándose desde un lado (o escala desde 0 si escala=True) y encaja; sale hacia otro lado."""
    fx, fy = DESDE.get(desde, ('0', '0'))
    sx, sy = DESDE.get(hacia, ('0', '0'))
    st = f'left:{x}px;top:{y}px;width:{w}px;height:{h}px;--d:{A(t)};--dur:{dur}s;z-index:{z};'
    st += f'--fs:0;' if escala else f'--fx:{fx};--fy:{fy};--fr:{-40 if desde in ("izq", "arriba") else 40}deg;'
    st += f'--sx:{sx};--sy:{sy};--sr:{30 if hacia in ("der", "abajo") else -30}deg;'
    cls = 'fm sx' + (' x' if sale is not None else '')
    if sale is not None:
        st += f'--x:{A(sale)};'
    inner_st = f'width:100%;height:100%;transform:rotate({rot}deg);'
    if tipo == 'c':
        inner = f'<div style="{inner_st}border-radius:50%;background:{color}"></div>'
    elif tipo == 'anillo':
        inner = f'<div style="{inner_st}border-radius:50%;border:{max(10, int(w * .14))}px solid {color}"></div>'
    elif tipo == 'sq' or tipo == 'barra':
        inner = f'<div style="{inner_st}background:{color}"></div>'
    elif tipo == 'medio':
        inner = f'<div style="{inner_st}background:{color};border-radius:{w}px {w}px 0 0"></div>'
    elif tipo == 'cuarto':
        inner = f'<div style="{inner_st}background:{color};border-radius:0 {w}px 0 0"></div>'
    elif tipo == 'tri':
        inner = f'<div style="{inner_st}background:{color};clip-path:polygon(50% 0,100% 100%,0 100%)"></div>'
    else:
        inner = f'<div style="{inner_st}background:{color}">{tipo}</div>'
    if gira:
        inner = f'<div class="gira" style="width:100%;height:100%">{inner}</div>'
    return f'<div class="{cls}" style="{st}{extra}">{inner}</div>'


def texto(lineas, A, t, x=70, y=300, size=120, sale=None, color=None, bar='#151515', step=.12, ancho=940, ac=None):
    """Líneas reveladas por una barra que barre (cada línea a `step`). [acento] = color de acento; {resalte} = fondo amarillo."""
    import re
    html = ''
    for i, ln in enumerate(lineas):
        d = t + i * step
        ln = re.sub(r'\[(.+?)\]', r'<span class="ac">\1</span>', ln)
        ln = re.sub(r'\{(.+?)\}', r'<span class="hl">\1</span>', ln)
        html += f'<span class="ln" style="--d:{A(d)};--m:{A(d + .31)}"><span class="t">{ln}</span></span>'
    st = f'left:{x}px;top:{y}px;width:{ancho}px;font-size:{size}px;--bar:{bar};' + (f'color:{color};' if color else '') + (f'--ac:{ac};' if ac else '')
    cls = 'tx'
    if sale is not None:
        cls += ' x'; st += f'--x:{A(sale)};'
    return f'<div class="{cls}" style="{st}">{html}</div>'


def N(keys, f='', suf='', pre=''):
    return (f"<b data-n='{json.dumps([list(k) for k in keys])}'" + (f' data-f="{f}"' if f else '') + (f' data-suf="{suf}"' if suf else '')
            + (f' data-pre="{pre}"' if pre else '') + ' style="font-weight:inherit">0</b>')


def numero(html, x, y, size, A, t, color='#151515', sale=None):
    return ap(f'<div class="num" style="left:{x}px;top:{y}px;font-size:{size}px;color:{color}">{html}</div>', A, t, sale)


def etiqueta(txt, x, y, A, t, fondo='#151515', color='#efe8da', size=34):
    return f'<div class="et" style="left:{x}px;top:{y}px;--d:{A(t)};background:{fondo};color:{color};font-size:{size}px">{txt}</div>'


def linea(x, y, w, A, t, grosor=8, color='#151515', vertical=False):
    st = f'left:{x}px;top:{y}px;width:{w}px;height:{grosor}px;--d:{A(t)};background:{color};' + ('transform-origin:left;rotate:90deg;' if vertical else '')
    return f'<div class="lin" style="{st}"></div>'


def ap(html, A, t, sale=None, estilo=''):
    """Aparece de golpe. estilo = posición/z-index del propio contenedor (la opacidad crea contexto de apilamiento)."""
    cls, st = 'ap', f'--d:{A(t)};{estilo}'
    if sale is not None:
        cls += ' x'; st += f'--x:{A(sale)};'
    return f'<div class="{cls}" style="{st}">{html}</div>'


ESQ = {'si': (0, 0), 'sd': (1080, 0), 'ii': (0, 1920), 'id': (1080, 1920), 'c': (540, 960)}


def page(css, body, dur, S0=0.0, fondo='#efe8da', entra='sd', reticula=True, lineas='rgba(21,21,21,.10)', transparente=False):
    """Escena plana. entra = esquina desde donde crece el círculo del nuevo color (si, sd, ii, id, c) o None."""
    if transparente:
        inner = f'<div style="position:absolute;inset:0">{body}</div>'
    else:
        anim = ''
        if entra:
            cx, cy = ESQ[entra]
            css += (f'@keyframes ci{{from{{clip-path:circle(0px at {cx}px {cy}px)}}to{{clip-path:circle(2300px at {cx}px {cy}px)}}}}'
                    f'.lz{{animation:ci .7s cubic-bezier(.7,0,.25,1) both}}')
        inner = f'<div class="lz" style="--fondo:{fondo};--lin:{lineas}">{"<div class=rj></div>" if reticula else ""}{body}</div>'
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{BASE}{css}</style></head><body>{inner}
<script>const S0={S0};{JS}</script></body></html>"""
