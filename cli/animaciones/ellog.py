"""El Log — sección semanal de noticias. Identidad visual reutilizable: cada noticia es una
entrada de `git log` (hash + número), estética de terminal oscura con acento verde.

Las escenas son a pantalla completa y opacas (las protagonistas); los clips solo asoman
en momentos puntuales. Este módulo da el estilo base, los logos y las piezas fijas de cada
semana (intro, encabezado de entrada, cierre); el contenido de cada semana vive en
ejemplos/ellog-NN.py.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
VERDE = '#3dff9a'

BASE = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:transparent;font-family:Inter,-apple-system,system-ui,sans-serif;color:#fff;-webkit-font-smoothing:antialiased}
.scene{position:absolute;inset:0;overflow:hidden;background:radial-gradient(1100px 800px at 50% 18%,#10261d 0%,#0a1210 45%,#050706 100%)}
.scene.in{animation:sIn .4s ease both}.scene.out{animation:sIn .4s ease both,sOut .4s ease var(--out) forwards}
.scene:before{content:'';position:absolute;inset:0;opacity:.5;pointer-events:none;
  background-image:linear-gradient(rgba(61,255,154,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(61,255,154,.045) 1px,transparent 1px);
  background-size:54px 54px;mask-image:radial-gradient(circle at 50% 35%,#000 25%,transparent 78%)}
.scene:after{content:'';position:absolute;inset:0;pointer-events:none;background:repeating-linear-gradient(0deg,rgba(0,0,0,.18) 0 2px,transparent 2px 4px);opacity:.35}
@keyframes sIn{from{opacity:0;transform:scale(1.03)}to{opacity:1;transform:none}}
@keyframes sOut{to{opacity:0;transform:scale(.985)}}
.mono{font-family:'JetBrains Mono',ui-monospace,Menlo,monospace}
.g{color:#3dff9a}.dim{color:rgba(255,255,255,.45)}.red{color:#ff5c5c}
.pop{animation:pop .55s cubic-bezier(.22,1.35,.36,1) both}
@keyframes pop{from{opacity:0;transform:translateY(34px) scale(.9)}to{opacity:1;transform:none}}
.fade{animation:fade .45s ease both}@keyframes fade{from{opacity:0}to{opacity:1}}
.wipe{animation:wipe .6s cubic-bezier(.6,0,.2,1) both}@keyframes wipe{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}
.gone{animation:gone .35s ease forwards}@keyframes gone{to{opacity:0;transform:translateY(-40px) scale(.96);filter:blur(6px)}}
.type{display:inline-block;overflow:hidden;white-space:nowrap;vertical-align:bottom;animation:typ var(--td,1s) steps(var(--n,20)) both}
@keyframes typ{from{width:0}to{width:calc(var(--n,20) * 1ch)}}
.cur{display:inline-block;width:.55em;height:1em;background:#3dff9a;vertical-align:-.12em;margin-left:4px;animation:blink 1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
/* encabezado de entrada: ● #01  a1f3c9e  OpenAI */
.entry{position:absolute;left:70px;right:70px;top:120px;display:flex;align-items:center;gap:20px;font-size:28px;
  padding-bottom:24px;border-bottom:2px solid rgba(61,255,154,.18)}
.entry .dot{width:18px;height:18px;border-radius:50%;background:#3dff9a;box-shadow:0 0 18px #3dff9a}
.entry .co{margin-left:auto;display:flex;align-items:center;gap:14px;font-family:Inter;font-weight:700;font-size:30px}
.entry .co svg{width:44px;height:44px}
.ttl{position:absolute;left:60px;right:60px;text-align:center;font-weight:900;letter-spacing:-.035em;line-height:1.02}
.ttl em{font-style:normal;color:#3dff9a}
.chip{display:inline-flex;align-items:center;gap:12px;padding:14px 24px;border-radius:16px;background:rgba(255,255,255,.07);
  box-shadow:inset 0 0 0 2px rgba(255,255,255,.12);font-size:28px;font-weight:700}
.panel{border-radius:30px;background:rgba(14,22,19,.92);box-shadow:inset 0 0 0 2px rgba(61,255,154,.16),0 30px 80px rgba(0,0,0,.55)}
@keyframes stIn{from{opacity:0;transform:translateY(26px);filter:blur(8px)}to{opacity:1;transform:none;filter:none}}
@keyframes stOut{to{opacity:0;transform:translateY(-26px);filter:blur(8px)}}
"""

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900'
         '&family=JetBrains+Mono:wght@400;600;800&display=block" rel="stylesheet">')


def page(css, body, dur, script='', salida=True):
    """salida=False cuando la escena siguiente empieza justo encima (sin hueco al clip)."""
    cls = 'scene out' if salida else 'scene in'
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}
<style>{BASE}{css}</style></head><body><div class="{cls}" style="--out:{dur - 0.4:.2f}s">{body}</div>
<script>{script}</script></body></html>"""


def logo(name, color='#fff', size=None):
    """Logo de Simple Icons (CC0) en logos/<name>.svg, recoloreado."""
    svg = open(os.path.join(HERE, 'logos', f'{name}.svg')).read()
    d = re.search(r' d="([^"]+)"', svg).group(1)
    st = f' style="width:{size}px;height:{size}px"' if size else ''
    return f'<svg viewBox="0 0 24 24"{st}><path fill="{color}" d="{d}"/></svg>'


def at(start):
    """Devuelve un helper que convierte segundos del video final en delay local de la escena."""
    return lambda t: f'{max(0.0, t - start):.2f}s'


def steps(items, start, cls='ttl', top=300, size=78):
    """Titulares que se reemplazan: [(html, t_entra, t_sale|None), …] en segundos del video final."""
    out = []
    for html, a, b in items:
        anim = f'stIn .45s cubic-bezier(.22,1.2,.36,1) {a - start:.2f}s both' + (f',stOut .3s ease {b - start:.2f}s forwards' if b else '')
        out.append(f'<div class="{cls}" style="top:{top}px;font-size:{size}px;opacity:0;animation:{anim}">{html}</div>')
    return ''.join(out)


def entry(num, sha, co_logo, co_name, t0=0.15):
    return (f'<div class="entry mono fade" style="animation-delay:{t0}s"><span class="dot"></span><span class="g">#{num:02d}</span>'
            f'<span class="dim">{sha}</span><span class="co">{co_logo}{co_name}</span></div>')


# ───────────── piezas fijas de cada semana ─────────────

def intro(semana, entradas, dur, salida=False):
    """Terminal: `git log` → logo EL LOG → índice de la semana. entradas = [(sha, texto), …]"""
    filas = ''.join(f'<div class="row pop" style="animation-delay:{2.2 + k * .22:.2f}s"><span class="g">{sha}</span> {txt}</div>'
                    for k, (sha, txt) in enumerate(entradas))
    css = """
.term{position:absolute;left:70px;right:70px;top:420px;padding:40px 44px;animation:pop .5s cubic-bezier(.22,1.3,.36,1) both}
.term .bar{display:flex;gap:12px;margin-bottom:30px}.term .bar i{width:18px;height:18px;border-radius:50%;background:#ff5f57}
.term .bar i:nth-child(2){background:#febc2e}.term .bar i:nth-child(3){background:#28c840}
.cmd{font-size:34px}
.brand{margin:44px 0 10px;font-family:Inter;font-weight:900;font-size:150px;letter-spacing:-.05em;line-height:.9;animation:brand .6s cubic-bezier(.22,1.4,.36,1) 1.0s both}
.brand b{color:#3dff9a;text-shadow:0 0 50px rgba(61,255,154,.55)}
@keyframes brand{from{opacity:0;transform:scale(.7);filter:blur(10px)}to{opacity:1;transform:none;filter:none}}
.sem{font-size:28px;margin-bottom:34px;animation:fade .4s ease 1.6s both}
.row{font-size:29px;padding:13px 0;border-top:1.5px solid rgba(255,255,255,.07)}
"""
    body = f"""<div class="term panel mono"><div class="bar"><i></i><i></i><i></i></div>
<div class="cmd"><span class="g">$</span> <span class="type" style="--n:21;--td:.8s;animation-delay:.2s">git log --esta-semana</span></div>
<div class="brand">EL <b>LOG</b></div><div class="sem dim">// {semana}</div>{filas}</div>"""
    return page(css, body, dur, salida=salida)


def cierre(entradas, dur, pregunta='¿Cuál te sorprendió más?'):
    """Resumen final (deja libre la parte de arriba para la tarjeta «Sígueme»)."""
    filas = ''.join(f'<div class="row pop" style="animation-delay:{.3 + k * .2:.2f}s"><span class="ck">✓</span><span class="g">{sha}</span> {txt}</div>'
                    for k, (sha, txt) in enumerate(entradas))
    css = """
.term{position:absolute;left:70px;right:70px;top:690px;padding:36px 44px}
.cmd{font-size:30px;margin-bottom:18px}
.row{font-size:28px;padding:12px 0;border-top:1.5px solid rgba(255,255,255,.07);display:flex;gap:16px;align-items:center}
.ck{color:#06210f;background:#3dff9a;border-radius:50%;width:34px;height:34px;display:inline-flex;align-items:center;justify-content:center;font-size:20px;font-weight:900;flex-shrink:0}
.end{position:absolute;left:0;right:0;top:1390px;text-align:center}
.end .b{font-weight:900;font-size:96px;letter-spacing:-.05em;animation:pop .55s cubic-bezier(.22,1.35,.36,1) 1.8s both}.end .b b{color:#3dff9a}
.end .q{margin-top:18px;font-size:36px;font-weight:700;animation:pop .5s cubic-bezier(.22,1.35,.36,1) 2.5s both}
"""
    body = f"""<div class="term panel mono pop"><div class="cmd"><span class="g">$</span> git log --oneline <span class="dim">#{len(entradas)} esta semana</span></div>{filas}</div>
<div class="end"><div class="b">EL <b>LOG</b></div><div class="q">{pregunta} 💬</div></div>"""
    return page(css, body, dur)
