"""El Log #04 · diseño «Destino» (gloss 2 + tarjetas tipo destino de viaje). Cinta de noticiero arriba todo el video
y cada noticia se cuenta con tarjetas de marco blanco: variante A (foto a sangre con desenfoque progresivo abajo,
texto blanco, botón blanco y favorito de cristal) y variante B (foto arriba, contenido sobre blanco, botón negro y
corazón). La «foto» es un lienzo teñido y el objeto 3D vive dentro de ella: cada tarjeta se parte en dos capas,
`lo` (marco + foto, debajo del canvas 3D) y `hi` (desenfoque + textos, encima).
Tiempos = voz recortada de noticias/4 (voz/voz-norm.wav, 122.86 s). Necesita internet al capturar.
Uso: SALIDA=noticias/4/animaciones REL=noticias/4/animaciones python3 ejemplos/ellog-04-destino.py [ids…]   (SOLO_HTML=1 para revisar)
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import ellog_gloss as G
from ellog_gloss import js

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.getcwd()))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
FIN = 122.86
TOP = 410

G.PALETAS['gris'] = ('#24262d', '#0b0b0e', '#8d96a8', '#e6e9ef', '141,150,168', '#111318')

NOTICIAS = [(0.0, 2, '01', 'Google lanza Gemini 4 Argon'),
            (27.9, 'amb', '02', 'OpenAI vs. Apple: 100+ archivos'),
            (49.9, 1, '03', '8 estados demandan a OpenAI'),
            (79.5, 3, '04', 'GitHub rehízo su historial de ⭐'),
            (89.7, 'pass', '05', 'Música con IA: etiquetas y filtros'),
            (114.1, 0, '✓', '¿Le darías chance a Argon?')]
CORRIDO = ['Gemini 4 Argon: $2 / $10 por millón de tokens hasta el 30 nov', 'Desde el 1 dic: $4 / $20',
           'Argon en la app de Gemini (Pro y Ultra), AI Mode y Antigravity', 'OpenAI: ~100 archivos de un dispositivo sin lanzar',
           'Apple dice no tener evidencia', 'Demandas en Arizona, Arkansas, Idaho, Iowa, Kansas, Montana, Nebraska y West Virginia',
           'GitHub: historial de estrellas de ~2,500 a ~24 peticiones', 'YouTube Music: «Fully Gen AI» y «Partly Gen AI»',
           'Deezer: filtro anti-IA antes de fin de año']

SHIELD = 'M12 1.5 3.5 4.8v6.1c0 5.3 3.6 10 8.5 11.6 4.9-1.6 8.5-6.3 8.5-11.6V4.8z'

# iconos de línea (estilo de la referencia)
ICON = {
    'tag': '<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.2"/>',
    'cal': '<rect x="3" y="4" width="18" height="18" rx="3"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    'heart': '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    'code': '<path d="m16 18 6-6-6-6M8 6l-6 6 6 6"/>',
    'folder': '<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>',
    'scale': '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10M12 3v18M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
    'star': '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z"/>',
    'music': '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
    'mic': '<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M19 10v1a7 7 0 0 1-14 0v-1M12 18v4"/>',
    'trend': '<path d="M22 7 13.5 15.5 8.5 10.5 2 17"/><path d="M16 7h6v6"/>',
    'chat': '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    'bot': '<path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2M20 14h2M15 13v2M9 13v2"/>',
    'play': '<polygon points="6 3 20 12 6 21 6 3"/>',
    'check': '<path d="M20 6 9 17l-5-5"/>',
    'lock': '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
}


def ic(n, extra=''):
    return f'<svg class="ico{extra}" viewBox="0 0 24 24">{ICON[n]}</svg>'


def foto(pal):
    c1, c2, ac, ac2 = G.PALETAS[pal][:4]
    return f'radial-gradient(120% 75% at 50% 16%,{ac2} 0%,{ac} 30%,{c1} 72%,{c2} 100%)'


FCSS = """
.p1.lo,.p2.lo,.p3.lo{z-index:4}
.fc{position:absolute;animation:cardIn .85s cubic-bezier(.22,1.15,.36,1) both}
@keyframes cardIn{from{opacity:0;transform:translateY(150px) scale(.92)}to{opacity:1;transform:none}}
.fc.lo{border-radius:calc(var(--k)*36px);background:linear-gradient(180deg,#ffffff,#f1f2f5);
  box-shadow:inset 0 -2px 0 rgba(0,0,0,.05),0 calc(var(--k)*26px) calc(var(--k)*56px) rgba(0,0,0,.5),0 0 calc(var(--k)*50px) rgba(var(--acr),.22)}
.fc .ph{position:absolute;left:calc(var(--k)*8px);right:calc(var(--k)*8px);top:calc(var(--k)*8px);bottom:calc(var(--k)*8px);border-radius:calc(var(--k)*30px);overflow:hidden;background:var(--ph)}
.fc.b .ph{bottom:auto;height:var(--phh)}
.fc.h .ph{right:auto;width:var(--phw);bottom:calc(var(--k)*8px);height:auto}
.fc .ph:before{content:'';position:absolute;left:8%;right:8%;top:10%;height:62%;border-radius:50%;background:radial-gradient(closest-side,rgba(255,255,255,.42),rgba(255,255,255,.08) 60%,transparent);filter:blur(10px)}
.fc .ph:after{content:'';position:absolute;left:-12%;right:-12%;bottom:-10%;height:40%;border-radius:50% 50% 0 0;background:linear-gradient(180deg,rgba(255,255,255,.14),rgba(0,0,0,.28));filter:blur(2px)}
.fc.hi{background:none}
.fc .bl{position:absolute;left:calc(var(--k)*8px);right:calc(var(--k)*8px);bottom:calc(var(--k)*8px);height:var(--blh,50%);border-radius:0 0 calc(var(--k)*30px) calc(var(--k)*30px);
  -webkit-backdrop-filter:blur(calc(var(--k)*11px));backdrop-filter:blur(calc(var(--k)*11px));
  -webkit-mask:linear-gradient(180deg,transparent,#000 40%);mask:linear-gradient(180deg,transparent,#000 40%);
  background:linear-gradient(180deg,rgba(0,0,0,0),rgba(0,0,0,.45))}
.fc .ct{position:absolute;left:calc(var(--k)*28px);right:calc(var(--k)*28px);bottom:calc(var(--k)*28px);color:#fff}
.fc.b .ct{color:#1a1a1a}
.fc.h .ct{left:calc(var(--phw) + var(--k)*34px);top:50%;bottom:auto;transform:translateY(-50%)}
.fc .t{font-size:calc(var(--k)*30px);font-weight:700;letter-spacing:-.035em;line-height:1.04}
.fc .s{font-size:calc(var(--k)*18px);font-weight:500;margin-top:calc(var(--k)*6px);color:rgba(255,255,255,.68);line-height:1.25}
.fc.b .s{color:#9a9a9a}
.fc .m{display:flex;flex-wrap:wrap;gap:calc(var(--k)*8px) calc(var(--k)*20px);margin-top:calc(var(--k)*20px);font-size:calc(var(--k)*16px);font-weight:500}
.fc .m>span{display:inline-flex;align-items:center;gap:calc(var(--k)*8px)}
.fc .m b{font-weight:800}.fc .m s{opacity:.45;margin-left:calc(var(--k)*4px)}
.ico{width:calc(var(--k)*17px);height:calc(var(--k)*17px);fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;opacity:.7;flex-shrink:0}
.fc .bt{display:flex;gap:calc(var(--k)*10px);margin-top:calc(var(--k)*22px)}
.fc .cta{flex:1;height:calc(var(--k)*48px);border-radius:999px;display:flex;align-items:center;justify-content:center;gap:calc(var(--k)*8px);font-size:calc(var(--k)*15px);font-weight:700;white-space:nowrap;
  background:linear-gradient(180deg,#ffffff,#e9e9ee);color:#1a1a1a;box-shadow:inset 0 -2px 0 rgba(0,0,0,.06),0 calc(var(--k)*6px) calc(var(--k)*16px) rgba(0,0,0,.28)}
.fc.b .cta{background:linear-gradient(180deg,#2b2b2e,#121214);color:#fff;box-shadow:inset 0 1.5px 0 rgba(255,255,255,.18),0 calc(var(--k)*6px) calc(var(--k)*14px) rgba(0,0,0,.25)}
.fc .cta.ac{background:linear-gradient(180deg,var(--ac2),var(--ac));color:var(--ink)}
.fc .cta .ico{opacity:1}
.fc .hrt{width:calc(var(--k)*48px);height:calc(var(--k)*48px);border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;background:#fff;box-shadow:inset 0 0 0 1.5px #e4e4e8;color:#e5484d}
.fc .hrt .ico{width:calc(var(--k)*20px);height:calc(var(--k)*20px);opacity:1}.fc .hrt svg:not(.ico){width:calc(var(--k)*20px);height:calc(var(--k)*20px)}
.fc .fav{position:absolute;top:calc(var(--k)*22px);right:calc(var(--k)*22px);width:calc(var(--k)*44px);height:calc(var(--k)*44px);border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;
  background:rgba(255,255,255,.16);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.45)}
.fc .fav .ico{width:calc(var(--k)*20px);height:calc(var(--k)*20px);opacity:1}
.like .ico{animation:like .5s cubic-bezier(.22,1.6,.36,1) var(--ld) forwards}
@keyframes like{40%{transform:scale(1.4)}to{fill:#e5484d;stroke:#e5484d;transform:none}}
.tap{animation:tap .3s ease var(--td) both}@keyframes tap{50%{transform:scale(.92)}}
.tag{position:absolute;top:calc(var(--k)*22px);left:calc(var(--k)*22px);display:inline-flex;align-items:center;gap:calc(var(--k)*7px);padding:calc(var(--k)*9px) calc(var(--k)*15px);border-radius:999px;
  font-size:calc(var(--k)*14px);font-weight:700;color:#fff;white-space:nowrap;background:rgba(255,255,255,.16);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.4)}
.tag svg{width:calc(var(--k)*18px);height:calc(var(--k)*18px)}
.tag.w{background:#fff;color:#1a1a1a;box-shadow:0 10px 26px rgba(0,0,0,.3)}
.fc .em{position:absolute;left:0;right:0;text-align:center;font-size:calc(var(--k)*100px);line-height:1;top:50%;transform:translateY(-58%);filter:drop-shadow(0 14px 24px rgba(0,0,0,.35))}
.fc .lg{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.fc .lg svg{filter:drop-shadow(0 16px 30px rgba(0,0,0,.35))}
.ring{position:absolute;inset:-10px;border-radius:calc(var(--k)*36px + 10px);box-shadow:0 0 0 7px var(--ac),0 0 50px rgba(var(--acr),.8);opacity:0;animation:pop .45s cubic-bezier(.22,1.6,.36,1) both}
.vs{position:absolute;width:150px;height:150px;margin:-75px 0 0 -75px;border-radius:50%;display:flex;align-items:center;justify-content:center;z-index:9;
  font-size:52px;font-weight:800;letter-spacing:-.04em;background:linear-gradient(160deg,var(--ac2),var(--ac));color:var(--ink);
  box-shadow:inset 0 3px 0 rgba(255,255,255,.6),0 0 0 12px rgba(255,255,255,.95),0 30px 60px rgba(0,0,0,.5)}
.below{position:absolute;left:0;right:0;text-align:center;z-index:9}.below .pill{font-size:36px;padding:20px 40px}
"""


def fc(v, x, y, w, h, k, pal, d, body, phh=None, phw=None, fav=None, lo_in='', hi_in='', blh=None):
    """Tarjeta de la referencia: devuelve (capa baja, capa alta) con la misma geometría y la misma animación."""
    st = f'left:{x}px;top:{y}px;width:{w}px;height:{h}px;--k:{k};--ph:{foto(pal)};animation-delay:{d}'
    st += f';--phh:{phh}px' if phh else ''
    st += f';--phw:{phw}px' if phw else ''
    st += f';--blh:{blh}' if blh else ''
    c1, c2, ac, ac2, acr, ink = G.PALETAS[pal]
    st += f';--ac:{ac};--ac2:{ac2};--acr:{acr};--ink:{ink}'
    fv = '' if fav is None else f'<div class="fav{" like" if fav else ""}" style="--ld:{fav or "0s"}">{ic("heart")}</div>'
    lo = f'<div class="fc {v} lo" style="{st}"><div class="ph">{lo_in}</div></div>'
    hi = f'<div class="fc {v} hi" style="{st}">{"<div class=bl></div>" if v == "a" else ""}{hi_in}{fv}<div class="ct">{body}</div></div>'
    return lo, hi


def meta(*items):
    return '<div class="m">' + ''.join(f'<span class="pop" style="animation-delay:{d}">{ic(i)}{h}</span>' for i, h, d in items) + '</div>'


def boton(txt, d, icon=None, ac=False, heart=None, tap=None, hrt_html=None):
    hr = ''
    if heart is not None or hrt_html:
        hr = f'<div class="hrt{" like" if heart else ""}" style="--ld:{heart or "0s"}">{hrt_html or ic("heart")}</div>'
    t = f' tap" style="--td:{tap}' if tap else ''
    return f'<div class="bt pop" style="animation-delay:{d}"><div class="cta{" ac" if ac else ""}{t}">{ic(icon) if icon else ""}{txt}</div>{hr}</div>'


# geometría: tarjeta grande y par de tarjetas lado a lado
BX, BW, BK = 150, 780, 2.4
LX, RX, SW, SK = 50, 560, 470, 1.44

LIB = r"""const {THREE}=R;
R.robot=(w)=>{const G=R.group();G.add(R.rbox(w,w*.86,w*.8,w*.16,R.metal('#5b6270',{roughness:.22})));
 const visor=R.rbox(w*.8,w*.26,10,w*.12,R.gloss('#0b0c10',{roughness:.08}));visor.position.set(0,R.u(w*.08),R.u(w*.41));G.add(visor);
 const em=R.gloss('#ff3030',{emissive:'#ff1010',emissiveIntensity:1.6});G.userData.em=em;
 for(const x of[-1,1]){const e=new THREE.Mesh(new THREE.SphereGeometry(R.u(w*.07),24,16),em);e.position.set(R.u(x*w*.2),R.u(w*.08),R.u(w*.45));G.add(e)}
 const ant=new THREE.Mesh(new THREE.CylinderGeometry(R.u(w*.025),R.u(w*.025),R.u(w*.3),16),R.metal('#c9d2de'));ant.position.y=R.u(w*.56);G.add(ant);
 const tip=new THREE.Mesh(new THREE.SphereGeometry(R.u(w*.06),24,16),em);tip.position.y=R.u(w*.72);G.add(tip);
 for(const x of[-1,1]){const ear=new THREE.Mesh(new THREE.CylinderGeometry(R.u(w*.12),R.u(w*.12),R.u(w*.1),32),R.metal('#3a404c'));ear.rotation.z=Math.PI/2;ear.position.x=R.u(x*w*.53);G.add(ear)}
 return G};
R.gem=(w)=>R.shape(""" + js(G.svgpath('googlegemini')) + r""",w,3,R.iri('#bcd4ff',{metalness:.55,roughness:.1,opacity:1,transparent:false,emissive:'#3b6cff',emissiveIntensity:.18}),.7);
R.gavel=(w)=>{const G=R.group(),wood=R.gloss('#8a5428',{roughness:.3}),band=R.metal('#e2b74a',{roughness:.2});
 const head=new THREE.Mesh(new THREE.CylinderGeometry(R.u(w*.17),R.u(w*.17),R.u(w*.62),40),wood);head.rotation.z=Math.PI/2;G.add(head);
 for(const x of[-1,1]){const b=new THREE.Mesh(new THREE.CylinderGeometry(R.u(w*.18),R.u(w*.18),R.u(w*.05),40),band);b.rotation.z=Math.PI/2;b.position.x=R.u(x*w*.22);G.add(b)}
 const h=new THREE.Mesh(new THREE.CylinderGeometry(R.u(w*.05),R.u(w*.065),R.u(w*.95),24),wood);h.position.y=R.u(-w*.52);G.add(h);return G};
R.vinyl=(r,lab)=>{const G=R.group(),V=R.group();G.add(V);
 const d=new THREE.Mesh(new THREE.CylinderGeometry(R.u(r),R.u(r),R.u(r*.05),96),R.gloss('#121318',{roughness:.22}));d.rotation.x=Math.PI/2;V.add(d);
 for(let i=1;i<6;i++){const g=new THREE.Mesh(new THREE.TorusGeometry(R.u(r*(.4+i*.1)),R.u(r*.006),8,140),R.metal('#454955',{roughness:.3}));g.position.z=R.u(r*.026);V.add(g)}
 const l=new THREE.Mesh(new THREE.CylinderGeometry(R.u(r*.33),R.u(r*.33),R.u(r*.06),64),R.gloss(lab,{emissive:lab,emissiveIntensity:.35}));l.rotation.x=Math.PI/2;V.add(l);
 const p=new THREE.Mesh(new THREE.CylinderGeometry(R.u(r*.05),R.u(r*.05),R.u(r*.09),24),R.metal('#e8e8ee'));p.rotation.x=Math.PI/2;V.add(p);G.userData.V=V;return G};
R.sheet=(c)=>{const G=R.group();G.add(R.rbox(120,150,5,12,R.gloss('#ffffff',{roughness:.3})));
 const s=R.rbox(84,14,6,6,R.gloss(c));s.position.set(0,R.u(42),R.u(1));G.add(s);
 for(let i=0;i<3;i++){const l=R.rbox(84,7,6,3,R.gloss('#c9ccd4'));l.position.set(0,R.u(14-i*20),R.u(1));G.add(l)}return G};
"""

PIEZAS = []


def escena(pid, start, end, n, css, body, js3d=None, script='', sigue=True):
    if sigue:
        end += 0.45
    PIEZAS.append((pid, start, end, G.page(FCSS + css, body, end - start, script, n=n, js3d=js3d, salida=not sigue, t0=start)))


def st(items, S, size=88):
    return G.steps(items, S, top=TOP, size=size)


# ───────── 0:00 · #01 Gemini 4 Argon
S = 0.0; A = G.at(S)
BY, BH = 420, 1340
lo1, hi1 = fc('a', BX, BY, BW, BH, BK, 2, A(0.2),
              f"""<div class="t">Gemini 4 Argon</div><div class="s pop" style="animation-delay:{A(2.5)}">Su modelo para código pesado</div>
{meta(('tag', '<b>$2</b> / M tokens<s>$4</s>', A(6.9)), ('cal', 'hasta el <b>30 nov</b>', A(7.5)))}
{boton('Mitad de precio en la API', A(5.8), 'code', tap=A(7.1))}""",
              fav=A(4.6), hi_in=f'<div class="tag pop" style="animation-delay:{A(1.0)}">{G.logo("google", "#fff")}Google</div>'
                               f'<div class="off" style="position:absolute;left:54px;top:500px"><span class="pill bad stamp" style="font-size:46px;padding:18px 36px;animation-delay:{A(6.5)}">−50 %</span></div>')
GR = [('💻', 'Código', 'apps y repos', 2, 10.4), ('🔬', 'Ciencias', 'investigación', 4, 11.0), ('📈', 'Finanzas', 'análisis', 'fin', 11.8), ('🛡️', 'Ciberseguridad', 'defensa', 1, 12.4)]
lo2 = hi2 = ''
for i, (e, t, s, p, t0) in enumerate(GR):
    l, h = fc('b', LX if i % 2 == 0 else RX, 600 + (i // 2) * 600, SW, 560, 1.3, p, A(t0), f'<div class="t">{t}</div><div class="s">{s}</div>',
              phh=360, lo_in=f'<div class="em">{e}</div>')
    lo2 += l; hi2 += h
escena('e00-argon', S, 13.9, 2, f"""
.p1{{animation:gone .4s ease {A(8.5)} forwards}}
.p2{{opacity:0;animation:fade .35s ease {A(8.6)} forwards}}
""", f"""<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>
<div class="p2 lo">{lo2}</div><div class="p2">{st([('Para lo <em>pesado</em>', 8.7, None)], S, 92)}{hi2}</div>""",
LIB + r"""const gm=R.gem(400);R.scene.add(gm);
return t=>{const a=R.eb(R.k(t,.35,.9)),o=R.eo(R.k(t,8.3,.45));gm.visible=t<8.8;gm.scale.setScalar(Math.max(.001,a*(1-o)));
 R.at(gm,540,860-o*200+12*Math.sin(t*1.6),2);gm.rotation.set(.15+.08*Math.sin(t*1.1),(1-a)*3+.5*Math.sin(t*.8),.05*Math.sin(t*.9))}""")

# ───────── 0:14 · #01 (parte 2): dónde está y «ponlos a competir»
S = 13.9; A = G.at(S)
LUG = [(G.logo('googlegemini', '#fff', 140), 'App de Gemini', 'en las suscripciones', 2, 14.6, meta(('star', '<b>Pro</b>', A(17.6)), ('star', '<b>Ultra</b>', A(18.0)))),
       (G.logo('google', '#fff', 130), 'AI Mode', 'en Google Search', 4, 19.6, ''),
       ('<div class="em" style="font-size:150px;transform:translateY(-50%)">🚀</div>', 'Antigravity', 'su plataforma con agentes', 3, 20.8, meta(('lock', 'con <b>Ultra</b>', A(21.3))))]
lo1 = hi1 = ''
for i, (lg, t, s, p, t0, m) in enumerate(LUG):
    l, h = fc('b h', 70, 580 + i * 360, 940, 330, 1.6, p, A(t0), f'<div class="t">{t}</div><div class="s">{s}</div>{m}', phw=300,
              lo_in=lg if lg.startswith('<div') else f'<div class="lg">{lg}</div>')
    lo1 += l; hi1 += h
CY = 620
lo2a, hi2a = fc('a', LX, CY, SW, 820, SK, 'gris', A(22.9), f'<div class="t">Tu modelo</div><div class="s">el que ya usas</div>{boton("Revisar código", A(24.0), "code")}', fav='')
lo2b, hi2b = fc('b', RX, CY, SW, 820, SK, 2, A(23.5),
                f'<div class="t">Gemini 4 Argon</div><div class="s">a mitad de precio</div>{meta(("tag", "<b>$2</b> / M", A(24.6)))}{boton("Revisar código", A(24.4), "code", heart="")}', phh=440)
escena('e01-donde', S, 27.9, 2, f"""
.p1{{animation:gone .4s ease {A(22.2)} forwards}}
.p2{{opacity:0;animation:fade .35s ease {A(22.3)} forwards}}
""", f"""<div class="p1 lo">{lo1}</div><div class="p1">{st([('¿Dónde <em>está</em>?', 14.0, None)], S, 92)}{hi1}</div>
<div class="p2 lo">{lo2a}{lo2b}</div><div class="p2">{st([('¿Ya usas <em>otro modelo</em>?', 22.4, 25.1), ('Ponlos a <em>competir</em>', 25.2, None)], S, 88)}{hi2a}{hi2b}
 <div class="vs stamp" style="left:540px;top:{CY + 330}px;--r:-8deg;animation-delay:{A(26.2)}">VS</div>
 <div class="below" style="top:{CY + 870}px"><span class="pill on pop" style="animation-delay:{A(25.4)}">📅 el descuento acaba el 30 nov</span></div></div>""",
LIB + r"""const rb=R.robot(190);R.scene.add(rb);const gm=R.gem(230);R.scene.add(gm);
return t=>{const a=R.eb(R.k(t,23.2,.85)),b=R.eb(R.k(t,23.8,.85)),hit=Math.sin(Math.PI*R.k(t,26.2,.35));
 rb.visible=t>22.9;rb.scale.setScalar(Math.max(.001,a));R.at(rb,285+hit*20,880,2);rb.rotation.set(.12+.05*Math.sin(t*1.3),.45+.25*Math.sin(t*.9),.05*Math.sin(t*2));
 gm.visible=t>23.5;gm.scale.setScalar(Math.max(.001,b));R.at(gm,795-hit*20,850,2);gm.rotation.set(.12,(1-b)*3-.4+.35*Math.sin(t*1.1),0)}""")

# ───────── 0:28 · #02 OpenAI: ex empleado se llevó archivos a Apple
S = 27.9; A = G.at(S)
PHH = 700
lo1, hi1 = fc('b', BX, BY, BW, BH, BK, 'amb', A(28.1),
              f"""<div class="t"><span id="nf">0</span>+ archivos</div><div class="s pop" style="animation-delay:{A(32.9)}">de productos sin lanzar</div>
{meta(('folder', 'un <b>dispositivo</b> de IA', A(33.5)), ('cal', 'último día: <b>2 jun</b>', A(34.0)))}
{boton('Lo mostró a directivos', A(35.0), hrt_html=G.logo('apple', '#1a1a1a'))}""",
              phh=PHH, hi_in=f'<div class="tag pop" style="animation-delay:{A(28.3)}">{G.logo("openai", "#fff")}OpenAI dice</div>'
                             f'<div class="tag w pop" style="top:620px;left:auto;right:53px;animation-delay:{A(29.1)}">{ic("user")}ex empleado → Apple</div>')
escena('e02-archivos', S, 36.6, 'amb', '', f'<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>',
LIB + "const OA=" + js(G.svgpath('openai')) + ",AP=" + js(G.svgpath('apple')) + r""";
const oa=R.shape(OA,220,3,R.gloss('#f4f4f6',{roughness:.18}),.5);R.scene.add(oa);
const ap=R.shape(AP,190,3,R.metal('#d9dbe2',{roughness:.14}),.5);R.scene.add(ap);
const sh=[];for(let i=0;i<9;i++){const s=R.sheet(i%2?'#ffb340':'#7aa7ff');s.userData={t:30.6+i*.32,z:(i%3)-1};R.scene.add(s);sh.push(s)}
return t=>{const a=R.eb(R.k(t,28.4,.8)),b=R.eb(R.k(t,29.9,.8)),gl=Math.sin(Math.PI*R.k(t,35.0,.7));
 oa.scale.setScalar(Math.max(.001,a));R.at(oa,330,790,1);oa.rotation.set(.15,.5*Math.sin(t*.9)+(1-a)*3,0);
 ap.visible=t>29.8;ap.scale.setScalar(Math.max(.001,b*(1+.15*gl)));R.at(ap,770,790,1);ap.rotation.set(.12,-.45*Math.sin(t*.8)+(1-b)*3,0);
 ap.material.emissive.set('#ffb340');ap.material.emissiveIntensity=.5*gl;
 for(const s of sh){const u=s.userData,p=R.k(t,u.t,1.3),e=R.eio(p);s.visible=p>0&&p<1;
  R.at(s,R.mix(380,730,e),790-Math.sin(Math.PI*e)*260,3+u.z);s.rotation.set(.3*Math.sin(t*3+u.z),e*2.5,e*1.2+u.z*.3);s.scale.setScalar(Math.max(.001,Math.sin(Math.PI*p)*.9+.1))}}""",
f"""window.__cnt=t=>{{t+={S};const e=1-Math.pow(1-Math.min(1,Math.max(0,(t-31.3)/1.0)),3);document.getElementById('nf').textContent=Math.round(100*e)}}""")

# ───────── 0:37 · #02 (parte 2): documento judicial → «ya está en los tribunales»
S = 36.6; A = G.at(S)
lo1, hi1 = fc('a', BX, 600, BW, 1160, BK, 'amb', A(36.8),
              f"""<div class="t pop" style="animation-delay:{A(38.5)}">Documento judicial</div><div class="s pop" style="animation-delay:{A(40.3)}">en la demanda de Apple contra OpenAI</div>
{meta(('scale', '<b>secretos</b> comerciales', A(41.9)))}
{boton('Apple: «no hay evidencia»', A(42.6))}""", fav='')
lo2a, hi2a = fc('b', LX, 640, SW, 760, 1.4, 0, A(43.9), '<div class="t">OpenAI</div><div class="s">su dispositivo de IA</div>', phh=470,
                lo_in=f'<div class="lg">{G.logo("openai", "#fff", 170)}</div>')
lo2b, hi2b = fc('b', RX, 640, SW, 760, 1.4, 'gris', A(44.2), '<div class="t">Apple</div><div class="s">sus propios dispositivos</div>', phh=470,
                lo_in=f'<div class="lg">{G.logo("apple", "#fff", 160)}</div>')
escena('e03-tribunal', S, 49.9, 'amb', f"""
.p1{{animation:gone .4s ease {A(43.6)} forwards}}
.p2{{opacity:0;animation:fade .35s ease {A(43.7)} forwards}}
.mk{{position:relative;display:inline-block}}.mk:after{{content:'';position:absolute;left:24px;right:24px;top:50%;height:7px;border-radius:4px;background:#ff4d5e;transform:scaleX(0);transform-origin:left;animation:strike .35s ease {A(46.9)} forwards}}
@keyframes strike{{to{{transform:scaleX(1)}}}}
""", f"""<div class="p1 lo">{lo1}</div><div class="p1">{st([('Pero <em>ojo</em>', 36.7, None)], S, 92)}{hi1}</div>
<div class="p2 lo">{lo2a}{lo2b}</div><div class="p2">{st([('¿Puro <em>marketing</em>?', 43.8, 47.2), ('Ya está en los<br><em>tribunales</em>', 47.3, None)], S, 88)}{hi2a}{hi2b}
 <div class="below" style="top:1470px"><span class="mk pop" style="animation-delay:{A(46.2)}"><span class="pill">📣 la pelea del hardware de IA</span></span></div>
 <div class="below" style="top:1610px"><span class="pill bad stamp" style="font-size:44px;animation-delay:{A(48.7)}">⚖️ en los tribunales</span></div></div>""",
LIB + r"""const gv=R.gavel(300);R.scene.add(gv);
return t=>{const a=R.eb(R.k(t,37.0,.9)),m=R.eio(R.k(t,43.4,.8)),sl=R.k(t,48.2,.5),hit=sl<.6?R.eio(sl/.6):1-R.eo((sl-.6)/.4)*.25;
 const y=R.mix(960,1500,m),x=R.mix(540,880,m);gv.scale.setScalar(Math.max(.001,a*R.mix(1,.6,m)));R.at(gv,x,y,3);
 gv.rotation.set(.25+.05*Math.sin(t*1.2),R.mix(-.5+.35*Math.sin(t*.8),-.2,m),R.mix(.35,.9,m)-hit*1.3*(t>48.2?1:0))}""")

# ───────── 0:50 · #03 ocho estados demandan a OpenAI
S = 49.9; A = G.at(S)
EST = [('IA', 'Iowa', 58.06), ('KS', 'Kansas', 58.47), ('AZ', 'Arizona', 59.05), ('NE', 'Nebraska', 0), ('AR', 'Arkansas', 0),
       ('ID', 'Idaho', 0), ('MT', 'Montana', 0), ('WV', 'W. Virginia', 0)]
lo1 = hi1 = ''
for i, (ab, nm, th) in enumerate(EST):
    ring = f'<div class="ring" style="animation-delay:{A(th)}"></div>' if th else ''
    l, h = fc('b', 60 + (i % 4) * 244, 660 + (i // 4) * 320, 228, 300, 1.0, 1 if th else 'gris', A(52.2 + i * .17),
              f'<div class="t" style="font-size:25px">{nm}</div>', phh=190,
              lo_in=f'<div class="em" style="font-size:78px;font-weight:800;letter-spacing:-.04em;color:#fff">{ab}</div>', hi_in=ring)
    lo1 += l; hi1 += h
lo2a, hi2a = fc('a', LX, 620, SW, 820, SK, 1, A(61.7), '<div class="t">Dañar a niños</div><div class="s">menores en riesgo</div>', fav='',
                lo_in='<div class="em" style="top:40%">🧒</div>')
lo2b, hi2b = fc('b', RX, 620, SW, 820, SK, 'gris', A(62.8), '<div class="t">Engañar</div><div class="s">sobre qué tan seguro es ChatGPT</div>', phh=470)
escena('e04-estados', S, 66.0, 1, f"""
.p1{{animation:gone .4s ease {A(61.1)} forwards}}
.p2{{opacity:0;animation:fade .35s ease {A(61.2)} forwards}}
""", f"""<div class="p1 lo">{lo1}</div><div class="p1">{st([('<em>8 estados</em> demandan<br>a OpenAI', 50.1, None)], S, 86)}{hi1}
 <div class="below" style="top:1330px"><span class="pill on pop" style="animation-delay:{A(55.4)}">🛡️ seguridad de ChatGPT con menores</span></div></div>
<div class="p2 lo">{lo2a}{lo2b}</div><div class="p2">{st([('Lo <em>acusan</em> de…', 61.3, None)], S, 92)}{hi2a}{hi2b}</div>""",
LIB + "const OA=" + js(G.svgpath('openai')) + ",SH=" + js(SHIELD) + r""";
const oa=R.shape(OA,250,3,R.gloss('#f4f4f6',{roughness:.18}),.5);R.scene.add(oa);
const sh=R.shape(SH,230,5,R.gloss('#8d96a8',{emissive:'#ff2a3a',emissiveIntensity:0,roughness:.16}));R.scene.add(sh);
return t=>{const a=R.eb(R.k(t,51.0,.85)),o=R.eo(R.k(t,60.9,.4)),b=R.eb(R.k(t,63.1,.8)),r=R.k(t,64.3,.5);
 oa.visible=t<61.4;oa.scale.setScalar(Math.max(.001,a*(1-o)));R.at(oa,540,1580,1);oa.rotation.set(.2,(1-a)*3+.6*Math.sin(t*.8),0);
 sh.visible=t>62.9;sh.scale.setScalar(Math.max(.001,b));R.at(sh,795,850,2);sh.rotation.set(.15,(1-b)*3+.4*Math.sin(t*1.1),r>0&&r<1?Math.sin(t*50)*.06:0);
 sh.material.color.set(r>.5?'#ff8a95':'#8d96a8');sh.material.emissiveIntensity=.45*r}""")

# ───────── 1:06 · #03 (parte 2): del diseño del chatbot a los agentes descontrolados; si usas su API
S = 66.0; A = G.at(S)
lo1a, hi1a = fc('b h', 70, 600, 940, 330, 1.6, 2, A(67.2), '<div class="t">Desde el diseño</div><div class="s">del chatbot</div>', phw=300,
                lo_in='<div class="em" style="font-size:150px;transform:translateY(-50%)">💬</div>')
lo1b, hi1b = fc('a', 70, 1060, 940, 600, 1.6, 1, A(70.8), '<div class="t">Hasta agentes</div><div class="s">descontrolados</div>', fav='', blh='42%')
CODE = ['<i>const</i> r = <i>await</i> client.chat({', '  model, messages,', '  tools: [agente]', '})']
code = ''.join(f'<div class="ln" style="animation-delay:{A(73.9 + k * .35)}">{c}</div>' for k, c in enumerate(CODE))
lo2, hi2 = fc('b', BX, 660, BW, 1000, BK, 'gris', A(73.5),
              f"""<div class="t pop" style="animation-delay:{A(75.3)}">Puede cambiar</div><div class="s pop" style="animation-delay:{A(76.2)}">cómo se lanzan</div>
{meta(('chat', '<b>chatbots</b>', A(77.8)), ('bot', '<b>agentes</b>', A(78.5)))}""", phh=640,
              lo_in=f'<div class="code">{code}</div>')
escena('e05-demandas', S, 79.5, 1, f"""
.p1{{animation:gone .4s ease {A(73.0)} forwards}}
.p2{{opacity:0;animation:fade .35s ease {A(73.1)} forwards}}
.code{{position:absolute;left:60px;right:60px;top:150px;padding:40px 44px;border-radius:40px;background:rgba(8,9,12,.72);box-shadow:inset 0 1.5px 0 rgba(255,255,255,.15);
  font-family:'JetBrains Mono',monospace;font-size:34px;line-height:1.6;color:#e6e9ef;white-space:pre}}
.code .ln{{opacity:0;animation:fade .25s ease forwards}}.code i{{font-style:normal;color:#ff8a6b}}
""", f"""<div class="p1 lo">{lo1a}{lo1b}</div><div class="p1">{st([('Las demandas van…', 66.1, None)], S, 88)}{hi1a}{hi1b}
 <div class="below" style="top:960px"><span class="pill pop" style="animation-delay:{A(68.7)}">⬇ hasta</span></div></div>
<div class="p2 lo">{lo2}</div><div class="p2">{st([('¿Construyes sobre<br>su <em>API</em>?', 73.2, None)], S, 86)}{hi2}</div>""",
LIB + r"""const rb=R.robot(230);R.scene.add(rb);
return t=>{const a=R.eb(R.k(t,71.1,.8)),o=R.eo(R.k(t,72.8,.35)),c=R.k(t,71.6,.2);
 rb.visible=t>70.9&&t<73.2;rb.scale.setScalar(Math.max(.001,a*(1-o)));R.at(rb,540+(c>0?Math.sin(t*37)*14:0),1250,2);
 rb.rotation.set(.1+(c>0?.25*Math.sin(t*9):0),-.3+(c>0?1.2*Math.sin(t*5.3):0),c>0?.3*Math.sin(t*7.1):0);rb.userData.em.emissiveIntensity=1.6+(c>0?2*Math.abs(Math.sin(t*12)):0)}""")

# ───────── 1:20 · #04 GitHub rehízo el historial de estrellas
S = 79.5; A = G.at(S)
lo1, hi1 = fc('a', BX, BY, BW, BH, BK, 3, A(79.7),
              f"""<div class="t">Historial de estrellas</div><div class="s pop" style="animation-delay:{A(80.4)}">GitHub lo rehízo desde cero</div>
{meta(('trend', '<b id="rq">2,500</b> peticiones', A(82.0)), ('star', 'repo de <b>251K</b>', A(82.6)))}
{boton('≈100× menos peticiones', A(85.0), 'check', ac=True)}""",
              fav=A(81.0), hi_in=f'<div class="tag pop" style="animation-delay:{A(79.9)}">{G.logo("github", "#fff")}GitHub</div>')
AV = ''.join(f'<i style="background:linear-gradient(160deg,{a},{b})"></i>' for a, b in
             [('#ffd9cc', '#ff8a6b'), ('#dbe8ff', '#6ea8ff'), ('#f1fbc9', '#c6e64a'), ('#e9e0ff', '#a78bfa'), ('#d3f4ff', '#4fd2ff'), ('#ffe6c2', '#ffb340')])
lo2a, hi2a = fc('a', LX, 620, SW, 820, SK, 'gris', A(86.1), '<div class="t">Quién te dio ⭐</div><div class="s">ya no se devuelve</div>', fav='',
                lo_in=f'<div class="avs">{AV}</div>', hi_in=f'<div class="below" style="top:250px"><span class="pill bad stamp" style="font-size:40px;animation-delay:{A(86.6)}">✕ oculto</span></div>')
lo2b, hi2b = fc('b', RX, 620, SW, 820, SK, 3, A(87.4),
                f'<div class="t">La tendencia</div><div class="s">por semana y por día</div>{meta(("check", "<b>sin nombres</b>", A(88.6)))}', phh=470,
                lo_in='<svg class="chart" viewBox="0 0 400 300"><path d="M20 260 L80 240 L130 245 L180 200 L230 190 L280 130 L330 110 L380 40"/></svg>')
escena('e06-estrellas', S, 89.7, 3, f"""
.p1{{animation:gone .4s ease {A(85.8)} forwards}}
.p2{{opacity:0;animation:fade .35s ease {A(85.9)} forwards}}
.avs{{position:absolute;left:50px;right:50px;top:110px;display:grid;grid-template-columns:repeat(3,1fr);gap:26px;filter:blur(7px)}}
.avs i{{aspect-ratio:1;border-radius:50%;box-shadow:inset 0 3px 0 rgba(255,255,255,.5)}}
.chart{{position:absolute;left:30px;right:30px;top:60px;width:calc(100% - 60px);height:360px;overflow:visible}}
.chart path{{fill:none;stroke:#fff;stroke-width:12;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:700;stroke-dashoffset:700;filter:drop-shadow(0 10px 20px rgba(0,0,0,.35));
  animation:draw 1s cubic-bezier(.45,0,.2,1) {A(88.0)} forwards}}@keyframes draw{{to{{stroke-dashoffset:0}}}}
""", f"""<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>
<div class="p2 lo">{lo2a}{lo2b}</div><div class="p2">{st([('Ya no dice <em>quién</em>', 86.0, None)], S, 92)}{hi2a}{hi2b}</div>""",
LIB + r"""const sr=R.star(5,190,82,60,R.gloss('#ffd34d',{emissive:'#ffb000',emissiveIntensity:.25,metalness:.3,roughness:.14}));R.scene.add(sr);
return t=>{const a=R.eb(R.k(t,80.0,.9)),o=R.eo(R.k(t,85.6,.4)),p=Math.sin(Math.PI*R.k(t,84.0,.6));
 sr.visible=t<86.1;sr.scale.setScalar(Math.max(.001,a*(1-o)*(1+.12*p)));R.at(sr,540,860+10*Math.sin(t*1.5),2);sr.rotation.set(.18+.06*Math.sin(t*1.2),(1-a)*3+.55*Math.sin(t*1.2),.08*Math.sin(t*.9))}""",
f"""window.__cnt=t=>{{t+={S};const e=1-Math.pow(1-Math.min(1,Math.max(0,(t-83.9)/1.1)),3);document.getElementById('rq').textContent=Math.round(2500-2476*e).toLocaleString('en-US')}}""")

# ───────── 1:30 · #05 YouTube Music etiqueta la música hecha con IA
S = 89.7; A = G.at(S)
lo1, hi1 = fc('a', BX, BY, BW, BH, BK, 'pass', A(89.9),
              f"""<div class="t">Hecha con IA</div><div class="s pop" style="animation-delay:{A(93.8)}">aunque sea solo una parte</div>
{meta(('mic', '<b>voz</b>', A(94.9)), ('music', '<b>composición</b>', A(95.3)))}
<div class="pg pop" style="animation-delay:{A(96.8)}"><i></i></div>
{boton('Reproducir', A(96.8), 'play', tap=A(98.8))}""",
              fav='', hi_in=f'<div class="tag pop" style="animation-delay:{A(90.1)}">{G.logo("youtubemusic", "#fff")}YouTube Music</div>'
                            f'<div class="tag w stamp" style="top:150px;--r:-3deg;animation-delay:{A(91.3)}">✨ Fully Gen AI</div>'
                            f'<div class="tag w stamp" style="top:250px;--r:2deg;animation-delay:{A(94.3)}">◐ Partly Gen AI</div>')
escena('e07-ytmusic', S, 100.2, 'pass', f"""
.pg{{height:12px;border-radius:6px;background:rgba(255,255,255,.22);margin-top:44px;overflow:hidden}}
.pg i{{display:block;height:100%;width:100%;border-radius:6px;background:#fff;transform-origin:left;transform:scaleX(0);animation:pgo 4s linear {A(98.9)} forwards}}
@keyframes pgo{{to{{transform:scaleX(.35)}}}}
""", f'<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>',
LIB + r"""const vy=R.vinyl(250,'#ff2d48');R.scene.add(vy);const V=vy.userData.V;
return t=>{const a=R.eb(R.k(t,90.1,.9)),sp=R.k(t,98.8,.6);vy.scale.setScalar(Math.max(.001,a));R.at(vy,540,840,1);
 vy.rotation.set(.35+.06*Math.sin(t*1.1),-.35+.2*Math.sin(t*.7)+(1-a)*2.5,0);V.rotation.y=0;V.rotation.z=-(t*.6+Math.max(0,t-98.8)*4*sp)}""")

# ───────── 1:40 · #05 (parte 2): Deezer y su botón para quitar la música de IA
S = 100.2; A = G.at(S)
lo1, hi1 = fc('b', BX, BY, BW, BH, BK, 0, A(100.4),
              f"""<div class="t pop" style="animation-delay:{A(101.3)}">Filtro anti-IA</div><div class="s pop" style="animation-delay:{A(102.8)}">un botón para quitar toda la música de IA</div>
<div class="tg pop" style="animation-delay:{A(103.2)}"><span>Ocultar música IA</span><b><i></i></b></div>
{meta(('cal', 'antes de <b>fin de año</b>', A(109.3)))}
{boton('Próximamente', A(106.8), 'clock', heart='')}""", phh=640,
              hi_in=f'<div class="tag pop" style="animation-delay:{A(100.6)}">{G.logo("deezer", "#fff")}Deezer</div>'
                    f'<div class="below" style="top:520px"><span class="pill bad stamp" style="font-size:40px;animation-delay:{A(106.5)}">⏳ todavía no sale</span></div>')
lo2a, hi2a = fc('a', LX, 620, SW, 820, SK, 'pass', A(110.7), f'<div class="t">YouTube Music</div><div class="s">etiquetas de IA</div>{boton("Ya está", A(111.3), "check")}', fav='',
                lo_in=f'<div class="lg" style="bottom:40%">{G.logo("youtubemusic", "#fff", 170)}</div>')
lo2b, hi2b = fc('b', RX, 620, SW, 820, SK, 0, A(111.0), f'<div class="t">Deezer</div><div class="s">filtro anti-IA</div>{boton("Fin de año", A(111.6), "clock", heart="")}', phh=440,
                lo_in=f'<div class="lg">{G.logo("deezer", "#fff", 170)}</div>')
escena('e08-deezer', S, 114.1, 0, f"""
.p1{{animation:gone .4s ease {A(110.4)} forwards}}
.p2{{opacity:0;animation:fade .35s ease {A(110.5)} forwards}}
.tg{{display:flex;align-items:center;justify-content:space-between;margin-top:34px;padding:22px 30px;border-radius:999px;background:#f3f3f6;font-size:36px;font-weight:700}}
.tg b{{position:relative;width:120px;height:68px;border-radius:34px;background:#d9d9df;animation:tgOn .3s ease {A(103.9)} forwards}}
.tg b i{{position:absolute;left:6px;top:6px;width:56px;height:56px;border-radius:50%;background:#fff;box-shadow:0 4px 12px rgba(0,0,0,.25);animation:tgK .3s cubic-bezier(.22,1.4,.36,1) {A(103.9)} forwards}}
@keyframes tgOn{{to{{background:#a78bfa}}}}@keyframes tgK{{to{{transform:translateX(52px)}}}}
""", f"""<div class="p1 lo">{lo1}</div><div class="p1">{hi1}</div>
<div class="p2 lo">{lo2a}{lo2b}</div><div class="p2">{st([('¿Creas música con <em>IA</em>?', 110.6, None)], S, 88)}{hi2a}{hi2b}
 <div class="below" style="top:1500px"><span class="pill on stamp" style="font-size:40px;--r:-3deg;animation-delay:{A(112.6)}">🏷️ el etiquetado ya viene</span></div></div>""",
LIB + "const DZ=" + js(G.svgpath('deezer')) + r""";
const dz=R.shape(DZ,360,3,R.iri('#d9c9ff',{metalness:.5,roughness:.1,opacity:1,transparent:false,emissive:'#7c5ce6',emissiveIntensity:.2}),.5);R.scene.add(dz);
return t=>{const a=R.eb(R.k(t,100.6,.9)),o=R.eo(R.k(t,110.2,.4));dz.visible=t<110.7;dz.scale.setScalar(Math.max(.001,a*(1-o)));
 R.at(dz,540,760+10*Math.sin(t*1.4),2);dz.rotation.set(.2+.06*Math.sin(t*1.2),(1-a)*3+.45*Math.sin(t*.8),0)}""")

# ───────── 1:54 · cierre: ¿le darías chance a Argon? (arriba entra «Sígueme»)
S = 114.1; A = G.at(S)
lo1a, hi1a = fc('a', LX, 620, SW, 840, SK, 2, A(115.5),
                f'<div class="t">Gemini 4 Argon</div><div class="s">con su descuento</div>{meta(("tag", "<b>$2</b> / M", A(117.2)))}{boton("Probarlo", A(116.4))}', fav=A(117.5))
lo1b, hi1b = fc('b', RX, 620, SW, 840, SK, 'gris', A(117.8),
                f'<div class="t">Lo que ya usas</div><div class="s">tu modelo de siempre</div>{boton("Me quedo", A(118.4), heart=A(119.1))}', phh=460)
SEG_INI = 119.6
escena('e09-cierre', S, FIN, 0, f"""
.p1{{animation:gone .4s ease {A(119.5)} forwards}}
""", f"""<div class="p1 lo">{lo1a}{lo1b}</div><div class="p1">{st([('¿Le darías <em>chance</em>?', 114.9, None)], S, 92)}{hi1a}{hi1b}
 <div class="vs stamp" style="left:540px;top:1040px;--r:6deg;font-size:44px;animation-delay:{A(117.9)}">¿o?</div></div>""",
LIB + r"""const gm=R.gem(240);R.scene.add(gm);const rb=R.robot(180);R.scene.add(rb);
const tx=R.text('EL LOG',140,60,R.iri('#b9a2ff',{metalness:.85,roughness:.14,opacity:1,transparent:false,iridescence:1}));R.scene.add(tx);
return t=>{const a=R.eb(R.k(t,115.8,.85)),b=R.eb(R.k(t,118.1,.85)),o=R.eo(R.k(t,119.3,.4));
 gm.visible=t>115.5&&t<119.8;gm.scale.setScalar(Math.max(.001,a*(1-o)));R.at(gm,285,860,2);gm.rotation.set(.15,(1-a)*3+.45*Math.sin(t*1.1),0);
 rb.visible=t>117.8&&t<119.8;rb.scale.setScalar(Math.max(.001,b*(1-o)));R.at(rb,795,850,2);rb.rotation.set(.12+.05*Math.sin(t*1.3),-.45+.3*Math.sin(t*.9),.05*Math.sin(t*2));
 const c=R.eb(R.k(t,119.8,.8));tx.visible=t>119.7;tx.scale.setScalar(Math.max(.001,c));R.at(tx,540,1450+(1-c)*150);tx.rotation.set(.18+.05*Math.sin(t*2),(1-c)*1.8+.22*Math.sin(t*1.5),0)}""",
sigue=False)

# ───────── tarjeta «Sígueme» (entra al final, debajo de la cinta)
SEGUIR = G.tarjeta("""
.tt{display:flex;align-items:center;gap:24px;padding-right:170px}
.av{width:120px;height:120px;border-radius:50%;background:linear-gradient(160deg,#e9e0ff,#a78bfa);display:flex;align-items:center;justify-content:center;font-size:56px;font-weight:800;color:#160b33;
  box-shadow:inset 0 3px 0 rgba(255,255,255,.6),0 0 0 6px rgba(255,255,255,.12),0 0 40px rgba(167,139,250,.45)}
.nm{font-size:44px;font-weight:800;letter-spacing:-.03em}
.btn{position:relative;margin-top:30px;height:96px}
.btn span{position:absolute;inset:0;border-radius:999px;display:flex;align-items:center;justify-content:center;font-size:36px;font-weight:800}
.b1{background:linear-gradient(180deg,#e9e0ff,#a78bfa);color:#160b33;box-shadow:inset 0 2px 0 #fff,0 20px 50px rgba(167,139,250,.4);animation:tap .22s ease .8s,off .2s ease .97s forwards}
.b2{background:linear-gradient(180deg,rgba(255,255,255,.18),rgba(255,255,255,.07));opacity:0;animation:fade .25s ease .97s forwards}
@keyframes tap{50%{transform:scale(.92)}}
.q{margin-top:22px;text-align:center}.q .pill{font-size:28px}
.cm{display:flex;gap:18px;align-items:center;margin-top:20px;padding:20px 26px;border-radius:36px;background:linear-gradient(180deg,rgba(255,255,255,.1),rgba(255,255,255,.03));animation:pop .45s cubic-bezier(.22,1.3,.36,1) 1.5s both}
.cm .mini{background:linear-gradient(160deg,#e9e0ff,#a78bfa)}.cm .t{font-size:28px;font-weight:600}
""", """<div class="tt"><div class="av">A</div><div><div class="nm">Armando</div><div class="sub">El Log · cada semana</div></div></div>
<div class="btn"><span class="b1">Seguir</span><span class="b2">Siguiendo ✓</span></div>
<div class="q pop" style="animation-delay:.4s"><span class="pill on">💎 ¿Argon con descuento o lo de siempre?</span></div>
<div class="cm"><div class="mini">💬</div><div><div class="sub" style="font-size:21px">Tú · ahora</div><div class="t"><span class="type" style="--td:.9s;--n:24;animation-delay:1.7s">Ya lo estoy probando 👀</span></div></div></div>""",
round(FIN - SEG_INI, 2), pal='ia', top=380,
js3d=LIB + r"""const gm=R.gem(150);R.scene.add(gm);
return t=>{const a=R.IN(t),o=R.OUT(t);gm.scale.setScalar(Math.max(.001,a*(1-o)));R.at(gm,870,450-o*80,4);gm.rotation.set(.15,-.45+.5*Math.sin(t*1.2),0)}""")


# ───────── cinta de noticiero (todo el video, encima de las escenas)
def cinta():
    heads = []
    for k, (t0, pal, num, txt) in enumerate(NOTICIAS):
        t1 = NOTICIAS[k + 1][0] if k + 1 < len(NOTICIAS) else None
        ac, ac2, ink = G.PALETAS[pal][2], G.PALETAS[pal][3], G.PALETAS[pal][5]
        anim = f'hIn .5s cubic-bezier(.22,1.2,.36,1) {t0 + (.35 if k == 0 else 0):.2f}s both' + (f',hOut .35s ease {t1 - .05:.2f}s forwards' if t1 else '')
        heads.append(f'<div class="hl" style="animation:{anim}"><span class="nn" style="background:linear-gradient(160deg,{ac2},{ac});color:{ink}">{num}</span><span class="tx">{txt}</span></div>')
    crawl = ''.join(f'<span>{c}</span><i>◆</i>' for c in CORRIDO)
    css = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:transparent;font-family:{G.SANS};color:#fff;-webkit-font-smoothing:antialiased}}
.cin{{position:absolute;left:36px;right:36px;top:170px;animation:cIn .6s cubic-bezier(.22,1.2,.36,1) .05s both}}
@keyframes cIn{{from{{opacity:0;transform:translateY(-60px)}}to{{opacity:1;transform:none}}}}
.band{{position:relative;height:112px;border-radius:30px 30px 10px 10px;display:flex;align-items:center;overflow:hidden;
  background:linear-gradient(180deg,rgba(30,27,42,.94),rgba(14,13,20,.96));box-shadow:inset 0 1.5px 0 rgba(255,255,255,.22),0 26px 60px rgba(0,0,0,.55)}}
.lg{{height:100%;display:flex;align-items:center;gap:14px;padding:0 30px 0 28px;flex-shrink:0;font-size:38px;font-weight:800;letter-spacing:-.02em;color:#160b33;
  background:linear-gradient(160deg,#e9e0ff,#a78bfa);box-shadow:inset 0 2px 0 rgba(255,255,255,.6),12px 0 40px rgba(167,139,250,.35)}}
.lg i{{width:18px;height:18px;border-radius:50%;background:#ff2d48;box-shadow:0 0 0 0 rgba(255,45,72,.7);animation:rec 1.2s ease-in-out infinite}}
@keyframes rec{{50%{{box-shadow:0 0 0 9px rgba(255,45,72,0);opacity:.55}}}}
.hs{{position:relative;flex:1;height:100%}}
.hl{{position:absolute;inset:0;display:flex;align-items:center;gap:18px;padding:0 26px;opacity:0}}
.hl .nn{{min-width:62px;height:62px;padding:0 10px;border-radius:31px;display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:800;flex-shrink:0;box-shadow:inset 0 2px 0 rgba(255,255,255,.6)}}
.hl .tx{{font-size:31px;font-weight:700;letter-spacing:-.01em;line-height:1.1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
@keyframes hIn{{from{{opacity:0;transform:translateY(60px)}}to{{opacity:1;transform:none}}}}
@keyframes hOut{{to{{opacity:0;transform:translateY(-60px)}}}}
.crawl{{position:relative;margin-top:6px;height:54px;border-radius:10px 10px 24px 24px;overflow:hidden;display:flex;align-items:center;
  background:linear-gradient(90deg,rgba(167,139,250,.92),rgba(124,92,230,.92));box-shadow:0 18px 40px rgba(0,0,0,.4)}}
.crawl .tag{{position:relative;z-index:2;height:100%;display:flex;align-items:center;padding:0 22px;font-size:22px;font-weight:800;letter-spacing:.08em;color:#fff;background:#160b33}}
.mv{{display:flex;align-items:center;white-space:nowrap;gap:22px;padding-left:22px;font-size:25px;font-weight:700;color:#160b33;animation:mv {FIN:.2f}s linear both}}
.mv i{{font-style:normal;font-size:16px;opacity:.6}}
@keyframes mv{{from{{transform:translateX(0)}}to{{transform:translateX(-{len(CORRIDO) * 2 * 520}px)}}}}
"""
    body = f"""<div class="cin"><div class="band"><div class="lg"><i></i>EL LOG</div><div class="hs">{''.join(heads)}</div></div>
<div class="crawl"><span class="tag">ÚLTIMO</span><div class="mv">{crawl}{crawl}{crawl}</div></div></div>"""
    return f"""<!doctype html><html><head><meta charset="utf-8">{G.FONTS}<style>{css}</style>
<script>window.__listo=Promise.resolve();</script></head><body>{body}</body></html>"""


PIEZAS.append(('seguir', SEG_INI, FIN, SEGUIR))
PIEZAS.append(('cinta', 0.0, FIN, cinta()))  # al final: queda encima de todo
PRE = 'cards-'

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
        rel = os.environ.get('REL', 'noticias/4/animaciones')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
