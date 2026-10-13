"""Animaciones del video 7 (dos apps del homelab en el teléfono: Finanzas y Contraseñas, vía PWA + Tailscale).
Reutiliza el sistema visual de tarjetas.py / escenas.py. Tiempos = segundos del video final.
Uso: SALIDA=videos/7/animaciones python3 ejemplos/video7.py [ids…]   (sin ids escribe overlays.json)
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import tarjetas as T
import escenas as E

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.getcwd()))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
d = T.d

TG_SVG = ('<svg width="34" height="34" viewBox="0 0 24 24"><path fill="#fff" d="M21.5 4.3 2.9 11.5c-1.1.4-1.1 1.1-.2 1.4l4.8 1.5 1.8 5.6c.2.6.4.8.9.8.4 0 .6-.2.9-.5l2.3-2.2 '
          '4.7 3.5c.9.5 1.5.2 1.7-.8l3.1-14.6c.3-1.3-.5-1.9-1.4-1.4zM8.6 14l9.2-5.8c.4-.3.8-.1.5.2l-7.6 6.9-.3 3.2z"/></svg>')
TG_IC = f'<div class="ic" style="background:linear-gradient(160deg,#37aee2,#1e96c8)">{TG_SVG}</div>'
FIN_IC = '<div class="ic" style="background:linear-gradient(135deg,#30d158,#0a7d3b);font-size:32px">💰</div>'
PASS_IC = '<div class="ic" style="background:linear-gradient(135deg,#ff6b6b,#c9184a);font-size:30px">🔐</div>'
AI_IC = '<div class="ic" style="background:linear-gradient(135deg,#bf5af2,#5e5ce6);font-size:32px;font-weight:800">✦</div>'
TS_IC = '<div class="ic" style="background:#242424;box-shadow:inset 0 0 0 2px rgba(255,255,255,.18)"><svg width="34" height="34" viewBox="0 0 24 24" fill="#fff">' + ''.join(
    f'<circle cx="{x}" cy="{y}" r="2.3" opacity="{o}"/>' for x, y, o in
    [(4, 4, .35), (12, 4, .35), (20, 4, .35), (4, 12, 1), (12, 12, 1), (20, 12, 1), (4, 20, .35), (12, 20, 1), (20, 20, .35)]) + '</svg></div>'

ROWS_CSS = """
.row{display:flex;gap:18px;align-items:center;padding:15px 0}
.row+.row{border-top:1.5px solid rgba(255,255,255,.08)}
.mini{width:52px;height:52px;border-radius:13px;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:28px}
.info{flex:1}.info .n{font-size:25px;font-weight:600}
.amt{font-size:27px;font-weight:800;text-align:right}
.bd{display:inline-flex;align-items:center;gap:8px;font-size:18px;font-weight:700;padding:6px 12px;border-radius:9px}
.ok{background:rgba(48,209,88,.16);color:#30d158}
.dot{display:inline-block;width:12px;height:12px;border-radius:50%;background:#30d158;animation:pulse 1.4s ease-in-out infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(48,209,88,.6)}70%{box-shadow:0 0 0 9px rgba(48,209,88,0)}}
"""
CHAT_CSS = """
.chat{display:flex;flex-direction:column;gap:12px}
.me{align-self:flex-end;background:#2b5278;border-radius:22px 22px 6px 22px;padding:14px 20px;font-size:25px;max-width:480px}
.bot{align-self:flex-start;display:flex;gap:12px;align-items:flex-end}
.bot .av{width:46px;height:46px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:24px}
.bot .bb{background:rgba(255,255,255,.1);border-radius:22px 22px 22px 6px;padding:14px 20px;font-size:24px;line-height:1.35;max-width:470px}
.bb .who{font-size:18px;font-weight:700;color:#5ac8fa;margin-bottom:4px}
.dots{display:flex;gap:9px;padding:6px 2px}
.dots i{width:13px;height:13px;border-radius:50%;background:rgba(255,255,255,.55);animation:dt 1s ease-in-out infinite}
.dots i:nth-child(2){animation-delay:.15s}.dots i:nth-child(3){animation-delay:.3s}
@keyframes dt{50%{transform:translateY(-7px);opacity:.3}}
.gone{animation:gone .25s ease forwards}
@keyframes gone{to{opacity:0;height:0;padding:0;margin:0;overflow:hidden}}
"""

TARJETAS = {}  # id → (inicio en el video, duración, css, html, script)

# 0:00 · «dos aplicaciones corriendo 24-7… también desde mi teléfono»
TARJETAS['c01-homelab'] = (0.3, 9.0, ROWS_CSS + """
.big24{margin-left:auto;font-size:30px;font-weight:900;color:#30d158;letter-spacing:-.02em}
.phone{margin-top:14px;display:flex;gap:14px;align-items:center;padding:14px 18px;border-radius:16px;background:rgba(10,132,255,.14);box-shadow:inset 0 0 0 1.5px rgba(10,132,255,.45);font-size:24px;font-weight:600}
.phone .sub{margin-left:auto;font-size:20px}
""", f"""<div class="hd">{T.SERVER_IC}<div class="app">Homelab</div><div class="big24 pop" {d(3.5)}>24/7</div></div>
<div class="ti" style="margin-bottom:6px"><span class="dot" style="margin-right:12px"></span>ubuntu-server · en línea</div>
<div class="row pop" {d(1.3)}><div class="mini" style="background:linear-gradient(135deg,#30d158,#0a7d3b)">💰</div><div class="info"><div class="n">Finanzas</div><div class="sub">:3000</div></div><span class="bd ok"><span class="dot"></span>corriendo</span></div>
<div class="row pop" {d(1.6)}><div class="mini" style="background:linear-gradient(135deg,#ff6b6b,#c9184a)">🔐</div><div class="info"><div class="n">Contraseñas</div><div class="sub">:4000</div></div><span class="bd ok"><span class="dot"></span>corriendo</span></div>
<div class="phone pop" {d(5.9)}>📱 También en mi teléfono<span class="sub green">conectado ✓</span></div>""")

# 0:18 · ficha de Finanzas: «básica y sencilla… se lo pedí a Claude… desde cero… auto-hosteado»
TARJETAS['c02-finanzas'] = (18.4, 7.4, """
.app-row{display:flex;gap:22px;align-items:center}
.big-ic{width:120px;height:120px;border-radius:28px;background:linear-gradient(135deg,#30d158,#0a5a2b);display:flex;align-items:center;justify-content:center;font-size:60px;box-shadow:0 8px 24px rgba(48,209,88,.3)}
.nm{font-size:36px;font-weight:700}
.tags{display:flex;gap:10px;margin-top:22px;flex-wrap:wrap}
.tag{padding:10px 18px;border-radius:12px;background:rgba(255,255,255,.08);font-size:21px;font-weight:600}
.tag.cl{background:rgba(217,119,87,.18);color:#ffc2a8;box-shadow:inset 0 0 0 2px rgba(217,119,87,.55)}
""", f"""<div class="app-row"><div class="big-ic pop" {d(.2)}>💰</div><div><div class="nm">Finanzas</div><div class="sub">Básica y sencilla</div></div></div>
<div class="tags"><div class="tag cl pop" {d(3.3)}>✦ Hecha por Claude</div><div class="tag pop" {d(4.9)}>🧱 Desde cero</div><div class="tag pop" {d(5.9)}>🏠 Auto-hosteada</div></div>""")

# 0:26 · movimientos: «registrando mis movimientos, mis ingresos y sobre todo mis egresos»
movs = [('🍔', 'Comida', 'hoy', '−$420', 6.0), ('⛽', 'Gasolina', 'ayer', '−$800', 6.35), ('📺', 'Suscripciones', 'lun', '−$219', 6.7)]
rows = ''.join(f'<div class="row pop" {d(t)}><div class="mini" style="background:rgba(255,69,58,.16)">{e}</div><div class="info"><div class="n">{n}</div><div class="sub">{w}</div></div><div class="amt red">{a}</div></div>' for e, n, w, a, t in movs)
TARJETAS['c03-movimientos'] = (26.3, 8.4, ROWS_CSS + """
.bal{display:flex;align-items:baseline;gap:14px;margin-bottom:6px}.bal b{font-size:48px;font-weight:900;letter-spacing:-.03em}
""", f"""<div class="hd">{FIN_IC}<div class="app">Movimientos</div><div class="tm">octubre</div></div>
<div class="bal pop" {d(.5)}><b id="bal">$32,352</b><span class="sub">balance</span></div>
<div class="row pop" {d(4.1)}><div class="mini" style="background:rgba(48,209,88,.16)">💼</div><div class="info"><div class="n">Ingreso · Nómina</div><div class="sub">1 oct</div></div><div class="amt green">+$18,500</div></div>
{rows}""",
"""window.__seek=t=>{const v=t<6.0?32352:t<6.35?31932:t<6.7?31132:30913;document.getElementById('bal').textContent='$'+v.toLocaleString('en-US')}""")

# 0:39 · «cada vez que gasto algo se lo mando a un bot de Telegram… y aquí lo registra»
TARJETAS['c04-telegram'] = (39.0, 8.2, CHAT_CSS + """
.rec{display:flex;gap:12px;align-items:center;margin-top:16px;padding:14px 18px;border-radius:16px;background:rgba(48,209,88,.12);box-shadow:inset 0 0 0 1.5px rgba(48,209,88,.45);font-size:23px;font-weight:600}
""", f"""<div class="hd">{TG_IC}<div class="app">Telegram · FinanzasBot</div><div class="tm">ahora</div></div>
<div class="chat">
 <div class="me pop" {d(.7)}><span class="type" style="--td:1.1s;--n:22;animation-delay:.9s">Gasté $250 en tacos 🌮</span></div>
 <div class="bot pop" {d(3.0)}><div class="av" style="background:linear-gradient(135deg,#30d158,#0a7d3b)">💰</div>
  <div class="bb"><div class="who">FinanzasBot</div><div class="dots" style="animation:gone .2s ease 4.9s forwards"><i></i><i></i><i></i></div>
  <div class="pop" style="animation-delay:5.1s">✅ Registrado: <b>Comida −$250</b></div></div></div>
</div>
<div class="rec pop" {d(6.0)}>💰 Finanzas · nuevo movimiento <span class="red" style="margin-left:auto;font-weight:800">−$250</span></div>""")

# 1:02 · análisis con IA: «cada mes analiza… en qué se me está yendo el dinero… mejores prácticas para ahorrar»
cats = [('Comida', 38, '#ff9f0a'), ('Transporte', 22, '#5ac8fa'), ('Suscripciones', 15, '#bf5af2'), ('Otros', 25, '#8e8e93')]
bars = ''.join(f'<div class="cat pop{" hot" if k == 0 else ""}" style="animation-delay:{8.0 + k * .3:.1f}s"><div class="cl"><span>{n}</span><b>{p}%</b></div>'
               f'<div class="trk"><i style="width:{p * 2.2}%;background:{c};animation-delay:{8.15 + k * .3:.2f}s"></i></div></div>' for k, (n, p, c) in enumerate(cats))
TARJETAS['c05-analisis'] = (62.4, 17.9, """
.prog{margin:4px 0 16px}.prog .r{display:flex;justify-content:space-between;font-size:22px;color:rgba(255,255,255,.6);margin-bottom:10px}
.trk{height:16px;border-radius:8px;background:rgba(255,255,255,.1);overflow:hidden}
.trk i{display:block;height:100%;border-radius:8px;transform-origin:left;animation:fillL 1s ease both}
@keyframes fillL{from{transform:scaleX(0)}}
.cat{padding:9px 12px;margin:0 -12px;border-radius:14px}.cat .cl{display:flex;justify-content:space-between;font-size:23px;font-weight:600;margin-bottom:8px}
.hot{animation:pop .45s cubic-bezier(.22,1.3,.36,1) 8.0s both,hot .5s ease 12.4s forwards}
@keyframes hot{to{background:rgba(255,159,10,.14);box-shadow:inset 0 0 0 2px rgba(255,159,10,.7)}}
.warn{font-size:20px;font-weight:800;color:#ff9f0a;margin-left:10px;opacity:0;animation:fade .3s ease 12.6s forwards}
.tip{display:flex;gap:14px;align-items:flex-start;margin-top:16px;padding:16px 18px;border-radius:16px;background:rgba(48,209,88,.12);box-shadow:inset 0 0 0 1.5px rgba(48,209,88,.45);font-size:23px;line-height:1.35}
""", f"""<div class="hd">{AI_IC}<div class="app">Análisis con IA</div><div class="tm">cada mes</div></div>
<div class="prog pop" {d(.4)}><div class="r"><span>Octubre · ingresos y gastos</span><span id="pc">0%</span></div><div class="trk"><i style="width:100%;background:linear-gradient(90deg,#bf5af2,#5e5ce6);animation-duration:2.6s;animation-delay:4.8s"></i></div></div>
{bars.replace('<span>Comida</span>', '<span>Comida<span class="warn">⚠ aquí se te va</span></span>', 1)}
<div class="tip pop" {d(14.6)}><span style="font-size:30px">💡</span><span>Cocina 2 días más por semana y <b class="green">ahorra ~$1,200 al mes</b></span></div>""",
"""window.__seek=t=>{const p=Math.min(1,Math.max(0,(t-4.8)/2.6));document.getElementById('pc').textContent=Math.round(p*100)+'%'}""")

# 1:20 · contraseñas: «generar y guardar contraseñas seguras… palabra secreta… para visualizarlas»
accs = [('G', '#ea4335', 'Gmail', 'p4$Wq!9zLm'), ('A', '#ff9900', 'AWS', 'K7#vR2@xTe'), ('⌥', '#24292f', 'GitHub', 'm9!Zc8&QwY')]
vault = ''.join(f'<div class="row pop" style="animation-delay:{6.6 + k * .25:.2f}s"><div class="mini" style="background:{c};font-size:24px;font-weight:800">{l}</div>'
                f'<div class="info"><div class="n">{n}</div></div><div class="pw"><span class="hid">••••••••••</span><span class="vis">{p}</span></div></div>' for k, (l, c, n, p) in enumerate(accs))
TARJETAS['c06-contrasenas'] = (80.5, 13.6, ROWS_CSS + """
.gen{display:flex;gap:14px;align-items:center;padding:16px 18px;border-radius:16px;background:rgba(255,255,255,.07);font-family:ui-monospace,Menlo,monospace;font-size:27px}
.gen .lb{font-family:Inter,sans-serif;font-size:19px;font-weight:700;color:rgba(255,255,255,.5);text-transform:uppercase;letter-spacing:.06em}
.saved{margin-left:auto;font-family:Inter,sans-serif;font-size:19px}
.lock{display:flex;gap:14px;align-items:center;margin:16px 0 4px;padding:16px 18px;border-radius:16px;background:rgba(255,69,58,.12);box-shadow:inset 0 0 0 1.5px rgba(255,69,58,.45);font-size:23px;font-weight:600;
  animation:pop .45s cubic-bezier(.22,1.3,.36,1) 6.3s both,unl .4s ease 11.4s forwards}
@keyframes unl{to{background:rgba(48,209,88,.12);box-shadow:inset 0 0 0 1.5px rgba(48,209,88,.5)}}
.lock .inp{margin-left:auto;font-size:30px;letter-spacing:.12em;color:rgba(255,255,255,.85)}
.lk{position:relative;display:inline-block;width:30px}.lk2{position:absolute;left:0;top:0;opacity:0;animation:fade .2s ease 11.4s forwards}.lk1{animation:off .1s linear 11.4s forwards}
.pw{position:relative;font-family:ui-monospace,Menlo,monospace;font-size:24px;min-width:200px;text-align:right}
.pw .vis{position:absolute;right:0;top:0;opacity:0;animation:fade .3s ease 11.7s forwards;color:#30d158}
.pw .hid{animation:off .2s ease 11.6s forwards;color:rgba(255,255,255,.5)}
@keyframes off{to{opacity:0}}
""", f"""<div class="hd">{PASS_IC}<div class="app">Contraseñas</div><div class="tm">homelab</div></div>
<div class="gen pop" {d(2.4)}><span class="lb">Generar</span><span class="type" style="--td:1.2s;--n:14;animation-delay:2.8s">Xq7!mZ@2vL#9pR</span><span class="saved bd ok pop" {d(3.9)}>✓ Guardada</span></div>
<div class="lock"><span class="lk"><span class="lk1">🔒</span><span class="lk2">🔓</span></span>Palabra secreta<span class="inp"><span class="type" style="--td:1.3s;--n:8;animation-delay:8.3s">••••••••</span></span></div>
{vault}""")

# 1:42 · «yo construí el backend y le pedí a Claude que mejorara el frontend»
TARJETAS['c07-stack'] = (102.1, 8.6, """
.cols{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.col{border-radius:20px;padding:22px;background:rgba(255,255,255,.06);text-align:center}
.col .e{font-size:54px;line-height:1.1}.col .k{font-size:19px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.5);margin-top:10px}
.col .w{font-size:32px;font-weight:800;margin-top:4px}
.col.cl{background:rgba(217,119,87,.14);box-shadow:inset 0 0 0 2px rgba(217,119,87,.6)}
""", f"""<div class="hd">{PASS_IC}<div class="app">Contraseñas · cómo la hice</div></div>
<div class="cols"><div class="col pop" {d(2.0)}><div class="e">⚙️</div><div class="k">Backend</div><div class="w">Yo</div></div>
<div class="col cl pop" {d(4.4)}><div class="e" style="color:#d97757">✦</div><div class="k">Frontend</div><div class="w">Claude</div></div></div>""")

# 1:51 · «me la manda por Telegram… 30 segundos en modo spoiler… después se borra»
TARJETAS['c08-spoiler'] = (111.3, 16.8, CHAT_CSS + """
.spo{position:relative;display:inline-block;font-family:ui-monospace,Menlo,monospace;font-size:27px;margin-top:6px;padding:4px 8px;border-radius:8px}
.spo .txt{filter:blur(9px);opacity:.9}
.spo:after{content:'';position:absolute;inset:0;border-radius:8px;background-image:radial-gradient(rgba(255,255,255,.75) 1px,transparent 1.4px);background-size:7px 7px;animation:shim .6s steps(3) infinite}
@keyframes shim{50%{background-position:3px 4px}}
.timer{display:flex;align-items:center;gap:14px;margin-top:16px;font-size:22px;font-weight:600;color:rgba(255,255,255,.65)}
.timer .trk{flex:1;height:12px;border-radius:6px;background:rgba(255,255,255,.1);overflow:hidden}
.timer .trk i{display:block;height:100%;width:100%;background:linear-gradient(90deg,#ff453a,#ff9f0a);transform-origin:left;animation:drain 8.2s linear 6.6s both}
@keyframes drain{to{transform:scaleX(0)}}
.timer b{font-size:30px;font-weight:900;color:#fff;min-width:66px;text-align:right}
.msg{animation:pop .45s cubic-bezier(.22,1.3,.36,1) 4.8s both,poof .5s ease 14.9s forwards}
@keyframes poof{to{opacity:0;filter:blur(10px);transform:scale(.9)}}
.del{position:absolute;left:27px;right:27px;bottom:94px;text-align:center;font-size:23px;color:rgba(255,255,255,.55);font-style:italic;opacity:0;animation:fade .4s ease 15.3s forwards}
.card{position:relative}
""", f"""<div class="hd">{TG_IC}<div class="app">Telegram · ContraseñasBot</div><div class="tm">ahora</div></div>
<div class="chat">
 <div class="me pop" {d(2.2)}>/pass gmail</div>
 <div class="bot msg"><div class="av" style="background:linear-gradient(135deg,#ff6b6b,#c9184a)">🔐</div>
  <div class="bb"><div class="who">ContraseñasBot</div>Tu contraseña de Gmail:<br><span class="spo"><span class="txt">p4$Wq!9zLm</span></span></div></div>
</div>
<div class="del">🗑 Mensaje eliminado</div>
<div class="timer pop" {d(6.6)}>⏱ Se borra en<div class="trk"><i></i></div><b id="sec">30s</b></div>""",
"""window.__seek=t=>{const p=Math.min(1,Math.max(0,(t-6.6)/8.2));document.getElementById('sec').textContent=Math.ceil(30*(1-p))+'s'}""")

# 2:53 · «si agregas a más personas a tu red privada, también van a poder acceder»
people = [('📱', 'iPhone de Armando', 'tú', .5), ('🖥️', 'homelab', 'servidor', .8), ('👩', 'Mamá', 'invitada', 2.9), ('👨', 'Hermano', 'invitado', 3.3)]
prow = ''.join(f'<div class="row pop" {d(t)}><div class="mini" style="background:rgba(255,255,255,.08)">{e}</div><div class="info"><div class="n">{n}</div><div class="sub">{s}</div></div>'
               f'<span class="bd ok acc" style="animation-delay:{5.7 + k * .15:.2f}s">✓ apps</span></div>' for k, (e, n, s, t) in enumerate(people))
TARJETAS['c09-red'] = (173.2, 8.0, ROWS_CSS + """
.acc{opacity:0;animation:fade .3s ease both}
""", f"""<div class="hd">{TS_IC}<div class="app">Tailscale · mi red privada</div><div class="tm">4 equipos</div></div>{prow}""")

ESCENAS = {}  # id → (inicio, duración, css, html, script)

def heads(steps, grad):
    return ''.join(f'<div class="step" style="animation:stIn .45s cubic-bezier(.22,1.2,.36,1) {a}s both' + (f',stOut .3s ease {b}s forwards' if b else '') + f'">{t}</div>' for t, a, b in steps)

STEP_CSS = """
.step{position:absolute;left:40px;right:40px;top:120px;text-align:center;font-size:64px;font-weight:900;letter-spacing:-.03em;line-height:1.08;opacity:0}
.step em{font-style:normal;background:linear-gradient(90deg,var(--g1),var(--g2));-webkit-background-clip:text;color:transparent}
@keyframes stIn{from{opacity:0;transform:translateY(24px);filter:blur(6px)}to{opacity:1;transform:none;filter:none}}
@keyframes stOut{to{opacity:0;transform:translateY(-24px);filter:blur(6px)}}
.phone{position:absolute;left:50%;width:470px;height:960px;margin-left:-235px;border-radius:70px;background:#0b0c12;
  box-shadow:inset 0 0 0 12px #2a2c36,inset 0 0 0 14px #444754,0 40px 90px rgba(0,0,0,.6)}
.phone:before{content:'';position:absolute;left:50%;top:30px;width:130px;height:36px;margin-left:-65px;border-radius:20px;background:#000;z-index:5}
.scr{position:absolute;inset:14px;border-radius:58px;overflow:hidden}
"""

# 0:51 · PWA: «le pedí a Claude que la convirtiera en una PWA… instalar la web como una aplicación de mi teléfono»
ESCENAS['s1-pwa'] = (50.8, 11.8, STEP_CSS + """
.scene{--g1:#5ac8fa;--g2:#30d158}
.phone{top:380px;animation:pop .6s cubic-bezier(.22,1.3,.36,1) .5s both}
.web{position:absolute;inset:0;background:#10131c;padding:90px 26px 0}
.url{height:52px;border-radius:26px;background:rgba(255,255,255,.1);display:flex;align-items:center;justify-content:center;font-size:21px;color:rgba(255,255,255,.7)}
.wb{margin-top:26px;border-radius:24px;padding:24px;background:linear-gradient(160deg,#173a2a,#0f1a16);box-shadow:inset 0 0 0 1.5px rgba(48,209,88,.35)}
.wb .k{font-size:20px;color:rgba(255,255,255,.55)}.wb .v{font-size:46px;font-weight:900;letter-spacing:-.02em;margin-top:6px}
.wl{height:70px;border-radius:18px;background:rgba(255,255,255,.06);margin-top:16px}
.sheet{position:absolute;left:0;right:0;bottom:0;padding:26px 24px 50px;border-radius:34px 34px 0 0;background:#23252e;transform:translateY(100%);
  animation:shUp .45s cubic-bezier(.22,1.1,.36,1) 4.6s forwards,shDn .35s ease 6.5s forwards}
@keyframes shUp{to{transform:none}}@keyframes shDn{from{transform:none}to{transform:translateY(100%)}}
.opt{display:flex;align-items:center;gap:16px;padding:18px;border-radius:16px;font-size:24px;font-weight:600;margin-top:8px;background:rgba(255,255,255,.06)}
.opt.add{background:rgba(10,132,255,.2);box-shadow:inset 0 0 0 2px #0a84ff;animation:tap .25s ease 5.9s}
@keyframes tap{50%{transform:scale(.94)}}
.home{position:absolute;inset:0;padding:110px 34px 0;background:radial-gradient(500px 500px at 30% 20%,#3a2a6b,transparent),radial-gradient(500px 500px at 80% 90%,#0f4a5c,transparent),#11131d;
  opacity:0;animation:fade .45s ease 6.8s forwards}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:30px 20px}
.ap{display:flex;flex-direction:column;align-items:center;gap:8px;font-size:16px;color:rgba(255,255,255,.75)}
.ap i{width:82px;height:82px;border-radius:20px;background:rgba(255,255,255,.12)}
.ap.new i{display:flex;align-items:center;justify-content:center;font-size:44px;font-style:normal;background:linear-gradient(135deg,#30d158,#0a5a2b);
  box-shadow:0 0 0 3px rgba(48,209,88,.6),0 0 40px rgba(48,209,88,.6);animation:pop .55s cubic-bezier(.22,1.6,.36,1) 7.5s both}
.ap.new span{color:#fff;font-weight:700;animation:fade .3s ease 7.8s both}
.badge{position:absolute;left:50%;top:1400px;transform:translateX(-50%);white-space:nowrap;padding:18px 30px;border-radius:999px;background:rgba(48,209,88,.14);
  box-shadow:inset 0 0 0 2px rgba(48,209,88,.5);font-size:28px;font-weight:800;color:#b8f5c8;opacity:0;animation:fade .5s ease 8.4s forwards}
""", f"""{heads([('Le pedí a <em>Claude</em>', .2, 2.9), ('que la hiciera <em>PWA</em>', 3.0, 4.6), ('<em>instalar</em> la web…', 4.7, 6.6), ('…como una <em>app</em><br>de mi teléfono', 6.7, None)], '')}
<div class="phone"><div class="scr">
 <div class="web"><div class="url">🔒 finanzas.homelab</div><div class="wb"><div class="k">Balance</div><div class="v">$32,352</div></div><div class="wl"></div><div class="wl"></div><div class="wl"></div></div>
 <div class="sheet"><div class="opt">↗️ Compartir</div><div class="opt add">➕ Agregar a inicio</div><div class="opt">🔖 Marcador</div></div>
 <div class="home"><div class="grid">{''.join('<div class="ap"><i></i>&nbsp;</div>' for _ in range(6))}<div class="ap new"><i>💰</i><span>Finanzas</span></div>{''.join('<div class="ap"><i></i>&nbsp;</div>' for _ in range(5))}</div></div>
</div></div>
<div class="badge">📲 sin App Store · se abre como app</div>""")

# 2:25 · Tailscale: «gracias a Tailscale, que funciona como una VPN… desde cualquier lugar… lo llevo en el bolsillo»
ESCENAS['s2-tailscale'] = (145.3, 17.0, STEP_CSS + """
.scene{--g1:#ffffff;--g2:#5ac8fa}
.node{position:absolute;width:250px;height:250px;border-radius:60px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;font-size:28px;font-weight:800;
  background:rgba(255,255,255,.07);box-shadow:inset 0 0 0 2px rgba(255,255,255,.18)}
.node span{font-size:96px;line-height:1}
.n-ph{left:90px;top:760px;animation:pop .55s cubic-bezier(.22,1.35,.36,1) .6s both}
.n-hl{right:90px;top:760px;animation:pop .55s cubic-bezier(.22,1.35,.36,1) 1.0s both}
.tun{position:absolute;left:340px;right:340px;top:860px;height:50px;border-radius:25px;background:rgba(90,200,250,.1);box-shadow:inset 0 0 0 2px rgba(90,200,250,.5),0 0 40px rgba(90,200,250,.35);
  transform-origin:left;animation:tunIn .7s ease 2.0s both}
@keyframes tunIn{from{transform:scaleX(0)}}
.tun i{position:absolute;top:15px;width:20px;height:20px;border-radius:50%;background:#5ac8fa;box-shadow:0 0 16px #5ac8fa;opacity:0;animation:pk 1.3s linear infinite}
@keyframes pk{0%{left:10px;opacity:0}10%{opacity:1}90%{opacity:1}100%{left:calc(100% - 30px);opacity:0}}
.ts{position:absolute;left:50%;top:640px;margin-left:-60px;width:120px;height:120px;border-radius:30px;background:#242424;box-shadow:inset 0 0 0 2px rgba(255,255,255,.2),0 0 50px rgba(90,200,250,.35);
  display:flex;align-items:center;justify-content:center;animation:pop .55s cubic-bezier(.22,1.35,.36,1) 1.6s both}
.lock{position:absolute;left:50%;top:930px;margin-left:-110px;width:220px;text-align:center;font-size:24px;font-weight:700;color:#bfe9ff;opacity:0;animation:fade .4s ease 3.2s forwards}
.places{position:absolute;left:0;right:0;top:1150px;display:flex;justify-content:center;gap:18px;flex-wrap:wrap;padding:0 60px}
.pl{padding:16px 26px;border-radius:999px;background:rgba(255,255,255,.08);font-size:27px;font-weight:700;animation:pop .45s cubic-bezier(.22,1.35,.36,1) both}
.pocket{position:absolute;left:50%;top:1370px;transform:translateX(-50%);white-space:nowrap;padding:20px 34px;border-radius:999px;background:rgba(48,209,88,.14);
  box-shadow:inset 0 0 0 2px rgba(48,209,88,.5);font-size:30px;font-weight:800;color:#b8f5c8;opacity:0;animation:fade .5s ease 11.4s forwards}
.x{position:absolute;left:50%;top:1150px;transform:translateX(-50%);white-space:nowrap;font-size:30px;font-weight:700;color:rgba(255,255,255,.7);opacity:0;animation:fade .4s ease 7.6s forwards,off .3s ease 10.8s forwards}
.x s{text-decoration-color:#ff453a;text-decoration-thickness:4px}
@keyframes off{to{opacity:0}}
.places.p1{animation:off .3s ease 7.3s forwards}
""", f"""{heads([('<em>Tailscale</em>', .2, 1.7), ('funciona como una <em>VPN</em>', 1.8, 3.9), ('acceso desde<br><em>cualquier lugar</em>', 4.0, 7.4), ('sin estar en<br><em>la computadora</em>', 7.5, 10.9), ('siempre en el <em>bolsillo</em>', 11.0, None)], '')}
<div class="ts">{TS_IC.replace('class="ic"', 'style="transform:scale(1.9)"')}</div>
<div class="node n-ph"><span>📱</span>Teléfono</div>
<div class="tun"><i></i><i style="animation-delay:.45s"></i><i style="animation-delay:.9s"></i></div>
<div class="lock">🔒 red privada</div>
<div class="node n-hl"><span>🖥️</span>Homelab</div>
<div class="places p1">{''.join(f'<div class="pl" style="animation-delay:{4.4 + k * .3:.1f}s">{p}</div>' for k, p in enumerate(['☕ Café', '🏢 Oficina', '✈️ De viaje', '🚗 En la calle']))}</div>
<div class="x">🖥️ <s>sentarme frente al homelab</s></div>
<div class="pocket">💰 Finanzas · 🔐 Contraseñas · y más…</div>""")

# 2:42 · receta: «computadora viejita → instala Ubuntu → instala Tailscale → tu servidor»
pasos = [('💻', 'Una compu viejita', 3.3), ('🐧', 'Instala Ubuntu', 5.9), ('⠿', 'Instala Tailscale', 6.9), ('🚀', 'Tu propio servidor', 8.7)]
steps_html = ''.join(f'<div class="ps" style="animation-delay:{t}s"><div class="num">{k + 1}</div><span class="e">{e}</span>{n}</div>' for k, (e, n, t) in enumerate(pasos))
ESCENAS['s3-receta'] = (162.3, 10.8, STEP_CSS + """
.scene{--g1:#ff9f0a;--g2:#ffd60a}
.list{position:absolute;left:110px;right:110px;top:470px}
.ps{display:flex;align-items:center;gap:24px;padding:30px 32px;margin-bottom:22px;border-radius:28px;background:rgba(255,255,255,.07);box-shadow:inset 0 0 0 2px rgba(255,255,255,.12);
  font-size:38px;font-weight:800;animation:pop .5s cubic-bezier(.22,1.35,.36,1) both}
.ps .num{width:56px;height:56px;border-radius:50%;background:rgba(255,159,10,.2);color:#ffb340;font-size:28px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.ps .e{font-size:56px;line-height:1;width:66px;text-align:center}
.ps:last-child{background:rgba(48,209,88,.13);box-shadow:inset 0 0 0 2.5px rgba(48,209,88,.6),0 0 50px rgba(48,209,88,.25)}
.ps:last-child .num{background:rgba(48,209,88,.25);color:#30d158}
""", f"""{heads([('¿Tienes una<br><em>compu viejita</em>?', .2, None)], '')}
<div class="list">{steps_html}</div>""")

# cierre (mismo «Sígueme» del video 6): «aún tengo más servicios… nos vemos en un próximo commit»
SEGUIR = (181.2, 8.37)

if __name__ == '__main__':
    solo = set(sys.argv[1:])
    peek = os.environ.get('SOLO_HTML')
    todos = {**{k: ('T', v) for k, v in TARJETAS.items()}, **{k: ('E', v) for k, v in ESCENAS.items()}}
    for kid, (kind, (ini, dur, css, body, *script)) in todos.items():
        if solo and kid not in solo:
            continue
        html = T.page(css, body, dur, script[0] if script else '') if kind == 'T' else E.page(css, body, dur, script[0] if script else '')
        path = f'{WORK}/{kid}.html'
        open(path, 'w').write(html)
        if peek:
            print('html', path); continue
        r = subprocess.run(['node', CAP, path, str(dur), f'{OUT}/{kid}.webm'], capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr[-600:], flush=True)
    if not solo:
        rel = os.environ.get('REL', 'videos/7/animaciones')
        ov = [{'file': f'{rel}/{k}.webm', 'start': v[1][0], 'end': round(v[1][0] + v[1][1], 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for k, v in todos.items()]
        ov.append({'file': f'{rel}/seguir.webm', 'start': SEGUIR[0], 'end': round(SEGUIR[0] + SEGUIR[1], 2), 'trimIn': 0, 'scale': 1, 'position': 'center'})
        json.dump(sorted(ov, key=lambda o: o['start']), open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
