"""Versiones ligeras de los clips para ver en el reproductor (sobre todo en el modo de comparar con 4 manifiestos).

  python3 cli/proxies.py <manifest.json> [más manifiestos…] [--base ~/Documents/Videos] [-P 4]

Por cada clip de video crea <carpeta del clip>/.proxies/<mismo nombre>: lado corto 540 px, H.264, mismos cuadros por segundo y
mismos tiempos (los recortes del manifiesto siguen valiendo), audio AAC. Las tomas HDR se pasan a SDR con la misma LUT del
render, así la vista previa se parece al resultado. El editor normal y el render SIEMPRE usan los originales; solo el modo de
comparar busca primero en .proxies/.
"""
import argparse, json, os, subprocess
from concurrent.futures import ThreadPoolExecutor

LUTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'luts')


def trc(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=color_transfer', '-of', 'csv=p=0', path],
                       capture_output=True, text=True)
    t = r.stdout.split(',')[0].strip()
    return 'hlg' if t == 'arib-std-b67' else 'pq' if t == 'smpte2084' else None


def proxy(src):
    d, n = os.path.split(src)
    dst = os.path.join(d, '.proxies', n)
    if os.path.exists(dst) and os.path.getmtime(dst) > os.path.getmtime(src):
        return f'= {dst}'
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    esc = "scale=w='if(lt(iw,ih),540,-2)':h='if(lt(iw,ih),-2,540)'"
    h = trc(src)
    vf = esc if not h else (f"{esc}:in_color_matrix=bt2020:in_range=tv:out_range=pc,format=gbrp16le,lut3d=file='{LUTS}/{h}-a-bt709.cube',"
                            "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p")
    tmp = dst + '.tmp' + os.path.splitext(n)[1]
    r = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-hwaccel', 'videotoolbox', '-i', src, '-vf', vf, '-fps_mode', 'passthrough',
                        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', tmp],
                       capture_output=True, text=True)
    if r.returncode:
        return f'✖ {src}: {r.stderr[-300:]}'
    os.replace(tmp, dst)
    return f'✔ {dst}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('manifests', nargs='+')
    ap.add_argument('--base', default=os.path.expanduser('~/Documents/Videos'))
    ap.add_argument('-P', type=int, default=4)
    o = ap.parse_args()
    clips = []
    for mp in o.manifests:
        for c in json.load(open(mp))['clips']:
            p = os.path.join(o.base, c['file'])
            if p not in clips and os.path.exists(p) and not p.lower().endswith('.webm'):
                clips.append(p)
    with ThreadPoolExecutor(o.P) as ex:
        for r in ex.map(proxy, clips):
            print(r, flush=True)


if __name__ == '__main__':
    main()
