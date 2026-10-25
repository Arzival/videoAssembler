"""El Log #04 · diseño «Catálogo» (prueba): gloss 2 + tarjetas oscuras tipo ficha de modelo de IA — imagen arriba
(o a la izquierda), título, metadatos con separador fino, descripción corta, etiquetas tintadas (violeta, verde, cian),
separador punteado, pestañas con subrayado blanco que cambian solas y bloque de comando con botón de copiar.
Misma voz y tiempos que «Destino» (ellog-04-destino.py); reutiliza de ahí la cinta, el 3D y la tarjeta «Sígueme».
Uso: SALIDA=noticias/4/catalogo REL=noticias/4/catalogo python3 ejemplos/ellog-04-catalogo.py [ids…]   (SOLO_HTML=1 para revisar)
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
FIN, TOP, LIB, foto = D.FIN, D.TOP, D.LIB, D.foto

ICON = dict(D.ICON,
            copy='<rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
            down='<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>',
            file='<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/>',
            cpu='<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M15 2v2M15 20v2M2 15h2M2 9h2M20 15h2M20 9h2M9 2v2M9 20v2"/>',
            term='<path d="m4 17 6-6-6-6M12 19h8"/>')


def ic(n):
    return f'<svg class="ico" viewBox="0 0 24 24">{ICON[n]}</svg>'


CCSS = """
@property --on{syntax:'<number>';inherits:true;initial-value:0}
@keyframes tOn{to{--on:1}}@keyframes tOff{to{--on:0}}
.p1.lo,.p2.lo,.p3.lo{z-index:4}
.cc{position:absolute;animation:cardIn .8s cubic-bezier(.22,1.15,.36,1) both}
@keyframes cardIn{from{opacity:0;transform:translateY(140px) scale(.94)}to{opacity:1;transform:none}}
.cc.lo{border-radius:calc(var(--k)*16px);background:#0b0b0c;
  box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.07),inset 0 1.5px 0 rgba(255,255,255,.1),0 40px 90px rgba(0,0,0,.6),0 0 90px rgba(var(--acr),.18)}
.cc .im{position:absolute;left:calc(var(--k)*11px);top:calc(var(--k)*11px);right:calc(var(--k)*11px);height:var(--ih);border-radius:calc(var(--k)*10px);overflow:hidden;background:var(--ph)}
.cc.h .im{right:auto;width:var(--iw);bottom:calc(var(--k)*11px);height:auto}
.cc .im:before{content:'';position:absolute;left:6%;right:6%;top:8%;height:66%;border-radius:50%;background:radial-gradient(closest-side,rgba(255,255,255,.4),rgba(255,255,255,.07) 60%,transparent);filter:blur(10px)}
.cc .im:after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,transparent 55%,rgba(0,0,0,.35)),
  radial-gradient(120% 50% at 50% 115%,rgba(255,255,255,.18),transparent 60%)}
.cc .cb{position:absolute;left:calc(var(--k)*11px);right:calc(var(--k)*11px);top:calc(var(--ih) + var(--k)*23px);color:#f4f4f5}
.cc.h .cb{left:calc(var(--iw) + var(--k)*23px);top:calc(var(--k)*14px)}
.ti{font-size:calc(var(--k)*16px);font-weight:600;letter-spacing:-.015em;line-height:1.1}
.mt{display:flex;align-items:center;gap:calc(var(--k)*8px);margin-top:calc(var(--k)*6px);font-size:calc(var(--k)*10.5px);color:#9a9a9a;font-weight:500;white-space:nowrap}
.mt>span{display:inline-flex;align-items:center;gap:calc(var(--k)*5px)}.mt b{color:#d4d4d8;font-weight:700}
.mt .sp{width:1.5px;height:calc(var(--k)*11px);background:#34343a}
.ico{width:calc(var(--k)*12px);height:calc(var(--k)*12px);fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex-shrink:0}
.ds{font-size:calc(var(--k)*11px);color:#c4c4cb;line-height:1.42;margin-top:calc(var(--k)*9px);font-weight:500;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.tg{display:flex;flex-wrap:wrap;gap:calc(var(--k)*5px);margin-top:calc(var(--k)*10px)}
.tg span{height:calc(var(--k)*19px);padding:0 calc(var(--k)*6px);border-radius:calc(var(--k)*4px);font-size:calc(var(--k)*10px);font-weight:600;display:inline-flex;align-items:center;border:1.5px solid}
.tg .v{color:#b9a2ff;background:rgba(124,92,214,.18);border-color:rgba(124,92,214,.5)}
.tg .gr{color:#5ee59a;background:rgba(34,170,95,.15);border-color:rgba(34,170,95,.5)}
.tg .cy{color:#6fd3f0;background:rgba(58,167,201,.16);border-color:rgba(58,167,201,.5)}
.tg .rd{color:#ff8a95;background:rgba(229,72,77,.16);border-color:rgba(229,72,77,.5)}
.dt{border-top:1.5px dashed #2c2c31;margin-top:calc(var(--k)*13px)}
.tabs{display:flex;gap:calc(var(--k)*3px);margin-top:calc(var(--k)*5px);font-size:calc(var(--k)*11.5px);font-weight:600;white-space:nowrap}
.tabs>span{position:relative;display:inline-flex;align-items:center;gap:calc(var(--k)*5px);padding:calc(var(--k)*8px) calc(var(--k)*9px);color:#f4f4f5;opacity:calc(.5 + .5*var(--on))}
.tabs>span:after{content:'';position:absolute;left:calc(var(--k)*4px);right:calc(var(--k)*4px);bottom:0;height:2px;border-radius:1px;background:#fff;opacity:var(--on)}
.tabs>span>i{font-style:normal;display:inline-flex}.tabs svg{width:calc(var(--k)*12px);height:calc(var(--k)*12px)}
.cm{position:relative;margin-top:calc(var(--k)*8px);height:calc(var(--k)*31px);border-radius:calc(var(--k)*6px);background:#1a1a1c;box-shadow:inset 0 0 0 1px rgba(255,255,255,.04);
  font-family:'JetBrains Mono',monospace;font-size:calc(var(--k)*10.5px);color:#e4e4e7}
.cm .c{position:absolute;left:calc(var(--k)*10px);right:calc(var(--k)*34px);top:0;bottom:0;line-height:calc(var(--k)*31px);white-space:pre;overflow:hidden;text-overflow:ellipsis;opacity:var(--on)}
.cm .c i{font-style:normal;color:#9a9a9a}.cm .c em{font-style:normal;color:var(--ac)}.cm .c s{color:#6b6b73}
.cm .cp{position:absolute;right:calc(var(--k)*9px);top:50%;transform:translateY(-50%);width:calc(var(--k)*14px);height:calc(var(--k)*14px);color:#9a9a9a}
.cm .cp svg{position:absolute;inset:0;width:100%;height:100%}.cm .cp .a{opacity:calc(1 - var(--on))}.cm .cp .b{opacity:var(--on);color:#5ee59a}
.cm .ok{position:absolute;right:calc(var(--k)*-4px);top:calc(var(--k)*-30px);padding:calc(var(--k)*4px) calc(var(--k)*8px);border-radius:calc(var(--k)*5px);background:#f4f4f5;color:#0b0b0c;
  font-family:inherit;font-size:calc(var(--k)*9.5px);font-weight:700;opacity:var(--on);transform:translateY(calc((1 - var(--on))*8px))}
.cc .em{position:absolute;left:0;right:0;top:50%;transform:translateY(-55%);text-align:center;font-size:calc(var(--k)*80px);line-height:1;filter:drop-shadow(0 14px 24px rgba(0,0,0,.4))}
.cc .lg{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}.cc .lg svg{filter:drop-shadow(0 16px 30px rgba(0,0,0,.4))}
.ring{position:absolute;inset:-8px;border-radius:calc(var(--k)*16px + 8px);box-shadow:0 0 0 6px var(--ac),0 0 50px rgba(var(--acr),.8);opacity:0;animation:pop .45s cubic-bezier(.22,1.6,.36,1) both}
.vs{position:absolute;width:140px;height:140px;margin:-70px 0 0 -70px;border-radius:50%;display:flex;align-items:center;justify-content:center;z-index:9;
  font-size:48px;font-weight:800;letter-spacing:-.04em;background:#0b0b0c;color:#f4f4f5;box-shadow:inset 0 0 0 2px rgba(255,255,255,.12),0 0 0 10px rgba(var(--acr),.55),0 30px 60px rgba(0,0,0,.5)}
.below{position:absolute;left:0;right:0;text-align:center;z-index:9}.below .pill{font-size:36px;padding:20px 40px}
.chip{position:absolute;display:inline-flex;align-items:center;gap:calc(var(--k)*5px);padding:calc(var(--k)*5px) calc(var(--k)*9px);border-radius:calc(var(--k)*6px);
  font-size:calc(var(--k)*10.5px);font-weight:700;color:#f4f4f5;background:rgba(11,11,12,.72);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);box-shadow:inset 0 0 0 1px rgba(255,255,255,.12)}
.chip svg{width:calc(var(--k)*12px);height:calc(var(--k)*12px)}
"""


def win(ws, A):
    """Ventanas [(entra, sale|None), …] en segundos del video → lista de animaciones que prenden/apagan --on."""
    out = []
    for a, b in ws:
        out.append(f'tOn .2s ease {A(a)} forwards')
        if b:
            out.append(f'tOff .2s ease {A(b)} forwards')
    return 'animation:' + ','.join(out)


def card(x, y, w, h, k, pal, d, A, title, meta=(), desc='', tags=(), tabs=None, cmds=None, copy=None, ih=None, iw=None, lo_in='', hi_in='', dd=None):
    """Ficha del catálogo: (capa baja = fondo + imagen, capa alta = textos). Tiempos en segundos del video."""
    c1, c2, ac, ac2, acr, ink = G.PALETAS[pal]
    st = f'left:{x}px;top:{y}px;width:{w}px;height:{h}px;--k:{k};--ph:{foto(pal)};--ac:{ac};--ac2:{ac2};--acr:{acr};--ink:{ink};animation-delay:{A(d)}'
    st += f';--ih:{ih}px' if ih else ';--ih:0px'
    st += f';--iw:{iw}px' if iw else ''
    cls = 'cc h' if iw else 'cc'
    b = f'<div class="ti">{title}</div>'
    if meta:
        b += '<div class="mt">' + '<i class="sp"></i>'.join(f'<span>{ic(i)}{t}</span>' for i, t in meta) + '</div>'
    if desc:
        b += f'<div class="ds{" pop" if dd else ""}" style="animation-delay:{A(dd or d)}">{desc}</div>'
    if tags:
        b += '<div class="tg">' + ''.join(f'<span class="{c}{" pop" if t else ""}" style="animation-delay:{A(t or d)}">{x_}</span>' for c, x_, t in tags) + '</div>'
    if tabs:
        b += '<div class="dt"></div><div class="tabs">' + ''.join(f'<span style="{win(ws, A)}"><i>{i}</i>{n}</span>' for i, n, ws in tabs) + '</div>'
    if cmds:
        cp = f'<span class="cp" style="{win([copy], A)}"><svg class="a ico" viewBox="0 0 24 24">{ICON["copy"]}</svg><svg class="b ico" viewBox="0 0 24 24">{ICON["check"]}</svg></span>' if copy else \
             f'<span class="cp"><svg class="a ico" viewBox="0 0 24 24">{ICON["copy"]}</svg></span>'
        ok = f'<span class="ok" style="{win([copy], A)}">Copiado</span>' if copy else ''
        b += '<div class="cm">' + ''.join(f'<span class="c" style="{win(ws, A)}">{c}</span>' for c, ws in cmds) + cp + ok + '</div>'
    lo = f'<div class="{cls} lo" style="{st}"><div class="im">{lo_in}</div></div>'
    hi = f'<div class="{cls} hi" style="{st}">{hi_in}<div class="cb">{b}</div></div>'
    return lo, hi


def chip(html, x, y, d, A, cls='pop', extra=''):
    return f'<div class="chip {cls}" style="left:{x}px;top:{y}px;animation-delay:{A(d)};{extra}">{html}</div>'


PIEZAS = []


def escena(pid, start, end, n, css, body, js3d=None, script='', sigue=True):
    if sigue:
        end += 0.45
    PIEZAS.append((pid, start, end, G.page(CCSS + css, body, end - start, script, n=n, js3d=js3d, salida=not sigue, t0=start)))


def st(items, S, size=88):
    return G.steps(items, S, top=TOP, size=size)


def fase(n, a, b=None):
    """CSS de una fase: entra en a y (si hay b) se va en b."""
    if n == 1:
        return f'.p1{{animation:gone .4s ease {b} forwards}}' if b else ''
    return f'.p{n}{{opacity:0;animation:fade .35s ease {a} forwards' + (f',gone .4s ease {b} forwards' if b else '') + '}'


# geometría: ficha grande vertical, par lado a lado, ficha horizontal
BX, BW, BK, BIH = 100, 880, 2.5, 640
LX, RX, SW, SK, SIH = 50, 560, 470, 1.85, 330
GOOG = G.logo('googlegemini', '#fff')

# ───────── 0:00 · #01 Gemini 4 Argon
S = 0.0; A = G.at(S)
lo1, hi1 = card(BX, 430, BW, 1240, BK, 2, 0.2, A, 'gemini-4-argon', [('cpu', '<b>Google</b>'), ('clock', 'disponible 13 oct')],
                'Su modelo para código pesado. Si eres desarrollador, la API te sale a mitad de precio hasta noviembre.',
                [('v', 'código', 3.2), ('gr', 'api', 5.8), ('cy', '−50 %', 6.6), ('cy', 'hasta 30 nov', 7.5)],
                [(ic('term'), 'API', [(0.3, None)]), (GOOG, 'App', [(99, None)]), (ic('chat'), 'Search', [(99, None)]), ('🚀', 'Antigravity', [(99, None)])],
                [('<i>model=</i><em>"gemini-4-argon"</em>', [(0.3, 6.4)]), ('<i>$</i>2 <i>/ M tokens</i> <s>$4</s> <i>· hasta 30 nov</i>', [(6.5, None)])],
                copy=(4.6, 5.9), ih=BIH, dd=2.4,
                hi_in=chip(f'{G.logo("google", "#fff")}Google', 30, 30, 1.0, A))
GR = [('💻', 'código', 'v', 10.4), ('🔬', 'ciencias', 'cy', 11.0), ('📈', 'finanzas', 'gr', 11.8), ('🛡️', 'ciberseguridad', 'rd', 12.4)]
lo2 = hi2 = ''
for i, (e, t, c, t0) in enumerate(GR):
    l, h = card(LX if i % 2 == 0 else RX, 600 + (i // 2) * 570, SW, 540, SK, [2, 4, 'fin', 1][i], t0, A, t, [('check', 'incluido')], tags=[(c, 'pesado', None)],
                ih=330, lo_in=f'<div class="em">{e}</div>')
    lo2 += l; hi2 += h
escena('e00-argon', S, 13.9, 2, fase(1, 0, A(8.5)) + fase(2, A(8.6)),
       f"""<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>
<div class="p2 lo">{lo2}</div><div class="p2">{st([('Para lo <em>pesado</em>', 8.7, None)], S, 92)}{hi2}</div>""",
LIB + r"""const gm=R.gem(380);R.scene.add(gm);
return t=>{const a=R.eb(R.k(t,.35,.9)),o=R.eo(R.k(t,8.3,.45));gm.visible=t<8.8;gm.scale.setScalar(Math.max(.001,a*(1-o)));
 R.at(gm,540,780-o*200+12*Math.sin(t*1.6),2);gm.rotation.set(.15+.08*Math.sin(t*1.1),(1-a)*3+.5*Math.sin(t*.8),.05*Math.sin(t*.9))}""")

# ───────── 0:14 · #01 (parte 2): dónde está (las pestañas cambian solas) y «ponlos a competir»
S = 13.9; A = G.at(S)
lo1, hi1 = card(BX, 560, BW, 1150, BK, 2, 14.1, A, 'gemini-4-argon', [('lock', '<b>Pro</b> y <b>Ultra</b>'), ('clock', 'ya disponible')],
                'Ya está en la app de Gemini, en su modo AI Search y en Antigravity.',
                [('v', 'pro', 17.6), ('v', 'ultra', 18.0), ('gr', 'ai mode', 19.6), ('cy', 'antigravity', 20.8)],
                [(GOOG, 'App', [(14.6, 19.5)]), (ic('chat'), 'AI Mode', [(19.6, 20.7)]), ('🚀', 'Antigravity', [(20.8, None)])],
                [('<i>Gemini app ›</i> <em>Pro · Ultra</em>', [(14.6, 19.5)]), ('<i>google.com ›</i> <em>AI Mode</em>', [(19.6, 20.7)]),
                 ('<i>Antigravity ›</i> <em>con Ultra</em>', [(20.8, None)])], ih=540)
CY = 640
lo2a, hi2a = card(LX, CY, SW, 790, SK, 'gris', 22.9, A, 'tu-modelo', [('clock', 'el de siempre')], 'El que ya usas para revisar tu código.',
                  [('v', 'review', None)], [(ic('term'), 'CLI', [(23.0, None)]), (ic('code'), 'IDE', [(99, None)])],
                  [('<i>$</i> review <em>--model tu-modelo</em>', [(23.4, None)])], ih=SIH)
lo2b, hi2b = card(RX, CY, SW, 790, SK, 2, 23.5, A, 'gemini-4-argon', [('tag', '<b>$2</b> / M')], 'A mitad de precio hasta el 30 de noviembre.',
                  [('v', 'review', None), ('cy', '−50 %', 24.6)], [(ic('term'), 'CLI', [(23.6, None)]), (ic('code'), 'IDE', [(99, None)])],
                  [('<i>$</i> review <em>--model argon</em>', [(24.0, None)])], ih=SIH)
escena('e01-donde', S, 27.9, 2, fase(1, 0, A(22.2)) + fase(2, A(22.3)),
       f"""<div class="p1 lo">{lo1}</div><div class="p1">{st([('¿Dónde <em>está</em>?', 14.0, None)], S, 92)}{hi1}</div>
<div class="p2 lo">{lo2a}{lo2b}</div><div class="p2">{st([('¿Ya usas <em>otro modelo</em>?', 22.4, 25.1), ('Ponlos a <em>competir</em>', 25.2, None)], S, 88)}{hi2a}{hi2b}
 <div class="vs stamp" style="left:540px;top:{CY + 170}px;--r:-8deg;animation-delay:{A(26.2)}">VS</div>
 <div class="below" style="top:{CY + 840}px"><span class="pill on pop" style="animation-delay:{A(25.4)}">📅 el descuento acaba el 30 nov</span></div></div>""",
LIB + r"""const gm=R.gem(300);R.scene.add(gm);const rb=R.robot(170);R.scene.add(rb);const g2=R.gem(170);R.scene.add(g2);
return t=>{const a=R.eb(R.k(t,14.3,.9)),o=R.eo(R.k(t,22.0,.4)),b=R.eb(R.k(t,23.2,.85)),c=R.eb(R.k(t,23.8,.85)),hit=Math.sin(Math.PI*R.k(t,26.2,.35));
 gm.visible=t<22.5;gm.scale.setScalar(Math.max(.001,a*(1-o)));R.at(gm,540,830,2);gm.rotation.set(.15,(1-a)*3+.5*Math.sin(t*.8)+(t>19.6?.6:0)+(t>20.8?.6:0),0);
 rb.visible=t>22.9;rb.scale.setScalar(Math.max(.001,b));R.at(rb,285+hit*20,820,2);rb.rotation.set(.12+.05*Math.sin(t*1.3),.45+.25*Math.sin(t*.9),.05*Math.sin(t*2));
 g2.visible=t>23.5;g2.scale.setScalar(Math.max(.001,c));R.at(g2,795-hit*20,820,2);g2.rotation.set(.12,(1-c)*3-.4+.35*Math.sin(t*1.1),0)}""")

# ───────── 0:28 · #02 OpenAI: ex empleado se llevó archivos a Apple (las pestañas recorren lo que había en los archivos)
S = 27.9; A = G.at(S)
lo1, hi1 = card(BX, 430, BW, 1240, BK, 'amb', 28.1, A, '<span id="nf">0</span>+ archivos', [('file', '<b>dispositivo</b> sin lanzar'), ('clock', 'último día: 2 jun')],
                'OpenAI dice que un ex empleado se los llevó al irse a Apple y luego se los presentó a sus directivos.',
                [('v', 'openai', None), ('rd', 'sin lanzar', 33.5), ('cy', 'apple', 35.0)],
                [('🖼️', 'Imágenes', [(32.3, 32.9)]), ('⚙️', 'Ingeniería', [(32.9, 33.5)]), ('🏭', 'Proveedores', [(33.5, 34.1)]), ('✨', 'Acabados', [(34.1, None)])],
                [('<i>$</i> cp -r <em>./dispositivo</em> ~/personal/', [(30.6, 34.9)]), ('<i>→</i> presentado a <em>directivos de Apple</em>', [(35.0, None)])],
                ih=BIH, dd=29.0, hi_in=chip(f'{G.logo("openai", "#fff")}OpenAI dice', 30, 30, 28.3, A))
escena('e02-archivos', S, 36.6, 'amb', '', f'<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>',
LIB + "const OA=" + js(G.svgpath('openai')) + ",AP=" + js(G.svgpath('apple')) + r""";
const oa=R.shape(OA,210,3,R.gloss('#f4f4f6',{roughness:.18}),.5);R.scene.add(oa);
const ap=R.shape(AP,180,3,R.metal('#d9dbe2',{roughness:.14}),.5);R.scene.add(ap);
const sh=[];for(let i=0;i<9;i++){const s=R.sheet(i%2?'#ffb340':'#7aa7ff');s.userData={t:30.6+i*.32,z:(i%3)-1};R.scene.add(s);sh.push(s)}
return t=>{const a=R.eb(R.k(t,28.4,.8)),b=R.eb(R.k(t,29.9,.8)),gl=Math.sin(Math.PI*R.k(t,35.0,.7));
 oa.scale.setScalar(Math.max(.001,a));R.at(oa,300,760,1);oa.rotation.set(.15,.5*Math.sin(t*.9)+(1-a)*3,0);
 ap.visible=t>29.8;ap.scale.setScalar(Math.max(.001,b*(1+.15*gl)));R.at(ap,780,760,1);ap.rotation.set(.12,-.45*Math.sin(t*.8)+(1-b)*3,0);
 ap.material.emissive.set('#ffb340');ap.material.emissiveIntensity=.5*gl;
 for(const s of sh){const u=s.userData,p=R.k(t,u.t,1.3),e=R.eio(p);s.visible=p>0&&p<1;
  R.at(s,R.mix(350,740,e),760-Math.sin(Math.PI*e)*240,3+u.z);s.rotation.set(.3*Math.sin(t*3+u.z),e*2.5,e*1.2+u.z*.3);s.scale.setScalar(Math.max(.001,Math.sin(Math.PI*p)*.9+.1))}}""",
f"""window.__cnt=t=>{{t+={S};const e=1-Math.pow(1-Math.min(1,Math.max(0,(t-31.3)/1.0)),3);document.getElementById('nf').textContent=Math.round(100*e)}}""")

# ───────── 0:37 · #02 (parte 2): documento judicial (pestañas OpenAI | Apple) → «ya está en los tribunales»
S = 36.6; A = G.at(S)
lo1, hi1 = card(BX, 600, BW, 1110, BK, 'amb', 36.8, A, 'documento-judicial', [('scale', '<b>Apple</b> vs. OpenAI'), ('clock', 'oct 2026')],
                'Viene en el pleito donde Apple ya demanda a OpenAI por secretos comerciales.',
                [('v', 'demanda', 40.7), ('gr', 'secretos comerciales', 41.9)],
                [(G.logo('openai', '#fff'), 'OpenAI', [(37.2, 42.5)]), (G.logo('apple', '#fff'), 'Apple', [(42.6, None)])],
                [('<i>«</i>circula dentro de <em>Apple</em><i>»</i>', [(38.6, 42.5)]), ('<i>«</i>no hay <em>evidencia</em><i>»</i>', [(42.6, None)])],
                ih=520, dd=38.5)
lo2a, hi2a = card(LX, 640, SW, 560, SK, 0, 43.9, A, 'openai', [('cpu', 'su dispositivo de IA')], tags=[('v', 'hardware', None)], ih=SIH,
                  lo_in=f'<div class="lg">{G.logo("openai", "#fff", 160)}</div>')
lo2b, hi2b = card(RX, 640, SW, 560, SK, 'gris', 44.2, A, 'apple', [('cpu', 'sus dispositivos')], tags=[('cy', 'hardware', None)], ih=SIH,
                  lo_in=f'<div class="lg">{G.logo("apple", "#fff", 150)}</div>')
escena('e03-tribunal', S, 49.9, 'amb', fase(1, 0, A(43.6)) + fase(2, A(43.7)) + f"""
.mk{{position:relative;display:inline-block}}.mk:after{{content:'';position:absolute;left:24px;right:24px;top:50%;height:7px;border-radius:4px;background:#ff4d5e;transform:scaleX(0);transform-origin:left;animation:strike .35s ease {A(46.9)} forwards}}
@keyframes strike{{to{{transform:scaleX(1)}}}}""",
       f"""<div class="p1 lo">{lo1}</div><div class="p1">{st([('Pero <em>ojo</em>', 36.7, None)], S, 92)}{hi1}</div>
<div class="p2 lo">{lo2a}{lo2b}</div><div class="p2">{st([('¿Puro <em>marketing</em>?', 43.8, 47.2), ('Ya está en los<br><em>tribunales</em>', 47.3, None)], S, 88)}{hi2a}{hi2b}
 <div class="below" style="top:1340px"><span class="mk pop" style="animation-delay:{A(46.2)}"><span class="pill">📣 la pelea del hardware de IA</span></span></div>
 <div class="below" style="top:1490px"><span class="pill bad stamp" style="font-size:44px;animation-delay:{A(48.7)}">⚖️ en los tribunales</span></div></div>""",
LIB + r"""const gv=R.gavel(270);R.scene.add(gv);
return t=>{const a=R.eb(R.k(t,37.0,.9)),m=R.eio(R.k(t,43.4,.8)),sl=R.k(t,48.2,.5),hit=sl<.6?R.eio(sl/.6):1-R.eo((sl-.6)/.4)*.25;
 const y=R.mix(890,1480,m),x=R.mix(540,880,m);gv.scale.setScalar(Math.max(.001,a*R.mix(1,.6,m)));R.at(gv,x,y,3);
 gv.rotation.set(.25+.05*Math.sin(t*1.2),R.mix(-.5+.35*Math.sin(t*.8),-.2,m),R.mix(.35,.9,m)-hit*1.3*(t>48.2?1:0))}""")

# ───────── 0:50 · #03 ocho estados demandan a OpenAI
S = 49.9; A = G.at(S)
EST = [('IA', 'iowa', 58.06), ('KS', 'kansas', 58.47), ('AZ', 'arizona', 59.05), ('NE', 'nebraska', 0), ('AR', 'arkansas', 0),
       ('ID', 'idaho', 0), ('MT', 'montana', 0), ('WV', 'w-virginia', 0)]
lo1 = hi1 = ''
for i, (ab, nm, th) in enumerate(EST):
    ring = f'<div class="ring" style="animation-delay:{A(th)}"></div>' if th else ''
    l, h = card(60 + (i % 4) * 244, 650 + (i // 4) * 345, 228, 330, 1.25, 1 if th else 'gris', 52.2 + i * .17, A,
                f'<span style="font-size:22px">{nm}</span>', tags=[('rd' if th else 'v', 'demanda', None)], ih=170,
                lo_in=f'<div class="em" style="font-size:76px;font-weight:800;letter-spacing:-.04em;color:#fff">{ab}</div>', hi_in=ring)
    lo1 += l; hi1 += h
lo2a, hi2a = card(LX, 620, SW, 640, SK, 1, 61.7, A, 'dañar-a-niños', [('user', 'menores')], 'Una de las acusaciones de los estados.',
                  [('rd', 'seguridad', None)], ih=SIH, lo_in='<div class="em">🧒</div>')
lo2b, hi2b = card(RX, 620, SW, 640, SK, 'gris', 62.8, A, 'engañar', [('chat', 'ChatGPT')], 'Sobre qué tan seguro es realmente ChatGPT.',
                  [('rd', 'publicidad', None)], ih=SIH)
escena('e04-estados', S, 66.0, 1, fase(1, 0, A(61.1)) + fase(2, A(61.2)),
       f"""<div class="p1 lo">{lo1}</div><div class="p1">{st([('<em>8 estados</em> demandan<br>a OpenAI', 50.1, None)], S, 86)}{hi1}
 <div class="below" style="top:1380px"><span class="pill on pop" style="animation-delay:{A(55.4)}">🛡️ seguridad de ChatGPT con menores</span></div></div>
<div class="p2 lo">{lo2a}{lo2b}</div><div class="p2">{st([('Lo <em>acusan</em> de…', 61.3, None)], S, 92)}{hi2a}{hi2b}</div>""",
LIB + "const OA=" + js(G.svgpath('openai')) + ",SH=" + js(D.SHIELD) + r""";
const oa=R.shape(OA,240,3,R.gloss('#f4f4f6',{roughness:.18}),.5);R.scene.add(oa);
const sh=R.shape(SH,210,5,R.gloss('#8d96a8',{emissive:'#ff2a3a',emissiveIntensity:0,roughness:.16}));R.scene.add(sh);
return t=>{const a=R.eb(R.k(t,51.0,.85)),o=R.eo(R.k(t,60.9,.4)),b=R.eb(R.k(t,63.1,.8)),r=R.k(t,64.3,.5);
 oa.visible=t<61.4;oa.scale.setScalar(Math.max(.001,a*(1-o)));R.at(oa,540,1630,1);oa.rotation.set(.2,(1-a)*3+.6*Math.sin(t*.8),0);
 sh.visible=t>62.9;sh.scale.setScalar(Math.max(.001,b));R.at(sh,795,805,2);sh.rotation.set(.15,(1-b)*3+.4*Math.sin(t*1.1),r>0&&r<1?Math.sin(t*50)*.06:0);
 sh.material.color.set(r>.5?'#ff8a95':'#8d96a8');sh.material.emissiveIntensity=.45*r}""")

# ───────── 1:06 · #03 (parte 2): del diseño a los agentes; si construyes sobre su API (pestañas por lenguaje)
S = 66.0; A = G.at(S)
lo1a, hi1a = card(60, 600, 960, 340, 1.9, 2, 67.2, A, 'diseño-del-chatbot', [('chat', 'ChatGPT'), ('clock', 'desde el inicio')],
                  'Las demandas van desde cómo está diseñado el chatbot…', [('v', 'diseño', None)], iw=300,
                  lo_in='<div class="em" style="font-size:150px">💬</div>')
lo1b, hi1b = card(60, 1060, 960, 420, 1.9, 1, 70.8, A, 'agentes-descontrolados', [('bot', 'agentes'), ('clock', 'lo más reciente')],
                  '…hasta sus problemas más recientes con agentes que se salen de control.', [('rd', 'agentes', 71.3), ('rd', 'sin control', 71.8)], iw=380)
lo2, hi2 = card(BX, 660, BW, 1050, BK, 'gris', 73.5, A, 'tu-integracion', [('code', 'API de OpenAI'), ('clock', 'puede cambiar')],
                'Si construyes sobre su API, esto puede cambiar cómo se lanzan los chatbots y los agentes.',
                [('v', 'chatbots', 77.8), ('gr', 'agentes', 78.5)],
                [('🐍', 'Python', [(73.9, 75.6)]), ('⬢', 'Node', [(75.6, 77.2)]), (ic('term'), 'cURL', [(77.2, None)])],
                [('<i>$</i> pip install <em>openai</em>', [(73.9, 75.6)]), ('<i>$</i> npm i <em>openai</em>', [(75.6, 77.2)]),
                 ('<i>$</i> curl <em>api.openai.com</em>/v1/…', [(77.2, None)])], ih=430, dd=75.2,
                lo_in='<div class="code">' + ''.join(f'<div class="ln" style="animation-delay:{A(73.9 + k * .35)}">{c}</div>' for k, c in enumerate(D.CODE)) + '</div>')
escena('e05-demandas', S, 79.5, 1, fase(1, 0, A(73.0)) + fase(2, A(73.1)) + """
.code{position:absolute;left:44px;right:44px;top:80px;padding:34px 40px;border-radius:24px;background:rgba(8,9,12,.75);box-shadow:inset 0 0 0 1px rgba(255,255,255,.1);
  font-family:'JetBrains Mono',monospace;font-size:32px;line-height:1.6;color:#e6e9ef;white-space:pre}
.code .ln{opacity:0;animation:fade .25s ease forwards}.code i{font-style:normal;color:#ff8a6b}""",
       f"""<div class="p1 lo">{lo1a}{lo1b}</div><div class="p1">{st([('Las demandas van…', 66.1, None)], S, 88)}{hi1a}{hi1b}
 <div class="below" style="top:968px"><span class="pill pop" style="animation-delay:{A(68.7)}">⬇ hasta</span></div></div>
<div class="p2 lo">{lo2}</div><div class="p2">{st([('¿Construyes sobre<br>su <em>API</em>?', 73.2, None)], S, 86)}{hi2}</div>""",
LIB + r"""const rb=R.robot(200);R.scene.add(rb);
return t=>{const a=R.eb(R.k(t,71.1,.8)),o=R.eo(R.k(t,72.8,.35)),c=R.k(t,71.6,.2);
 rb.visible=t>70.9&&t<73.2;rb.scale.setScalar(Math.max(.001,a*(1-o)));R.at(rb,250+(c>0?Math.sin(t*37)*12:0),1270,2);
 rb.rotation.set(.1+(c>0?.25*Math.sin(t*9):0),-.3+(c>0?1.2*Math.sin(t*5.3):0),c>0?.3*Math.sin(t*7.1):0);rb.userData.em.emissiveIntensity=1.6+(c>0?2*Math.abs(Math.sin(t*12)):0)}""")

# ───────── 1:20 · #04 GitHub rehízo el historial de estrellas (pestañas Antes | Ahora)
S = 79.5; A = G.at(S)
lo1, hi1 = card(BX, 430, BW, 1240, BK, 3, 79.7, A, 'star-history', [('star', 'repo de <b>251K</b>'), ('clock', 'nueva API')],
                'GitHub rehízo su historial de estrellas: menos peticiones y ya no expone quién te dio estrella.',
                [('v', 'privacidad', 80.6), ('gr', 'api', 81.2), ('cy', '≈100× menos', 85.1)],
                [('⏪', 'Antes', [(80.0, 83.9)]), ('⚡', 'Ahora', [(83.97, None)])],
                [('<i>peticiones:</i> <em id="rq">2,500</em>', [(80.2, None)])], ih=BIH, dd=80.4,
                hi_in=chip(f'{G.logo("github", "#fff")}GitHub', 30, 30, 79.9, A))
AV = ''.join(f'<i style="background:linear-gradient(160deg,{a},{b})"></i>' for a, b in
             [('#ffd9cc', '#ff8a6b'), ('#dbe8ff', '#6ea8ff'), ('#f1fbc9', '#c6e64a'), ('#e9e0ff', '#a78bfa'), ('#d3f4ff', '#4fd2ff'), ('#ffe6c2', '#ffb340')])
lo2a, hi2a = card(LX, 620, SW, 640, SK, 'gris', 86.1, A, 'stargazers', [('user', 'quién te dio ⭐')], 'Ya no se devuelve la lista de personas.',
                  [('rd', 'oculto', 86.6)], ih=SIH, lo_in=f'<div class="avs">{AV}</div>')
lo2b, hi2b = card(RX, 620, SW, 640, SK, 3, 87.4, A, 'tendencia', [('trend', 'semana y día')], 'Solo la tendencia, sin nombres.',
                  [('gr', 'agregado', 88.6)], ih=SIH,
                  lo_in='<svg class="chart" viewBox="0 0 400 300"><path d="M20 260 L80 240 L130 245 L180 200 L230 190 L280 130 L330 110 L380 40"/></svg>')
escena('e06-estrellas', S, 89.7, 3, fase(1, 0, A(85.8)) + fase(2, A(85.9)) + f"""
.avs{{position:absolute;left:40px;right:40px;top:40px;display:grid;grid-template-columns:repeat(3,1fr);gap:22px;filter:blur(7px)}}
.avs i{{aspect-ratio:1;border-radius:50%;box-shadow:inset 0 3px 0 rgba(255,255,255,.5)}}
.chart{{position:absolute;left:30px;top:30px;width:calc(100% - 60px);height:260px;overflow:visible}}
.chart path{{fill:none;stroke:#fff;stroke-width:12;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:700;stroke-dashoffset:700;filter:drop-shadow(0 10px 20px rgba(0,0,0,.35));
  animation:draw 1s cubic-bezier(.45,0,.2,1) {A(88.0)} forwards}}@keyframes draw{{to{{stroke-dashoffset:0}}}}""",
       f"""<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>
<div class="p2 lo">{lo2a}{lo2b}</div><div class="p2">{st([('Ya no dice <em>quién</em>', 86.0, None)], S, 92)}{hi2a}{hi2b}</div>""",
LIB + r"""const sr=R.star(5,180,78,60,R.gloss('#ffd34d',{emissive:'#ffb000',emissiveIntensity:.25,metalness:.3,roughness:.14}));R.scene.add(sr);
return t=>{const a=R.eb(R.k(t,80.0,.9)),o=R.eo(R.k(t,85.6,.4)),p=Math.sin(Math.PI*R.k(t,84.0,.6));
 sr.visible=t<86.1;sr.scale.setScalar(Math.max(.001,a*(1-o)*(1+.12*p)));R.at(sr,540,780+10*Math.sin(t*1.5),2);sr.rotation.set(.18+.06*Math.sin(t*1.2),(1-a)*3+.55*Math.sin(t*1.2),.08*Math.sin(t*.9))}""",
f"""window.__cnt=t=>{{t+={S};const e=1-Math.pow(1-Math.min(1,Math.max(0,(t-83.9)/1.1)),3);document.getElementById('rq').textContent=Math.round(2500-2476*e).toLocaleString('en-US')}}""")

# ───────── 1:30 · #05 YouTube Music etiqueta la música hecha con IA (pestañas Fully | Partly)
S = 89.7; A = G.at(S)
lo1, hi1 = card(BX, 430, BW, 1240, BK, 'pass', 89.9, A, 'youtube-music', [('music', 'etiquetas de IA'), ('clock', 'desde el 14 oct')],
                'Ya etiqueta las canciones hechas con IA, aunque sea solo la voz o la composición.',
                [('v', 'voz', 94.9), ('v', 'composición', 95.3), ('gr', 'en el reproductor', 98.0)],
                [('✨', 'Fully Gen AI', [(91.3, 94.2)]), ('◐', 'Partly Gen AI', [(94.3, None)])],
                [('<i>▶</i> reproduciendo <i>·</i> <em>hecha con IA</em>', [(98.8, None)]), ('<i>etiqueta:</i> <em>toda la canción</em>', [(91.3, 94.2)]),
                 ('<i>etiqueta:</i> <em>solo una parte</em>', [(94.3, 98.7)])], ih=BIH, dd=93.8,
                hi_in=chip(f'{G.logo("youtubemusic", "#fff")}YouTube Music', 30, 30, 90.1, A))
escena('e07-ytmusic', S, 100.2, 'pass', '', f'<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>',
LIB + r"""const vy=R.vinyl(240,'#ff2d48');R.scene.add(vy);const V=vy.userData.V;
return t=>{const a=R.eb(R.k(t,90.1,.9)),sp=R.k(t,98.8,.6);vy.scale.setScalar(Math.max(.001,a));R.at(vy,540,770,1);
 vy.rotation.set(.35+.06*Math.sin(t*1.1),-.35+.2*Math.sin(t*.7)+(1-a)*2.5,0);V.rotation.z=-(t*.6+Math.max(0,t-98.8)*4*sp)}""")

# ───────── 1:40 · #05 (parte 2): Deezer (pestañas = dónde esconde la música de IA)
S = 100.2; A = G.at(S)
lo1, hi1 = card(BX, 430, BW, 1240, BK, 0, 100.4, A, 'deezer · filtro anti-IA', [('lock', 'un botón'), ('clock', 'antes de fin de año')],
                'Quiere ir aún más lejos: un botón para quitar toda la música de IA. Todavía no sale.',
                [('v', 'filtro', 102.9), ('rd', 'todavía no sale', 106.5), ('cy', 'fin de año', 109.4)],
                [('🔎', 'Búsqueda', [(103.9, None)]), ('💿', 'Álbumes', [(104.3, None)]), ('🎤', 'Artistas', [(104.7, None)])],
                [('<i>música IA:</i> <em>visible</em>', [(100.6, 103.8)]), ('<i>música IA:</i> <em>oculta ✓</em>', [(103.9, None)])],
                ih=BIH, dd=101.3, hi_in=chip(f'{G.logo("deezer", "#fff")}Deezer', 30, 30, 100.6, A))
lo2a, hi2a = card(LX, 620, SW, 640, SK, 'pass', 110.7, A, 'youtube-music', [('check', 'ya disponible')], 'Etiquetas en el reproductor.',
                  [('gr', 'ya está', None)], ih=SIH, lo_in=f'<div class="lg">{G.logo("youtubemusic", "#fff", 150)}</div>')
lo2b, hi2b = card(RX, 620, SW, 640, SK, 0, 111.0, A, 'deezer', [('clock', 'fin de año')], 'Filtro para ocultar la música de IA.',
                  [('cy', 'pronto', None)], ih=SIH, lo_in=f'<div class="lg">{G.logo("deezer", "#fff", 150)}</div>')
escena('e08-deezer', S, 114.1, 0, fase(1, 0, A(110.4)) + fase(2, A(110.5)),
       f"""<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>
<div class="p2 lo">{lo2a}{lo2b}</div><div class="p2">{st([('¿Creas música con <em>IA</em>?', 110.6, None)], S, 88)}{hi2a}{hi2b}
 <div class="below" style="top:1360px"><span class="pill on stamp" style="font-size:40px;--r:-3deg;animation-delay:{A(112.6)}">🏷️ el etiquetado ya viene</span></div></div>""",
LIB + "const DZ=" + js(G.svgpath('deezer')) + r""";
const dz=R.shape(DZ,340,3,R.iri('#d9c9ff',{metalness:.5,roughness:.1,opacity:1,transparent:false,emissive:'#7c5ce6',emissiveIntensity:.2}),.5);R.scene.add(dz);
return t=>{const a=R.eb(R.k(t,100.6,.9)),o=R.eo(R.k(t,110.2,.4));dz.visible=t<110.7;dz.scale.setScalar(Math.max(.001,a*(1-o)));
 R.at(dz,540,760+10*Math.sin(t*1.4),2);dz.rotation.set(.2+.06*Math.sin(t*1.2),(1-a)*3+.45*Math.sin(t*.8),0)}""")

# ───────── 1:54 · cierre: ¿le darías chance a Argon? (arriba entra «Sígueme»)
S = 114.1; A = G.at(S)
lo1a, hi1a = card(LX, 620, SW, 790, SK, 2, 115.5, A, 'gemini-4-argon', [('tag', '<b>$2</b> / M')], 'Con su descuento hasta el 30 de noviembre.',
                  [('cy', '−50 %', None)], [(ic('term'), 'Probar', [(115.7, None)])], [('<i>$</i> try <em>argon</em>', [(116.4, None)])], copy=(117.5, None), ih=SIH)
lo1b, hi1b = card(RX, 620, SW, 790, SK, 'gris', 117.8, A, 'lo-que-ya-usas', [('clock', 'el de siempre')], 'Tu modelo de siempre.',
                  [('v', 'conocido', None)], [(ic('term'), 'Quedarme', [(118.0, None)])], [('<i>$</i> keep <em>tu-modelo</em>', [(118.4, None)])], copy=(119.1, None), ih=SIH)
escena('e09-cierre', S, FIN, 0, fase(1, 0, A(119.5)),
       f"""<div class="p1 lo">{lo1a}{lo1b}</div><div class="p1">{st([('¿Le darías <em>chance</em>?', 114.9, None)], S, 92)}{hi1a}{hi1b}
 <div class="vs stamp" style="left:540px;top:800px;--r:6deg;font-size:42px;animation-delay:{A(117.9)}">¿o?</div></div>""",
LIB + r"""const gm=R.gem(220);R.scene.add(gm);const rb=R.robot(170);R.scene.add(rb);
const tx=R.text('EL LOG',140,60,R.iri('#b9a2ff',{metalness:.85,roughness:.14,opacity:1,transparent:false,iridescence:1}));R.scene.add(tx);
return t=>{const a=R.eb(R.k(t,115.8,.85)),b=R.eb(R.k(t,118.1,.85)),o=R.eo(R.k(t,119.3,.4));
 gm.visible=t>115.5&&t<119.8;gm.scale.setScalar(Math.max(.001,a*(1-o)));R.at(gm,285,800,2);gm.rotation.set(.15,(1-a)*3+.45*Math.sin(t*1.1),0);
 rb.visible=t>117.8&&t<119.8;rb.scale.setScalar(Math.max(.001,b*(1-o)));R.at(rb,795,800,2);rb.rotation.set(.12+.05*Math.sin(t*1.3),-.45+.3*Math.sin(t*.9),.05*Math.sin(t*2));
 const c=R.eb(R.k(t,119.8,.8));tx.visible=t>119.7;tx.scale.setScalar(Math.max(.001,c));R.at(tx,540,1450+(1-c)*150);tx.rotation.set(.18+.05*Math.sin(t*2),(1-c)*1.8+.22*Math.sin(t*1.5),0)}""",
sigue=False)

PIEZAS.append(('seguir', D.SEG_INI, FIN, D.SEGUIR))
PIEZAS.append(('cinta', 0.0, FIN, D.cinta()))  # al final: queda encima de todo
PRE = 'cat-'

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
        rel = os.environ.get('REL', 'noticias/4/catalogo')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
