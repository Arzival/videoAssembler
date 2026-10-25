"""El Log #08 · edición «Escritorio»: la noticia de PHP2Shell contada dentro de LogOS, un sistema operativo retro inventado
(System 7 / Windows 98). Bloc de notas que teclea los titulares, diálogos de alerta que sacuden, terminal con un usuario
desconocido, ventanitas de sitios en cascada, barra de progreso que instala el parche y un cursor que hace clic.
Capas: 'mesa' (escritorio opaco con íconos, todo el video) → un capítulo transparente por noticia (sus ventanas se cierran
con los rectángulos de zoom mientras abren las del siguiente) → 'seguir' → 'barra' (menú + marquesina «última hora» = la cinta).
Tiempos = voz recortada de noticias/8 (97.46 s), los mismos de ellog-08-recorte.py.
Uso: SALIDA=~/Documents/Videos/noticias/8/escritorio REL=noticias/8/escritorio python3 ejemplos/ellog-08-escritorio.py [ids…]   (SOLO_HTML=1 para revisar)
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import escritorio as E
from escritorio import sprite, teclea, progreso, N, cursor, grafica, ap

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.path.expanduser('~/Documents/Videos/noticias/8/escritorio')))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
FIN = 97.46
TOP = 150                    # debajo de la barra de menú + marquesina
PIEZAS = []
# el botón solo se ve hundido durante el clic (la librería lo deja hundido antes por el relleno «both»)
CSS = ('.btn.pr{animation:pr .25s steps(1) var(--p) forwards}'
       # aparecer de golpe dentro de ventanas: opacidad a pasos (la visibilidad de E.ap ganaría a la ventana cerrada)
       '.op{opacity:0;animation:opn .01s steps(1) var(--d) forwards}.op.x{animation:opn .01s steps(1) var(--d) forwards,opf .01s steps(1) var(--x) forwards}'
       '@keyframes opn{to{opacity:1}}@keyframes opf{to{opacity:0}}')


def op(html, A, t, sale=None, extra=''):
    cls, st = 'op', f'--d:{A(t)};'
    if sale is not None:
        cls += ' x'; st += f'--x:{A(sale)};'
    return f'<div class="{cls}" style="{st}{extra}">{html}</div>'


E.SPR['papelera'] = ["   kkkkkkkkkk   ", "  kggggggggggk  ", " kkkkkkkkkkkkkk ", "  kwggwggwggwk  ", "  kwggwggwggwk  ", "  kwggwggwggwk  ",
                     "  kwggwggwggwk  ", "  kwggwggwggwk  ", "  kwggwggwggwk  ", "  kwggwggwggwk  ", "  kwggwggwggwk  ", "  kwggwggwggwk  ",
                     "  kkkkkkkkkkkk  ", "                ", "                ", "                "]
E.SPR['navegador'] = ["kkkkkkkkkkkkkkkk", "kbbbbbbbbbbbrgyk", "kkkkkkkkkkkkkkkk", "kwwwwwwwwwwwwwwk", "kwkkkkkkkkkkkkwk", "kwwwwwwwwwwwwwwk",
                      "kwssssssssswwwwk", "kwwwwwwwwwwwwwwk", "kwsssssssssssswk", "kwwwwwwwwwwwwwwk", "kwssssssswwwwwwk", "kwwwwwwwwwwwwwwk",
                      "kkkkkkkkkkkkkkkk", "                ", "                ", "                "]

# íconos del escritorio (abajo): las ventanas se abren desde ellos
ICX = {'Proyectos': 30, 'Servidor': 290, 'php.ini': 550, 'Papelera': 810}
ICY = 1690
DESDE = {k: (x + 95, ICY + 55) for k, x in ICX.items()}


def escena(pid, start, end, body, sigue=True):
    if sigue:
        end += E.COLA
    PIEZAS.append((pid, start, round(end, 2), E.page(CSS, body, round(end - start, 2), S0=start, transparente=True)))


def win(x, y, w, hz, titulo, cuerpo, A, t, sale=None, desde=None, **kw):
    """Ventana con rectángulos de zoom hacia una altura estimada hz (la ventana mide lo que su contenido)."""
    z = ''
    if desde:
        v = [[t - .2, 0, .2]] + ([[sale, 1, .2]] if sale is not None else [])
        z = f"<div class=\"zm\" data-z='{json.dumps({'o': [desde[0] - 30, desde[1] - 30, 60, 60], 'r': [x, y, w, hz], 'v': v})}'></div>"
    return z + E.ventana(x, y, w, titulo, cuerpo, A, t, sale=sale, **kw)


def dlg(x, y, w, hz, icono, texto, A, t, desde=None, sale=None, **kw):
    d = E.dialogo(x, y, w, icono, texto, A, t, sale=sale, **kw)
    if desde:
        v = [[t - .2, 0, .2]] + ([[sale, 1, .2]] if sale is not None else [])
        d = f"<div class=\"zm\" data-z='{json.dumps({'o': [desde[0] - 30, desde[1] - 30, 60, 60], 'r': [x, y, w, hz], 'v': v})}'></div>" + d
    return d


def bloque(lineas, A, t, ancho=930, maxs=104):
    """Titular tecleado en el Bloc de notas con tamaño que cabe en el ancho."""
    import re
    n = max(len(re.sub(r'[*_]|<[^>]+>', '', l)) for l in lineas)
    return E.grande(lineas, A, t, size=min(maxs, int(ancho / (.67 * n))))


def bloc(y, bloques, A, t, sale=None, desde=DESDE['php.ini'], nombre='alerta.txt', hz=420):
    cu = ''.join(f'<div style="margin-top:{14 if i else 0}px">{bloque(ls, A, tb)}</div>' for i, (ls, tb) in enumerate(bloques))
    return win(40, y, 1000, hz, f'{nombre} — Bloc de notas', cu, A, t, sale=sale, desde=desde, icono='archivo')


def fila(html, extra=''):
    return f'<div class="ps" style="font-size:34px;font-weight:600;padding:8px 0;display:flex;align-items:center;gap:18px;{extra}">{html}</div>'


# ───────── 0:00 · «Dicen que PHP está muerto…» → dos fallos críticos | ¿Laravel, WordPress o PHP? → te toca actualizar
S = 0.0; A = E.at(S); X1 = 5.0; X2 = 10.9
c0 = (bloc(TOP, [(['Dicen que PHP', 'está *muerto*…'], .3), (['Dos fallos', '_críticos_'], 1.8)], A, .15, sale=X1)
      + dlg(90, 700, 900, 300, 'error', 'Se detectaron <b>2 fallos críticos</b> en PHP.', A, 2.3, botones=('Ver detalles', 'Cerrar'),
            titulo='Alerta de seguridad', sacude=True, desde=(540, 470), sale=X1)
      + win(190, 1080, 700, 220, 'Detalles', '<div class="vt" style="font-size:52px;line-height:1.15">'
            + f'<div>{teclea("#  CVE-2026-<span style=color:#d8262a>109618</span>", A, 3.0, .55)}</div>'
            + f'<div>{teclea("#  CVE-2026-<span style=color:#d8262a>109619</span>", A, 3.6, .55)}</div></div>', A, 2.85, sale=X1, desde=(540, 900), icono='info')
      # fase 2
      + bloc(TOP, [(['¿Laravel, WordPress', 'o *PHP*?'], 5.25)], A, 5.1, sale=X2, nombre='pregunta.txt', hz=300)
      + win(60, 500, 960, 400, 'Mis proyectos', '<div style="display:flex;gap:40px;justify-content:space-around;padding:10px 0">'
            + op(f'<div style="text-align:center">{sprite("carpeta", 140)}<div class="ps" style="font-size:32px;font-weight:700">laravel/</div></div>', A, 6.6)
            + op(f'<div style="text-align:center">{sprite("carpeta", 140)}<div class="ps" style="font-size:32px;font-weight:700">wordpress/</div></div>', A, 7.2)
            + op(f'<div style="text-align:center">{sprite("archivo", 140)}<div class="ps" style="font-size:32px;font-weight:700">loquesea.php</div></div>', A, 8.8)
            + '</div>', A, 6.3, sale=X2, desde=DESDE['Proyectos'], icono='carpeta')
      + dlg(90, 1000, 900, 330, 'alerta', 'Tus proyectos usan PHP.<br><b>Te toca actualizar.</b>', A, 9.2, botones=('Actualizar ahora', 'Después'),
            pulsa=9.8, titulo='Actualización requerida', desde=(540, 850), sale=X2)
      + cursor([(8.0, 1000, 1600), (9.5, 330, 1255), (9.8, 330, 1255, True), (10.5, 1150, 1500)]))
escena('c0-alerta', S, 10.9, c0)

# ───────── 0:11 · se llama PHP2Shell · lo encontraron con IA
S = 10.9; A = E.at(S); X = 17.0
c1 = (bloc(TOP, [(['Lo llamaron', '_PHP2Shell_'], 11.0), (['Lo encontraron', 'con *IA*'], 14.7)], A, 10.95, sale=X, nombre='nombre.txt', hz=560)
      + win(110, 780, 860, 300, 'Propiedades de PHP2Shell', fila(sprite('error', 64) + '<b>PHP2Shell</b>') + fila('Tipo: <span style="font-weight:400">fallo de seguridad</span>')
            + fila('Gravedad: <span style="color:#d8262a">crítica</span>'), A, 13.6, sale=X, desde=DESDE['php.ini'], cu='gris', icono='info')
      + win(170, 1210, 740, 320, 'Buscador con IA', f'<div style="display:flex;gap:24px;align-items:center">{sprite("robot", 120)}<div style="flex:1">'
            + op(fila('Buscando fallos…'), A, 14.8, sale=15.6) + op(fila('<span style="color:#14a046">✓</span> PHP2Shell encontrado'), A, 15.6)
            + progreso([(0, 0), (14.8, 100, .8)], '#14a046') + '</div></div>', A, 14.75, sale=X, desde=DESDE['Servidor'], cu='gris', icono='robot'))
escena('c1-php2shell', S, 17.0, c1)

# ───────── 0:17 · PHP saca un parche hoy · dos fallos de 9.2 | del 0 al 10 → casi lo máximo
S = 17.0; A = E.at(S); X1 = 25.2; X2 = 32.85
VERS = '<div class="vt" style="font-size:46px;margin-top:6px">8.5.12 · 8.4.27 · 8.3.36 · 8.2.35</div>'
ESC = ''.join(f'<span style="width:72px;text-align:center">{i}</span>' for i in range(11))
c2 = (bloc(TOP, [(['PHP saca un', '_parche_ hoy'], 17.1), (['Dos fallos', 'de *9.2*'], 21.7)], A, 17.05, sale=X1, nombre='parche.txt', hz=560)
      + win(70, 790, 940, 260, 'Acerca de PHP', f'<div style="display:flex;gap:24px;align-items:flex-start">{sprite("info", 90)}<div style="flex:1">'
            + fila('<b>PHP</b> · versión de seguridad') + VERS + op(fila('✓ Corrige <b>2 fallos</b>', 'color:#14a046'), A, 21.7) + '</div></div>',
            A, 18.2, sale=X1, desde=DESDE['php.ini'], cu='gris', icono='info')
      + win(190, 1200, 700, 360, 'Calificación CVSS', '<div class="big" style="font-size:150px;color:#d8262a;text-align:center;line-height:1">'
            + N([(0, 0), (24.1, 9.2, 1.0)], f='1') + '<span style="font-size:60px;color:#0a0a0a"> / 10</span></div>' + progreso([(0, 0), (24.1, 92, 1.0)], '#d8262a'),
            A, 23.9, sale=X1, desde=(540, 1000), cu='gris', icono='alerta')
      # fase 2
      + bloc(TOP, [(['Del 0 al 10…'], 25.4), (['Casi lo', '*máximo*'], 30.1)], A, 25.3, sale=X2, nombre='escala.txt', hz=440)
      + win(40, 700, 1000, 360, 'Medidor de gravedad', f'<div class="vt" style="display:flex;justify-content:space-between;font-size:48px;margin-bottom:8px">{ESC}</div>'
            + progreso([(0, 0), (26.8, 8, .4), (27.1, 100, .7), (29.2, 92, .8)], '#d8262a')
            + '<div class="ps" style="display:flex;justify-content:space-between;font-size:30px;font-weight:700;margin-top:12px">'
            + op('<span style="color:#14a046">0 · nada grave</span>', A, 26.8) + op('<span style="color:#d8262a">10 · lo máximo</span>', A, 27.1) + '</div>'
            + op('<div class="big" style="font-size:80px;text-align:center;margin-top:10px">▲ <span class="rj">9.2</span></div>', A, 29.2),
            A, 26.5, sale=X2, desde=DESDE['Servidor'], cu='gris', icono='chip')
      + dlg(110, 1200, 860, 300, 'error', 'Gravedad: <b style="color:#d8262a">CRÍTICA (9.2)</b><br>Casi lo máximo.', A, 31.6, botones=('Entendido',),
            titulo='LogOS', sacude=True, desde=(540, 1000), sale=X2))
escena('c2-parche', S, 32.85, c2)

# ───────── 0:33 · ejecución remota de código → corre comandos en tu servidor | tu teclado a un desconocido
S = 32.85; A = E.at(S); X1 = 42.5; X2 = 45.4
TERM = (f'<div>{teclea("<span style=color:#ff5f5f>desconocido@tu-servidor</span>:~$ whoami", A, 39.4, .6)}</div>'
        f'<div>{teclea("www-data", A, 40.0, .3)}</div>'
        f'<div>{teclea("desconocido@tu-servidor:~$ ls /var/www", A, 40.9, .5)}</div>'
        f'<div>{teclea("desconocido@tu-servidor:~$ cat config.php", A, 41.6, .5)}</div><span class="car"></span>')
TECLAS = ''.join(f'<i style="display:inline-block;width:64px;height:58px;margin:4px;background:#c3c3c3;box-shadow:inset -3px -3px 0 #0a0a0a,inset 3px 3px 0 #fff"></i>' for _ in range(39))
c3 = (bloc(TOP, [(['Ejecución', '_remota_', 'de código'], 32.95)], A, 32.9, sale=X1, nombre='ataque.txt', hz=440)
      + dlg(90, 650, 900, 300, 'candado', 'Un <b>desconocido</b> puede ejecutar código<br><b>sin iniciar sesión.</b>', A, 36.6, botones=('Bloquear', 'Ignorar'),
            titulo='Conexión entrante', sacude=True, desde=(540, 500), sale=X1)
      + win(40, 1010, 1000, 520, 'Terminal — corre comandos en tu servidor', TERM, A, 38.0, sale=X1, desde=DESDE['Servidor'], cu='negro', icono='compu')
      + cursor([(38.3, 1120, 1300), (39.2, 760, 1180), (40.4, 420, 1290), (41.4, 840, 1380), (42.2, 600, 1420)])
      # fase 2
      + bloc(TOP, [(['Tu teclado a un', '_desconocido_'], 42.75)], A, 42.6, sale=X2, nombre='ojo.txt', hz=320)
      + win(60, 560, 960, 380, 'Teclado en pantalla', f'<div style="line-height:0;text-align:center">{TECLAS}</div>', A, 43.4, sale=X2, desde=DESDE['Proyectos'], cu='gris', icono='compu')
      + dlg(90, 1020, 900, 320, 'error', '<b>Control remoto activo:</b><br>alguien más está usando tu teclado.', A, 44.2, botones=('¡Desconectar!',),
            titulo='LogOS', sacude=True, desde=(540, 900), sale=X2))
escena('c3-remoto', S, 45.4, c3)

# ───────── 0:45 · no es cualquier cosa · millones de sitios · sitios en alerta | Hacker News: Países Bajos (sin confirmar)
S = 45.4; A = E.at(S); X1 = 52.8; X2 = 63.5
MINI = ''
for i in range(12):
    c, r = i % 3, i // 3
    t0 = 47.3 + i * .14
    mal = (i * 5) % 3 == 0
    MINI += win(50 + c * 330 + (r % 2) * 18, 640 + r * 230, 320, 210, f'sitio-{i + 1}.com',
                '<div style="height:16px;background:#ddd;margin-bottom:10px"></div><div style="height:16px;width:70%;background:#ddd"></div>'
                + (op(f'<div style="position:absolute;right:14px;top:14px">{sprite("error", 64)}</div>', A, 50.2 + (i % 5) * .2) if mal else ''),
                A, t0, sale=X1, z=20 + i, icono='mundo')
c4 = (bloc(TOP, [(['No es cualquier *cosa*'], 45.5), (['_Millones_ de sitios'], 47.0), (['Sitios en *alerta*'], 49.9)], A, 45.45, sale=X1, nombre='alcance.txt', hz=440)
      + MINI
      + dlg(150, 1590, 780, 200, 'info', '«Sitios en alerta», dicen los medios.', A, 51.5, titulo='Noticias', sale=X1, z=60)
      # fase 2
      + win(40, TOP, 1000, 640, 'Hacker News — news.ycombinator.com', '<div style="background:#ff6600;color:#fff;font-weight:700;font-size:32px;padding:8px 14px;margin:-24px -28px 22px">Y  Hacker News</div>'
            + '<div class="ps" style="font-size:52px;line-height:1.2;font-weight:600">«' + teclea('El centro de ciberseguridad', A, 55.6, .5)
            + ' ' + teclea('de <b>Países Bajos</b>', A, 57.1, .4) + ' ' + teclea('quedó fuera de línea', A, 58.3, .45) + ' ' + teclea('por usar PHP»', A, 59.1, .4) + '</div>',
            A, 53.0, sale=X2, desde=DESDE['Proyectos'], icono='navegador', t1='#c94f00', t2='#ff8a3d')
      + bloc(860, [(['Ojo: aún', '_sin confirmar_'], 60.0)], A, 59.9, sale=X2, nombre='ojo.txt', hz=320)
      + dlg(110, 1270, 860, 300, 'alerta', 'Este dato <b>aún no está confirmado.</b>', A, 60.2, botones=('Entendido',), titulo='Sin confirmar', sacude=True,
            desde=(540, 1100), sale=X2))
escena('c4-sitios', S, 63.5, c4)

# ───────── 1:03 · PHP no es malo · la IA ya encuentra fallos · saldrán más seguido | no lo dejes para después
S = 63.5; A = E.at(S); X1 = 73.1; X2 = 76.6
ARCH = ['index.php', 'login.php', 'upload.php', 'config.php', 'api.php']
FL = {2: 69.2, 3: 70.1}
FILAS = ''.join(f'<div class="ps" style="position:relative;display:flex;align-items:center;gap:18px;font-size:34px;font-weight:600;padding:6px 10px">'
                f'{sprite("archivo", 48)}<span class="sl" style="--s:{A(67.9 + i * .3)};padding:0 8px">{n}</span>'
                + (op(f'<span style="margin-left:auto;display:flex;gap:10px;align-items:center;color:#d8262a">{sprite("error", 44)}fallo</span>', A, FL[i]) if i in FL else '')
                + '</div>' for i, n in enumerate(ARCH))
c5 = (bloc(TOP, [(['PHP no es *malo*'], 63.6), (['La IA ya encuentra', '_fallos_'], 67.4), (['Saldrán más *seguido*'], 71.1)], A, 63.55, sale=X1, nombre='ia.txt', hz=500)
      + win(40, 720, 1000, 470, 'Buscador de fallos con IA', f'<div style="display:flex;gap:20px"><div>{sprite("robot", 110)}{sprite("lupa", 110)}</div><div style="flex:1">{FILAS}</div></div>',
            A, 67.6, sale=X1, desde=DESDE['Servidor'], icono='lupa')
      + win(240, 1260, 600, 340, 'Reportes de fallos', grafica(560, 230, [(0, 15), (72.3, 90, 1.4)], '#ffd400', 5), A, 72.0, sale=X1, desde=(540, 1100), cu='negro', icono='chip')
      # fase 2
      + bloc(TOP, [(['No lo dejes', 'para *después*'], 73.3)], A, 73.2, sale=X2, nombre='pendiente.txt', hz=320)
      + dlg(90, 620, 900, 320, 'reloj', 'Recordatorio:<br><b>actualizar PHP</b>', A, 74.6, botones=('Ahora', 'Más tarde'), pulsa=75.9, titulo='Recordatorio',
            desde=DESDE['php.ini'], sale=X2)
      + cursor([(74.8, 1000, 1500), (75.7, 330, 860), (75.9, 330, 860, True), (76.5, 700, 1300)]))
escena('c5-ia', S, 76.6, c5)

# ───────── 1:17 · ¿qué versión tienes? · corre php -v · ya con el parche (versiones por rama) | PHP no está muerto · hoy lo actualizamos
S = 76.6; A = E.at(S); X1 = 86.0; X2 = 91.1
RAMAS = [('8.5', '8.5.12', 83.2), ('8.4', '8.4.27', 83.5), ('8.3', '8.3.36', 83.8), ('8.2', '8.2.35', 84.1)]
UPD = ''.join(op(fila(f'<span class="vt" style="font-size:44px">rama {r}</span> → <b>{v}</b> <span style="color:#14a046">✓</span>'), A, t) for r, v, t in RAMAS)
c6 = (bloc(TOP, [(['¿Qué versión *tienes*?'], 76.7), (['Corre _php -v_'], 79.6), (['Ya con el _parche_'], 83.2)], A, 76.65, sale=X1, nombre='version.txt', hz=420)
      + win(40, 600, 1000, 300, 'Terminal', f'<div>{teclea("$ php -v", A, 79.9, .35)}</div><div>{teclea("PHP 8.4.<span style=color:#ffd400>27</span> (cli)", A, 80.6, .4)}</div>'
            + f'<div style="color:#8a8579">{teclea("# compárala con la última de tu rama", A, 81.8, .9)}</div>', A, 79.7, sale=X1, desde=DESDE['Servidor'], cu='negro', icono='compu')
      + win(90, 980, 900, 520, 'Actualizaciones disponibles', UPD + op('<div class="vt" style="margin:10px 0 8px">Instalando php-8.4.27… ' + N([(0, 0), (84.4, 100, 1.4)], suf=' %') + '</div>'
            + progreso([(0, 0), (84.4, 100, 1.4)]), A, 84.3), A, 83.05, sale=X1, desde=DESDE['php.ini'], cu='gris', icono='info')
      # fase 2
      + bloc(TOP, [(['PHP no está', '*muerto*'], 86.2), (['Tan vivo que hoy', 'lo _actualizamos_'], 88.3)], A, 86.1, sale=X2, nombre='vivo.txt', hz=520)
      + dlg(90, 760, 900, 340, 'papelera', '¿Seguro que quieres mover<br><b>PHP</b> a la Papelera?', A, 86.5, botones=('Cancelar', 'Mover'), pulsa=87.2,
            titulo='Papelera', desde=DESDE['Papelera'], sale=88.2)
      + dlg(140, 1180, 800, 280, 'info', '<b>PHP 8.4.27</b> instalado <span style="color:#14a046">✓</span>', A, 89.8, titulo='LogOS', desde=DESDE['php.ini'], sale=X2)
      + cursor([(86.6, 1050, 1500), (87.0, 330, 1010), (87.2, 330, 1010, True), (87.9, 760, 1350), (91.0, 1150, 1500)]))
escena('c6-version', S, 91.1, c6)

# ───────── 1:31 · cierre: encuesta ¿cada cuánto actualizas tu servidor? (abajo entra «Sígueme»)
S = 91.1; A = E.at(S)
OPC = ''.join(op(f'<div class="ps" style="display:flex;align-items:center;gap:20px;font-size:40px;font-weight:700;padding:14px 6px">'
                 f'<i style="width:44px;height:44px;border-radius:50%;background:#fff;box-shadow:inset 3px 3px 0 #828282,inset -3px -3px 0 #fff,inset 5px 5px 0 #0a0a0a"></i>{o}</div>', A, t)
              for o, t in [('📅 Siempre al día', 92.1), ('🔥 Cuando algo truena', 92.9)])
c7 = win(40, TOP, 1000, 560, 'Encuesta — El Log', bloque(['¿Cada cuánto actualizas', 'tu *servidor*?'], A, 91.2, ancho=920) + f'<div style="margin-top:20px">{OPC}</div>',
         A, 91.15, desde=DESDE['Servidor'], icono='info')
escena('c7-cierre', S, FIN, c7, sigue=False)

# ───────── «Sígueme»: perfil con botón que el cursor pulsa + comentario tecleado
SEG_INI = 93.9
S = SEG_INI; A = E.at(S)
PERFIL = (f'<div style="display:flex;gap:26px;align-items:center">{sprite("compu", 120)}<div><div class="big" style="font-size:72px">Armando</div>'
          f'<div class="ps" style="font-size:32px;font-weight:600">El Log · cada semana</div></div></div>'
          f'<div style="margin-top:22px;display:flex;justify-content:center"><span class="btn def pr" style="--p:{A(94.8)};min-width:340px;font-size:38px">'
          f'{op("Seguir", A, 0, sale=94.85, extra="display:inline")}{op("Siguiendo ✓", A, 94.85, extra="display:inline;color:#14a046")}</span></div>')
COMENT = (f'<div class="ps" style="font-size:36px;font-weight:700">🛠️ ¿Cada cuánto actualizas?</div>'
          f'<div class="vt" style="font-size:50px;margin-top:10px;color:#0a1f8f">› {teclea("Cada semana, ya aprendí 😅", A, 95.3, .9)}</div>')
SEG = (win(140, 760, 800, 330, 'Perfil — Armando', PERFIL, A, 94.0, desde=(540, 1500), cu='gris', icono='compu', z=50)
       + win(90, 1150, 900, 240, 'Comentarios', COMENT, A, 94.5, desde=(540, 1500), icono='archivo', z=51)
       + cursor([(94.0, 1100, 1550), (94.6, 560, 1020), (94.8, 560, 1020, True), (95.6, 900, 1450)]))
PIEZAS.append(('seguir', SEG_INI, FIN, E.page(CSS, SEG, round(FIN - SEG_INI, 2), S0=SEG_INI, transparente=True)))

# ───────── mesa: escritorio opaco con los íconos (todo el video, hasta abajo)
A = E.at(0)
MESA = ''.join(E.icono(x, ICY, spr, nm, A, 0) for nm, x, spr in [('Proyectos', ICX['Proyectos'], 'carpeta'), ('Servidor', ICX['Servidor'], 'servidor'),
                                                                     ('php.ini', ICX['php.ini'], 'archivo'), ('Papelera', ICX['Papelera'], 'papelera')])
PIEZAS.insert(0, ('mesa', 0.0, FIN, E.page('', MESA, FIN, S0=0.0, mesa='noche', menu=False)))

# ───────── barra de menú + marquesina «última hora» (la cinta de El Log) + capítulo actual — encima de todo
CORRIDO = ['PHP 8.5.12, 8.4.27, 8.3.36 y 8.2.35 corrigen los dos fallos', 'CVE-2026-109618 y CVE-2026-109619: 9.2 de 10',
           'Ejecución de código sin iniciar sesión', 'Parche de emergencia: salió un día antes por una filtración',
           'Los encontraron investigadores de Calif, Wiz y OpenAI', 'Hacker News: lo de Países Bajos aún no está confirmado', 'Revisa tu versión: php -v']
CAPS = [(0.0, 'Alerta'), (10.9, 'PHP2Shell'), (17.0, 'El parche'), (32.85, 'Ejecución remota'), (45.4, 'Sitios en alerta'), (63.5, 'La IA'),
        (76.6, 'Tu versión'), (91.1, 'Tu opinión')]
CAPH = ''.join(ap(f'{i + 1:02d}/08 · {n}', A, t, sale=CAPS[i + 1][0] if i + 1 < len(CAPS) else None,
                  extra='position:absolute;right:0;top:0;white-space:nowrap;background:#0a1f8f;color:#fff;padding:0 12px')
               for i, (t, n) in enumerate(CAPS))
TICK = ''.join(f'<span>⚠ {c}</span>' for c in CORRIDO)
BARRA = (f'<div class="barra"><span class="lg">{sprite("compu", 40)}LogOS</span><span style="font-weight:500">Archivo</span><span style="font-weight:500">Edición</span>'
         f'<span style="margin-left:auto;position:relative;width:440px;height:40px;font-size:26px">{CAPH}</span>'
         f'<span class="hr" style="margin-left:18px">21:42</span></div>'
         f'<div class="mq" style="top:64px"><span class="tg">⚠ ÚLTIMA HORA</span><div class="mv">{TICK}{TICK}</div></div>')
PIEZAS.append(('barra', 0.0, FIN, E.page('', BARRA, FIN, S0=0.0, transparente=True)))
PRE = 'elle8-'

if __name__ == '__main__':
    solo = set(sys.argv[1:])
    for pid, a, b, html in PIEZAS:
        if solo and pid not in solo:
            continue
        path = f'{WORK}/{pid}.html'
        open(path, 'w').write(html)
        if os.environ.get('SOLO_HTML'):
            print('html', path, f'{b - a:.2f}'); continue
        r = subprocess.run(['node', CAP, path, f'{b - a:.2f}', f'{OUT}/{PRE}{pid}.webm'], capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr[-600:], flush=True)
    if not solo:
        rel = os.environ.get('REL', 'noticias/8/escritorio')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
