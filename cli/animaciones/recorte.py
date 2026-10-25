"""Estilo «Recorte»: collage editorial + tipografía cinética (referencias 2026: el texto ES la animación,
papel/grano/cinta/marcador en vez de brillo, explicadores tipo Vox con el movimiento a 12 cps).

Lienzos: papel crema, papel negro (noticia urgente) y cuadrícula de ingeniería (tecnología). Piezas: titulares que
golpean palabra por palabra, marcatextos, garabatos que se dibujan (círculo, subrayado, tachón, flecha), recortes
de papel rasgado con cinta, notas adhesivas, sellos de goma, tickets de terminal, números gigantes y calcomanías
con logos. Entre escenas la hoja nueva entra rasgada desde la derecha. Todo se cuantiza a 12 cuadros por segundo.

Tiempos: todo en segundos del video final; cada escena convierte con A(t) = retardo local.
"""
import json, math, os, random, re
import ellog_gloss as G

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900'
         '&family=Instrument+Serif:ital@0;1&family=Caveat:wght@600;700&family=JetBrains+Mono:wght@500;700&display=block" rel="stylesheet">')
COLA = 0.7          # la hoja vieja se queda debajo mientras la nueva entra rasgada
CPS = 12            # cuadros por segundo del movimiento (efecto hecho a mano)

COL = {'papel': '#efe8da', 'tinta': '#171513', 'rojo': '#e3342a', 'amarillo': '#ffe14a', 'azul': '#2457e6',
       'verde': '#17a35a', 'naranja': '#ff6a1f', 'kraft': '#c9a26b', 'rosa': '#ff8fb1', 'lila': '#8c7cf0'}

RUIDO = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' "
         "baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .1 0 0 0 0 .08 0 0 0 0 .06 0 0 0 .55 0'/%3E%3C/filter%3E"
         "%3Crect width='300' height='300' filter='url(%23n)'/%3E%3C/svg%3E")
FIBRA = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='600' height='600'%3E%3Cfilter id='f'%3E%3CfeTurbulence type='fractalNoise' "
         "baseFrequency='.012 .09' numOctaves='2' seed='4'/%3E%3CfeColorMatrix values='0 0 0 0 .3 0 0 0 0 .25 0 0 0 0 .2 0 0 0 .22 0'/%3E%3C/filter%3E"
         "%3Crect width='600' height='600' filter='url(%23f)'/%3E%3C/svg%3E")
SUCIO = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='200'%3E%3Cfilter id='s'%3E%3CfeTurbulence type='fractalNoise' "
         "baseFrequency='.9' numOctaves='2' seed='7'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -2.6 1.9'/%3E%3C/filter%3E"
         "%3Crect width='400' height='200' filter='url(%23s)'/%3E%3C/svg%3E")

BASE = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:transparent;font-family:'Archivo',sans-serif;color:var(--tinta);-webkit-font-smoothing:antialiased}
:root{--papel:#f3ecdf;--tinta:#171513;--rojo:#e3342a;--amarillo:#ffe14a;--azul:#2457e6;--verde:#17a35a;--naranja:#ff6a1f;--ac:var(--rojo)}
.hoja{position:absolute;inset:0;overflow:hidden;background:var(--papel)}
.hoja:before{content:'';position:absolute;inset:0;background:url("FIBRA");opacity:.45;pointer-events:none}
.hoja:after{content:'';position:absolute;inset:0;pointer-events:none;background:radial-gradient(120% 80% at 50% 40%,transparent 55%,rgba(60,40,20,.18))}
.hoja.negra{background:#151413;color:#f3eee4}.hoja.negra:before{opacity:.35;mix-blend-mode:screen}
.hoja.cuad{background-color:#f2f0ea;background-image:linear-gradient(rgba(36,87,230,.16) 2px,transparent 2px),linear-gradient(90deg,rgba(36,87,230,.16) 2px,transparent 2px),
  linear-gradient(rgba(36,87,230,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(36,87,230,.07) 1px,transparent 1px);background-size:120px 120px,120px 120px,24px 24px,24px 24px;background-position:-2px -2px}
.grano{position:absolute;inset:-60px;pointer-events:none;z-index:80;background:url("RUIDO");mix-blend-mode:multiply;opacity:.32;animation:boil .5s steps(1) infinite}
.negra .grano{mix-blend-mode:screen;opacity:.25}
@keyframes boil{0%{transform:translate(0,0)}25%{transform:translate(-17px,9px)}50%{transform:translate(11px,-13px)}75%{transform:translate(-7px,-8px)}}
.L{position:absolute}
/* titulares cinéticos */
.tt{position:absolute;left:60px;right:60px;z-index:20;font-weight:900;font-stretch:62%;text-transform:uppercase;line-height:.86;letter-spacing:-.005em}
.tt .ln{display:block;white-space:nowrap}
.tt .w{display:inline-block;margin-right:.18em;animation:slam .42s cubic-bezier(.2,1.6,.4,1) var(--d) both}
.tt .w.x{animation:slam .42s cubic-bezier(.2,1.6,.4,1) var(--d) both,fuera .34s cubic-bezier(.6,0,.9,.4) var(--x) forwards}
.tt .sf{font-family:'Instrument Serif',serif;font-style:italic;font-weight:400;font-stretch:100%;text-transform:none;letter-spacing:-.02em;color:var(--ac);font-size:1.08em;line-height:.8}
.negra .tt .sf{color:var(--ac2,var(--amarillo))}
@keyframes slam{from{opacity:0;transform:translateY(.45em) scale(1.5) rotate(var(--r,-4deg))}40%{opacity:1}to{opacity:1;transform:none}}
@keyframes fuera{to{opacity:0;transform:translateY(-.6em) rotate(var(--r2,6deg)) scale(.9)}}
/* marcatextos */
.mk{position:relative;z-index:0;white-space:nowrap}
.mk:before{content:'';position:absolute;left:-.1em;right:-.1em;top:.12em;bottom:-.02em;z-index:-1;background:var(--mk,var(--amarillo));border-radius:6px 14px 8px 16px;
  transform-origin:left center;transform:skewX(-8deg) rotate(-1.5deg) scaleX(0);animation:mk .45s cubic-bezier(.5,0,.3,1) var(--m) forwards;mix-blend-mode:multiply}
.negra .mk:before{mix-blend-mode:normal}.negra .mk{color:var(--tinta)}
@keyframes mk{to{transform:skewX(-8deg) rotate(-1.5deg) scaleX(1)}}
/* garabatos */
.gb{position:absolute;overflow:visible;pointer-events:none;z-index:30}
.gb path{fill:none;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;animation:draw var(--dd,.5s) cubic-bezier(.5,0,.4,1) var(--d) forwards}
@keyframes draw{to{stroke-dashoffset:0}}
/* recorte de papel rasgado */
.rcw{position:absolute;z-index:15;filter:drop-shadow(0 5px 0 rgba(0,0,0,.18)) drop-shadow(0 22px 22px rgba(0,0,0,.28));animation:cae .5s cubic-bezier(.2,1.4,.4,1) var(--d) both}
.rcw.x{animation:cae .5s cubic-bezier(.2,1.4,.4,1) var(--d) both,vuela .45s cubic-bezier(.6,0,.9,.4) var(--x) forwards}
.rc{background:#fbf8f1;padding:34px 40px;color:var(--tinta)}
.rc.crema{background:#f6efdf}.rc.negro{background:#1b1a18;color:#f3eee4}.rc.kraft{background:#cfab72}.rc.rojo{background:var(--rojo);color:#fff}
.rc.amarillo{background:var(--amarillo)}.rc.azul{background:var(--azul);color:#fff}
@keyframes cae{from{opacity:0;transform:translateY(-90px) rotate(calc(var(--r,0deg) - 10deg)) scale(1.12)}35%{opacity:1}to{opacity:1;transform:rotate(var(--r,0deg))}}
@keyframes vuela{to{opacity:0;transform:translate(var(--vx,-160px),420px) rotate(calc(var(--r,0deg) - 24deg))}}
.cinta{position:absolute;width:190px;height:54px;background:rgba(236,226,196,.82);z-index:3;box-shadow:0 2px 4px rgba(0,0,0,.12);
  clip-path:polygon(0 8%,5% 0,10% 9%,16% 1%,22% 8%,28% 0,34% 7%,40% 0,46% 9%,52% 1%,58% 8%,64% 0,70% 7%,76% 0,82% 9%,88% 0,94% 8%,100% 2%,100% 92%,95% 100%,89% 91%,83% 100%,77% 92%,71% 100%,65% 91%,59% 100%,53% 92%,47% 100%,41% 91%,35% 100%,29% 92%,23% 100%,17% 91%,11% 100%,5% 92%,0 100%)}
/* nota adhesiva */
.nt{position:absolute;z-index:16;width:var(--w,330px);min-height:var(--w,330px);padding:34px 30px;font-family:'Caveat',cursive;font-weight:700;font-size:54px;line-height:1.02;color:#2a2410;
  background:linear-gradient(170deg,var(--c,#ffe46b) 70%,color-mix(in srgb,var(--c,#ffe46b) 82%,#000));box-shadow:0 26px 30px -14px rgba(0,0,0,.45),inset 0 -20px 30px -20px rgba(0,0,0,.2);
  animation:cae .5s cubic-bezier(.2,1.4,.4,1) var(--d) both}
.nt.x{animation:cae .5s cubic-bezier(.2,1.4,.4,1) var(--d) both,vuela .45s cubic-bezier(.6,0,.9,.4) var(--x) forwards}
/* sello de goma */
.sl{position:absolute;z-index:40;padding:14px 30px;border:9px solid currentColor;border-radius:14px;font-weight:900;font-stretch:75%;text-transform:uppercase;letter-spacing:.04em;
  color:var(--rojo);-webkit-mask:url("SUCIO") 0 0/400px 200px;mask:url("SUCIO") 0 0/400px 200px;white-space:nowrap;animation:sello .32s cubic-bezier(.3,1.7,.5,1) var(--d) both}
@keyframes sello{from{opacity:0;transform:scale(2.6) rotate(calc(var(--r,-8deg) + 10deg))}60%{opacity:1}to{opacity:1;transform:rotate(var(--r,-8deg))}}
/* ticket de terminal */
.tk{position:absolute;z-index:15;background:#fbfaf5;font-family:'JetBrains Mono',monospace;font-size:34px;line-height:1.5;padding:30px 34px 46px;color:#1d1c1a;
  clip-path:polygon(0 0,100% 0,100% calc(100% - 16px),97% 100%,94% calc(100% - 16px),91% 100%,88% calc(100% - 16px),85% 100%,82% calc(100% - 16px),79% 100%,76% calc(100% - 16px),73% 100%,70% calc(100% - 16px),67% 100%,64% calc(100% - 16px),61% 100%,58% calc(100% - 16px),55% 100%,52% calc(100% - 16px),49% 100%,46% calc(100% - 16px),43% 100%,40% calc(100% - 16px),37% 100%,34% calc(100% - 16px),31% 100%,28% calc(100% - 16px),25% 100%,22% calc(100% - 16px),19% 100%,16% calc(100% - 16px),13% 100%,10% calc(100% - 16px),7% 100%,4% calc(100% - 16px),0 100%)}
.tkw{position:absolute;z-index:15;filter:drop-shadow(0 18px 18px rgba(0,0,0,.3));animation:cae .5s cubic-bezier(.2,1.4,.4,1) var(--d) both}
.tkw.x{animation:cae .5s cubic-bezier(.2,1.4,.4,1) var(--d) both,vuela .45s cubic-bezier(.6,0,.9,.4) var(--x) forwards}
.tk .ty{display:block;white-space:pre;clip-path:inset(0 100% 0 0);animation:tip var(--td,.8s) steps(var(--n,20)) var(--d) forwards}
.tk .ty b{color:var(--rojo);font-weight:700}.tk .ty i{font-style:normal;color:#8a8579}
@keyframes tip{to{clip-path:inset(0 0 0 0)}}
/* número gigante */
.nm{position:absolute;z-index:12;font-weight:900;font-stretch:62%;line-height:.8;letter-spacing:-.03em;font-variant-numeric:tabular-nums;animation:slam .5s cubic-bezier(.2,1.5,.4,1) var(--d) both}
.nm.out{color:transparent;-webkit-text-stroke:5px var(--tinta)}
/* calcomanía con logo */
.st{position:absolute;z-index:18;width:var(--s);height:var(--s);border-radius:50%;background:var(--bg,#fff);display:flex;align-items:center;justify-content:center;
  box-shadow:0 0 0 10px #fff,0 18px 24px rgba(0,0,0,.35);animation:pega .38s cubic-bezier(.3,1.6,.5,1) var(--d) both}
.st.x{animation:pega .38s cubic-bezier(.3,1.6,.5,1) var(--d) both,vuela .45s cubic-bezier(.6,0,.9,.4) var(--x) forwards}
.st svg{width:58%;height:58%}.st .em{font-size:calc(var(--s) * .5)}
@keyframes pega{from{opacity:0;transform:scale(1.9) rotate(calc(var(--r,0deg) - 25deg))}50%{opacity:1}to{opacity:1;transform:rotate(var(--r,0deg))}}
/* mano (anotaciones) */
.mano{position:absolute;z-index:31;font-family:'Caveat',cursive;font-weight:700;color:var(--rojo);white-space:nowrap;animation:slam .35s ease var(--d) both}
.mono{font-family:'JetBrains Mono',monospace}.ser{font-family:'Instrument Serif',serif;font-style:italic}
.fade0{animation:apar .01s linear var(--d) both}@keyframes apar{from{opacity:0}to{opacity:1}}
/* hoja nueva rasgada */
.borde{position:absolute;top:-20px;bottom:-20px;left:0;width:60px;z-index:99;pointer-events:none;background:#fbf8f1;filter:drop-shadow(-10px 0 14px rgba(0,0,0,.35))}
""".replace('FIBRA', FIBRA).replace('RUIDO', RUIDO).replace('SUCIO', SUCIO)

# cuantiza el tiempo a 12 cps y mueve contadores (data-n = claves [[t, v], [t, v, dur]] en segundos del video)
JS = """const _Q=1000/%d;window.__cps=1000/_Q;  // capturar.ts: los cuadros del mismo paso son idénticos
const _e=p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2;
const _v=(k,t)=>{let v=k[0][1];for(const [a,b,d] of k.slice(1)){const p=Math.min(1,Math.max(0,(t-a)/(d||.8)));v=v+(b-v)*_e(p)}return v};
const _f=(v,f)=>f==='c'?Math.round(v).toLocaleString('en-US'):f==='1'?v.toFixed(1):f==='p'?Math.round(v)+'%%':Math.round(v);
const _N=[...document.querySelectorAll('[data-n]')].map(e=>[e,JSON.parse(e.dataset.n)]);
window.__seek=s=>{const ms=Math.floor(s*1000/_Q+1e-6)*_Q;for(const a of document.getAnimations()){a.pause();a.currentTime=ms}
 const t=ms/1000+S0;for(const [e,k] of _N)e.textContent=(e.dataset.pre||'')+_f(_v(k,t),e.dataset.f)+(e.dataset.suf||'');window.__u3&&window.__u3(t)};
// espera las cuatro fuentes y truena si no cargaron (mejor una captura fallida que una con letra equivocada)
const _F=['900 100px Archivo','400 100px "Instrument Serif"','700 100px Caveat','500 100px "JetBrains Mono"'];
window.__listo=Promise.all(_F.map(f=>document.fonts.load(f))).then(()=>document.fonts.ready).then(()=>{const m=_F.filter(f=>!document.fonts.check(f));if(m.length)throw new Error('faltan fuentes: '+m)}).then(()=>window.__p3);
window.__seek(0);""" % CPS


def at(start):
    return lambda t: f'{max(0.0, t - start):.2f}s'


def _rnd(seed):
    return random.Random(seed)


def _palabras(html):
    """Parte una línea en palabras respetando *serif*, _marcatextos_ y etiquetas <..> sueltas."""
    out, buf, i = [], '', 0
    while i < len(html):
        ch = html[i]
        if ch == '<':
            j = html.index('>', i)
            buf += html[i:j + 1]; i = j + 1; continue
        if ch == ' ':
            if buf:
                out.append(buf)
            buf = ''
        else:
            buf += ch
        i += 1
    if buf:
        out.append(buf)
    return out


def titular(lineas, A, t, x=None, top=300, size=150, align='left', seed=1, step=.075, color=None, extra=''):
    """Titular que golpea palabra por palabra. lineas = ['DOS FALLOS', '*críticos*'] (*serif de acento*, _marcatextos_).
    t = entra (s del video); x = sale (o None)."""
    r = _rnd(seed)
    html, k = '', 0
    # *varias palabras* / _varias palabras_ → cada palabra lleva su marca
    lineas = [re.sub(r'([*_])([^*_]+?)\1', lambda m_: ' '.join(f'{m_.group(1)}{w}{m_.group(1)}' for w in m_.group(2).split(' ')), ln) for ln in lineas]
    for ln in lineas:
        ws = []
        for w in _palabras(ln):
            cls = 'w'
            inner = re.sub(r'\*(.+?)\*', r'<span class="sf">\1</span>', w)
            inner = re.sub(r'_(.+?)_', lambda m_: f'<span class="mk" style="--m:{A(t + .35 + k * step)}">{m_.group(1)}</span>', inner)
            st = f'--d:{A(t + k * step)};--r:{r.uniform(-6, 6):.1f}deg;--r2:{r.uniform(-10, 10):.1f}deg'
            if x is not None:
                cls += ' x'; st += f';--x:{A(x + k * .03)}'
            ws.append(f'<span class="{cls}" style="{st}">{inner}</span>')
            k += 1
        html += f'<span class="ln">{"".join(ws)}</span>'
    col = f'color:{color};' if color else ''
    return f'<div class="tt" style="top:{top}px;font-size:{size}px;text-align:{align};{col}{extra}">{html}</div>'


def marca(txt, A, t, color=None):
    c = f'--mk:{color};' if color else ''
    return f'<span class="mk" style="{c}--m:{A(t)}">{txt}</span>'


def _jit(r, a):
    return r.uniform(-a, a)


def circulo(cx, cy, w, h, A, t, color='var(--rojo)', grosor=9, seed=3, dur=.55):
    r = _rnd(seed)
    pts = []
    for i in range(15):
        a = -1.9 + i / 14 * (2 * math.pi + .55)
        k = 1 + _jit(r, .035) + i * .005
        pts.append((cx + w / 2 * k * math.cos(a), cy + h / 2 * k * math.sin(a)))
    d = f'M{pts[0][0]:.0f} {pts[0][1]:.0f}'
    for i in range(1, len(pts) - 1):
        mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
        d += f' Q{pts[i][0]:.0f} {pts[i][1]:.0f} {mx:.0f} {my:.0f}'
    return (f'<svg class="gb" style="left:0;top:0;width:1080px;height:1920px;--d:{A(t)};--dd:{dur}s" viewBox="0 0 1080 1920">'
            f'<path d="{d}" pathLength="1" stroke="{color}" stroke-width="{grosor}"/></svg>')


def subraya(x, y, w, A, t, color='var(--rojo)', grosor=10, seed=5, doble=False):
    r = _rnd(seed)
    d = f'M{x} {y + _jit(r, 4):.0f} C{x + w * .3:.0f} {y + _jit(r, 9):.0f},{x + w * .7:.0f} {y + _jit(r, 9):.0f},{x + w} {y + _jit(r, 6):.0f}'
    if doble:
        d += f' M{x + w * .08:.0f} {y + 22 + _jit(r, 4):.0f} C{x + w * .4:.0f} {y + 18 + _jit(r, 8):.0f},{x + w * .7:.0f} {y + 26:.0f},{x + w * .95:.0f} {y + 20:.0f}'
    return (f'<svg class="gb" style="left:0;top:0;width:1080px;height:1920px;--d:{A(t)};--dd:.4s" viewBox="0 0 1080 1920">'
            f'<path d="{d}" pathLength="1" stroke="{color}" stroke-width="{grosor}"/></svg>')


def tacha(x, y, w, A, t, color='var(--rojo)', grosor=14, seed=6):
    r = _rnd(seed)
    d = f'M{x} {y + _jit(r, 6):.0f} L{x + w} {y - 24 + _jit(r, 6):.0f} M{x + 10} {y - 30:.0f} L{x + w - 6} {y + 6:.0f}'
    return (f'<svg class="gb" style="left:0;top:0;width:1080px;height:1920px;--d:{A(t)};--dd:.45s" viewBox="0 0 1080 1920">'
            f'<path d="{d}" pathLength="1" stroke="{color}" stroke-width="{grosor}"/></svg>')


def flecha(x1, y1, x2, y2, A, t, color='var(--rojo)', curva=.25, grosor=9):
    import math
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    cx, cy = mx - dy * curva, my + dx * curva
    ang = math.atan2(y2 - cy, x2 - cx)
    a1, a2 = ang + 2.6, ang - 2.6
    h = 38
    d = (f'M{x1} {y1} Q{cx:.0f} {cy:.0f} {x2} {y2} M{x2 + h * math.cos(a1):.0f} {y2 + h * math.sin(a1):.0f} L{x2} {y2} '
         f'L{x2 + h * math.cos(a2):.0f} {y2 + h * math.sin(a2):.0f}')
    return (f'<svg class="gb" style="left:0;top:0;width:1080px;height:1920px;--d:{A(t)};--dd:.5s" viewBox="0 0 1080 1920">'
            f'<path d="{d}" pathLength="1" stroke="{color}" stroke-width="{grosor}"/></svg>')


def _rasgado(w, h, seed, a=10, n=14):
    """clip-path con los cuatro bordes rasgados."""
    r = _rnd(seed)
    p = []
    for i in range(n + 1):
        p.append((i / n * w, _jit(r, a) + a))
    for i in range(1, n + 1):
        p.append((w - a - _jit(r, a), i / n * h))
    for i in range(n - 1, -1, -1):
        p.append((i / n * w, h - a - _jit(r, a)))
    for i in range(n - 1, 0, -1):
        p.append((a + _jit(r, a), i / n * h))
    return 'polygon(' + ','.join(f'{x:.0f}px {y:.0f}px' for x, y in p) + ')'


def recorte(x, y, w, h, html, A, t, sale=None, rot=0.0, cls='', seed=11, cinta=True, z=15, pad=None, vx=-160):
    st = f'left:{x}px;top:{y}px;width:{w}px;height:{h}px;--r:{rot}deg;--d:{A(t)};--vx:{vx}px;z-index:{z}'
    if sale is not None:
        st += f';--x:{A(sale)}'
    cin = ''
    if cinta:
        r = _rnd(seed)
        cin = f'<div class="cinta" style="left:{w / 2 - 95 + _jit(r, 60):.0f}px;top:-26px;transform:rotate({_jit(r, 7):.1f}deg)"></div>'
    p = f'padding:{pad};' if pad else ''
    return (f'<div class="rcw{" x" if sale is not None else ""}" style="{st}"><div class="rc {cls}" style="width:100%;height:100%;{p}clip-path:{_rasgado(w, h, seed)}">'
            f'{html}</div>{cin}</div>')


def nota(x, y, html, A, t, sale=None, rot=-3.0, w=330, color='#ffe46b', size=54, z=16):
    st = f'left:{x}px;top:{y}px;--w:{w}px;--r:{rot}deg;--d:{A(t)};--c:{color};font-size:{size}px;z-index:{z}'
    if sale is not None:
        st += f';--x:{A(sale)}'
    return f'<div class="nt{" x" if sale is not None else ""}" style="{st}">{html}</div>'


def sello(x, y, txt, A, t, rot=-8.0, size=64, color=None):
    c = f'color:{color};' if color else ''
    return f'<div class="sl" style="left:{x}px;top:{y}px;font-size:{size}px;--r:{rot}deg;--d:{A(t)};{c}">{txt}</div>'


def ticket(x, y, w, lineas, A, rot=0.0, sale=None, size=34):
    """lineas = [(texto, t, dur_tecleo)] — se teclean una por una."""
    ls = ''.join(f'<span class="ty" style="--d:{A(t)};--td:{dt}s;--n:{max(4, len(_txt(tx)))}">{tx}</span>' for tx, t, dt in lineas)
    st = f'left:{x}px;top:{y}px;width:{w}px;--r:{rot}deg;--d:{A(lineas[0][1] - .3)}'
    if sale is not None:
        st += f';--x:{A(sale)}'
    return f'<div class="tkw{" x" if sale is not None else ""}" style="{st}"><div class="tk" style="font-size:{size}px;transform:rotate({rot}deg)">{ls}</div></div>'


def _txt(h):
    import re
    return re.sub(r'<[^>]+>', '', h)


def numero(x, y, html, A, t, size=420, cls='', color=None, extra=''):
    c = f'color:{color};' if color else ''
    return f'<div class="nm {cls}" style="left:{x}px;top:{y}px;font-size:{size}px;--d:{A(t)};{c}{extra}">{html}</div>'


def N(keys, f='', suf='', pre=''):
    return (f"<b data-n='{json.dumps([list(k) for k in keys])}'" + (f' data-f="{f}"' if f else '') + (f' data-suf="{suf}"' if suf else '')
            + (f' data-pre="{pre}"' if pre else '') + ' style="font-weight:inherit">0</b>')


def logo(name, x, y, s, A, t, sale=None, rot=0.0, bg='#fff', color='#171513', emoji=None):
    inner = f'<span class="em">{emoji}</span>' if emoji else G.logo(name, color)
    st = f'left:{x}px;top:{y}px;--s:{s}px;--bg:{bg};--r:{rot}deg;--d:{A(t)}'
    if sale is not None:
        st += f';--x:{A(sale)}'
    return f'<div class="st{" x" if sale is not None else ""}" style="{st}">{inner}</div>'


def mano(x, y, txt, A, t, size=58, color=None, rot=-4.0):
    c = f'color:{color};' if color else ''
    return f'<div class="mano" style="left:{x}px;top:{y}px;font-size:{size}px;transform:rotate({rot}deg);--d:{A(t)};{c}">{txt}</div>'


def sale(html_list):
    return ''.join(html_list)


def _borde(seed):
    r = _rnd(seed)
    n = 40
    izq = [(18 + _jit(r, 16), i / n * 1960) for i in range(n + 1)]
    pts = [(x, y) for x, y in izq] + [(60, 1960), (60, 0)]
    return 'polygon(' + ','.join(f'{x:.0f}px {y:.0f}px' for x, y in pts) + ')', izq


def page(css, body, dur, S0=0.0, fondo='papel', entra=True, seed=1, ac='var(--rojo)', ac2=None, transparente=False, js3d=None):
    """Escena. fondo: papel | negra | cuad. entra=True → la hoja llega rasgada desde la derecha (0.6 s)."""
    cls = 'hoja ' + ('' if fondo == 'papel' else fondo)
    rasgo = ''
    if entra and not transparente:
        clip, izq = _borde(seed)
        def pol(X):
            return 'polygon(' + ','.join(f'{X + x:.0f}px {y:.0f}px' for x, y in izq) + f',1200px 1960px,1200px -40px)'
        css += (f'@keyframes rasga{{from{{clip-path:{pol(1140)}}}to{{clip-path:{pol(-80)}}}}}'
                f'.hoja{{animation:rasga .6s cubic-bezier(.6,0,.25,1) both}}'
                f'@keyframes rasgaB{{from{{transform:translateX(1140px)}}to{{transform:translateX(-80px)}}}}'
                f'.borde{{clip-path:{clip};animation:rasgaB .6s cubic-bezier(.6,0,.25,1) both}}')
        rasgo = '<div class="borde"></div>'
    v = f'--ac:{ac};' + (f'--ac2:{ac2};' if ac2 else '')
    tres = ''
    if js3d:
        body = '<div id="p3"></div>' + body
        tres = (f'<script>window.__p3=new Promise(r=>window.__p3ok=r);</script><script type="importmap">{{"imports":{{"three":"{G.THREE}/build/three.module.js",'
                f'"three/addons/":"{G.THREE}/examples/jsm/"}}}}</script><script type="module">{RT3D.replace("SOMBRA_PISO", "false" if transparente else "true")}\n'
                f'const update=await (async(P,THREE)=>{{{js3d}}})(P,THREE);window.__u3=t=>{{if(window.__perdido||ren.getContext().isContextLost())throw new Error("contexto WebGL perdido");P.fx0();update(t);ren.render(scene,cam)}};window.__u3({S0});window.__p3ok();</script>')
    if transparente:
        inner = f'<div class="L" style="inset:0;{v}">{body}</div>'
    else:
        inner = f'<div class="{cls}" style="{v}">{body}<div class="grano"></div></div>{rasgo}'
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{BASE}{css}</style>{tres}</head><body>{inner}
<script>const S0={S0};{JS}</script></body></html>"""


FASE_CSS = """
.fz{position:absolute;inset:0;z-index:10}
.fz.x{animation:barre .5s cubic-bezier(.6,0,.9,.4) var(--x) forwards}
@keyframes barre{to{transform:translate(-1250px,260px) rotate(-14deg)}}
.fz.in{animation:apar .01s linear var(--d) both}
.fz.in.x{animation:apar .01s linear var(--d) both,barre .5s cubic-bezier(.6,0,.9,.4) var(--x) forwards}
"""


def fase(html, A, entra=None, sale=None):
    """Grupo de piezas; al salir se barre de la mesa hacia la izquierda (como papeles que se apartan)."""
    cls, st = 'fz', ''
    if entra is not None:
        cls += ' in'; st += f'--d:{A(entra)};'
    if sale is not None:
        cls += ' x'; st += f'--x:{A(sale)};'
    return f'<div class="{cls}" style="{st}">{html}</div>'


def palomita(x, y, s, A, t, color='var(--verde)', grosor=16):
    d = f'M{x} {y + s * .55:.0f} L{x + s * .38:.0f} {y + s:.0f} L{x + s} {y}'
    return (f'<svg class="gb" style="left:0;top:0;width:1080px;height:1920px;--d:{A(t)};--dd:.4s" viewBox="0 0 1080 1920">'
            f'<path d="{d}" pathLength="1" stroke="{color}" stroke-width="{grosor}"/></svg>')


BASE += FASE_CSS


# ───────────────────────── capa 3D de papel («pop-up»): cartón, papel arrugado y sombras reales sobre la hoja
BASE += "#p3{position:absolute;inset:0;z-index:14;pointer-events:none}"
RT3D = r"""
import * as THREE from 'three';
import {SVGLoader} from 'three/addons/loaders/SVGLoader.js';
const el=document.getElementById('p3');
const ren=new THREE.WebGLRenderer({antialias:true,alpha:true,preserveDrawingBuffer:true});
ren.setPixelRatio(location.hash.includes("preview")?1:2);ren.setSize(1080,1920);ren.shadowMap.enabled=true;ren.shadowMap.type=THREE.PCFSoftShadowMap;ren.toneMapping=THREE.NeutralToneMapping;
el.appendChild(ren.domElement);
// si la GPU pierde el contexto, que la captura truene (antes salía la capa 3D en blanco)
ren.domElement.addEventListener('webglcontextlost',()=>{window.__perdido=true});
const scene=new THREE.Scene();
const cam=new THREE.PerspectiveCamera(30,1080/1920,1,200);cam.position.z=40;
const PX=1920/(2*40*Math.tan(15*Math.PI/180));
scene.add(new THREE.HemisphereLight('#fffaf2','#a89a86',1.5));
const sun=new THREE.DirectionalLight('#fff3df',2.4);sun.position.set(-9,13,24);sun.castShadow=true;
sun.shadow.mapSize.set(2048,2048);Object.assign(sun.shadow.camera,{left:-20,right:20,top:34,bottom:-34,near:1,far:90});sun.shadow.radius=5;sun.shadow.bias=-.0005;scene.add(sun);
if(SOMBRA_PISO){const piso=new THREE.Mesh(new THREE.PlaneGeometry(80,120),new THREE.ShadowMaterial({opacity:.26}));piso.receiveShadow=true;scene.add(piso)}
// textura de papel hecha en un canvas (fibras + grano)
const TEX=(()=>{const c=document.createElement('canvas');c.width=c.height=256;const g=c.getContext('2d');g.fillStyle='#fff';g.fillRect(0,0,256,256);
 let sd=7;const rn=()=>(sd=(sd*16807)%2147483647)/2147483647;
 for(let i=0;i<9000;i++){const v=226+(rn()*29|0);g.fillStyle=`rgb(${v},${v},${v-7})`;g.fillRect(rn()*256,rn()*256,1+rn()*2,1)}
 for(let i=0;i<140;i++){g.strokeStyle=`rgba(140,120,90,${rn()*.16})`;g.beginPath();const x=rn()*256,y=rn()*256;g.moveTo(x,y);g.lineTo(x+rn()*34-17,y+rn()*8-4);g.stroke()}
 const t=new THREE.CanvasTexture(c);t.wrapS=t.wrapT=THREE.RepeatWrapping;t.colorSpace=THREE.SRGBColorSpace;return t})();
const _sv=[];
const P={THREE,scene,PX,TEX,
 u:p=>p/PX,
 at:(o,x,y,z=1.2)=>{o.position.set((x-540)/PX,(960-y)/PX,z);return o},
 k:(t,a,d)=>Math.min(1,Math.max(0,(t-a)/d)),
 eo:p=>1-Math.pow(1-p,3),eio:p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2,
 eb:p=>{const c=1.9;return 1+(c+1)*Math.pow(p-1,3)+c*Math.pow(p-1,2)},
 h:i=>{const x=Math.sin(i*12.9898+4.1)*43758.5453;return x-Math.floor(x)},
 papel:(c,o={})=>new THREE.MeshStandardMaterial({color:c,map:TEX,roughness:.96,metalness:0,...o}),
 sombra:o=>{o.traverse(m=>{if(m.isMesh){m.castShadow=true;m.receiveShadow=true}});return o},
 // figura SVG (viewBox 24) recortada en cartón: frente de color, canto de papel claro. size = ancho en px, grosor en px
 recorte:(d,size,c,grosor=14,canto='#f3ede0')=>{const data=new SVGLoader().parse(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="${d}"/></svg>`);
  const shapes=data.paths.flatMap(p=>SVGLoader.createShapes(p));const g0=new THREE.ShapeGeometry(shapes);g0.computeBoundingBox();const bw=g0.boundingBox.max.x-g0.boundingBox.min.x;
  const g=new THREE.ExtrudeGeometry(shapes,{depth:grosor/size*bw,bevelEnabled:true,bevelThickness:grosor/size*bw*.08,bevelSize:grosor/size*bw*.05,bevelSegments:1,curveSegments:28});
  g.rotateX(Math.PI);g.center();const s=(size/PX)/bw;g.scale(s,s,s);const m=new THREE.Mesh(g,[P.papel(c),P.papel(canto)]);return P.sombra(m)},
 // caja de cartón (servidor, paquete): w,h,d en px
 caja:(w,h,d,c='#c9a26b',cinta=true)=>{const G=new THREE.Group();G.add(new THREE.Mesh(new THREE.BoxGeometry(w/PX,h/PX,d/PX),P.papel(c)));
  if(cinta){const t=new THREE.Mesh(new THREE.BoxGeometry(w*.22/PX,h*1.01/PX,d*1.01/PX),P.papel('#e9dfc8'));G.add(t)}return P.sombra(G)},
 // hoja de papel ligeramente curvada (w,h px)
 hoja:(w,h,c='#fbf8f1',curva=.12)=>{const g=new THREE.PlaneGeometry(w/PX,h/PX,16,4);const p=g.attributes.position;
  for(let i=0;i<p.count;i++){const x=p.getX(i)/(w/PX);p.setZ(i,Math.sin((x+.5)*Math.PI)*curva*w/PX*.25)}g.computeVertexNormals();
  return P.sombra(new THREE.Mesh(g,P.papel(c,{side:THREE.DoubleSide})))},
 // bola de papel arrugado
 bola:(r,c='#f6f1e6',seed=1)=>{const g=new THREE.IcosahedronGeometry(r/PX,2);const p=g.attributes.position,v=new THREE.Vector3();
  for(let i=0;i<p.count;i++){v.fromBufferAttribute(p,i);const n=.78+.34*P.h(seed*97+Math.round(v.x*50)*7+Math.round(v.y*50)*13+Math.round(v.z*50)*3);v.multiplyScalar(n);p.setXYZ(i,v.x,v.y,v.z)}
  g.computeVertexNormals();return P.sombra(new THREE.Mesh(g,P.papel(c,{flatShading:true})))},
 // avión de papel (largo en px)
 avion:(l,c='#fbf8f1')=>{const L=l/PX,W=L*.55,H=L*.22;const v=new Float32Array([0,0,L/2, -W/2,0,-L/2, 0,0,-L/2*.8,  0,0,L/2, 0,0,-L/2*.8, W/2,0,-L/2,
   0,0,L/2, 0,-H,-L/2, 0,0,-L/2*.8]);const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(v,3));g.computeVertexNormals();
  return P.sombra(new THREE.Mesh(g,P.papel(c,{side:THREE.DoubleSide,flatShading:true})))},
 // laptop de cartón: base + tapa con bisagra (userData.tapa, userData.pantalla)
 laptop:(w,c='#2b2b30',pant='#6ea8ff')=>{const G=new THREE.Group(),d=w*.68;
  const base=new THREE.Mesh(new THREE.BoxGeometry(w/PX,w*.05/PX,d/PX),P.papel(c));G.add(base);
  const tapa=new THREE.Group();tapa.position.set(0,w*.025/PX,-d/2/PX);G.add(tapa);
  const lid=new THREE.Mesh(new THREE.BoxGeometry(w/PX,d/PX,w*.04/PX),P.papel(c));lid.position.y=d/2/PX;tapa.add(lid);
  const sc=new THREE.Mesh(new THREE.PlaneGeometry(w*.86/PX,d*.8/PX),P.papel(pant,{emissive:pant,emissiveIntensity:.35}));sc.position.set(0,d/2/PX,w*.021/PX);tapa.add(sc);
  G.userData.tapa=tapa;G.userData.pantalla=sc;return P.sombra(G)},
 // bisagra: envuelve el objeto para que gire desde su borde de abajo (alto en px)
 bisagra:(o,alto)=>{const G=new THREE.Group();o.position.y=alto/2/PX;G.add(o);G.userData.o=o;return G},
 // se levanta de la hoja como pop-up (gira desde acostado) en t0
 sube:(g,t,t0,d=.55)=>{const q=P.eb(P.k(t,t0,d));g.rotation.x=(1-q)*(-Math.PI/2);g.visible=t>=t0;return q},
 // se barre igual que las fases del DOM (translate(-1250px,260px) rotate(-14deg) en .5 s)
 barre:(o,t,tx)=>{if(tx==null||t<tx)return 0;const q=Math.pow(P.k(t,tx,.5),2.2);o.position.x+=-1250/PX*q;o.position.y+=-260/PX*q;o.rotation.z+=-.25*q;return q},
 fx0:()=>{},
};
"""
