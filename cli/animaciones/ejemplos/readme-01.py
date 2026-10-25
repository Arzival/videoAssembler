"""El Readme #01 · SDD — sección de conceptos: todo animación con objetos 3D (como El Log), pero con identidad propia:
pestaña «README.md» con migas markdown en vez de la cinta de noticiero, encabezados tipo «## Paso 1», bloque «> ⚠️ Ojo»,
tarjeta resumen para guardar y cierre «actualizar el README».
Base = la ficha de «Catálogo» (imagen con 3D, título tipo archivo, metadatos, etiquetas, pestañas que cambian solas y bloque
de comando con copiar), con la piel de uno de tres estilos de prueba:
  cabana — vidrio translúcido con borde blanco sobre bosque con niebla y luz ámbar (ref. WoodNest)
  pista  — tarjeta gris oscura sobre degradado granate → naranja, negritas y píldoras rojas (ref. app de F1)
  notas  — vidrio esmerilado violeta con halo ámbar y degradado lavanda → naranja (ref. app de notas IA)
Variante tel = la ficha dentro de un teléfono con su botón principal (como las referencias); full = la ficha libre sobre el fondo.
Tiempos = readme/1/voz/voz-norm.wav (125.30 s).
Uso: ESTILO=cabana VAR=tel SALIDA=readme/1/cabana-tel REL=readme/1/cabana-tel python3 ejemplos/readme-01.py [ids…]   (SOLO_HTML=1 para revisar)
"""
import importlib.util, json, os, random, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import ellog_gloss as G
from ellog_gloss import js

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('catalogo', os.path.join(HERE, 'ellog-04-catalogo.py'))
C = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(C)
D = C.D
ic = C.ic

CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.getcwd()))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
E = os.environ.get('ESTILO', 'cabana')
V = os.environ.get('VAR', 'full')
TEL = V == 'tel'
TIT = V == 'titular'     # propuesta B: titular grande + 3D libre al centro + ficha solo de texto abajo
FIN = 125.30

# geometría de la ficha grande (en «tel» va dentro del teléfono)
if TEL:
    PX, PY, PW, PH = 150, 350, 780, 1500
    CX, CY, CW = 180, 450, 720
elif TIT:
    CX, CY, CW = 100, 945, 880
else:
    CX, CY, CW = 100, 400, 880
SC = CW / 880
CK, CH = 2.5 * SC, round(1240 * SC)
IH0 = 600
IMX, IMY = 540, round(CY + 11 * CK + IH0 * SC / 2)     # centro de la imagen (ancla del 3D)
S3D = 1.0
if TIT:
    CH, IMY, S3D = 700, 790, 1.1

G.PALETAS['rm-cabana'] = ('#3e5a60', '#172326', '#f5b82e', '#ffe6b0', '245,184,46', '#1f2f33')
G.PALETAS['rm-pista'] = ('#8b3a3e', '#2c2b2e', '#ff8a5c', '#ffd2bd', '226,96,63', '#2a0c05')
G.PALETAS['rm-notas'] = ('#5b4a9c', '#0b0a10', '#f5a54a', '#ffe1bd', '169,156,240', '#1a1622')
PAL = f'rm-{E}'

FONT = {'cabana': ('Space+Grotesk:wght@300;400;500;600;700', "'Space Grotesk'"),
        'pista': ('Inter:wght@400;500;600;700;800;900', "'Inter'"),
        'notas': ('Outfit:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400;1,500;1,600', "'Outfit'")}[E]
FLINK = f'<link href="https://fonts.googleapis.com/css2?family={FONT[0]}&display=block" rel="stylesheet">'
FF = FONT[1]

# ───────────────────────── fondo + teléfono + ficha (piel de cada estilo)
COMMON = f"""
.scene{{font-family:{FF},system-ui,sans-serif}}
.cc .cb,.cc .ti{{font-family:{FF},system-ui,sans-serif}}
.phone{{position:absolute;z-index:3;animation:pIn .7s cubic-bezier(.22,1.15,.36,1) both}}
@keyframes pIn{{from{{opacity:0;transform:translateY(80px) scale(.96)}}to{{opacity:1;transform:none}}}}
.ph-h{{position:absolute;display:flex;align-items:center;justify-content:space-between}}
.cta{{position:absolute;z-index:9;display:flex;align-items:center;justify-content:center;animation:pop .6s cubic-bezier(.22,1.35,.36,1) both}}
.cta.tap{{animation:pop .6s cubic-bezier(.22,1.35,.36,1) both,tapc .5s ease var(--tp) both}}
.chip.st{{animation:none;opacity:var(--on)}}
.dots{{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.16) 1.6px,transparent 1.8px);background-size:38px 38px;
  -webkit-mask-image:radial-gradient(90% 70% at 50% 45%,#000,transparent);mask-image:radial-gradient(90% 70% at 50% 45%,#000,transparent)}}
.circ{{position:absolute;inset:0;width:1080px;height:1920px}}
@keyframes pulse{{from{{stroke-dashoffset:100}}to{{stroke-dashoffset:0}}}}
.codes{{position:absolute;inset:0;overflow:hidden}}
.cl{{position:absolute;font-family:'JetBrains Mono',monospace;font-size:22px;color:rgba(255,255,255,.13);white-space:nowrap;animation:cf 30s linear infinite}}
@keyframes cf{{from{{transform:translateY(40px)}}to{{transform:translateY(-40px)}}}}
.glow2{{position:absolute;left:50%;bottom:-200px;width:1100px;height:700px;margin-left:-550px;border-radius:50%;filter:blur(20px)}}
.sum{{position:absolute;left:7%;top:10%;font-family:'JetBrains Mono',monospace;font-size:calc(var(--k)*15px);line-height:1.85;font-weight:700;color:#fff;z-index:2;text-shadow:0 4px 18px rgba(0,0,0,.35)}}
.sum b{{color:var(--ac)}}.sum div{{opacity:0;animation:fade .3s ease forwards}}
"""
SKIN = {}
SKIN['cabana'] = """
.scene{background:radial-gradient(1200px 900px at 50% -10%,rgba(95,150,158,.55),rgba(95,150,158,0) 70%),linear-gradient(180deg,#14292d 0%,#0d1c1f 55%,#081214 100%)}
.glow2{background:radial-gradient(closest-side,rgba(245,184,46,.22),transparent)}
.bg1,.bg2{display:none}
.cc.lo{border-radius:calc(var(--k)*20px);background:linear-gradient(180deg,rgba(43,64,70,.6),rgba(18,29,32,.82));-webkit-backdrop-filter:blur(24px) saturate(1.2);backdrop-filter:blur(24px) saturate(1.2);
  box-shadow:inset 0 0 0 2.5px rgba(255,255,255,.34),0 40px 90px rgba(0,0,0,.4)}
.cc .im{border-radius:calc(var(--k)*14px);background:repeating-linear-gradient(0deg,rgba(159,211,218,.07) 0 1.5px,transparent 1.5px 34px),repeating-linear-gradient(90deg,rgba(159,211,218,.07) 0 1.5px,transparent 1.5px 34px),
  radial-gradient(120% 90% at 50% 0%,#4f8a92 0%,#25494f 45%,#122a2e 80%,#0b1a1c 100%)!important}
.cc .im:before{left:-10%;right:-10%;top:auto;bottom:-25%;height:75%;background:radial-gradient(closest-side,rgba(255,196,110,.6),rgba(232,144,44,.18) 55%,transparent);filter:blur(14px)}
.ti{font-weight:500;letter-spacing:-.02em}.mt{color:#a9babd}.mt b{color:#fff}.mt .sp{background:rgba(255,255,255,.2)}.ds{color:#d5dfe0}
.tg span{border-radius:calc(var(--k)*6px)}
.tg .v{color:#ffe6b0;background:rgba(245,184,46,.14);border-color:rgba(245,184,46,.55)}
.tg .gr{color:#fff;background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.45)}
.tg .cy{color:#c6e6ea;background:rgba(120,190,200,.14);border-color:rgba(150,205,214,.5)}
.dt{border-top-color:rgba(255,255,255,.18)}.tabs>span:after{background:#f5b82e}
.cm{background:rgba(10,18,20,.55);box-shadow:inset 0 0 0 1px rgba(255,255,255,.14)}.cm .c em{color:#f5b82e}.cm .c i{color:#93a8ab}
.cm .ok{background:#fff;color:#1f2f33}
.chip{background:rgba(20,32,35,.5);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.4);border-radius:calc(var(--k)*8px)}
.phone{border-radius:70px;background:rgba(62,90,96,.22);-webkit-backdrop-filter:blur(16px) saturate(1.2);backdrop-filter:blur(16px) saturate(1.2);box-shadow:inset 0 0 0 3px rgba(255,255,255,.45),0 50px 120px rgba(0,0,0,.4)}
.ph-h{left:44px;right:44px;top:34px;font-size:30px;font-weight:500}.ph-h .lg{display:flex;align-items:center;gap:12px}
.ph-h .lg i{width:40px;height:40px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#ffd36b,#e8902c);box-shadow:0 0 18px rgba(232,144,44,.6)}
.ph-h .hb{width:40px;height:16px;border-top:3px solid #fff;border-bottom:3px solid #fff}
.cta{border-radius:16px;background:#fff;color:#1f2f33;font-size:32px;font-weight:600;box-shadow:0 20px 50px rgba(0,0,0,.3)}
@keyframes tapc{40%{transform:scale(.95);background:#f5b82e}to{background:#f5b82e}}
"""
SKIN['pista'] = """
.scene{background:radial-gradient(1300px 1000px at 50% -12%,rgba(226,96,63,.85),rgba(139,58,62,.45) 45%,rgba(44,43,46,0) 75%),linear-gradient(180deg,#3a2426 0%,#2c2b2e 50%,#1f1e21 100%)}
.glow2{background:radial-gradient(closest-side,rgba(214,58,69,.25),transparent)}
.floor{position:absolute;left:-50%;right:-50%;bottom:-200px;height:900px;transform:perspective(700px) rotateX(64deg);transform-origin:50% 100%;opacity:.5;
  background:repeating-linear-gradient(90deg,rgba(255,138,92,.45) 0 2px,transparent 2px 90px),repeating-linear-gradient(0deg,rgba(255,138,92,.45) 0 2px,transparent 2px 90px);
  -webkit-mask-image:linear-gradient(0deg,#000 20%,transparent 85%);mask-image:linear-gradient(0deg,#000 20%,transparent 85%);animation:flr 1.6s linear infinite}
@keyframes flr{to{background-position:0 90px,0 90px}}
.bg1,.bg2{display:none}
.cc.lo{border-radius:calc(var(--k)*24px);background:#2c2b2e;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.07),0 40px 90px rgba(0,0,0,.5)}
.cc .im{border-radius:calc(var(--k)*18px);background:linear-gradient(180deg,#8b3a3e 0%,#c94a3c 35%,#e2603f 55%,#8b3a3e 85%,#5a3032 100%)!important}
.cc .im:before{background:radial-gradient(closest-side,rgba(255,190,150,.5),rgba(255,140,90,.12) 60%,transparent)}
.ti{font-weight:800;letter-spacing:-.035em}.mt{color:rgba(255,255,255,.62)}.mt b{color:#fff}.mt .sp{background:rgba(255,255,255,.22)}.ds{color:rgba(255,255,255,.82)}
.tg span{border-radius:999px;padding:0 calc(var(--k)*9px)}
.tg .v{color:#fff;background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.28)}
.tg .gr{color:#2c2b2e;background:#fff;border-color:#fff}
.tg .cy{color:#ffd2bd;background:rgba(226,96,63,.2);border-color:rgba(226,96,63,.65)}
.tg .rd{color:#fff;background:#d63a45;border-color:#d63a45}
.dt{border-top:1.5px solid rgba(255,255,255,.12)}.tabs>span:after{background:#e2603f;height:3px}
.cm{background:#3f3e42;border-radius:999px}.cm .c{left:calc(var(--k)*14px)}.cm .c em{color:#ffb38a}.cm .c i{color:rgba(255,255,255,.5)}
.cm .ok{background:#d63a45;color:#fff}
.chip{background:rgba(255,255,255,.2);border-radius:999px;box-shadow:none}
.phone{border-radius:96px;background:linear-gradient(180deg,#8b3a3e 0%,#d0533f 26%,#7a3438 52%,#2c2b2e 76%);overflow:hidden;
  box-shadow:inset 0 0 0 14px #3f3e42,inset 0 0 0 16px #55545a,0 50px 120px rgba(0,0,0,.5)}
.ph-h{left:62px;right:62px;top:36px;font-size:28px;font-weight:600}.ph-h .sig{letter-spacing:.1em;font-size:22px}
.cta{justify-content:flex-start;padding:0 16px 0 44px;border-radius:999px;background:#d63a45;color:#fff;font-size:34px;font-weight:500;box-shadow:0 24px 50px rgba(214,58,69,.4)}
.cta:after{content:'↗';margin-left:auto;width:84px;height:84px;border-radius:50%;background:rgba(255,255,255,.2);display:flex;align-items:center;justify-content:center;font-size:38px}
@keyframes tapc{40%{transform:scale(.95);background:#e2603f}to{background:#e2603f}}
"""
SKIN['notas'] = """
.scene{background:radial-gradient(1100px 1000px at 25% 8%,rgba(91,74,156,.95),rgba(91,74,156,0) 70%),radial-gradient(800px 800px at 95% 62%,rgba(245,165,74,.32),rgba(245,165,74,0) 70%),
  linear-gradient(180deg,#1a1622 0%,#120f19 60%,#08070b 100%)}
.bg1,.bg2{display:none}
.glow2{background:radial-gradient(closest-side,rgba(245,165,74,.22),transparent)}
.net{position:absolute;inset:0;width:1080px;height:1920px;animation:nd 14s ease-in-out infinite alternate}@keyframes nd{to{transform:translateY(-40px)}}
.cc.lo{border-radius:calc(var(--k)*22px);background:linear-gradient(180deg,rgba(255,255,255,.1),rgba(255,255,255,.04));-webkit-backdrop-filter:blur(28px) saturate(1.4);backdrop-filter:blur(28px) saturate(1.4);
  box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.14),0 40px 90px rgba(0,0,0,.45)}
.cc .im{border-radius:calc(var(--k)*16px);background:radial-gradient(120% 90% at 30% 8%,#b9adf5 0%,#6e5bb8 34%,#3a2d63 66%,#1a1622 100%)!important}
.cc .im:before{left:40%;right:-20%;top:auto;bottom:-30%;height:80%;background:radial-gradient(closest-side,rgba(245,165,74,.55),rgba(245,165,74,.12) 60%,transparent);filter:blur(16px)}
.ti{font-weight:600;letter-spacing:-.02em}
.mt{color:rgba(255,255,255,.55)}.mt b{color:#fff}.mt .sp{background:rgba(255,255,255,.18)}.ds{color:rgba(255,255,255,.78)}
.tg span{border-radius:999px;padding:0 calc(var(--k)*9px)}
.tg .v{color:#d6ccff;background:rgba(169,156,240,.16);border-color:rgba(169,156,240,.55)}
.tg .gr{color:#ffd59a;background:rgba(245,165,74,.14);border-color:rgba(245,165,74,.55)}
.tg .cy{color:#fff;background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.3)}
.dt{border-top:1.5px solid rgba(255,255,255,.1)}.tabs>span:after{background:linear-gradient(90deg,#a99cf0,#f5a54a);height:3px}
.cm{background:rgba(255,255,255,.07);border-radius:999px;box-shadow:inset 0 0 0 1px rgba(255,255,255,.1)}.cm .c{left:calc(var(--k)*14px)}.cm .c em{color:#f5a54a}.cm .c i{color:rgba(255,255,255,.45)}
.cm .ok{background:linear-gradient(90deg,#a99cf0,#f5a54a);color:#1a1622}
.chip{background:rgba(255,255,255,.1);border-radius:999px;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.18)}
.phone{border-radius:72px;background:linear-gradient(180deg,rgba(60,48,104,.55),rgba(20,16,28,.72));-webkit-backdrop-filter:blur(18px);backdrop-filter:blur(18px);
  box-shadow:inset 0 0 0 2px rgba(255,255,255,.16),0 50px 120px rgba(0,0,0,.55)}
.ph-h{left:52px;right:52px;top:36px;font-size:26px;font-weight:500}
.cta{border-radius:999px;background:linear-gradient(90deg,#a99cf0,#c9a6c4 50%,#f5a54a);color:#1a1622;font-size:32px;font-weight:600;box-shadow:0 20px 50px rgba(169,156,240,.35)}
@keyframes tapc{40%{transform:scale(.95);filter:brightness(1.2)}to{filter:brightness(1.12)}}
"""


CODE_LN = ['## Paso 1 · spec', 'spec.md › qué · para quién', 'const ctx = read("docs/INDEX.md")', 'tokens: 18 %', '$ npm test', '› implementa T1',
           'plan.md › framework · db', 'git diff --stat', 'if (spec.outdated) update()', '- [x] T2 formulario', 'model.review(pr)', '> ⚠️ ojo',
           'README.md · #01', 'ci: lint · types · agent', 'return { ok: true }', '$ cat docs/auth.md']


def fondo():
    """Fondo de tecnología en la paleta del estilo: rejilla de puntos, pistas de circuito con pulsos y líneas de código tenues."""
    ac = {'cabana': ('#9fd3da', '#f5b82e'), 'pista': ('#ffb38a', '#ff5a3c'), 'notas': ('#b9adf5', '#f5a54a')}[E]
    rnd = random.Random(11)
    # pistas de circuito: caminos ortogonales con un pulso que viaja
    paths = ''
    for i in range(14):
        x = rnd.choice([rnd.uniform(-20, 260), rnd.uniform(820, 1100)])
        y = rnd.uniform(120, 1880)
        d = f'M{x:.0f} {y:.0f}'
        for _ in range(4):
            if rnd.random() < .5:
                x += rnd.choice([-1, 1]) * rnd.uniform(60, 220)
            else:
                y += rnd.choice([-1, 1]) * rnd.uniform(60, 260)
            d += f' L{x:.0f} {y:.0f}'
        dur = rnd.uniform(3.5, 7)
        paths += (f'<path d="{d}" stroke="{ac[0]}" stroke-opacity=".16" stroke-width="2.5" fill="none"/>'
                  f'<circle cx="{x:.0f}" cy="{y:.0f}" r="6" fill="none" stroke="{ac[0]}" stroke-opacity=".3" stroke-width="2.5"/>'
                  f'<path d="{d}" stroke="{ac[1]}" stroke-width="3.5" fill="none" stroke-linecap="round" pathLength="100" stroke-dasharray="6 94" '
                  f'style="animation:pulse {dur:.1f}s linear {-rnd.uniform(0, dur):.1f}s infinite;filter:drop-shadow(0 0 6px {ac[1]})"/>')
    code = ''
    for i, ln in enumerate(CODE_LN):
        left = i % 2 == 0
        code += (f'<div class="cl" style="{"left" if left else "right"}:{rnd.uniform(24, 60):.0f}px;top:{100 + i * 112 + rnd.uniform(-20, 20):.0f}px;'
                 f'animation-delay:{-rnd.uniform(0, 30):.1f}s">{ln}</div>')
    extra = ''
    if E == 'pista':
        extra = '<div class="floor"></div>'
    elif E == 'notas':
        nodes = [(rnd.uniform(40, 1040), rnd.uniform(200, 1880)) for _ in range(16)]
        ln = ''.join(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="{ac[0]}" stroke-opacity=".14" stroke-width="2"/>'
                     for i, a in enumerate(nodes) for b in nodes[i + 1:] if (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 < 300 ** 2)
        dots = ''.join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(4, 8):.0f}" fill="{ac[1] if k % 4 == 0 else ac[0]}" fill-opacity=".55"/>' for k, (x, y) in enumerate(nodes))
        extra = f'<svg class="net" viewBox="0 0 1080 1920">{ln}{dots}</svg>'
    return (f'<div class="dots"></div>{extra}<svg class="circ" viewBox="0 0 1080 1920">{paths}</svg><div class="codes">{code}</div><div class="glow2"></div>')


def telefono():
    if not TEL:
        return ''
    if E == 'cabana':
        h = '<div class="ph-h"><span class="lg"><i></i>readme</span><span class="hb"></span></div>'
    elif E == 'pista':
        h = '<div class="ph-h"><span>11:30</span><span class="sig">▮▮▮ ◠ ▭</span></div>'
    else:
        h = '<div class="ph-h"><span>9:40</span><span>▮▮▮ ◠ ▭</span></div>'
    return f'<div class="phone" style="left:{PX}px;top:{PY}px;width:{PW}px;height:{PH}px">{h}</div>'


def boton(txt, A, d, tap=None):
    """Botón principal del teléfono (solo en «tel»)."""
    if not TEL:
        return ''
    st = f'left:{PX + 50}px;width:{PW - 100}px;top:{PY + PH - 190}px;height:{120 if E == "pista" else 108}px;animation-delay:{A(d)}' + (f',{A(tap)};--tp:{A(tap)}' if tap else '')
    return f'<div class="cta{" tap" if tap else ""}" style="{st}">{txt}</div>'


# ───────────────────────── 3D con los materiales de cada estilo
TEMA = {'cabana': ('#8a5428', '#f5b82e', '#f3ece0', '#d9e4e6'), 'pista': ('#d63a45', '#ff8a5c', '#f1eeee', '#ffd2bd'),
        'notas': ('#7c68d6', '#f5a54a', '#f4f0ff', '#d6ccff')}[E]
LIB = D.LIB + f"const C1='{TEMA[0]}',C2='{TEMA[1]}',C3='{TEMA[2]}',C4='{TEMA[3]}';" + r"""
const MAT=(c,o={})=>""" + {'cabana': "R.gloss(c,{roughness:.3,...o})", 'pista': "R.metal(c,{roughness:.2,...o})",
                          'notas': "R.iri(c,{metalness:.45,roughness:.12,opacity:1,transparent:false,...o})"}[E] + r""";
R.board=(w)=>{const G=R.group();G.add(R.rbox(w,w*1.3,w*.08,w*.08,MAT(C1)));
 const pp=R.rbox(w*.82,w*1.08,w*.04,w*.04,R.gloss(C3,{roughness:.35}));pp.position.set(0,R.u(-w*.06),R.u(w*.05));G.add(pp);
 const cl=R.rbox(w*.42,w*.16,w*.12,w*.06,R.metal('#e8ecf3'));cl.position.set(0,R.u(w*.62),R.u(w*.06));G.add(cl);
 const ls=[];for(let i=0;i<4;i++){const l=R.rbox(w*.56,w*.09,w*.05,w*.04,R.gloss(C2,{emissive:C2,emissiveIntensity:.1}));l.position.set(R.u(w*.08),R.u(w*.3-i*w*.2),R.u(w*.09));G.add(l);ls.push(l);
  const c=new THREE.Mesh(new THREE.SphereGeometry(R.u(w*.05),16,12),MAT(C1));c.position.set(R.u(-w*.28),R.u(w*.3-i*w*.2),R.u(w*.1));G.add(c)}
 G.userData.ls=ls;return G};
R.warn=(w)=>{const G=R.group();const t=R.shape('M12 1.8 23 21.5H1Z',w,4,MAT(C2,{emissive:C2,emissiveIntensity:.15}),.8);G.add(t);
 const ex=R.text('!',w*.42,w*.08,R.gloss('#1b1e26'));ex.position.set(0,R.u(-w*.08),R.u(w*.06));G.add(ex);G.userData.t=t;return G};
R.loop=(r)=>{const G=R.group();G.add(new THREE.Mesh(new THREE.TorusGeometry(R.u(r),R.u(r*.12),24,120,Math.PI*1.7),MAT(C2)));
 const cone=new THREE.Mesh(new THREE.ConeGeometry(R.u(r*.26),R.u(r*.42),32),MAT(C2));cone.position.set(R.u(r),R.u(-r*.12),0);G.add(cone);return G};
R.stairs=(w)=>{const G=R.group(),bs=[];for(let i=0;i<4;i++){const b=R.rbox(w,w*.3,w*.5,w*.08,i?R.gloss(C3,{roughness:.3}):MAT(C1));b.position.set(R.u(-w*1.1+i*w*.75),R.u(w*.6-i*w*.4),0);G.add(b);bs.push(b)}
 G.userData.bs=bs;return G};
R.tx=(s,size,depth)=>R.text(s,size,depth,MAT(C4,{metalness:.8,roughness:.14}));
R.bot=(w)=>{const r=R.robot(w);r.userData.em.color.set(C2);r.userData.em.emissive.set(C2);return r};
"""


def z(n):
    return round(n * SC * S3D)


# ───────────────────────── ficha y escena
PIEZAS = []
TRJS = """const _e=p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2;
const _v=(k,t)=>{let v=k[0][1];for(const [a,b,d] of k.slice(1)){const p=Math.min(1,Math.max(0,(t-a)/(d||.8)));v=v+(b-v)*_e(p)}return v};
const _N=[...document.querySelectorAll('[data-n]')].map(e=>[e,JSON.parse(e.dataset.n)]);
window.__cnt=t=>{t+=S0;for(const [e,k] of _N)e.textContent=(e.dataset.pre||'')+Math.round(_v(k,t)).toLocaleString('en-US')+(e.dataset.suf||'')};"""


def K(*keys):
    return js([list(k) for k in keys])


def N(keys, txt, suf=''):
    return f"<em data-n='{keys}'" + (f' data-suf="{suf}"' if suf else '') + f'>{txt}{suf}</em>'


def ficha(d, A, title, meta=(), desc='', tags=(), tabs=None, cmds=None, copy=None, ih=IH0, dd=None, lo_in='', hi_in=''):
    if TIT:
        ih, lo_in, hi_in = 0, '', ''
    return C.card(CX, CY, CW, CH, CK, PAL, d, A, title, meta, desc, tags, tabs, cmds, copy=copy, ih=round(ih * SC), dd=dd, lo_in=lo_in, hi_in=hi_in)


def paso(items, A):
    """Etiqueta sobre la imagen que cambia sola: [(html, entra, sale|None)]."""
    return ''.join(f'<div class="chip st" style="left:{z(30)}px;top:{z(30)}px;{C.win([(a, b)], A)}">{h}</div>' for h, a, b in items)


TITS = {
    's0-gancho': [('¿Tu IA se <em>inventa</em><br>tu app?', 0.1, 3.6), ('Antes del código,<br><em>escríbele una spec</em>', 3.7, None)],
    's1-sdd': [('<em>SDD</em>', 8.6, 12.8), ('Primero lo<br><em>dejas por escrito</em>', 12.88, 22.4), ('En la práctica,<br><em>4 pasos</em>', 22.5, None)],
    's2-pasos': [('## Paso 1<br><em>La spec</em>', 25.44, 31.95), ('## Paso 2<br><em>El plan</em>', 32.06, 37.8), ('## Paso 3<br><em>Las tareas</em>', 37.86, 40.8),
                 ('## Paso 4<br><em>Implementa</em>', 40.86, None)],
    's3-ejemplo': [('En mis <em>proyectos</em>', 48.5, 54.8), ('Solo lee lo que<br><em>ocupa</em>', 54.92, 59.7), ('Menos <em>tokens</em>,<br>cero inventos', 59.8, None)],
    's4-ojo': [('&gt; ⚠️ <em>Ojo</em>', 65.85, 68.0), ('Si se queda<br><em>desactualizada</em>', 68.08, 78.3), ('No la apruebes<br><em>sin leerla</em>', 78.38, 81.5),
               ('Ni de<br><em>40 páginas</em>', 81.52, None)],
    's5-cascada': [('¿Se vuelve<br><em>cascada</em>?', 90.1, 94.2), ('No: la spec<br><em>cambia contigo</em>', 94.28, None)],
    's6-hoy': [('Funciona <em>hoy</em>', 99.9, 104.8), ('Puede <em>cambiar</em>', 104.88, 110.0), ('Tema para<br><em>otro README</em>', 110.1, None)],
    's7-resumen': [('Tu próxima<br><em>spec</em>', 112.1, 118.7), ('¿Spec o<br><em>puro prompt</em>?', 118.78, None)],
    's8-cierre': [('Nos vemos cuando<br>toque <em>actualizar<br>el README</em>', 122.6, None)],
}
TCSS = {'cabana': ".ttl{font-weight:400;letter-spacing:-.035em}.ttl em{background:none;-webkit-background-clip:initial;background-clip:initial;color:rgba(232,240,241,.55)}",
        'pista': ".ttl{font-weight:800;letter-spacing:-.04em}.ttl em{background:none;-webkit-background-clip:initial;background-clip:initial;color:rgba(255,255,255,.72)}",
        'notas': ".ttl{font-weight:500;letter-spacing:-.03em}.ttl em{font-style:italic;background:linear-gradient(90deg,#d6ccff,#a99cf0 40%,#f5a54a);-webkit-background-clip:text;background-clip:text;color:transparent;padding-right:.06em}"}[E] + \
       ".ttl{font-family:" + FF + ",system-ui,sans-serif}.cc .im{display:none}.beam{z-index:1}"


def escena(pid, start, end, css, fases, js3d, sigue=True, boton_html=''):
    """fases = [(lo, hi)] → capas .pN lo (debajo del 3D) / .pN (encima)."""
    if sigue:
        end += G.COLA
    body = FLINK + fondo() + telefono() + ''.join(f'<div class="p{i + 1} lo">{lo}</div><div class="p{i + 1}">{hi}</div>' for i, (lo, hi) in enumerate(fases)) + boton_html
    if TIT:
        body = (FLINK + fondo() + f'<div class="beam" style="left:{IMX - 360}px;top:{IMY - 360}px;width:720px;height:720px"></div>'
                + body[len(FLINK + fondo()):] + f'<div style="position:absolute;inset:0;z-index:10">{G.steps(TITS[pid], start, cls="ttl", top=345, size=88)}</div>')
        css += TCSS
    PIEZAS.append((pid, start, end, G.page(C.CCSS + COMMON + SKIN[E] + css, body, end - start, f'const S0={start};' + TRJS, n=PAL, js3d=LIB + js3d, salida=not sigue, t0=start)))


def fase(n, a, b=None):
    return C.fase(n, a, b)


# ───────────────────────── 0:00 · gancho: la IA se inventa tu app → escríbele una spec
S = 0.0; A = G.at(S)
f1 = ficha(0.2, A, 'prompt-sin-spec', [('bot', 'tu IA'), ('clock', 'sin contexto')], 'Le pides código y se inventa cómo funciona tu aplicación.',
           [('v', 'firebase?', 1.3), ('v', 'roles?', 1.6), ('rd', 'inventado', 2.0)],
           [(ic('term'), 'Prompt', [(0.3, None)])],
           [('<i>›</i> hazme el <em>login</em>', [(0.3, 1.0)]), ('<i>🤖 usé</i> <em>Firebase</em> <i>y un panel admin…</i>', [(1.1, None)])], dd=0.9,
           hi_in=C.chip('🤖 tu IA', z(30), z(30), 0.5, A))
f2 = ficha(3.7, A, 'spec.md', [('file', 'especificaciones'), ('check', 'antes del código')], 'Antes de pedirle código, escríbele un documento de especificaciones.',
           [('gr', 'qué', 5.5), ('gr', 'para quién', 5.9), ('cy', 'cuándo está listo', 6.3)],
           [('📄', 'spec.md', [(3.9, None)]), (ic('code'), 'Código', [(99, None)])],
           [('<i>$</i> touch <em>spec.md</em>', [(4.1, None)])], copy=(6.6, None), dd=4.6,
           hi_in=C.chip('📄 primero esto', z(30), z(30), 4.2, A))
escena('s0-gancho', S, 8.5, fase(1, 0, A(3.5)) + fase(2, A(3.6)), [f1, f2], f"""const rb=R.bot({z(250)});R.scene.add(rb);const bd=R.board({z(210)});R.scene.add(bd);
return t=>{{const a=R.eb(R.k(t,.4,.8)),o=R.eo(R.k(t,3.3,.4)),b=R.eb(R.k(t,4.0,.8)),sh=R.k(t,2.0,.7);
 rb.visible=t<3.8;rb.scale.setScalar(Math.max(.001,a*(1-o)));R.at(rb,{IMX}+(sh>0&&sh<1?Math.sin(t*40)*10:0),{IMY}+10*Math.sin(t*1.6),3);
 rb.rotation.set(.1,-.4+.3*Math.sin(t*.9)+(sh>0&&sh<1?.5*Math.sin(t*22):0),0);rb.userData.em.emissiveIntensity=sh>0&&sh<1?3.2:1.4;
 bd.visible=t>3.9;bd.scale.setScalar(Math.max(.001,b));R.at(bd,{IMX},{IMY}+10*Math.sin(t*1.4),3);bd.rotation.set(.15,(1-b)*3-.35+.3*Math.sin(t*.8),.05);
 bd.userData.ls.forEach((l,i)=>{{l.material.emissiveIntensity=t>[5.1,5.5,5.9,6.3][i]?1:.1}})}}""",
       boton_html=boton('Escribir la spec', A, 4.4, tap=6.75))

# ───────────────────────── 0:08 · SDD: qué quieres, para quién, cuándo está terminado → 4 pasos
S = 8.5; A = G.at(S)
f1 = ficha(8.6, A, 'sdd', [('file', 'Spec-Driven Development')], 'Desarrollo guiado por especificaciones.',
           [('v', 'spec primero', 9.5), ('gr', 'código después', 10.6)],
           [('📘', 'Concepto', [(8.8, None)])], [('<i>SDD =</i> <em>spec</em> <i>→</i> <em>código</em>', [(9.5, None)])], dd=9.7)
f2 = ficha(12.8, A, 'antes-de-la-ia', [('code', '<b>0</b> líneas'), ('clock', 'por escrito')], 'Antes de que la IA escriba una sola línea, dejas por escrito:',
           [('v', 'qué quieres', 17.39), ('gr', 'para quién', 18.34), ('cy', 'cuándo está terminado', 20.5)],
           [('❓', 'Qué', [(13.0, 18.1)]), ('👤', 'Para quién', [(18.11, 19.8)]), ('🏁', 'Terminado', [(19.89, None)])],
           [('<i>## qué:</i> <em>lo que quieres</em>', [(13.0, 18.1)]), ('<i>## para:</i> <em>quién lo usa</em>', [(18.11, 19.8)]),
            ('<i>## listo cuando:</i> <em>…</em>', [(19.89, None)])], dd=13.2,
           hi_in=paso([('✍️ antes del código', 13.0, None)], A))
f3 = ficha(22.4, A, 'sdd · 4 pasos', [('check', 'en la práctica')], 'Spec, plan, tareas e implementación.',
           [('v', '1 spec', 24.14), ('v', '2 plan', 24.34), ('v', '3 tareas', 24.54), ('v', '4 código', 24.74)],
           [('1', 'Spec', [(24.2, None)]), ('2', 'Plan', [(99, None)]), ('3', 'Tareas', [(99, None)]), ('4', 'Código', [(99, None)])],
           [('<i>spec →</i> plan <i>→</i> tareas <i>→</i> <em>código</em>', [(24.2, None)])], dd=23.0)
escena('s1-sdd', S, 25.4, fase(1, 0, A(12.6)) + fase(2, A(12.7), A(22.2)) + fase(3, A(22.3)), [f1, f2, f3],
       f"""const tx=R.tx('SDD',{z(150)},{z(60)});R.scene.add(tx);const bd=R.board({z(200)});R.scene.add(bd);const n4=R.tx('4',{z(320)},{z(110)});R.scene.add(n4);
return t=>{{const a=R.eb(R.k(t,8.9,.9)),o=R.eo(R.k(t,12.4,.4)),b=R.eb(R.k(t,13.1,.8)),ob=R.eo(R.k(t,22.0,.4)),c=R.eb(R.k(t,23.9,.8));
 tx.visible=t<12.9;tx.scale.setScalar(Math.max(.001,a*(1-o)));R.at(tx,{IMX},{IMY}+10*Math.sin(t*1.5),2);tx.rotation.set(.15+.05*Math.sin(t*1.2),(1-a)*2+.3*Math.sin(t*.9),0);
 bd.visible=t>12.9&&t<22.5;bd.scale.setScalar(Math.max(.001,b*(1-ob)));R.at(bd,{IMX},{IMY}+10*Math.sin(t*1.4),3);bd.rotation.set(.15,(1-b)*3-.35+.3*Math.sin(t*.8),.05);
 bd.userData.ls.forEach((l,i)=>{{l.material.emissiveIntensity=t>[17.4,18.34,20.5,99][i]?1:.1}});
 n4.visible=t>23.8;n4.scale.setScalar(Math.max(.001,c));R.at(n4,{IMX},{IMY}+10*Math.sin(t*1.5),2);n4.rotation.set(.15,(1-c)*3+.4*Math.sin(t*.9),0)}}""")

# ───────────────────────── 0:25 · los 4 pasos: una sola ficha, las pestañas avanzan paso a paso
S = 25.4; A = G.at(S)
PAS = [(25.44, 32.0), (32.06, 37.8), (37.86, 40.8), (40.86, None)]
f1 = ficha(25.5, A, '## pasos', [('file', 'spec · plan · tareas'), ('clock', 'paso a paso')], 'Una spec, un plan, tareas pequeñas y la IA implementa una por una mientras revisas.',
           [('v', 'qué hace', 27.84), ('v', 'para quién', 28.42), ('rd', 'sin código', 29.4), ('gr', 'framework', 35.32), ('gr', 'base de datos', 36.07),
            ('cy', 'tareas pequeñas', 39.2), ('cy', 'una por una', 44.75), ('gr', 'tú revisas', 46.72)],
           [(f'{i + 1}', n, [w]) for i, (n, w) in enumerate(zip(['Spec', 'Plan', 'Tareas', 'Código'], PAS))],
           [('<i>spec.md ›</i> <em>qué hace · para quién</em>', [(25.6, 29.3)]), ('<i>spec.md ›</i> <s>código</s> <i>nada de código</i>', [(29.4, 32.0)]),
            ('<i>plan.md ›</i> <em>framework · base de datos</em>', [(32.06, 37.8)]), ('<i>tareas.md ›</i> <em>T1 · T2 · T3 · T4</em>', [(37.86, 40.8)]),
            ('<i>›</i> implementa <em>T1</em> <i>→ revisa ✓</i>', [(40.86, 44.7)]), ('<i>›</i> <em>una por una</em> <i>· tú revisas ✓</i>', [(44.75, None)])],
           copy=(47.0, None), ih=540, dd=26.0,
           hi_in=paso([('## Paso 1 · Spec', 25.5, 32.0), ('## Paso 2 · Plan', 32.06, 37.8), ('## Paso 3 · Tareas', 37.86, 40.8), ('## Paso 4 · Implementa', 40.86, None)], A))
escena('s2-pasos', S, 48.4, '.chip.st{font-family:"JetBrains Mono",monospace}', [f1], f"""const bd=R.board({z(200)});R.scene.add(bd);const L=bd.userData.ls;
return t=>{{const a=R.eb(R.k(t,25.8,.9)),sw=[32.06,37.86,40.86].reduce((s,x)=>s+R.eio(R.k(t,x,.6)),0);bd.scale.setScalar(Math.max(.001,a));
 R.at(bd,{IMX},{IMY - z(30)}+10*Math.sin(t*1.4),3);bd.rotation.set(.15,(1-a)*3-.35+.25*Math.sin(t*.8)+sw*6.283,.05);
 L.forEach((l,i)=>{{l.material.emissiveIntensity=t>[27.8,32.1,39.2,44.8][i]?1:.1}})}}""",
       boton_html=boton('Siguiente paso', A, 26.4))

# ───────────────────────── 0:48 · mi ejemplo: docs/ + INDEX.md → solo lee lo que ocupa → menos tokens
S = 48.4; A = G.at(S)
f1 = ficha(48.5, A, 'docs/', [('folder', 'mis proyectos'), ('file', 'INDEX.md')],
           'Una carpeta con la documentación y un índice que la IA lee primero; luego solo lee lo que ocupa.',
           [('v', 'INDEX.md', 52.98), ('gr', 'lee primero', 53.88), ('cy', 'solo lo que ocupa', 56.56), ('gr', 'menos tokens', 60.38), ('rd', '0 inventos', 62.53)],
           [('📘', 'INDEX.md', [(48.6, 56.5)]), ('📄', 'auth.md', [(56.56, 60.3)]), ('🪙', 'Tokens', [(60.38, None)])],
           [('<i>$</i> cat <em>docs/INDEX.md</em>', [(48.6, 56.5)]), ('<i>$</i> cat <em>docs/auth.md</em> <i># solo esto</i>', [(56.56, 60.3)]),
            ('<i>tokens:</i> ' + N(K((0, 100), (60.4, 18, 1.2)), '100', ' %') + ' <i>· inventos: 0</i>', [(60.38, None)])],
           copy=(54.4, 55.5), dd=50.6,
           hi_in=paso([('📁 docs/', 48.6, 52.9), ('📘 INDEX.md · lee primero', 52.98, 56.5), ('📄 solo auth.md', 56.56, None)], A))
escena('s3-ejemplo', S, 65.8, '', [f1], f"""const ss=[];for(let i=0;i<5;i++){{const s=R.sheet(i==0?C2:i==1?C1:'#a9b4bf');R.scene.add(s);ss.push(s)}}
return t=>{{ss.forEach((s,i)=>{{const a=R.eb(R.k(t,50.7+i*.15,.7)),pick=i==0?R.eio(R.k(t,53.9,.7))*(1-R.eio(R.k(t,56.4,.5))):i==1?R.eio(R.k(t,56.6,.8)):0,out=i>1?R.eo(R.k(t,56.6,.6)):0;
 s.visible=out<.99;s.scale.setScalar(Math.max(.001,a*(1-out)*{1.6 * SC:.2f}*(1+.3*pick)));R.at(s,{IMX - z(120)}+i*{z(60)},{IMY + z(30)}-i*{z(14)}-pick*{z(60)},3+i*.4+pick*2);
 s.rotation.set(.2+.05*Math.sin(t+i),-.35+.15*Math.sin(t*.8+i),.12-i*.06)}})}}""",
       boton_html=boton('Leer INDEX.md primero', A, 49.2, tap=53.9))

# ───────────────────────── 1:05 · > ⚠️ Ojo: desactualizada · sin leer · 40 páginas
S = 65.8; A = G.at(S)
f1 = ficha(65.9, A, '&gt; ⚠️ ojo', [('lock', 'cuidados'), ('check', '3')], 'Tres cuidados para que la spec te siga sirviendo.',
           [('rd', 'desactualizada', 69.5), ('gr', 'actualízala', 76.05), ('rd', 'sin leerla', 80.55), ('rd', '40 páginas', 83.66), ('rd', 'se come el contexto', 86.23)],
           [('1', 'Al día', [(68.08, 78.3)]), ('2', 'Léela', [(78.38, 81.5)]), ('3', 'Corta', [(81.52, None)])],
           [('<i>spec</i> v1 <i>≠ tu app</i> <em>v2</em>', [(66.0, 72.2)]), ('<i>la IA →</i> <em>programa algo que ya no existe</em>', [(72.3, 75.4)]),
            ('<i>cada cambio →</i> <em>actualiza spec.md</em>', [(75.46, 78.3)]), ('<s>[Aprobar]</s> <i>sin leer →</i> <em>léela primero</em>', [(78.38, 81.5)]),
            ('<i>páginas:</i> ' + N(K((0, 1), (83.7, 40, 1.0)), '1') + ' <i>· contexto:</i> ' + N(K((0, 10), (86.2, 100, 1.2)), '10', ' %'), [(81.52, None)])],
           dd=66.6,
           hi_in=paso([('⚠️ 1/3 · desactualizada', 68.08, 78.3), ('⚠️ 2/3 · sin leer', 78.38, 81.5), ('⚠️ 3/3 · 40 páginas', 81.52, None)], A))
escena('s4-ojo', S, 90.0, '', [f1], f"""const w=R.warn({z(240)});R.scene.add(w);
return t=>{{const a=R.eb(R.k(t,66.1,.9)),hot=R.k(t,86.2,1.2),b=[68.08,78.38,81.52].reduce((s,x)=>s+Math.sin(Math.PI*R.k(t,x,.5)),0);
 w.scale.setScalar(Math.max(.001,a*(1+.15*b)));R.at(w,{IMX}+(hot>.6?Math.sin(t*38)*8:0),{IMY}+10*Math.sin(t*1.5),3);w.rotation.set(.12+.05*Math.sin(t*1.2),(1-a)*3+.4*Math.sin(t*.9),0);
 w.userData.t.material.emissiveIntensity=.15+.25*b+hot*1.2}}""",
       boton_html=boton('Entendido', A, 66.6))

# ───────────────────────── 1:30 · ¿cascada? No: la spec cambia conforme avanzas
S = 90.0; A = G.at(S)
f1 = ficha(90.1, A, '¿cascada?', [('trend', 'de arriba abajo'), ('clock', 'conforme avanzas')], 'Alguien dirá que es cascada. No: la spec cambia conforme avanzas en el proyecto.',
           [('rd', 'cascada', 93.32), ('gr', 'no', 94.31), ('cy', 'iterar', 95.72), ('gr', 'conforme avanzas', 98.2)],
           [('⬇️', 'Cascada', [(90.2, 94.2)]), ('🔁', 'Ciclo', [(94.28, None)])],
           [('<i>spec → plan → tareas → código →</i> <em>fin</em>', [(90.2, 94.2)]), ('<i>spec ⇄ código ·</i> <em>↻ en cada avance</em>', [(94.28, None)])], dd=90.8,
           hi_in=paso([('⬇️ ¿cascada?', 90.2, 94.2), ('🔁 no: ciclo', 94.28, None)], A))
escena('s5-cascada', S, 99.86, '', [f1], f"""const st=R.stairs({z(130)});R.scene.add(st);const lp=R.loop({z(150)});R.scene.add(lp);
return t=>{{const a=R.eb(R.k(t,90.4,.8)),br=R.k(t,94.3,.7),b=R.eb(R.k(t,94.6,.8));
 st.visible=t<95.1;st.scale.setScalar(Math.max(.001,a*(1-R.eo(br))));R.at(st,{IMX},{IMY},2);st.rotation.set(.25,-.3+.2*Math.sin(t*.8),0);
 st.userData.bs.forEach((x,i)=>{{x.rotation.z=br*(i%2?.6:-.6)}});
 lp.visible=t>94.5;lp.scale.setScalar(Math.max(.001,b));R.at(lp,{IMX},{IMY},2);lp.rotation.set(.35+.1*Math.sin(t),.2*Math.sin(t*.7),-t*2.2)}}""",
       boton_html=boton('Iterar', A, 90.8))

# ───────────────────────── 1:40 · funciona hoy · puede cambiar · tema para otro README
S = 99.86; A = G.at(S)
f1 = ficha(99.95, A, 'funciona-hoy', [('cpu', 'modelos de hoy'), ('clock', '2026')], 'Funciona con los modelos que tenemos hoy. Puede llegar el punto en que ya no sea útil.',
           [('gr', 'hoy ✓', 102.28), ('v', 'modelos actuales', 103.35), ('rd', 'puede cambiar', 106.95), ('cy', 'otro README', 110.67)],
           [('✅', 'Hoy', [(100.0, 104.8)]), ('🔮', 'Mañana', [(104.88, None)])],
           [('<i>estado:</i> <em>funciona hoy</em>', [(100.0, 104.8)]), ('<i>mañana:</i> <em>¿otra forma de programar?</em>', [(104.88, 110.6)]),
            ('<i>pendiente:</i> <em>tema para otro README</em>', [(110.67, None)])], dd=100.6,
           hi_in=paso([('✅ hoy', 100.0, 104.8), ('🔮 mañana', 104.88, None)], A))
escena('s6-hoy', S, 112.04, '', [f1], f"""const rb=R.bot({z(230)});R.scene.add(rb);
return t=>{{const a=R.eb(R.k(t,100.2,.9)),c=R.eio(R.k(t,104.9,1.2));rb.scale.setScalar(Math.max(.001,a));R.at(rb,{IMX},{IMY}+10*Math.sin(t*1.6),3);
 rb.rotation.set(.1+.05*Math.sin(t*1.3),-.4+.3*Math.sin(t*.9)+c*6.283,0);rb.userData.em.emissiveIntensity=1.4+(t>104.9&&t<110.6?1.2*Math.abs(Math.sin(t*3)):0)}}""",
       boton_html=boton('Seguir aprendiendo', A, 100.6))

# ───────────────────────── 1:52 · resumen para guardar + pregunta
S = 112.04; A = G.at(S)
SUM = '<div class="sum">' + ''.join(f'<div style="animation-delay:{A(112.6 + i * .25)}"><b>{i + 1}</b> {n}</div>' for i, n in enumerate(['Spec', 'Plan', 'Tareas', 'Implementa'])) + \
      f'<div style="animation-delay:{A(113.8)}"><b>&gt;</b> ⚠️ Ojo</div></div>'
f1 = ficha(112.1, A, '# readme · sdd', [('check', 'guárdalo'), ('file', '1 página')], 'Antes de pedirle código, escríbele una página de especificaciones.',
           [('v', '1 spec', 112.6), ('v', '2 plan', 112.85), ('v', '3 tareas', 113.1), ('v', '4 implementa', 113.35),
            ('rd', 'actualízala', 113.8), ('rd', 'léela', 114.0), ('gr', '1 página, no 40', 114.2)],
           [('🔖', 'Guardar', [(112.3, 118.7)]), ('💬', 'Tu turno', [(118.78, None)])],
           [('<i>›</i> antes del código, <em>1 página de spec</em>', [(112.3, 118.7)]), ('<i>¿</i><em>spec</em> <i>o</i> <em>puro prompt</em><i>?</i>', [(118.78, None)])],
           copy=(116.5, 118.6), dd=113.0, lo_in=SUM,
           hi_in=paso([('🔖 guárdalo', 112.3, 118.7), ('💬 cuéntame', 118.78, None)], A))
escena('s7-resumen', S, 122.54, '.chip.st{left:auto!important;right:calc(var(--k)*12px)}', [f1], f"""const bd=R.board({z(180)});R.scene.add(bd);
return t=>{{const a=R.eb(R.k(t,112.4,.9));bd.scale.setScalar(Math.max(.001,a));R.at(bd,{IMX + z(190)},{IMY}+10*Math.sin(t*1.4),3);bd.rotation.set(.15,-.55+.2*Math.sin(t*.8),.06);
 bd.userData.ls.forEach((l,i)=>{{l.material.emissiveIntensity=t>112.6+i*.25?1:.1}})}}""",
       boton_html=boton('🔖 Guárdalo', A, 112.8, tap=116.5))

# ───────────────────────── 2:02 · cierre: «nos vemos cuando toque actualizar el README»
S = 122.54; A = G.at(S)
f1 = ficha(122.6, A, 'README.md', [('check', 'guardado'), ('clock', 'hasta la próxima')], 'Nos vemos cuando toque actualizar el README.',
           [('gr', '✓ guardado', 123.7)], [('💾', 'Guardar', [(122.7, None)])], [('<i>⌘S</i> <em>README.md</em>', [(122.8, None)])], copy=(123.6, None), dd=122.9)
escena('s8-cierre', S, FIN, '', [f1], f"""const tx=R.tx('README',{z(120)},{z(48)});R.scene.add(tx);
return t=>{{const c=R.eb(R.k(t,122.9,.8));tx.scale.setScalar(Math.max(.001,c));R.at(tx,{IMX},{IMY}+(1-c)*120,2);tx.rotation.set(.18+.05*Math.sin(t*2),(1-c)*1.8+.22*Math.sin(t*1.5),0)}}""",
       sigue=False, boton_html=boton('Seguir', A, 123.0, tap=124.2))

# ───────────────────────── pestaña README.md (identidad de la sección, encima de todo, en vez de la cinta de El Log)
SECC = [(0.0, '# SDD'), (8.5, '## ¿Qué es?'), (25.4, '## Paso 1 · La spec'), (32.0, '## Paso 2 · El plan'), (37.8, '## Paso 3 · Las tareas'),
        (40.8, '## Paso 4 · Implementa'), (48.4, '## Mi ejemplo'), (65.8, '&gt; ⚠️ Ojo'), (90.0, '## ¿Cascada?'), (99.86, '## Funciona hoy'),
        (112.04, '## Resumen'), (122.54, '✓ guardado')]


def pestana():
    crumbs = ''
    for k, (t0, txt) in enumerate(SECC):
        t1 = SECC[k + 1][0] if k + 1 < len(SECC) else None
        anim = f'cIn2 .4s cubic-bezier(.22,1.2,.36,1) {t0 + (.3 if k == 0 else 0):.2f}s both' + (f',cOut2 .25s ease {t1 - .05:.2f}s forwards' if t1 else '')
        crumbs += f'<span class="cr" style="animation:{anim}">{txt}</span>'
    skin = {
        'cabana': """.tb{background:linear-gradient(180deg,rgba(43,64,70,.7),rgba(24,37,41,.78));-webkit-backdrop-filter:blur(24px);backdrop-filter:blur(24px);border-radius:30px;box-shadow:inset 0 0 0 2.5px rgba(255,255,255,.3),0 24px 60px rgba(0,0,0,.35)}
.tab{background:rgba(255,255,255,.1);border-radius:18px;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.22)}.dt{background:#f5b82e;box-shadow:0 0 12px #f5b82e}.nm{color:#ffe6b0}""",
        'pista': """.tb{background:transparent}.tab{background:rgba(255,255,255,.2);border-radius:999px;-webkit-backdrop-filter:blur(20px);backdrop-filter:blur(20px)}
.circ{width:84px;height:84px;border-radius:50%;background:rgba(255,255,255,.2);-webkit-backdrop-filter:blur(20px);backdrop-filter:blur(20px);display:flex;align-items:center;justify-content:center;font-size:36px;flex-shrink:0}
.r1 .circ:last-child{margin-left:auto}.dt{background:#fff}.nm{color:#ffd2bd}.crumb{padding-left:100px}""",
        'notas': """.tb{background:transparent}.tab{background:rgba(255,255,255,.09);border-radius:999px;-webkit-backdrop-filter:blur(24px);backdrop-filter:blur(24px);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.14)}
.dt{background:linear-gradient(135deg,#a99cf0,#f5a54a);box-shadow:0 0 14px rgba(245,165,74,.7)}.nm{color:#d6ccff}
.circ{width:84px;height:84px;border-radius:50%;background:rgba(255,255,255,.09);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.14);display:flex;align-items:center;justify-content:center;font-size:34px;margin-left:auto}""",
    }[E]
    left = '<span class="circ">‹</span>' if E == 'pista' else ''
    right = '<span class="circ">≡</span>' if E == 'pista' else '<span class="circ">⚙︎</span>' if E == 'notas' else '<span class="ln mono">L1–42</span>'
    css = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:transparent;font-family:{FF},system-ui,sans-serif;color:#fff;-webkit-font-smoothing:antialiased}}
.mono{{font-family:'JetBrains Mono',monospace}}
.tb{{position:absolute;left:40px;right:40px;top:150px;padding:18px 20px;animation:cIn .6s cubic-bezier(.22,1.2,.36,1) .05s both}}
@keyframes cIn{{from{{opacity:0;transform:translateY(-50px)}}to{{opacity:1;transform:none}}}}
.r1{{display:flex;align-items:center;gap:16px}}
.tab{{display:inline-flex;align-items:center;gap:14px;height:72px;padding:0 26px;font-family:'JetBrains Mono',monospace;font-size:30px;font-weight:700}}
.dt{{width:16px;height:16px;border-radius:50%;animation:dsv .3s ease {FIN - 1.6:.2f}s forwards}}
@keyframes dsv{{to{{background:#3ee08a;box-shadow:0 0 12px #3ee08a}}}}
.nm{{font-family:'JetBrains Mono',monospace;font-size:28px;font-weight:700;opacity:.9}}
.ln{{margin-left:auto;font-size:24px;opacity:.6}}
.crumb{{position:relative;height:44px;margin-top:14px;padding-left:8px;font-family:'JetBrains Mono',monospace;font-size:27px;font-weight:500;overflow:hidden}}
.cr{{position:absolute;top:0;white-space:nowrap;opacity:0;color:rgba(255,255,255,.85)}}
@keyframes cIn2{{from{{opacity:0;transform:translateY(30px)}}to{{opacity:1;transform:none}}}}
@keyframes cOut2{{to{{opacity:0;transform:translateY(-30px)}}}}
{skin}"""
    body = (f'<div class="tb"><div class="r1">{left}<span class="tab"><i class="dt"></i>README.md</span><span class="nm">#01 · SDD</span>{right}</div>'
            f'<div class="crumb">{crumbs}</div></div>')
    return f"""<!doctype html><html><head><meta charset="utf-8">{G.FONTS}{FLINK}<style>{css}</style>
<script>window.__listo=Promise.resolve();</script></head><body>{body}</body></html>"""


PIEZAS.append(('pestana', 0.0, FIN, pestana()))
PRE = f'rm1-{E}-{V}-'

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
        rel = os.environ.get('REL', f'readme/1/{E}-{V}')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
