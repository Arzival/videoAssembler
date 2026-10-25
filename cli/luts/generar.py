"""Genera las LUT 3D (.cube) que pasan tomas HDR del iPhone a SDR BT.709 en el render (cli/render.ts las usa solas).

El ffmpeg de Homebrew no trae zscale/libplacebo, así que la conversión estándar va en una tabla:
  entrada  = R'G'B' BT.2020 codificado en HLG (ARIB STD-B67) o PQ (SMPTE ST 2084), rango completo 0–1
  1. a luz lineal (OETF⁻¹ de HLG + OOTF con gamma de sistema 1.2 a 1000 nits · o EOTF de PQ en nits)
  2. REF nits → blanco SDR (1.0); el estándar BT.2408 usa 203, pero las tomas del iPhone quedan claras y lavadas: con 400
     el brillo medio y los blancos quedan como en la exportación de CapCut
  3. gama BT.2020 → BT.709 (matriz lineal), negativos a 0
  4. compresión suave de altas luces por canal máximo (conserva el tono) de RODILLA hacia TOPE
  5. codificación SDR con gamma 2.4 (BT.1886)
Es conversión de formato, no un filtro de estilo: la idea es que se vea como en el iPhone.
Uso: python3 cli/luts/generar.py   (escribe hlg-a-bt709.cube y pq-a-bt709.cube junto a este archivo)
"""
import math, os

N = 33
REF = 400.0          # nits que se vuelven blanco SDR (calibrado contra la exportación de CapCut del Inventario #1)
PICO_HLG = 1000.0    # nits de pico del sistema HLG
RODILLA = 0.25       # desde dónde se comprimen las altas luces (lineal SDR)
TOPE = 0.60          # a dónde tienden las altas luces (lineal SDR): blancos con detalle, sin quemarse
M2020_709 = ((1.6605, -0.5876, -0.0728), (-0.1246, 1.1329, -0.0083), (-0.0182, -0.1006, 1.1187))
A, B, C = 0.17883277, 0.28466892, 0.55991073


def hlg_lineal(rgb):
    e = [x * x / 3 if x <= .5 else (math.exp((x - C) / A) + B) / 12 for x in rgb]
    ys = .2627 * e[0] + .6780 * e[1] + .0593 * e[2]
    g = ys ** .2 if ys > 0 else 0.0          # OOTF: gamma de sistema 1.2
    return [v * g * PICO_HLG / REF for v in e]


def pq_lineal(rgb):
    m1, m2, c1, c2, c3 = 2610 / 16384, 2523 / 4096 * 128, 3424 / 4096, 2413 / 4096 * 32, 2392 / 4096 * 32
    out = []
    for x in rgb:
        p = max(x, 0) ** (1 / m2)
        out.append(10000 * (max(p - c1, 0) / (c2 - c3 * p)) ** (1 / m1) / REF)
    return out


def a_sdr(lin):
    r, g, b = (max(0.0, sum(M2020_709[i][j] * lin[j] for j in range(3))) for i in range(3))
    m = max(r, g, b)
    if m > RODILLA:
        k = RODILLA
        m2 = k + (TOPE - k) * math.tanh((m - k) / (TOPE - k))
        r, g, b = r * m2 / m, g * m2 / m, b * m2 / m
    return [min(1.0, v) ** (1 / 2.4) for v in (r, g, b)]


def escribe(nombre, f):
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), nombre)
    with open(ruta, 'w') as o:
        o.write(f'TITLE "{nombre[:-5]}"\nLUT_3D_SIZE {N}\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n')
        for bi in range(N):
            for gi in range(N):
                for ri in range(N):   # en .cube el rojo cambia más rápido
                    o.write('%.6f %.6f %.6f\n' % tuple(a_sdr(f([ri / (N - 1), gi / (N - 1), bi / (N - 1)]))))
    print(ruta)


if __name__ == '__main__':
    escribe('hlg-a-bt709.cube', hlg_lineal)
    escribe('pq-a-bt709.cube', pq_lineal)
