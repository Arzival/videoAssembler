"""El Log #04 · diseño «Trayecto» (prueba): gloss 2 + widget oscuro de ruta. Cada noticia es un tramo del viaje:
tarjeta casi negra con resplandor de color arriba, cabecera (icono + etiqueta, anillo de progreso, botón contorneado
«Siguiente ▸»), dos métricas grandes en lila con etiquetas diminutas, barra de progreso con degradado y tirador blanco,
tres columnas de microtexto, pie con «paradas» marcadas por una línea de color y dos miniaturas. Detrás asoman,
apiladas como baraja, las píldoras de las próximas noticias con su minuto. El objeto 3D va debajo de la tarjeta.
Misma voz y tiempos que «Destino» (ellog-04-destino.py); reutiliza de ahí la cinta, el 3D y la tarjeta «Sígueme».
Barras, anillos y contadores se mueven con data-k / data-r / data-n (claves [[t, valor], [t, valor, duración], …] en segundos del video).
Uso: SALIDA=noticias/4/trayecto REL=noticias/4/trayecto python3 ejemplos/ellog-04-trayecto.py [ids…]   (SOLO_HTML=1 para revisar)
"""
import importlib.util, json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import ellog_gloss as G
from ellog_gloss import js

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('destino', os.path.join(HERE, 'ellog-04-destino.py'))
D = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(D)

CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.getcwd()))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
FIN, TOP, LIB = D.FIN, D.TOP, D.LIB
ICON = dict(D.ICON, foot='<path d="M4 16v-2.38C4 11.5 2.97 10.5 3 8c.03-2.72 1.49-6 4.5-6C9.37 2 10 3.8 10 5.5c0 3.11-2 5.66-2 8.68V16a2 2 0 1 1-4 0ZM20 20v-2.38c0-2.12 1.03-3.12 1-5.62-.03-2.72-1.49-6-4.5-6C14.63 6 14 7.8 14 9.5c0 3.11 2 5.66 2 8.68V20a2 2 0 1 0 4 0Z"/>')


def ic(n):
    return f'<svg class="ico" viewBox="0 0 24 24">{ICON[n]}</svg>'


TCSS = """
@property --on{syntax:'<number>';inherits:true;initial-value:0}
@keyframes tOn{to{--on:1}}@keyframes tOff{to{--on:0}}
.tr{position:absolute;border-radius:calc(var(--k)*24px);padding:calc(var(--k)*22px) calc(var(--k)*24px);color:#e9e9eb;
  background:radial-gradient(60% 60% at 50% -8%,rgba(var(--acr),.62),rgba(var(--acr),.14) 45%,transparent 75%),#0d0b10;
  box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.16),inset 0 1.5px 0 rgba(255,255,255,.12),0 40px 90px rgba(0,0,0,.6),0 0 90px rgba(var(--acr),.2);
  animation:cardIn .8s cubic-bezier(.22,1.15,.36,1) both}
@keyframes cardIn{from{opacity:0;transform:translateY(140px) scale(.94)}to{opacity:1;transform:none}}
.tr .h2{display:flex;align-items:center;justify-content:space-between;gap:calc(var(--k)*10px)}
.tr .who{flex:1;display:flex;align-items:center;gap:calc(var(--k)*9px);font-size:calc(var(--k)*14px);font-weight:500;color:#e9e9eb;white-space:nowrap}
.tr .who svg{width:calc(var(--k)*18px);height:calc(var(--k)*18px)}.tr .who .em{font-size:calc(var(--k)*17px)}
.ico{width:calc(var(--k)*16px);height:calc(var(--k)*16px);fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;flex-shrink:0}
.rg{position:relative;width:calc(var(--k)*38px);height:calc(var(--k)*38px);flex-shrink:0}
.rg svg{width:100%;height:100%;transform:rotate(-90deg)}.rg circle{fill:none;stroke-width:2.6}.rg .b{stroke:rgba(255,255,255,.14)}
.rg .f{stroke:var(--ac2);stroke-linecap:round;stroke-dasharray:100;stroke-dashoffset:100;filter:drop-shadow(0 0 4px rgba(var(--acr),.8))}
.rg span{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:calc(var(--k)*9.5px);font-weight:600;color:#e9e9eb}
.nx{flex:1;display:flex;justify-content:flex-end}
.nx b{display:inline-flex;align-items:center;gap:calc(var(--k)*6px);padding:calc(var(--k)*7px) calc(var(--k)*13px);border-radius:999px;font-size:calc(var(--k)*11px);font-weight:500;white-space:nowrap;
  box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.45);animation:nxTap .45s ease var(--td,999s) both}
@keyframes nxTap{40%{transform:scale(.9);background:#fff;color:#0d0b10}to{background:#fff;color:#0d0b10}}
.ms{display:flex;justify-content:space-between;align-items:flex-end;margin-top:calc(var(--k)*14px);gap:calc(var(--k)*12px)}
.ms .r{text-align:right}
.ms small{display:block;font-size:calc(var(--k)*10px);color:#8b8794;font-weight:500;margin-bottom:calc(var(--k)*3px)}
.ms .v{font-size:calc(var(--k)*26px);font-weight:300;letter-spacing:-.025em;line-height:1.05;color:var(--ac2);white-space:nowrap}
.ms .v b{font-weight:500}
.sw{display:inline-grid}.sw>span{grid-area:1/1;opacity:var(--on)}.ms .r .sw>span{justify-self:end}
.br{position:relative;height:calc(var(--k)*16px);border-radius:999px;background:#2a2233;margin-top:calc(var(--k)*14px)}
.br .fl{position:absolute;left:0;top:0;bottom:0;width:0;min-width:calc(var(--k)*16px);border-radius:999px;background:linear-gradient(90deg,var(--ac0,var(--ac)),var(--ac2))}
.br .fl:after{content:'';position:absolute;right:calc(var(--k)*-4px);top:50%;width:calc(var(--k)*21px);height:calc(var(--k)*21px);margin-top:calc(var(--k)*-10.5px);border-radius:50%;
  background:#fff;box-shadow:0 0 0 calc(var(--k)*5px) rgba(255,255,255,.22),0 0 calc(var(--k)*16px) rgba(var(--acr),.9)}
.cl{display:flex;justify-content:space-between;margin-top:calc(var(--k)*9px);font-size:calc(var(--k)*10px);color:#8b8794;font-weight:500}
.cl>div:nth-child(2){text-align:center}.cl>div:last-child{text-align:right}
.cl b{display:block;font-size:calc(var(--k)*12.5px);color:#e9e9eb;font-weight:500;margin-top:calc(var(--k)*2px)}
.ft{display:flex;align-items:center;justify-content:space-between;margin-top:calc(var(--k)*18px);gap:calc(var(--k)*12px)}
.stp{border-left:2px solid var(--ac);padding-left:calc(var(--k)*11px);display:grid;gap:calc(var(--k)*4px)}
.stp div{font-size:calc(var(--k)*13px);font-weight:500;color:#f4f4f5;white-space:nowrap}.stp small{font-size:calc(var(--k)*10px);color:#8b8794;margin-right:calc(var(--k)*8px)}
.th{display:flex;gap:calc(var(--k)*7px)}
.th i{width:calc(var(--k)*46px);height:calc(var(--k)*46px);border-radius:calc(var(--k)*9px);display:flex;align-items:center;justify-content:center;font-style:normal;font-size:calc(var(--k)*22px);font-weight:800;
  box-shadow:inset 0 0 0 1px rgba(255,255,255,.15)}.th i svg{width:55%;height:55%}
.dk{position:absolute;left:50%;height:calc(var(--k)*38px);border-radius:999px;display:flex;align-items:center;justify-content:space-between;padding:0 calc(var(--k)*16px);
  font-size:calc(var(--k)*12.5px);font-weight:500;color:#e9e9eb;white-space:nowrap;
  background:radial-gradient(50% 120% at 50% 100%,rgba(var(--acr),.45),transparent 70%),#0d0b10;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.18),0 20px 40px rgba(0,0,0,.45);
  animation:dkIn .6s cubic-bezier(.22,1.2,.36,1) both}
.dk span{display:inline-flex;align-items:center;gap:calc(var(--k)*9px)}.dk em{font-style:normal;color:#a8a3b3}
@keyframes dkIn{from{opacity:0;transform:translate(-50%,40px)}to{opacity:1;transform:translateX(-50%)}}
.below{position:absolute;left:0;right:0;text-align:center;z-index:9}.below .pill{font-size:36px;padding:20px 40px}
.mk{position:relative;display:inline-block}
"""

TRJS = """const _e=p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2;
const _v=(k,t)=>{let v=k[0][1];for(const [a,b,d] of k.slice(1)){const p=Math.min(1,Math.max(0,(t-a)/(d||.8)));v=v+(b-v)*_e(p)}return v};
const _f=(v,f)=>f==='c'?Math.round(v).toLocaleString('en-US'):f==='p'?Math.round(v)+'%':f==='d'?v.toFixed(0):Math.round(v);
const _K=[...document.querySelectorAll('[data-k]')].map(e=>[e,JSON.parse(e.dataset.k)]),_R=[...document.querySelectorAll('[data-r]')].map(e=>[e,JSON.parse(e.dataset.r)]),
_N=[...document.querySelectorAll('[data-n]')].map(e=>[e,JSON.parse(e.dataset.n)]);
window.__cnt=t=>{t+=S0;for(const [e,k] of _K)e.style.width=_v(k,t)+'%';for(const [e,k] of _R)e.style.strokeDashoffset=100-_v(k,t);
 for(const [e,k] of _N)e.textContent=(e.dataset.pre||'')+_f(_v(k,t),e.dataset.f)+(e.dataset.suf||'')};"""

RGDEF = '<svg width="0" height="0" style="position:absolute"><defs><linearGradient id="rgG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="currentColor"/></linearGradient></defs></svg>'


def win(ws, A):
    out = []
    for a, b in ws:
        out.append(f'tOn .25s ease {A(a)} forwards')
        if b:
            out.append(f'tOff .25s ease {A(b)} forwards')
    return 'animation:' + ','.join(out)


def sw(A, *items):
    """Valor que cambia: (html, [(entra, sale|None)…]) apilados en la misma celda."""
    return '<span class="sw">' + ''.join(f'<span style="{win(ws, A)}">{h}</span>' for h, ws in items) + '</span>'


def K(*keys):
    return js([list(k) for k in keys])


def pop(t, A):
    return f' class="pop" style="animation-delay:{A(t)}"'


def tray(x, y, w, k, pal, d, A, icon, label, ring=None, btn=None, mL=None, mR=None, bar=None, cols=None, stops=None, thumbs=None, z=9, ac0=None):
    """Tarjeta de ruta. ring=(texto, claves %); btn=(texto, t_tap); mL/mR=(etiqueta, valor, t|None); bar=claves %;
    cols=[(etiqueta, valor, t|None)×3]; stops=[(etiqueta, valor, t)]; thumbs=[(html, fondo, t)]."""
    c1, c2, ac, ac2, acr, ink = G.PALETAS[pal]
    st = f'left:{x}px;top:{y}px;width:{w}px;--k:{k};--ac:{ac};--ac2:{ac2};--acr:{acr};color:{ac};z-index:{z};animation-delay:{A(d)}' + (f';--ac0:{ac0}' if ac0 else '')
    h = f'<div class="h2"><div class="who">{icon}<span>{label}</span></div>'
    if ring:
        h += (f'<div class="rg"><svg viewBox="0 0 36 36"><circle class="b" cx="18" cy="18" r="15.5"/><circle class="f" cx="18" cy="18" r="15.5" pathLength="100" data-r=\'{ring[1]}\'/></svg>'
              f'<span>{ring[0]}</span></div>')
    h += f'<div class="nx">{f"""<b style="--td:{A(btn[1])}">{btn[0]} ▸</b>""" if btn else ""}</div></div>'
    if mL or mR:
        def m(x_, cls):
            if not x_:
                return '<div></div>'
            lb, v, t = x_
            return f'<div class="{cls}{" pop" if t else ""}" style="animation-delay:{A(t or d)}"><small>{lb}</small><div class="v">{v}</div></div>'
        h += f'<div class="ms">{m(mL, "l")}{m(mR, "r")}</div>'
    if bar:
        h += f'<div class="br"><div class="fl" data-k=\'{bar}\'></div></div>'
    if cols:
        h += '<div class="cl">' + ''.join(f'<div{pop(t, A) if t else ""}>{lb}<b>{v}</b></div>' for lb, v, t in cols) + '</div>'
    if stops or thumbs:
        s_ = ''.join(f'<div{pop(t, A)}><small>{lb}</small>{v}</div>' for lb, v, t in (stops or []))
        t_ = ''.join(f'<i class="pop" style="background:{bg};animation-delay:{A(t)}">{ht}</i>' for ht, bg, t in (thumbs or []))
        h += f'<div class="ft"><div class="stp">{s_}</div><div class="th">{t_}</div></div>'
    return f'<div class="tr" style="{st}">{h}</div>'


def baraja(top, k, A, d, items):
    """Píldoras apiladas detrás de la tarjeta (próximas noticias): items = [(icono, texto, minuto, paleta)], de atrás hacia adelante."""
    out = ''
    n = len(items)
    for i, (e, t, mm, pal) in enumerate(items):
        acr = G.PALETAS[pal][4]
        w = [480, 700][i] if n == 2 else 640
        y = top - (n - i) * 78
        out += (f'<div class="dk" style="top:{y}px;width:{w}px;--k:{k};--acr:{acr};z-index:{7 + i};animation-delay:{A(d + i * .12)}">'
                f'<span>{e} {t}</span><em>~{mm}</em></div>')
    return out


PIEZAS = []


def escena(pid, start, end, n, css, body, js3d=None, sigue=True):
    if sigue:
        end += 0.45
    PIEZAS.append((pid, start, end, G.page(TCSS + css, RGDEF + body, end - start, f'const S0={start};' + TRJS, n=n, js3d=js3d, salida=not sigue, t0=start)))


def st(items, S, size=88):
    return G.steps(items, S, top=TOP, size=size)


def fase(n, a, b=None):
    if n == 1:
        return f'.p1{{animation:gone .4s ease {b} forwards}}' if b else ''
    return f'.p{n}{{opacity:0;animation:fade .35s ease {a} forwards' + (f',gone .4s ease {b} forwards' if b else '') + '}'


def gl(name, color='#fff'):
    return G.logo(name, color)


TX, TW, TK = 60, 960, 2.2       # tarjeta principal
CYT = 780                       # su borde superior (las píldoras asoman encima)
SIG = {  # próximas paradas (píldoras de atrás)
    1: [('⚖️', 'OpenAI vs. Apple', '0:28', 'amb'), ('🏛️', '8 estados vs. OpenAI', '0:50', 1)],
    2: [('🏛️', '8 estados vs. OpenAI', '0:50', 1), ('⭐', 'GitHub y sus estrellas', '1:20', 3)],
    3: [('⭐', 'GitHub y sus estrellas', '1:20', 3), ('🎵', 'Música con IA', '1:30', 'pass')],
    4: [('🎵', 'Música con IA', '1:30', 'pass'), ('💬', 'Tu opinión', '1:54', 0)],
    5: [('💬', 'Tu opinión', '1:54', 0)],
}
BG = 'linear-gradient(160deg,{a},{b})'

# ───────── 0:00 · #01 Gemini 4 Argon: la «ruta» es la ventana del descuento (13 oct → 30 nov)
S = 0.0; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 2, 0.2, A, gl('googlegemini'), 'Gemini 4 Argon', ring=('<b data-n=\'' + K((0, 0), (7.6, 4, .9)) + '\' data-f="p">0%</b>', K((0, 0), (7.6, 4, .9))),
          btn=('Siguiente', 27.3),
          mL=('Para', sw(A, ('código <b>pesado</b>', [(3.2, 6.4)]), ('<b>$2</b> / M', [(6.5, None)])), 3.2),
          mR=('Descuento', '<b>−50 %</b>', 6.6),
          bar=K((0, 0), (7.6, 4, .9)),
          cols=[('Lanzamiento', '13 oct', 7.5), ('Hoy', '15 oct', 7.7), ('Fin del descuento', '30 nov', 7.9)],
          stops=[('Para', 'código · ciencias', 10.5), ('Para', 'finanzas · ciberseguridad', 12.0)],
          thumbs=[('💻', BG.format(a='#dbe8ff', b='#6ea8ff'), 10.6), ('🛡️', BG.format(a='#ffd9cc', b='#ff8a6b'), 12.5)])
escena('e00-argon', S, 13.9, 2, '',
       f"""<div class="p1">{st([('Gemini <em>4 Argon</em>', 0.3, 8.5), ('Para lo <em>pesado</em>', 8.6, None)], S, 92)}
{baraja(CYT, TK, A, 0.6, SIG[1])}{c1}</div>""",
LIB + r"""const gm=R.gem(330);R.scene.add(gm);
return t=>{const a=R.eb(R.k(t,.6,.9));gm.scale.setScalar(Math.max(.001,a));R.at(gm,540,1640+12*Math.sin(t*1.6),2);
 gm.rotation.set(.15+.08*Math.sin(t*1.1),(1-a)*3+.5*Math.sin(t*.8)+(t>10.4?.6*R.eio(R.k(t,10.4,.8)):0),.05*Math.sin(t*.9))}""")

# ───────── 0:14 · #01 (parte 2): la ruta App → AI Mode → Antigravity; luego la carrera de modelos
S = 13.9; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 2, 14.1, A, gl('google'), 'Dónde ya está', ring=('<b data-n=\'' + K((0, 0), (14.9, 1, .3), (19.6, 2, .3), (20.8, 3, .3)) + '\'>0</b>/3', K((0, 0), (14.9, 33), (19.6, 66), (20.8, 100))),
          btn=('Siguiente', 27.3),
          mL=('Suscripciones', '<b>Pro</b> · <b>Ultra</b>', 17.6), mR=('Antigravity', 'con <b>Ultra</b>', 20.9),
          bar=K((0, 0), (14.9, 4, .6), (19.6, 50), (20.8, 100)),
          cols=[('Parada 1', 'App de Gemini', 14.9), ('Parada 2', 'AI Mode', 19.6), ('Parada 3', 'Antigravity', 20.8)],
          stops=[('Dentro de', 'la app de Gemini', 15.0), ('Y en', 'Google Search', 19.8)],
          thumbs=[(G.logo('googlegemini', '#fff'), BG.format(a='#6ea8ff', b='#1a3a8a'), 15.2), (G.logo('google', '#fff'), BG.format(a='#4fd2ff', b='#0b4a66'), 19.9)])
RACE = []
for i, (pal, ico, nm, fin, t0) in enumerate([('gris', '<span class="em">🤖</span>', 'Tu modelo', 62, 22.9), (2, gl('googlegemini'), 'Gemini 4 Argon', 100, 23.5)]):
    RACE.append(tray(TX, 640 + i * 400, TW, 1.75, pal, t0, A, ico, nm, ring=(f'<b data-n=\'{K((0, 0), (25.4, fin, 1.6))}\' data-f="p">0%</b>', K((0, 0), (25.4, fin, 1.6))),
                     mL=('Revisando', 'tu código', None), mR=('Precio', '<b>$2</b> / M' if i else 'el de siempre', None),
                     bar=K((0, 0), (25.4, fin, 1.6)), ac0=None))
escena('e01-donde', S, 27.9, 2, fase(1, 0, A(22.2)) + fase(2, A(22.3)),
       f"""<div class="p1">{st([('¿Dónde <em>está</em>?', 14.0, None)], S, 92)}{baraja(CYT, TK, A, 14.3, SIG[1])}{c1}</div>
<div class="p2">{st([('¿Ya usas <em>otro modelo</em>?', 22.4, 25.1), ('Ponlos a <em>competir</em>', 25.2, None)], S, 88)}{''.join(RACE)}
 <div class="below" style="top:1500px"><span class="pill on pop" style="animation-delay:{A(26.3)}">🏁 este es el mes · hasta el 30 nov</span></div></div>""",
LIB + r"""const gm=R.gem(300);R.scene.add(gm);
return t=>{const a=R.eb(R.k(t,14.3,.9)),o=R.eo(R.k(t,22.0,.4));gm.visible=t<22.5;gm.scale.setScalar(Math.max(.001,a*(1-o)));
 R.at(gm,540,1640,2);gm.rotation.set(.15,(1-a)*3+.5*Math.sin(t*.8)+(t>19.6?.6:0)+(t>20.8?.6:0),0)}""")

# ───────── 0:28 · #02 OpenAI → Apple: el tirador «viaja» con los archivos
S = 27.9; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 'amb', 28.1, A, gl('openai'), 'Un ex empleado de OpenAI', ring=('<b data-n=\'' + K((0, 0), (31.3, 100, 1.0)) + '\'>0</b>+', K((0, 0), (31.3, 100, 1.0))),
          btn=('Siguiente', 49.4),
          mL=('Archivos', '<b data-n=\'' + K((0, 0), (31.3, 100, 1.0)) + '\'>0</b>+', 31.2), mR=('Destino', '<b>Apple</b>', 30.1),
          bar=K((0, 0), (30.6, 100, 3.4)),
          cols=[('Salida', 'OpenAI', 30.0), ('Último día', '2 jun', 34.0), ('Llegada', 'Apple', 30.3)],
          stops=[('Contenido', 'dispositivo sin lanzar', 33.4), ('Después', 'presentado a directivos', 35.0)],
          thumbs=[(G.logo('openai', '#fff'), BG.format(a='#3a3a44', b='#121218'), 30.0), (G.logo('apple', '#fff'), BG.format(a='#ffe6c2', b='#ffb340'), 30.3)])
escena('e02-archivos', S, 36.6, 'amb', '', f'<div class="p1">{st([("OpenAI <em>vs.</em> Apple", 28.0, None)], S, 92)}{baraja(CYT, TK, A, 28.4, SIG[2])}{c1}</div>',
LIB + "const OA=" + js(G.svgpath('openai')) + ",AP=" + js(G.svgpath('apple')) + r""";
const oa=R.shape(OA,190,3,R.gloss('#f4f4f6',{roughness:.18}),.5);R.scene.add(oa);
const ap=R.shape(AP,165,3,R.metal('#d9dbe2',{roughness:.14}),.5);R.scene.add(ap);
const sh=[];for(let i=0;i<9;i++){const s=R.sheet(i%2?'#ffb340':'#7aa7ff');s.userData={t:30.6+i*.32,z:(i%3)-1};R.scene.add(s);sh.push(s)}
return t=>{const a=R.eb(R.k(t,28.4,.8)),b=R.eb(R.k(t,29.9,.8)),gl=Math.sin(Math.PI*R.k(t,35.0,.7));
 oa.scale.setScalar(Math.max(.001,a));R.at(oa,250,1640,1);oa.rotation.set(.15,.5*Math.sin(t*.9)+(1-a)*3,0);
 ap.visible=t>29.8;ap.scale.setScalar(Math.max(.001,b*(1+.15*gl)));R.at(ap,830,1640,1);ap.rotation.set(.12,-.45*Math.sin(t*.8)+(1-b)*3,0);
 ap.material.emissive.set('#ffb340');ap.material.emissiveIntensity=.5*gl;
 for(const s of sh){const u=s.userData,p=R.k(t,u.t,1.3),e=R.eio(p);s.visible=p>0&&p<1;
  R.at(s,R.mix(300,780,e),1640-Math.sin(Math.PI*e)*200,3+u.z);s.rotation.set(.3*Math.sin(t*3+u.z),e*2.5,e*1.2+u.z*.3);s.scale.setScalar(Math.max(.001,Math.sin(Math.PI*p)*.9+.1))}}""")

# ───────── 0:37 · #02 (parte 2): cronología judicial; luego el «jaloneo» OpenAI ↔ Apple
S = 36.6; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 'amb', 36.8, A, '<span class="em">⚖️</span>', 'Documento judicial', ring=('oct', K((0, 0), (37.2, 100, 5.0))),
          btn=('Siguiente', 49.4),
          mL=('Demanda', '<b>Apple</b>', 40.7), mR=('Por', '<b>secretos</b>', 42.0),
          bar=K((0, 0), (37.2, 30, 1.2), (40.4, 100, 1.4)),
          cols=[('2 jun', 'se va a Apple', 37.3), ('Apple', 'demanda', 40.7), ('Oct 2026', 'OpenAI responde', 38.6)],
          stops=[('OpenAI', '«circula dentro de Apple»', 38.8), ('Apple', '«no hay evidencia»', 42.6)],
          thumbs=[(G.logo('openai', '#fff'), BG.format(a='#3a3a44', b='#121218'), 38.8), (G.logo('apple', '#fff'), BG.format(a='#ffe6c2', b='#ffb340'), 42.6)])
c2 = tray(TX, 700, TW, TK, 'amb', 43.9, A, '<span class="em">🥊</span>', 'La pelea del hardware de IA', ring=('⚖️', K((0, 0), (48.4, 100, .6))),
          mL=('De un lado', '<b>OpenAI</b>', None), mR=('Del otro', '<b>Apple</b>', None),
          bar=K((0, 50), (44.4, 38, .7), (45.2, 64, .7), (46.0, 42, .7), (46.8, 58, .7), (47.6, 50, .5)),
          cols=[('Su dispositivo', 'de IA', None), ('¿Marketing?', 'no', 47.3), ('Sus', 'dispositivos', None)])
escena('e03-tribunal', S, 49.9, 'amb', fase(1, 0, A(43.6)) + fase(2, A(43.7)) + f"""
.mk:after{{content:'';position:absolute;left:24px;right:24px;top:50%;height:7px;border-radius:4px;background:#ff4d5e;transform:scaleX(0);transform-origin:left;animation:strike .35s ease {A(46.9)} forwards}}
@keyframes strike{{to{{transform:scaleX(1)}}}}""",
       f"""<div class="p1">{st([('Pero <em>ojo</em>', 36.7, None)], S, 92)}{baraja(CYT, TK, A, 37.0, SIG[2])}{c1}</div>
<div class="p2">{st([('¿Puro <em>marketing</em>?', 43.8, 47.2), ('Ya está en los<br><em>tribunales</em>', 47.3, None)], S, 88)}{c2}
 <div class="below" style="top:1260px"><span class="mk pop" style="animation-delay:{A(46.2)}"><span class="pill">📣 la pelea del hardware de IA</span></span></div>
 <div class="below" style="top:1400px"><span class="pill bad stamp" style="font-size:44px;animation-delay:{A(48.7)}">⚖️ en los tribunales</span></div></div>""",
LIB + r"""const gv=R.gavel(250);R.scene.add(gv);
return t=>{const a=R.eb(R.k(t,37.0,.9)),m=R.eio(R.k(t,43.4,.8)),sl=R.k(t,48.2,.5),hit=sl<.6?R.eio(sl/.6):1-R.eo((sl-.6)/.4)*.25;
 const y=R.mix(1640,1640,m),x=R.mix(540,790,m);gv.scale.setScalar(Math.max(.001,a*R.mix(1,.85,m)));R.at(gv,x,y,3);
 gv.rotation.set(.25+.05*Math.sin(t*1.2),R.mix(-.5+.35*Math.sin(t*.8),-.2,m),R.mix(.35,.9,m)-hit*1.3*(t>48.2?1:0))}""")

# ───────── 0:50 · #03 ocho estados: el tirador recorre Iowa → Kansas → Arizona
S = 49.9; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 1, 50.1, A, gl('openai'), 'Demandas a OpenAI', ring=('<b data-n=\'' + K((0, 0), (52.2, 8, 1.4)) + '\'>0</b>', K((0, 0), (52.2, 100, 1.4))),
          btn=('Siguiente', 79.0),
          mL=('Estados', '<b data-n=\'' + K((0, 0), (52.2, 8, 1.4)) + '\'>0</b>', 52.1), mR=('Por', 'menores', 55.5),
          bar=K((0, 0), (58.0, 12, .4), (58.45, 50, .4), (59.0, 100, .5)),
          cols=[('Primera', 'Iowa', 58.06), ('Luego', 'Kansas', 58.47), ('Y', 'Arizona', 59.05)],
          stops=[('También', 'Nebraska · Arkansas', 59.7), ('Y', 'Idaho · Montana · W. Va.', 60.1)],
          thumbs=[('IA', BG.format(a='#ffd9cc', b='#ff8a6b'), 58.1), ('KS', BG.format(a='#ffd9cc', b='#ff8a6b'), 58.5)])
c2 = tray(TX, 720, TW, TK, 1, 61.4, A, '<span class="em">⚠️</span>', 'Los acusan de…', ring=('2', K((0, 0), (61.9, 50, .5), (63.0, 100, .5))),
          mL=('Dañar a', '<b>niños</b>', 61.9), mR=('Engañar sobre', 'su <b>seguridad</b>', 63.0),
          bar=K((0, 0), (61.9, 50, .5), (63.0, 100, .5)), ac0='#ff4d5e',
          cols=[('Acusación 1', 'daño a menores', 61.9), ('', '', None), ('Acusación 2', 'qué tan seguro es', 63.0)])
escena('e04-estados', S, 66.0, 1, fase(1, 0, A(61.1)) + fase(2, A(61.2)),
       f"""<div class="p1">{st([('<em>8 estados</em> demandan<br>a OpenAI', 50.1, None)], S, 86)}{baraja(CYT, TK, A, 50.4, SIG[3])}{c1}</div>
<div class="p2">{st([('Lo <em>acusan</em> de…', 61.3, None)], S, 92)}{c2}</div>""",
LIB + "const OA=" + js(G.svgpath('openai')) + ",SH=" + js(D.SHIELD) + r""";
const oa=R.shape(OA,230,3,R.gloss('#f4f4f6',{roughness:.18}),.5);R.scene.add(oa);
const sh=R.shape(SH,230,5,R.gloss('#8d96a8',{emissive:'#ff2a3a',emissiveIntensity:0,roughness:.16}));R.scene.add(sh);
return t=>{const a=R.eb(R.k(t,51.0,.85)),o=R.eo(R.k(t,60.9,.4)),b=R.eb(R.k(t,63.1,.8)),r=R.k(t,64.3,.5);
 oa.visible=t<61.4;oa.scale.setScalar(Math.max(.001,a*(1-o)));R.at(oa,540,1650,1);oa.rotation.set(.2,(1-a)*3+.6*Math.sin(t*.8),0);
 sh.visible=t>62.9;sh.scale.setScalar(Math.max(.001,b));R.at(sh,540,1500,2);sh.rotation.set(.15,(1-b)*3+.4*Math.sin(t*1.1),r>0&&r<1?Math.sin(t*50)*.06:0);
 sh.material.color.set(r>.5?'#ff8a95':'#8d96a8');sh.material.emissiveIntensity=.45*r}""")

# ───────── 1:06 · #03 (parte 2): ruta «diseño → agentes descontrolados»; si usas su API
S = 66.0; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 1, 66.2, A, '<span class="em">📑</span>', 'Las demandas van…', ring=('↔', K((0, 0), (67.5, 10, .5), (71.2, 100, 1.0))),
          btn=('Siguiente', 79.0),
          mL=('Desde', 'el <b>diseño</b>', 67.5), mR=('Hasta', '<b>agentes</b>', 71.3),
          bar=K((0, 0), (67.5, 10, .5), (68.8, 100, 2.6)), ac0='#ff4d5e',
          cols=[('Inicio', 'diseño del chatbot', 67.5), ('', '', None), ('Lo más reciente', 'agentes sin control', 71.8)])
c2 = tray(TX, CYT, TW, TK, 'gris', 73.4, A, ic('code'), 'Si construyes sobre su API', ring=('API', K((0, 0), (75.2, 100, 2.0))),
          btn=('Siguiente', 79.0),
          mL=('Puede cambiar', '<b>chatbots</b>', 77.8), mR=('y también', '<b>agentes</b>', 78.5),
          bar=K((0, 0), (75.2, 100, 2.0)),
          cols=[('Cómo se', 'diseñan', 75.4), ('Cómo se', 'lanzan', 77.2), ('Cómo se', 'usan', 77.6)],
          stops=[('Python', 'pip install openai', 74.0), ('Node', 'npm i openai', 74.6)],
          thumbs=[('🐍', BG.format(a='#3a3a44', b='#121218'), 74.0), ('⬢', BG.format(a='#3a3a44', b='#121218'), 74.6)])
escena('e05-demandas', S, 79.5, 1, fase(1, 0, A(73.0)) + fase(2, A(73.1)),
       f"""<div class="p1">{st([('Las demandas van…', 66.1, None)], S, 88)}{baraja(CYT, TK, A, 66.4, SIG[3])}{c1}</div>
<div class="p2">{st([('¿Construyes sobre<br>su <em>API</em>?', 73.2, None)], S, 86)}{baraja(CYT, TK, A, 73.4, SIG[3])}{c2}</div>""",
LIB + r"""const rb=R.robot(230);R.scene.add(rb);
return t=>{const a=R.eb(R.k(t,71.1,.8)),o=R.eo(R.k(t,72.8,.35)),c=R.k(t,71.6,.2);
 rb.visible=t>70.9&&t<73.2;rb.scale.setScalar(Math.max(.001,a*(1-o)));R.at(rb,540+(c>0?Math.sin(t*37)*14:0),1610,2);
 rb.rotation.set(.1+(c>0?.25*Math.sin(t*9):0),-.3+(c>0?1.2*Math.sin(t*5.3):0),c>0?.3*Math.sin(t*7.1):0);rb.userData.em.emissiveIntensity=1.6+(c>0?2*Math.abs(Math.sin(t*12)):0)}""")

# ───────── 1:20 · #04 GitHub: la barra se encoge de 2,500 a 24 peticiones (≈1 %)
S = 79.5; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 3, 79.7, A, gl('github'), 'Historial de estrellas', ring=('<b data-n=\'' + K((0, 100), (84.0, 1, 1.1)) + '\' data-f="p">100%</b>', K((0, 100), (84.0, 1, 1.1))),
          btn=('Siguiente', 89.2),
          mL=('Antes', '<b>2,500</b>', 82.0), mR=('Ahora', '<b data-n=\'' + K((0, 2500), (84.0, 24, 1.1)) + '\' data-f="c">2,500</b>', 84.0),
          bar=K((0, 0), (82.2, 100, .8), (84.0, 1, 1.1)),
          cols=[('Peticiones', 'antes', 82.2), ('Repo de', '251K ⭐', 82.7), ('Peticiones', 'ahora', 84.0)])
c2 = tray(TX, CYT, TW, TK, 3, 86.0, A, '<span class="em">👤</span>', 'Ya no dice quién', ring=('✕', K((0, 0), (86.6, 100, .5))),
          btn=('Siguiente', 89.2),
          mL=('Quién te dio ⭐', '<b>oculto</b>', 86.6), mR=('Lo que ves', '<b>tendencia</b>', 88.6),
          bar=K((0, 0), (88.0, 72, 1.0)),
          cols=[('Por', 'semana', 88.2), ('', '', None), ('Por', 'día', 88.5)])
escena('e06-estrellas', S, 89.7, 3, fase(1, 0, A(85.8)) + fase(2, A(85.9)),
       f"""<div class="p1">{st([('GitHub y sus <em>estrellas</em>', 79.6, None)], S, 88)}{baraja(CYT, TK, A, 79.9, SIG[4])}{c1}</div>
<div class="p2">{st([('Ya no dice <em>quién</em>', 86.0, None)], S, 92)}{baraja(CYT, TK, A, 86.1, SIG[4])}{c2}</div>""",
LIB + r"""const sr=R.star(5,170,74,60,R.gloss('#ffd34d',{emissive:'#ffb000',emissiveIntensity:.25,metalness:.3,roughness:.14}));R.scene.add(sr);
return t=>{const a=R.eb(R.k(t,80.0,.9)),p=Math.sin(Math.PI*R.k(t,84.0,.6));
 sr.scale.setScalar(Math.max(.001,a*(1+.12*p)));R.at(sr,540,1640+10*Math.sin(t*1.5),2);sr.rotation.set(.18+.06*Math.sin(t*1.2),(1-a)*3+.55*Math.sin(t*1.2),.08*Math.sin(t*.9))}""")

# ───────── 1:30 · #05 YouTube Music: la tarjeta es un reproductor (la barra avanza al reproducir)
S = 89.7; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 'pass', 89.9, A, gl('youtubemusic'), 'YouTube Music', ring=('IA', K((0, 0), (91.3, 100, .6))),
          btn=('Siguiente', 113.6),
          mL=('Etiqueta', sw(A, ('<b>Fully</b> Gen AI', [(91.3, 94.2)]), ('<b>Partly</b> Gen AI', [(94.3, None)])), 91.3),
          mR=('Aunque sea', sw(A, ('la <b>voz</b>', [(94.9, 95.3)]), ('la <b>composición</b>', [(95.35, None)])), 94.9),
          bar=K((0, 0), (98.8, 34, 1.4)),
          cols=[('Ahora', '0:42', 98.8), ('Visible', 'al reproducir', 98.9), ('Duración', '3:12', 98.8)],
          stops=[('Sonando', 'canción hecha con IA', 97.0), ('Etiqueta', '✨ generada con IA', 98.9)],
          thumbs=[('♪', BG.format(a='#ffd3df', b='#ff5d86'), 97.0), ('✨', BG.format(a='#e9e0ff', b='#a78bfa'), 98.9)])
escena('e07-ytmusic', S, 100.2, 'pass', '', f'<div class="p1">{st([("Música hecha<br>con <em>IA</em>", 89.8, None)], S, 86)}{baraja(CYT, TK, A, 90.1, SIG[4])}{c1}</div>',
LIB + r"""const vy=R.vinyl(210,'#ff2d48');R.scene.add(vy);const V=vy.userData.V;
return t=>{const a=R.eb(R.k(t,90.1,.9)),sp=R.k(t,98.8,.6);vy.scale.setScalar(Math.max(.001,a));R.at(vy,540,1650,1);
 vy.rotation.set(.35+.06*Math.sin(t*1.1),-.35+.2*Math.sin(t*.7)+(1-a)*2.5,0);V.rotation.z=-(t*.6+Math.max(0,t-98.8)*4*sp)}""")

# ───────── 1:40 · #05 (parte 2): Deezer — ruta hasta fin de año; luego YouTube Music vs Deezer
S = 100.2; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 0, 100.4, A, gl('deezer'), 'Deezer · filtro anti-IA', ring=('<b>off</b>', K((0, 0), (103.9, 100, .4))),
          btn=('Siguiente', 113.6),
          mL=('Un botón para', 'quitar la <b>IA</b>', 103.7), mR=('Llega', 'fin de <b>año</b>', 109.5),
          bar=K((0, 0), (106.5, 18, .8)),
          cols=[('Hoy', 'todavía no sale', 106.5), ('', '', None), ('Meta', 'antes de 2027', 109.5)],
          stops=[('Oculta de', 'búsqueda · álbumes', 104.2), ('Y de', 'artistas relacionados', 104.8)],
          thumbs=[('🔎', BG.format(a='#e9e0ff', b='#7c5ce6'), 104.2), ('🎤', BG.format(a='#e9e0ff', b='#7c5ce6'), 104.8)])
c2a = tray(TX, 640, TW, 1.75, 'pass', 110.7, A, gl('youtubemusic'), 'YouTube Music', ring=('✓', K((0, 0), (111.0, 100, .8))),
           mL=('Etiquetas', '<b>ya están</b>', None), mR=('Desde', '14 oct', None), bar=K((0, 0), (111.0, 100, .8)))
c2b = tray(TX, 1040, TW, 1.75, 0, 111.0, A, gl('deezer'), 'Deezer', ring=('⏳', K((0, 0), (111.3, 18, .8))),
           mL=('Filtro', '<b>pronto</b>', None), mR=('Llega', 'fin de año', None), bar=K((0, 0), (111.3, 18, .8)))
escena('e08-deezer', S, 114.1, 0, fase(1, 0, A(110.4)) + fase(2, A(110.5)) + """
.rg span b{font-weight:700}""",
       f"""<div class="p1">{st([('Deezer va<br>más <em>lejos</em>', 100.3, None)], S, 86)}{baraja(CYT, TK, A, 100.6, SIG[5])}{c1}
 <div class="below" style="top:1430px"><span class="pill bad stamp" style="font-size:40px;animation-delay:{A(106.5)}">⏳ todavía no sale</span></div></div>
<div class="p2">{st([('¿Creas música con <em>IA</em>?', 110.6, None)], S, 88)}{c2a}{c2b}
 <div class="below" style="top:1500px"><span class="pill on stamp" style="font-size:40px;--r:-3deg;animation-delay:{A(112.6)}">🏷️ el etiquetado ya viene</span></div></div>""",
LIB + "const DZ=" + js(G.svgpath('deezer')) + r""";
const dz=R.shape(DZ,300,3,R.iri('#d9c9ff',{metalness:.5,roughness:.1,opacity:1,transparent:false,emissive:'#7c5ce6',emissiveIntensity:.2}),.5);R.scene.add(dz);
return t=>{const a=R.eb(R.k(t,100.6,.9)),o=R.eo(R.k(t,110.2,.4));dz.visible=t<110.7;dz.scale.setScalar(Math.max(.001,a*(1-o)));
 R.at(dz,540,1660+10*Math.sin(t*1.4),2);dz.rotation.set(.2+.06*Math.sin(t*1.2),(1-a)*3+.45*Math.sin(t*.8),0)}""")

# ───────── 1:54 · cierre: el tirador duda entre Argon y lo de siempre (arriba entra «Sígueme»)
S = 114.1; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 0, 114.3, A, '<span class="em">🧭</span>', 'Última parada', ring=('<b data-n=\'' + K((0, 96), (114.4, 100, 1.0)) + '\' data-f="p">96%</b>', K((0, 96), (114.4, 100, 1.0))),
          btn=('Sígueme', 119.3),
          mL=('Con descuento', '<b>Argon</b>', 115.6), mR=('O te quedas con', '<b>lo de siempre</b>', 117.9),
          bar=K((0, 50), (116.2, 20, .9), (118.2, 80, .9), (119.0, 50, .6)),
          cols=[('Gemini 4 Argon', '$2 / M', 116.0), ('¿Tú?', 'cuéntame', 119.0), ('Tu modelo', 'el de siempre', 118.1)])
escena('e09-cierre', S, FIN, 0, fase(1, 0, A(119.5)),
       f"""<div class="p1">{st([('¿Le darías <em>chance</em>?', 114.9, None)], S, 92)}{c1}</div>""",
LIB + r"""const gm=R.gem(200);R.scene.add(gm);const rb=R.robot(160);R.scene.add(rb);
const tx=R.text('EL LOG',140,60,R.iri('#b9a2ff',{metalness:.85,roughness:.14,opacity:1,transparent:false,iridescence:1}));R.scene.add(tx);
return t=>{const a=R.eb(R.k(t,115.8,.85)),b=R.eb(R.k(t,118.1,.85)),o=R.eo(R.k(t,119.3,.4));
 gm.visible=t>115.5&&t<119.8;gm.scale.setScalar(Math.max(.001,a*(1-o)));R.at(gm,270,1620,2);gm.rotation.set(.15,(1-a)*3+.45*Math.sin(t*1.1),0);
 rb.visible=t>117.8&&t<119.8;rb.scale.setScalar(Math.max(.001,b*(1-o)));R.at(rb,810,1620,2);rb.rotation.set(.12+.05*Math.sin(t*1.3),-.45+.3*Math.sin(t*.9),.05*Math.sin(t*2));
 const c=R.eb(R.k(t,119.8,.8));tx.visible=t>119.7;tx.scale.setScalar(Math.max(.001,c));R.at(tx,540,1450+(1-c)*150);tx.rotation.set(.18+.05*Math.sin(t*2),(1-c)*1.8+.22*Math.sin(t*1.5),0)}""",
sigue=False)

PIEZAS.append(('seguir', D.SEG_INI, FIN, D.SEGUIR))
PIEZAS.append(('cinta', 0.0, FIN, D.cinta()))  # al final: queda encima de todo
PRE = 'tray-'

if __name__ == '__main__':
    solo = set(sys.argv[1:])
    for pid, a, b, html in PIEZAS:
        if solo and pid not in solo:
            continue
        path = f'{WORK}/{pid}.html'
        open(path, 'w').write(html)
        if os.environ.get('SOLO_HTML'):
            print('html', path); continue
        r = subprocess.run(['node', CAP, path, f'{b - a:.2f}', f'{OUT}/{PRE}{pid}.webm'], capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr[-600:], flush=True)
    if not solo:
        rel = os.environ.get('REL', 'noticias/4/trayecto')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
