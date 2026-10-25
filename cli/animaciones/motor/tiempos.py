"""Tiempos del guion: un número (segundos del video final) o una palabra de la transcripción.

  {"palabra": "quinientas", "n": 1, "desfase": -0.1}
    → segundo donde empieza la n-ésima aparición de esa palabra a partir del inicio de la escena (+ desfase).

La transcripción es la del audio FINAL (render o voz ya recortada): {"words": [{"word", "start", "end"}]} (cli/transcribe.ts)
o {"palabras": [[palabra, inicio, fin]]} (cli/subtitulos.py).
"""
import json, re, unicodedata


def norm(t):
    t = unicodedata.normalize('NFD', str(t).lower())
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9ñ]+', '', t)


def cargar(path):
    if not path:
        return []
    d = json.load(open(path))
    if 'words' in d:
        return [(norm(w['word']), w['start'], w['end']) for w in d['words']]
    return [(norm(w), a, b) for w, a, b in d.get('palabras', [])]


class ErrorTiempo(Exception):
    pass


def resolver(v, palabras, desde=0.0):
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, dict) and 'palabra' in v:
        if not palabras:
            raise ErrorTiempo(f'el guion usa {{"palabra": "{v["palabra"]}"}} pero no hay transcripción ("transcripcion" en el guion)')
        objetivo, n, vistas = norm(v['palabra']), int(v.get('n', 1)), 0
        for w, a, _ in palabras:
            if a + 1e-6 >= desde and w == objetivo:
                vistas += 1
                if vistas == n:
                    return round(a + float(v.get('desfase', 0)), 2)
        raise ErrorTiempo(f'no encontré «{v["palabra"]}» (aparición {n}) después de {desde:.2f}s')
    raise ErrorTiempo(f'tiempo inválido: {v!r}')


def resolver_todo(obj, palabras, desde=0.0):
    """Reemplaza en cualquier parte del objeto los {"palabra": …} por segundos."""
    if isinstance(obj, dict):
        if 'palabra' in obj and set(obj) <= {'palabra', 'n', 'desfase'}:
            return resolver(obj, palabras, desde)
        return {k: resolver_todo(v, palabras, desde) for k, v in obj.items()}
    if isinstance(obj, list):
        return [resolver_todo(x, palabras, desde) for x in obj]
    return obj
