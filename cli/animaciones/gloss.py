"""Tema «gloss» (prueba): reviste ellog.py, tarjetas.py y escenas.py sin tocar los guiones.

Dirección: lienzo teñido por noticia + brillo radial arriba + forma de vidrio translúcida al fondo,
superficies de vidrio rellenas (no bordes de 1 px), píldoras sólidas y sans geométrica (Plus Jakarta).
Se quita la estética de terminal (cuadrícula, scanlines, mono, hashes de git).

Uso: python3 ejemplos/gloss-prueba.py ellog-02|video7 [ids…]   (mismas variables SALIDA/REL/SOLO_HTML)
"""
import os, re, types
import ellog as _ellog, tarjetas as _tarjetas, escenas as _escenas

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800'
         '&family=JetBrains+Mono:wght@500;700&display=block" rel="stylesheet">')
SANS = "'Plus Jakarta Sans',-apple-system,system-ui,sans-serif"

# paleta por noticia: (lienzo, lienzo2, acento, acento claro, rgb del acento, tinta sobre acento)
PALETAS = {
    0: ('#120c2a', '#07060f', '#a78bfa', '#e0d4ff', '167,139,250', '#160b33'),  # gancho / intro / cierre: violeta
    1: ('#2a0f0f', '#0e0606', '#ff8a6b', '#ffd2c2', '255,138,107', '#2a0c05'),  # Anthropic: granate + coral
    2: ('#0b1638', '#05070f', '#6ea8ff', '#d3e4ff', '110,168,255', '#06122e'),  # Nadella: azul profundo
    3: ('#141a08', '#070903', '#c6e64a', '#effac4', '198,230,74', '#1a2203'),   # Intel/AMD: lima
    4: ('#06202e', '#03090f', '#4fd2ff', '#cdf3ff', '79,210,255', '#032231'),   # Maia: azure
}

GLASS = """
.scene:before{content:'';position:absolute;left:50%;top:-520px;width:1500px;height:1200px;margin-left:-750px;border-radius:50%;pointer-events:none;
  background:radial-gradient(closest-side,rgba(var(--acr),.55),rgba(var(--acr),.14) 55%,transparent);filter:blur(30px);animation:breathe 6s ease-in-out infinite alternate}
.scene:after{content:'';position:absolute;right:-380px;bottom:-300px;width:1000px;height:1000px;border-radius:50%;pointer-events:none;opacity:.55;
  background:conic-gradient(from 200deg,transparent,rgba(var(--acr),.55),rgba(255,255,255,.35),rgba(var(--acr),.15),transparent 70%);
  -webkit-mask:radial-gradient(closest-side,transparent 58%,#000 60%,#000 74%,transparent 76%);filter:blur(2px);animation:spin 40s linear infinite}
@keyframes breathe{to{transform:translateY(60px) scale(1.08)}}
@keyframes spin{to{transform:rotate(360deg)}}
.scene>*{z-index:1}
"""

SURF = """
.panel,.glass{border-radius:44px;background:linear-gradient(180deg,rgba(255,255,255,.13),rgba(255,255,255,.04));
  -webkit-backdrop-filter:blur(28px) saturate(1.4);backdrop-filter:blur(28px) saturate(1.4);
  box-shadow:inset 0 1.5px 0 rgba(255,255,255,.28),inset 0 0 0 1.5px rgba(255,255,255,.07),0 40px 90px rgba(0,0,0,.45)}
.chip{display:inline-flex;align-items:center;gap:12px;padding:16px 28px;border-radius:999px;font-size:28px;font-weight:700;
  background:linear-gradient(180deg,rgba(255,255,255,.18),rgba(255,255,255,.07));-webkit-backdrop-filter:blur(20px);backdrop-filter:blur(20px);
  box-shadow:inset 0 1.5px 0 rgba(255,255,255,.3),0 14px 34px rgba(0,0,0,.3)}
"""


def _tint(s):
    """Lleva el verde de El Log (y su tinta oscura) al acento de la paleta."""
    s = s.replace('#3dff9a', 'var(--ac)').replace('rgba(61,255,154,', 'rgba(var(--acr),')
    for ink in ('#04210f', '#06210f', '#06210F'):
        s = s.replace(ink, 'var(--ink)')
    return s


def _vars(n):
    c1, c2, ac, ac2, acr, ink = PALETAS.get(n, PALETAS[0])
    return f'--c1:{c1};--c2:{c2};--ac:{ac};--ac2:{ac2};--acr:{acr};--ink:{ink}'


# ───────────────────────── El Log ─────────────────────────
L = types.ModuleType('ellog')
L.__dict__.update({k: v for k, v in _ellog.__dict__.items() if not k.startswith('__')})

L.BASE = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:transparent;font-family:""" + SANS + """;color:#fff;-webkit-font-smoothing:antialiased}
.scene{position:absolute;inset:0;overflow:hidden;background:radial-gradient(1300px 1100px at 50% 0%,var(--c1),var(--c2) 70%)}
.scene.in{animation:sIn .4s ease both}.scene.out{animation:sIn .4s ease both,sOut .4s ease var(--out) forwards}
@keyframes sIn{from{opacity:0;transform:scale(1.03)}to{opacity:1;transform:none}}
@keyframes sOut{to{opacity:0;transform:scale(.985)}}
""" + GLASS + SURF + """
.mono{font-family:""" + SANS + """;font-variant-numeric:tabular-nums;letter-spacing:0}
.g{color:var(--ac)}.dim{color:rgba(255,255,255,.55)}.red{color:#ff6b7a}
.pop{animation:pop .6s cubic-bezier(.22,1.35,.36,1) both}
@keyframes pop{from{opacity:0;transform:translateY(40px) scale(.9)}to{opacity:1;transform:none}}
.fade{animation:fade .45s ease both}@keyframes fade{from{opacity:0}to{opacity:1}}
.wipe{animation:wipe .6s cubic-bezier(.6,0,.2,1) both}@keyframes wipe{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}
.gone{animation:gone .35s ease forwards}@keyframes gone{to{opacity:0;transform:translateY(-40px) scale(.96);filter:blur(8px)}}
.type{display:inline-block;overflow:hidden;white-space:nowrap;vertical-align:bottom;font-family:'JetBrains Mono',monospace;animation:typ var(--td,1s) steps(var(--n,20)) both}
@keyframes typ{from{width:0}to{width:calc(var(--n,20) * 1ch)}}
.cur{display:inline-block;width:.5em;height:1em;border-radius:3px;background:var(--ac);vertical-align:-.12em;margin-left:4px;animation:blink 1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
/* encabezado: (01) Anthropic ·· progreso */
.entry{position:absolute;left:60px;right:60px;top:110px;display:flex;align-items:center;gap:18px;font-size:28px;font-weight:700}
.entry .num{width:76px;height:76px;border-radius:50%;background:linear-gradient(160deg,var(--ac2),var(--ac));color:var(--ink);display:flex;align-items:center;justify-content:center;
  font-size:30px;font-weight:800;box-shadow:inset 0 2px 0 rgba(255,255,255,.6),0 0 40px rgba(var(--acr),.55)}
.entry .co{padding:14px 28px 14px 18px;font-size:30px}.entry .co svg{width:42px;height:42px}
.entry .dots{margin-left:auto;display:flex;gap:10px}.entry .dots i{width:16px;height:16px;border-radius:8px;background:rgba(255,255,255,.18)}
.entry .dots i.on{width:46px;background:var(--ac);box-shadow:0 0 16px rgba(var(--acr),.7)}
.ttl{position:absolute;left:60px;right:60px;text-align:center;font-weight:800;letter-spacing:-.045em;line-height:1.02}
.ttl em{font-style:normal;background:linear-gradient(180deg,var(--ac2) 10%,var(--ac) 90%);-webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 0 30px rgba(var(--acr),.45))}
.ttl em.red{background:linear-gradient(180deg,#ffd0d5,#ff6b7a);-webkit-background-clip:text;background-clip:text}
@keyframes stIn{from{opacity:0;transform:translateY(30px) scale(.96);filter:blur(10px)}to{opacity:1;transform:none;filter:none}}
@keyframes stOut{to{opacity:0;transform:translateY(-30px);filter:blur(10px)}}
"""

L.FONTS = FONTS


def _page(css, body, dur, script='', salida=True):
    m = re.search(r'data-n="(\d+)"', body)
    n = int(m.group(1)) if m else 0
    body = re.sub(r'(>\s*)// ?', r'\1', body)  # fuera los «// comentario» de terminal
    cls = 'scene out' if salida else 'scene in'
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}
<style>{L.BASE}{_tint(css)}</style></head><body><div class="{cls}" style="--out:{dur - 0.4:.2f}s;{_vars(n)}">{_tint(body)}</div>
<script>{script}</script></body></html>"""


def _entry(num, sha, co_logo, co_name, t0=0.15):
    dots = ''.join(f'<i class="{"on" if k + 1 == num else ""}"></i>' for k in range(4))
    return (f'<div class="entry fade" data-n="{num}" style="animation-delay:{t0}s"><span class="num">{num:02d}</span>'
            f'<span class="chip co">{co_logo}{co_name}</span><span class="dots">{dots}</span></div>')


def _intro(semana, entradas, dur, salida=False):
    filas = ''.join(f'<div class="row glass pop" style="animation-delay:{1.7 + k * .2:.2f}s"><span class="n">{k + 1:02d}</span>{txt}</div>'
                    for k, (_, txt) in enumerate(entradas))
    css = """
.brand{position:absolute;left:0;right:0;top:300px;text-align:center;font-weight:800;font-size:230px;letter-spacing:-.07em;line-height:.9;
  animation:brand .7s cubic-bezier(.22,1.4,.36,1) .15s both}
.brand span{background:linear-gradient(180deg,#fff 20%,var(--ac2) 55%,var(--ac) 100%);-webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 20px 50px rgba(var(--acr),.55))}
@keyframes brand{from{opacity:0;transform:scale(.7) translateY(40px);filter:blur(14px)}to{opacity:1;transform:none;filter:none}}
.sem{position:absolute;left:0;right:0;top:560px;text-align:center;animation:pop .5s cubic-bezier(.22,1.35,.36,1) .7s both}
.sem .chip{font-size:30px}
.list{position:absolute;left:90px;right:90px;top:760px;display:grid;gap:20px}
.row{display:flex;align-items:center;gap:26px;padding:28px 34px;border-radius:999px;font-size:34px;font-weight:700}
.row .n{width:64px;height:64px;border-radius:50%;background:linear-gradient(160deg,var(--ac2),var(--ac));color:var(--ink);display:flex;align-items:center;justify-content:center;
  font-size:26px;font-weight:800;flex-shrink:0}
"""
    body = f"""<div class="brand"><span>El Log</span></div><div class="sem"><span class="chip">🗓️ {semana}</span></div><div class="list">{filas}</div>"""
    return _page(css, body, dur, salida=salida)


def _cierre(entradas, dur, pregunta='¿Cuál te sorprendió más?'):
    filas = ''.join(f'<div class="row glass pop" style="animation-delay:{.3 + k * .2:.2f}s"><span class="ck" style="--a:{PALETAS[k + 1][2]}">✓</span>{txt}</div>'
                    for k, (_, txt) in enumerate(entradas))
    css = """
.list{position:absolute;left:90px;right:90px;top:690px;display:grid;gap:18px}
.row{display:flex;align-items:center;gap:24px;padding:24px 32px;border-radius:999px;font-size:31px;font-weight:700}
.ck{width:54px;height:54px;border-radius:50%;background:var(--a);color:#111;display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:800;flex-shrink:0;
  box-shadow:inset 0 2px 0 rgba(255,255,255,.55),0 0 26px var(--a)}
.end{position:absolute;left:0;right:0;top:1330px;text-align:center}
.end .b{font-weight:800;font-size:150px;letter-spacing:-.07em;animation:pop .55s cubic-bezier(.22,1.35,.36,1) 1.6s both}
.end .b span{background:linear-gradient(180deg,#fff 20%,var(--ac2) 55%,var(--ac));-webkit-background-clip:text;background-clip:text;color:transparent}
.end .q{margin-top:22px;animation:pop .5s cubic-bezier(.22,1.35,.36,1) 2.3s both}.end .q .chip{font-size:36px}
"""
    body = f"""<div class="list">{filas}</div><div class="end"><div class="b"><span>El Log</span></div><div class="q"><span class="chip">💬 {pregunta}</span></div></div>"""
    return _page(css, body, dur)


L.page, L.entry, L.intro, L.cierre = _page, _entry, _intro, _cierre


# ───────────────────────── tarjetas (sobre la cámara) ─────────────────────────
T = types.ModuleType('tarjetas')
T.__dict__.update({k: v for k, v in _tarjetas.__dict__.items() if not k.startswith('__')})
T.BASE_CSS = _tarjetas.BASE_CSS.replace('font-family:Inter,', f'font-family:{SANS},') + """
.card{border-radius:40px;padding:30px;background:linear-gradient(170deg,rgba(58,58,72,.78),rgba(20,20,28,.82));
  -webkit-backdrop-filter:blur(30px) saturate(1.6);backdrop-filter:blur(30px) saturate(1.6);
  box-shadow:inset 0 1.5px 0 rgba(255,255,255,.3),inset 0 0 0 1.5px rgba(255,255,255,.08),0 30px 70px rgba(0,0,0,.5)}
.card:before{content:'';position:absolute;left:-60px;top:-80px;width:360px;height:260px;border-radius:50%;pointer-events:none;
  background:radial-gradient(closest-side,rgba(255,255,255,.16),transparent);filter:blur(10px)}
.ic{border-radius:50%;box-shadow:inset 0 2px 0 rgba(255,255,255,.35),0 8px 24px rgba(0,0,0,.35)}
.app{text-transform:none;letter-spacing:0;font-weight:700;font-size:23px;color:rgba(255,255,255,.62)}
.ti{font-weight:700;font-size:28px}
"""


def _tpage(css, body, dur, script=''):
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}
<style>{T.BASE_CSS}{css}.card{{position:relative}}</style></head><body>
<div class="wrap" style="--out:{dur - 0.45}s"><div class="card">{body}</div></div>
<script>{script}</script></body></html>"""


T.page = _tpage


# ───────────────────────── escenas a pantalla completa ─────────────────────────
E = types.ModuleType('escenas')
E.__dict__.update({k: v for k, v in _escenas.__dict__.items() if not k.startswith('__')})
E.BASE = _escenas.BASE.replace('font-family:Inter,', f'font-family:{SANS},') + """
.scene{--g1:#a78bfa;--g2:#5ac8fa;--acr:167,139,250;
  background:radial-gradient(1300px 1100px at 50% 0%,color-mix(in srgb,var(--g1) 22%,#07070d),#06060b 72%)}
.scene:before{content:'';position:absolute;left:50%;top:-520px;width:1500px;height:1200px;margin-left:-750px;border-radius:50%;opacity:1;pointer-events:none;mask-image:none;
  background:radial-gradient(closest-side,color-mix(in srgb,var(--g1) 60%,transparent),color-mix(in srgb,var(--g2) 18%,transparent) 55%,transparent);filter:blur(30px);
  animation:breathe 6s ease-in-out infinite alternate}
.scene:after{content:'';position:absolute;right:-380px;bottom:-300px;width:1000px;height:1000px;border-radius:50%;pointer-events:none;opacity:.5;
  background:conic-gradient(from 200deg,transparent,color-mix(in srgb,var(--g2) 60%,transparent),rgba(255,255,255,.35),color-mix(in srgb,var(--g1) 25%,transparent),transparent 70%);
  -webkit-mask:radial-gradient(closest-side,transparent 58%,#000 60%,#000 74%,transparent 76%);animation:spin 40s linear infinite}
@keyframes breathe{to{transform:translateY(60px) scale(1.08)}}
@keyframes spin{to{transform:rotate(360deg)}}
.scene>*{z-index:1}
.step{font-weight:800;letter-spacing:-.045em}
.step em{filter:drop-shadow(0 0 28px color-mix(in srgb,var(--g1) 50%,transparent))}
.phone{box-shadow:inset 0 0 0 12px #24252e,inset 0 0 0 14px #5a5d6c,0 0 0 2px rgba(255,255,255,.08),0 50px 120px rgba(0,0,0,.65),0 0 140px color-mix(in srgb,var(--g1) 30%,transparent)}
.node,.ps,.pl{background:linear-gradient(180deg,rgba(255,255,255,.14),rgba(255,255,255,.04)) !important;
  -webkit-backdrop-filter:blur(26px);backdrop-filter:blur(26px);box-shadow:inset 0 1.5px 0 rgba(255,255,255,.3),0 30px 70px rgba(0,0,0,.4) !important}
.node{border-radius:70px}.ps{border-radius:999px !important}
.ps:last-child{background:linear-gradient(180deg,rgba(48,209,88,.35),rgba(48,209,88,.12)) !important;box-shadow:inset 0 1.5px 0 rgba(255,255,255,.35),0 0 60px rgba(48,209,88,.35) !important}
.badge,.pocket{background:linear-gradient(180deg,#5ef08a,#22b552) !important;color:#062a12 !important;box-shadow:inset 0 2px 0 rgba(255,255,255,.5),0 20px 50px rgba(48,209,88,.35) !important}
"""


def _epage(css, body, dur, script=''):
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}
<style>{E.BASE}{css}</style></head><body><div class="scene" style="--out:{dur - 0.45}s">{body}</div>
<script>{script}</script></body></html>"""


E.page = _epage
