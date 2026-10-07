"""Tarjetas de interfaz integradas (mismo lenguaje visual que las notificaciones de Telegram).

Cada tarjeta = HTML con animaciones CSS (+ window.__seek para contadores) → cap.mjs → WebM con alfa.
Escala: notificación macOS ×1.7 (ancho 646px, arriba y centrada, entra desde la derecha).
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
# carpeta de salida de los .webm (y de los .html intermedios): SALIDA=… o la actual
OUT = os.path.abspath(os.environ.get('SALIDA', os.getcwd()))
WORK = os.path.join(OUT, '_html')
os.makedirs(WORK, exist_ok=True)

BASE_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;background:transparent;overflow:hidden;font-family:Inter,-apple-system,system-ui,sans-serif;color:#fff;-webkit-font-smoothing:antialiased}
.wrap{position:absolute;left:217px;top:198px;width:646px;animation:salida .42s cubic-bezier(.5,0,.75,0) var(--out) both}
.card{background:rgba(30,30,30,.86);border-radius:27px;padding:27px;box-shadow:0 14px 54px rgba(0,0,0,.45),inset 0 0 0 1.5px rgba(255,255,255,.1);
  animation:entra .62s cubic-bezier(.22,1.25,.36,1) both}
@keyframes entra{from{transform:translateX(720px);opacity:0}to{transform:none;opacity:1}}
@keyframes salida{to{transform:translateX(720px);opacity:0}}
.hd{display:flex;align-items:center;gap:18px;margin-bottom:18px}
.ic{width:61px;height:61px;border-radius:14px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-weight:700}
.app{font-size:22px;font-weight:600;color:rgba(255,255,255,.5);text-transform:uppercase;letter-spacing:.02em;flex:1}
.tm{font-size:22px;color:rgba(255,255,255,.35)}
.ti{font-size:27px;font-weight:600;line-height:1.25}
.sub{font-size:22px;color:rgba(255,255,255,.6);line-height:1.35}
.pop{animation:pop .45s cubic-bezier(.22,1.3,.36,1) both}
@keyframes pop{from{opacity:0;transform:translateY(16px) scale(.96)}to{opacity:1;transform:none}}
.fade{animation:fade .35s ease both}
@keyframes fade{from{opacity:0}to{opacity:1}}
.type{display:inline-block;white-space:nowrap;clip-path:inset(0 100% 0 0);animation:type var(--td,1.4s) steps(var(--n,30),end) both}
@keyframes type{to{clip-path:inset(0 0 0 0)}}
.green{color:#30d158}.red{color:#ff453a}.orange{color:#ff9f0a}
"""

def page(css, body, dur, script=''):
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=block" rel="stylesheet">
<style>{BASE_CSS}{css}</style></head><body>
<div class="wrap" style="--out:{dur - 0.45}s"><div class="card">{body}</div></div>
<script>{script}</script></body></html>"""

def d(s):  # helper: animation-delay inline
    return f'style="animation-delay:{s}s"'

SERVER_IC = '<div class="ic" style="background:#1f8a4c"><svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><rect x="3" y="4" width="18" height="7" rx="2"/><rect x="3" y="13" width="18" height="7" rx="2"/><circle cx="7" cy="7.5" r=".6" fill="#fff"/><circle cx="7" cy="16.5" r=".6" fill="#fff"/></svg></div>'
CLAUDE_IC = '<div class="ic" style="background:#d97757"><svg width="36" height="36" viewBox="0 0 24 24"><path fill="#fff" d="M12 2l1.6 6.1L19.8 6l-4.3 4.7L22 12l-6.5 1.3 4.3 4.7-6.2-2.1L12 22l-1.6-6.1L4.2 18l4.3-4.7L2 12l6.5-1.3L4.2 6l6.2 2.1z"/></svg></div>'
Q_IC = '<div class="ic" style="background:linear-gradient(135deg,#7c3aed,#06b6d4);font-size:34px">Q</div>'

COMPONENTES = {}

# 1 · estado del servidor (0:08 «laptop corriendo 24/7 este Linux»)
bars = ''.join(f'<i style="height:{h}%;animation-delay:{0.7 + k * 0.035:.3f}s"></i>' for k, h in
               enumerate([30, 45, 38, 52, 41, 60, 35, 48, 57, 44, 39, 62, 50, 43, 55, 47, 36, 58, 49, 41, 53, 46, 38, 51]))
COMPONENTES['u01-servidor'] = (5.0, """
.dot{display:inline-block;width:16px;height:16px;border-radius:50%;background:#30d158;margin-right:10px;vertical-align:middle;animation:pulse 1.4s ease-in-out infinite}
@keyframes pulse{50%{box-shadow:0 0 0 9px rgba(48,209,88,0)}0%{box-shadow:0 0 0 0 rgba(48,209,88,.6)}}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:20px}
.st{background:rgba(255,255,255,.06);border-radius:16px;padding:16px 18px}
.st b{display:block;font-size:40px;font-weight:700;letter-spacing:-.02em}
.bars{display:flex;align-items:flex-end;gap:5px;height:56px;margin-top:20px}
.bars i{flex:1;background:linear-gradient(#30d158,#1f8a4c);border-radius:3px;transform-origin:bottom;animation:grow .4s cubic-bezier(.22,1.3,.36,1) both}
@keyframes grow{from{transform:scaleY(0)}}
""", f"""<div class="hd">{SERVER_IC}<div class="app">Homelab</div><div class="tm">ahora</div></div>
<div class="ti"><span class="dot"></span>ubuntu-server · en línea</div>
<div class="stats">
 <div class="st pop" {d(.35)}><b>24/7</b><span class="sub">Uptime</span></div>
 <div class="st pop" {d(.5)}><b id="cpu">12%</b><span class="sub">CPU</span></div>
 <div class="st pop" {d(.65)}><b>6.2 GB</b><span class="sub">RAM de 16</span></div>
</div><div class="bars">{bars}</div>""", "window.__seek=t=>{document.getElementById('cpu').textContent=Math.round(10+4*Math.abs(Math.sin(t*2.3)))+'%'}")

# 2 · capturas → prompt a Claude (0:27 «las manda como un prompt a Claude o Codex»)
COMPONENTES['u02-prompt'] = (6.5, """
.me{display:flex;flex-direction:column;align-items:flex-end;gap:12px}
.thumbs{display:flex;gap:12px}
.th{width:118px;height:158px;border-radius:16px;position:relative;overflow:hidden;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.15)}
.th span{position:absolute;bottom:10px;left:10px;font-size:17px;font-weight:600;background:rgba(0,0,0,.45);padding:3px 9px;border-radius:8px}
.th:before{content:'';position:absolute;left:14px;right:14px;top:16px;height:10px;border-radius:5px;background:rgba(255,255,255,.35);box-shadow:0 22px 0 rgba(255,255,255,.22),0 44px 0 rgba(255,255,255,.22),0 66px 0 -10px rgba(255,255,255,.18)}
.bub{background:#0a84ff;border-radius:24px 24px 6px 24px;padding:16px 22px;font-size:24px;line-height:1.3;max-width:520px}
.dots{display:flex;gap:9px;padding:20px 4px 4px}
.dots i{width:14px;height:14px;border-radius:50%;background:rgba(255,255,255,.55);animation:dot 1s ease-in-out infinite}
.dots i:nth-child(2){animation-delay:.15s}.dots i:nth-child(3){animation-delay:.3s}
@keyframes dot{50%{transform:translateY(-8px);opacity:.3}}
.dotswrap{animation:fade .3s ease 1.7s both,gone .25s ease 3.1s forwards}
@keyframes gone{to{opacity:0;height:0;padding:0}}
.rep{display:flex;gap:14px;align-items:flex-start;margin-top:6px}
.rep .txt{font-size:24px;line-height:1.4}
""", f"""<div class="hd">{CLAUDE_IC}<div class="app">Claude</div><div class="tm">ahora</div></div>
<div class="me"><div class="thumbs">
 <div class="th pop" style="background:linear-gradient(160deg,#25f4ee,#fe2c55);animation-delay:.35s"><span>TikTok</span></div>
 <div class="th pop" style="background:linear-gradient(160deg,#f58529,#dd2a7b,#8134af);animation-delay:.5s"><span>Instagram</span></div>
</div><div class="bub pop" {d(.85)}>Analiza estas capturas y dame mis métricas</div></div>
<div class="dotswrap"><div class="dots"><i></i><i></i><i></i></div></div>
<div class="rep pop" {d(3.15)}><div class="txt">📈 TikTok <b class="green">+128</b> seguidores esta semana · Instagram <b class="green">+34</b></div></div>""")

# 3 · métricas exactas al enfocar un edificio (0:55 «me va mostrando unas métricas todavía más exactas»)
COMPONENTES['u03-metricas'] = (5.5, """
.big{font-size:64px;font-weight:800;letter-spacing:-.03em;margin-top:4px}
.chart{margin:10px 0 18px}
.chart path.l{stroke:#30d158;stroke-width:5;fill:none;stroke-linecap:round;stroke-dasharray:900;stroke-dashoffset:900;animation:draw 1.6s cubic-bezier(.4,0,.2,1) .6s forwards}
.chart path.a{fill:url(#g);opacity:0;animation:fade .8s ease 1.4s forwards}
@keyframes draw{to{stroke-dashoffset:0}}
.row{display:flex;align-items:center;gap:14px;padding-top:18px;border-top:1.5px solid rgba(255,255,255,.1);font-size:24px}
.row b{margin-left:auto}
""", f"""<div class="hd"><div class="ic" style="background:#000;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.2);font-size:32px">♪</div><div class="app">Métricas · TikTok</div><div class="tm">hoy</div></div>
<div class="sub">Seguidores</div><div class="big"><span id="n">2,303</span> <span class="green" style="font-size:30px;font-weight:700">▲ +128</span></div>
<svg class="chart" width="592" height="130" viewBox="0 0 592 130"><defs><linearGradient id="g" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#30d158" stop-opacity=".35"/><stop offset="1" stop-color="#30d158" stop-opacity="0"/></linearGradient></defs>
<path class="a" d="M4 110 L80 98 L160 102 L240 80 L320 84 L400 58 L480 50 L588 14 L588 130 L4 130Z"/>
<path class="l" d="M4 110 L80 98 L160 102 L240 80 L320 84 L400 58 L480 50 L588 14"/></svg>
<div class="row pop" {d(1.9)}><span style="font-size:28px">📸</span> Instagram <b>1,208 <span class="green">▲ +34</span></b></div>""",
"window.__seek=t=>{const p=Math.min(1,Math.max(0,(t-.6)/1.6));const e=1-Math.pow(1-p,3);document.getElementById('n').textContent=Math.round(2303+128*e).toLocaleString('en-US')}")

# 4 · nuevo encargo (1:10 «escribirle una instrucción… cuándo… frecuencia… confirmación por Telegram»)
COMPONENTES['u04-encargo'] = (9.6, """
.f{margin-top:18px}
.lb{font-size:19px;font-weight:600;color:rgba(255,255,255,.45);text-transform:uppercase;letter-spacing:.04em;margin-bottom:8px}
.in{background:rgba(255,255,255,.07);border-radius:14px;padding:15px 18px;font-size:23px;min-height:56px;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.08)}
.chips{display:flex;gap:12px}
.chip{padding:12px 20px;border-radius:12px;font-size:22px;font-weight:600;background:rgba(255,255,255,.07)}
.chip.on{box-shadow:inset 0 0 0 2.5px #d97757;color:#ffb38f;animation:sel .3s ease 3.3s both}
@keyframes sel{from{box-shadow:inset 0 0 0 2.5px rgba(255,255,255,0);color:#fff}}
.tg{display:flex;align-items:center;gap:14px;margin-top:22px;font-size:23px}
.sw{margin-left:auto;width:72px;height:42px;border-radius:21px;background:rgba(255,255,255,.18);position:relative;animation:swbg .3s ease 8.5s forwards}
.sw:after{content:'';position:absolute;top:4px;left:4px;width:34px;height:34px;border-radius:50%;background:#fff;box-shadow:0 2px 6px rgba(0,0,0,.3);animation:knob .3s cubic-bezier(.3,1.4,.5,1) 8.5s forwards}
@keyframes swbg{to{background:#30d158}}@keyframes knob{to{transform:translateX(30px)}}
""", f"""<div class="hd">{SERVER_IC}<div class="app">Homelab · Encargos</div><div class="tm">nuevo</div></div>
<div class="ti">Nuevo encargo</div>
<div class="f pop" {d(.4)}><div class="lb">Instrucción</div><div class="in"><span class="type" style="--td:2.4s;--n:42;animation-delay:.8s">Resume cómo le fue al homelab esta semana</span></div></div>
<div class="f pop" {d(3.0)}><div class="lb">Modelo</div><div class="chips"><div class="chip on">✳ Claude Code</div><div class="chip">Codex</div></div></div>
<div class="f pop" {d(4.6)}><div class="lb">Frecuencia</div><div class="in">Cada lunes · 9:00</div></div>
<div class="tg pop" {d(7.6)}><span style="font-size:30px">✈️</span> Confirmar por Telegram<div class="sw"></div></div>""")

# 5 · ficha de Qstify (1:59 «una aplicación que puedes usar 100% gratis… actividades o notas»)
COMPONENTES['u05-qstify'] = (5.6, """
.app-row{display:flex;gap:22px;align-items:center}
.big-ic{width:120px;height:120px;border-radius:28px;background:linear-gradient(135deg,#7c3aed,#06b6d4);display:flex;align-items:center;justify-content:center;font-size:64px;font-weight:800;box-shadow:0 8px 24px rgba(124,58,237,.4)}
.nm{font-size:36px;font-weight:700}
.btn{margin-left:auto;background:#0a84ff;padding:14px 30px;border-radius:30px;font-size:24px;font-weight:700;animation:pop .45s cubic-bezier(.22,1.3,.36,1) .7s both,press .25s ease 2.2s}
@keyframes press{50%{transform:scale(.9)}}
.tags{display:flex;gap:10px;margin-top:22px}
.tag{padding:10px 18px;border-radius:12px;background:rgba(255,255,255,.08);font-size:21px;font-weight:600}
.free{margin-top:20px;font-size:24px;font-weight:600}
""", f"""<div class="app-row"><div class="big-ic pop" {d(.2)}>Q</div><div><div class="nm">Qstify</div><div class="sub">Actividades, notas y proyectos</div></div><div class="btn">Gratis</div></div>
<div class="tags"><div class="tag pop" {d(1.0)}>📋 Kanban</div><div class="tag pop" {d(1.15)}>📝 Notas</div><div class="tag pop" {d(1.3)}>🕸️ Grafo</div><div class="tag pop" {d(1.45)}>⏱️ Sesiones</div></div>
<div class="free pop" {d(1.8)}><span class="green">100% gratis</span> <span class="sub">· qstify.com</span></div>""")

# 6 · notas creadas por Claude (2:32 «todas estas notas, ninguna la creé yo, todas las creó Claude»)
rows = [('Bitácora semanal del homelab', .5), ('Métricas de redes · semana 41', .8), ('Encargo: respaldo diario', 1.1), ('Recomendaciones de contenido', 1.4)]
COMPONENTES['u06-notas'] = (6.5, """
.nt{display:flex;align-items:center;gap:14px;padding:14px 0;border-bottom:1.5px solid rgba(255,255,255,.08);font-size:23px}
.nt .by{margin-left:auto;font-size:18px;font-weight:700;color:#ffb38f;background:rgba(217,119,87,.18);padding:6px 12px;border-radius:9px;white-space:nowrap}
.tot{display:flex;gap:14px;margin-top:20px}
.tot div{flex:1;background:rgba(255,255,255,.06);border-radius:16px;padding:14px 18px}
.tot b{display:block;font-size:44px;font-weight:800}
""", f"""<div class="hd">{Q_IC}<div class="app">Qstify · Notas</div><div class="tm">ahora</div></div>
<div class="ti" style="margin-bottom:6px">Notas del homelab</div>
""" + ''.join(f'<div class="nt pop" {d(t)}>📄 {n}<span class="by">✳ Claude</span></div>' for n, t in rows) + f"""
<div class="tot pop" {d(2.1)}><div><b>0</b><span class="sub">escritas por ti</span></div><div><b class="orange" id="c">0</b><span class="sub">escritas por Claude</span></div></div>""",
"window.__seek=t=>{const p=Math.min(1,Math.max(0,(t-2.3)/1.4));document.getElementById('c').textContent=Math.round(47*(1-Math.pow(1-p,3)))}")

# 7 · suscripciones (2:57 «la suscripción de 100 dólares… la de 20 se me acaba enseguida»)
COMPONENTES['u07-subs'] = (9.0, """
.sub-row{display:flex;gap:18px;align-items:center;padding:16px 0}
.sub-row+.sub-row{border-top:1.5px solid rgba(255,255,255,.08)}
.mini{width:52px;height:52px;border-radius:13px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.info{flex:1}.info .n{font-size:25px;font-weight:600}
.bar{height:10px;border-radius:5px;background:rgba(255,255,255,.1);margin-top:10px;overflow:hidden}
.bar i{display:block;height:100%;border-radius:5px;transform-origin:left}
.b1 i{background:#30d158;transform:scaleX(.38);animation:fill1 1.2s ease .8s both}
.b2 i{background:linear-gradient(90deg,#ff9f0a,#ff453a);animation:fill2 1.6s cubic-bezier(.5,0,.3,1) 4.4s both}
@keyframes fill1{from{transform:scaleX(0)}}@keyframes fill2{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.pr{text-align:right;font-size:25px;font-weight:700}
.bd{display:block;font-size:17px;font-weight:700;padding:5px 10px;border-radius:8px;margin-top:6px}
.ok{background:rgba(48,209,88,.16);color:#30d158}
.lim{background:rgba(255,69,58,.18);color:#ff453a;animation:pop .4s cubic-bezier(.22,1.3,.36,1) 6.0s both}
""", f"""<div class="hd"><div class="ic" style="background:#3a3a3c;font-size:30px">💳</div><div class="app">Suscripciones</div><div class="tm">este mes</div></div>
<div class="sub-row pop" {d(.4)}><div class="mini" style="background:#d97757"><svg width="30" height="30" viewBox="0 0 24 24"><path fill="#fff" d="M12 2l1.6 6.1L19.8 6l-4.3 4.7L22 12l-6.5 1.3 4.3 4.7-6.2-2.1L12 22l-1.6-6.1L4.2 18l4.3-4.7L2 12l6.5-1.3L4.2 6l6.2 2.1z"/></svg></div>
 <div class="info"><div class="n">Claude Max</div><div class="bar b1"><i></i></div></div><div class="pr">$100<span class="sub">/mes</span><span class="bd ok">Activa</span></div></div>
<div class="sub-row pop" {d(3.8)}><div class="mini" style="background:#10a37f;font-size:28px;font-weight:800">◎</div>
 <div class="info"><div class="n">ChatGPT Plus</div><div class="bar b2"><i></i></div></div><div class="pr">$20<span class="sub">/mes</span><span class="bd lim">Límite alcanzado</span></div></div>""")

# 8 · caja de comentario (3:17 «déjame un comentario y con gusto te respondo»)
COMPONENTES['u08-comentario'] = (5.6, """
.box{display:flex;gap:16px;align-items:center;margin-top:6px}
.av{width:54px;height:54px;border-radius:50%;background:linear-gradient(135deg,#ff9f0a,#ff375f);flex-shrink:0}
.inp{flex:1;background:rgba(255,255,255,.07);border-radius:28px;padding:15px 22px;font-size:23px;position:relative;overflow:hidden}
.ph{color:rgba(255,255,255,.35);position:absolute;left:22px;top:15px;animation:gone2 .1s linear .7s forwards}
@keyframes gone2{to{opacity:0}}
.caret{display:inline-block;width:2.5px;height:26px;background:#0a84ff;vertical-align:middle;margin-left:2px;animation:blink 1s step-end infinite}
@keyframes blink{50%{opacity:0}}
.send{width:54px;height:54px;border-radius:50%;background:rgba(255,255,255,.12);display:flex;align-items:center;justify-content:center;font-size:26px;animation:ready .25s ease 2.6s forwards,press .25s ease 3.0s}
@keyframes ready{to{background:#0a84ff}}@keyframes press{50%{transform:scale(.85)}}
.posted{display:flex;gap:16px;margin-top:22px;align-items:flex-start}
.posted .t{font-size:23px;line-height:1.35}.posted .who{font-size:19px;color:rgba(255,255,255,.45);margin-bottom:4px}
.heart{margin-left:auto;font-size:30px;animation:pop .4s cubic-bezier(.22,1.6,.36,1) 4.0s both}
""", f"""<div class="hd"><div class="ic" style="background:#ff375f;font-size:30px">💬</div><div class="app">Comentarios</div><div class="tm">ahora</div></div>
<div class="box"><div class="av"></div><div class="inp"><span class="ph">Añade un comentario…</span><span class="type" style="--td:1.8s;--n:34;animation-delay:.7s">¿Qué usas para la ciudad de métricas?</span><span class="caret"></span></div><div class="send">➤</div></div>
<div class="posted pop" {d(3.3)}><div class="av"></div><div><div class="who">Tú · ahora</div><div class="t">¿Qué usas para la ciudad de métricas?</div></div><div class="heart">❤️</div></div>""")

# 9 · cierre TikTok: seguir + like + comentario (3:15 «déjame un comentario…»)
COMPONENTES['u09-seguir'] = (8.5, """
.tt-hd{display:flex;align-items:center;gap:20px}
.tt-av{width:96px;height:96px;border-radius:50%;background:linear-gradient(135deg,#7c3aed,#06b6d4);display:flex;align-items:center;justify-content:center;font-size:44px;font-weight:800;position:relative;box-shadow:0 0 0 3px #fff}
.tt-name{font-size:32px;font-weight:800}.tt-sub{font-size:22px;color:rgba(255,255,255,.55)}
.tt-btn{margin-left:auto;position:relative;width:190px;height:66px}
.tt-btn span{position:absolute;inset:0;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:800}
.b-seg{background:linear-gradient(135deg,#7c3aed,#06b6d4);animation:tap .22s ease 1.55s,offB .2s ease 1.72s forwards}
.b-sig{background:rgba(255,255,255,.14);opacity:0;animation:onB .25s ease 1.72s forwards}
@keyframes tap{50%{transform:scale(.88)}}@keyframes offB{to{opacity:0}}@keyframes onB{to{opacity:1}}
.acts{display:flex;gap:18px;margin-top:24px}
.act{flex:1;display:flex;align-items:center;gap:14px;background:rgba(255,255,255,.07);border-radius:18px;padding:16px 20px;font-size:25px;font-weight:700;position:relative}
.act .ico{font-size:38px;line-height:1;position:relative}
.heart-on{position:absolute;left:0;top:0;opacity:0;animation:hpop .5s cubic-bezier(.22,1.8,.36,1) 3.15s both}
@keyframes hpop{0%{opacity:0;transform:scale(.2)}60%{opacity:1;transform:scale(1.35)}100%{opacity:1;transform:scale(1)}}
.burst{position:absolute;left:18px;top:18px;width:8px;height:8px;border-radius:50%;opacity:0;animation:burst .55s ease-out 3.15s both}
@keyframes burst{0%{opacity:1;box-shadow:0 0 0 #ff375f,0 0 0 #ff375f,0 0 0 #7c3aed,0 0 0 #7c3aed,0 0 0 #06b6d4,0 0 0 #06b6d4}
100%{opacity:0;box-shadow:0 -46px 0 #ff375f,40px -24px 0 #ff375f,40px 24px 0 #7c3aed,0 46px 0 #7c3aed,-40px 24px 0 #06b6d4,-40px -24px 0 #06b6d4}}
.cm{display:flex;gap:16px;align-items:center;margin-top:22px;background:rgba(255,255,255,.07);border-radius:20px;padding:16px 20px;animation:pop .45s cubic-bezier(.22,1.3,.36,1) 4.8s both}
.cm .mini{width:50px;height:50px;border-radius:50%;background:linear-gradient(135deg,#ff9f0a,#ff375f);flex-shrink:0}
.cm .who{font-size:19px;color:rgba(255,255,255,.45)}.cm .t{font-size:24px}
.finger{position:absolute;width:86px;height:86px;left:0;top:0;font-size:70px;line-height:1;filter:drop-shadow(0 6px 12px rgba(0,0,0,.6));opacity:0;
  offset-path:path('M700 560 L558 192 L88 300 L288 300');offset-rotate:0deg;
  animation:fmove 4.6s cubic-bezier(.45,0,.25,1) .7s both,ftap .22s ease 1.55s,ftap .22s ease 3.1s,ftap .22s ease 4.6s,fout .3s ease 5.6s forwards}
@keyframes fmove{0%{offset-distance:0%;opacity:0}8%{opacity:1}18%{offset-distance:36%}40%{offset-distance:36%}52%{offset-distance:81%}72%{offset-distance:81%}84%,100%{offset-distance:100%;opacity:1}}
@keyframes ftap{50%{transform:scale(.82)}}@keyframes fout{to{opacity:0}}
""", f"""<div class="hd"><div class="ic" style="background:linear-gradient(135deg,#7c3aed,#06b6d4);font-size:32px">✦</div><div class="app">Sígueme</div><div class="tm">ahora</div></div>
<div class="tt-hd"><div class="tt-av">A</div><div><div class="tt-name">Armando</div><div class="tt-sub">Homelab · Qstify · IA</div></div>
 <div class="tt-btn"><span class="b-seg">Seguir</span><span class="b-sig">Siguiendo ✓</span></div></div>
<div class="acts">
 <div class="act"><span class="ico">🤍<span class="heart-on">❤️</span><i class="burst"></i></span><span id="likes">1,203</span></div>
 <div class="act"><span class="ico">💬</span><span id="coms">48</span></div>
 <div class="act"><span class="ico">↗️</span>Compartir</div>
</div>
<div class="cm"><div class="mini"></div><div><div class="who">Tú · ahora</div><div class="t"><span class="type" style="--td:1.5s;--n:30;animation-delay:5.1s">¡Quiero ver más del homelab! 🔥</span></div></div></div>
<div class="finger">👆</div>""",
"window.__seek=t=>{document.getElementById('likes').textContent=t>=3.15?'1,204':'1,203';document.getElementById('coms').textContent=t>=4.8?'49':'48'}")

if __name__ == '__main__':
    solo = set(sys.argv[1:])
    for cid, (dur, css, body, *script) in COMPONENTES.items():
        if solo and cid not in solo:
            continue
        html = f'{WORK}/{cid}.html'
        open(html, 'w').write(page(css, body, dur, script[0] if script else ''))
        if os.environ.get('SOLO_HTML'):
            continue
        r = subprocess.run(['node', f'{HERE}/capturar.ts', html, str(dur), f'{OUT}/{cid}.webm'], capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr[-600:], flush=True)
