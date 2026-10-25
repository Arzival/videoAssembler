"""Estilo «Escritorio»: un sistema operativo retro inventado (LogOS), con la estética de System 7 / Windows 98 que regresa en 2026
como reacción al vidrio esmerilado. Ventanas grises biseladas con barra de título, diálogos de alerta, barras de progreso por bloques,
cursor que se mueve y hace clic, íconos en pixel art, selección de texto como marcatextos y letra pixelada.
Nada se desvanece: las ventanas se abren y cierran con los rectángulos de «zoom» del sistema, los textos se teclean y todo va a pasos.

Tiempos: segundos del video final (A(t) = retardo local de la escena). Las ventanas se abren desde un punto (ícono) con 4 pasos.
"""
import json, math, re

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Jersey+15&family=VT323'
         '&family=IBM+Plex+Sans:wght@400;600;700&display=block" rel="stylesheet">')
COLA = 0.45

# paleta del sistema
C = {'gris': '#c3c3c3', 'claro': '#ffffff', 'sombra': '#828282', 'negro': '#0a0a0a', 'azul': '#0a1f8f', 'azul2': '#3d6fd6',
     'teal': '#0e7c7b', 'sel': '#0a1f8f', 'rojo': '#d8262a', 'amarillo': '#ffd400', 'verde': '#14a046', 'lila': '#6b5bd6'}

# sprites 16×16: cada letra es un color
PAL = {'k': '#0a0a0a', 'w': '#ffffff', 'g': '#c3c3c3', 's': '#828282', 'y': '#ffd400', 'r': '#d8262a', 'b': '#0a1f8f', 'l': '#6fa8ff',
       'o': '#f08c1c', 'v': '#14a046', 'p': '#b8a2ff', 'm': '#7a86e0', 'c': '#33c6d6', 'd': '#3a3a3a', 'n': '#c48a3a'}
SPR = {
    'alerta': ["       kk       ", "      kyyk      ", "      kyyk      ", "     kyyyyk     ", "     kykkyk     ", "    kyykkyyk    ",
               "    kyykkyyk    ", "   kyyykkyyyk   ", "   kyyykkyyyk   ", "  kyyyykkyyyyk  ", "  kyyyyyyyyyyk  ", " kyyyyykkyyyyyk ",
               " kyyyyykkyyyyyk ", "kyyyyyyyyyyyyyyk", "kkkkkkkkkkkkkkkk", "                "],
    'error': ["     kkkkkk     ", "   kkrrrrrrkk   ", "  krrrrrrrrrrk  ", " krrwwrrrrwwrrk ", " krrwwwrrwwwrrk ", "krrrrwwwwwwrrrrk",
              "krrrrrwwwwrrrrrk", "krrrrrwwwwrrrrrk", "krrrrwwwwwwrrrrk", " krrwwwrrwwwrrk ", " krrwwrrrrwwrrk ", "  krrrrrrrrrrk  ",
              "   kkrrrrrrkk   ", "     kkkkkk     ", "                ", "                "],
    'info': ["     kkkkkk     ", "   kkllllllkk   ", "  kllllwwllllk  ", " klllllwwlllllk ", " kllllllllllllk ", "kllllwwwwllllllk",
             "kllllllwwllllllk", "kllllllwwllllllk", "kllllllwwllllllk", " klllllwwlllllk ", " kllllwwwwllllk ", "  kllllllllllk  ",
             "   kklllllllk   ", "     kkkkllk    ", "          klk   ", "           kk   "],
    'carpeta': ["                ", " kkkkk          ", "kyyyyyk         ", "kyyyyyykkkkkkkk ", "kyyyyyyyyyyyyyyk", "kyookkkkkkkkkkkk",
                "kyok          k ", "kyok           k", "kyok           k", "kok            k", "kok            k", "kok            k",
                "kokkkkkkkkkkkkkk", "kkkkkkkkkkkkkkk ", "                ", "                "],
    'archivo': ["  kkkkkkkkk     ", "  kwwwwwwwkk    ", "  kwwwwwwwkwk   ", "  kwkkkkwwkkkk  ", "  kwwwwwwwwwwk  ", "  kwkkkkkkkkwk  ",
                "  kwwwwwwwwwwk  ", "  kwkkkkkkkkwk  ", "  kwwwwwwwwwwk  ", "  kwkkkkkkwwwk  ", "  kwwwwwwwwwwk  ", "  kwkkkkkkkkwk  ",
                "  kwwwwwwwwwwk  ", "  kwwwwwwwwwwk  ", "  kkkkkkkkkkkk  ", "                "],
    'compu': ["                ", " kkkkkkkkkkkkkk ", " kggggggggggggk ", " kgkkkkkkkkkkgk ", " kgkllllllllkgk ", " kgkllllllllkgk ",
              " kgkllllllllkgk ", " kgkllllllllkgk ", " kgkkkkkkkkkkgk ", " kggggggggggvgk ", " kkkkkkkkkkkkkk ", "     kggggk     ",
              "  kkkkkkkkkkkk  ", "  kggggggggggk  ", "  kkkkkkkkkkkk  ", "                "],
    'servidor': ["   kkkkkkkkkk   ", "   kddddddddk   ", "   kdvdssssdk   ", "   kddddddddk   ", "   kkkkkkkkkk   ", "   kddddddddk   ",
                 "   kdvdssssdk   ", "   kddddddddk   ", "   kkkkkkkkkk   ", "   kddddddddk   ", "   kdrdssssdk   ", "   kddddddddk   ",
                 "   kkkkkkkkkk   ", "    kk    kk    ", "                ", "                "],
    'lupa': ["     kkkk       ", "   kkwwwwkk     ", "  kwwllllwwk    ", "  kwllllllwk    ", " kwllllllllwk   ", " kwllllllllwk   ",
             " kwllllllllwk   ", "  kwllllllwk    ", "  kwwllllwwk    ", "   kkwwwwkkk    ", "     kkkk kkk   ", "          kkkk  ",
             "           kkkk ", "            kkk ", "                ", "                "],
    'robot': ["       kk       ", "       rk       ", "   kkkkkkkkkk   ", "  kggggggggggk  ", "  kgkkkggkkkgk  ", "  kgkrkggkrkgk  ",
              "  kgkkkggkkkgk  ", "  kggggggggggk  ", "  kggkkkkkkggk  ", "  kggggggggggk  ", "   kkkkkkkkkk   ", "  kggggggggggk  ",
              " kgkggggggggkgk ", " kgkggggggggkgk ", "  kkkkkkkkkkkk  ", "                "],
    'mundo': ["     kkkkkk     ", "   kkllvvllkk   ", "  kllvvvvlllvk  ", " kllvvvvvlllvvk ", " klllvvvllllvvk ", "kllllvvlllllvlvk",
              "klllllllllvvlllk", "klllllllvvvvlllk", "kllvvlllvvvlllk ", "klvvvvllllvllllk", " kvvvvvllllllk  ", " kllvvlllllllk  ",
              "  kllllllllllk  ", "   kkllllllkk   ", "     kkkkkk     ", "                "],
    'candado': ["     kkkkkk     ", "    kssssssk    ", "   ksk    ksk   ", "   ksk    ksk   ", "   ksk    ksk   ", " kkkkkkkkkkkkkk ",
                " kyyyyyyyyyyyyk ", " kyyyyykkyyyyyk ", " kyyyyykkyyyyyk ", " kyyyyyykyyyyyk ", " kyyyyyykyyyyyk ", " kyyyyyyyyyyyyk ",
                " kkkkkkkkkkkkkk ", "                ", "                ", "                "],
    'reloj': ["     kkkkkk     ", "   kkwwwwwwkk   ", "  kwwwwkwwwwwk  ", " kwwwwwkwwwwwwk ", " kwwwwwkwwwwwwk ", "kwwwwwwkwwwwwwwk",
              "kwwwwwwkwwwwwwwk", "kwwwwwwkkkkkwwwk", "kwwwwwwwwwwwwwwk", "kwwwwwwwwwwwwwwk", " kwwwwwwwwwwwwk ", " kwwwwwwwwwwwwk ",
              "  kwwwwwwwwwwk  ", "   kkwwwwwwkk   ", "     kkkkkk     ", "                "],
    'cursor': ["k               ", "kk              ", "kwk             ", "kwwk            ", "kwwwk           ", "kwwwwk          ",
               "kwwwwwk         ", "kwwwwwwk        ", "kwwwwwwwk       ", "kwwwwwwwwk      ", "kwwwwwkkkkk     ", "kwwkwwk         ",
               "kwk kwwk        ", "kk  kwwk        ", "     kwwk       ", "     kkk        "],
    'chip': ["   k k k k k    ", "  kkkkkkkkkkk   ", "k kdddddddddk k ", "  kdkkkkkkkdk   ", "k kdkvvvvvkdk k ", "  kdkvvvvvkdk   ",
             "k kdkvvvvvkdk k ", "  kdkvvvvvkdk   ", "k kdkkkkkkkdk k ", "  kdddddddddk   ", "  kkkkkkkkkkk   ", "   k k k k k    ",
             "                ", "                ", "                ", "                "],
}


def sprite(name, size=64, extra=''):
    rows = SPR[name]
    rects = ''.join(f'<rect x="{x}" y="{y}" width="1" height="1" fill="{PAL[ch]}"/>' for y, r in enumerate(rows) for x, ch in enumerate(r) if ch != ' ')
    return f'<svg viewBox="0 0 16 16" width="{size}" height="{size}" shape-rendering="crispEdges" style="display:block;{extra}">{rects}</svg>'


BASE = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:transparent;font-family:'Jersey 15',monospace;color:#0a0a0a;-webkit-font-smoothing:none;font-synthesis:none}
.mesa{position:absolute;inset:0;overflow:hidden;background-color:var(--mesa,#0e7c7b);
  background-image:radial-gradient(rgba(0,0,0,.16) 1.2px,transparent 1.4px);background-size:6px 6px}
.mesa.rojo{--mesa:#7a1414}.mesa.morado{--mesa:#4b3fa0}.mesa.noche{--mesa:#101a3a}
.barra{position:absolute;left:0;right:0;top:0;height:64px;z-index:90;background:#c3c3c3;display:flex;align-items:center;gap:30px;padding:0 24px;
  font-weight:700;font-size:30px;box-shadow:inset 0 -3px 0 #0a0a0a,inset 0 3px 0 #fff}
.barra .lg{display:flex;align-items:center;gap:10px}.barra .hr{margin-left:auto;font-family:VT323;font-size:38px}
/* ventana */
.vn{position:absolute;z-index:20;background:#c3c3c3;padding:5px;
  box-shadow:inset -3px -3px 0 #0a0a0a,inset 3px 3px 0 #fff,inset -6px -6px 0 #828282,inset 6px 6px 0 #dfdfdf,12px 12px 0 rgba(0,0,0,.35);
  visibility:hidden;animation:ab .01s steps(1) var(--d) forwards}
.vn.x{animation:ab .01s steps(1) var(--d) forwards,ci .01s steps(1) var(--x) forwards}
@keyframes ab{to{visibility:visible}}@keyframes ci{to{visibility:hidden;clip-path:inset(50% 50%)}}
.vn .tb{height:52px;display:flex;align-items:center;gap:12px;padding:0 6px 0 12px;color:#fff;font-weight:700;font-size:28px;white-space:nowrap;overflow:hidden;
  background:linear-gradient(90deg,var(--t1,#0a1f8f),var(--t2,#3d6fd6))}
.vn.off .tb{--t1:#7b7b7b;--t2:#b5b5b5}
.vn .tb .bt{margin-left:auto;display:flex;gap:6px}
.vn .tb .bt i{width:38px;height:34px;background:#c3c3c3;box-shadow:inset -2px -2px 0 #0a0a0a,inset 2px 2px 0 #fff,inset -4px -4px 0 #828282;color:#0a0a0a;
  font-style:normal;font-size:24px;line-height:32px;text-align:center}
.vn .cu{position:relative;margin-top:6px;background:#fff;box-shadow:inset 3px 3px 0 #828282,inset -3px -3px 0 #fff,inset 6px 6px 0 #0a0a0a;padding:24px 28px;overflow:hidden}
.vn .cu.gris{background:#c3c3c3;box-shadow:none;padding:18px 20px}
.vn .cu.negro{background:#0a0a0a;color:#33ff66;font-family:VT323;font-size:44px;line-height:1.05}
/* rectángulos de zoom al abrir/cerrar */
.zm{position:absolute;z-index:60;border:3px dotted #0a0a0a;outline:2px dotted #fff;visibility:hidden;pointer-events:none}
/* texto */
.big{font-weight:700;line-height:.98;letter-spacing:-.01em}
.big .sel{background:#0a1f8f;color:#fff;padding:0 .08em}
.big .rj{color:#d8262a}
.ty{display:inline-block;white-space:pre;clip-path:inset(0 100% 0 0);animation:tip var(--td,.8s) steps(var(--n,20)) var(--d) forwards;vertical-align:top}
@keyframes tip{to{clip-path:inset(0 -5% 0 0)}}
.sl{background:transparent;color:inherit;animation:sel .25s steps(3) var(--s) forwards}
@keyframes sel{to{background:#0a1f8f;color:#fff}}
.car{display:inline-block;width:.45em;height:.9em;background:currentColor;vertical-align:-.08em;animation:blink 1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
.vt{font-family:VT323;font-size:46px;line-height:1}
.ps{font-family:'IBM Plex Sans',sans-serif}
/* botones */
.btn{display:inline-block;min-width:170px;padding:12px 26px;text-align:center;font-weight:700;font-size:30px;background:#c3c3c3;
  box-shadow:inset -3px -3px 0 #0a0a0a,inset 3px 3px 0 #fff,inset -6px -6px 0 #828282,inset 6px 6px 0 #dfdfdf}
.btn.def{outline:3px solid #0a0a0a;outline-offset:2px}
.btn.pr{animation:pr .25s steps(1) var(--p) forwards}
@keyframes pr{0%{box-shadow:inset 3px 3px 0 #0a0a0a,inset -3px -3px 0 #fff,inset 6px 6px 0 #828282;transform:translate(2px,2px)}100%{}}
/* barra de progreso por bloques */
.pg{height:54px;padding:5px;background:#fff;box-shadow:inset 3px 3px 0 #828282,inset -3px -3px 0 #fff,inset 6px 6px 0 #0a0a0a;overflow:hidden}
.pg b{display:block;height:100%;width:0;background:repeating-linear-gradient(90deg,var(--pc,#0a1f8f) 0 30px,transparent 30px 36px)}
/* ícono del escritorio */
.ic{position:absolute;z-index:12;width:190px;text-align:center;color:#fff;font-size:28px;font-weight:600;visibility:hidden;animation:ab .01s steps(1) var(--d) forwards}
.ic svg{margin:0 auto 8px}
.ic span{padding:2px 8px;text-shadow:2px 2px 0 #000}
.ic.on span{animation:icsel .01s steps(1) var(--s) forwards}
@keyframes icsel{to{background:#0a1f8f;text-shadow:none}}
.ic.on svg{animation:icsv .01s steps(1) var(--s) forwards}@keyframes icsv{to{filter:brightness(.55) sepia(1) hue-rotate(190deg) saturate(4)}}
/* cursor */
.cur{position:absolute;z-index:95;left:0;top:0;width:72px;height:72px;pointer-events:none}
.cur .ck{position:absolute;left:-18px;top:-18px;width:36px;height:36px;border:4px solid #fff;border-radius:50%;visibility:hidden}
/* marquesina (cinta) */
.mq{position:absolute;left:0;right:0;z-index:89;height:58px;background:#0a0a0a;color:#ffd400;overflow:hidden;display:flex;align-items:center;font-family:VT323;font-size:44px;
  box-shadow:inset 0 -3px 0 #333}
.mq .mv{display:flex;gap:60px;white-space:nowrap;padding-left:120px;animation:mv 80s linear infinite}
@keyframes mv{to{transform:translateX(-100%)}}
.mq .tg{position:relative;z-index:2;height:100%;display:flex;align-items:center;padding:0 18px;flex-shrink:0;white-space:nowrap;background:#d8262a;color:#fff;font-family:'Jersey 15';font-weight:700;font-size:30px;
  animation:tgb 1s steps(1) infinite}
@keyframes tgb{50%{background:#ffd400;color:#0a0a0a}}
/* sacudida de error */
.sac{animation:ab .01s steps(1) var(--d) forwards,sac .4s steps(6) var(--d)}
.vn.sac.x{animation:ab .01s steps(1) var(--d) forwards,sac .4s steps(6) var(--d),ci .01s steps(1) var(--x) forwards}
@keyframes sac{0%,100%{transform:none}20%{transform:translate(-14px,0)}40%{transform:translate(12px,0)}60%{transform:translate(-9px,0)}80%{transform:translate(6px,0)}}
.ic.apx{animation:ab .01s steps(1) var(--d) forwards,ci .01s steps(1) var(--x) forwards}
.ap{opacity:0;animation:apo .01s steps(1) var(--d) forwards}
.ap.x{animation:apo .01s steps(1) var(--d) forwards,apc .01s steps(1) var(--x) forwards}
@keyframes apo{to{opacity:1}}@keyframes apc{to{opacity:0}}
"""

JS = """const _e=p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2;
const _v=(k,t)=>{let v=k[0][1];for(const [a,b,d] of k.slice(1)){const p=Math.min(1,Math.max(0,(t-a)/(d||.8)));v=v+(b-v)*_e(p)}return v};
const _f=(v,f)=>f==='c'?Math.round(v).toLocaleString('en-US'):f==='1'?v.toFixed(1):f==='p'?Math.round(v)+'%':Math.round(v);
const _N=[...document.querySelectorAll('[data-n]')].map(e=>[e,JSON.parse(e.dataset.n)]),_K=[...document.querySelectorAll('[data-k]')].map(e=>[e,JSON.parse(e.dataset.k)]);
const _C=[...document.querySelectorAll('.cur')].map(e=>[e,JSON.parse(e.dataset.c),e.querySelector('.ck')]);
const _G=[...document.querySelectorAll('[data-g]')].map(e=>[e,JSON.parse(e.dataset.g)]);
const _Z=[...document.querySelectorAll('.zm')].map(e=>[e,JSON.parse(e.dataset.z)]);
window.__seek=s=>{const t=s+S0;
 for(const [e,k] of _N)e.textContent=(e.dataset.pre||'')+_f(_v(k,t),e.dataset.f)+(e.dataset.suf||'');
 for(const [e,k] of _K)e.style.width=(Math.floor(_v(k,t)/6)*6)+'%';
 for(const [e,ks,ck] of _C){let x=ks[0][1],y=ks[0][2],on=t>=ks[0][0],clk=false;
  for(let i=1;i<ks.length;i++){const [a,X,Y,c]=ks[i],[a0]=ks[i-1];const d=Math.max(.01,a-a0-.0),p=Math.min(1,Math.max(0,(t-a0)/d));if(t>=a0){x=x+(X-x)*_e(p);y=y+(Y-y)*_e(p)}if(c&&t>=a&&t<a+.22)clk=true}
  e.style.transform=`translate(${x}px,${y}px)`;e.style.visibility=on&&!(e.dataset.fin&&t>=+e.dataset.fin)?'visible':'hidden';ck.style.visibility=clk?'visible':'hidden'}
 for(const [e,g] of _G){const w=e.width,h=e.height,c=e.getContext('2d');c.clearRect(0,0,w,h);c.fillStyle='#0a0a0a';c.fillRect(0,0,w,h);
  c.strokeStyle='#0d4d1d';c.lineWidth=2;for(let x=0;x<w;x+=40){c.beginPath();c.moveTo(x-((t*80)%40),0);c.lineTo(x-((t*80)%40),h);c.stroke()}for(let y=0;y<h;y+=40){c.beginPath();c.moveTo(0,y);c.lineTo(w,y);c.stroke()}
  c.strokeStyle=g.c||'#33ff66';c.lineWidth=5;c.beginPath();for(let i=0;i<=60;i++){const tt=t-(60-i)*.1;const v=Math.max(0,Math.min(100,_v(g.k,tt)+(g.r||6)*Math.sin(tt*7+i)));const X=i/60*w,Y=h-v/100*h;i?c.lineTo(X,Y):c.moveTo(X,Y)}c.stroke()}
 for(const [e,z] of _Z){let vis=false;for(const [a,b,dur] of z.v){if(t>=a&&t<a+dur){const p=Math.min(3,Math.floor((t-a)/dur*4))/3,q=b?1-p:p;
   e.style.left=(z.o[0]+(z.r[0]-z.o[0])*q)+'px';e.style.top=(z.o[1]+(z.r[1]-z.o[1])*q)+'px';e.style.width=(z.o[2]+(z.r[2]-z.o[2])*q)+'px';e.style.height=(z.o[3]+(z.r[3]-z.o[3])*q)+'px';vis=true}}
  e.style.visibility=vis?'visible':'hidden'}
 for(const f of (window.__xs||[]))f(t)};
const _F=['100px "Jersey 15"','100px VT323','600 100px "IBM Plex Sans"'];
window.__listo=Promise.all(_F.map(f=>document.fonts.load(f))).then(()=>document.fonts.ready).then(()=>{const m=_F.filter(f=>!document.fonts.check(f));if(m.length)throw new Error('faltan fuentes: '+m)});
window.__seek(0);"""


def at(start):
    return lambda t: f'{max(0.0, t - start):.2f}s'


def _txt(h):
    return re.sub(r'<[^>]+>', '', h)


def ventana(x, y, w, titulo, cuerpo, A, t, sale=None, h=None, icono=None, desde=None, cls='', cu='', activa=True, z=20, t1=None, t2=None):
    """Ventana que se abre en t (con rectángulos de zoom desde `desde`=(x,y) si se da) y se cierra en `sale`."""
    st = f'left:{x}px;top:{y}px;width:{w}px;{f"height:{h}px;" if h else ""}--d:{A(t)};z-index:{z};' + (f'--t1:{t1};' if t1 else '') + (f'--t2:{t2};' if t2 else '')
    if sale is not None:
        cls += ' x'; st += f'--x:{A(sale)};'
    ic = sprite(icono, 34) if icono else ''
    zoom = ''
    if desde:
        hh = h or 400
        v = [[t - .2, 0, .2]] + ([[sale, 1, .2]] if sale is not None else [])
        zoom = f"<div class=\"zm\" data-z='{json.dumps({'o': [desde[0] - 30, desde[1] - 30, 60, 60], 'r': [x, y, w, hh], 'v': v})}'></div>"
    return (f'{zoom}<div class="vn{"" if activa else " off"} {cls}" style="{st}"><div class="tb">{ic}<span>{titulo}</span>'
            f'<div class="bt"><i>_</i><i>□</i><i>×</i></div></div><div class="cu {cu}">{cuerpo}</div></div>')


def teclea(txt, A, t, dt=None, extra=''):
    n = max(3, len(_txt(txt)))
    dt = dt or min(1.2, .035 * n + .15)
    return f'<span class="ty" style="--d:{A(t)};--td:{dt:.2f}s;--n:{n};{extra}">{txt}</span>'


def grande(lineas, A, t, size=110, step=.035, color=None):
    """Texto grande tecleado línea por línea. _palabra_ = seleccionada (azul) un instante después; *palabra* = roja."""
    html, tt = '', t
    for ln in lineas:
        n = len(_txt(re.sub(r'[*_]', '', ln)))
        dt = max(.2, n * step)
        ln = re.sub(r'_(.+?)_', lambda m: f'<span class="sl" style="--s:{A(tt + dt + .15)}">{m.group(1)}</span>', ln)
        ln = re.sub(r'\*(.+?)\*', r'<span class="rj">\1</span>', ln)
        html += f'<div>{teclea(ln, A, tt, dt)}</div>'
        tt += dt + .05
    c = f'color:{color};' if color else ''
    return f'<div class="big" style="font-size:{size}px;{c}">{html}</div>'


def dialogo(x, y, w, icono, texto, A, t, botones=('Aceptar',), pulsa=None, sale=None, titulo='LogOS', sacude=False, desde=None, z=40, t1=None):
    bts = ''.join(f'<span class="btn{" def" if i == 0 else ""}{" pr" if pulsa and i == 0 else ""}" style="{f"--p:{A(pulsa)}" if pulsa and i == 0 else ""}">{b}</span>'
                  for i, b in enumerate(botones))
    cu = (f'<div style="display:flex;gap:26px;align-items:flex-start">{sprite(icono, 96)}<div class="ps" style="font-size:36px;line-height:1.25;font-weight:600;flex:1">{texto}</div></div>'
          f'<div style="display:flex;gap:20px;justify-content:center;margin-top:26px">{bts}</div>')
    v = ventana(x, y, w, titulo, cu, A, t, sale=sale, desde=desde, cu='gris', z=z, t1=t1)
    if sacude:
        v = v.replace('class="vn', 'class="vn sac', 1)
    return v


def progreso(keys, color=None):
    c = f'--pc:{color};' if color else ''
    return f"<div class=\"pg\" style=\"{c}\"><b data-k='{json.dumps([list(k) for k in keys])}'></b></div>"


def N(keys, f='', suf='', pre=''):
    return (f"<b data-n='{json.dumps([list(k) for k in keys])}'" + (f' data-f="{f}"' if f else '') + (f' data-suf="{suf}"' if suf else '')
            + (f' data-pre="{pre}"' if pre else '') + ' style="font-weight:inherit">0</b>')


def icono(x, y, spr, label, A, t, sel=None, size=110, sale=None):
    cls, st = 'ic', f'left:{x}px;top:{y}px;--d:{A(t)};'
    if sel is not None:
        cls += ' on'; st += f'--s:{A(sel)};'
    if sale is not None:
        st += f'--x:{A(sale)};'
        cls += ' apx'
    return f'<div class="{cls}" style="{st}">{sprite(spr, size)}<span>{label}</span></div>'


def cursor(keys, fin=None):
    """keys = [(t, x, y, clic?)] — se mueve con suavidad entre puntos; clic dibuja un círculo un instante; fin = se oculta (s del video)."""
    fn = f' data-fin="{fin}"' if fin is not None else ''
    ks = json.dumps([list(k) + [False] * (4 - len(k)) for k in keys])
    return f'<div class="cur"{fn} data-c=\'{ks}\'>{sprite("cursor", 72)}<i class="ck"></i></div>'


def grafica(w, h, keys, color='#33ff66', ruido=6):
    return f"<canvas width=\"{w}\" height=\"{h}\" data-g='{json.dumps({'k': [list(k) for k in keys], 'c': color, 'r': ruido})}' style=\"display:block;width:{w}px;height:{h}px\"></canvas>"


def ap(html, A, t, sale=None, extra=''):
    """Aparece de golpe en t (y desaparece en sale)."""
    cls, st = 'ap', f'--d:{A(t)};'
    if sale is not None:
        cls += ' x'; st += f'--x:{A(sale)};'
    return f'<div class="{cls}" style="{st}{extra}">{html}</div>'


def barra_menu(app='LogOS', menus=('Archivo', 'Edición', 'Ver', 'Ayuda'), hora='21:42'):
    return (f'<div class="barra"><span class="lg">{sprite("compu", 40)}{app}</span>' + ''.join(f'<span style="font-weight:500">{m}</span>' for m in menus)
            + f'<span class="hr">{hora}</span></div>')


def page(css, body, dur, S0=0.0, mesa='', transparente=False, menu=True):
    if transparente:
        inner = f'<div style="position:absolute;inset:0">{body}</div>'
    else:
        inner = f'<div class="mesa {mesa}">{barra_menu() if menu else ""}{body}</div>'
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{BASE}{css}</style></head><body>{inner}
<script>const S0={S0};{JS}</script></body></html>"""
