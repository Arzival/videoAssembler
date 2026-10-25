"""Validación del guion antes de generar nada: errores claros en vez de escenas rotas."""


class ErrorGuion(Exception):
    pass


def validar(g, plantillas, fin=None):
    errores = []
    for k in ('estilo', 'fin', 'escenas'):
        if k not in g:
            errores.append(f'falta «{k}» en el guion')
    if errores:
        raise ErrorGuion('\n'.join(errores))
    fin = fin or g['fin']
    ids = set()
    for i, e in enumerate(g['escenas']):
        donde = f'escena {i + 1} ({e.get("id", "sin id")})'
        if 'id' not in e:
            errores.append(f'{donde}: falta «id»')
        elif e['id'] in ids:
            errores.append(f'{donde}: id repetido')
        ids.add(e.get('id'))
        p = e.get('plantilla')
        if p not in plantillas:
            errores.append(f'{donde}: plantilla «{p}» no existe en el estilo {g["estilo"]} (hay: {", ".join(sorted(plantillas))})')
            continue
        req, opc = plantillas[p].get('req', ()), plantillas[p].get('opc', ())
        datos = e.get('datos', {})
        for r in req:
            if r not in datos:
                errores.append(f'{donde}: la plantilla «{p}» necesita datos.{r}')
        sobran = set(datos) - set(req) - set(opc)
        if sobran:
            errores.append(f'{donde}: datos desconocidos para «{p}»: {", ".join(sorted(sobran))} (acepta: {", ".join(list(req) + list(opc))})')
        for k in ('inicio', 'fin'):
            if not isinstance(e.get(k), (int, float)):
                errores.append(f'{donde}: «{k}» debe ser un número de segundos (ya resuelto)')
        if isinstance(e.get('inicio'), (int, float)) and isinstance(e.get('fin'), (int, float)):
            if not 0 <= e['inicio'] < e['fin'] <= fin + .01:
                errores.append(f'{donde}: tiempos fuera de rango ({e["inicio"]}–{e["fin"]}, video de {fin}s)')
    if errores:
        raise ErrorGuion('\n'.join(errores))
