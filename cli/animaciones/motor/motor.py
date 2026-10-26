"""Motor de animaciones: guion JSON → escenas HTML (mismo contrato __seek/__listo de siempre) → overlays + manifiesto.

  python3 cli/animaciones/motor/motor.py <guion.json> [--capturar] [--solo id1,id2] [--base ~/Documents/Videos]

Guion (ver docs/plan-motor-animaciones.md, sección 4.3):
  {"video": "noticias/10", "estilo": "recorte", "fin": 92.95, "prefijo": "elm10-",
   "transcripcion": "voz/palabras.json",          ← opcional: tiempos {"palabra": …} (relativo a la carpeta del video)
   "manifest_base": "manifest.json",               ← opcional: de aquí salen clips, voz y música del manifiesto nuevo
   "salida": "animaciones-motor",                   ← carpeta (relativa al video) de los HTML/WebM
   "escenas": [{"id": "e01", "plantilla": "cifra", "inicio": 12.86, "fin": 23.76, "datos": {…}}, …]}
Cualquier tiempo puede ser {"palabra": "x", "n": 1, "desfase": -0.1}.
Variantes del gancho (para comparar con el modo de comparar del reproductor):
  "variantes_gancho": [{"nombre": "b", "escenas": [{…escena que reemplaza a la del mismo id…}]}, …]
  → un manifiesto extra por variante: <manifest_out sin .json>-<nombre>.json (solo cambian esas escenas). Sin --capturar solo se generan los HTML y el manifiesto
(los overlays llevan "html" para la vista previa en vivo y "file" con el .webm que tendrá al grabarse).
"""
import argparse, importlib, json, os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import tiempos, esquema

ENTRADA = .6   # lo que tarda en entrar la hoja/escena (Recorte: rasga .6 s)


def generar(g, escenas, estilo, vdir, base, sufijo='', solo=()):
    """Escenas → HTML + lista de capas (overlays) + lote de captura."""
    fin = g['fin']
    salida = os.path.join(vdir, g.get('salida', 'animaciones-motor'))
    work = os.path.join(salida, '_html')
    os.makedirs(work, exist_ok=True)
    pre = g.get('prefijo', 'm-')
    piezas, capas = [], []
    for e in escenas:
        pid = e['id'] + (sufijo if e.get('_variante') else '')
        if e['plantilla'] in estilo.CAPAS:
            capas.append((pid, *estilo.CAPAS[e['plantilla']]['f'](e, fin)))
        else:
            # la escena que abre el video ya debe estar en pantalla en el cuadro 0: se arma ENTRADA s antes (su hoja entrando queda
            # en ese tramo) y la capa se recorta con trimIn; si no, los primeros cuadros muestran el fondo vacío
            if e['inicio'] <= .01:
                e = dict(e, inicio=-ENTRADA)
            piezas.append((pid, *estilo.escena_pantalla(e, siguiente=e['fin'] < fin - .01)))
    piezas += capas                      # las capas transparentes (Sígueme, cabecera) van encima de todo
    lote = []
    for pid, a, b, html in piezas:
        if solo and pid not in solo:
            continue
        h = os.path.join(work, f'{pid}.html')
        open(h, 'w').write(html)
        lote.append(dict(html=h, dur=round(b - a, 2), out=os.path.join(salida, f'{pre}{pid}.webm')))
        print(f'html {pid:18s} {a:7.2f}–{min(b, fin):7.2f}')
    rel = os.path.relpath(salida, base)
    ovs = [dict(file=f'{rel}/{pre}{pid}.webm', html=f'{rel}/_html/{pid}.html', start=round(max(0, a), 2), end=round(min(b, fin), 2),
                trimIn=round(max(0, -a), 2), scale=1, position='center') for pid, a, b, _ in piezas]
    return ovs, lote, salida


def resolver_escenas(lista, palabras, fin):
    out = []
    for e in lista:
        e = dict(e)
        e['inicio'] = tiempos.resolver(e['inicio'], palabras, 0)
        e['fin'] = fin if e['fin'] == 'fin' else tiempos.resolver(e['fin'], palabras, e['inicio'])
        e['datos'] = tiempos.resolver_todo(e.get('datos', {}), palabras, e['inicio'])
        out.append(e)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('guion')
    ap.add_argument('--base', default=os.path.expanduser('~/Documents/Videos'))
    ap.add_argument('--capturar', action='store_true')
    ap.add_argument('--solo', default='')
    ap.add_argument('--manifest-out')
    o = ap.parse_args()
    g = json.load(open(o.guion))
    estilo = importlib.import_module(f'plantillas.{g["estilo"]}')
    vdir = os.path.join(o.base, g['video'])
    tr = g.get('transcripcion')
    palabras = tiempos.cargar(tr if not tr or os.path.isabs(tr) else os.path.join(vdir, tr))
    fin = g['fin']
    try:
        escenas = resolver_escenas(g['escenas'], palabras, fin)
        esquema.validar(dict(g, escenas=escenas), estilo.PLANTILLAS)
        variantes = []
        for v in g.get('variantes_gancho', []):
            cambio = {e['id']: dict(e, _variante=True) for e in resolver_escenas(v['escenas'], palabras, fin)}
            ev = [cambio.get(e['id'], e) for e in escenas]
            esquema.validar(dict(g, escenas=ev), estilo.PLANTILLAS)
            variantes.append((v['nombre'], ev))
    except (tiempos.ErrorTiempo, esquema.ErrorGuion) as err:
        sys.exit(f'✖ guion inválido:\n{err}')

    solo = set(filter(None, o.solo.split(',')))
    ovs, lote, salida = generar(g, escenas, estilo, vdir, o.base, solo=solo)
    json.dump(ovs, open(os.path.join(salida, 'overlays.json'), 'w'), indent=2, ensure_ascii=False)
    if g.get('manifest_base'):
        base_m = json.load(open(os.path.join(vdir, g['manifest_base'])))
        mo = o.manifest_out or os.path.join(vdir, g.get('manifest_out', 'manifest-motor.json'))
        nombre = g.get('nombre', base_m.get('name', 'video') + '-motor')
        def escribe(ruta, nom, capas):
            json.dump(dict(base_m, name=nom, overlays=capas), open(ruta, 'w'), indent=2, ensure_ascii=False)
            print('manifiesto', ruta)
        escribe(mo, nombre, ovs)
        for nom, ev in variantes:
            ovv, lv, _ = generar(g, ev, estilo, vdir, o.base, sufijo=f'--{nom}')
            escribe(mo[:-5] + f'-{nom}.json', f'{nombre}-{nom}', ovv)
            lote += [x for x in lv if '--' in os.path.basename(x['html'])]
    if o.capturar and lote:
        lp = os.path.join(salida, '_html', '_lote.json')
        json.dump(lote, open(lp, 'w'))
        r = subprocess.run(['node', os.path.join(AQUI, '..', 'capturar.ts'), '--lote', lp])
        sys.exit(r.returncode)


if __name__ == '__main__':
    main()
