"""El Log #01 (semana del 5 al 9 oct 2026). Tiempos = segundos del video final (noticias/1).
Uso: SALIDA=noticias/1/animaciones python3 ejemplos/ellog-01.py [ids…]   (SOLO_HTML=1 para revisar)
Imprime al final los overlays listos para el manifiesto.
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import ellog as L
import tarjetas as T

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.getcwd()))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)

ENTRADAS = [('a1f3c9e', 'OpenAI · GPT-6 para todos'), ('7be20d4', 'OpenAI · Decisions API'), ('c93f1a8', 'Deno se une a Cloudflare'),
            ('4d8e6b2', 'Google · Gemini Agent'), ('e51a7c0', 'Mistral Large 4'), ('9f2c3d1', 'Claude Haiku 5.5')]

PIEZAS = []  # (id, inicio, fin, html)  — inicio/fin en segundos del video final


def escena(pid, start, end, css, body, script='', sigue=False):
    """sigue=True: la siguiente escena empieza en `end` encima de esta → sin salida y 0.45 s extra."""
    if sigue:
        end += 0.45
    PIEZAS.append((pid, start, end, L.page(css, body, end - start, script, salida=not sigue)))


# ───────── 0:00 · gancho
S = 0.0; A = L.at(S)
escena('e00-gancho', S, 4.8, """
.blk{position:absolute;left:60px;right:60px;padding:56px 50px;text-align:center}
.b1{top:420px;animation:pop .5s cubic-bezier(.22,1.3,.36,1) .1s both}
.b2{top:1080px;animation:pop .5s cubic-bezier(.22,1.3,.36,1) 2.7s both}
.big{font-size:150px;font-weight:900;letter-spacing:-.05em;line-height:1}
.sub{font-size:44px;font-weight:700;margin-top:14px}
.ring{position:absolute;left:50%;top:50%;width:520px;height:520px;margin:-260px 0 0 -260px;border-radius:50%;border:3px solid rgba(61,255,154,.35);opacity:0;animation:ring 1.6s ease-out .4s 3}
@keyframes ring{from{transform:scale(.4);opacity:.9}to{transform:scale(1.6);opacity:0}}
.mg{display:flex;align-items:center;justify-content:center;gap:40px}
.mg .lg{width:150px;height:150px;border-radius:36px;display:flex;align-items:center;justify-content:center}
.ar{font-size:80px;color:#3dff9a;animation:arr .6s ease-in-out 3.2s 3 alternate both}@keyframes arr{to{transform:translateX(18px)}}
.tag{position:absolute;left:0;right:0;top:170px;text-align:center;font-size:30px;letter-spacing:.3em;animation:fade .4s ease both}
""", f"""<div class="tag mono g">● ESTA SEMANA</div>
<div class="blk b1 panel"><div class="ring"></div><div style="display:flex;justify-content:center;margin-bottom:20px">{L.logo('openai', '#fff', 90)}</div>
 <div class="big">GPT-6</div><div class="sub">se libera en <span class="g">todo el mundo</span></div></div>
<div class="blk b2 panel"><div class="mg"><div class="lg" style="background:#fff">{L.logo('deno', '#000', 110)}</div><div class="ar">→</div>
 <div class="lg" style="background:#f38020">{L.logo('cloudflare', '#fff', 120)}</div></div>
 <div class="sub" style="margin-top:30px">Deno se va con <span style="color:#f38020">Cloudflare</span></div></div>""", sigue=True)

# ───────── 0:05 · intro de la sección
PIEZAS.append(('e01-intro', 4.8, 8.8 + .45, L.intro('semana del 5 al 9 de octubre', ENTRADAS, 4.45)))

# ───────── 0:09 · GPT-6 + Intelligent UI
S = 8.8; A = L.at(S)
escena('e02-gpt6', S, 26.3, f"""
.fase1{{animation:gone .35s ease {A(14.7)} forwards}}
.globe{{position:absolute;left:50%;top:600px;width:380px;height:380px;margin-left:-190px;border-radius:50%;
  background:radial-gradient(circle at 35% 30%,#1f5f45,#08130f 70%);box-shadow:0 0 0 3px rgba(61,255,154,.4),0 0 90px rgba(61,255,154,.3);animation:pop .55s cubic-bezier(.22,1.35,.36,1) {A(11.6)} both}}
.globe i{{position:absolute;inset:0;border-radius:50%;border:2px solid rgba(61,255,154,.35)}}
.globe i:nth-child(1){{animation:spinY 3s linear infinite}}.globe i:nth-child(2){{animation:spinY 3s linear -1s infinite}}.globe i:nth-child(3){{animation:spinY 3s linear -2s infinite}}
@keyframes spinY{{from{{transform:scaleX(1)}}50%{{transform:scaleX(.05)}}to{{transform:scaleX(1)}}}}
.globe b{{position:absolute;left:0;right:0;top:50%;height:2px;background:rgba(61,255,154,.35)}}
.stat{{position:absolute;top:1030px;left:0;right:0;display:flex;justify-content:center;gap:20px}}
.mods{{position:absolute;top:1170px;left:70px;right:70px;display:grid;gap:16px}}
.mod{{display:flex;align-items:center;gap:20px;padding:22px 28px;font-size:30px}}
.mod b{{font-size:34px;min-width:120px}}.mod span{{color:rgba(255,255,255,.6)}}
.fase2{{opacity:0;animation:fade .3s ease {A(14.9)} forwards}}
.chat{{position:absolute;left:70px;right:70px;top:500px;height:1050px;padding:36px;overflow:hidden}}
.u{{margin-left:auto;width:fit-content;max-width:80%;padding:20px 28px;border-radius:26px 26px 6px 26px;background:#2f3a35;font-size:30px;animation:pop .45s cubic-bezier(.22,1.35,.36,1) {A(15.6)} both}}
.ai{{display:flex;gap:18px;margin-top:30px;animation:fade .3s ease {A(16.4)} both}}
.ai .av{{width:56px;height:56px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;flex-shrink:0}}
.ai .av svg{{width:36px;height:36px}}
.resp{{flex:1}}
.txt{{font-size:28px;color:rgba(255,255,255,.8);margin-bottom:22px}}
.ui{{border-radius:22px;background:rgba(255,255,255,.05);box-shadow:inset 0 0 0 2px rgba(255,255,255,.1);padding:24px;margin-bottom:20px}}
.bars{{display:flex;align-items:flex-end;gap:16px;height:250px;padding-top:10px}}
.bars i{{flex:1;border-radius:10px 10px 4px 4px;background:linear-gradient(#3dff9a,#1b8f57);transform-origin:bottom;animation:grow .7s cubic-bezier(.22,1.2,.36,1) both}}
@keyframes grow{{from{{transform:scaleY(0)}}}}
.lbls{{display:flex;gap:16px;margin-top:10px}}.lbls span{{flex:1;text-align:center;font-size:20px;color:rgba(255,255,255,.5)}}
.form{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
.in{{padding:16px 18px;border-radius:12px;background:rgba(255,255,255,.07);font-size:22px;color:rgba(255,255,255,.55)}}
.btns{{display:flex;gap:14px;margin-top:16px}}
.bt{{padding:16px 26px;border-radius:14px;font-size:24px;font-weight:700;background:rgba(255,255,255,.1)}}
.bt.p{{background:#3dff9a;color:#04210f;animation:press .3s ease {A(22.0)} 2 alternate}}@keyframes press{{to{{transform:scale(.93)}}}}
.live{{display:flex;align-items:center;gap:14px;font-size:24px}}
.live .dt{{width:16px;height:16px;border-radius:50%;background:#ff5c5c;box-shadow:0 0 14px #ff5c5c;animation:blink 1s steps(1) infinite}}
.live b{{font-size:44px;margin-left:auto}}
.lbl2{{position:absolute;left:0;right:0;top:440px;text-align:center;font-size:30px;letter-spacing:.06em}}
""", f"""{L.entry(1, 'a1f3c9e', L.logo('openai'), 'OpenAI')}
<div class="fase1">
 {L.steps([('<em>GPT-6</em> para todos', 8.95, None)], S, top=290, size=96)}
 <div class="globe"><i></i><i></i><i></i><b></b></div>
 <div class="stat"><span class="chip pop" style="animation-delay:{A(12.1)}">🌎 a nivel global</span><span class="chip pop" style="animation-delay:{A(12.5)}">📅 desde el 7 oct</span></div>
 <div class="mods">
  <div class="mod panel pop" style="animation-delay:{A(12.9)}"><b class="g">Sol</b><span>planes de pago</span></div>
  <div class="mod panel pop" style="animation-delay:{A(13.3)}"><b class="g">Luna</b><span>Free y Go</span></div>
  <div class="mod panel pop" style="animation-delay:{A(13.7)}"><b class="g">Astra</b><span>el más potente</span></div></div>
</div>
<div class="fase2">
 {L.steps([('Intelligent <em>UI</em>', 15.0, None)], S, top=290, size=96)}
 <div class="lbl2 mono dim fade" style="animation-delay:{A(15.3)}">// la respuesta ya no es solo texto</div>
 <div class="chat panel">
  <div class="u">¿Cómo van las ventas del trimestre?</div>
  <div class="ai"><div class="av">{L.logo('openai', '#000')}</div><div class="resp">
   <div class="txt"><span class="type" style="--n:26;--td:.8s;animation-delay:{A(16.6)}">Aquí tienes el resumen ✨</span></div>
   <div class="ui pop" style="animation-delay:{A(17.3)}"><div class="bars">
     <i style="height:45%;animation-delay:{A(17.6)}"></i><i style="height:62%;animation-delay:{A(17.75)}"></i><i style="height:54%;animation-delay:{A(17.9)}"></i>
     <i style="height:80%;animation-delay:{A(18.05)}"></i><i style="height:96%;animation-delay:{A(18.2)}"></i></div>
     <div class="lbls"><span>Jun</span><span>Jul</span><span>Ago</span><span>Sep</span><span>Oct</span></div></div>
   <div class="ui pop" style="animation-delay:{A(19.6)}"><div class="form"><div class="in">Región ▾</div><div class="in">Periodo ▾</div></div>
     <div class="btns"><div class="bt p">Proyectar</div><div class="bt">Exportar</div></div></div>
   <div class="ui pop" style="animation-delay:{A(22.6)}"><div class="live"><span class="dt"></span>en tiempo real<b id="vv">$0</b></div></div>
  </div></div></div>
</div>""", f"""window.__seek=t=>{{t+={S};const p=Math.min(1,Math.max(0,(t-23.0)/2.2));
document.getElementById('vv').textContent='$'+(679.0*(1-Math.pow(1-p,3))+(t>25.2?((t-25.2)*1.3):0)).toFixed(1)+'k'}}""")

# ───────── 0:29 · Decisions API
S = 29.0; A = L.at(S)
escena('e03-decisions', S, 35.3, f"""
.dev{{position:absolute;left:0;right:0;top:300px;text-align:center}}
.q{{position:absolute;left:70px;right:70px;top:640px;padding:40px}}
.q .lb{{font-size:24px;margin-bottom:14px}}.q .tx{{font-size:38px;font-weight:700;margin-bottom:30px}}
.ops{{display:grid;gap:16px}}
.op{{display:flex;align-items:center;gap:18px;padding:22px 26px;border-radius:18px;background:rgba(255,255,255,.06);font-size:30px;font-weight:600}}
.op i{{width:30px;height:30px;border-radius:50%;box-shadow:inset 0 0 0 3px rgba(255,255,255,.35)}}
.op.win{{animation:pop .45s cubic-bezier(.22,1.35,.36,1) {A(31.3)} both,win .35s ease {A(33.7)} forwards}}
.op.win i{{animation:dotOn .3s ease {A(33.7)} forwards}}
@keyframes win{{to{{background:rgba(61,255,154,.16);box-shadow:inset 0 0 0 3px #3dff9a}}}}
@keyframes dotOn{{to{{background:#3dff9a;box-shadow:0 0 16px #3dff9a}}}}
.ms{{margin-left:auto;font-size:24px;color:#3dff9a;opacity:0;animation:fade .3s ease {A(33.8)} forwards}}
.facts{{position:absolute;top:1330px;left:70px;right:70px;display:flex;flex-wrap:wrap;gap:16px;justify-content:center}}
""", f"""{L.entry(2, '7be20d4', L.logo('openai'), 'OpenAI')}
<div class="dev"><span class="chip pop" style="animation-delay:{A(29.6)}">🎤 DevDay · 29 sep</span></div>
{L.steps([('<em>Decisions</em> API', 32.4, None)], S, top=440, size=100)}
<div class="q panel pop" style="animation-delay:{A(30.6)}"><div class="lb mono dim">pregunta → respuestas cerradas</div>
 <div class="tx">¿A qué equipo va este ticket?</div><div class="ops">
 <div class="op pop" style="animation-delay:{A(30.9)}"><i></i>Soporte</div><div class="op pop" style="animation-delay:{A(31.1)}"><i></i>Ventas</div>
 <div class="op win"><i></i>Facturación<span class="ms mono">✓ ~150 ms</span></div></div></div>
<div class="facts"><span class="chip pop" style="animation-delay:{A(34.0)}">⚡ ~10× más rápida</span><span class="chip pop" style="animation-delay:{A(34.3)}">GPT-6 Luna</span>
 <span class="chip pop" style="animation-delay:{A(34.6)}">🔒 preview limitada</span></div>""", sigue=True)

# ───────── 0:35 · Deno se une a Cloudflare + Hacker News
S = 35.3; A = L.at(S)
escena('e04-deno', S, 47.7, f"""
.merge{{position:absolute;left:0;right:0;top:330px;height:420px}}
.lg{{position:absolute;top:60px;width:260px;height:260px;border-radius:60px;display:flex;align-items:center;justify-content:center;box-shadow:0 30px 70px rgba(0,0,0,.5)}}
.dn{{left:130px;background:#fff;animation:pop .5s cubic-bezier(.22,1.35,.36,1) {A(35.6)} both,toCF .9s cubic-bezier(.6,0,.2,1) {A(38.2)} forwards}}
.cf{{right:130px;background:#f38020;animation:pop .5s cubic-bezier(.22,1.35,.36,1) {A(36.0)} both,cfGlow .6s ease {A(39.0)} both}}
@keyframes toCF{{to{{transform:translateX(560px) scale(.45);opacity:0}}}}
@keyframes cfGlow{{50%{{transform:translateX(-140px) scale(1.12)}}to{{transform:translateX(-280px);box-shadow:0 0 0 6px rgba(243,128,32,.4),0 0 110px rgba(243,128,32,.6)}}}}
.plus{{position:absolute;left:0;right:0;top:150px;text-align:center;font-size:90px;font-weight:900;color:#3dff9a;animation:fade .3s ease {A(36.3)} both,gone .3s ease {A(38.2)} forwards}}
.hn{{position:absolute;left:70px;right:70px;top:1010px;overflow:hidden;border-radius:26px;background:#f6f6ef;color:#000;box-shadow:0 30px 80px rgba(0,0,0,.55);
  animation:pop .55s cubic-bezier(.22,1.3,.36,1) {A(40.1)} both}}
.hn .hd{{display:flex;align-items:center;gap:16px;padding:18px 24px;background:#ff6600;font-size:30px;font-weight:800}}
.hn .hd span{{border:3px solid #fff;color:#fff;width:46px;height:46px;display:flex;align-items:center;justify-content:center;font-weight:900}}
.hn .bd{{padding:30px 34px}}
.hn .t{{font-size:38px;font-weight:700;font-family:Verdana,Inter,sans-serif}}.hn .t small{{font-size:24px;color:#828282;font-weight:400}}
.nums{{display:flex;gap:26px;margin-top:26px}}
.nm{{flex:1;padding:22px;border-radius:18px;background:#fff;box-shadow:inset 0 0 0 2px #e4e4dc}}
.nm b{{display:block;font-size:72px;font-weight:900;letter-spacing:-.03em;color:#ff6600}}.nm span{{font-size:24px;color:#555}}
.top{{position:absolute;right:90px;top:985px;z-index:2;padding:12px 22px;border-radius:14px;background:#3dff9a;color:#04210f;font-size:26px;font-weight:900;transform:rotate(4deg);
  animation:pop .45s cubic-bezier(.22,1.5,.36,1) {A(42.4)} both}}
""", f"""{L.entry(3, 'c93f1a8', L.logo('deno'), 'Deno')}
<div class="merge"><div class="lg dn">{L.logo('deno', '#000', 170)}</div><div class="plus">+</div><div class="lg cf">{L.logo('cloudflare', '#fff', 190)}</div></div>
{L.steps([('Deno se une a <em style="color:#f38020">Cloudflare</em>', 38.3, None)], S, top=800, size=76)}
<div class="top">🔥 lo más comentado</div>
<div class="hn"><div class="hd"><span>Y</span>Hacker News</div><div class="bd">
 <div class="t">Deno is joining Cloudflare <small>(deno.com)</small></div>
 <div class="nums"><div class="nm"><b id="pts">0</b><span>puntos</span></div><div class="nm"><b id="cms">0</b><span>comentarios</span></div></div></div></div>""",
f"""window.__seek=t=>{{t+={S};const c=(v,s,e)=>Math.round(v*(1-Math.pow(1-Math.min(1,Math.max(0,(t-s)/e)),3)));
document.getElementById('pts').textContent=c(500,44.2,1.0)+(t>45.2?'+':'');document.getElementById('cms').textContent=(t>46.6?'~':'')+c(300,45.6,1.0)}}""")

# ───────── 0:48 · tarjeta sobre el clip (web de Deno): qué cambia
PIEZAS.append(('e05-deno-cambios', 47.9, 54.1, T.page("""
.rw{display:flex;gap:18px;align-items:flex-start;padding:16px 0}.rw+.rw{border-top:1.5px solid rgba(255,255,255,.08)}
.rw i{font-style:normal;font-size:34px;line-height:1}.rw b{display:block;font-size:26px}.rw span{font-size:22px;color:rgba(255,255,255,.6)}
""", f"""<div class="hd"><div class="ic" style="background:#fff">{L.logo('deno', '#000', 40)}</div><div class="app">Si usas Deno</div><div class="tm">qué cambia</div></div>
<div class="rw pop" {T.d(.5)}><i>⏳</i><div><b>Deno Deploy cierra</b><span>en ~6 meses · migración a Workers</span></div></div>
<div class="rw pop" {T.d(1.7)}><i>🛠️</i><div><b>Runtime: 1 año más</b><span>parches de seguridad y bugs</span></div></div>
<div class="rw pop" {T.d(2.9)}><i>📦</i><div><b>JSR sigue</b><span>ahora sobre Cloudflare</span></div></div>""", 6.2)))

# ───────── 0:54 · Gemini Agent
S = 54.2; A = L.at(S)
apps = [('gmail', '#ea4335', -300, -40), ('googledrive', '#1fa463', -200, -230), ('googlecalendar', '#4285f4', 0, -300),
        ('googlesheets', '#0f9d58', 200, -230), ('slack', '#e01e5a', 300, -40), ('salesforce', '#00a1e0', 0, 260)]
apps_html = ''.join(f'<div class="app" style="--x:{x}px;--y:{y}px;animation-delay:{A(60.1 + k * .2)}">{L.logo(n, c, 54)}</div>' for k, (n, c, x, y) in enumerate(apps))
lines = ''.join(f'<line x1="540" y1="880" x2="{540 + x}" y2="{880 + y}" style="animation-delay:{A(60.3 + k * .2)}"/>' for k, (n, c, x, y) in enumerate(apps))
escena('e06-gemini', S, 76.2, f"""
.zone{{position:absolute;left:0;top:0;width:1080px;height:1920px}}
.core{{position:absolute;left:440px;top:780px;width:200px;height:200px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  background:radial-gradient(circle at 35% 30%,#5b8cff,#1a3fb0);box-shadow:0 0 0 4px rgba(91,140,255,.45),0 0 110px rgba(91,140,255,.55);
  animation:pop .55s cubic-bezier(.22,1.35,.36,1) {A(55.6)} both,pulse 1.6s ease-in-out {A(57)} infinite}}
@keyframes pulse{{50%{{box-shadow:0 0 0 14px rgba(91,140,255,.12),0 0 140px rgba(91,140,255,.7)}}}}
.app{{position:absolute;left:calc(540px + var(--x) - 55px);top:calc(880px + var(--y) - 55px);width:110px;height:110px;border-radius:28px;background:#fff;
  display:flex;align-items:center;justify-content:center;box-shadow:0 16px 40px rgba(0,0,0,.5);animation:pop .45s cubic-bezier(.22,1.35,.36,1) both}}
svg.ln{{position:absolute;left:0;top:0;width:1080px;height:1920px}}
svg.ln line{{stroke:rgba(91,140,255,.55);stroke-width:4;stroke-dasharray:10 12;opacity:0;animation:fade .3s ease both,flow .8s linear infinite}}
@keyframes flow{{to{{stroke-dashoffset:-44}}}}
.apps{{animation:gone .35s ease {A(63.3)} forwards}}
.subs{{position:absolute;left:0;right:0;top:1100px;display:flex;justify-content:center;gap:30px}}
.sa{{width:270px;padding:26px 20px;text-align:center;border-radius:26px;animation:pop .45s cubic-bezier(.22,1.35,.36,1) both}}
.sa .ro{{font-size:46px}}.sa .n{{font-size:24px;font-weight:700;margin:8px 0 14px}}
.md{{display:inline-flex;align-items:center;gap:8px;padding:8px 14px;border-radius:12px;font-size:21px;font-weight:800;opacity:0;animation:pop .4s cubic-bezier(.22,1.35,.36,1) both}}
.md svg{{width:24px;height:24px}}
.cl{{background:rgba(217,119,87,.18);color:#ffb38f;box-shadow:inset 0 0 0 2px #d97757}}.ge{{background:rgba(91,140,255,.16);color:#a9c1ff;box-shadow:inset 0 0 0 2px #5b8cff}}
.cl.hl{{animation:pop .4s cubic-bezier(.22,1.35,.36,1) {A(67.3)} both,hl 1s ease-in-out {A(67.8)} 3}}@keyframes hl{{50%{{box-shadow:inset 0 0 0 2px #d97757,0 0 40px rgba(217,119,87,.8)}}}}
.fase2{{animation:gone .35s ease {A(69.0)} forwards}}
.id{{position:absolute;left:110px;right:110px;top:640px;padding:44px;opacity:0;animation:pop .55s cubic-bezier(.22,1.3,.36,1) {A(69.3)} both}}
.id .tp{{display:flex;justify-content:space-between;font-size:22px;margin-bottom:30px}}
.id .who{{display:flex;gap:26px;align-items:center}}
.id .pic{{width:140px;height:140px;border-radius:30px;background:radial-gradient(circle at 35% 30%,#5b8cff,#1a3fb0);display:flex;align-items:center;justify-content:center;font-size:76px}}
.id .nm{{font-size:44px;font-weight:800}}.id .rl{{font-size:26px;color:rgba(255,255,255,.6);margin-top:6px}}
.mail{{margin-top:36px;padding:24px 26px;border-radius:18px;background:rgba(255,255,255,.06);display:flex;gap:18px;align-items:center;font-size:29px}}
.mail svg{{width:46px;height:46px;flex-shrink:0}}
.ok{{display:inline-block;margin-top:28px;padding:12px 20px;border-radius:12px;background:rgba(61,255,154,.15);color:#3dff9a;font-size:24px;font-weight:800;opacity:0;animation:pop .4s ease {A(70.4)} both}}
""", f"""{L.entry(4, '4d8e6b2', L.logo('googlecloud'), 'Google Cloud')}
{L.steps([('<em style="color:#8fb0ff">Gemini</em> Agent', 54.5, 58.5), ('Planea y <em style="color:#8fb0ff">ejecuta</em>', 58.6, 63.3), ('Reparte el trabajo', 63.4, 66.0),
          ('con <em style="color:#ffb38f">Claude</em> incluido', 66.1, 69.0), ('Su propia <em style="color:#8fb0ff">identidad</em>', 69.1, None)], S, top=290, size=88)}
<div class="lbl mono dim fade" style="position:absolute;left:0;right:0;top:420px;text-align:center;font-size:28px;animation-delay:{A(56.8)};animation:fade .4s ease {A(56.8)} both,gone .3s ease {A(58.5)} forwards">// un agente para empresas</div>
<div class="fase2"><div class="zone apps"><svg class="ln">{lines}</svg>{apps_html}</div>
 <div class="core">{L.logo('googlegemini', '#fff', 110)}</div>
 <div class="subs">
  <div class="sa panel" style="animation-delay:{A(64.4)}"><div class="ro">🤖</div><div class="n">subagente 1</div><span class="md ge" style="animation-delay:{A(66.4)}">{L.logo('googlegemini', '#a9c1ff')}Gemini</span></div>
  <div class="sa panel" style="animation-delay:{A(64.8)}"><div class="ro">🤖</div><div class="n">subagente 2</div><span class="md cl hl">{L.logo('claude', '#ffb38f')}Claude</span></div>
  <div class="sa panel" style="animation-delay:{A(65.2)}"><div class="ro">🤖</div><div class="n">subagente 3</div><span class="md ge" style="animation-delay:{A(66.7)}">{L.logo('googlegemini', '#a9c1ff')}Gemini</span></div>
 </div></div>
<div class="id panel"><div class="tp mono"><span class="g">● ACTIVO</span><span class="dim">ID-4D8E6B2</span></div>
 <div class="who"><div class="pic">🤖</div><div><div class="nm">Agente de Finanzas</div><div class="rl">miembro del equipo · Workspace</div></div></div>
 <div class="mail">{L.logo('gmail', '#ea4335')}<span class="mono"><span class="type" style="--n:25;--td:1.4s;animation-delay:{A(72.9)}">finanzas@agents.empresa</span></span></div>
 <div class="ok">✓ correo, calendario y Drive propios</div></div>""", sigue=True)

# ───────── 1:16 · Mistral Large 4
S = 76.2; A = L.at(S)
escena('e07-mistral', S, 89.0, f"""
.prev{{position:absolute;left:0;right:0;top:420px;text-align:center}}
.par{{position:absolute;left:70px;right:70px;top:540px;padding:40px;text-align:center;animation:pop .5s cubic-bezier(.22,1.3,.36,1) {A(79.8)} both}}
.par .v{{font-size:84px;font-weight:900;letter-spacing:-.03em;font-variant-numeric:tabular-nums}}
.par .u{{font-size:32px;font-weight:700;margin-top:6px}}.par .m{{font-size:24px;margin-top:16px}}
.gpu{{position:absolute;left:70px;right:70px;top:900px;padding:34px;animation:pop .5s cubic-bezier(.22,1.3,.36,1) {A(82.1)} both}}
.gpu .hd{{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:22px}}
.gpu .hd b{{font-size:66px;font-weight:900}}.gpu .hd span{{font-size:26px}}
canvas{{display:block;width:100%;border-radius:12px}}
.nv{{display:flex;align-items:center;gap:16px;margin-top:24px;font-size:30px;font-weight:800;opacity:0;animation:pop .45s ease {A(86.6)} both}}
.nv svg{{width:64px;height:64px}}
.ow{{position:absolute;left:0;right:0;top:1570px;text-align:center}}
""", f"""{L.entry(5, 'e51a7c0', L.logo('mistralai', '#fa520f'), 'Mistral AI')}
{L.steps([('Mistral <em style="color:#ff8a3d">Large 4</em>', 77.6, None)], S, top=290, size=96)}
<div class="prev"><span class="chip pop" style="animation-delay:{A(77.0)}">👀 vista previa</span></div>
<div class="par panel"><div class="v mono" id="pv">0</div><div class="u">un <span style="color:#ff8a3d">billón</span> de parámetros</div>
 <div class="m mono dim fade" style="animation-delay:{A(81.6)}">// MoE · ~49 mil millones activos por token</div></div>
<div class="gpu panel"><div class="hd"><b class="mono" id="gv">0</b><span class="dim">GPUs · clúster propio en Europa</span></div>
 <canvas id="cv" width="880" height="330"></canvas><div class="nv">{L.logo('nvidia', '#76b900')}NVIDIA Grace Blackwell</div></div>
<div class="ow"><span class="chip pop" style="animation-delay:{A(87.9)}">🔓 pesos abiertos el 27 oct</span></div>""",
f"""const cv=document.getElementById('cv'),x=cv.getContext('2d');
window.__seek=t=>{{t+={S};const e=p=>1-Math.pow(1-Math.min(1,Math.max(0,p)),3);
const pv=Math.round(1e12*e((t-80.1)/1.1));document.getElementById('pv').textContent=pv.toLocaleString('en-US');
const n=Math.round(3800*e((t-84.3)/1.8));document.getElementById('gv').textContent=n.toLocaleString('en-US');
x.clearRect(0,0,880,330);const cols=100,s=8.8;for(let i=0;i<3800;i++){{const c=i%cols,r=Math.floor(i/cols);
x.fillStyle=i<n?(i>n-120?'#d6ff9a':'#76b900'):'rgba(255,255,255,.07)';x.fillRect(c*s,r*8.7,s-2.4,6.4)}}}}""", sigue=True)

# ───────── 1:29 · Claude Haiku 5.5
S = 89.0; A = L.at(S)
escena('e08-haiku', S, 101.0, f"""
.mk{{position:absolute;left:50%;top:430px;width:220px;height:220px;margin-left:-110px;border-radius:56px;background:#d97757;display:flex;align-items:center;justify-content:center;
  box-shadow:0 0 0 4px rgba(217,119,87,.4),0 0 120px rgba(217,119,87,.55);animation:pop .55s cubic-bezier(.22,1.35,.36,1) {A(89.8)} both,spinIn 1s cubic-bezier(.22,1.2,.36,1) {A(92.4)} both}}
@keyframes spinIn{{from{{transform:rotate(-90deg) scale(.8)}}to{{transform:none}}}}
.tags{{position:absolute;left:0;right:0;top:860px;display:flex;justify-content:center;gap:18px}}
.vs{{position:absolute;left:70px;right:70px;top:1010px;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:20px}}
.mc{{padding:30px 24px;text-align:center}}.mc .n{{font-size:40px;font-weight:900}}.mc .d{{font-size:22px;margin-top:6px}}.mc .p{{font-size:46px;font-weight:900;margin-top:18px}}.mc .p small{{font-size:20px;font-weight:600;color:rgba(255,255,255,.5)}}
.old{{animation:pop .45s ease {A(96.9)} both,old .5s ease {A(98.4)} forwards}}@keyframes old{{to{{opacity:.38;filter:grayscale(1)}}}}
.old .p{{position:relative}}.old .p:after{{content:'';position:absolute;left:10%;right:10%;top:52%;height:5px;border-radius:3px;background:#ff5c5c;transform:scaleX(0);transform-origin:left;animation:strike .4s ease {A(98.6)} forwards}}
@keyframes strike{{to{{transform:scaleX(1)}}}}
.new{{box-shadow:inset 0 0 0 3px #d97757,0 0 60px rgba(217,119,87,.35);animation:pop .5s cubic-bezier(.22,1.4,.36,1) {A(97.4)} both}}
.arrow{{font-size:60px;color:#3dff9a;animation:fade .3s ease {A(97.2)} both}}
.cut{{position:absolute;left:0;right:0;top:1420px;text-align:center;animation:pop .5s cubic-bezier(.22,1.5,.36,1) {A(99.0)} both}}
.cut b{{display:inline-block;padding:18px 40px;border-radius:22px;background:#3dff9a;color:#04210f;font-size:56px;font-weight:900}}
.cut div{{margin-top:16px;font-size:24px}}
""", f"""{L.entry(6, '9f2c3d1', L.logo('anthropic'), 'Anthropic')}
{L.steps([('Claude <em style="color:#ffb38f">Haiku 5.5</em>', 92.4, None)], S, top=290, size=96)}
<div class="mk">{L.logo('claude', '#fff', 140)}</div>
<div class="tags"><span class="chip pop" style="animation-delay:{A(95.1)}">⚡ rápido</span><span class="chip pop" style="animation-delay:{A(95.7)}">💸 barato</span></div>
<div class="vs"><div class="mc panel old"><div class="n">Haiku 4.5</div><div class="d dim mono">oct 2025</div><div class="p">$1<small> /M</small></div></div>
 <div class="arrow">→</div>
 <div class="mc panel new"><div class="n" style="color:#ffb38f">Haiku 5.5</div><div class="d dim mono">oct 2026</div><div class="p">$0.10<small> /M</small></div></div></div>
<div class="cut"><b>−90%</b><div class="dim mono">// entrada, prompts de menos de 100k tokens</div></div>""", sigue=True)

# ───────── 1:41 · cierre (arriba queda la tarjeta «Sígueme»)
PIEZAS.append(('e09-cierre', 101.0, 105.6, L.cierre(ENTRADAS, 4.6)))

SIGUEME = ('seguir', 101.86, 110.36)  # copia de videos/5/demos/elementos/u09-seguir.webm

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
        ovs = [{'file': f'{pid}.webm', 'start': a, 'end': round(b, 2)} for pid, a, b, _ in PIEZAS]
        ovs.append({'file': f'{SIGUEME[0]}.webm', 'start': SIGUEME[1], 'end': SIGUEME[2]})
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2)
