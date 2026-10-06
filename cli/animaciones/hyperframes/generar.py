"""Genera los elementos HyperFrames de los 3 demos como WebM transparentes 1080x1920.

Cada elemento: bloque base + reemplazos de texto/CONFIG → render HyperFrames →
recorte automático de la zona con contenido (bbox del alfa) → se recoloca en un
lienzo vertical transparente en (x, y). Así los bloques horizontales conservan su
tamaño real de letra en el video vertical.
"""
import json, os, re, subprocess, sys

# proyecto HyperFrames de trabajo (npx hyperframes init) con los bloques agregados; ver README de animaciones
HF = os.environ.get('HF_PROYECTO', os.path.join(os.getcwd(), 'hf-proyecto'))
OUT = os.path.abspath(os.environ.get('SALIDA', os.getcwd()))
os.makedirs(OUT, exist_ok=True)
ENV = {**os.environ, 'HYPERFRAMES_SKIP_SKILLS': '1'}

def run(cmd, text=True, **kw):
    r = subprocess.run(cmd, capture_output=True, text=text, **kw)
    if r.returncode:
        sys.exit(f'falló: {" ".join(cmd[:4])}…\n{(r.stderr if text else r.stderr.decode(errors="replace"))[-1500:]}')
    return r

def config(s, key, value):
    """Reemplaza `key: <valor>,` dentro del objeto CONFIG del bloque."""
    s2, n = re.subn(rf'(\n\s*{key}:\s*)([^,\n]+)(,)', lambda m: m.group(1) + value + m.group(3), s, count=1)
    if n == 0: sys.exit(f'CONFIG.{key} no encontrado')
    return s2


TELEGRAM_ICON = ('<svg viewBox="0 0 36 36" fill="none"><rect width="36" height="36" rx="8" fill="#2AABEE"/>'
                 '<path d="M8 17.5l17.5-7c.8-.3 1.5.2 1.2 1.4l-3 14c-.2 1-.8 1.2-1.6.8l-4.4-3.3-2.1 2c-.2.2-.4.4-.9.4l.3-4.5 8.2-7.4c.4-.3-.1-.5-.6-.2l-10.1 6.4-4.4-1.4c-1-.3-1-1 .2-1.4z" fill="#fff"/></svg>')
AVATAR = ('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
          '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="%237c3aed"/>'
          '<stop offset="1" stop-color="%2306b6d4"/></linearGradient></defs><rect width="100" height="100" fill="url(%23g)"/>'
          '<text x="50" y="66" font-family="Helvetica,Arial" font-size="52" font-weight="700" fill="white" text-anchor="middle">A</text></svg>')
CAMERA_ICON = ('<svg viewBox="0 0 36 36" fill="none"><rect width="36" height="36" rx="8" fill="#7c3aed"/>'
               '<path d="M11 13h3.5l1.8-2.6h3.4l1.8 2.6H25a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H11a2 2 0 0 1-2-2v-9a2 2 0 0 1 2-2z" fill="#fff"/>'
               '<circle cx="18" cy="19.5" r="3.8" fill="#7c3aed"/></svg>')
EXTRA = {
    'instagram-follow': [('src="assets/avatar.jpg" alt="HeyGen"', f'src=\'{AVATAR}\' alt="Armando"')],
}

ELEMENTOS = {
    # Demo guionizado: cada elemento acompaña lo que se dice en ese momento.
    'e01-247':      ('lt-kicker-name', [('>QSTIFY · DEV<', '>MI HOMELAB<'), ('>ARMANDO<', '>24/7 · LINUX<')], {}, ('left', 1250)),
    'e02-cap-tt':   ('macos-notification', [(TELEGRAM_ICON, CAMERA_ICON), ('>HyperFrames<', '>Homelab<'), ('>Prompt to replace this title<', '>Captura · TikTok<'), ('__BODY__', 'Nueva captura de tu perfil lista para analizar')], {}, ('center', 170), 1.7),
    'e03-cap-ig':   ('macos-notification', [(TELEGRAM_ICON, CAMERA_ICON), ('>HyperFrames<', '>Homelab<'), ('>Prompt to replace this title<', '>Captura · Instagram<'), ('__BODY__', 'Nueva captura de tu perfil lista para analizar')], {}, ('center', 500), 1.7),
    'e04-prompt':   ('hw-text-cloud', [], {'text': '"Claude, analiza mis capturas y dame mis métricas"', 'x': '300', 'y': '200', 'w': '760', 'h': '360', 'fontSize': '54'}, ('center', 1180)),
    'e05-ciudad':   ('hw-title', [], {'text': '"la ciudad de métricas"'}, ('center', 1300)),
    'e06-edificios':('lt-soft-pill', [('>Dr. Maya Chen<', '>Un edificio por proyecto<'), ('>Host · Neuroscientist<', '>Apps · Redes sociales<')], {}, ('left', 1250)),
    'e07-encargo':  ('TEXTO:maquina', [], {'texto': '> encargo para Claude', 'duracion': '4.5'}, ('center', 1300)),
    'e08-tg-conf':  ('macos-notification', [('>HyperFrames<', '>Telegram<'), ('>Prompt to replace this title<', '>Claude entendió tu encargo · ¿Procedo?<'), ('__BODY__', 'Voy a crear la bitácora semanal del homelab. Responde ✅ para continuar')], {}, ('center', 170), 1.7),
    'e09-tg-fin':   ('macos-notification', [('>HyperFrames<', '>Telegram<'), ('>Prompt to replace this title<', '>✅ Encargo terminado<'), ('__BODY__', 'La bitácora semanal ya quedó guardada en Qstify')], {}, ('center', 170), 1.7),
    'e10-gratis':   ('TEXTO:resaltar', [], {'texto': 'Qstify es 100% gratis', 'resalta': '100% gratis', 'duracion': '3.6'}, ('center', 1280)),
    'e11-notas':    ('hw-title', [], {'text': '"todas las escribió Claude"'}, ('center', 1300)),
    'e12-subs':     ('lt-kicker-name', [('>QSTIFY · DEV<', '>SUSCRIPCIONES<'), ('>ARMANDO<', '>$100 VS $20<')], {}, ('left', 1250)),
    'e13-coment':   ('hw-text-cloud', [], {'text': '"¡déjame tu comentario!"', 'x': '400', 'y': '220', 'w': '620', 'h': '300', 'fontSize': '60'}, ('center', 380)),
    'e14-follow':   ('instagram-follow', [('>HeyGen<', '>Armando<'), ('>@heygen_official<', '>@arzival<'), ('>47.5K followers<', '>Homelab · Qstify<'), ('>Follow<', '>Seguir<'), ('<span>Following</span>', '<span>Siguiendo</span>')], {}, ('center', 1150)),
}


TEXTO_CLI = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'texto.ts')

def render_block(eid, block, repl, cfg, raw):
    src = open(f'{HF}/compositions/{block}.html').read()
    repl = list(repl) + EXTRA.get(block, [])
    for a, b in repl:
        if a not in src: sys.exit(f'{eid}: texto «{a}» no está en {block}')
        src = src.replace(a, b)
    for k, v in cfg.items():
        src = config(src, k, v)
    comp = f'compositions/_{eid}.html'
    open(f'{HF}/{comp}', 'w').write(src)
    run(['npx', '-y', 'hyperframes@latest', 'render', '-c', comp, '--format', 'webm', '-o', raw], cwd=HF, env=ENV)

solo = set(sys.argv[1:])
info = {}
if os.path.exists(f'{OUT}/info.json'):
    info = json.load(open(f'{OUT}/info.json'))
for eid, spec in ELEMENTOS.items():
    block, repl, cfg, (px, py) = spec[:4]
    zoom = spec[4] if len(spec) > 4 else 1.0
    if solo and eid not in solo:
        continue
    raw = f'{HF}/renders/_{eid}.webm'
    if block.startswith('TEXTO:'):
        args = ['node', TEXTO_CLI, '--estilo', block.split(':', 1)[1], '--out', raw]
        for k, v in cfg.items():
            args += [f'--{k}', str(v)]
        run(args)
    else:
        render_block(eid, block, repl, cfg, raw)
    # bbox del contenido = unión del alfa en todos los cuadros (a 1/4 de resolución)
    rw, rh = map(int, run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                           'stream=width,height', '-of', 'csv=p=0:s=x', raw]).stdout.strip().split('x')[:2])
    FW, FH = rw // 4, rh // 4
    raw_alpha = run(['ffmpeg', '-v', 'error', '-c:v', 'libvpx-vp9', '-i', raw, '-vf',
                     f'fps=15,alphaextract,scale={FW}:{FH}:flags=area', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                    text=False).stdout
    on = bytes(1 if v > 40 else 0 for v in range(256))
    x0, y0, x1, y1 = FW, FH, -1, -1
    for f in range(len(raw_alpha) // (FW * FH)):
        fr = raw_alpha[f * FW * FH:(f + 1) * FW * FH].translate(on)
        for r in range(FH):
            row = fr[r * FW:(r + 1) * FW]
            a = row.find(1)
            if a < 0: continue
            b = row.rfind(1)
            x0, x1, y0, y1 = min(x0, a), max(x1, b), min(y0, r), max(y1, r)
    if x1 < 0: sys.exit(f'{eid}: el render salió vacío')
    pad = 28  # margen para sombras y antialias
    x, y = max(0, x0 * 4 - pad), max(0, y0 * 4 - pad)
    w = min(rw - x, (x1 + 1) * 4 + pad - x)
    h = min(rh - y, (y1 + 1) * 4 + pad - y)
    w, h = w - w % 2, h - h % 2
    zw, zh = int(w * zoom) // 2 * 2, int(h * zoom) // 2 * 2
    if zw > 1080:
        sys.exit(f'{eid}: el contenido mide {zw}px de ancho, no cabe en vertical')
    dx = 60 if px == 'left' else (1080 - zw) // 2
    dy = min(py, 1920 - zh)
    out = f'{OUT}/{eid}.webm'
    run(['ffmpeg', '-v', 'error', '-y', '-c:v', 'libvpx-vp9', '-i', raw, '-vf',
         f'crop={w}:{h}:{x}:{y},scale={zw}:{zh}:flags=lanczos,format=yuva420p,pad=1080:1920:{dx}:{dy}:color=black@0.0',
         '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-b:v', '0', '-crf', '30', '-row-mt', '1', '-auto-alt-ref', '0', out])
    dur = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out]).stdout)
    info[eid] = {'dur': round(dur, 2), 'size': [zw, zh]}
    print(f'✔ {eid:14s} {block:22s} {zw}x{zh} → ({dx},{dy}) · {dur:.1f}s', flush=True)
json.dump(info, open(f'{OUT}/info.json', 'w'), indent=2)
