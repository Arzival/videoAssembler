"""Animaciones del video 6 (suscripciones de Claude y Codex). Reutiliza el sistema visual de
tarjetas.py / escenas.py. Uso: SALIDA=videos/6/animaciones python3 ejemplos/video6.py [ids…]
"""
import os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import tarjetas as T
import escenas as E

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.getcwd()))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
d = T.d
CLAUDE_MINI = ('<div class="mini" style="background:#d97757"><svg width="30" height="30" viewBox="0 0 24 24"><path fill="#fff" '
               'd="M12 2l1.6 6.1L19.8 6l-4.3 4.7L22 12l-6.5 1.3 4.3 4.7-6.2-2.1L12 22l-1.6-6.1L4.2 18l4.3-4.7L2 12l6.5-1.3L4.2 6l6.2 2.1z"/></svg></div>')
CODEX_MINI = '<div class="mini" style="background:#101114;box-shadow:inset 0 0 0 2px rgba(255,255,255,.22);font-size:26px;font-weight:800">⌘</div>'
ROWS_CSS = """
.sub-row{display:flex;gap:18px;align-items:center;padding:16px 0}
.sub-row+.sub-row{border-top:1.5px solid rgba(255,255,255,.08)}
.mini{width:52px;height:52px;border-radius:13px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.info{flex:1}.info .n{font-size:25px;font-weight:600}
.pr{text-align:right;font-size:27px;font-weight:800}
.bd{display:inline-block;font-size:17px;font-weight:700;padding:5px 10px;border-radius:8px;margin-top:6px}
.ok{background:rgba(48,209,88,.16);color:#30d158}
"""

TARJETAS = {}  # id → (duración, css, html, script)

# 0:00 · suscripciones (gancho)
TARJETAS['c01-subs'] = (6.5, ROWS_CSS, f"""<div class="hd"><div class="ic" style="background:#3a3a3c;font-size:30px">💳</div><div class="app">Suscripciones</div><div class="tm">mensual</div></div>
<div class="sub-row pop" {d(.4)}>{CLAUDE_MINI}<div class="info"><div class="n">Claude Max</div><div class="sub">Opus · Fable</div></div><div class="pr">$100<span class="sub">/mes</span></div></div>
<div class="sub-row pop" {d(1.6)}>{CODEX_MINI}<div class="info"><div class="n">Codex</div><div class="sub">Astra</div></div><div class="pr">$20<span class="sub">/mes</span></div></div>""")

# 0:18 · historial: Claude Pro (abril) → Cursor antes → 3 meses en $20 → hoy Max
TARJETAS['c02-historial'] = (21.0, """
.tl{position:relative;padding-left:46px;margin-top:8px}
.tl:before{content:'';position:absolute;left:15px;top:12px;bottom:12px;width:3px;border-radius:2px;background:rgba(255,255,255,.12)}
.ev{position:relative;padding:12px 0 14px}
.ev:before{content:'';position:absolute;left:-39px;top:20px;width:20px;height:20px;border-radius:50%;background:var(--c);box-shadow:0 0 0 5px rgba(30,30,30,1),0 0 18px var(--c)}
.ev .w{font-size:19px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:rgba(255,255,255,.45)}
.ev .n{font-size:26px;font-weight:700;margin-top:2px}.ev .n b{float:right;font-weight:800}
.ev .x{font-size:21px;color:rgba(255,255,255,.55);margin-top:2px}
.strike b{text-decoration:line-through;text-decoration-color:#ff453a;text-decoration-thickness:3px}
""", f"""<div class="hd"><div class="ic" style="background:#5e5ce6;font-size:30px">🧾</div><div class="app">Historial de pagos</div><div class="tm">2026</div></div>
<div class="tl">
 <div class="ev pop strike" style="--c:#8e8e93;animation-delay:8.6s"><div class="w">Antes</div><div class="n">Cursor <b>hasta $60</b></div><div class="x">se empezaron a poner con sus cosas…</div></div>
 <div class="ev pop" style="--c:#d97757;animation-delay:2.4s"><div class="w">Abril</div><div class="n">Claude Pro <b>$20</b></div><div class="x">la suscripción con la que empecé</div></div>
 <div class="ev pop" style="--c:#30d158;animation-delay:15.6s"><div class="w">3 meses</div><div class="n">Pagando $20 <b class="green">✓ muy buena</b></div></div>
 <div class="ev pop" style="--c:#ff9f0a;animation-delay:18.0s"><div class="w">Hoy</div><div class="n">Claude Max <b>$100</b></div></div>
</div>""")

# 0:41 · consejo: con $20 alcanza
TARJETAS['c03-tip'] = (6.5, """
.big{font-size:40px;font-weight:800;letter-spacing:-.02em;margin:4px 0 10px}
.chk{display:flex;gap:14px;align-items:center;margin-top:14px;font-size:23px}
.chk i{font-style:normal;width:40px;height:40px;border-radius:50%;background:#30d158;color:#06210f;font-weight:900;display:flex;align-items:center;justify-content:center;flex-shrink:0}
""", f"""<div class="hd"><div class="ic" style="background:#ffd60a;font-size:32px">💡</div><div class="app">Tip</div><div class="tm">ahora</div></div>
<div class="big pop" {d(.35)}>Con $20 alcanza</div>
<div class="sub pop" {d(.7)}>No necesitas pasarte al plan de $100 para trabajar muy bien.</div>
<div class="chk pop" {d(1.4)}><i>✓</i>Proyectos reales con el plan Pro</div>""")

# 0:53 · ficha de Claude Manager
TARJETAS['c04-app'] = (6.0, """
.app-row{display:flex;gap:22px;align-items:center}
.big-ic{width:120px;height:120px;border-radius:28px;background:linear-gradient(135deg,#d97757,#3b1d14);display:flex;align-items:center;justify-content:center;font-size:52px;font-weight:800;font-family:ui-monospace,Menlo,monospace;box-shadow:0 8px 24px rgba(217,119,87,.35)}
.nm{font-size:36px;font-weight:700}
.btn{margin-left:auto;background:#0a84ff;padding:14px 30px;border-radius:30px;font-size:24px;font-weight:700;animation:pop .45s cubic-bezier(.22,1.3,.36,1) .7s both}
.tags{display:flex;gap:10px;margin-top:22px;flex-wrap:wrap}
.tag{padding:10px 18px;border-radius:12px;background:rgba(255,255,255,.08);font-size:21px;font-weight:600}
""", f"""<div class="app-row"><div class="big-ic pop" {d(.2)}>&gt;_</div><div><div class="nm">Claude Manager</div><div class="sub">Controla tus consolas de Claude</div></div><div class="btn">Abrir</div></div>
<div class="tags"><div class="tag pop" {d(1.0)}>🖥️ Consolas</div><div class="tag pop" {d(1.15)}>📊 Estadísticas de uso</div><div class="tag pop" {d(1.3)}>⚙️ Y más</div></div>""")

# 1:16 · uso real vs lo que pagas (el dato fuerte)
TARJETAS['c05-uso'] = (19.0, ROWS_CSS + """
.cmp{display:grid;grid-template-columns:1fr auto;align-items:end;gap:6px 18px;margin-top:8px}
.val{font-size:62px;font-weight:900;letter-spacing:-.03em;line-height:1}
.paid{text-align:right;font-size:22px;color:rgba(255,255,255,.55)}.paid b{display:block;font-size:30px;color:#fff}
.x{display:inline-block;margin-top:10px;font-size:22px;font-weight:800;padding:6px 14px;border-radius:10px;background:rgba(48,209,88,.16);color:#30d158}
.blk{padding:14px 0 18px}.blk+.blk{border-top:1.5px solid rgba(255,255,255,.08)}
.who{display:flex;align-items:center;gap:14px;font-size:24px;font-weight:700;margin-bottom:10px}.who .mini{width:44px;height:44px;border-radius:11px}
""", f"""<div class="hd"><div class="ic" style="background:#30d158;font-size:30px">📊</div><div class="app">Últimos 30 días</div><div class="tm">valor en API</div></div>
<div class="blk pop" {d(4.2)}><div class="who">{CLAUDE_MINI} Claude</div>
 <div class="cmp"><div class="val" id="v1">$0</div><div class="paid">pagas<b>$100</b></div></div><span class="x pop" {d(6.6)}>8.3× lo que pagas</span></div>
<div class="blk pop" {d(12.3)}><div class="who">{CODEX_MINI} Codex</div>
 <div class="cmp"><div class="val" id="v2">$0</div><div class="paid">pagas<b>$20</b></div></div><span class="x pop" {d(14.6)}>3× lo que pagas</span></div>""",
"""window.__seek=t=>{const c=(a,b,s,e)=>{const p=Math.min(1,Math.max(0,(t-s)/e));return Math.round(a+(b-a)*(1-Math.pow(1-p,3)))};
document.getElementById('v1').textContent='$'+c(0,829,4.5,2.0);document.getElementById('v2').textContent='$'+c(0,61,12.6,1.8)}""")

# 1:40 · modelos que más uso
TARJETAS['c06-modelos'] = (14.0, """
.grp{margin-top:14px}.grp .lb{display:flex;align-items:center;gap:12px;font-size:22px;font-weight:700;color:rgba(255,255,255,.6);margin-bottom:12px}
.grp .lb .mini{width:40px;height:40px;border-radius:10px}
.chips{display:flex;gap:12px;flex-wrap:wrap}
.chip{padding:13px 22px;border-radius:14px;font-size:25px;font-weight:700;background:rgba(255,255,255,.07)}
.chip.o{box-shadow:inset 0 0 0 2.5px #d97757;color:#ffc2a8}.chip.g{box-shadow:inset 0 0 0 2.5px #5ac8fa;color:#bfe9ff}
.note{margin-top:14px;font-size:21px;color:#ff9f0a}
""", f"""<div class="hd"><div class="ic" style="background:#bf5af2;font-size:30px">🧠</div><div class="app">Modelos que más uso</div><div class="tm">30 días</div></div>
<div class="grp"><div class="lb">{CLAUDE_MINI} Claude</div><div class="chips">
 <div class="chip o pop" {d(3.4)}>Opus 5</div><div class="chip o pop" {d(7.5)}>Opus 5.5</div><div class="chip o pop" {d(9.6)}>Fable 5</div></div></div>
<div class="grp pop" {d(11.4)}><div class="lb">{CODEX_MINI} Codex</div><div class="chips"><div class="chip g">Astra</div></div>
 <div class="note pop" {d(12.6)}>⚡ se come los tokens enseguida</div></div>""")

# 3:07 · notificación: salto a Max
TARJETAS['c07-max'] = (5.0, """
.nt{display:flex;gap:18px;align-items:flex-start}.nt .t{font-size:26px;font-weight:600}
""", f"""<div class="hd" style="margin-bottom:10px">{T.CLAUDE_IC}<div class="app">Claude</div><div class="tm">ahora</div></div>
<div class="ti">Bienvenido a Claude Max 🎉</div><div class="sub" style="margin-top:4px">Plan de $100/mes activado · Opus 5.5 y Fable</div>""")

# 3:18 · tip: optimiza tus prompts
TARJETAS['c08-prompts'] = (6.5, """
.big{font-size:40px;font-weight:800;letter-spacing:-.02em;margin:4px 0 12px}
.pr{display:flex;gap:12px;align-items:center;margin-top:12px;font-size:22px;padding:12px 16px;border-radius:14px;background:rgba(255,255,255,.06)}
.pr .tag{font-size:17px;font-weight:800;padding:4px 10px;border-radius:8px}
.bad .tag{background:rgba(255,69,58,.18);color:#ff453a}.good .tag{background:rgba(48,209,88,.16);color:#30d158}
""", f"""<div class="hd"><div class="ic" style="background:#ffd60a;font-size:32px">✍️</div><div class="app">Tip</div><div class="tm">ahora</div></div>
<div class="big pop" {d(.35)}>Optimiza tus prompts</div>
<div class="pr bad pop" {d(1.0)}><span class="tag">ANTES</span>«arréglame esto»</div>
<div class="pr good pop" {d(1.8)}><span class="tag">MEJOR</span>contexto + objetivo + pasos claros</div>
<div class="sub pop" style="margin-top:14px;animation-delay:2.6s">y el plan de $20 te rinde de sobra</div>""")

# 4:00 · cómo mejoré los diseños (mientras se ven en pantalla)
TARJETAS['c09-pulido'] = (8.0, """
.st{display:flex;gap:16px;align-items:center;padding:13px 0;font-size:24px}
.st i{font-style:normal;width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;flex-shrink:0;font-size:20px}
""", f"""<div class="hd"><div class="ic" style="background:#5ac8fa;font-size:30px">🎨</div><div class="app">Diseños del homelab</div><div class="tm">proceso</div></div>
<div class="st pop" {d(.4)}><i style="background:#5ac8fa;color:#002">1</i>Base creada con <b>Astra</b></div>
<div class="st pop" {d(2.0)}><i style="background:#d97757">2</i><b>Opus 5.5</b> la mejora con una librería</div>
<div class="st pop" {d(4.6)}><i style="background:#30d158;color:#032">3</i>Con imágenes de referencia</div>""")

ESCENAS = {}

# 2:25 → 3:01 · el método de antes: Opus planea, Sonnet ejecuta
acts = ['Analizar el problema', 'Crear la estructura', 'Implementar la lógica', 'Probar y corregir']
docl = ''.join(f'<div class="dl" style="animation-delay:{12.8 + k * .5:.1f}s"><span>☐</span>{a}</div>' for k, a in enumerate(acts))
todo = ''.join(f'<div class="td" style="animation-delay:{18.6 + k * .45:.2f}s"><i class="ck" style="animation-delay:{21.0 + k * 1.1:.1f}s">✓</i>{a}</div>' for k, a in enumerate(acts))
steps = [('Un problema <em>complicado</em>', .2, 6.2), ('<em>Opus</em> lo planea', 6.3, 17.3), ('<em>Sonnet</em> lo ejecuta', 17.4, 26.2), ('con el plan de <em>$20</em>', 26.3, None)]
heads = ''.join(f'<div class="step" style="animation:stIn .45s cubic-bezier(.22,1.2,.36,1) {a}s both' + (f',stOut .3s ease {b}s forwards' if b else '') + f'">{t}</div>' for t, a, b in steps)
ESCENAS['s1-metodo'] = (35.5, """
.step{position:absolute;left:40px;right:40px;top:110px;text-align:center;font-size:66px;font-weight:900;letter-spacing:-.03em;opacity:0}
.step em{font-style:normal;background:linear-gradient(90deg,#ffb38f,#d97757);-webkit-background-clip:text;color:transparent}
@keyframes stIn{from{opacity:0;transform:translateY(24px);filter:blur(6px)}to{opacity:1;transform:none;filter:none}}
@keyframes stOut{to{opacity:0;transform:translateY(-24px);filter:blur(6px)}}
.bug{position:absolute;left:50%;top:330px;width:300px;margin-left:-150px;padding:26px;border-radius:30px;text-align:center;background:rgba(255,69,58,.12);
  box-shadow:inset 0 0 0 2px rgba(255,69,58,.5);font-size:30px;font-weight:700;animation:pop .55s cubic-bezier(.22,1.35,.36,1) .9s both,bugOut .4s ease 6.6s forwards}
.bug span{display:block;font-size:80px;line-height:1.1}
@keyframes bugOut{to{opacity:0;transform:scale(.8) translateY(-40px)}}
.node{position:absolute;width:200px;height:200px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;font-size:28px;font-weight:800}
.node svg{width:70px;height:70px}
.opus{left:440px;top:300px;background:radial-gradient(circle at 35% 30%,#f0936f,#b4552f);box-shadow:0 0 0 3px rgba(217,119,87,.5),0 0 70px rgba(217,119,87,.45);
  animation:pop .55s cubic-bezier(.22,1.35,.36,1) 6.6s both,glow 1.4s ease-in-out 7.4s 6}
.sonnet{left:440px;top:1060px;background:radial-gradient(circle at 35% 30%,#ffd6c4,#d97757);color:#3b1d14;box-shadow:0 0 0 3px rgba(255,214,196,.5),0 0 70px rgba(255,214,196,.35);
  animation:pop .55s cubic-bezier(.22,1.35,.36,1) 17.6s both}
@keyframes glow{50%{transform:scale(1.06)}}
.doc{position:absolute;left:210px;top:560px;width:660px;border-radius:26px;padding:28px 30px;background:#f4f1ea;color:#1c1c1e;box-shadow:0 30px 70px rgba(0,0,0,.55);
  transform-origin:top center;animation:docIn .6s cubic-bezier(.22,1.3,.36,1) 8.0s both,docOut .5s ease 26.0s forwards}
@keyframes docIn{from{opacity:0;transform:translateY(-60px) scale(.7)}to{opacity:1;transform:none}}
@keyframes docOut{to{opacity:0;transform:translateY(30px) scale(.92)}}
.doc h4{font-size:30px;font-weight:800;margin-bottom:6px}
.doc .ln{height:12px;border-radius:6px;background:#d7d3c9;margin:12px 0;transform-origin:left;animation:lnIn .5s ease both}
@keyframes lnIn{from{transform:scaleX(0)}}
.dl{display:flex;gap:14px;align-items:center;font-size:26px;font-weight:600;padding:9px 0;animation:pop .4s cubic-bezier(.22,1.35,.36,1) both}
.dl span{color:#8e8e93}
.flow{position:absolute;left:530px;top:945px;width:20px;height:110px}
.flow i{position:absolute;left:0;width:20px;height:20px;border-radius:50%;background:#ffb38f;box-shadow:0 0 16px #ffb38f;opacity:0;animation:drop .9s ease-in 17.5s 4}
@keyframes drop{0%{top:0;opacity:0}20%{opacity:1}100%{top:100px;opacity:0}}
.todo{position:absolute;left:150px;right:150px;top:1300px}
.td{display:flex;align-items:center;gap:16px;padding:16px 22px;margin-bottom:12px;border-radius:18px;background:rgba(255,255,255,.07);font-size:27px;font-weight:600;
  animation:pop .45s cubic-bezier(.22,1.35,.36,1) both}
.ck{font-style:normal;width:42px;height:42px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-weight:900;
  background:rgba(255,255,255,.1);color:transparent;animation:ckOn .35s cubic-bezier(.22,1.6,.36,1) both}
@keyframes ckOn{from{background:rgba(255,255,255,.1);color:transparent;transform:scale(.6)}to{background:#30d158;color:#06210f;transform:none}}
.meter{position:absolute;left:150px;right:150px;top:560px;padding:30px;border-radius:30px;background:rgba(255,255,255,.07);
  box-shadow:inset 0 0 0 2px rgba(255,255,255,.12);animation:pop .6s cubic-bezier(.22,1.35,.36,1) 26.6s both}
.meter .r{display:flex;justify-content:space-between;font-size:26px;font-weight:700;margin:6px 0 10px}
.trk{height:24px;border-radius:12px;background:rgba(255,255,255,.1);overflow:hidden;margin-bottom:22px}
.trk i{display:block;height:100%;border-radius:12px;background:#30d158;transform-origin:left;animation:fillL 1.6s ease 27.3s both}
@keyframes fillL{from{transform:scaleX(0)}}
.never{text-align:center;font-size:34px;font-weight:900;margin-top:6px;animation:pop .5s cubic-bezier(.22,1.35,.36,1) 30.0s both}
""", f"""{heads}
<div class="bug"><span>🧩</span>Problema complicado</div>
<div class="node opus">{E.CLAUDE_SVG}Opus</div>
<div class="doc"><h4>📄 plan.md</h4><div class="ln" style="width:80%;animation-delay:8.7s"></div><div class="ln" style="width:60%;animation-delay:9.2s"></div>{docl}</div>
<div class="flow"><i></i></div>
<div class="node sonnet">{E.CLAUDE_SVG.replace('fill="#fff"', 'fill="#3b1d14"')}Sonnet</div>
<div class="todo">{todo}</div>
<div class="meter"><div class="r"><span>Sesiones</span><span class="green">sin problemas</span></div><div class="trk"><i style="transform:scaleX(.35)"></i></div>
 <div class="r"><span>Tokens semanales</span><span class="green">nunca se acabaron</span></div><div class="trk"><i style="transform:scaleX(.42);animation-delay:27.8s"></i></div>
 <div class="never">Jamás me pasó ✓</div></div>""")

# 3:25 → 3:50 · diseño web: Opus/Fable crea la base, Astra mejora el front
blocks = '''<div class="nav"></div><div class="hero"><div class="t1"></div><div class="t2"></div><div class="cta"></div></div>
<div class="cards"><div class="cd"></div><div class="cd"></div><div class="cd"></div></div>'''
steps2 = [('Diseño web con <em>Astra</em>', .2, 7.0), ('<em>Opus</em> o <em>Fable</em> crean la base', 7.1, 15.2), ('<em>Astra</em> mejora el front', 15.3, 20.3), ('menos contexto, <em>mejor resultado</em>', 20.4, None)]
heads2 = ''.join(f'<div class="step" style="animation:stIn .45s cubic-bezier(.22,1.2,.36,1) {a}s both' + (f',stOut .3s ease {b}s forwards' if b else '') + f'">{t}</div>' for t, a, b in steps2)
ESCENAS['s2-diseno'] = (24.5, """
.step{position:absolute;left:40px;right:40px;top:110px;text-align:center;font-size:62px;font-weight:900;letter-spacing:-.03em;opacity:0}
.step em{font-style:normal;background:linear-gradient(90deg,#5ac8fa,#bf5af2);-webkit-background-clip:text;color:transparent}
@keyframes stIn{from{opacity:0;transform:translateY(24px);filter:blur(6px)}to{opacity:1;transform:none;filter:none}}
@keyframes stOut{to{opacity:0;transform:translateY(-24px);filter:blur(6px)}}
.ais{position:absolute;top:300px;left:0;right:0;display:flex;justify-content:center;gap:40px}
.ai{width:170px;height:170px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;font-size:25px;font-weight:800}
.ai svg{width:56px;height:56px}
.a-op{background:radial-gradient(circle at 35% 30%,#f0936f,#b4552f);animation:pop .5s cubic-bezier(.22,1.35,.36,1) 7.3s both}
.a-fb{background:radial-gradient(circle at 35% 30%,#c79bff,#6e3bd8);animation:pop .5s cubic-bezier(.22,1.35,.36,1) 7.6s both}
.a-as{background:radial-gradient(circle at 35% 30%,#7fd8ff,#1a7fd0);animation:pop .5s cubic-bezier(.22,1.35,.36,1) 15.4s both;box-shadow:0 0 0 3px rgba(90,200,250,.5),0 0 70px rgba(90,200,250,.5)}
.browser{position:absolute;left:110px;right:110px;top:580px;height:900px;border-radius:30px;overflow:hidden;background:#1c1d24;
  box-shadow:inset 0 0 0 2px rgba(255,255,255,.12),0 40px 90px rgba(0,0,0,.6);animation:pop .6s cubic-bezier(.22,1.3,.36,1) 1.0s both}
.bar{height:60px;display:flex;align-items:center;gap:12px;padding:0 22px;background:#262833}
.bar i{width:16px;height:16px;border-radius:50%;background:#ff5f57}.bar i:nth-child(2){background:#febc2e}.bar i:nth-child(3){background:#28c840}
.bar .url{margin-left:14px;flex:1;height:30px;border-radius:15px;background:rgba(255,255,255,.08)}
.page{position:absolute;inset:60px 0 0 0;padding:30px}
.page>*{opacity:0;animation:pop .45s cubic-bezier(.22,1.35,.36,1) both}
.nav{height:44px;border-radius:10px;background:#3a3c48;animation-delay:8.6s!important}
.hero{margin-top:28px;padding:40px 30px;border-radius:18px;background:#2c2e39;animation-delay:9.2s!important}
.t1{height:44px;width:75%;border-radius:10px;background:#4a4c5a}.t2{height:22px;width:55%;border-radius:8px;background:#40424f;margin-top:18px}
.cta{height:56px;width:220px;border-radius:12px;background:#55576a;margin-top:30px}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:28px;animation-delay:10.0s!important}
.cd{height:230px;border-radius:16px;background:#2c2e39}
/* Astra: el mismo layout se vuelve diseño final */
.skin{position:absolute;inset:60px 0 0 0;padding:30px;background:radial-gradient(700px 400px at 70% 0%,rgba(191,90,242,.35),transparent),radial-gradient(600px 500px at 0% 100%,rgba(90,200,250,.3),transparent),#0d0f1a;
  clip-path:inset(0 100% 0 0);animation:wipe 1.6s cubic-bezier(.6,0,.2,1) 16.2s forwards}
@keyframes wipe{to{clip-path:inset(0 0 0 0)}}
.skin .nav{background:rgba(255,255,255,.08);box-shadow:inset 0 0 0 1px rgba(255,255,255,.12);opacity:1;animation:none}
.skin .hero{background:linear-gradient(135deg,rgba(191,90,242,.25),rgba(90,200,250,.18));box-shadow:inset 0 0 0 1px rgba(255,255,255,.15);opacity:1;animation:none}
.skin .t1{background:linear-gradient(90deg,#fff,#bfe9ff)}.skin .t2{background:rgba(255,255,255,.45)}
.skin .cta{background:linear-gradient(90deg,#5ac8fa,#bf5af2);box-shadow:0 10px 30px rgba(191,90,242,.5)}
.skin .cards{opacity:1;animation:none}.skin .cd{background:linear-gradient(160deg,rgba(255,255,255,.12),rgba(255,255,255,.03));box-shadow:inset 0 0 0 1px rgba(255,255,255,.14)}
.sweep{position:absolute;top:60px;bottom:0;width:8px;left:0;background:#5ac8fa;box-shadow:0 0 30px 10px rgba(90,200,250,.7);opacity:0;animation:sw 1.6s cubic-bezier(.6,0,.2,1) 16.2s both}
@keyframes sw{0%{opacity:0;left:0}3%{opacity:1}95%{opacity:1}100%{opacity:0;left:100%}}
.badge{position:absolute;left:50%;top:1530px;transform:translateX(-50%);white-space:nowrap;padding:18px 30px;border-radius:999px;background:rgba(90,200,250,.15);
  box-shadow:inset 0 0 0 2px rgba(90,200,250,.5);font-size:28px;font-weight:800;color:#bfe9ff;opacity:0;animation:fade .5s ease 20.6s forwards}
""", f"""{heads2}
<div class="ais"><div class="ai a-op">{E.CLAUDE_SVG}Opus</div><div class="ai a-fb">✦<span>Fable</span></div><div class="ai a-as"><span style="font-size:56px">🤖</span>Astra</div></div>
<div class="browser"><div class="bar"><i></i><i></i><i></i><div class="url"></div></div>
 <div class="page">{blocks}</div><div class="skin">{blocks}</div><div class="sweep"></div></div>
<div class="badge">✦ sin darle tanto contexto</div>""")

if __name__ == '__main__':
    solo = set(sys.argv[1:])
    peek = os.environ.get('SOLO_HTML')
    for kid, spec in {**{k: ('T', v) for k, v in TARJETAS.items()}, **{k: ('E', v) for k, v in ESCENAS.items()}}.items():
        if solo and kid not in solo:
            continue
        kind, (dur, css, body, *script) = spec
        html = T.page(css, body, dur, script[0] if script else '') if kind == 'T' else E.page(css, body, dur, script[0] if script else '')
        path = f'{WORK}/{kid}.html'
        open(path, 'w').write(html)
        if peek:
            print('html', path); continue
        r = subprocess.run(['node', CAP, path, str(dur), f'{OUT}/{kid}.webm'], capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr[-600:], flush=True)
