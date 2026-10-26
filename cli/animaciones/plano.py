"""Estilo «Plano técnico»: la historia se cuenta como un plano de ingeniería (blueprint). Fondo azul de plano con retícula
fina, y todo se DIBUJA con trazos blancos/cian (stroke-dashoffset): diagramas de flujo, esquemáticos, cotas con flechas,
servidores en isométrico, anotaciones a mano (Architects Daughter) y correcciones en lápiz rojo (nubes de revisión,
taches, sellos). Las cifras van con letra técnica condensada (Barlow Condensed) que primero se traza y luego se rellena.
Arriba, un cajetín fijo con la serie y la hoja. Entre páginas la cámara barre el plano hacia otra zona (sin fundidos):
las dos páginas coinciden en la retícula, así que el corte no se nota.

Todo va en SEGUNDOS DEL VIDEO FINAL; cada página recibe S0 (su inicio) y el runtime mueve todo desde __seek, sin
animaciones CSS ni WAAPI (nada que Chrome pueda descartar al capturar en paralelo). 30 cps.

Piezas (devuelven SVG; el «mundo» se mueve con la cámara, el cajetín y los subtítulos no):
  linea, poli, rect, circ, flecha, cota, cotav, texto, sello, nube, tache, subraya, punteado, caja_punteada,
  servidor_frente, servidor_iso, interruptor, sobre, reloj, codigo, palomita, campana
  g(contenido, pop=…, on=…, mv=…, rot=…, cls=…, jit=…)  → grupo con animación
  page(S0, dur, mundo, cam, hoja, total)  · subtitulos(G, dur)
"""
import html as H
import json
import math

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Architects+Daughter&family=Barlow+Condensed:wght@600;800'
         '&family=IBM+Plex+Mono:wght@400;600&display=block" rel="stylesheet">')
CPS = 30
BL, CI, RO, AM = '#eaf4ff', '#7fe3ff', '#ff5a4f', '#ffd166'
MONO = .6  # ancho de un carácter de IBM Plex Mono (em): las cajas de texto se calculan exactas

_n = [0]


def uid(p='m'):
    _n[0] += 1
    return f'{p}{_n[0]}'


def f(x):
    return ('%.2f' % x).rstrip('0').rstrip('.') if isinstance(x, float) else str(x)


def esc(s):
    return H.escape(str(s), quote=True)


# ── trazos ──────────────────────────────────────────────────────────────────────────────────────────────
def path(d, t, dur=.5, cls='ln', frac=1, extra=''):
    """Cualquier trazo: se dibuja de 0 a `frac` de su largo entre t y t+dur."""
    return f'<path d="{d}" pathLength="1" class="{cls}" data-draw="{f(t)} {f(dur)} {f(frac)}" {extra}/>'


def linea(x1, y1, x2, y2, t, dur=.35, cls='ln'):
    return path(f'M{f(x1)} {f(y1)}L{f(x2)} {f(y2)}', t, dur, cls)


def poli(pts, t, dur=.5, cls='ln', cerrar=False):
    return path('M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pts) + ('Z' if cerrar else ''), t, dur, cls)


def rect(x, y, w, h, t, dur=.5, cls='ln', extra=''):
    return path(f'M{f(x)} {f(y)}H{f(x + w)}V{f(y + h)}H{f(x)}Z', t, dur, cls, extra=extra)


def arco_d(cx, cy, r, a0=-90):
    a = math.radians(a0)
    x0, y0 = cx + r * math.cos(a), cy + r * math.sin(a)
    x1, y1 = cx - r * math.cos(a), cy - r * math.sin(a)
    return f'M{f(x0)} {f(y0)}A{f(r)} {f(r)} 0 1 1 {f(x1)} {f(y1)}A{f(r)} {f(r)} 0 1 1 {f(x0)} {f(y0)}'


def circ(cx, cy, r, t, dur=.5, cls='ln', frac=1, a0=-90):
    return path(arco_d(cx, cy, r, a0), t, dur, cls, frac)


def punta(x1, y1, x2, y2, t, cls='ln', s=22):
    """Punta de flecha abierta en (x2,y2) apuntando desde (x1,y1)."""
    a = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - s * math.cos(a - .45), y2 - s * math.sin(a - .45))
    p2 = (x2 - s * math.cos(a + .45), y2 - s * math.sin(a + .45))
    return poli([p1, (x2, y2), p2], t, .12, cls)


def flecha(pts, t, dur=.45, cls='ln', s=22, doble=False):
    out = poli(pts, t, dur, cls) + punta(*pts[-2], *pts[-1], t + dur * .85, cls, s)
    if doble:
        out += punta(*pts[1], *pts[0], t + dur * .85, cls, s)
    return out


def cota(x1, x2, y, label, t, dur=.6, size=30, cls='ln c', fill='fc', arriba=True):
    """Cota horizontal: líneas de referencia, línea con dos puntas y la medida al centro."""
    e = 26
    out = linea(x1, y - e, x1, y + e, t, .15, cls) + linea(x2, y - e, x2, y + e, t, .15, cls)
    out += flecha([(x1, y), (x2, y)], t + .1, dur, cls, 20, doble=True)
    yy = y - 16 if arriba else y + size + 8
    out += texto((x1 + x2) / 2, yy, label, t + dur * .6, size, 'mono', 'middle', 'escribe', cls=fill)
    return out


def cotav(x, y1, y2, label, t, dur=.6, size=28, cls='ln c', fill='fc', lado=1):
    e = 26
    out = linea(x - e, y1, x + e, y1, t, .15, cls) + linea(x - e, y2, x + e, y2, t, .15, cls)
    out += flecha([(x, y1), (x, y2)], t + .1, dur, cls, 20, doble=True)
    out += texto(x + lado * 22, (y1 + y2) / 2 + size * .35, label, t + dur * .6, size, 'mono', 'start' if lado > 0 else 'end', 'escribe', cls=fill)
    return out


# ── texto ───────────────────────────────────────────────────────────────────────────────────────────────
def texto(x, y, txt, t, size=40, fuente='mono', anchor='start', modo='escribe', dur=.6, cls='', lleno=None, L=None,
          rot=0, cps=28, peso=None):
    """modo: 'trazo' (se dibuja el contorno y en `lleno` se rellena), 'escribe' (letra por letra), 'pop', 'fijo'."""
    fam = {'mono': 'mono', 'big': 'bc', 'nota': 'nota'}[fuente]
    st = f'font-size:{f(size)}px' + (f';font-weight:{peso}' if peso else '')
    tr = f' transform="rotate({f(rot)} {f(x)} {f(y)})"' if rot else ''
    base = f'x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" style="{st}"{tr}'
    if modo == 'trazo':
        L = L or size * 4.2
        ll = lleno if lleno is not None else t + dur
        return (f'<text {base} class="{fam} tz {cls}" data-draw="{f(t)} {f(dur)} 1 {f(L)}" '
                f'data-cls="{f(ll)} lleno">{esc(txt)}</text>')
    if modo == 'escribe':
        return f'<text {base} class="{fam} {cls}" data-type="{f(t)} {cps}" data-full="{esc(txt)}"></text>'
    if modo == 'pop':
        return g(f'<text {base} class="{fam} {cls}">{esc(txt)}</text>', pop=(t, .35))
    return g(f'<text {base} class="{fam} {cls}">{esc(txt)}</text>', on=(t,))


def ancho(txt, size):
    return len(txt) * size * MONO


def etiqueta(x, y, txt, t, size=28, cls='ln', fill='', anchor='start', pad=14, modo='escribe'):
    """Texto mono dentro de una caja dibujada (medidas exactas por ser monoespaciada)."""
    w = ancho(txt, size) + pad * 2
    h = size + pad * 1.4
    x0 = x if anchor == 'start' else x - w / 2 if anchor == 'middle' else x - w
    return (rect(x0, y - h / 2, w, h, t, .35, cls) +
            texto(x0 + pad, y + size * .36, txt, t + .2, size, 'mono', 'start', modo, cls=fill))


def sello(x, y, txt, t, rot=-8, size=60, color='r', doble=True):
    """Sello de lápiz rojo que cae de golpe (escala 2.2 → 1 en 0.18 s)."""
    w = ancho(txt, size) + 56
    h = size + 40
    c = {'r': RO, 'c': CI, 'b': BL, 'a': AM}[color]
    inner = (f'<rect x="{f(-w / 2)}" y="{f(-h / 2)}" width="{f(w)}" height="{f(h)}" rx="6" fill="none" stroke="{c}" stroke-width="6"/>'
             + (f'<rect x="{f(-w / 2 + 10)}" y="{f(-h / 2 + 10)}" width="{f(w - 20)}" height="{f(h - 20)}" rx="3" fill="none" stroke="{c}" stroke-width="2"/>' if doble else '')
             + f'<text x="0" y="{f(size * .36)}" text-anchor="middle" class="mono" style="font-size:{size}px;font-weight:600;fill:{c};letter-spacing:.04em">{esc(txt)}</text>')
    return (f'<g transform="translate({f(x)} {f(y)}) rotate({f(rot)})"><g class="pp" data-sello="{f(t)}">{inner}</g></g>')


def nube(x, y, w, h, t, dur=.7, cls='ln r grueso', r=26):
    """Nube de revisión (la marca roja de «aquí hay un cambio» en los planos)."""
    pts = []
    per = 2 * (w + h)
    n = max(8, int(per / (r * 1.6)))
    for i in range(n + 1):
        d = per * i / n
        if d <= w:
            pts.append((x + d, y))
        elif d <= w + h:
            pts.append((x + w, y + d - w))
        elif d <= 2 * w + h:
            pts.append((x + w - (d - w - h), y + h))
        else:
            pts.append((x, y + h - (d - 2 * w - h)))
    dd = f'M{f(pts[0][0])} {f(pts[0][1])}'
    for (px, py) in pts[1:]:
        dd += f'A{r} {r} 0 0 1 {f(px)} {f(py)}'
    return path(dd, t, dur, cls)


def tache(cx, cy, s, t, cls='ln r grueso'):
    return linea(cx - s, cy - s, cx + s, cy + s, t, .18, cls) + linea(cx + s, cy - s, cx - s, cy + s, t + .15, .18, cls)


def subraya(x1, x2, y, t, cls='ln r', amp=7, dur=.35):
    """Subrayado a mano (ondulado)."""
    n = max(3, int((x2 - x1) / 60))
    d = f'M{f(x1)} {f(y)}'
    for i in range(1, n + 1):
        xx = x1 + (x2 - x1) * i / n
        d += f'Q{f(xx - (x2 - x1) / n / 2)} {f(y + (amp if i % 2 else -amp))} {f(xx)} {f(y)}'
    return path(d, t, dur, cls)


def palomita(cx, cy, s, t, cls='ln c grueso'):
    return poli([(cx - s, cy), (cx - s * .3, cy + s * .7), (cx + s, cy - s * .8)], t, .25, cls)


def punteado(d, t, dur=.6, cls='ln', dash='16 12', ident=None):
    """Trazo punteado que también se dibuja: la máscara se traza y deja ver la línea punteada debajo.
    `ident` permite volverlo sólido después con data-cls (clase «solido»)."""
    m = uid('pm')
    return (f'<mask id="{m}" maskUnits="userSpaceOnUse" x="-5000" y="-5000" width="15000" height="20000">'
            f'<path d="{d}" pathLength="1" fill="none" stroke="#fff" stroke-width="22" stroke-linecap="round" data-draw="{f(t)} {f(dur)} 1"/></mask>'
            f'<path d="{d}" class="{cls} pt" style="stroke-dasharray:{dash}" mask="url(#{m})"{(" id=" + chr(34) + ident + chr(34)) if ident else ""}/>')


def caja_punteada(x, y, w, h, t, dur=.7, cls='ln', solido=None):
    """Caja en línea punteada («fuera de servicio»); con `solido=t` la línea se vuelve continua en ese segundo."""
    d = f'M{f(x)} {f(y)}H{f(x + w)}V{f(y + h)}H{f(x)}Z'
    out = punteado(d, t, dur, cls)
    if solido is not None:
        out = out.replace(' pt"', f' pt" data-cls="{f(solido)} solido"', 1)
    return out


# ── figuras ─────────────────────────────────────────────────────────────────────────────────────────────
def servidor_frente(x, y, w, h, t, dur=1.0, cls='ln', unidades=9, leds=True):
    """Rack en alzado: marco, unidades, rejillas y LEDs, dibujados en cascada."""
    out = rect(x, y, w, h, t, dur * .35, cls + ' grueso')
    uh = (h - 40) / unidades
    for i in range(unidades):
        yy = y + 20 + i * uh
        ti = t + dur * .3 + i * dur * .6 / unidades
        out += rect(x + 22, yy + 4, w - 44, uh - 8, ti, .2, cls + ' fino')
        out += linea(x + 40, yy + uh / 2, x + w * .52, yy + uh / 2, ti + .05, .15, cls + ' fino')
        if leds:
            out += circ(x + w - 52, yy + uh / 2, 6, ti + .1, .12, 'ln c')
            out += circ(x + w - 78, yy + uh / 2, 6, ti + .12, .12, 'ln c')
    return out


def iso_pts(x, y, W, Hh):
    dx, dy = W * .866, W * .5
    A, B, C, D = (x, y), (x + dx, y - dy), (x, y - 2 * dy), (x - dx, y - dy)
    A2, B2, D2 = (x, y + Hh), (x + dx, y - dy + Hh), (x - dx, y - dy + Hh)
    return A, B, C, D, A2, B2, D2


def servidor_iso(x, y, t, W=90, Hh=150, cls='ln', dur=.45, ranuras=4):
    """Servidor en isométrico (línea). (x,y) = vértice frontal de arriba."""
    A, B, C, D, A2, B2, D2 = iso_pts(x, y, W, Hh)
    out = poli([A, B, C, D], t, dur * .45, cls, cerrar=True)
    out += poli([D, D2, A2, B2, B], t + dur * .3, dur * .55, cls)
    out += linea(*A, *A2, t + dur * .3, dur * .4, cls)
    for i in range(1, ranuras + 1):
        k = Hh * i / (ranuras + 1)
        out += linea(A[0] + 8, A[1] + k - 4, B[0] - 6, B[1] + k - 4 + 3, t + dur * .6 + i * .03, .15, cls + ' fino')
        out += linea(D[0] + 6, D[1] + k - 4 + 3, A[0] - 8, A[1] + k - 4, t + dur * .6 + i * .03, .15, cls + ' fino')
    return out


def interruptor(x, y, t, keys, cls='ln grueso', largo=150, cables=110, dur=.5):
    """Esquemático de un interruptor: cable — o  /o — cable. `keys` = [[ángulo0], [t, d, ángulo], …] (grados; -32 = abierto)."""
    out = linea(x - cables, y, x - 10, y, t, dur * .4, cls)
    out += circ(x, y, 10, t + dur * .3, .15, cls)
    out += circ(x + largo, y, 10, t + dur * .35, .15, cls)
    out += linea(x + largo + 10, y, x + largo + cables, y, t + dur * .45, dur * .4, cls)
    palanca = linea(x + 8, y, x + largo - 2, y, t + dur * .5, .25, cls)
    return out + f'<g data-rk=\'{json.dumps([[x, y]] + keys)}\'>{palanca}</g>'


def sobre(x, y, w, t, dur=.22, cls='ln'):
    h = w * .64
    return rect(x, y, w, h, t, dur, cls) + poli([(x, y), (x + w / 2, y + h * .55), (x + w, y)], t + dur * .5, dur, cls)


def reloj(cx, cy, r, t, sweep_t, sweep_d, frac=.75, cls='ln'):
    """Reloj: carátula, marcas, sector rojo que se barre (frac de vuelta) y manecilla que lo sigue."""
    out = circ(cx, cy, r, t, .4, cls + ' grueso')
    for i in range(12):
        a = math.radians(i * 30 - 90)
        r1 = r - (22 if i % 3 == 0 else 12)
        out += linea(cx + r1 * math.cos(a), cy + r1 * math.sin(a), cx + (r - 4) * math.cos(a), cy + (r - 4) * math.sin(a), t + .1 + i * .015, .1, cls)
    out += path(arco_d(cx, cy, r * .42), sweep_t, sweep_d, 'sector', frac).replace('pathLength="1"', f'pathLength="1" style="stroke-width:{f(r * .84)}"')
    man = linea(cx, cy, cx, cy - r * .82, t + .3, .2, cls + ' grueso')
    out += f'<g data-rk=\'{json.dumps([[cx, cy], [0], [sweep_t, sweep_d, frac * 360, "l"]])}\'>{man}</g>'
    out += circ(cx, cy, 8, t + .3, .1, cls + ' grueso')
    return out


def codigo(x, y, lineas, t, size=28, cls='ln', w=None, cps=40, gap=.25):
    """Caja de código con líneas que se teclean."""
    lh = size * 1.45
    w = w or max(ancho(l, size) for l in lineas) + 60
    h = lh * len(lineas) + 36
    out = rect(x, y, w, h, t, .4, cls)
    tt = t + .3
    for i, l in enumerate(lineas):
        out += texto(x + 30, y + 18 + lh * (i + .75), l, tt, size, 'mono', cls='fc' if l.lstrip().startswith(('if', 'else', 'def')) else '', cps=cps)
        tt += len(l) / cps + gap
    return out


def campana(cx, cy, s, t, cls='ln'):
    d = (f'M{f(cx - s)} {f(cy + s * .6)}Q{f(cx - s * .8)} {f(cy + s * .2)} {f(cx - s * .7)} {f(cy - s * .3)}'
         f'Q{f(cx - s * .6)} {f(cy - s)} {f(cx)} {f(cy - s)}Q{f(cx + s * .6)} {f(cy - s)} {f(cx + s * .7)} {f(cy - s * .3)}'
         f'Q{f(cx + s * .8)} {f(cy + s * .2)} {f(cx + s)} {f(cy + s * .6)}Z')
    return path(d, t, .5, cls) + circ(cx, cy + s * .78, s * .16, t + .4, .15, cls)


def g(contenido, pop=None, on=None, mv=None, rot=None, cls=None, jit=None, blink=None, sello_t=None, extra=''):
    """Grupo animado. pop=(t,d) · on=(t0[,t1]) · mv=[[x,y],[t,d,x,y],…] · rot=[[cx,cy],[a],[t,d,a],…] ·
    cls=(t, clase) · jit=(t0,t1,amp) · blink=(t0,t1,periodo)."""
    a = []
    if pop:
        a.append(f'class="pp" data-pop="{f(pop[0])} {f(pop[1])}"')
    if on:
        a.append(f'data-on="{" ".join(f(v) for v in on)}"')
    if mv:
        a.append(f"data-mv='{json.dumps(mv)}'")
    if rot:
        a.append(f"data-rk='{json.dumps(rot)}'")
    if cls:
        a.append(f'data-cls="{f(cls[0])} {cls[1]}"')
    if jit:
        a.append(f'data-jit="{" ".join(f(v) for v in jit)}"')
    if blink:
        a.append(f'data-blink="{" ".join(f(v) for v in blink)}"')
    if sello_t is not None:
        a.append(f'class="pp" data-sello="{f(sello_t)}"')
    return f'<g {" ".join(a)} {extra}>{contenido}</g>'


# ── página ──────────────────────────────────────────────────────────────────────────────────────────────
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#0b3a7e;-webkit-font-smoothing:antialiased;font-synthesis:none}
.fondo{position:absolute;inset:0;background:radial-gradient(1400px 1800px at 50% 38%,#1a5bb5,#0c3a80 58%,#072653)}
.ruido{position:absolute;inset:0;opacity:.22;mix-blend-mode:soft-light;pointer-events:none;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' seed='4'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)'/%3E%3C/svg%3E")}
.pliegue{position:absolute;pointer-events:none;background:linear-gradient(90deg,transparent,rgba(255,255,255,.05),rgba(0,0,0,.08),transparent)}
svg.capa{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:visible}
.ln{fill:none;stroke:#eaf4ff;stroke-width:3.4;stroke-linecap:round;stroke-linejoin:round}
.ln.fino{stroke-width:1.8}.ln.grueso{stroke-width:6}.ln.c{stroke:#7fe3ff}.ln.r{stroke:#ff5a4f}.ln.a{stroke:#ffd166}.ln.tenue{stroke:rgba(234,244,255,.45)}
.ln.pt.solido{stroke-dasharray:none!important}
.sector{fill:none;stroke:rgba(255,90,79,.55)}
.mono{font-family:'IBM Plex Mono',monospace;font-weight:600;fill:#eaf4ff;letter-spacing:.01em}
.bc{font-family:'Barlow Condensed',sans-serif;font-weight:800;fill:#eaf4ff;letter-spacing:.005em}
.nota{font-family:'Architects Daughter',cursive;fill:#eaf4ff}
.tz{fill:transparent;stroke:#eaf4ff;stroke-width:3;stroke-linejoin:round;paint-order:stroke}
.tz.lleno{fill:#eaf4ff}.tz.hatch.lleno{fill:url(#ht)}.tz.r{stroke:#ff5a4f}.tz.r.lleno{fill:#ff5a4f}.tz.c{stroke:#7fe3ff}.tz.c.lleno{fill:#7fe3ff}
.tz.r.hatch.lleno{fill:url(#htr)}
.fr{fill:#ff5a4f}.fc{fill:#7fe3ff}.fa{fill:#ffd166}.ft{fill:rgba(234,244,255,.55)}
.pp{transform-box:fill-box;transform-origin:center}
.tapa{fill:#0f4590}
"""

RUNTIME = r"""
const CPS=%(cps)d,_Q=1000/CPS;window.__cps=CPS;
const cl=x=>x<0?0:x>1?1:x,eio=p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2,ei=p=>p*p*p,eo=p=>1-Math.pow(1-p,3),EZ={io:eio,i:ei,o:eo,l:p=>p};
const bk=p=>{const c=2.1;return 1+(c+1)*Math.pow(p-1,3)+c*Math.pow(p-1,2)};
const hs=i=>{const x=Math.sin(i*12.9898+78.233)*43758.5453;return x-Math.floor(x)};
const K=(k,T)=>{let v=k[0].slice();for(const s of k.slice(1)){const w=s.slice(2);const e=typeof w[w.length-1]==='string'?EZ[w.pop()]:eio;
  const p=e(cl((T-s[0])/(s[1]||1e-6)));v=v.map((x,i)=>x+(w[i]-x)*p)}return v};
const Q=a=>[...document.querySelectorAll('['+a+']')].map(e=>[e,e.getAttribute(a)]);
const N=v=>v.split(' ').map(Number);
const DR=Q('data-draw').map(([e,v])=>[e,...N(v)]),PO=Q('data-pop').map(([e,v])=>[e,...N(v)]),SE=Q('data-sello').map(([e,v])=>[e,+v]);
const ON=Q('data-on').map(([e,v])=>[e,...N(v)]),TY=Q('data-type').map(([e,v])=>[e,...N(v),e.dataset.full]);
const RK=Q('data-rk').map(([e,v])=>{const k=JSON.parse(v);return [e,k[0],k.slice(1)]}),MV=Q('data-mv').map(([e,v])=>[e,JSON.parse(v)]);
const CL=Q('data-cls').map(([e,v])=>{const [t,c]=v.split(' ');return [e,+t,c]}),NU=Q('data-n').map(([e,v])=>[e,...v.split(' ')]);
const JI=Q('data-jit').map(([e,v])=>[e,...N(v)]),BL=Q('data-blink').map(([e,v])=>[e,...N(v)]);
const cam=document.getElementById('cam');
const fmt=(v,f)=>f==='c'?Math.round(v).toLocaleString('en-US'):Math.round(v)+'';
window.__seek=s=>{const ms=Math.floor(s*1000/_Q+1e-6)*_Q,T=ms/1000+S0,fr=Math.round(T*CPS);
 const vis=(e,b)=>{e.style.display=b?'':'none'};  // display (no visibility): un grupo oculto oculta a sus hijos aunque ellos estén «visibles»
 for(const [e,t,d,fr_,L] of DR){if(T<=t){vis(e,0);continue}vis(e,1);const p=eio(cl((T-t)/d));
   e.style.strokeDasharray=p>=1?'none':(L?(p*L)+'px '+(2*L)+'px':(p*fr_)+' 3');if(p>=1&&fr_<1)e.style.strokeDasharray=fr_+' 3'}
 for(const [e,t,d] of PO){if(T<t){vis(e,0);continue}vis(e,1);const p=cl((T-t)/d);e.style.transform=p>=1?'none':'scale('+Math.max(.001,bk(p))+')'}
 for(const [e,t] of SE){if(T<t){vis(e,0);continue}vis(e,1);const p=cl((T-t)/.2);e.style.transform=p>=1?'none':'scale('+(1+(1-eo(p))*1.3)+') rotate('+((1-p)*6)+'deg)'}
 for(const [e,t0,t1] of ON)vis(e,T>=t0&&!(t1>0&&T>=t1));
 for(const [e,t,c,full] of TY){const n=T<t?0:Math.min(full.length,Math.floor((T-t)*c)+1);e.textContent=full.slice(0,n);vis(e,n>0)}
 for(const [e,[cx,cy],k] of RK)e.setAttribute('transform','rotate('+K(k,T)[0]+' '+cx+' '+cy+')');
 for(const [e,k] of MV){const [x,y,sc]=K(k,T);e.setAttribute('transform','translate('+x+' '+y+')'+(sc!=null?' scale('+sc+')':''))}
 for(const [e,t,c] of CL)e.classList.toggle(c,T>=t);
 for(const [e,t,d,a,b,f] of NU){const p=eio(cl((T-+t)/+d));e.textContent=(e.dataset.pre||'')+fmt(+a+(+b-+a)*p,f)+(e.dataset.suf||'')}
 for(const [e,t0,t1,a] of JI){const on=T>=t0&&T<t1;e.setAttribute('transform',on?'translate('+((hs(fr)-.5)*a)+' '+((hs(fr+7)-.5)*a)+')':'')}
 for(const [e,t0,t1,p] of BL)vis(e,T>=t0&&(T>=t1||Math.floor((T-t0)/p)%%2===0));
 const [cx,cy,sc]=K(CAM,T);cam.setAttribute('transform','translate(540 960) scale('+sc+') translate('+(-cx)+' '+(-cy)+')');
};
const _F=['800 100px "Barlow Condensed"','600 100px "IBM Plex Mono"','400 100px "IBM Plex Mono"','400 100px "Architects Daughter"'];
window.__listo=Promise.all(_F.map(f=>document.fonts.load(f))).then(()=>document.fonts.ready).then(()=>{const m=_F.filter(f=>!document.fonts.check(f));if(m.length)throw new Error('faltan fuentes: '+m)}).then(()=>window.__seek(0));
window.__seek(0);
"""

DEFS = """<defs>
<pattern id="gm" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="rgba(234,244,255,.075)" stroke-width="1"/></pattern>
<pattern id="gM" width="120" height="120" patternUnits="userSpaceOnUse"><rect width="120" height="120" fill="url(#gm)"/><path d="M120 0H0V120" fill="none" stroke="rgba(234,244,255,.16)" stroke-width="1.6"/></pattern>
<pattern id="ht" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="12" height="12" fill="rgba(234,244,255,.18)"/><line x1="0" y1="0" x2="0" y2="12" stroke="#eaf4ff" stroke-width="4"/></pattern>
<pattern id="htr" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="12" height="12" fill="rgba(255,90,79,.2)"/><line x1="0" y1="0" x2="0" y2="12" stroke="#ff5a4f" stroke-width="4"/></pattern>
</defs>"""


def cajetin(hoja, total, t=None, serie='ARCHIVO', num='#01', titulo='KNIGHT CAPITAL', anio='2012'):
    """Cajetín fijo arriba (no se mueve con la cámara). Con t se dibuja; sin t ya está puesto."""
    T = -99 if t is None else t
    k = (lambda i: T + i * .05) if t is not None else (lambda i: -99)
    out = rect(24, 24, 1032, 1872, k(0), .6, 'ln tenue fino')
    out += rect(44, 44, 640, 132, k(1), .45, 'ln')
    out += linea(310, 44, 310, 176, k(3), .2, 'ln fino') + linea(310, 110, 684, 110, k(4), .2, 'ln fino')
    modo = 'fijo' if t is None else 'escribe'
    out += texto(62, 70, 'SERIE', k(5), 17, 'mono', modo=modo, cls='ft')
    out += texto(60, 150, serie, k(6), 74, 'big', modo=modo)
    out += texto(328, 92, f'{num} · {titulo}', k(7), 25, 'mono', modo=modo)
    out += texto(328, 154, f'HOJA {hoja:02d}/{total:02d} · {anio}', k(8), 22, 'mono', modo=modo, cls='fc', peso=400)
    # escala gráfica y marca de revisión (decorativas)
    x0 = 720
    for i in range(4):
        out += rect(x0 + i * 60, 132, 60, 14, k(9 + i), .15, 'ln fino')
        if i % 2 == 0:
            out += g(f'<rect x="{x0 + i * 60}" y="132" width="60" height="14" fill="#eaf4ff" opacity=".7"/>', on=(k(10 + i),))
    out += texto(x0, 120, 'ESC. 1:1 · m', k(14), 18, 'mono', modo=modo, cls='ft', peso=400)
    out += texto(x0, 170, '0       1       2', k(15), 16, 'mono', modo=modo, cls='ft', peso=400)
    out += circ(980, 92, 34, k(16), .3, 'ln fino') + linea(980, 46, 980, 138, k(17), .2, 'ln fino') + linea(934, 92, 1026, 92, k(17), .2, 'ln fino')
    out += texto(980, 64, 'N', k(18), 18, 'mono', 'middle', modo=modo, cls='ft')
    return out


def page(S0, dur, mundo, cam, hoja, total, chrome_t=None, fijo='', titulo='KNIGHT CAPITAL', anio='2012', num='#01'):
    """Página a pantalla completa. cam = [[cx,cy,s], [t,d,cx,cy,s(,'i'|'o'|'io'|'l')], …] en tiempo global."""
    caj = cajetin(hoja, total, chrome_t, titulo=titulo, anio=anio, num=num)
    body = (f'<div class="fondo"></div>'
            f'<svg class="capa" viewBox="0 0 1080 1920">{DEFS}<g id="cam">'
            f'<rect x="-8000" y="-8000" width="22000" height="26000" fill="url(#gM)"/>{mundo}</g></svg>'
            f'<div class="ruido"></div>'
            f'<svg class="capa" viewBox="0 0 1080 1920">{caj}{fijo}</svg>')
    js = f'const S0={S0},DUR={dur},CAM={json.dumps(cam)};' + RUNTIME % {'cps': CPS}
    return (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{CSS}</style></head>'
            f'<body>{body}<script>{js}</script></body></html>')


def barrido(S, E, c_ini, c_fin, desde=(0, -2160), hacia=(0, 2160), entra=.42, sale=.36, sin_entrada=False):
    """Cámara de una página: llega barriendo desde `desde` (relativo a c_ini) y se va barriendo hacia `hacia`.
    Las distancias son múltiplos de 120 → la retícula coincide en el corte entre páginas.
    Devuelve (inicio, entrada, salida) para intercalar movimientos propios en medio."""
    cx, cy, s = c_ini
    ini = [cx, cy, s] if sin_entrada else [cx + desde[0], cy + desde[1], s]
    ent = [] if sin_entrada else [[S, entra, cx, cy, s, 'o']]
    fx, fy, fs = c_fin
    sal = [[E - sale, sale, fx + hacia[0], fy + hacia[1], fs, 'i']]
    return ini, ent, sal


def subtitulos(G, dur, y=1425, ocultar=()):
    """Capa transparente: cada grupo es una etiqueta de anotación técnica (caja con esquinas marcadas y «REF.»),
    palabra activa en ámbar y subrayada. Cambia de golpe (10 cps), sin fundidos."""
    data = json.dumps([dict(i=round(g_['ini'], 2), f=round(g_['fin'], 2), w=[[H.escape(w), round(a, 2)] for w, a, *_ in g_['w']]) for g_ in G], ensure_ascii=False)
    css = ("*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1920px;overflow:hidden;background:transparent}"
           f"#z{{position:absolute;left:60px;right:140px;top:{y - 110}px;height:220px;display:flex;align-items:center;justify-content:center}}"
           "#b{position:relative;display:none;padding:20px 34px 22px;background:rgba(9,42,98,.93);border:3px solid #eaf4ff;"
           "font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:54px;line-height:1.1;color:#eaf4ff;text-align:center;max-width:880px}"
           "#b:before{content:'REF.';position:absolute;left:-3px;top:-34px;font-size:20px;letter-spacing:.12em;color:#7fe3ff;font-weight:600}"
           "#b:after{content:'';position:absolute;left:-18px;top:50%;width:18px;border-top:3px solid #eaf4ff}"
           ".k{position:absolute;width:16px;height:16px;border-color:#7fe3ff;border-style:solid}"
           ".k1{left:-10px;top:-10px;border-width:4px 0 0 4px}.k2{right:-10px;top:-10px;border-width:4px 4px 0 0}"
           ".k3{left:-10px;bottom:-10px;border-width:0 0 4px 4px}.k4{right:-10px;bottom:-10px;border-width:0 4px 4px 0}"
           "#b i{font-style:normal;padding:0 .06em}#b i.on{color:#ffd166;text-decoration:underline;text-decoration-thickness:4px;text-underline-offset:8px}"
           "#d{position:absolute;left:12px;top:50%;width:14px;height:14px;margin-top:-7px;border-radius:50%;background:#eaf4ff;display:none}")
    js = (f"const G={data},O={json.dumps(list(ocultar))};const b=document.getElementById('b'),t=document.getElementById('t'),d=document.getElementById('d');"
          "window.__cps=10;window.__seek=s=>{s=Math.floor(s*10+1e-6)/10;"
          "const k=G.findIndex(g=>s>=g.i&&s<g.f);if(k<0||O.some(([a,c])=>s>=a&&s<c)){b.style.display='none';d.style.display='none';return}"
          "const g=G[k];let on=-1;g.w.forEach(([w,a],j)=>{if(s>=a-.05)on=j});b.style.display='inline-block';d.style.display='block';"
          "t.innerHTML=g.w.map(([w],j)=>`<i class=\"${j===on?'on':''}\">${w}</i>`).join(' ')};"
          "const _F=['600 54px \"IBM Plex Mono\"'];window.__listo=Promise.all(_F.map(f=>document.fonts.load(f))).then(()=>document.fonts.ready)"
          ".then(()=>{const m=_F.filter(f=>!document.fonts.check(f));if(m.length)throw new Error('faltan fuentes: '+m)});window.__seek(0);")
    return (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{css}</style></head><body>'
            f'<div id="z"><div id="d"></div><div id="b"><span class="k k1"></span><span class="k k2"></span><span class="k k3"></span><span class="k k4"></span>'
            f'<span id="t"></span></div></div><script>{js}</script></body></html>')
