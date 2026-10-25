# Reporte de implementación · 25 oct 2026

> **Actualización (25 oct 2026):** el zoom en frases clave (A8), el ducking de la música (A5), el render en CapCut y la
> transición «órbita» se probaron y **se descartaron**; su código se eliminó del repo. Lo que este documento diga de ellos es historia.

Implementación del plan de `docs/plan-motor-animaciones.md`, en el orden de su sección 12. Ningún video final entregado se tocó.

## Resumen

| Bloque | Estado | Prueba |
|---|---|---|
| C1 · HDR en el render | ✅ hecho · **espera tu visto bueno** | Mismo brillo y contraste que la exportación de CapCut |
| 10.1 · Reproductor congelado | ✅ hecho | Navegador automático: se detiene, vuelve a 0 y arranca bien |
| A2 · Detector de errores de voz | ✅ hecho | Video 11: encontró justo los 8 tramos que se cortaron a mano, sin falsos |
| A3 · Revisión antes de entregar | ✅ hecho | Detectó un tropiezo simulado; en el video 11 encontró un destello negro real |
| 10.2 · Comparar hasta 4 manifests (+ B3) | ✅ hecho | 3 paneles sincronizados; quitar uno a media reproducción no lo congela |
| Fase 0 · Captura más rápida (B1, B2, B6) | ✅ hecho · B7 no | −36 % a −43 % de tiempo, misma calidad |
| A1 · Subtítulos | ✅ prueba de look · **espera tu visto bueno** | 2 manifests de prueba |
| B4 · Transcripción sin ciclos | ✅ hecho | 8 min 20 s de audio en 22 trozos, sin repeticiones |
| C3 + B5 · Granja | ✅ hecho | Legion simulada: archivo a medias, capa en blanco y pieza faltante |
| Fase 1 · Motor de plantillas | ✅ Recorte y Bauhaus · faltan 3 estilos | Réplica de El Log #09 y de Inventario #1: idénticas píxel por píxel |
| Fase 2 · Vista previa en vivo | ✅ hecho | Escena 3D en vivo, sincronizada, con fuentes y three.js |
| A5 · Música que se agacha | ✅ hecho · **espera tu visto bueno** | Baja ~10 dB al hablar y sube en las pausas |
| A6 · Portada automática | ✅ hecho | 3 portadas del Inventario #1 |
| A7 · Biblioteca de rellenos | ✅ hecho | 19 tomas de `ayuda/` descritas y con avisos |
| A4 · Variantes del gancho | ✅ hecho | 3 versiones de la apertura de El Log #09 |
| A8 · Zoom en frases clave | ✅ prueba · **espera tu visto bueno** | Acerca justo lo pedido solo en los tramos marcados |
| Fase 3 · Edición en el reproductor | ⏸ no empezada | El plan pide antes usar la Fase 2 en un video real |

## Detalle por bloque

### C1 · HDR en el render
- Desde el Inventario #1 grabas en HDR (HLG, 10 bits). Este ffmpeg no trae `zscale`, así que la conversión va en una tabla de
  colores (`cli/luts/hlg-a-bt709.cube`, generada por `cli/luts/generar.py`). La tabla se calibró contra la exportación de CapCut
  del Inventario #1 y quedaron casi iguales en brillo y en blancos con detalle.
- `render.ts` detecta solo las tomas HDR y las convierte antes de renderizar, varias a la vez y con decodificación por hardware.
  Los intermedios quedan en `<salida>/.hdr-cache`.
  - **Tiempos del Inventario #1 (85 s):** 21 min convirtiendo dentro del render → 7.5 min la primera vez → 1 min cuando ya
    está en caché.
  - **Etiqueta de color:** el video sale marcado como BT.709. Antes heredaba la etiqueta HLG de las tomas y los reproductores lo
    interpretaban mal.
- **Para tu visto bueno:** `~/Documents/Videos/inventario/1/prueba-hdr/inventario1-vertical.mp4`. Es solo conversión de formato,
  no un filtro: la idea es que se vea como en tu iPhone.
- Detalle: comparado con la conversión directa, en un tramo puede quedar un cuadro (16 ms) corrido. No se nota con la voz.

### 10.1 · Reproductor congelado al cargar otro manifest
- **Causa:** el índice del clip que sonaba sobrevivía al cambio de manifest.
- **Arreglo:** al cargar, primero se detiene todo y el cursor vuelve a 0. También se ignoran los avisos de tiempo atrasados del
  video viejo.
- **Prueba:** con el manifest A reproduciéndose se cargó B, que quedó detenido en 0:00 y al darle play corrió desde 0.
- No se hizo lo opcional (que el manifest nuevo arranque solo).

### A2 · Detector de errores de voz (`cli/revisar-voz.py`)
- Transcribe cada frase por separado y marca:
  - arranques fallidos, también con una palabra distinta («para ver en un minuto…» → «para ver un minuto…»)
  - tomas repetidas
  - repeticiones inmediatas
  - palabras sueltas
  - ruido que Whisper convierte en texto inventado («¡Gracias!», «Suscríbete»)
- **Video 11:** marcó los 8 tramos que se cortaron a mano (incluidos los dos arranques que se me habían pasado) y ningún falso.
- **Inventario #1:** marcó la primera toma de «Todos tenemos un gadget…» y todos los ruidos sueltos.
- Salida: `revision-voz.md` (para leer) y `.json` (con propuesta de cortes).

### A3 · Revisión automática antes de entregar (`cli/revisar-entrega.py`)
- Revisa:
  - micro-clips
  - capas encimadas
  - cuadros negros o blancos
  - capas 3D en blanco
  - «tropiezos» (un fragmento corto de otra toma que asoma)
  - pico de audio
- Arma una hoja de contacto de cada corte y de cada entrada y salida de capa.
- **Prueba:** detectó el tropiezo que simulé en el video 11 y no marcó nada en la versión buena.
- **Hallazgo real en el video 11 ya entregado:** a 1:09.6 hay un destello negro de 0.2 s entre las escenas «texto» y «huellas».
  La primera se recoge y la segunda entra sobre el negro (es la parte sin toma). No lo toqué.

### 10.2 · Comparar hasta 4 manifests (+ B3 versiones ligeras)
- **Cómo se abre:** con el botón **Comparar** o soltando de 2 a 4 `.json` a la vez.
- **Control:** uno solo; espacio, ← y → mueven todos los paneles. Los paneles que no son el maestro se recolocan si se desfasan
  más de 80 ms.
- **Audio:** sale solo del panel marcado con 🔊.
- **Paneles:** cualquiera se puede ampliar a pantalla completa (⤢) o quitar (✕).
- Las escenas del motor también se ven en vivo aquí.
- **Versiones ligeras:** `cli/proxies.py` crea copias chicas (lado corto de 540 px) en `.proxies/` junto a cada clip. Solo el modo
  de comparar las usa; el editor normal y el render usan los originales. Ya están hechas las del video 11.
- Pendiente: probarlo tú con manifests reales (la carpeta conectada necesita tu clic).

### Fase 0 · Captura más rápida
- `capturar.ts`:
  - manda los PNG a ffmpeg mientras captura
  - repite el cuadro anterior en los estilos de 12 cps (Recorte y Plastilina), respetando la salida lisa de Plastilina
  - reusa los `.webm` cuyo HTML no cambió (huella)
  - tiene un modo por lotes con un solo navegador
- **Tiempos:** escena 3D de El Log #09 de 4:02 a 2:36 (−36 %); escena de Plastilina de 1:45 a 1:00 (−43 %).
- **Calidad:** con 3D, dos capturas viejas de la misma escena tampoco salen idénticas. Comparando, la nueva difiere de la vieja lo
  mismo que dos viejas entre sí (~50 dB, imposible de ver).
- **B7 (escenas opacas sin alfa) no se hizo:** cambia un ajuste del VP9 y eso no está aprobado.
- La Legion tiene su propia copia del repo; para que use la captura nueva hay que sincronizarle `cli/animaciones/capturar.ts`.

### A1 · Subtítulos (prueba de look, `cli/subtitulos.py`)
- Palabra por palabra en el estilo de la sección, resaltando la que suena. Se esconden en las escenas a pantalla completa y
  corrigen términos con `cli/subtitulos-diccionario.json` (Cloud → Claude, powerbands → powerbanks…).
- **Manifests de prueba:**
  - `manifest de prueba/video11-subtitulos.json` (Plastilina)
  - `manifest de prueba/inventario1-subtitulos.json` (Bauhaus)
- **Ojo:** en Inventario el tercio inferior es donde enseñas los gadgets, así que los subtítulos los tapan. Si te gustan, habría que
  moverlos de lugar en esa sección.

### B4 · Transcripción sin ciclos
- `transcribe.ts` parte solo los audios de más de 30 s, cortando en silencios. El micro del video 11 (8:20) salió en 22 trozos sin
  repeticiones.

### C3 + B5 · Granja (`cli/granja.py`)
- Reparte entre la Mac y la Legion (la Zenbook ya no). Ya no usa xargs, así que las rutas con espacios funcionan.
- Al recoger:
  - espera a que cada archivo deje de crecer y revisa su duración
  - detecta capas 3D en blanco y las regraba en la Mac
  - regraba en la Mac lo que la Legion no entregue a tiempo
- Probado con una Legion simulada. Avisarle al becario sigue siendo un mensaje mío: el script imprime el id de la tanda.
- La detección de capas en blanco podría regrabar sin necesidad una escena de Escritorio con una ventana blanca enorme. Eso
  cuesta tiempo, no calidad.

### Fase 1 · Motor de plantillas (`cli/animaciones/motor/`)
- **Cómo funciona:** guion JSON → mismas páginas HTML de siempre → `overlays.json` y manifiesto. Los tiempos pueden ir amarrados a
  palabras (`{"palabra": "tres"}`). El guion se valida con mensajes claros antes de generar nada.
- **Recorte:**
  - la plantilla genérica `fases` reproduce El Log #09 **idéntico píxel por píxel** (`noticias/9/guion-motor.json`)
  - 7 plantillas de alto nivel: titular, cifra, comparación, lista, cita, logo con dato y antes/después
  - demo: `noticias/9/guion-plantillas.json` → `manifest de prueba/el-log-09-plantillas.json`
- **Bauhaus:** tarjeta, escena, dato y sígueme. La réplica de dos piezas del Inventario #1 sale idéntica
  (`inventario/1/guion-motor.json`).
- **Pendiente:** plantillas de Escritorio, Plastilina y Sombras, y usarlo en el siguiente video real.

### Fase 2 · Vista previa en vivo
- Las capas del manifest pueden traer `html`, y el reproductor la muestra en vivo, sincronizada con la voz, sin haberla grabado.
  Se mueve igual que en la grabación, así que se ve lo mismo que se va a grabar.
- Solo monta las escenas cercanas al cursor, por el límite de 3D de Chrome. En la vista previa el 3D baja su supermuestreo.
- Si una capa tiene `html` y `.webm`, sale un interruptor «En vivo / Grabado».
- Si falta grabar alguna escena, `render.ts` avisa claro qué correr.
- Para verlo: abre `manifest de prueba/el-log-09-plantillas.json` con la carpeta de videos conectada.

### A5 · Música que se agacha con la voz
- En el manifiesto: `music.ducking = {"nivelVoz": 0.04, "nivelPausa": 0.10}`.
- **Medido:** la música baja ~10 dB mientras hablas (el objetivo eran 8) y en las pausas queda en 0.10. La voz no cambia y no satura.
- **Para tu visto bueno:** `manifest de prueba/inventario1-ducking.json`.
- El reproductor del editor no aplica el ducking; solo se oye en el render.

### A6 · Portada (`cli/portada.py`)
- Elige 3 cuadros nítidos y quietos, distintos entre sí y sin capas encima (con `--manifest`). Encima pone el titular en el estilo,
  ajustado al ancho.
- Las del Inventario #1 están en `inventario/1/prueba-hdr/portada-1..3.png`.

### A7 · Biblioteca de rellenos (`cli/biblioteca.py`)
- `ayuda/catalogo.json` con las 19 tomas descritas, temas y avisos (9 en 1080p, 3 a 30 fps, 7 HDR horizontales). Tiene búsqueda
  por tema y las descripciones se conservan al volver a catalogar.

### A4 · Variantes del gancho
- `variantes_gancho` en el guion genera un manifest extra por variante.
- **Demo de El Log #09:**
  - `el-log-09-plantillas.json` (titular)
  - `-b.json` (antes/después)
  - `-c.json` (logo con dato)

### A8 · Zoom en frases clave (a prueba)
- `clips[].zoom = [{desde, hasta, escala, centro}]`: entra en 0.4 s, se sostiene y sale. Se trabaja al doble de tamaño para que no
  tiemble.
- **Para tu visto bueno:** `manifest de prueba/inventario1-zoom.json`, con zoom en «25 mil miliamperios» y en «165 W».

## Lo que espera tu visto bueno
1. **Conversión HDR** → `inventario/1/prueba-hdr/inventario1-vertical.mp4`
2. **Subtítulos** → `manifest de prueba/video11-subtitulos.json` y `inventario1-subtitulos.json`
3. **Música que se agacha** → `manifest de prueba/inventario1-ducking.json`
4. **Zoom** → `manifest de prueba/inventario1-zoom.json`
5. **Portadas** → `inventario/1/prueba-hdr/portada-*.png`
6. **Motor y vista previa en vivo** → `manifest de prueba/el-log-09-plantillas.json` y sus variantes `-b` y `-c`

## Pendientes
- Plantillas del motor para Escritorio, Plastilina y Sombras.
- Fase 3 (edición en el reproductor): esperar a usar la Fase 2 en un video real.
- B7 (escenas sin alfa) y los ajustes de velocidad del VP9: necesitan aprobación.
- Probar el modo de comparar con tus clips reales.
- Sincronizar `capturar.ts` en la Legion.

## Archivos nuevos o cambiados
- **Nuevos:**
  - en `cli/`: `revisar-voz.py`, `revisar-entrega.py`, `subtitulos.py`, `subtitulos-diccionario.json`, `portada.py`,
    `biblioteca.py`, `proxies.py`, `granja.py`, `luts/`
  - en `cli/animaciones/`: `foto.ts`, `motor/`
  - en `src/components/`: `CompararPane.tsx`, `HtmlOverlay.tsx`
- **Cambiados:**
  - `cli/`: `render.ts`, `transcribe.ts`, `animaciones/capturar.ts`, `animaciones/recorte.py`, `animaciones/plastilina.py`,
    `animaciones/ejemplos/video11-plastilina.py`
  - `src/`: `lib/graph.ts`, `lib/types.ts`, `lib/mediaFolder.ts`, `state.ts`, `App.tsx`, `components/PreviewPane.tsx`,
    `components/TopBar.tsx`, `components/ManifestHelp.tsx`, `index.css`
  - documentación: los dos README y este plan
- **Material de prueba en `~/Documents/Videos`:**
  - `inventario/1/prueba-hdr/`
  - `inventario/1/subtitulos/` y `videos/11/subtitulos/`
  - `videos/11/.proxies/`
  - `noticias/9/animaciones-motor/` y `animaciones-plantillas/`
  - `inventario/1/animaciones-motor/`
  - `ayuda/catalogo.json` y `ayuda/.biblioteca/`
  - los manifests nuevos en `manifest de prueba/`
