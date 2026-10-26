"""Archivo #01 · Knight Capital (2012) · edición «Cinta VHS»: noticiero de los 90 grabado en casete, 100 % animado sobre la voz.
Tiempos = video final de archivo/1 (74.81 s, voz/voz-editada.wav). La cinta rebobina a 2003 cuando dice «años antes», pausa en
«Nadie los leyó», graba encima (● REC) en «bórralo» y adelanta (▶▶ FF) en «automatizarlo».
Uso: SALIDA=~/Documents/Videos/archivo/1/animaciones REL=archivo/1/animaciones python3 ejemplos/archivo01-vhs.py [ids…]   (SOLO_HTML=1 para revisar)
Las páginas van a _html-vhs/; los webm salen con prefijo «av1-».
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import vhs as V
from vhs import el, tt, nr, vt, num, caja, urgente, cintillo, ticker, grafica, rack, interruptor, cassette, barra, ROJO, ORO, AMBAR, CIAN

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.path.expanduser('~/Documents/Videos/archivo/1/animaciones')))
REL = os.environ.get('REL', 'archivo/1/animaciones')
VOZ = os.path.join(OUT, '..', 'voz')
WORK = os.path.join(OUT, '_html-vhs'); os.makedirs(WORK, exist_ok=True)
PRE = 'av1-'
FIN = 74.81

# la cinta: modos de la videocasetera, fechador de cámara y reloj del día (todo en segundos del video final)
MODOS = [(0, 'PLAY'), (23.88, 'REW'), (25.2, 'PLAY'), (29.68, 'FF'), (31.4, 'PLAY'), (57.3, 'PAUSE'), (59.3, 'PLAY'),
         (67.75, 'REC'), (68.55, 'PLAY'), (72.45, 'FF'), (73.4, 'STOP'), (74.15, 'EJECT')]
FECHAS = ([(0, 'AGO. 01 2012')] + [(23.88 + k * .13, f'---. -- {2011 - k}') for k in range(8)] + [(25.2, '---. -- 2003')]
          + [(29.68 + k * .19, f'---. -- {2004 + k}') for k in range(8)] + [(31.4, 'AGO. 01 2012')])
RELOJ = [(37.73, 59.34, 9.5 * 3600, 10.25 * 3600)]   # abre la bolsa 9:30 → lo apagan 45 min después
CINTA = 'KCG ▼  ·  NYSE ABRE 9:30  ·  ARCHIVO 01  ·  ÓRDENES ▲▲▲  ·  WALL ST. EN VIVO  ·  '


def pagina(S0, S1, body, glitches=(), cinta=CINTA, vel=200, cinta_fin=None, **kw):
    """Escena opaca de S0 a S1 con la barra de cotizaciones decorativa abajo (zona de interfaz, nada importante ahí)."""
    V.nueva(S0)
    deco = ticker(cinta, 1600, S0, cinta_fin, vel, color='#fff', fondo='rgba(5,10,50,.85)')
    return V.page(body + deco, round(S1 - S0, 3), S0, glitches=glitches, modos=MODOS, fechas=FECHAS, reloj=RELOJ, **kw)


def p1():
    S0, S1 = 0.0, 8.95; V.nueva(S0)
    reloj = (f'<div class="nr" style="font-size:40px;color:{ORO}">EN SOLO</div>'
             f'<div class="vt" style="font-size:150px;line-height:.9"><span data-n=\'[[4.18,0],[4.2,2700,1.0]]\' data-f="ms">00:00</span></div>'
             f'<div class="nr" style="font-size:40px">MINUTOS</div>')
    b = (urgente(0.0, 5.45)
         + nr('UNA EMPRESA PERDIÓ', 70, 420, 66, 0.12, 5.45)
         + num([[1.54, 0], [1.56, 470_000_000, 1.3]], 56, 500, 126, 1.54, 5.45, f='m', color=ROJO)
         + nr('DE DÓLARES', 70, 640, 62, 3.26, 5.45, color=ORO)
         + caja(reloj, 70, 750, 4.02, 5.45, w=330)
         + grafica([.95, .9, .93, .8, .84, .66, .7, .5, .42, .46, .28, .2, .08], 470, 760, 440, 280, 2.0, 5.45, d=3.2)
         + cintillo('EN VIVO', 'PÉRDIDA MILLONARIA EN 45 MINUTOS', 0.6, 5.45)
         # ¿la razón?
         + tt('¿LA RAZÓN?', 70, 330, 140, 5.50, S1)
         + rack(360, 520, 6.60, S1, w=340, u=8, nombre='SERVIDOR')
         + caja(f'<span class="led r on" style="display:inline-block;width:24px;height:24px;margin-right:14px"></span>SIN ACTUALIZAR', 250, 860, 8.12, S1,
                fx='flip', cls='rojo tt', st='font-size:50px')
         + cintillo('LA CAUSA', 'UN SERVIDOR QUE NADIE ACTUALIZÓ', 6.6, S1))
    return pagina(S0, S1, b, glitches=[(5.45, .3, .7)], entra=False)


def p2():
    S0, S1 = 8.95, 21.65; V.nueva(S0)
    barras = ''
    for k, (hh, nom) in enumerate([(120, ''), (170, ''), (240, 'KNIGHT'), (215, ''), (105, '')]):
        c = f'linear-gradient(180deg,#fff2a6,{ORO})' if nom else 'linear-gradient(180deg,#7d8bd6,#2c3a8f)'
        barras += el(f'<div style="width:120px;height:{hh}px;background:{c};border:3px solid #fff;box-shadow:0 8px 0 rgba(0,0,0,.4)"></div>',
                     110 + k * 160, 1040 - hh, 12.2 + k * .12, 15.45, 'wipeu', .35)
        if nom:
            barras += vt(nom, 100 + k * 160, 1040 - hh - 62, 58, 12.91, 15.45, color=ORO, fx='pop')
    crt = el('', 70, 440, 16.6, S1, 'zoom', .3, w=600, h=480, cls='crt')
    b = (caja(f'<div class="vt" style="font-size:56px;color:{ORO}">1 AGO.</div><div class="tt" style="font-size:150px">2012</div>', 70, 320, 9.55, 15.45)
         + caja('KNIGHT CAPITAL', 70, 560, 10.68, 15.45, fx='slider', cls='oro tt', st='font-size:76px')
         + nr('CORREDORA DE ACCIONES · EE.UU.', 70, 680, 44, 11.1, 15.45)
         + barras
         + el('', 70, 1043, 12.2, 15.45, 'wipe', .4, w=860, h=6, st='background:#fff')
         + vt('ACCIONES MOVIDAS EN EE.UU.', 110, 1056, 46, 14.81, 15.45, color='#cfd6ff', r=50)
         + cintillo('PERFIL', 'UNO DE LOS GIGANTES DE LA BOLSA', 10.7, 15.4, y=1130)
         # sistema nuevo + interruptor
         + caja('SISTEMA NUEVO', 70, 320, 15.87, S1, cls='tt', st='font-size:66px')
         + el('ESTRENO', 590, 340, 16.2, S1, 'blink', cls='cj rojo nr', st='font-size:40px;padding:10px 20px')
         + crt
         + vt('SMARS · VERSIÓN NUEVA<br>&gt; LISTO PARA ESTRENAR', 110, 480, 54, 16.7, S1, color=AMBAR, r=30, cls='amb')
         + vt('if (FLAG == ON) {<br>&nbsp;&nbsp;arranca(NUEVO);<br>}', 110, 680, 58, 19.97, S1, color=AMBAR, r=28, cls='amb')
         + interruptor(730, 520, 18.9, S1, etiqueta='FLAG')
         + cintillo('EL PLAN', 'UN INTERRUPTOR QUE YA EXISTÍA', 18.6, S1))
    return pagina(S0, S1, b, glitches=[(15.45, .28, .6)])


def p3():
    S0, S1 = 21.65, 31.5; V.nueva(S0)
    viejo = ('<div class="tt" style="font-size:64px">POWER PEG</div>'
             '<div class="vt" style="font-size:44px;color:#ddd">PROGRAMA VIEJO</div>')
    cable = el('<svg width="300" height="200" style="overflow:visible"><path d="M0 120 C 90 120, 110 40, 210 40" fill="none" stroke="#ffcf3a" '
               f'stroke-width="10" stroke-dasharray="1" data-dr="{V.L(24.71)},.5"/></svg>', 280, 580, 24.71, S1)
    b = (tt('EL PROBLEMA', 70, 320, 120, 21.70, 26.25, color=ROJO)
         + interruptor(110, 520, 22.75, S1, etiqueta='FLAG')
         + nr('AÑOS ANTES…', 470, 470, 60, 23.95, 26.25, color=ORO)
         + cable
         + caja('OTRO PROGRAMA', 480, 570, 25.27, 26.32, cls='tt', st='font-size:54px')
         # uno viejo, apagado desde 2003
         + caja(viejo, 480, 560, 26.32, S1, fx='cut', st='--c1:#8a8f9e;--c2:#3c404c')
         + tt('UNO VIEJO', 70, 320, 120, 26.32, S1, color='#cfd3e0')
         + el('<span class="led"></span>&nbsp;APAGADO', 490, 760, 27.91, S1, 'pop', cls='vt', st='font-size:58px;display:flex;align-items:center;gap:12px')
         + tt('DESDE 2003', 480, 845, 80, 28.71, S1, color=ORO)
         + caja('NUNCA LO BORRARON', 70, 960, 30.05, S1, fx='flip', cls='rojo tt', st='font-size:50px')
         + cintillo('OJO', 'EL INTERRUPTOR PRENDÍA OTRO PROGRAMA', 21.75, 26.25, y=1100))
    return pagina(S0, S1, b)


def p4():
    S0, S1 = 31.5, 44.9; V.nueva(S0)
    racks = ''
    for k in range(8):
        x, y = 70 + (k % 4) * 215, 440 + (k // 4) * 270
        ok = k < 7
        racks += rack(x, y, 31.6 + k * .08, 37.65, w=170, u=3)
        racks += barra([[32.1 + k * .15, 0], [32.2 + k * .15, 1 if ok else 0, 1.1]], x, y + 225, 170, 31.9, 37.65, alto=30, color=CIAN)
        racks += (vt(f'#{k + 1} v2 OK', x + 10, y + 172, 46, 33.4 + k * .1, 37.65, color='#7dffa0', fx='pop') if ok else
                  vt(f'#{k + 1} v1', x + 30, y + 172, 46, 36.40, 37.65, color=ROJO, fx='pop'))
    b = (tt('ACTUALIZACIÓN', 70, 320, 92, 31.57, 37.65)
         + racks
         + el('', 280 + 3 * 215 - 225, 700, 36.40, 37.65, 'blink', w=210, h=300, st=f'border:7px solid {ROJO};box-shadow:0 0 24px {ROJO}')
         + num([[33.47, 8], [35.45, 7, .15]], 70, 1000, 72, 33.47, 37.65, suf=' / 8 LISTOS')
         + caja('SE LES PASÓ', 450, 1090, 36.69, 37.65, fx='flip', cls='rojo tt', st='font-size:46px')
         # abre la bolsa
         + tt('9:30 AM', 70, 320, 150, 37.73, S1, color=ORO)
         + nr('ABRE LA BOLSA', 70, 470, 64, 38.0, S1)
         + interruptor(90, 650, 38.6, S1, on_t=39.3, etiqueta='FLAG')
         + rack(420, 600, 40.65, 41.95, w=300, u=6, nombre='SERVIDOR #8 · v1')
         + rack(420, 600, 41.95, S1, w=300, u=6, nombre='SERVIDOR #8 · v1', leds='r', fx='cut', sk=10)
         + caja('POWER PEG: ACTIVO', 300, 960, 42.1, S1, fx='flip', cls='rojo tt', st='font-size:52px')
         + cintillo('ALERTA', 'EL PROGRAMA VIEJO DESPIERTA', 43.3, S1, y=1100))
    return pagina(S0, S1, b, glitches=[(37.65, .3, .8), (41.95, .35, .5)])


def p5():
    S0, S1 = 44.9, 57.2; V.nueva(S0)
    filas = ''
    for k in range(7):
        y = 640 + k * 50
        filas += vt(f'SMARS &nbsp;ERROR · POWER PEG DISABLED', 110, y, 44, 52.0 + k * .18, S1, color=AMBAR, fx='cut', cls='amb')
        filas += el('', 96, y - 2, 54.62 + k * .05, S1, 'blink', w=800, h=46, st='background:rgba(255,40,60,.35)')
    b = (caja('COMPRA CARO ▲', 70, 330, 45.82, 49.4, fx='pop', cls='rojo tt', st='font-size:64px')
         + caja('VENDE BARATO ▼', 70, 460, 47.0, 49.4, fx='pop', cls='tt', st='font-size:64px')
         + tt('SIN PARAR', 520, 580, 92, 48.28, 49.4, color=ROJO, sk=10)
         + grafica([.9, .7, .95, .5, .8, .35, .6, .2, .45, .1, .3, .02], 70, 700, 860, 240, 45.2, 49.4, d=3.6)
         + vt('ÓRDENES', 70, 975, 46, 45.18, 49.4, color='#cfd6ff', r=40)
         + num([[45.2, 0], [45.25, 2_000_000, 4.2]], 70, 1020, 62, 45.18, 49.4, f='c', cls='vt', color='#fff')
         + vt('PÉRDIDA', 520, 975, 46, 45.18, 49.4, color='#cfd6ff', r=40)
         + num([[45.2, 0], [45.25, 260_000_000, 4.2]], 520, 1020, 62, 45.18, 49.4, f='m', cls='vt', color=ROJO)
         # 97 correos antes de abrir
         + tt('Y LO PEOR…', 70, 320, 100, 49.72, S1, color=ORO)
         + vt('ANTES DE ABRIR · 8:01 AM', 70, 450, 54, 50.19, S1, color='#cfd6ff', r=40)
         + el('', 70, 520, 51.94, S1, 'zoom', .3, w=860, h=520, cls='crt')
         + vt('BANDEJA DE ENTRADA', 110, 560, 50, 51.94, S1, color=AMBAR, r=40, cls='amb')
         + filas
         + el(f'<span data-n=\'[[52.67,0],[52.7,97,1.2]]\' data-f="i">0</span>', 750, 455, 52.67, S1, 'pop', cls='tt',
              st=f'font-size:120px;color:#fff;background:{ROJO};border-radius:90px;padding:6px 38px;box-shadow:0 0 0 6px #fff,0 12px 0 rgba(0,0,0,.4)')
         + cintillo('AVISO', '97 CORREOS: ALGO ANDABA MAL', 54.62, S1, y=1100))
    return pagina(S0, S1, b, glitches=[(49.4, .3, .8)], cinta='COMPRA ▲  ·  VENDE ▼  ·  COMPRA ▲  ·  VENDE ▼  ·  KCG ▼▼  ·  ', vel=700)


def p6():
    S0, S1 = 57.2, 64.9; V.nueva(S0)
    b = (tt('NADIE', 70, 360, 220, 57.30, 59.25)
         + tt('LOS LEYÓ.', 70, 590, 130, 57.49, 59.25, color=ORO)
         + el('97 NO LEÍDOS', 70, 780, 57.7, 59.25, 'blink', cls='vt amb', st='font-size:84px')
         # final
         + caja('SISTEMA APAGADO', 70, 320, 59.34, S1, cls='tt', st='font-size:60px')
         + num([[59.3, 260_000_000], [60.47, 470_000_000, 1.2]], 60, 480, 100, 60.05, S1, f='m', color=ROJO)
         + nr('PERDIDOS EN 45 MINUTOS', 70, 600, 56, 60.8, S1, color=ORO)
         + caja('KNIGHT CAPITAL', 70, 740, 62.6, S1, fx='slide', cls='oro tt', st='font-size:72px')
         + caja('VENDIDA', 70, 860, 63.24, S1, w=860, cls='rojo tt', st='font-size:150px;text-align:center')
         + cintillo('FINAL', 'LA EMPRESA TERMINÓ VENDIDA', 63.3, S1, y=1100))
    return pagina(S0, S1, b, glitches=[(59.25, .3, .8)])


def p7():
    S0, S1 = 64.9, FIN; V.nueva(S0)
    tarjeta = (el('', 0, 0, 73.35, None, w=1080, h=1920, st=f'background:{V.AZUL}')
               + tt('ARCHIVO', 100, 620, 170, 73.4, None, color=ORO, fx='zoom', d=.25)
               + vt('#01 · KNIGHT CAPITAL', 110, 810, 72, 73.55, None, r=60)
               + caja('SÍGUEME PARA MÁS HISTORIAS', 100, 940, 73.8, None, cls='tt', st='font-size:46px'))
    b = (tt('LA LECCIÓN', 70, 320, 110, 65.0, 68.55, color=ORO)
         + cassette(230, 480, 65.56, 68.55, etiqueta='CÓDIGO VIEJO<br><span style="font-size:.8em">(APAGADO, POR SI ACASO)</span>')
         + el('', 280, 507, 67.75, 68.55, 'wipe', .7, w=520, h=138, st='background:repeating-linear-gradient(0deg,#fff 0 2px,#222 2px 4px,#888 4px 7px,#000 7px 9px)')
         + vt('BORRADO', 410, 545, 72, 68.3, 68.55, color='#fff', fx='cut', st='background:#000;padding:0 16px')
         + barra([[67.75, 0], [67.8, 1, .7]], 230, 880, 620, 67.75, 68.55, color=ROJO,
                 etiqueta=f'<div class="vt" style="font-size:50px;margin-top:8px;color:{ROJO}">● BORRANDO…</div>')
         # cambios a mano → automatiza
         + tt('¿SUBES CAMBIOS<br>A MANO?', 70, 320, 84, 68.61, 73.35)
         + vt('DEPLOY MANUAL', 70, 560, 56, 69.7, 73.35, color='#cfd6ff', r=40)
         + barra([[69.7, 0], [72.4, .25, 2.6], [72.53, 1, .5]], 70, 630, 860, 69.7, 73.35, alto=56)
         + num([[69.9, 0], [72.4, 2, 2.4], [72.53, 8, .5]], 70, 720, 62, 69.9, 73.35, cls='vt', suf=' / 8 SERVIDORES')
         + nr('HOY ES UN BUEN DÍA PARA…', 70, 850, 60, 71.02, 73.35, color=ORO)
         + caja('AUTOMATIZARLO ▶▶', 70, 950, 72.53, 73.35, fx='pop', cls='oro tt', st='font-size:70px')
         + tarjeta)
    return pagina(S0, S1, b, glitches=[(67.75, .25, .5), (68.55, .3, .8), (73.35, .3, 1)], cinta_fin=73.35, sale=False)


ESCENAS = [('p1-gancho', 0.0, 8.95, p1), ('p2-knight', 8.95, 21.65, p2), ('p3-viejo', 21.65, 31.5, p3), ('p4-servidores', 31.5, 44.9, p4),
           ('p5-caos', 44.9, 57.2, p5), ('p6-nadie', 57.2, 64.9, p6), ('p7-cierre', 64.9, FIN, p7)]


def main():
    ids = sys.argv[1:]
    G = json.load(open(os.path.join(VOZ, 'grupos.json')))
    paginas = [(pid, a, b, f()) for pid, a, b, f in ESCENAS]
    paginas.append(('sub', 0.0, FIN, V.subtitulos(G, FIN, ocultar=[(57.2, 59.25), (73.35, FIN)])))
    lote, ovs = [], []
    for pid, a, b, html in paginas:
        ruta = os.path.join(WORK, f'{pid}.html')
        open(ruta, 'w').write(html)
        out = os.path.join(OUT, f'{PRE}{pid}.webm')
        lote.append(dict(html=ruta, dur=round(b - a, 3), out=out))
        ovs.append(dict(file=f'{REL}/{PRE}{pid}.webm', html=f'{REL}/_html-vhs/{pid}.html', start=a, end=b, trimIn=0, scale=1, position='center'))
    if ids:
        lote = [x for x in lote if any(os.path.basename(x['html']).startswith(i) for i in ids)]
    else:
        json.dump(ovs, open(os.path.join(OUT, 'overlays-vhs.json'), 'w'), indent=2, ensure_ascii=False)
    json.dump(lote, open(os.path.join(OUT, 'lote-vhs.json' if not ids else '_lote-vhs-parcial.json'), 'w'), indent=2, ensure_ascii=False)
    print(f'{len(paginas)} páginas en {WORK}')
    if os.environ.get('SOLO_HTML'):
        return
    subprocess.run(['node', CAP, '--lote', os.path.join(OUT, 'lote-vhs.json' if not ids else '_lote-vhs-parcial.json')], check=True)


if __name__ == '__main__':
    main()
