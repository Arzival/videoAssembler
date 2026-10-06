"""Escenas explicativas a pantalla completa (tapan el video unos segundos; la voz sigue).

Mismo lenguaje visual que las tarjetas: fondo oscuro, Inter, acentos de color por herramienta.
Los tiempos internos están sincronizados con la transcripción del video 5.
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
# carpeta de salida de los .webm (y de los .html intermedios): SALIDA=… o la actual
OUT = os.path.abspath(os.environ.get('SALIDA', os.getcwd()))
WORK = os.path.join(OUT, '_html')
os.makedirs(WORK, exist_ok=True)

BASE = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:transparent;font-family:Inter,-apple-system,system-ui,sans-serif;color:#fff;-webkit-font-smoothing:antialiased}
.scene{position:absolute;inset:0;overflow:hidden;
  background:radial-gradient(1200px 900px at 50% 30%,#1b2140 0%,#0d1020 55%,#07080f 100%);
  animation:sIn .45s ease both,sOut .45s ease var(--out) forwards}
.scene:before{content:'';position:absolute;inset:0;opacity:.35;
  background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);
  background-size:60px 60px;mask-image:radial-gradient(circle at 50% 40%,#000 30%,transparent 75%)}
@keyframes sIn{from{opacity:0;transform:scale(1.04)}to{opacity:1;transform:none}}
@keyframes sOut{to{opacity:0;transform:scale(.98)}}
.lbl{position:absolute;left:0;right:0;text-align:center;font-size:26px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:rgba(255,255,255,.45)}
.h{position:absolute;left:60px;right:60px;text-align:center;font-size:62px;font-weight:800;letter-spacing:-.03em;line-height:1.08}
.pop{animation:pop .55s cubic-bezier(.22,1.35,.36,1) both}
@keyframes pop{from{opacity:0;transform:translateY(30px) scale(.9)}to{opacity:1;transform:none}}
.fade{animation:fade .5s ease both}@keyframes fade{from{opacity:0}to{opacity:1}}
.glow-o{box-shadow:0 0 0 2px rgba(217,119,87,.6),0 0 60px rgba(217,119,87,.45)}
.green{color:#30d158}.red{color:#ff453a}.orange{color:#ff9f0a}
"""

def page(css, body, dur, script=''):
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=block" rel="stylesheet">
<style>{BASE}{css}</style></head><body><div class="scene" style="--out:{dur - 0.45}s">{body}</div>
<script>{script}</script></body></html>"""

def d(s):
    return f'style="animation-delay:{s}s"'

CLAUDE_SVG = '<svg viewBox="0 0 24 24"><path fill="#fff" d="M12 2l1.6 6.1L19.8 6l-4.3 4.7L22 12l-6.5 1.3 4.3 4.7-6.2-2.1L12 22l-1.6-6.1L4.2 18l4.3-4.7L2 12l6.5-1.3L4.2 6l6.2 2.1z"/></svg>'

ESCENAS = {}

# ───────────────────────── 1 · cómo se sacan las métricas (18.1 → 32.0)
ESCENAS['s1-metricas'] = (13.9, """
.clock{position:absolute;left:50%;top:250px;width:150px;height:150px;margin-left:-75px;border-radius:50%;
  border:6px solid rgba(255,255,255,.85);animation:pop .55s cubic-bezier(.22,1.35,.36,1) .1s both}
.clock:before,.clock:after{content:'';position:absolute;left:50%;bottom:50%;width:6px;margin-left:-3px;border-radius:3px;background:#fff;transform-origin:bottom}
.clock:before{height:44px;animation:spin 1.6s linear .2s 2}
.clock:after{height:30px;background:#0a84ff;animation:spin 9.6s linear .2s}
@keyframes spin{to{transform:rotate(360deg)}}
.prof{position:absolute;top:500px;width:220px;height:220px;border-radius:44px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;font-size:26px;font-weight:700}
.prof span{font-size:74px;line-height:1}
.flash{position:absolute;left:40px;right:40px;top:480px;height:260px;border-radius:50px;background:#fff;opacity:0;animation:flash .5s ease-out 3.7s both}
@keyframes flash{0%{opacity:0}15%{opacity:.95}100%{opacity:0}}
.shot{position:absolute;top:530px;width:120px;height:170px;border-radius:16px;background:linear-gradient(170deg,#2b3150,#151a2e);
  box-shadow:inset 0 0 0 2px rgba(255,255,255,.35),0 18px 40px rgba(0,0,0,.5);opacity:0}
.shot:before{content:'';position:absolute;left:16px;right:16px;top:18px;height:12px;border-radius:6px;background:rgba(255,255,255,.4);
  box-shadow:0 26px 0 rgba(255,255,255,.22),0 52px 0 rgba(255,255,255,.22),0 78px 0 -12px rgba(255,255,255,.18)}
.s1{left:180px;animation:fly1 1.4s cubic-bezier(.5,0,.2,1) 4.1s both}
.s2{left:480px;animation:fly2 1.4s cubic-bezier(.5,0,.2,1) 4.3s both}
.s3{left:780px;animation:fly3 1.4s cubic-bezier(.5,0,.2,1) 4.5s both}
@keyframes fly1{0%{opacity:0;transform:scale(1.4)}20%{opacity:1}100%{opacity:1;transform:translate(260px,330px) rotate(-8deg)}}
@keyframes fly2{0%{opacity:0;transform:scale(1.4)}20%{opacity:1}100%{opacity:1;transform:translate(0,320px)}}
@keyframes fly3{0%{opacity:0;transform:scale(1.4)}20%{opacity:1}100%{opacity:1;transform:translate(-260px,330px) rotate(8deg)}}
.cap{position:absolute;top:1020px;left:0;right:0;text-align:center;font-size:30px;font-weight:600;color:rgba(255,255,255,.7)}
svg.links{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:visible}
.ln{fill:none;stroke:rgba(255,255,255,.25);stroke-width:4;stroke-dasharray:10 12;stroke-dashoffset:0;opacity:0;animation:fade .4s ease 6.4s forwards,flow 1s linear 6.4s infinite}
@keyframes flow{to{stroke-dashoffset:-44}}
.step{position:absolute;left:40px;right:40px;top:96px;text-align:center;font-size:66px;font-weight:900;letter-spacing:-.03em;opacity:0}
.step em{font-style:normal;background:linear-gradient(90deg,#5ac8fa,#bf5af2);-webkit-background-clip:text;color:transparent}
@keyframes stIn{from{opacity:0;transform:translateY(24px);filter:blur(6px)}to{opacity:1;transform:none;filter:none}}
@keyframes stOut{to{opacity:0;transform:translateY(-24px);filter:blur(6px)}}
.pk{position:absolute;width:22px;height:22px;border-radius:50%;background:#fff;box-shadow:0 0 18px #fff;offset-rotate:0deg;opacity:0}
.pk1{offset-path:path('M540 1080 C 540 1180, 300 1160, 300 1290');animation:pk 1.1s ease-in-out 6.7s 3 both}
.pk2{offset-path:path('M540 1080 C 540 1180, 780 1160, 780 1290');animation:pk 1.1s ease-in-out 7.0s 3 both}
@keyframes pk{0%{offset-distance:0%;opacity:0}15%{opacity:1}85%{opacity:1}100%{offset-distance:100%;opacity:0}}
.ai{position:absolute;top:1280px;width:230px;height:230px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;font-size:30px;font-weight:800}
.ai svg{width:80px;height:80px}
.claude{left:185px;background:radial-gradient(circle at 35% 30%,#f0936f,#c65f3f);animation:pop .55s cubic-bezier(.22,1.35,.36,1) 6.6s both,beat 1.1s ease-in-out 7.4s infinite}
.codex{left:665px;background:radial-gradient(circle at 35% 30%,#3a3f4b,#16181d);box-shadow:inset 0 0 0 3px rgba(255,255,255,.25);animation:pop .55s cubic-bezier(.22,1.35,.36,1) 6.85s both,beat 1.1s ease-in-out 7.65s infinite}
@keyframes beat{50%{transform:scale(1.05)}}
.dash{position:absolute;left:90px;right:90px;top:1580px;border-radius:36px;padding:34px 36px;background:rgba(255,255,255,.07);
  box-shadow:inset 0 0 0 2px rgba(255,255,255,.12),0 30px 80px rgba(0,0,0,.5);animation:pop .6s cubic-bezier(.22,1.35,.36,1) 10.6s both}
.dash .t{font-size:24px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.5);margin-bottom:18px}
.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.kpi b{display:block;font-size:52px;font-weight:900;letter-spacing:-.03em}
.kpi span{font-size:22px;color:rgba(255,255,255,.55)}
""", f"""
<div class="step" style="animation:stIn .45s cubic-bezier(.22,1.2,.36,1) 0.1s both,stOut .3s ease 1.75s forwards">Cada <em>hora</em></div><div class="step" style="animation:stIn .45s cubic-bezier(.22,1.2,.36,1) 1.8s both,stOut .3s ease 3.65s forwards">revisa mis <em>perfiles</em></div><div class="step" style="animation:stIn .45s cubic-bezier(.22,1.2,.36,1) 3.7s both,stOut .3s ease 6.35s forwards">toma <em>capturas</em></div><div class="step" style="animation:stIn .45s cubic-bezier(.22,1.2,.36,1) 6.4s both,stOut .3s ease 10.5s forwards">se las pasa a la <em>IA</em></div><div class="step" style="animation:stIn .45s cubic-bezier(.22,1.2,.36,1) 10.55s both">y me da mis <em>métricas</em></div>
<div class="clock"></div>
<div class="prof pop" style="left:120px;background:linear-gradient(150deg,#25f4ee,#000 55%,#fe2c55);animation-delay:1.8s"><span>♪</span>TikTok</div>
<div class="prof pop" style="left:430px;background:linear-gradient(150deg,#f58529,#dd2a7b,#8134af);animation-delay:2.0s"><span>◎</span>Instagram</div>
<div class="prof pop" style="left:740px;background:linear-gradient(150deg,#ff3b30,#a3150c);animation-delay:2.2s"><span>▶</span>YouTube</div>
<div class="flash"></div>
<div class="shot s1"></div><div class="shot s2"></div><div class="shot s3"></div>
<div class="cap fade" {d(5.2)}>Capturas → prompt</div>
<svg class="links"><path class="ln" d="M540 1080 C 540 1180, 300 1160, 300 1290"/><path class="ln" d="M540 1080 C 540 1180, 780 1160, 780 1290"/></svg>
<i class="pk pk1"></i><i class="pk pk2"></i>
<div class="ai claude">{CLAUDE_SVG}Claude</div>
<div class="ai codex"><span style="font-size:70px;line-height:1">⌘</span>Codex</div>
<div class="dash"><div class="t">Mis métricas</div><div class="kpis">
 <div class="kpi"><b class="green" id="k1">+0</b><span>seguidores</span></div>
 <div class="kpi"><b id="k2">0.0%</b><span>engagement</span></div>
 <div class="kpi"><b id="k3">8 pm</b><span>mejor hora</span></div></div></div>""",
"""window.__seek=t=>{const p=Math.min(1,Math.max(0,(t-11.0)/1.6)),e=1-Math.pow(1-p,3);
document.getElementById('k1').textContent='+'+Math.round(128*e);document.getElementById('k2').textContent=(6.2*e).toFixed(1)+'%'}""")

# ───────────────────────── 2 · el homelab documenta en Qstify (107.9 → 118.8)
docs = ''.join(f'<i class="doc" style="animation-delay:{2.4 + k * 0.55:.2f}s"></i>' for k in range(6))
items = ['Bitácora semanal', 'Métricas · semana 41', 'Encargo: respaldo', 'Recomendaciones', 'Proceso: capturas', 'Estado del servidor']
rows = ''.join(f'<div class="ql" style="animation-delay:{3.4 + k * 0.55:.2f}s"><span class="b"></span>{n}<em>✳ Claude</em></div>' for k, n in enumerate(items))
ESCENAS['s2-qstify'] = (10.9, """
.srv{position:absolute;left:50%;top:230px;width:300px;margin-left:-150px;border-radius:32px;padding:30px;background:rgba(255,255,255,.07);
  box-shadow:inset 0 0 0 2px rgba(48,209,88,.45),0 0 70px rgba(48,209,88,.25);text-align:center;animation:pop .55s cubic-bezier(.22,1.35,.36,1) .15s both}
.srv .r{height:30px;border-radius:9px;background:rgba(255,255,255,.12);margin:10px 0;position:relative}
.srv .r:after{content:'';position:absolute;left:14px;top:9px;width:12px;height:12px;border-radius:50%;background:#30d158;box-shadow:0 0 12px #30d158;animation:led .8s step-end infinite}
.srv .r:nth-child(2):after{animation-delay:.3s}.srv .r:nth-child(3):after{animation-delay:.55s}
@keyframes led{50%{opacity:.25}}
.srv b{display:block;font-size:32px;font-weight:800;margin-top:14px}
.tasks{position:absolute;top:610px;left:0;right:0;display:flex;justify-content:center;gap:16px}
.tk{padding:14px 24px;border-radius:999px;background:rgba(255,255,255,.08);font-size:25px;font-weight:600;box-shadow:inset 0 0 0 2px rgba(255,255,255,.1)}
.doc{position:absolute;left:510px;top:560px;width:60px;height:78px;border-radius:10px;background:#fff;box-shadow:0 10px 30px rgba(0,0,0,.4);opacity:0;
  offset-path:path('M0 0 C 0 260, 0 420, 0 620');offset-rotate:0deg;animation:docfly 1.1s cubic-bezier(.45,0,.2,1) both}
.doc:before{content:'';position:absolute;left:10px;right:10px;top:14px;height:7px;border-radius:4px;background:#c9c9d1;box-shadow:0 14px 0 #dcdce2,0 28px 0 #dcdce2}
@keyframes docfly{0%{offset-distance:0%;opacity:0;transform:scale(.6)}15%{opacity:1;transform:scale(1)}85%{opacity:1}100%{offset-distance:100%;opacity:0;transform:scale(.4)}}
.app{position:absolute;left:80px;right:80px;top:1180px;height:600px;border-radius:36px;background:#141625;overflow:hidden;
  box-shadow:inset 0 0 0 2px rgba(255,255,255,.1),0 40px 90px rgba(0,0,0,.6);animation:pop .6s cubic-bezier(.22,1.35,.36,1) 1.2s both}
.bar{display:flex;align-items:center;gap:16px;padding:24px 28px;border-bottom:2px solid rgba(255,255,255,.07)}
.q{width:56px;height:56px;border-radius:16px;background:linear-gradient(135deg,#7c3aed,#06b6d4);display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:900;animation:qg 1.2s ease 6.4s 2}
@keyframes qg{50%{box-shadow:0 0 0 10px rgba(124,58,237,.25),0 0 60px rgba(6,182,212,.6)}}
.bar b{font-size:32px;font-weight:800}.bar span{margin-left:auto;font-size:22px;color:rgba(255,255,255,.45)}
.ql{display:flex;align-items:center;gap:16px;padding:20px 30px;font-size:26px;border-bottom:1.5px solid rgba(255,255,255,.05);animation:row .45s cubic-bezier(.22,1.35,.36,1) both}
@keyframes row{from{opacity:0;transform:translateX(-40px)}to{opacity:1;transform:none}}
.ql .b{width:14px;height:14px;border-radius:4px;background:#7c3aed}
.ql em{margin-left:auto;font-style:normal;font-size:19px;font-weight:700;color:#ffb38f;background:rgba(217,119,87,.18);padding:6px 12px;border-radius:9px}
""", f"""
<div class="lbl" style="top:110px">Todo queda documentado</div>
<div class="srv"><div class="r"></div><div class="r"></div><div class="r"></div><b>Homelab</b></div>
<div class="tasks"><div class="tk pop" {d(.7)}>⚙️ Procesos</div><div class="tk pop" {d(.9)}>✅ Actividades</div><div class="tk pop" {d(1.1)}>📁 Proyectos</div></div>
{docs}
<div class="app"><div class="bar"><div class="q">Q</div><b>Qstify</b><span>Notas · Homelab</span></div>{rows}</div>""")

# ───────────────────────── 3 · Claude vs Astra (172.0 → 191.0)
ctasks = ['Métricas de redes', 'Encargos programados', 'Notas en Qstify', 'Avisos por Telegram', 'Documentación']
cl = ''.join(f'<div class="tsk" style="animation-delay:{1.6 + k * 0.9:.1f}s"><i>✓</i>{n}</div>' for k, n in enumerate(ctasks))
at = ''.join(f'<div class="tsk later" style="animation-delay:{16.0 + k * 0.45:.2f}s"><i>✓</i>{n}</div>' for k, n in enumerate(['Análisis de métricas', 'Revisión de código']))
ESCENAS['s3-ias'] = (19.0, """
.cols{position:absolute;top:330px;left:50px;right:50px;display:grid;grid-template-columns:1fr 1fr;gap:30px}
.col{border-radius:36px;padding:34px 28px;background:rgba(255,255,255,.06);box-shadow:inset 0 0 0 2px rgba(255,255,255,.1);min-height:1080px}
.c1{animation:pop .55s cubic-bezier(.22,1.35,.36,1) .3s both}.c2{animation:pop .55s cubic-bezier(.22,1.35,.36,1) .5s both}
.av{width:150px;height:150px;border-radius:50%;margin:0 auto 22px;display:flex;align-items:center;justify-content:center}
.av svg{width:80px;height:80px}
.nm{text-align:center;font-size:44px;font-weight:900}
.price{text-align:center;font-size:76px;font-weight:900;letter-spacing:-.04em;margin:18px 0 6px;position:relative;height:90px}
.price small{font-size:28px;font-weight:600;color:rgba(255,255,255,.5)}
.per{text-align:center;font-size:24px;color:rgba(255,255,255,.5);margin-bottom:28px}
.tsk{display:flex;align-items:center;gap:14px;padding:16px 18px;margin-bottom:12px;border-radius:18px;background:rgba(48,209,88,.12);font-size:25px;font-weight:600;
  animation:pop .45s cubic-bezier(.22,1.35,.36,1) both}
.tsk i{font-style:normal;width:38px;height:38px;border-radius:50%;background:#30d158;color:#06210f;display:flex;align-items:center;justify-content:center;font-weight:900;flex-shrink:0}
.meter{margin-top:40px}
.meter .lb{font-size:22px;color:rgba(255,255,255,.55);margin-bottom:12px}
.track{height:26px;border-radius:13px;background:rgba(255,255,255,.1);overflow:hidden}
.track i{display:block;height:100%;width:100%;transform-origin:left;transform:scaleX(0);border-radius:13px;background:linear-gradient(90deg,#30d158,#ff9f0a 60%,#ff453a);
  animation:fill 2.2s cubic-bezier(.5,0,.3,1) 7.6s forwards, drain .8s ease 15.3s forwards}
@keyframes fill{to{transform:scaleX(1)}}@keyframes drain{to{transform:scaleX(.12)}}
.lim{margin-top:22px;text-align:center;padding:16px;border-radius:18px;background:rgba(255,69,58,.15);color:#ff453a;font-size:28px;font-weight:800;
  animation:pop .45s cubic-bezier(.22,1.35,.36,1) 9.9s both,limOut .3s ease 15.0s forwards}
@keyframes limOut{to{opacity:0;transform:scale(.9)}}
.p20,.p100{position:absolute;left:0;right:0}
.p20{animation:pop .5s cubic-bezier(.22,1.35,.36,1) 7.2s both,swapOut .35s ease 15.2s forwards}
.p100{opacity:0;animation:pop .55s cubic-bezier(.22,1.35,.36,1) 15.45s both}
@keyframes swapOut{to{opacity:0;transform:translateY(-30px)}}
.soon{position:absolute;right:16px;top:-6px;font-size:20px;font-weight:800;color:#0a84ff;background:rgba(10,132,255,.16);padding:6px 12px;border-radius:10px;opacity:0;animation:pop .4s ease 15.8s both}
.later{background:rgba(10,132,255,.14)}.later i{background:#0a84ff;color:#fff}
""", f"""
<div class="h pop" style="top:150px;animation-delay:.1s">¿Quién hace el trabajo?</div>
<div class="cols">
 <div class="col c1"><div class="av glow-o" style="background:radial-gradient(circle at 35% 30%,#f0936f,#c65f3f)">{CLAUDE_SVG}</div>
  <div class="nm">Claude</div>
  <div class="price pop" {d(1.0)}>$100<small>/mes</small></div><div class="per fade" {d(1.2)}>suscripción Max</div>
  {cl}</div>
 <div class="col c2"><div class="av" style="background:radial-gradient(circle at 35% 30%,#3ad38f,#0f7a52);box-shadow:0 0 0 2px rgba(48,209,88,.5),0 0 60px rgba(48,209,88,.35)"><span style="font-size:76px">🤖</span></div>
  <div class="nm">Astra</div>
  <div class="price"><div class="p20">$20<small>/mes</small></div><div class="p100">$100<small>/mes</small></div><span class="soon">PRONTO</span></div>
  <div class="per" style="position:relative;height:30px"><span class="p20" style="animation:pop .5s cubic-bezier(.22,1.35,.36,1) 7.4s both,swapOut .35s ease 15.2s forwards">se acaba enseguida</span><span class="p100">próximamente plan Max</span></div>
  <div class="meter fade" {d(7.5)}><div class="lb">Uso del plan</div><div class="track"><i></i></div></div>
  <div class="lim">Límite alcanzado</div>
  {at}</div>
</div>""")

solo = set(sys.argv[1:])
for sid, (dur, css, body, *script) in ESCENAS.items():
    if solo and sid not in solo:
        continue
    html = f'{WORK}/{sid}.html'
    open(html, 'w').write(page(css, body, dur, script[0] if script else ''))
    if os.environ.get('SOLO_HTML'):
        continue
    r = subprocess.run(['node', f'{HERE}/capturar.ts', html, str(dur), f'{OUT}/{sid}.webm'], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr[-600:], flush=True)
