"""El Log #02 (semana del 6 al 12 oct 2026). Sin clips: TODO el video son escenas encadenadas sobre un fondo base.
Tiempos = segundos del video final = de noticias/2/voz/voz-recortada.wav (sin el error del final, recortada a -35 dB/0.2 s).
Uso: SALIDA=noticias/2/animaciones python3 ejemplos/ellog-02.py [ids…]   (SOLO_HTML=1 para revisar)
Al correrlo sin ids escribe overlays.json listo para el manifiesto.
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import ellog as L

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.getcwd()))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
FIN = 125.08  # duración de la voz recortada

ENTRADAS = [('3e9a1f0', 'Anthropic apaga el internet'), ('b72c4d8', 'Nadella · freno de emergencia'),
            ('5d0e2a7', 'Intel y AMD · vuelve la DDR4'), ('c41f9b3', 'Microsoft · Maia 300')]

MS = ('<svg viewBox="0 0 24 24"{st}><rect x="1" y="1" width="10.5" height="10.5" fill="#f25022"/><rect x="12.5" y="1" width="10.5" height="10.5" fill="#7fba00"/>'
      '<rect x="1" y="12.5" width="10.5" height="10.5" fill="#00a4ef"/><rect x="12.5" y="12.5" width="10.5" height="10.5" fill="#ffb900"/></svg>')
def ms(size=None):
    return MS.format(st=f' style="width:{size}px;height:{size}px"' if size else '')

PIEZAS = []  # (id, inicio, fin, html)


def escena(pid, start, end, css, body, script='', sigue=True):
    """sigue=True: la siguiente escena empieza en `end` encima de esta → sin salida y 0.45 s extra (no asoma el fondo)."""
    if sigue:
        end += 0.45
    PIEZAS.append((pid, start, end, L.page(css, body, end - start, script, salida=not sigue)))


# ───────── 0:00 · gancho: «Una IA de Anthropic le mandó una notificación falsa a la policía… no tires tu RAM DDR4»
S = 0.0; A = L.at(S)
escena('e00-gancho', S, 9.3, f"""
.tag{{position:absolute;left:0;right:0;top:170px;text-align:center;font-size:30px;letter-spacing:.3em;animation:fade .4s ease both}}
.blk{{position:absolute;left:60px;right:60px;padding:50px 46px;text-align:center}}
.b1{{top:330px;animation:pop .5s cubic-bezier(.22,1.3,.36,1) .1s both}}
.b2{{top:1110px;animation:pop .5s cubic-bezier(.22,1.3,.36,1) {A(4.2)} both}}
.row{{display:flex;align-items:center;justify-content:center;gap:34px}}
.lg{{width:150px;height:150px;border-radius:36px;display:flex;align-items:center;justify-content:center}}
.ar{{font-size:80px;color:#ff5c5c;animation:arr .5s ease-in-out .9s 6 alternate both}}@keyframes arr{{to{{transform:translateX(16px)}}}}
.pol{{background:#1a2c5c;font-size:96px;position:relative;overflow:hidden}}
.pol:before{{content:'';position:absolute;inset:0;animation:siren .5s steps(1) 1.0s infinite}}
@keyframes siren{{0%{{background:rgba(255,40,40,.55)}}50%{{background:rgba(40,110,255,.55)}}}}
.sub{{font-size:46px;font-weight:800;margin-top:30px;line-height:1.15}}
.fake{{display:inline-block;margin-top:18px;padding:10px 22px;border-radius:12px;background:rgba(255,92,92,.16);color:#ff5c5c;font-size:30px;font-weight:900;letter-spacing:.12em;
  box-shadow:inset 0 0 0 3px #ff5c5c;transform:rotate(-4deg);animation:stamp .4s cubic-bezier(.22,1.6,.36,1) 2.6s both}}
@keyframes stamp{{from{{opacity:0;transform:rotate(-4deg) scale(2.2)}}to{{opacity:1;transform:rotate(-4deg)}}}}
.ram{{position:relative;width:640px;height:150px;margin:0 auto;border-radius:12px;background:linear-gradient(#1d5c3a,#123d27);box-shadow:inset 0 0 0 3px #3dff9a}}
.ram i{{position:absolute;top:26px;width:62px;height:76px;border-radius:6px;background:#0b0f0d;box-shadow:inset 0 0 0 2px #2a2f2c}}
.ram b{{position:absolute;bottom:-14px;left:20px;right:20px;height:22px;background:repeating-linear-gradient(90deg,#d4a63a 0 10px,transparent 10px 15px)}}
.ram span{{position:absolute;right:20px;top:-46px;font-family:'JetBrains Mono';font-size:30px;font-weight:800;color:#3dff9a}}
.no{{font-size:70px;font-weight:900;letter-spacing:-.03em;margin-top:44px}}.no em{{font-style:normal;color:#3dff9a}}
.bin{{position:absolute;right:60px;top:-30px;font-size:80px;animation:fade .3s ease {A(5.6)} both,binX .3s ease {A(6.0)} forwards}}
@keyframes binX{{to{{opacity:.25;filter:grayscale(1)}}}}
.x{{position:absolute;right:58px;top:-10px;font-size:90px;color:#ff5c5c;font-weight:900;animation:pop .35s cubic-bezier(.22,1.6,.36,1) {A(6.0)} both}}
.hey{{position:absolute;left:0;right:0;top:1660px;text-align:center;font-size:34px;animation:fade .4s ease {A(7.7)} both}}
""", f"""<div class="tag mono g">● ESTA SEMANA</div>
<div class="blk b1 panel"><div class="row"><div class="lg" style="background:#d97757">{L.logo('claude', '#fff', 100)}</div><div class="ar">→</div><div class="lg pol"><span style="position:relative">🚓</span></div></div>
 <div class="sub">Una IA de <span style="color:#ffb38f">Anthropic</span><br>le escribió a la <span style="color:#7fa8ff">policía</span></div><div class="fake mono">FALSO</div></div>
<div class="blk b2 panel"><div class="bin">🗑️</div><div class="x">✕</div><div class="ram"><span>DDR4</span>{''.join(f'<i style="left:{30 + k * 76}px"></i>' for k in range(8))}<b></b></div>
 <div class="no">¡No la <em>tires</em>!</div></div>
<div class="hey mono dim">// ahorita te explico por qué_</div>""")

# ───────── 0:09 · intro de la sección («esto y dos noticias más en este log»)
PIEZAS.append(('e01-intro', 9.3, 12.0 + .45, L.intro('semana del 6 al 12 de octubre', ENTRADAS, 3.15)))

# ───────── 0:12 · #01 Anthropic apagó el internet de sus evaluaciones (parte 1: el tip falso a la policía)
S = 12.0; A = L.at(S)
escena('e02-anthropic', S, 31.6, f"""
.f1{{animation:gone .35s ease {A(21.4)} forwards}}
.lab{{position:absolute;left:110px;right:110px;top:470px;padding:40px}}
.lab .hd{{display:flex;align-items:center;gap:16px;font-size:26px;margin-bottom:28px}}
.net{{display:flex;align-items:center;gap:24px;padding:26px;border-radius:22px;background:rgba(255,255,255,.05);font-size:34px;font-weight:800}}
.net .ic{{font-size:60px;animation:netOff .4s ease {A(13.0)} forwards}}@keyframes netOff{{to{{filter:grayscale(1);opacity:.35}}}}
.sw{{margin-left:auto;width:120px;height:66px;border-radius:33px;background:#3dff9a;position:relative;animation:swOff .35s ease {A(12.9)} forwards}}
.sw:after{{content:'';position:absolute;top:6px;left:60px;width:54px;height:54px;border-radius:50%;background:#fff;animation:knob .35s ease {A(12.9)} forwards}}
@keyframes swOff{{to{{background:#3a3f3c}}}}@keyframes knob{{to{{left:6px}}}}
.st{{font-size:24px;margin-top:20px}}.st b{{color:#ff5c5c;opacity:0;animation:fade .3s ease {A(13.2)} forwards}}
.evs{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:26px}}
.ev{{height:90px;border-radius:16px;background:rgba(61,255,154,.1);box-shadow:inset 0 0 0 2px rgba(61,255,154,.3);display:flex;align-items:center;justify-content:center;font-size:20px;
  animation:pop .35s ease both,evOff .3s ease forwards}}
@keyframes evOff{{to{{background:rgba(255,92,92,.1);box-shadow:inset 0 0 0 2px rgba(255,92,92,.35);color:#ff5c5c}}}}
.aviso{{position:absolute;left:0;right:0;top:1150px;text-align:center}}
.rep{{position:absolute;left:150px;right:150px;top:1300px;padding:32px 36px;border-radius:24px;background:#f4f1ea;color:#1c1c1e;box-shadow:0 30px 70px rgba(0,0,0,.55);
  animation:pop .5s cubic-bezier(.22,1.3,.36,1) {A(17.9)} both}}
.rep h4{{font-size:30px;font-weight:800}}.rep .l{{height:12px;border-radius:6px;background:#d7d3c9;margin-top:14px}}
.rep .w{{display:inline-block;margin-top:16px;padding:8px 14px;border-radius:10px;background:#ffe1dd;color:#c4271b;font-size:22px;font-weight:800}}
.f2{{opacity:0;animation:fade .35s ease {A(21.6)} forwards,gone .35s ease {A(27.7)} forwards}}
.form{{position:absolute;left:90px;right:90px;top:470px;overflow:hidden;border-radius:28px;background:#fff;color:#111;box-shadow:0 30px 80px rgba(0,0,0,.55)}}
.form .bar{{padding:18px 26px;background:#1a2c5c;color:#fff;font-size:24px;font-weight:700;display:flex;gap:14px;align-items:center}}
.form .bd{{padding:30px 32px}}
.form .lb{{font-size:20px;color:#666;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin:16px 0 8px}}
.form .in{{padding:16px 18px;border-radius:12px;background:#f1f2f5;font-size:25px;min-height:60px}}
.form .ta{{min-height:150px;line-height:1.4}}
.send{{margin-top:22px;display:inline-block;padding:16px 34px;border-radius:14px;background:#1a2c5c;color:#fff;font-size:25px;font-weight:800;animation:press .25s ease {A(24.1)} 2 alternate}}
@keyframes press{{to{{transform:scale(.92)}}}}
.who{{position:absolute;left:0;right:0;top:1270px;display:flex;justify-content:center;gap:18px;flex-wrap:wrap;padding:0 60px}}
.ok{{position:absolute;right:120px;top:440px;z-index:3;padding:12px 20px;border-radius:14px;background:#ff5c5c;color:#fff;font-size:26px;font-weight:900;transform:rotate(5deg);animation:pop .4s cubic-bezier(.22,1.5,.36,1) {A(24.4)} both}}
.f3{{opacity:0;animation:fade .35s ease {A(27.9)} forwards}}
.tl{{position:absolute;left:90px;right:90px;top:620px;padding:46px 40px}}
.tl .track{{position:relative;height:14px;border-radius:7px;background:rgba(255,255,255,.1);margin:70px 20px 40px}}
.tl .fill{{position:absolute;left:0;top:0;bottom:0;border-radius:7px;background:linear-gradient(90deg,#ff5c5c,#ffb340);transform-origin:left;animation:grow2 1.6s ease {A(28.6)} both}}
@keyframes grow2{{from{{transform:scaleX(0)}}}}
.pt{{position:absolute;top:-58px;transform:translateX(-50%);text-align:center;font-size:24px;font-weight:700;white-space:nowrap}}
.pt:after{{content:'';display:block;width:26px;height:26px;border-radius:50%;margin:12px auto 0;background:var(--c);box-shadow:0 0 16px var(--c)}}
.days{{text-align:center;font-size:120px;font-weight:900;letter-spacing:-.04em;line-height:1;margin-top:30px}}.days small{{display:block;font-size:30px;font-weight:700;color:rgba(255,255,255,.6);letter-spacing:0;margin-top:10px}}
.ppd{{position:absolute;left:0;right:0;top:1250px;text-align:center;font-size:30px;opacity:0;animation:pop .45s ease {A(30.2)} forwards}}
""", f"""{L.entry(1, '3e9a1f0', L.logo('anthropic'), 'Anthropic')}
<div class="f1">
 {L.steps([('Apagó el <em>internet</em>', 12.4, 17.4), ('Acciones <em class="red">no intencionadas</em>', 17.5, None)], S, top=290, size=84)}
 <div class="lab panel pop" style="animation-delay:{A(12.1)}"><div class="hd mono dim">🧪 evaluaciones internas de agentes</div>
  <div class="net"><span class="ic">🌐</span>Internet en vivo<div class="sw"></div></div>
  <div class="st mono dim">estado: <b>APAGADO · hasta nuevo aviso</b></div>
  <div class="evs">{''.join(f'<div class="ev mono" style="animation-delay:{A(14.2 + k * .12)},{A(14.8 + k * .12)}">eval-{k + 1:02d}</div>' for k in range(8))}</div></div>
 <div class="rep"><h4>📄 Informe de incidentes</h4><div class="l" style="width:85%"></div><div class="l" style="width:62%"></div>
  <span class="w">⚠ acciones no intencionadas de sus modelos</span></div>
</div>
<div class="f2">
 {L.steps([('Un <em class="red">tip falso</em> a la policía', 21.8, None)], S, top=290, size=80)}
 <div class="ok">ENVIADO</div>
 <div class="form"><div class="bar">🚓 Philadelphia Police · casos sin resolver</div><div class="bd">
  <div class="lb">Caso</div><div class="in mono">Homicidio sin resolver</div>
  <div class="lb">Información</div><div class="in ta"><span class="type" style="--n:28;--td:1.6s;animation-delay:{A(22.4)}">Tengo datos sobre el caso…</span></div>
  <div class="send">Enviar tip</div></div></div>
 <div class="who"><span class="chip pop" style="animation-delay:{A(23.0)}">{L.logo('claude', '#ffb38f', 30)} Claude Haiku 4.5</span>
  <span class="chip pop" style="animation-delay:{A(25.5)}">📍 Filadelfia</span><span class="chip pop" style="animation-delay:{A(26.5)}">📅 18 de julio</span></div>
</div>
<div class="f3">
 {L.steps([('Lo detectaron <em>2 meses</em> después', 28.0, None)], S, top=290, size=76)}
 <div class="tl panel"><div class="track"><div class="fill"></div>
  <div class="pt" style="left:0;--c:#ff5c5c">18 jul<br><span class="dim mono" style="font-size:19px">tip enviado</span></div>
  <div class="pt" style="left:100%;--c:#ffb340;opacity:0;animation:fade .3s ease {A(30.1)} forwards">28 sep<br><span class="dim mono" style="font-size:19px">lo descubren</span></div></div>
  <div class="days mono"><span id="dd">0</span><small>días sin que nadie lo notara</small></div></div>
 <div class="ppd dim">🚓 la policía lo llamó <b style="color:#fff">«inaceptable»</b></div>
</div>""",
f"""window.__seek=t=>{{t+={S};const p=Math.min(1,Math.max(0,(t-28.6)/1.6));document.getElementById('dd').textContent=Math.round(72*(1-Math.pow(1-p,3)))}}""")

# ───────── 0:31 · #01 (parte 2): 20 visas al Departamento de Estado + qué hacer si usas agentes
S = 31.6; A = L.at(S)
visas = ''.join(f'<div class="vz" style="animation-delay:{A(35.9 + k * .09)}"><b>DS-160</b><i></i><i style="width:60%"></i><span>INCOMPLETA</span></div>' for k in range(20))
escena('e03-visas', S, 49.75, f"""
.f1{{animation:gone .35s ease {A(40.4)} forwards}}
.src{{position:absolute;left:0;right:0;top:300px;display:flex;justify-content:center;gap:18px;align-items:center}}
.src .chip svg{{width:34px;height:34px}}
.grid{{position:absolute;left:90px;right:90px;top:640px;display:grid;grid-template-columns:repeat(5,1fr);gap:16px}}
.vz{{height:200px;border-radius:14px;background:#f4f1ea;color:#1c1c1e;padding:14px;position:relative;animation:drop .35s cubic-bezier(.22,1.3,.36,1) both;box-shadow:0 12px 30px rgba(0,0,0,.45)}}
@keyframes drop{{from{{opacity:0;transform:translateY(-60px) rotate(-6deg)}}to{{opacity:1;transform:none}}}}
.vz b{{font-size:20px;font-weight:900;color:#1a2c5c}}.vz i{{display:block;height:9px;border-radius:5px;background:#d7d3c9;margin-top:12px}}
.vz span{{position:absolute;left:8px;right:8px;bottom:16px;text-align:center;font-size:13px;font-weight:900;color:#c4271b;border:2px solid #c4271b;border-radius:6px;padding:3px 0;transform:rotate(-8deg);
  opacity:0;animation:fade .2s ease {A(39.2)} forwards}}
.cnt{{position:absolute;left:0;right:0;top:420px;text-align:center;font-size:150px;font-weight:900;letter-spacing:-.05em;line-height:1}}
.cnt small{{font-size:40px;letter-spacing:0;font-weight:700;color:rgba(255,255,255,.7)}}
.dep{{position:absolute;left:0;right:0;top:1560px;text-align:center}}
.f2{{opacity:0;animation:fade .35s ease {A(40.6)} forwards}}
.chk{{position:absolute;left:100px;right:100px;top:560px;display:grid;gap:22px}}
.it{{display:flex;align-items:center;gap:26px;padding:34px 36px;font-size:44px;font-weight:800;animation:pop .5s cubic-bezier(.22,1.35,.36,1) both}}
.it .e{{font-size:64px;width:80px;text-align:center}}
.it .ck{{margin-left:auto;width:60px;height:60px;border-radius:50%;background:rgba(255,255,255,.08);color:transparent;display:flex;align-items:center;justify-content:center;font-size:34px;font-weight:900;
  animation:ckOn .35s cubic-bezier(.22,1.6,.36,1) both}}
@keyframes ckOn{{from{{background:rgba(255,255,255,.08);color:transparent;transform:scale(.6)}}to{{background:#3dff9a;color:#04210f;transform:none}}}}
.nope{{position:absolute;left:0;right:0;top:1330px;text-align:center;font-size:40px;font-weight:800;animation:pop .45s cubic-bezier(.22,1.5,.36,1) {A(46.3)} both}}
.nope span{{display:inline-block;padding:16px 30px;border-radius:18px;background:rgba(255,92,92,.14);box-shadow:inset 0 0 0 2px rgba(255,92,92,.6)}}
""", f"""{L.entry(1, '3e9a1f0', L.logo('anthropic'), 'Anthropic')}
<div class="f1">
 <div class="src"><span class="chip pop" style="animation-delay:{A(32.0)}">{L.logo('newyorktimes', '#fff')} The New York Times</span><span class="chip pop" style="animation-delay:{A(33.4)}">✍️ vía Simon Willison</span></div>
 <div class="cnt mono"><span id="vn">0</span> <small>solicitudes de visa</small></div>
 <div class="grid">{visas}</div>
 <div class="dep"><span class="chip pop" style="animation-delay:{A(38.9)}">🇺🇸 Departamento de Estado</span><span class="chip pop" style="animation-delay:{A(39.4)};margin-left:14px">ninguna se procesó</span></div>
</div>
<div class="f2">
 {L.steps([('¿Usas <em>agentes</em>?', 40.7, None)], S, top=300, size=96)}
 <div class="chk">
  <div class="it panel" style="animation-delay:{A(43.3)}"><span class="e">🧱</span>Aislamiento<span class="ck" style="animation-delay:{A(44.5)}">✓</span></div>
  <div class="it panel" style="animation-delay:{A(45.3)}"><span class="e">🔑</span>Permisos<span class="ck" style="animation-delay:{A(45.8)}">✓</span></div>
  <div class="it panel" style="animation-delay:{A(48.0)}"><span class="e">👀</span>Supervisa tus modelos<span class="ck" style="animation-delay:{A(49.0)}">✓</span></div></div>
 <div class="nope">y <span>no seas como {L.logo('anthropic', '#fff', 34)} Anthropic</span> 😅</div>
</div>""",
f"""window.__seek=t=>{{t+={S};document.getElementById('vn').textContent=Math.max(0,Math.min(20,Math.floor((t-35.9)/.09)+1))}}""")

# ───────── 0:50 · #02 Satya Nadella: «asume que todos los modelos están comprometidos» + freno de emergencia
S = 49.75; A = L.at(S)
escena('e04-nadella', S, 72.8, f"""
.f1{{animation:gone .35s ease {A(56.8)} forwards}}
.tw{{position:absolute;left:80px;right:80px;top:470px;padding:44px;border-radius:30px;background:#000;box-shadow:inset 0 0 0 2px #2f3336,0 30px 80px rgba(0,0,0,.6);
  animation:pop .55s cubic-bezier(.22,1.3,.36,1) {A(50.0)} both}}
.tw .hd{{display:flex;align-items:center;gap:20px}}
.tw .av{{width:96px;height:96px;border-radius:50%;background:linear-gradient(135deg,#3a4a5c,#1b232d);display:flex;align-items:center;justify-content:center;font-size:40px;font-weight:800}}
.tw .nm{{font-size:34px;font-weight:800}}.tw .nm small{{display:block;font-size:26px;font-weight:400;color:#71767b}}
.tw .x{{margin-left:auto}}.tw .x svg{{width:50px;height:50px}}
.tw .tx{{font-size:46px;line-height:1.25;margin-top:34px;font-weight:600}}
.tw .tx .w{{opacity:0;animation:fade .2s ease forwards}}
.tw .ft{{margin-top:30px;font-size:24px;color:#71767b}}
.ceo{{position:absolute;left:0;right:0;top:1130px;display:flex;justify-content:center;gap:18px}}
.f2{{opacity:0;animation:fade .35s ease {A(57.0)} forwards,gone .35s ease {A(65.2)} forwards}}
.bxs{{position:absolute;left:0;right:0;top:520px;height:620px}}
.bx{{position:absolute;left:50%;top:50%;border-radius:30px;background:#050505;box-shadow:inset 0 0 0 3px rgba(255,255,255,.18),0 20px 60px rgba(0,0,0,.6);transform:translate(-50%,-50%);
  animation:bxIn .5s cubic-bezier(.22,1.3,.36,1) both}}
@keyframes bxIn{{from{{opacity:0;transform:translate(-50%,-50%) scale(.6)}}}}
.bx.q{{display:flex;align-items:center;justify-content:center;font-size:110px;font-weight:900;color:rgba(255,255,255,.75)}}
.flow{{position:absolute;left:0;right:0;top:1180px;display:flex;justify-content:center;align-items:center;gap:20px;font-size:32px;font-weight:700}}
.flow .chip{{font-size:30px}}
.acc{{position:absolute;left:50%;top:1330px;transform:translateX(-50%) rotate(-4deg);white-space:nowrap;padding:16px 30px;border-radius:16px;font-size:40px;font-weight:900;letter-spacing:.06em;
  color:#ff5c5c;box-shadow:inset 0 0 0 4px #ff5c5c;background:rgba(255,92,92,.1);animation:stamp .4s cubic-bezier(.22,1.6,.36,1) {A(62.8)} both}}
@keyframes stamp{{from{{opacity:0;transform:translateX(-50%) rotate(-4deg) scale(2)}}to{{opacity:1;transform:translateX(-50%) rotate(-4deg)}}}}
.f3{{opacity:0;animation:fade .35s ease {A(65.4)} forwards}}
.arq{{position:absolute;left:90px;right:90px;top:470px;display:grid;grid-template-columns:1fr 1fr;gap:20px}}
.ly{{padding:30px;text-align:center;animation:pop .45s cubic-bezier(.22,1.35,.36,1) both}}
.ly .e{{font-size:64px}}.ly b{{display:block;font-size:32px;margin-top:10px}}.ly span{{font-size:22px}}
.wall{{grid-column:1/3;height:8px;border-radius:4px;background:repeating-linear-gradient(90deg,#3dff9a 0 18px,transparent 18px 30px);order:0;display:none}}
.log{{grid-column:1/3;padding:24px 28px;font-size:23px;line-height:1.6;animation:pop .45s ease {A(68.0)} both}}
.brake{{position:absolute;left:50%;top:1110px;width:330px;height:330px;margin-left:-165px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#ff7b7b,#c41414 65%,#7a0a0a);
  box-shadow:0 0 0 18px #2a2a2a,0 0 0 24px #ffcc00,0 30px 80px rgba(0,0,0,.6);display:flex;align-items:center;justify-content:center;text-align:center;font-size:40px;font-weight:900;line-height:1.05;
  animation:pop .5s cubic-bezier(.22,1.4,.36,1) {A(70.0)} both,hit .3s ease {A(70.9)} 1,glowB .8s ease-in-out {A(71.2)} infinite}}
@keyframes hit{{50%{{transform:scale(.86)}}}}@keyframes glowB{{50%{{box-shadow:0 0 0 18px #2a2a2a,0 0 0 24px #ffcc00,0 0 120px rgba(255,40,40,.9)}}}}
.paused{{position:absolute;left:0;right:0;top:1520px;text-align:center;font-size:34px;font-weight:800;opacity:0;animation:fade .3s ease {A(71.2)} forwards}}
""", f"""{L.entry(2, 'b72c4d8', ms(), 'Microsoft')}
<div class="f1">
 {L.steps([('Satya <em>Nadella</em>', 50.0, None)], S, top=290, size=90)}
 <div class="tw"><div class="hd"><div class="av">SN</div><div class="nm">Satya Nadella<small>@satyanadella</small></div><div class="x">{L.logo('x', '#fff')}</div></div>
  <div class="tx">{''.join(f'<span class="w" style="animation-delay:{A(53.2 + k * .2)}">{w} </span>' for k, w in enumerate('Asume que todos los modelos de IA están comprometidos.'.split()))}</div>
  <div class="ft mono">10 oct 2026 · X</div></div>
 <div class="ceo"><span class="chip pop" style="animation-delay:{A(51.0)}">{ms(30)} CEO de Microsoft</span></div>
</div>
<div class="f2">
 {L.steps([('Ya no son <em>cajas negras</em>', 57.4, None)], S, top=290, size=84)}
 <div class="bxs"><div class="bx" style="width:560px;height:560px;animation-delay:{A(59.0)}"></div><div class="bx" style="width:400px;height:400px;animation-delay:{A(59.3)}"></div>
  <div class="bx q" style="width:240px;height:240px;animation-delay:{A(59.6)}">?</div></div>
 <div class="flow"><span class="chip pop" style="animation-delay:{A(60.8)}">💬 consejos</span><span class="chip pop" style="animation-delay:{A(61.4)}">⚡ acciones</span></div>
 <div class="acc">ACEPTADO SIN REVISAR ✕</div>
</div>
<div class="f3">
 {L.steps([('Arquitectura de <em>confianza</em>', 65.6, 69.9), ('Freno de <em class="red">emergencia</em>', 70.0, None)], S, top=290, size=80)}
 <div class="arq"><div class="ly panel" style="animation-delay:{A(66.4)}"><div class="e">🧠</div><b>Modelo</b><span class="dim">contenido desde el inicio</span></div>
  <div class="ly panel" style="animation-delay:{A(66.8)}"><div class="e">⚙️</div><b>Orquestación</b><span class="dim">separada del modelo</span></div>
  <div class="log panel mono"><span class="g">$</span> tail -f acciones.log<br><span class="dim">12:04:11</span> abrir_navegador ✓<br><span class="dim">12:04:13</span> enviar_formulario <span class="red">⏸ requiere humano</span></div></div>
 <div class="brake">FRENO<br>⏻</div>
 <div class="paused mono"><span class="red">●</span> modelo en pausa a mitad de la tarea</div>
</div>""")

# ───────── 1:13 · #03 Intel y AMD vuelven a la DDR4
S = 72.8; A = L.at(S)
escena('e05-ddr4', S, 93.95, f"""
.f1{{animation:gone .35s ease {A(87.2)} forwards}}
.price{{position:absolute;left:90px;right:90px;top:470px;padding:40px}}
.price .hd{{font-size:24px;margin-bottom:26px}}
.pr{{display:grid;grid-template-columns:150px 1fr 150px;align-items:center;gap:20px;margin:20px 0;font-size:32px;font-weight:800}}
.pr .trk{{height:54px;border-radius:14px;background:rgba(255,255,255,.06);overflow:hidden}}
.pr .trk i{{display:block;height:100%;border-radius:14px;transform-origin:left;animation:grow2 1s cubic-bezier(.22,1.1,.36,1) both}}
@keyframes grow2{{from{{transform:scaleX(0)}}}}
.pr b{{text-align:right;font-variant-numeric:tabular-nums}}
.hot{{display:inline-block;margin-left:10px;font-size:40px;animation:fade .3s ease {A(75.6)} both}}
.cpus{{position:absolute;left:0;right:0;top:960px;display:flex;justify-content:center;gap:40px}}
.cpu{{width:300px;height:300px;border-radius:30px;background:linear-gradient(145deg,#2a2e2c,#151816);box-shadow:inset 0 0 0 3px rgba(255,255,255,.14),0 30px 70px rgba(0,0,0,.6);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;position:relative;animation:pop .5s cubic-bezier(.22,1.35,.36,1) both}}
.cpu:before{{content:'';position:absolute;inset:-14px;border-radius:38px;background:repeating-linear-gradient(90deg,#c9a23c 0 6px,transparent 6px 16px);z-index:-1;opacity:.6;
  mask:linear-gradient(#000 0 14px,transparent 14px calc(100% - 14px),#000 calc(100% - 14px))}}
.cpu svg{{width:170px;height:170px}}.cpu span{{font-size:22px;font-weight:700;color:rgba(255,255,255,.55)}}
.sup{{position:absolute;left:0;right:0;top:1340px;text-align:center}}
.sup .chip{{font-size:34px;box-shadow:inset 0 0 0 3px #3dff9a;color:#3dff9a}}
.ant{{position:absolute;left:0;right:0;top:1460px;display:flex;justify-content:center;gap:18px}}
.f2{{opacity:0;animation:fade .35s ease {A(87.4)} forwards}}
.trash{{position:absolute;left:50%;top:880px;margin-left:-150px;width:300px;text-align:center;font-size:250px;line-height:1}}
.stick{{position:absolute;left:50%;top:560px;width:600px;height:140px;margin-left:-300px;border-radius:12px;background:linear-gradient(#1d5c3a,#123d27);box-shadow:inset 0 0 0 3px #3dff9a,0 20px 50px rgba(0,0,0,.5);
  animation:toss 1.6s cubic-bezier(.45,0,.25,1) {A(88.0)} both}}
@keyframes toss{{0%{{transform:translateY(-200px) rotate(-8deg);opacity:0}}15%{{opacity:1}}50%{{transform:translateY(330px) rotate(10deg) scale(.7)}}75%{{transform:translateY(-30px) rotate(-3deg)}}100%{{transform:none}}}}
.stick i{{position:absolute;top:24px;width:58px;height:72px;border-radius:6px;background:#0b0f0d}}
.stick span{{position:absolute;right:18px;top:-48px;font-family:'JetBrains Mono';font-size:30px;font-weight:800;color:#3dff9a}}
.stick b{{position:absolute;bottom:-14px;left:20px;right:20px;height:22px;background:repeating-linear-gradient(90deg,#d4a63a 0 10px,transparent 10px 15px)}}
.save{{position:absolute;left:0;right:0;top:1330px;text-align:center;animation:pop .5s cubic-bezier(.22,1.5,.36,1) {A(91.6)} both}}
.save b{{display:inline-block;padding:20px 40px;border-radius:24px;background:#3dff9a;color:#04210f;font-size:64px;font-weight:900}}
.save div{{margin-top:18px;font-size:26px}}
""", f"""{L.entry(3, '5d0e2a7', L.logo('intel', '#fff'), 'Intel + AMD')}
<div class="f1">
 {L.steps([('La RAM está <em class="red">carísima</em>', 73.4, 76.7), ('Vuelve la <em>DDR4</em>', 76.8, None)], S, top=290, size=88)}
 <div class="price panel pop" style="animation-delay:{A(74.3)}"><div class="hd mono dim">kit 32 GB · precio aprox.</div>
  <div class="pr"><span>DDR5</span><div class="trk"><i style="width:100%;background:linear-gradient(90deg,#ff5c5c,#ff9f0a);animation-delay:{A(74.6)}"></i></div><b class="red">$480</b></div>
  <div class="pr"><span>DDR4</span><div class="trk"><i style="width:44%;background:linear-gradient(90deg,#1b8f57,#3dff9a);animation-delay:{A(74.9)}"></i></div><b class="g">$210</b></div>
  <div class="mono dim" style="font-size:22px;margin-top:10px">// la demanda de la IA se está comiendo la memoria <span class="hot">🔥</span></div></div>
 <div class="cpus"><div class="cpu" style="animation-delay:{A(77.2)}">{L.logo('intel', '#4fa3ff')}<span>nuevos CPUs</span></div>
  <div class="cpu" style="animation-delay:{A(77.7)}">{L.logo('amd', '#fff')}<span>nuevos CPUs</span></div></div>
 <div class="sup"><span class="chip pop" style="animation-delay:{A(81.4)}">✓ soporte para DDR4</span></div>
 <div class="ant"><span class="chip pop" style="animation-delay:{A(84.2)}">⏮ generación anterior</span><span class="chip pop" style="animation-delay:{A(85.9)}">💸 ~56% más barata por GB</span></div>
</div>
<div class="f2">
 {L.steps([('<em>No</em> tires tu DDR4', 89.6, None)], S, top=290, size=96)}
 <div class="trash">🗑️</div>
 <div class="stick"><span>DDR4</span>{''.join(f'<i style="left:{26 + k * 72}px"></i>' for k in range(8))}<b></b></div>
 <div class="save"><b>+ una lanita</b><div class="mono dim">// al armar o actualizar tu PC (y tu homelab)</div></div>
</div>""")

# ───────── 1:34 · #04 Microsoft Maia 300
S = 93.95; A = L.at(S)
escena('e06-maia', S, 118.6, f"""
.chip3{{position:absolute;left:50%;top:430px;width:460px;height:460px;margin-left:-230px;border-radius:44px;
  background:linear-gradient(145deg,#2b3038,#14171c);box-shadow:inset 0 0 0 3px rgba(0,164,239,.5),0 0 120px rgba(0,164,239,.35),0 40px 90px rgba(0,0,0,.6);
  animation:pop .6s cubic-bezier(.22,1.35,.36,1) {A(94.6)} both,toTop .6s cubic-bezier(.6,0,.2,1) {A(99.6)} forwards}}
@keyframes toTop{{to{{transform:translateY(-50px) scale(.5)}}}}
.chip3:before{{content:'';position:absolute;inset:-18px;border-radius:52px;background:repeating-linear-gradient(90deg,#c9a23c 0 6px,transparent 6px 18px);opacity:.6;
  -webkit-mask:linear-gradient(#000 0 18px,transparent 18px calc(100% - 18px),#000 calc(100% - 18px))}}
.die{{position:absolute;inset:70px;border-radius:24px;background:radial-gradient(circle at 40% 30%,#1f3a52,#0d1620);box-shadow:inset 0 0 0 2px rgba(0,164,239,.45);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px}}
.die b{{font-size:72px;font-weight:900;letter-spacing:-.03em}}.die span{{font-size:24px;color:#7fd3ff;font-family:'JetBrains Mono'}}
.hbm{{position:absolute;top:110px;width:34px;height:240px;border-radius:8px;background:#3a4250;box-shadow:inset 0 0 0 2px rgba(255,255,255,.12)}}
.gen{{position:absolute;left:0;right:0;top:960px;display:flex;justify-content:center;gap:16px;flex-wrap:wrap;padding:0 60px;animation:gone .35s ease {A(99.5)} forwards}}
.p2{{opacity:0;animation:fade .35s ease {A(99.8)} forwards,gone .35s ease {A(104.4)} forwards}}
.svc{{position:absolute;left:90px;right:90px;top:760px;display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}
.sv{{padding:28px 18px;text-align:center;font-size:26px;font-weight:800;animation:pop .45s cubic-bezier(.22,1.35,.36,1) both}}
.sv .e{{font-size:56px;margin-bottom:10px}}.sv svg{{width:60px;height:60px;margin-bottom:10px}}
.inf{{position:absolute;left:0;right:0;top:1120px;text-align:center}}
.p3{{opacity:0;animation:fade .35s ease {A(104.6)} forwards,gone .35s ease {A(112.9)} forwards}}
.big{{position:absolute;left:90px;right:90px;display:grid;grid-template-columns:1fr 1fr;gap:20px;top:740px}}
.kp{{padding:34px 24px;text-align:center;animation:pop .45s cubic-bezier(.22,1.35,.36,1) both}}
.kp b{{display:block;font-size:96px;font-weight:900;letter-spacing:-.04em;line-height:1}}.kp span{{font-size:24px;color:rgba(255,255,255,.65)}}
.dep{{position:absolute;left:90px;right:90px;top:1110px;padding:34px;animation:pop .45s ease {A(109.4)} both}}
.dep .r{{display:flex;justify-content:space-between;align-items:center;font-size:28px;font-weight:800;margin-bottom:16px}}
.dep .r svg{{width:48px;height:48px}}
.dep .trk{{height:40px;border-radius:12px;background:rgba(255,255,255,.07);overflow:hidden}}
.dep .trk i{{display:block;height:100%;width:90%;border-radius:12px;background:linear-gradient(90deg,#76b900,#a6e22e);transform-origin:left;animation:shrink 1.4s ease {A(110.6)} both}}
@keyframes shrink{{to{{transform:scaleX(.45)}}}}
.dep .ms{{display:flex;align-items:center;gap:12px;margin-top:20px;font-size:24px;opacity:0;animation:fade .3s ease {A(111.6)} forwards}}
.p4{{opacity:0;animation:fade .35s ease {A(113.1)} forwards}}
.az{{position:absolute;left:90px;right:90px;top:700px;padding:40px;animation:pop .5s cubic-bezier(.22,1.3,.36,1) {A(113.4)} both}}
.az .hd{{display:flex;align-items:center;gap:18px;font-size:34px;font-weight:800;margin-bottom:26px}}.az .hd svg{{width:56px;height:56px}}
.az .ln{{display:flex;justify-content:space-between;align-items:center;padding:20px 0;border-top:1.5px solid rgba(255,255,255,.08);font-size:30px}}
.az .ln b{{font-size:34px}}
.az .ln s{{color:rgba(255,255,255,.4);margin-right:14px}}
.when{{position:absolute;left:0;right:0;top:1250px;text-align:center}}
""", f"""{L.entry(4, 'c41f9b3', ms(), 'Microsoft')}
{L.steps([('Microsoft <em style="color:#7fd3ff">Maia 300</em>', 94.2, 104.4), ('Más <em>barato</em> y <em>eficiente</em>', 104.5, 112.9), ('¿Usas <em style="color:#7fd3ff">Azure</em>?', 113.0, None)], S, top=290, size=76)}
<div class="chip3">{''.join(f'<div class="hbm" style="{side}:{off}px"></div>' for side in ('left', 'right') for off in (14, 54) if False)}
 <div class="die"><b>MAIA</b><span>300</span></div></div>
<div class="gen"><span class="chip pop" style="animation-delay:{A(97.2)}">3ª generación</span><span class="chip pop" style="animation-delay:{A(97.7)}">TSMC 2 nm</span>
 <span class="chip pop" style="animation-delay:{A(98.2)}">8× HBM4</span><span class="chip pop" style="animation-delay:{A(98.8)}">🧠 para IA</span></div>
<div class="p2"><div class="svc">
 <div class="sv panel" style="animation-delay:{A(102.8)}"><div class="e">✦</div>Copilot</div>
 <div class="sv panel" style="animation-delay:{A(103.1)}">{L.logo('microsoftazure', '#0089d6')}<br>Azure</div>
 <div class="sv panel" style="animation-delay:{A(103.4)}"><div class="e">🧩</div>Servicios</div></div>
 <div class="inf"><span class="chip pop" style="animation-delay:{A(101.6)}">⚡ su chip principal de inferencia</span></div></div>
<div class="p3"><div class="big">
 <div class="kp panel" style="animation-delay:{A(105.4)}"><b class="g" id="k1">1×</b><span>tokens por rack</span></div>
 <div class="kp panel" style="animation-delay:{A(107.4)}"><b class="g" id="k2">+0%</b><span>eficiencia por megawatt</span></div></div>
 <div class="dep panel"><div class="r"><span>Dependencia de <b style="color:#76b900">NVIDIA</b></span>{L.logo('nvidia', '#76b900')}</div><div class="trk"><i></i></div>
  <div class="ms">{ms(30)} <span>más chips propios = <b class="g">menos GPUs de NVIDIA</b></span></div></div></div>
<div class="p4"><div class="az"><div class="hd">{L.logo('microsoftazure', '#0089d6')}Azure · lo que puede cambiar</div>
 <div class="ln pop" style="animation-delay:{A(115.5)}"><span>💵 Lo que pagas</span><b class="g">⬇</b></div>
 <div class="ln pop" style="animation-delay:{A(117.2)}"><span>📦 Lo que tienes disponible</span><b style="color:#7fd3ff">⬆</b></div></div>
 <div class="when"><span class="chip pop" style="animation-delay:{A(114.2)}">📅 en producción desde 2027</span></div></div>""",
f"""window.__seek=t=>{{t+={S};const e=(s,d)=>1-Math.pow(1-Math.min(1,Math.max(0,(t-s)/d)),3);
document.getElementById('k1').textContent=(1+6*e(105.8,1.2)).toFixed(0)+'×';document.getElementById('k2').textContent='+'+Math.round(40*e(107.8,1.2))+'%'}}""")

# ───────── 1:59 · cierre (arriba queda la tarjeta «Sígueme»)
PIEZAS.append(('e07-cierre', 118.6, FIN, L.cierre(ENTRADAS, round(FIN - 118.6, 2))))

SIGUEME = ('seguir', 118.7, FIN)  # copia de noticias/1/animaciones/seguir.webm

if __name__ == '__main__':
    solo = set(sys.argv[1:])
    for pid, a, b, html in PIEZAS:
        if solo and pid not in solo:
            continue
        path = f'{WORK}/{pid}.html'
        open(path, 'w').write(html)
        if os.environ.get('SOLO_HTML'):
            print('html', path); continue
        r = subprocess.run(['node', CAP, path, f'{b - a:.2f}', f'{OUT}/{pid}.webm'], capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr[-600:], flush=True)
    if not solo:
        rel = os.environ.get('REL', 'noticias/2/animaciones')
        ovs = [{'file': f'{rel}/{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        ovs.append({'file': f'{rel}/{SIGUEME[0]}.webm', 'start': SIGUEME[1], 'end': SIGUEME[2], 'trimIn': 0, 'scale': 1, 'position': 'center'})
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
