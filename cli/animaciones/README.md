# Animaciones integradas (opcional)

Elementos animados que se ponen **encima del video** como capas (`overlays` del manifiesto) o que lo **tapan unos segundos** como escenas explicativas mientras la voz sigue. Se diseñan en HTML/CSS, se capturan cuadro por cuadro a WebM con transparencia y se previsualizan en el editor web **sin renderizar** (el render final se hace al aprobar).

```bash
node cli/animaciones/capturar.ts elemento.html 6.5 elemento.webm          # 1 elemento
SALIDA=videos/N/animaciones python3 cli/animaciones/tarjetas.py [ids…]   # lote de tarjetas
SALIDA=videos/N/animaciones python3 cli/animaciones/escenas.py  [ids…]   # lote de escenas
```

En el manifiesto: `{ "file": "videos/N/animaciones/x.webm", "start": 27.3, "end": 33.8, "trimIn": 0, "scale": 1, "position": "center" }` (`start`/`end` en segundos del video final; ubica las frases con `cli/transcribe.ts`).

## Criterio editorial (lo que funcionó)

- **Integrado, no decorativo.** Cada elemento representa algo REAL de lo que se está diciendo: una notificación que llega, el chat donde se manda el prompt, el widget de métricas, el formulario del encargo, la ficha de la app. Texto suelto flotando encima se ve básico — evitarlo.
- **Un solo sistema visual.** Tarjetas estilo notificación macOS ×1.7: 646 px de ancho, arriba y centradas (top 198 px), fondo `rgba(30,30,30,.86)`, radio 27 px, Inter, entran desde la derecha y salen igual. El contenido anima por dentro (contadores, texto que se escribe, switches, barras que se llenan, listas que aparecen escalonadas).
- **Escenas a pantalla completa** para procesos que la cámara no muestra (un pipeline, una comparación, un flujo de datos): fondo oscuro con retícula, titulares grandes que narran cada paso sincronizados con la voz, elementos conectados con líneas y partículas. 10–20 s.
- **Densidad:** en ~3 min, ~10–12 momentos con aire entre ellos. Ni todo el tiempo ni 4 sueltos.
- **Historias encadenadas:** si algo tiene inicio y fin (confirmación → terminado), dos elementos que se respondan.
- **Cierre neutral** (sirve para TikTok, Instagram y Shorts): tarjeta «Sígueme» con un dedo que toca Seguir → like → comentario.
- **Zona segura:** nada pegado a la derecha ni muy abajo (ahí van los botones de cada red).

## Archivos

- `capturar.ts` — HTML animado → WebM VP9 con alfa (Chromium controlado; `window.__seek(s)` para contadores en JS).
- `tarjetas.py`, `escenas.py` — generadores con el sistema visual (CSS base) y los elementos del video 5 como ejemplo.
- `ejemplos/video5/` — los HTML finales del video 5 (servidor, métricas, encargo, Qstify, notas, seguir y 3 escenas): plantillas para copiar y adaptar.
- `hyperframes/` — notificaciones (Telegram, capturas) hechas con un bloque de [HyperFrames](https://github.com/heygen-com/hyperframes): `notificacion.html` (bloque adaptado: ícono de Telegram y cuerpo `__BODY__`) y `generar.py` (renderiza bloques del catálogo, recorta su contenido y lo recoloca en vertical). Requiere `npx hyperframes init` + `npx hyperframes add <bloque>` en `HF_PROYECTO`.
