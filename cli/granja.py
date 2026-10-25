"""Reparto de capturas entre la Mac y la Legion («becario») por una carpeta sincronizada (Syncthing).

  python3 cli/granja.py lanza <id> <lista.json> [-P 6]     reparte, graba lo de la Mac y recoge lo de la Legion
  python3 cli/granja.py recoge <id>                         solo recoger (si se cortó)
  python3 cli/granja.py verifica <manifest.json>…           revisa que cada capa exista y dure lo que debe

lista.json = [[html, dur, salida.webm, peso]]  (peso: 3 = escena 3D, 2 = hoja opaca, 1 = capa transparente ligera)
Carpeta de la Legion: GRANJA_LEGION (default ~/Sync/becario-render) con trabajos/<id>/ y resultados/<id>/.
Capacidad relativa: CAP_MAC (1.0) y CAP_LEGION (1.0; 0 = no usarla). La Zenbook ya no se usa (lenta).

Arreglos frente a los scripts sueltos de antes:
 · sin xargs ni sh -c: las rutas con espacios («terror demo») ya no truenan;
 · al recoger espera a que el .webm deje de crecer y comprueba su duración (antes se copiaban archivos de 0 bytes mientras
   Syncthing aún los pasaba);
 · revisa cuadros en blanco (capa 3D que perdió el contexto WebGL en la otra máquina) y, si los hay, la regraba en la Mac;
 · reintenta en la Mac cualquier pieza que la Legion no entregue a tiempo.
Al terminar el reparto hay que avisarle al becario el id de la tanda (lo imprime).
"""
import json, os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAP_TS = os.path.join(RAIZ, 'cli', 'animaciones', 'capturar.ts')
LEGION = os.path.expanduser(os.environ.get('GRANJA_LEGION', '~/Sync/becario-render'))
ESTADO = os.path.join(os.path.expanduser('~'), '.cache', 'granja')
ESPERA_MAX = float(os.environ.get('GRANJA_ESPERA', 3600))


def dur_de(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def en_blanco(path):
    """¿Hay cuadros con más de la mitad en blanco puro? (síntoma de capa 3D perdida)"""
    r = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-c:v', 'libvpx-vp9', '-i', path, '-vf', 'fps=2,scale=54:96,format=rgba', '-f', 'rawvideo', '-'],
                       capture_output=True)
    n = len(r.stdout) // (54 * 96 * 4)
    for k in range(n):
        f = r.stdout[k * 54 * 96 * 4:(k + 1) * 54 * 96 * 4]
        blancos = sum(1 for i in range(0, len(f), 4) if f[i] > 245 and f[i + 1] > 245 and f[i + 2] > 245 and f[i + 3] > 245)
        if blancos > .55 * 54 * 96:
            return True
    return False


def capturar(html, dur, out):
    for _ in range(2):
        r = subprocess.run(['node', CAP_TS, html, f'{float(dur):.2f}', out], capture_output=True, text=True)
        if r.returncode == 0:
            return True, r.stdout.strip()
    return False, r.stderr[-400:]


def reparte(ID, lista):
    cap = {'mac': float(os.environ.get('CAP_MAC', 1.0)), 'leg': float(os.environ.get('CAP_LEGION', 1.0))}
    if not os.path.isdir(LEGION):
        cap['leg'] = 0
    cap = {k: v for k, v in cap.items() if v > 0}
    carga = {k: 0.0 for k in cap}
    asig = {k: [] for k in cap}
    for html, dur, out, peso in sorted(lista, key=lambda x: -x[1] * x[3]):
        w = min(cap, key=lambda k: (carga[k] + dur * 30 * peso) / cap[k])
        carga[w] += dur * 30 * peso
        asig[w].append([html, dur, out, peso])
    mapa = []
    if asig.get('leg'):
        dest = os.path.join(LEGION, 'trabajos', ID)
        os.makedirs(dest, exist_ok=True)
        esc = []
        for html, dur, out, peso in asig['leg']:
            nm = os.path.basename(out)[:-5]
            shutil.copy(html, os.path.join(dest, nm + '.html'))
            esc.append({'html': nm + '.html', 'dur': dur, 'salida': nm + '.webm', 'tiene_3d': peso == 3})
            mapa.append([html, dur, out, nm + '.webm'])
        json.dump({'id': ID, 'nota': 'capturar.ts del repo; con 3D usa el envoltorio GPU; varias en paralelo, las más largas primero.', 'escenas': esc},
                  open(os.path.join(dest, 'tarea.json'), 'w'), indent=2, ensure_ascii=False)
    os.makedirs(ESTADO, exist_ok=True)
    json.dump(dict(mac=asig.get('mac', []), legion=mapa), open(os.path.join(ESTADO, f'{ID}.json'), 'w'), indent=1, ensure_ascii=False)
    for k, v in asig.items():
        print(f'{k}: {len(v)} piezas, {sum(x[1] for x in v):.1f}s')
    if mapa:
        print(f'→ avisar al becario: tanda «{ID}» en trabajos/{ID}')
    return asig.get('mac', []), mapa


def recoge(ID, mapa=None):
    if mapa is None:
        mapa = json.load(open(os.path.join(ESTADO, f'{ID}.json')))['legion']
    res = os.path.join(LEGION, 'resultados', ID)
    pend, tam, t0 = {m[3]: m for m in mapa}, {}, time.time()
    fallidas = []
    while pend and time.time() - t0 < ESPERA_MAX:
        for nm, (html, dur, out, _) in list(pend.items()):
            w, js = os.path.join(res, nm), os.path.join(res, nm[:-5] + '.json')
            if not (os.path.exists(w) and os.path.exists(js)):
                continue
            t = os.path.getsize(w)
            if t == 0 or tam.get(nm) != t:      # todavía llegando por Syncthing: esperar a que deje de crecer
                tam[nm] = t
                continue
            if dur_de(w) + .05 < float(dur):
                continue
            shutil.copy(w, out)
            if en_blanco(out):
                print(f'⚠ {nm}: capa en blanco (WebGL perdido en la Legion) → se regraba en la Mac', flush=True)
                fallidas.append((html, dur, out))
            else:
                print(f'{time.time() - t0:5.0f}s legion ✔ {nm}', flush=True)
            del pend[nm]
        if pend:
            time.sleep(10)
    fallidas += [(h, d, o) for h, d, o, _ in pend.values()]
    if pend:
        print(f'⚠ la Legion no entregó {len(pend)} piezas a tiempo → se graban en la Mac', flush=True)
    for h, d, o in fallidas:
        ok, msg = capturar(h, d, o)
        print(('✔ ' if ok else '✖ ') + (msg if not ok else f'mac (rescate) {os.path.basename(o)}'), flush=True)


def lanza(ID, lista, P):
    mac, mapa = reparte(ID, lista)
    t0 = time.time()
    with ThreadPoolExecutor(1) as rec:
        fut = rec.submit(recoge, ID, mapa) if mapa else None
        with ThreadPoolExecutor(P) as ex:
            for (h, d, o, _), (ok, msg) in zip(mac, ex.map(lambda x: capturar(x[0], x[1], x[2]), mac)):
                print(f'{time.time() - t0:5.0f}s mac {"✔" if ok else "✖"} {os.path.basename(o)}' + ('' if ok else f' {msg}'), flush=True)
        print(f'mac terminó en {time.time() - t0:.0f}s', flush=True)
        if fut:
            fut.result()
    print(f'tanda {ID} lista en {time.time() - t0:.0f}s')


def verifica(manifests, base=os.path.expanduser('~/Documents/Videos')):
    malos = 0
    for m in manifests:
        x = json.load(open(m))
        mal = []
        for o in x.get('overlays') or []:
            f = os.path.join(base, o['file'])
            if not os.path.exists(f):
                mal.append('FALTA ' + os.path.basename(f))
            elif os.path.getsize(f) == 0 or dur_de(f) + .05 < o['end'] - o['start']:
                mal.append(f'CORTO {os.path.basename(f)} ({dur_de(f):.2f}s)')
        malos += len(mal)
        print(os.path.basename(m), len(x.get('overlays') or []), 'capas', mal or 'ok')
    return malos


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    P = int(sys.argv[sys.argv.index('-P') + 1]) if '-P' in sys.argv else 6
    if cmd == 'lanza':
        lanza(sys.argv[2], json.load(open(sys.argv[3])), P)
    elif cmd == 'recoge':
        recoge(sys.argv[2])
    elif cmd == 'verifica':
        sys.exit(1 if verifica(sys.argv[2:]) else 0)
    else:
        sys.exit(__doc__)
