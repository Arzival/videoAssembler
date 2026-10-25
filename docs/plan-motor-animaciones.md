# Plan: motor de animaciones con vista previa en vivo

> **Actualización (25 oct 2026):** el zoom en frases clave (A8), el ducking de la música (A5), el render en CapCut y la
> transición «órbita» se probaron y **se descartaron**; su código se eliminó del repo. Lo que este documento diga de ellos es historia.

Este documento describe cómo pasar del flujo actual (un script por video que se graba completo para poder verlo) a un **motor de
plantillas** cuyas escenas se ven **en vivo en el reproductor web**, y solo se graban una vez, al aprobar. Incluye también las
mejoras de velocidad de la captura y el estado de las demás opciones que se evaluaron.

Índice

1. [Cómo funciona hoy](#1-cómo-funciona-hoy)
2. [Objetivos](#2-objetivos)
3. [Fase 0 · Captura más rápida](#3-fase-0--captura-más-rápida)
4. [Fase 1 · Motor de plantillas y guion en JSON](#4-fase-1--motor-de-plantillas-y-guion-en-json)
5. [Fase 2 · Vista previa en vivo en el reproductor](#5-fase-2--vista-previa-en-vivo-en-el-reproductor)
6. [Fase 3 · Plantillas dentro del reproductor (edición en vivo)](#6-fase-3--plantillas-dentro-del-reproductor-edición-en-vivo)
7. [Opciones evaluadas](#7-opciones-evaluadas)
8. [Riesgos y cómo evitarlos](#8-riesgos-y-cómo-evitarlos)
9. [Lista de pasos](#9-lista-de-pasos)
10. [Corrección y mejora del reproductor](#10-corrección-y-mejora-del-reproductor) (van primero: son cortas y se usan a diario)
11. [Mejoras adicionales (análisis de mercado)](#11-mejoras-adicionales-análisis-de-mercado)
12. [Orden general de implementación](#12-orden-general-de-implementación)

---

## 1. Cómo funciona hoy

```
voz + clips ──► transcripción (cli/transcribe.ts) ──► cortes de voz ──► piezas.json (tiempos del video final)
                                                                              │
script Python por video (cli/animaciones/ejemplos/<video>-<estilo>.py) ◄──────┘
   │  usa la librería del estilo (recorte.py, escritorio.py, plastilina.py, bauhaus.py, sombras.py)
   ▼
una página HTML por escena/tarjeta (_html/*.html, 1080×1920)
   │  cli/animaciones/capturar.ts: abre Chromium, por cada cuadro (30 fps) adelanta la animación (__seek),
   │  toma un PNG por CDP y lo guarda en disco; al final ffmpeg comprime todos los PNG a WebM VP9 con alfa
   ▼
*.webm + overlays.json ──► manifest.json ──► editor web (src/, PreviewPane reproduce los .webm) ──► cli/render.ts
```

**Dónde se pierde el tiempo:**

| Paso | Problema |
|---|---|
| Escribir el script | Cada escena se programa a mano (posiciones, tiempos, 3D). Mucho código repetido entre videos. |
| Revisar | Antes de grabar solo hay fotos sueltas (peek). Para ver el movimiento real hay que grabar. |
| Grabar | ~0.09 s/cuadro plano y bastante más con 3D. Un video de 90 s con 3D tarda varios minutos aunque solo cambie un texto. |
| Corregir | Cualquier cambio (un texto, un tiempo) obliga a regrabar la pieza completa. |

**Lo que ya existe y se reusa:**
- Las 5 librerías de estilo ya son componentes: `titular()`, `forma()`, `blq()`, `ventana()`, `N()` (contadores), capa 3D de three.js, etc.
- Todas las páginas cumplen el mismo contrato: `window.__seek(segundos)` deja la escena en ese instante y `window.__listo`
  avisa cuando cargaron fuentes y 3D. Ese contrato es justo lo que necesita un reproductor en vivo.
- El editor web (React + Vite) ya carga manifests, resuelve archivos con la File System Access API (`src/lib/mediaFolder.ts`),
  reproduce voz, música y clips, y sincroniza capas `<video>` con el cabezal (`src/components/PreviewPane.tsx`).

---

## 2. Objetivos

1. **Grabar más rápido** sin tocar la calidad ni los parámetros del VP9 (Fase 0).
2. **Armar cada video con datos, no con código:** un guion JSON con tipo de escena, textos y tiempos (Fase 1).
3. **Ver las animaciones en vivo** en el reproductor, sincronizadas con la voz, sin grabar nada (Fase 2).
4. **Editar textos y tiempos desde el reproductor** y verlos al instante (Fase 3).
5. **El render final no cambia:** al aprobar se graban las piezas y `cli/render.ts` arma el video como siempre.

El flujo de trabajo con el usuario se mantiene: yo genero un JSON, él lo carga en el reproductor, lo revisa y lo aprueba.

---

## 3. Fase 0 · Captura más rápida

Dos cambios en `cli/animaciones/capturar.ts`. Ninguno cambia el VP9 (`-crf 28 -b:v 0 -row-mt 1 -auto-alt-ref 0`, `yuva420p`).

### 3.1 No capturar cuadros repetidos

Recorte (El Log) y Plastilina mueven todo a **12 cps** a propósito (efecto hecho a mano): su `__seek` redondea el tiempo al paso
de 1/12 s. Capturamos a 30 fps, así que de cada 30 cuadros solo ~12 son distintos; los otros 18 son copias exactas.

**Contrato nuevo de la página (opcional, retrocompatible):**

```js
// cuántos pasos por segundo tiene la página (0 o ausente = todo liso, capturar cada cuadro)
window.__cps = 12
// tramos (segundos locales) donde algo va liso a propósito y hay que capturar cada cuadro
window.__liso = [[3.15, 3.60]]   // p. ej. la salida «recoge» de Plastilina
```

**En `capturar.ts`:**

```ts
const cps = await page.evaluate(() => (window as any).__cps || 0)
const liso: [number, number][] = await page.evaluate(() => (window as any).__liso || [])
let prevKey: string | null = null, prevPng: Buffer | null = null
for (let f = 0; f < frames; f++) {
  const s = f / FPS
  const enLiso = liso.some(([a, b]) => s >= a - 1e-6 && s < b)
  const key = cps && !enLiso ? `p${Math.floor(s * cps + 1e-6)}` : `f${f}`
  if (key === prevKey && prevPng) { emitir(prevPng); continue }   // mismo paso: repetir el PNG anterior
  await seek(s); prevPng = await captura(); prevKey = key; emitir(prevPng)
}
```

**Qué páginas lo declaran:**
- `recorte.py`: `JS` ya tiene `_Q = 1000/CPS` → agregar `window.__cps = CPS`. Su 3D también recibe el tiempo cuantizado, así que entra completo.
- `plastilina.py`: igual; las escenas que usan la salida lisa (`escena()` de `ejemplos/video11-plastilina.py`) agregan su tramo a `__liso`.
- `escritorio.py`, `bauhaus.py`, `sombras.py`: no lo declaran (sus movimientos son lisos o a pasos irregulares) y se capturan como hoy.

**Ganancia esperada:** en Recorte y Plastilina, ~60 % menos capturas (la captura es la parte cara del 3D).

### 3.2 Comprimir mientras se captura

Hoy los PNG se escriben en una carpeta temporal y ffmpeg arranca hasta el final. Cambio: abrir ffmpeg al inicio y mandarle cada
PNG por la entrada estándar.

```ts
const ff = spawn(FFMPEG, ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
  '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-b:v', '0', '-crf', '28', '-row-mt', '1', '-auto-alt-ref', '0', out])
const emitir = async (png: Buffer) => { if (!ff.stdin.write(png)) await once(ff.stdin, 'drain') }   // respetar la contrapresión
// …al terminar: ff.stdin.end(); await once(ff, 'close'); revisar el código de salida
```

- Se elimina la carpeta temporal de PNG (menos disco y menos E/S).
- Si ffmpeg falla a media captura: matar Chromium, borrar la salida parcial y salir con error (los guiones ya reintentan).
- Los reintentos actuales de carga (`for intento…`) se quedan igual.

**Ganancia esperada:** desaparece casi todo el tiempo de compresión al final (ocurre en paralelo con la captura).

### 3.3 Cómo medirlo y aceptarlo

1. Elegir piezas que ya existen: una escena 3D de El Log #09 (`ejemplos/ellog-09-recorte3d.py e03-preview`) y una escena de
   Plastilina del video 11 (`ejemplos/video11-plastilina.py e1-semana`).
2. Grabar cada una con el `capturar.ts` actual y con el nuevo, anotando el tiempo (`time`).
3. Comparar el resultado cuadro por cuadro con `ffmpeg -c:v libvpx-vp9 -i X.webm -f framemd5 -`:
   - 3.2 solo debe dar **cuadros idénticos** (misma entrada, mismos ajustes).
   - 3.1 también debe dar cuadros idénticos, porque los cuadros saltados eran copias exactas. Si alguno difiere, esa página
     tiene algo que no está cuantizado y hay que agregarlo a `__liso`.
4. Aceptar si los cuadros son idénticos y el tiempo baja. Anotar las cifras en la memoria de la granja para recalcular repartos.

### 3.4 Lo que queda fuera de esta fase

- **Ajustes de velocidad del VP9** (`-cpu-used`, `-deadline`): no aprobados; el usuario los quiere probar con el video del RAG.
- **Escenas opacas sin alfa**, **reusar el navegador entre piezas**, **bajar el supermuestreo 3D**: mejoras menores, para después.

---

## 4. Fase 1 · Motor de plantillas y guion en JSON

### 4.1 Idea

Cada estilo trae un **catálogo de plantillas de escena** con su animación, colores y 3D ya resueltos. Un video deja de ser un
script y pasa a ser un **guion JSON**: lista de escenas, cada una con su plantilla, sus textos y en qué segundo aparece cada cosa.
El motor convierte el guion en las mismas páginas HTML de siempre (mismo contrato `__seek`/`__listo`), así que la captura, el
manifest y el render no cambian.

### 4.2 Estructura de archivos

```
cli/animaciones/motor/
  motor.py              # lee el guion, valida, llama a la plantilla de cada escena, escribe HTML + overlays.json
  esquema.py            # validación del guion (tipos, campos obligatorios, tiempos dentro del video)
  tiempos.py            # resuelve "en la palabra X" → segundo, usando la transcripción con tiempos por palabra
  plantillas/
    recorte.py          # titular, cifra, comparacion, lista, cita, logo_dato, antes_despues, sigueme, cabecera
    escritorio.py       # ventana_titular, dialogo, progreso, terminal, comparacion, resumen, barra, mesa
    plastilina.py       # tarjeta_dato, escena_pasos, cifra, comparacion, sigueme
    bauhaus.py          # bloque_dato, specs, comparacion, escena_libre, sigueme
    sombras.py          # narracion, aparicion, silueta, titulo_capitulo
guiones/                # (en la carpeta de cada video) guion.json
```

Las plantillas son funciones de Python que reciben los datos de la escena y devuelven el HTML del cuerpo usando las librerías de
estilo que ya existen (`recorte.titular`, `bauhaus.forma`, etc.). No se reescribe ningún estilo.

### 4.3 Esquema del guion

```jsonc
{
  "video": "noticias/10",
  "estilo": "recorte",            // un estilo por video (regla de estilos oficiales)
  "fin": 92.95,                   // duración del video final
  "transcripcion": "voz/palabras.json",   // tiempos por palabra (para resolver "palabra")
  "escenas": [
    {
      "id": "e01-app",
      "plantilla": "cifra",
      "capa": "pantalla",         // pantalla = escena completa · tarjeta = encima de la cámara (transparente)
      "inicio": 12.86, "fin": 23.76,
      "fondo": "negra",           // opciones propias de la plantilla/estilo
      "datos": {
        "titulo": ["Claude en tu", "*teléfono*"],          // *x* = acento del estilo
        "cifra": { "de": 0, "a": 503, "formato": "miles", "en": { "palabra": "quinientas" } },
        "nota": "según Anthropic"
      },
      "3d": { "objeto": "appicon", "logo": "claude", "color": "#d97757" },
      "fases": [                   // cambios dentro de la escena (cada frase nueva)
        { "en": 19.4, "datos": { "titulo": ["Para negocios", "*pequeños*"] } }
      ]
    },
    {
      "id": "e02-libre",
      "plantilla": "libre",        // vía de escape: escena hecha a mano
      "funcion": "ejemplos/ellog-10-recorte.py:escena_mapa",
      "inicio": 23.76, "fin": 40.78
    }
  ]
}
```

Reglas del esquema:
- `inicio < fin`, dentro de `[0, fin del video]`; escenas de `capa: pantalla` consecutivas se encadenan solas (la cola de cada
  estilo, `COLA`, la agrega el motor, no el guion).
- Cualquier tiempo puede ser un número o `{ "palabra": "…", "n": 1, "desfase": -0.1 }`; `tiempos.py` lo convierte al segundo
  donde empieza esa palabra (la `n`-ésima aparición dentro de la escena).
- `datos` se valida contra la firma de la plantilla: si falta un campo obligatorio o sobra uno desconocido, el motor falla con
  un mensaje claro antes de generar nada.
- `plantilla: "libre"` llama a una función de Python que devuelve el cuerpo HTML; sirve para escenas que no caben en el catálogo
  (por ejemplo la recámara del Inventario #1).

### 4.4 Catálogo inicial (Recorte, para El Log)

| Plantilla | Para qué | Datos principales |
|---|---|---|
| `titular` | Abrir una noticia | `titulo` (líneas), `marca` (palabra a resaltar), `sello`, `3d` |
| `cifra` | Un número protagonista | `titulo`, `cifra {de,a,formato,en}`, `nota` |
| `comparacion` | A contra B | `a {titulo,puntos}`, `b {titulo,puntos}`, `ganador` |
| `lista` | Pasos o puntos | `titulo`, `items[] {texto,en}` |
| `cita` | Frase textual | `texto`, `autor` (solo si está confirmado) |
| `logo_dato` | Empresa + dato | `logo`, `dato`, `contexto` |
| `antes_despues` | Cambio | `antes`, `despues`, `tachar` |
| `sigueme` | Cierre | `pregunta`, `respuesta_tecleada` |
| `cabecera` | Cinta/cabecera de la edición | `titulares[] {texto,desde}` |

Cada plantilla se saca de escenas reales ya aprobadas (El Log #04–#09) para que el resultado se vea igual que hoy.

### 4.5 Cómo se usa

```bash
python3 cli/animaciones/motor/motor.py ~/Documents/Videos/noticias/10/guion.json            # genera HTML + overlays.json + manifest
python3 cli/animaciones/motor/motor.py … --capturar [ids…]                                   # graba (con la Fase 0)
python3 cli/animaciones/motor/motor.py … --solo e01-app                                      # regenera una escena
```

Salida: `animaciones/_html/<id>.html`, `animaciones/overlays.json` y el `manifest.json` del video (ver 5.1).

### 4.6 Orden de los estilos

1. **Recorte** (El Log): el que más escenas a pantalla completa tiene; es donde más se nota el ahorro.
2. **Escritorio** (El Readme).
3. **Plastilina** (devlogs): pocas piezas por video, pero se reusa la salida lisa.
4. **Bauhaus** (Inventario): tarjetas sobre cámara + una escena.
5. **Sombras** (terror): el más particular; puede quedarse con más `libre`.

Para cada estilo: (a) listar las escenas aprobadas de los últimos videos, (b) agruparlas en plantillas, (c) escribir la
plantilla, (d) regenerar un video ya entregado con el motor y comparar contra el original (hoja de cuadros lado a lado).

---

## 5. Fase 2 · Vista previa en vivo en el reproductor

**Paso 1 de la vista previa.** El motor sigue generando las páginas HTML; el reproductor las muestra en vivo encima del video,
sincronizadas con el cabezal. No hay que grabar para revisar.

### 5.1 Extensión del manifest (retrocompatible)

```ts
// src/lib/types.ts
export interface OverlaySpec {
  file?: string        // .webm grabado (como hoy)
  html?: string        // página HTML de la escena (relativa a la carpeta de medios), para verla en vivo
  start: number
  end: number
  trimIn: number
  scale: number
  position: OverlayPosition
}
```

- Un overlay puede tener `html`, `file` o los dos. Mientras se revisa: solo `html`. Al aprobar: el motor graba y agrega `file`.
- `cli/render.ts` y `src/lib/graph.ts` siguen usando `file`. Si un overlay no tiene `file`, `render.ts` falla con un mensaje
  claro («falta grabar ginv1-c03-cara: corre motor.py --capturar»). Opción futura: que `render.ts` llame a la captura solo.
- Manifests viejos (solo `file`) funcionan igual.

### 5.2 Capa HTML en `PreviewPane`

Componente nuevo `src/components/HtmlOverlay.tsx`:

1. **Carga:** lee el HTML desde la carpeta de medios (mismo `mediaFolder.ts` que ya resuelve los videos) y lo monta en un
   `<iframe>` con una URL `blob:` (mismo origen, así el reproductor puede llamar funciones de la página). Las fuentes de Google
   y three.js vienen de CDN con URL absoluta, así que funcionan dentro del blob.
2. **Tamaño:** el iframe mide 1080×1920 y se escala con `transform: scale(anchoPreview / 1080)` para encajar en el cuadro del
   preview; `pointer-events: none`, fondo transparente.
3. **Listo:** espera `window.__listo` (fuentes y 3D) antes de mostrarse; mientras, muestra un indicador «cargando escena».
4. **Sincronía:** en cada cambio del cabezal y en cada `requestAnimationFrame` mientras reproduce:
   ```ts
   const local = playhead - o.start
   win.document.getAnimations().forEach((a) => { a.pause(); a.currentTime = local * 1000 })
   win.__seek?.(local)
   ```
   Es exactamente lo que hace `capturar.ts`, así que lo que se ve en vivo es lo mismo que se grabará (incluido el paso de 12 cps).
5. **Visibilidad:** solo se ve dentro de `[start, end)`.

### 5.3 Rendimiento del preview

- **Montaje perezoso:** solo existen los iframes de escenas que empiezan en los próximos ~5 s o terminaron hace menos de ~2 s.
  Chrome limita los contextos WebGL (~16); sin esto, un El Log con muchas escenas 3D se quedaría sin contextos.
- **Modo preview en la página:** el reproductor abre la escena con `#preview`; las librerías de estilo lo leen y bajan el
  supermuestreo del 3D (`setPixelRatio(1)` en vez de 2) y las sombras. La grabación final sigue en calidad completa.
- Si una escena pesada va lenta, el reproductor salta cuadros de esa capa (la voz manda); para revisar el movimiento cuadro a
  cuadro se pausa y se arrastra el cabezal.

### 5.4 Cambios en el resto del editor

- `src/state.ts`: `OverlayState` admite `html` además del archivo de video; al cargar el manifest se resuelven ambos.
- `src/components/TimelinePane.tsx`: las escenas HTML se dibujan como bloques en la pista de overlays (con su `id`).
- `src/components/TopBar.tsx`: interruptor **«En vivo / Grabado»** cuando un overlay tiene los dos (para comparar).
- `src/components/ManifestHelp.tsx`: documentar el campo `html`.

### 5.5 Flujo de trabajo con la Fase 2

1. Yo: audio limpio → transcripción → `guion.json` → `motor.py` → `manifest.json` con overlays `html`. **Sin grabar.**
2. Él: carga el manifest en el reproductor, lo ve en vivo con su voz y me dice qué cambiar.
3. Yo: cambio el guion y regenero (segundos, no minutos); él recarga.
4. Al aprobar: `motor.py --capturar` (con la Fase 0 y, si conviene, la Legion) → overlays con `file` → `render.ts`.

---

## 6. Fase 3 · Plantillas dentro del reproductor (edición en vivo)

**Paso 2 de la vista previa.** Las plantillas viven en el propio reproductor, así que textos y tiempos se editan ahí mismo.

### 6.1 Una sola fuente de verdad en TypeScript

- Pasar las librerías de estilo y las plantillas de Python a TypeScript (`src/motor/estilos/*.ts`, `src/motor/plantillas/*.ts`).
  Son generadores de HTML/CSS/JS en texto, así que el paso es mecánico; el JS de las páginas (`__seek`, 3D) no cambia.
- El reproductor genera el HTML de cada escena en memoria a partir del guion y lo monta en el iframe (`srcdoc`/blob).
- La captura usa **el mismo código**: un script de Node (`cli/motor.ts`) genera los HTML con esos módulos y llama a
  `capturar.ts`. Así lo que se ve en el reproductor y lo que se graba no pueden diferir.
- `motor.py` queda como envoltorio delgado (o se retira) cuando todos los estilos estén en TS.

### 6.2 Edición

- **Inspector** (`src/components/Inspector.tsx`): al seleccionar una escena muestra sus campos (`titulo`, `cifra`, `items`…)
  según la firma de la plantilla; al escribir, la escena se regenera y se ve al instante.
- **Línea de tiempo:** arrastrar los bordes de una escena cambia `inicio`/`fin`; las fases aparecen como marcas dentro del
  bloque. Si se carga la transcripción, se muestran las palabras para alinear a mano.
- **Guardar:** descargar el `guion.json` o, con permiso de escritura de la File System Access API, guardarlo directo en la
  carpeta del video. Yo lo leo de ahí para grabar y renderizar.

### 6.3 Criterios para empezar la Fase 3

Solo cuando la Fase 2 esté en uso real y el catálogo de plantillas sea estable (si las plantillas cambian cada semana, portar a
TS antes de tiempo duplica trabajo).

---

## 7. Opciones evaluadas

| Opción | Estado | Notas |
|---|---|---|
| Render en CapCut (`cli/capcut.py`) | **Descartado** (24 oct 2026) | Funcionó técnicamente (proyecto generado desde el manifest, CapCut lo abrió), pero en TikTok se vio igual: la pérdida es de la compresión de TikTok. El script queda guardado. |
| Transición «órbita» tipo Higgsfield (`cli/animaciones/orbita.py`, `cli/orbita_clips.py`) | **Descartado** | Probada en El Log, Readme y devlog; no le gustó en ningún estilo. |
| HyperFrames (HeyGen) | Histórico | Nos dio la idea base (animación como página web → video transparente) y las primeras notificaciones. Hoy todo sale de nuestros estilos y `capturar.ts`. |
| Remotion (React) | No recomendado | Tiene reproductor en vivo, pero habría que rehacer los 5 estilos; la Fase 2/3 da lo mismo sobre lo nuestro. |
| Render a 2K (1440×2560) | Pendiente de prueba | TikTok no documenta si conserva más que 1080p. Requiere grabar las animaciones a 1440 (≈1.8× píxeles). Probar con un Readme subido en privado en 1080 y 2K. |
| Ajustes de velocidad del VP9 | Pendiente | No aprobados; se probarán con el video del RAG. |
| Captura: saltar cuadros repetidos + comprimir en paralelo | **Aprobado para implementar** | Fase 0 de este plan. |

---

## 8. Riesgos y cómo evitarlos

| Riesgo | Mitigación |
|---|---|
| El vivo y lo grabado se ven distintos | Misma rutina de sincronía que `capturar.ts`; en Fase 3, mismo código para generar el HTML. Interruptor «En vivo / Grabado» para comparar. |
| Límite de contextos WebGL en el reproductor | Montaje perezoso de iframes (5.3). |
| Escenas 3D pesadas trabadas en el preview | Modo `#preview` con menos supermuestreo; la voz manda y la capa salta cuadros. |
| Escenas que no caben en una plantilla | Plantilla `libre` con una función a mano. |
| Plantillas que se vuelven rígidas y todo se ve igual | Variantes por plantilla (disposición, color, 3D) y revisar cada mes qué escenas `libre` conviene convertir en plantilla. |
| Saltar cuadros que no eran copias | Verificación con `framemd5` (3.3) y tramos `__liso` declarados por la página. |
| Romper manifests viejos | `html` es opcional; `file` sigue funcionando igual. |
| Repo público | El guion y los HTML no llevan datos personales; las rutas son relativas a la carpeta de medios. |

---

## 9. Lista de pasos

### Fase 0 · Captura más rápida
- [x] Medir los tiempos actuales de `ellog-09-recorte3d.py e03-preview` y `video11-plastilina.py e1-semana`.
- [x] `capturar.ts`: ffmpeg por tubería (`image2pipe`), contrapresión, limpieza ante errores, sin carpeta temporal.
- [x] `capturar.ts`: leer `__cps` y `__liso`; repetir el PNG cuando el paso no cambia.
- [x] `recorte.py` y `plastilina.py`: declarar `window.__cps`; escenas con salida lisa declaran `__liso`.
- [x] Verificar con `framemd5` que los cuadros son idénticos; medir de nuevo. *(Con 3D la captura vieja tampoco es idéntica entre dos corridas; se comparó con PSNR: ~50 dB, igual que entre dos capturas viejas.)*
- [x] Actualizar `cli/animaciones/README.md` y la memoria de la granja con los tiempos nuevos.

### Fase 1 · Motor de plantillas
- [x] `motor/esquema.py` y `motor/tiempos.py` (resolver tiempos por palabra con la transcripción).
- [x] `motor/motor.py`: guion → HTML + `overlays.json` + `manifest.json`; opciones `--solo` y `--capturar`.
- [x] Plantillas de Recorte a partir de escenas aprobadas de El Log #04–#09.
- [x] Regenerar El Log #09 con el motor y comparar contra el original.
- [ ] Usarlo en el siguiente El Log real.
- [ ] Repetir para Escritorio, Plastilina, Bauhaus y Sombras (en ese orden). *(Bauhaus hecho, con paridad exacta; faltan Escritorio, Plastilina y Sombras.)*

### Fase 2 · Vista previa en vivo
- [x] `types.ts`: `html` opcional en `OverlaySpec`; `render.ts` falla claro si falta `file`.
- [x] `HtmlOverlay.tsx`: iframe blob escalado, espera `__listo`, sincronía por cabezal y `requestAnimationFrame`.
- [x] Montaje perezoso y modo `#preview` en las librerías de estilo.
- [x] `state.ts`, `TimelinePane.tsx`, `TopBar.tsx` (interruptor En vivo / Grabado), `ManifestHelp.tsx`. *(El interruptor quedó como aviso bajo la barra superior; la línea de tiempo ya dibujaba las capas.)*
- [x] Probar con El Log regenerado: escenas 3D, cabecera, Sígueme; comparar contra lo grabado.
- [ ] Usarlo en el siguiente video real (sin grabar hasta aprobar).

### Fase 3 · Edición en el reproductor
- [ ] Portar estilos y plantillas a TypeScript (`src/motor/`), empezando por el estilo más usado.
- [ ] `cli/motor.ts`: misma generación desde Node para la captura.
- [ ] Inspector con campos por plantilla, arrastre de tiempos en la línea de tiempo, palabras de la transcripción.
- [ ] Guardar `guion.json` en la carpeta del video.
- [ ] Retirar `motor.py` cuando todos los estilos estén en TS.

---

## 10. Corrección y mejora del reproductor

Una corrección (10.1) y una mejora (10.2); van **antes de la Fase 0**: son cambios acotados del editor web y se usan en cada revisión.

### 10.1 Corrección: cargar un manifest mientras se reproduce deja el reproductor congelado

**Síntoma:** con un manifest reproduciéndose, se carga otro (arrastrándolo o con el botón). El reproductor sigue «andando» pero
la imagen se congela; hay que darle pausa y otra vez play para que arranque.

**Causa (revisada en el código):**
- `loadManifest()` en `src/App.tsx` reemplaza `clips`, `voice`, `music` y `overlays` y regresa el cabezal a 0, pero **no detiene
  la reproducción**.
- En `src/components/PreviewPane.tsx` la reproducción vive en el estado `seq` (índice del clip que suena). Si `seq` ya valía,
  por ejemplo, 3 y el manifest nuevo también tiene un clip 3, el efecto de `seq` no se vuelve a disparar: el listener
  `timeupdate` sigue amarrado al clip viejo (`clipCleanup`) y el `<video>` cambia de archivo sin que nadie le dé `play()`.
- Además, los archivos del manifest nuevo se resuelven después (`resolveFromFolder` en un `setTimeout`): en ese momento los
  clips aún no tienen `url`, y la voz y la música cambian de `src` mientras el estado dice que se está reproduciendo.
- Resultado: estado «reproduciendo» con medios en pausa o sin fuente. Pausa + play llama a `stopAll()` y `playAll()`, que
  limpian todo, y por eso «lo arregla».

**Corrección:**
1. Exponer `stop()` en el `playerRef` de `PreviewPane` (hoy solo hay `toggle` y `seek`); `stop()` = `stopAll()` (quita
   listeners, pausa video/voz/música/capas y pone `seq = null`).
2. En `loadManifest()`, **lo primero** es `playerRef.current?.stop()`; después se reemplaza el estado.
3. Defensa adicional en `PreviewPane`: un contador `manifestId` (prop nueva, sube en cada `loadManifest`) y un efecto que, si
   cambia, llama a `stopAll()` y limpia `overlayRefs`. Así cualquier otra forma de reemplazar el proyecto (autoguardado,
   comparación) queda cubierta.
4. Opcional: si estaba reproduciendo al cargar, recordar `seguir = true` y, cuando terminen de resolverse los archivos del
   manifest nuevo (todos los clips con `url`), arrancar desde 0 solo. Si no, queda en pausa en 0.

**Cómo probarlo:**
- Reproducir el manifest A, arrastrar B a media reproducción: B queda en pausa en 0 (o arranca solo, si se activa el punto 4),
  sin congelarse, y al darle play corre normal.
- Lo mismo con A y B de distinta cantidad de clips (B con menos clips que el índice que sonaba en A).
- Lo mismo cargando B con el botón en vez de arrastrar, y con archivos que aún no estaban en la bandeja.

### 10.2 Mejora: comparar hasta 4 manifests al mismo tiempo

**Para qué:** cuando se piden varias pruebas del mismo video (por ejemplo el mismo El Log en Recorte, Escritorio, Plastilina y
Bauhaus), verlas lado a lado y sincronizadas en vez de una por una.

**Cómo se ve:**
- Botón **«Comparar»** en la barra superior (o soltar de 2 a 4 archivos `.json` a la vez).
- Hasta **4 paneles verticales en una fila** (en pantallas angostas, cuadrícula 2×2), cada uno con el nombre de su manifest
  arriba y una ✕ para quitarlo.
- **Un solo control** de reproducción y un solo cabezal: play, pausa, arrastrar y las flechas mueven los 4 a la vez, en el
  mismo segundo del video final.
- **Audio de un solo panel** (el marcado con 🔊; se cambia con un clic) para no oír 4 voces encimadas. Los demás van en
  silencio.
- Si los manifests duran distinto, los más cortos se quedan en su último cuadro.
- Atajo para pasar un panel a pantalla completa y regresar a la comparación.
- Es **solo para ver**: para editar se abre ese manifest en el editor normal.

**Implementación:**
1. **Separar el estado de un proyecto.** Hoy el estado del manifest vive suelto en `App.tsx` (`clips`, `voice`, `music`,
   `overlays`, `playhead`…). Moverlo a un hook `useProyecto()` (y la carga a `cargarManifest(m)` dentro del hook) para poder
   tener varias instancias. El editor normal usa una; la comparación, hasta 4.
2. **Medios compartidos.** Las pruebas casi siempre usan los mismos clips, voz y música. Una caché común (por nombre de archivo
   y carpeta de medios) entrega el mismo `blob:` URL a todos los paneles: el archivo se lee una sola vez.
3. **Componente `CompararPane`** con un `PreviewPane` por manifest. Cada panel recibe el mismo `playhead` y un `reloj`
   compartido.
4. **Reloj maestro.** El panel con audio es el maestro: su voz marca el tiempo. Cada ~250 ms los demás comparan su posición con
   el maestro y, si se desfasan más de 80 ms, se recolocan (`seek`) sin detenerse. En pausa, todos se colocan exacto en el
   cabezal.
5. **Capas.** Los `.webm` de cada manifest se sincronizan igual que hoy, por panel. Con la Fase 2 (escenas HTML en vivo), el
   montaje perezoso cuenta las escenas 3D de **todos** los paneles juntos para no pasar del límite de contextos WebGL.
6. **Carga.** `onDrop` en `App.tsx` hoy toma el primer `.json`; con 2–4 `.json` abre la comparación. El botón «Comparar»
   permite agregar uno por uno (y los recientes del autoguardado).

**Rendimiento y cómo evitar que se trabe:**
- 4 videos 4K HEVC decodificándose a la vez es pesado. La Mac lo decodifica por hardware, pero si se traba, **modo ligero**:
  yo genero versiones chicas de los clips (540×960, H.264) para las pruebas y el manifest de prueba las usa. El render final
  siempre usa los originales.
- Las capas `.webm` de animación son ligeras; el peso está en los clips de cámara.

**Cómo probarlo:**
- Cargar los 4 manifests de `manifest de prueba/el-log-08-*.json`: arrancan juntos, el cabezal mueve los 4, cambiar el audio
  de panel no corta la reproducción, y tras 2 minutos ningún panel se desfasa más de un cuadro o dos.
- Quitar un panel a media reproducción y agregar otro: no se congela (usa la misma limpieza de 10.1).

### 10.3 Lista de pasos

- [x] 10.1: `stop()` en `playerRef`; `loadManifest()` detiene antes de reemplazar; efecto por `manifestId` en `PreviewPane`.
- [ ] 10.1: (opcional) seguir reproduciendo desde 0 cuando el manifest nuevo termine de cargar. *(No se hizo: queda en pausa en 0.)*
- [x] 10.1: probar los tres casos de arriba.
- [x] 10.2: hook `useProyecto()` y caché de medios compartida. *(Sin tocar el estado del editor: `CompararPane` lleva su propio estado y caché.)*
- [x] 10.2: `CompararPane` con hasta 4 `PreviewPane`, control único, audio seleccionable, reloj maestro.
- [x] 10.2: botón «Comparar» y soltar varios `.json`.
- [x] 10.2: modo ligero con versiones chicas de los clips (si hace falta tras probar con 4 en paralelo).
- [ ] 10.2: probar con los manifests de El Log #08. *(Probado con clips de prueba en navegador automático; con tus clips reales falta que lo abras tú: la carpeta conectada necesita tu clic.)*

---

## 11. Mejoras adicionales (análisis de mercado)

Salen de comparar lo que tenemos con lo que ofrecen las herramientas para videos cortos (Submagic, OpusClip, Gling, FireCut,
Vizard, CapCut) y con lo que se ha pedido en las entregas. Lo que ya es nuestro y el mercado no da: 5 estilos propios con 3D,
animaciones a la medida de cada frase, voz sincronizada por correlación, render propio y granja de captura.

Lo que el mercado da por hecho y nos falta: subtítulos con estilo, detección automática de tomas malas, variantes de gancho,
música que se agacha con la voz, portadas y exportación por plataforma. (Las fuentes del análisis son en su mayoría blogs de los
propios vendedores: se toma como tendencia, no como dato medido.)

### 11.A Funciones nuevas

#### A1. Subtítulos en el estilo de cada sección
- **Qué:** subtítulos palabra por palabra (2–4 palabras visibles, la que suena resaltada) quemados en el video, con la
  tipografía y colores del estilo de la sección (Recorte, Escritorio, Plastilina, Bauhaus, Sombras).
- **Cómo:** `cli/subtitulos.py` toma la transcripción por palabra del audio ya recortado (los tiempos del video final que ya
  calculamos para las animaciones), agrupa en frases cortas respetando pausas y puntuación, y genera una capa HTML transparente
  por estilo (`<estilo>.subtitulos(palabras)`) que se graba como un overlay más (o se ve en vivo con la Fase 2).
- **Reglas:** zona fija (tercio inferior, por encima de la interfaz de TikTok y debajo de las tarjetas); se esconden durante
  las escenas a pantalla completa que ya tienen texto grande; corrección de nombres y términos con un diccionario por canal
  (`subtitulos-diccionario.json`: «Claude», «homelab», marcas) antes de quemarlos.
- **Opción por video:** `subtitulos: true|false` en el guion; arranca apagado hasta que se apruebe el look en una prueba.
- **Aceptación:** prueba en un El Log y un devlog vistos con el modo de comparar (con y sin subtítulos).

#### A2. Detector automático de errores de voz
- **Qué:** reporte de arranques fallidos, frases repetidas, frases cortadas y muletillas sueltas **antes** de armar el manifest.
- **Cómo:** `cli/revisar-voz.ts` (o `.py`):
  1. Detecta tramos de habla por RMS (−40 dB, ventanas de 25 ms) y los parte en frases por pausas > 0.35 s.
  2. Transcribe **cada frase por separado** (así Whisper no junta el intento fallido con el bueno).
  3. Marca: frase que empieza igual que la siguiente (≥ 3 palabras comunes al inicio), frase sin cierre seguida de otra que la
     repite completa, repeticiones inmediatas («y si y si»), palabras sueltas aisladas («Bien.», «y»), frases idénticas en
     distintas tomas (la primera suele ser la mala).
  4. Propone qué cortar (con tiempos) y genera un HTML/MD de revisión con el texto de cada empalme.
  5. Tras cortar, vuelve a transcribir solo los empalmes (±2.2 s) y confirma que no hay palabras mochas.
- **Integración:** paso obligatorio de la directiva base; su salida va en la entrega («qué se cortó»).
- **Aceptación:** en el audio del video 11 debe detectar solo los dos arranques que se cortaron a mano
  («y recuerda que también tengo un proceso…» y «Luego, otro saca las huellas de…»).

#### A3. Revisión automática antes de entregar
- **Qué:** un comando que revise el video (o el manifest) antes de decir «listo».
- **Cómo:** `cli/revisar-entrega.ts <manifest> [--video final.mp4]`:
  - Saca cuadros de cada corte de clip, cada entrada/salida de overlay y cada transición (±0.3 s) y arma una hoja de contacto.
  - Detecta cuadros negros o blancos (luma media < 8 o > 247), capas 3D en blanco (contexto WebGL perdido), overlays que se
    enciman en la misma zona, huecos sin clip, overlays que terminan después del final.
  - Audio: muestras > 1.0, pico, picos de volumen de la música frente a la voz.
  - Compara duración de voz, clips y música.
  - Salida: `revision/` con la hoja de contacto, un `reporte.md` con advertencias y código de salida ≠ 0 si hay errores graves.
- **Aceptación:** en el render de prueba del video 11 previo a la corrección, debe señalar los tropiezos de las salidas de
  pantalla completa.

#### A4. Variantes del gancho
- **Qué:** 2–3 versiones de los primeros 2–3 s (otro titular, otra toma de apertura, otra primera animación) del mismo video.
- **Cómo:** el guion admite `variantes_gancho: [...]`; el motor genera un manifest por variante en `manifest de prueba/` y se
  comparan con el modo de 4 manifests (10.2). La variante elegida se integra al manifest final.

#### A5. Música que se agacha con la voz (*ducking*)
- **Qué:** la música baja sola cuando hablas y sube un poco en las pausas, en vez de ir a volumen fijo (0.04).
- **Cómo:** en `cli/render.ts` / `src/lib/graph.ts`, `sidechaincompress` de ffmpeg con la voz como señal de control
  (umbral, ataque ~20 ms, liberación ~300 ms) o una envolvente calculada por RMS de la voz. Campo nuevo en el manifest:
  `music.ducking: { nivelVoz: 0.04, nivelPausa: 0.09 }`. Sin el campo, todo como hoy.
- **Aceptación:** sin saturación (> 1.0) y voz igual de clara; prueba A/B con el modo de comparar.

#### A6. Portada automática
- **Qué:** imagen de portada 1080×1920 por video: un cuadro de la toma + titular en el estilo de la sección.
- **Cómo:** `cli/portada.py`: elige 3 cuadros candidatos (nítidos, sin movimiento, con cara/gadget al centro) y genera 3
  portadas con la plantilla del estilo; se graban como PNG en `final/`.

#### A7. Biblioteca de rellenos
- **Qué:** catálogo de los clips de `ayuda/` (y tomas sobrantes) con descripción, resolución, fps, HDR/SDR y duración.
- **Cómo:** `cli/biblioteca.py` genera `ayuda/catalogo.json` (ffprobe + un cuadro por clip + descripción corta). Al armar un
  video, propone rellenos por tema y avisa si un clip es 1080p o de otra cámara (para no mezclar calidades).

#### A8. Zoom en frases clave (opcional, a prueba)
- **Qué:** acercamiento suave (105–112 %) en la cámara durante frases importantes. Es solo movimiento, sin color.
- **Cómo:** campo `zoom: [{inicio, fin, escala, centro}]` en los clips del manifest; `graph.ts` lo aplica con `zoompan`/`scale`
  + `crop` animados. **Primero en una prueba**, por la regla de no meter filtros a las tomas.

### 11.B Rendimiento

| # | Mejora | Cómo | Ganancia |
|---|---|---|---|
| B1 | Saltar cuadros repetidos y comprimir mientras se captura | Fase 0 (sección 3) | ~½ en Recorte/Plastilina; casi todo el tiempo de compresión |
| B2 | No regrabar lo que no cambió | Hash (SHA-1) del HTML + duración + versión de `capturar.ts`; si existe `<pieza>.webm` con el mismo hash en `.hash`, se reusa | En rondas de corrección solo se graban las escenas tocadas |
| B3 | Versiones ligeras para el reproductor | `cli/proxies.ts`: 540×960 H.264 de cada clip (en `.proxies/`); el editor las usa si existen; el render siempre usa los originales | Reproductor fluido con 4K y en el modo de comparar |
| B4 | Transcripción sin ciclos | `transcribe.ts` parte el audio largo por silencios (VAD por RMS) en trozos de ≤ 30 s, transcribe cada uno y une los tiempos | Se acaba el ciclo/alucinación de Whisper en audios largos |
| B5 | Reparto automático a la Legion | Cola por Syncthing que vigila `trabajos/`, avisa sola, recoge, corre `verifica.py` y reintenta los «CORTO»; quitar la dependencia de `lanza.sh`/xargs | Menos pasos manuales; usarla en más videos |
| B6 | Reusar el navegador entre piezas | Un Chromium por proceso de captura con páginas nuevas por pieza | 1–2 s por pieza |
| B7 | Escenas opacas sin alfa | Pantallas completas opacas: VP9 `yuv420p` sin canal alfa | Compresión y archivos más ligeros |

(Los ajustes de velocidad del VP9 siguen pendientes de la prueba con el video del RAG.)

### 11.C Correcciones

#### C1. HDR en el render (urgente)
- **Problema:** desde el Inventario #1 graba en **HDR (HLG, 10 bits)**. Ese video lo exportó CapCut, que convirtió solo a SDR.
  `cli/render.ts` no convierte HLG → SDR, así que el próximo devlog saldría lavado o con colores raros.
- **Cómo:** detectar por clip `color_transfer=arib-std-b67` (HLG) o `smpte2084` (PQ) con ffprobe y aplicar la conversión
  estándar a BT.709 antes de escalar: `zscale=t=linear:npl=203 → tonemap (hable o mobius, desat=0) → zscale=t=bt709:m=bt709:p=bt709:r=tv`.
  Si el ffmpeg instalado no trae `zscale`, usar `libplacebo` o instalar un ffmpeg con zimg. Es conversión de formato, no un
  filtro de estilo: el objetivo es que se vea como en el iPhone (avisarle al aplicarla por primera vez).
- **Aceptación:** comparar cuadros del render contra la exportación de CapCut del Inventario #1 (brillo y contraste
  parecidos, sin lavado); clips SDR intactos.

#### C2. Reproductor congelado al cargar otro manifest
- Ver 10.1.

#### C3. Granja
- `lanza.sh` truena con rutas con espacios («terror demo») → usar el repartidor en Python (o B5).
- `recoge.py` copia `.webm` de 0 bytes si Syncthing aún no termina → esperar a tamaño estable y correr `verifica.py` siempre.
- Contexto WebGL perdido en la Legion → `capturar.ts` ya truena; agregar reintento automático de la pieza en otra máquina.

#### C4. Limpieza del repo (público)
- Borrar los `*.err` sueltos de la raíz y agregarlos a `.gitignore`.
- Ordenar los cambios sin commit (estilos, ejemplos, `capcut.py`, `orbita*.py`) en commits por tema, sin datos personales
  (IPs, IDs de Syncthing) y sin atribución de IA en los mensajes.

---

## 12. Orden general de implementación

> Estado al 25 oct 2026: ver `docs/reporte-implementacion.md`.

Cuando se dé luz verde, este es el orden propuesto (cada bloque se cierra con su prueba antes de pasar al siguiente):

1. **C1** HDR en el render (bloquea el siguiente devlog).
2. **10.1 / C2** corrección del reproductor.
3. **A2** detector de errores de voz.
4. **A3** revisión automática antes de entregar.
5. **10.2** modo de comparar hasta 4 manifests (+ **B3** versiones ligeras si hace falta).
6. **Fase 0 / B1** captura más rápida, **B2** no regrabar lo que no cambió, **B6**, **B7**.
7. **A1** subtítulos en el estilo de cada sección (con prueba de look).
8. **B4** transcripción sin ciclos, **C3** granja, **B5** reparto automático, **C4** limpieza del repo.
9. **Fase 1** motor de plantillas (Recorte primero).
10. **Fase 2** vista previa en vivo.
11. **A5** ducking, **A6** portada, **A7** biblioteca, **A4** variantes del gancho, **A8** zoom (a prueba).
12. **Fase 3** edición en el reproductor.
