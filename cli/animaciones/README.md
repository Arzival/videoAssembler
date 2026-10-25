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

## El Log (sección semanal de noticias)

`ellog.py` define la identidad de la sección: cada noticia es una entrada de `git log` (hash + número), terminal oscura con acento verde, logos oficiales de `logos/` (Simple Icons, CC0). Aquí las escenas a pantalla completa son las protagonistas (~85 % del video) y los clips solo asoman en momentos puntuales con alguna tarjeta encima. Piezas fijas: `intro()` (índice de la semana) y `cierre()` (resumen; deja arriba libre para «Sígueme»). El contenido de cada semana va en `ejemplos/ellog-NN.py` con tiempos del video final; al correrlo sin ids escribe `overlays.json` listo para el manifiesto. Las escenas consecutivas se encadenan (`sigue=True`) para no asomar el clip entre una y otra.

## Estilos de edición

Cada estilo es una librería de Python que arma páginas HTML de 1080×1920 (escenas y capas) con su propio sistema visual. Los guiones de cada video viven en `ejemplos/<video>-<estilo>.py`, siempre con la misma interfaz:

```bash
SALIDA=videos/N/animaciones REL=videos/N/animaciones python3 cli/animaciones/ejemplos/ellog-09-recorte3d.py [ids…]
# SOLO_HTML=1 → solo escribe los .html para revisarlos en el navegador, sin capturar
# sin ids → escribe además overlays.json con start/end listos para pegar en el manifiesto
```

Todos los tiempos de un guion están en **segundos del video final**; cada escena convierte a tiempo local con `A(t)`.

| Estilo | Librería | Idea | Para qué |
|---|---|---|---|
| **Recorte** | `recorte.py` | Collage editorial + tipografía cinética a 12 cps: papel, cinta, marcatextos, garabatos que se dibujan, sellos, tickets de terminal, números gigantes. La hoja nueva entra rasgada. | Noticias (El Log). Estilo oficial. |
| **Recorte 3D** | `recorte.py` con `page(..., js3d=…)` | Lo mismo con una capa three.js de piezas de papel/cartón (`P.recorte`, `P.caja`, `P.hoja`, `P.avion`, `P.laptop`…). | Noticias con objetos que «salen» de la hoja. Estilo oficial. |
| **Escritorio** | `escritorio.py` | Un SO retro inventado (LogOS, tipo System 7 / Win 98): ventanas biseladas que abren con rectángulos de zoom, texto que se teclea, diálogos, barras de progreso, cursor que hace clic. Letra Jersey 15. | Temas técnicos y conceptos (El Readme). Estilo oficial. |
| **Bauhaus** | `bauhaus.py` | Geometría plana, primarios sobre crema, retícula; las formas encajan con rebote y los textos se revelan con una barra de color. Transición: círculo que crece desde una esquina. | En prueba: datos y números (especiales, reseñas). |
| **Plastilina** | `plastilina.py` | Claymation 3D mate, pastel, rebotes que aplastan, stop-motion a 12 cps con temblor de mano. Transición: mancha de plastilina. | En prueba: devlogs. |
| Gloss | `gloss.py`, `ellog_gloss.py` | Vidrio, lienzo teñido y capa 3D brillosa (estilo anterior). | Histórico; con `transiciones.py` (`TRANS=desliz\|ensamble`) se le quitan los fundidos. |

Reglas comunes a todos los estilos:
- **Nada se desvanece entre escenas.** Las piezas salen, entran y se arman; cada estilo trae su transición propia.
- **Una escena por idea, sincronizada con la frase** (ubícala con `cli/transcribe.ts`). Escenas consecutivas se encadenan para no asomar la cámara entre una y otra.
- **Nada de teléfonos dibujados**, zona segura libre a la derecha y abajo.

## Reglas de robustez (aprendidas a la mala)

La captura es cuadro por cuadro (`window.__seek`) y casi siempre en paralelo; lo que funciona viendo la página en el navegador puede fallar capturando. Las librerías ya traen esto, pero si escribes páginas nuevas:

- **Animaciones Web (WAAPI) en pausa y con `persist()`.** Con varias capturas en paralelo, Chrome descarta las animaciones terminadas y la pieza desaparece a medio video. Créalas con `pause()`, `currentTime = 0` y `persist()`, y muévelas solo desde `__seek`.
- **Fuentes obligatorias.** `window.__listo` carga cada fuente y **lanza un error** si falta alguna (`document.fonts.check`). Una captura con la fuente de respaldo sale con letras anchas y textos cortados; mejor que falle y se reintente.
- **Contexto WebGL perdido.** Con varias capas 3D a la vez la GPU puede tirar el contexto y la capa sale en blanco. Las páginas marcan `window.__perdido` en `webglcontextlost` y revisan `isContextLost()` en cada cuadro para fallar en vez de grabar cuadros vacíos.
- **Revisa antes de entregar:** duración de cada `.webm` contra el manifiesto, y que ningún cuadro salga totalmente blanco o transparente por error (una hoja de contacto con ffmpeg basta).

## Captura en paralelo

`capturar.ts` toma cada cuadro directo por CDP (`Page.captureScreenshot` con `optimizeForSpeed`), ~8× más rápido que `page.screenshot()` con 3D y desenfoques. Lanza varias capturas a la vez (una por núcleo, aprox.); las escenas con 3D pesan ~3× lo que una capa transparente, así que ordénalas de la más costosa a la más barata. Si tienes otras máquinas con Chrome y GPU, el mismo `capturar.ts` corre ahí: basta con copiar el `.html` (es autocontenido salvo fuentes de Google y three.js desde CDN) y traer de vuelta el `.webm`.

## Motor de plantillas (`motor/`)

`python3 cli/animaciones/motor/motor.py <guion.json> [--capturar] [--solo id1,id2]` convierte un guion JSON en las mismas páginas
HTML de siempre (contrato `__seek`/`__listo`), escribe `overlays.json` y, con `manifest_base`, un manifiesto con cada capa con `html`
(para verla en vivo en el reproductor) y `file` (el `.webm` que tendrá al grabarse). Tiempos: segundos o `{"palabra": "x", "n": 1,
"desfase": -0.1}` resueltos contra la transcripción del audio final. `variantes_gancho` genera un manifiesto extra por variante.
- Recorte: `fases` (genérica, reproduce cualquier escena hecha a mano) y `titular`, `cifra`, `comparacion`, `lista`, `cita`,
  `logo_dato`, `antes_despues`; capas `sigueme` y `cabecera`. Ejemplos: `noticias/9/guion-motor.json` (réplica exacta de El Log #09)
  y `noticias/9/guion-plantillas.json`.
- Bauhaus: `tarjeta`, `escena`, `dato`, `sigueme`. Ejemplo: `inventario/1/guion-motor.json`.
- `js3d` en una escena = JS propio (vía de escape); `html` en una pieza = HTML propio.

## Captura (`capturar.ts`)

- Los PNG van a ffmpeg por tubería mientras se captura. Si la página declara `window.__cps` (Recorte y Plastilina: 12), los cuadros del
  mismo paso se repiten sin volver a capturar; `window.__liso = [[a, b]]` marca tramos que van lisos a propósito.
- Huella `<salida>.huella`: si el HTML, la duración y el formato no cambiaron, se reusa el `.webm` (`NO_CACHE=1` obliga a regrabar).
- `--lote piezas.json` graba varias piezas con un solo navegador. Ajustes del VP9 sin cambios.
- `foto.ts pagina.html salida.png [t]`: foto fija de una página (portadas, revisiones).
