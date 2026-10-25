"""El Log #08 · edición «Recorte» (nueva, sin la base gloss): primera plana de última hora hecha de papel.
Titulares que golpean palabra por palabra, tachones, marcatextos, sellos de goma, tickets de terminal y recortes con cinta;
la hoja de cada capítulo entra rasgada sobre la anterior y todo se mueve a 12 cps. Arriba, cabecera de periódico con
cintillo rojo de «última hora» que corre los datos (la cinta de El Log de esta edición).
Tiempos = voz recortada de noticias/8 (97.46 s), los mismos de ellog-08-trayecto.py.
Uso: SALIDA=~/Documents/Videos/noticias/8/recorte REL=noticias/8/recorte python3 ejemplos/ellog-08-recorte.py [ids…]   (SOLO_HTML=1 para revisar)
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import recorte as K
from recorte import titular, tacha, subraya, circulo, flecha, recorte, nota, sello, ticket, numero, N, logo, mano, fase, palomita, marca

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.getcwd()))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
FIN = 97.46
TOP = 330          # primer renglón útil (debajo de la cabecera)
PIEZAS = []


def escena(pid, start, end, body, fondo='papel', css='', ac='var(--rojo)', sigue=True, seed=1):
    if sigue:
        end += K.COLA
    PIEZAS.append((pid, start, end, K.page(css, body, round(end - start, 2), S0=start, fondo=fondo, seed=seed, ac=ac)))


def caja(txt, size=96, extra=''):
    return f'<div style="font-weight:900;font-stretch:62%;font-size:{size}px;line-height:.88;text-transform:uppercase;{extra}">{txt}</div>'


def ser(txt, size=48, extra=''):
    return f'<div class="ser" style="font-size:{size}px;line-height:1.05;{extra}">{txt}</div>'


# ───────── 0:00 · «Dicen que PHP está muerto…» → dos fallos críticos | ¿Laravel, WordPress o PHP? → te toca actualizar
S = 0.0; A = K.at(S)
f1 = (titular(['Dicen que PHP', 'está muerto…'], A, .3, x=5.0, top=TOP, size=150, seed=2)
      + tacha(70, TOP + 205, 690, A, 1.5, grosor=16)
      + titular(['Dos fallos', '_críticos_'], A, 1.8, x=5.0, top=690, size=210, seed=3)
      + sello(590, 1130, 'Urgente', A, 2.5, size=96, rot=-9)
      + ticket(80, 1330, 620, [('<i>#</i> CVE-2026-<b>109618</b>', 3.0, .55), ('<i>#</i> CVE-2026-<b>109619</b>', 3.6, .55)], A, rot=-2)
      + logo('php', 760, 1330, 230, A, 2.2, rot=10, bg='#7a86e0', color='#fff'))
f2 = (titular(['¿Laravel,', 'WordPress', 'o *PHP*?'], A, 5.2, top=TOP, size=150, seed=4)
      + logo('laravel', 110, 830, 250, A, 6.6, rot=-8, bg='#ff2d20', color='#fff')
      + logo('wordpress', 415, 880, 250, A, 7.2, rot=6, bg='#21759b', color='#fff')
      + logo('php', 720, 830, 250, A, 8.8, rot=-4, bg='#7a86e0', color='#fff')
      + mano(150, 1110, 'o cualquier cosa en PHP', A, 8.8, size=60, rot=-3)
      + titular(['Te toca', '_actualizar_'], A, 9.2, top=1240, size=200, seed=5)
      + sello(610, 1660, 'Ahorita', A, 9.8, size=80, rot=-7))
escena('e00-alerta', S, 10.9, fase(f1, A, sale=5.0) + fase(f2, A, entra=5.1), fondo='negra', css='.negra .tt .sf{color:#9aa3ff}', seed=1)

# ───────── 0:11 · se llama PHP2Shell · lo encontraron con IA
S = 10.9; A = K.at(S)
escena('e01-php2shell', S, 17.0,
       titular(['Lo llamaron'], A, 11.0, top=TOP, size=130, seed=6)
       + recorte(60, 500, 960, 300, caja('PHP2Shell', 250, 'color:#fff;letter-spacing:-.01em;text-transform:none'), A, 11.4, rot=-2.5, cls='rojo', seed=21, pad='18px 40px')
       + mano(620, 830, 'así le pusieron ↑', A, 13.6, size=62)
       + titular(['Lo encontraron', 'con *IA*'], A, 14.7, top=980, size=145, seed=7)
       + circulo(300, 1200, 300, 190, A, 15.6, seed=8)
       + logo('', 700, 1400, 260, A, 15.6, rot=8, bg='#2457e6', emoji='🤖')
       + nota(110, 1440, 'la IA ayudó<br>a hallarlo', A, 16.3, rot=-5, w=340, size=56), seed=2)

# ───────── 0:17 · PHP saca un parche hoy · dos fallos de 9.2 | del 0 al 10 → casi lo máximo
S = 17.0; A = K.at(S)
REGLA = (f'<div class="rcw" style="left:70px;top:760px;width:940px;height:230px;--d:{A(26.6)};--r:-1.5deg">'
         '<div class="rc crema" style="height:100%;padding:0;position:relative;clip-path:polygon(0 4%,100% 0,99% 100%,1% 96%)">'
         '<div style="position:absolute;left:40px;right:40px;top:0;height:70px;background:repeating-linear-gradient(90deg,#171513 0 4px,transparent 4px 86px)"></div>'
         + ''.join(f'<div style="position:absolute;left:{40 + i * 86 - 30}px;width:60px;top:80px;text-align:center;font-weight:900;font-stretch:62%;font-size:64px">{i}</div>' for i in range(11))
         + '</div></div>')
f1 = (titular(['PHP saca un', '_parche_ hoy'], A, 17.1, x=21.5, top=TOP, size=160, seed=9)
      + ticket(90, 760, 900, [('<i>php.net ›</i> versión de seguridad', 18.2, .8), ('<i>✓</i> corrige <b>2 fallos</b>', 21.7, .5)], A, rot=-1.5, sale=25.2)
      + titular(['Dos fallos', 'de *9.2*'], A, 21.7, x=25.2, top=TOP, size=160, seed=10)
      + numero(50, 1050, N([(0, 0), (24.1, 9.2, 1.0)], f='1'), A, 24.0, size=560, color='var(--rojo)')
      + mano(640, 1640, 'de 10 posibles', A, 24.6, size=66))
f2 = (titular(['Del 0 al 10…'], A, 25.4, x=29.9, top=TOP, size=170, seed=11)
      + REGLA
      + mano(70, 1010, '← nada grave', A, 26.8, size=58, color='var(--verde)') + mano(760, 1010, 'lo máximo →', A, 27.1, size=58)
      + flecha(820, 600, 860, 750, A, 29.2, grosor=12)
      + sello(680, 520, '9.2', A, 29.3, size=110, rot=-6)
      + titular(['Casi lo', '*máximo*'], A, 30.1, top=1150, size=200, seed=12)
      + sello(140, 1640, '🔥 crítico', A, 31.6, size=78, rot=4))
escena('e02-parche', S, 32.85, fase(f1, A, sale=25.2) + fase(f2, A, entra=25.3), seed=3)

# ───────── 0:33 · ejecución remota de código → corre comandos en tu servidor | tu teclado a un desconocido
S = 32.85; A = K.at(S)
TECLAS = ''.join(f'<i style="display:inline-block;width:62px;height:62px;margin:5px;border-radius:10px;background:#f3eee4;box-shadow:inset 0 -6px 0 #c9c2b3"></i>' for _ in range(36))
f1 = (titular(['Ejecución', '_remota_', 'de código'], A, 32.95, x=37.8, top=TOP, size=170, seed=13)
      + sello(330, 1090, 'Sin iniciar sesión', A, 36.6, size=58, rot=-6, color='#ff6b6b')
      + titular(['Corre *comandos*', 'en tu servidor'], A, 38.0, top=TOP, size=120, seed=14)
      + ticket(70, 620, 940, [('<i>desconocido@tu-servidor:~$</i>', 38.8, .6), ('$ whoami', 39.6, .35), ('<b>www-data</b>', 40.2, .3),
                              ('$ ls /var/www', 40.9, .4), ('$ cat <b>config.php</b>', 41.6, .45)], A, rot=-1.5, size=36)
      + mano(560, 1430, '¡y no es tuyo!', A, 41.9, size=70, color='#ff6b6b'))
f2 = (titular(['Tu *teclado*', 'a un', '_desconocido_'], A, 42.7, top=TOP, size=165, seed=15)
      + recorte(110, 960, 600, 300, f'<div style="line-height:0">{TECLAS}</div>', A, 43.5, rot=-4, cls='negro', seed=22, pad='22px')
      + flecha(700, 1150, 830, 1330, A, 44.0, color='#ff6b6b')
      + logo('', 700, 1340, 260, A, 44.2, rot=-6, bg='#e3342a', emoji='🕵️'))
escena('e03-remoto', S, 45.4, fase(f1, A, sale=42.5) + fase(f2, A, entra=42.6), fondo='negra', css='.negra .tt .sf{color:#ff6b6b}', seed=4)

# ───────── 0:45 · no es cualquier cosa · millones de sitios · sitios en alerta | Hacker News: Países Bajos (sin confirmar)
S = 45.4; A = K.at(S)
VENT = ''
for i in range(30):
    c, r = i % 5, i // 5
    t0 = 47.3 + (i * 7 % 30) * .055
    roja = (i * 11) % 4 == 0
    VENT += (f'<div class="rcw" style="left:{70 + c * 190}px;top:{760 + r * 150}px;width:170px;height:126px;--d:{A(t0)};--r:{((i * 37) % 9) - 4}deg;z-index:{14 + i % 3}">'
             f'<div class="rc" style="height:100%;padding:0;border-radius:6px;overflow:hidden"><div style="height:22px;background:#171513;display:flex;gap:5px;padding:6px 8px">'
             '<i style="width:9px;height:9px;border-radius:50%;background:#e3342a"></i><i style="width:9px;height:9px;border-radius:50%;background:#ffe14a"></i></div>'
             f'<div style="margin:12px 12px 6px;height:12px;background:#d8d1c2"></div><div style="margin:0 12px;height:12px;width:60%;background:#d8d1c2"></div></div>'
             + (f'<div class="sl" style="left:28px;top:30px;font-size:30px;padding:2px 10px;border-width:5px;--d:{A(50.2 + (i % 7) * .18)};--r:-12deg">⚠</div>' if roja else '')
             + '</div>')
f1 = (titular(['No es cualquier', '*cosa*'], A, 45.5, x=46.9, top=TOP, size=150, seed=16)
      + titular(['_Millones_', 'de sitios'], A, 47.0, x=49.7, top=TOP, size=170, seed=17)
      + titular(['Sitios en', '*alerta*'], A, 49.9, top=TOP, size=170, seed=18)
      + VENT
      + recorte(560, 1590, 450, 210, ser('«Sitios en alerta», dicen los medios', 46), A, 51.5, rot=4, seed=23, z=30))
QUOTE = (f'<div class="ser" style="font-size:66px;line-height:1.08">«<span class="fade0" style="--d:{A(55.6)}">El centro de ciberseguridad</span> '
         f'<span class="fade0" style="--d:{A(57.1)}">de <b style="font-family:Archivo;font-style:normal;font-weight:900;font-stretch:62%">PAÍSES BAJOS</b></span> '
         f'<span class="fade0" style="--d:{A(58.3)}">quedó fuera de línea</span> <span class="fade0" style="--d:{A(59.1)}">por usar PHP</span>»</div>')
f2 = (logo('ycombinator', 80, 330, 200, A, 53.1, rot=-8, bg='#ff6600', color='#fff')
      + titular(['Lo que dicen en', '*Hacker News*'], A, 53.0, top=350, size=115, seed=19, extra='left:310px')
      + recorte(80, 700, 920, 560, QUOTE, A, 54.2, rot=-1.5, seed=24, pad='50px 54px')
      + titular(['Ojo: aún', '_sin confirmar_'], A, 60.0, top=1360, size=140, seed=20)
      + sello(470, 1140, 'Sin confirmar', A, 60.2, size=76, rot=-10))
escena('e04-sitios', S, 63.5, fase(f1, A, sale=52.8) + fase(f2, A, entra=52.9), css='.tt .sf{color:var(--naranja)}', seed=5)

# ───────── 1:03 · PHP no es malo · la IA ya encuentra fallos · saldrán más seguido | no lo dejes para después
S = 63.5; A = K.at(S)
CODIGO = ''.join(f'<div class="mono" style="font-size:30px;line-height:1.75;white-space:pre">{l}</div>' for l in [
    '<span style="color:#8a8579">&lt;?php</span>', '$user = $_GET[<span style="color:#17a35a">\'id\'</span>];', 'include($page . <span style="color:#17a35a">\'.php\'</span>);',
    'echo render($tpl);', '$db->query($sql);', 'exit;'])
f1 = (fase(titular(['PHP no es', '*malo*'], A, 63.6, top=TOP, size=190, seed=21) + palomita(700, 360, 190, A, 66.5), A, sale=67.2)
      + titular(['La IA ya encuentra', '_fallos_'], A, 67.4, x=71.0, top=TOP, size=125, seed=22)
      + recorte(80, 720, 920, 560, CODIGO, A, 67.6, rot=-1.2, seed=25, pad='40px 50px', sale=73.0)
      + circulo(390, 960, 640, 110, A, 69.2, seed=9) + circulo(400, 1065, 600, 110, A, 70.1, seed=10)
      + logo('', 760, 1250, 200, A, 69.2, rot=12, bg='#2457e6', emoji='🔍', sale=73.0)
      + titular(['Saldrán más', '*seguido*'], A, 71.1, top=TOP, size=170, seed=23)
      + flecha(150, 1560, 930, 1380, A, 72.3, color='var(--azul)', curva=-.15, grosor=14)
      + mano(560, 1580, 'más reportes', A, 72.4, size=66, color='var(--azul)'))
f2 = (titular(['No lo dejes', 'para *después*'], A, 73.3, top=TOP, size=170, seed=24)
      + nota(130, 880, 'Actualizar<br>después…', A, 73.8, rot=-6, w=420, size=74)
      + tacha(150, 1090, 380, A, 74.6, grosor=18)
      + sello(560, 1000, 'Hoy', A, 75.9, size=190, rot=-8))
escena('e05-ia', S, 76.6, fase(f1, A, sale=73.1) + fase(f2, A, entra=73.2), css='.tt .sf{color:var(--azul)}', ac='var(--azul)', seed=6)

# ───────── 1:17 · ¿qué versión tienes? · corre php -v · ya con el parche (versiones por rama) | PHP no está muerto · hoy lo actualizamos
S = 76.6; A = K.at(S)
RAMAS = [('8.5', '8.5.12', 83.2), ('8.4', '8.4.27', 83.5), ('8.3', '8.3.36', 83.8), ('8.2', '8.2.35', 84.1)]
NOTAS = ''.join(nota(90 + (i % 2) * 470, 1050 + (i // 2) * 330, f'<span style="font-size:40px">rama {r}</span><br>{v} ✓', A, t, rot=[-4, 3, 5, -3][i], w=420, size=76,
                     color=['#ffe46b', '#b8f0c8', '#ffd0dc', '#cfe0ff'][i]) for i, (r, v, t) in enumerate(RAMAS))
f1 = (titular(['¿Qué versión', '*tienes*?'], A, 76.7, x=79.4, top=TOP, size=170, seed=25)
      + titular(['Corre', '_php -v_'], A, 79.6, x=83.0, top=TOP, size=170, seed=26)
      + ticket(90, 720, 900, [('<i>$</i> php -v', 79.9, .4), ('PHP 8.4.<b>27</b> (cli)', 80.6, .5), ('<i># compárala con la última de tu rama</i>', 81.8, .9)], A, rot=-1.5, size=36)
      + titular(['Ya con el', '_parche_'], A, 83.2, top=TOP, size=170, seed=27)
      + NOTAS)
f2 = (titular(['PHP', 'está *muerto*'], A, 86.2, top=420, size=200, seed=28)
      + sello(400, 410, 'No', A, 87.2, size=150, rot=-10)
      + titular(['Tan vivo que hoy', 'lo _actualizamos_'], A, 88.3, top=1000, size=125, seed=29)
      + logo('php', 380, 1340, 300, A, 89.8, rot=-6, bg='#7a86e0', color='#fff')
      + mano(700, 1420, '♥', A, 90.0, size=150))
escena('e06-version', S, 91.1, fase(f1, A, sale=86.0) + fase(f2, A, entra=86.1), css='.tt .sf{color:var(--verde)}', ac='var(--verde)', seed=7)

# ───────── 1:31 · cierre: ¿cada cuánto actualizas tu servidor? (abajo entra «Sígueme»)
S = 91.1; A = K.at(S)
OPC = ''.join(recorte(80, 800 + i * 210, 920, 170, f'<div style="display:flex;align-items:center;gap:26px;height:100%">'
                      f'<i style="width:70px;height:70px;border:7px solid #171513;border-radius:12px;flex-shrink:0"></i>{caja(t, 84)}</div>',
                      A, t0, rot=[-1.5, 1.8][i], seed=26 + i, pad='20px 40px') for i, (t, t0) in enumerate([('📅 Siempre al día', 92.1), ('🔥 Cuando algo truena', 92.9)]))
escena('e07-cierre', S, FIN,
       titular(['¿Cada cuánto', 'actualizas tu', '*servidor*?'], A, 91.2, top=TOP, size=140, seed=30)
       + OPC + mano(110, 1200, 'cuéntame 👇', A, 93.4, size=64), sigue=False, seed=8)

# ───────── «Sígueme»: nota adhesiva + comentario tecleado (transparente, sobre el cierre)
SEG_INI = 93.9
S = SEG_INI; A = K.at(S)
SEG = (nota(570, 1250, '<div style="font-size:44px">Sígueme</div><div style="font-family:Archivo;font-weight:900;font-stretch:62%;font-size:84px;line-height:.9;text-transform:uppercase">El Log</div>'
            '<div style="font-size:40px;margin-top:6px">cada semana · Armando</div>', A, 94.0, rot=5, w=430, size=60)
       + sello(640, 1620, 'Seguir ✓', A, 94.8, size=60, rot=-4, color='var(--verde)')
       + recorte(60, 1280, 480, 330, '<div class="ser" style="font-size:40px;line-height:1.1">🛠️ ¿Cada cuánto actualizas?</div>'
                 f'<div style="margin-top:18px;font-family:Caveat;font-weight:700;font-size:42px;color:var(--azul)"><span class="mono" style="font-size:0"></span>'
                 f'<span style="display:inline-block;white-space:nowrap;clip-path:inset(0 100% 0 0);animation:tip .9s steps(26) {A(95.3)} forwards">Cada semana, ya aprendí 😅</span></div>',
                 A, 94.4, rot=-3, seed=31))
PIEZAS.append(('seguir', SEG_INI, FIN, K.page('', SEG, round(FIN - SEG_INI, 2), S0=SEG_INI, transparente=True)))

# ───────── cabecera de periódico + cintillo rojo de última hora (todo el video, encima de todo)
CORRIDO = ['PHP 8.5.12, 8.4.27, 8.3.36 y 8.2.35 corrigen los dos fallos', 'CVE-2026-109618 y CVE-2026-109619: 9.2 de 10',
           'Ejecución de código sin iniciar sesión', 'Parche de emergencia: salió un día antes por una filtración',
           'Los encontraron investigadores de Calif, Wiz y OpenAI', 'Hacker News: lo de Países Bajos aún no está confirmado', 'Revisa tu versión: php -v']
CAPS = [(0.0, 'Alerta'), (10.9, 'PHP2Shell'), (17.0, 'El parche'), (32.85, 'Ejecución remota'), (45.4, 'Sitios en alerta'), (63.5, 'La IA'),
        (76.6, 'Tu versión'), (91.1, 'Tu opinión')]
A = K.at(0)
CAPH = ''.join(f'<span class="cp" style="--d:{A(t)};{f"--x:{A(CAPS[i + 1][0])};" if i + 1 < len(CAPS) else ""}">{i + 1:02d} · {n}</span>' for i, (t, n) in enumerate(CAPS))
TICK = '<span>⚠</span>'.join(f'<span>{c}</span>' for c in CORRIDO)
CABE_CSS = """
.cab{position:absolute;left:0;right:0;top:0;height:250px;z-index:90;background:#f3ecdf;box-shadow:0 10px 24px rgba(0,0,0,.35);animation:cabIn .45s cubic-bezier(.2,1.3,.4,1) both}
.cab:before{content:'';position:absolute;inset:0;background:url("FIBRA");opacity:.45}
@keyframes cabIn{from{transform:translateY(-260px)}to{transform:none}}
.cab .mh{position:absolute;left:44px;right:44px;top:22px;height:108px;display:flex;align-items:flex-end;justify-content:space-between;border-bottom:5px double #171513;padding-bottom:6px}
.cab .lg{font-family:'Instrument Serif',serif;font-size:112px;line-height:.8;letter-spacing:-.02em}
.cab .lg i{color:var(--rojo)}
.cab .ed{text-align:right;font-weight:800;font-stretch:75%;text-transform:uppercase;font-size:24px;letter-spacing:.08em;line-height:1.3}
.cab .ed b{display:block;font-size:30px;color:var(--rojo)}
.cab .cp{position:absolute;right:44px;top:142px;font-weight:900;font-stretch:62%;font-size:40px;text-transform:uppercase;opacity:0;animation:capIn .3s steps(2) var(--d) forwards}
.cab .cp[style*="--x"]{animation:capIn .3s steps(2) var(--d) forwards,capOut .01s linear var(--x) forwards}
@keyframes capIn{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:none}}@keyframes capOut{to{opacity:0}}
.cab .ul{position:absolute;left:44px;top:146px;font-weight:900;font-stretch:62%;font-size:36px;text-transform:uppercase;color:#fff;background:var(--rojo);padding:2px 16px;
  animation:lat 1s steps(1) infinite}
@keyframes lat{50%{background:#171513}}
.tick{position:absolute;left:0;right:0;top:196px;height:54px;background:var(--rojo);overflow:hidden;display:flex;align-items:center}
.tick .mv{display:flex;gap:30px;white-space:nowrap;font-weight:800;font-stretch:80%;font-size:30px;color:#fff;text-transform:uppercase;animation:mv 70s linear infinite;padding-left:1080px}
@keyframes mv{to{transform:translateX(-100%)}}
""".replace('FIBRA', K.FIBRA)
CABE = (f'<div class="cab"><div class="mh"><div class="lg">El <i>Log</i></div><div class="ed"><b>Edición especial</b>N.º 08 · seguridad</div></div>'
        f'<span class="ul">⚠ Última hora</span>{CAPH}<div class="tick"><div class="mv">{TICK}<span>⚠</span>{TICK}</div></div></div>')
PIEZAS.append(('cabecera', 0.0, FIN, K.page(CABE_CSS, CABE, FIN, S0=0.0, transparente=True)))
PRE = 'ellr8-'

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
        rel = os.environ.get('REL', 'noticias/8/recorte')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
