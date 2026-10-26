# Video Assembler

<p align="center">
  <img src="docs/img/motor-el-log-10.gif" alt="Tres escenas verticales animadas en estilo collage: «Arc se apaga el 22 de dic», «Todo a Dia» y «Te quedan 2 meses»" width="100%">
  <br><sub>Escenas que el motor generó a partir de un guion JSON anclado a la voz (El Log #10, estilo Recorte).</sub>
</p>

Editor de video pensado para que **una IA (Claude Code u otro agente) arme los videos** y una persona los revise y apruebe.
Sirve para videos verticales u horizontales hechos de tomas de cámara, una nota de voz, música y animaciones encima.

Todo gira alrededor de un **manifiesto** (un JSON que describe el video completo):

- La IA lo escribe a partir de lo que pide la persona y de la transcripción de la voz.
- La persona lo abre en el **editor web** para verlo, compararlo y ajustarlo sin renderizar.
- El **CLI** lo renderiza con ffmpeg nativo cuando está aprobado.

Las animaciones (tarjetas, escenas a pantalla completa, subtítulos) se escriben en HTML/CSS, se ven **en vivo** en el
editor y se graban a WebM transparente solo al aprobarlas.

Licencia MIT. Todo corre en local: no hay backend ni se sube material a ningún servidor.

---

## 🤖 Si eres una IA: empieza aquí

### Orden de lectura

1. **Este README**: qué hay y cómo se usa cada pieza.
2. [`manifiesto.md`](manifiesto.md): la especificación del manifiesto.
   - Cada campo y la semántica de tiempos: todos los tiempos son segundos del **archivo fuente**, salvo los de las capas, que son del video final.
   - Una guía de tareas comunes.
   - **Léelo antes de escribir cualquier manifiesto.**
3. `src/lib/graph.ts`: la fuente de verdad del render. Traduce el manifiesto a argumentos de ffmpeg, y lo comparten el editor y el CLI.
4. [`cli/animaciones/README.md`](cli/animaciones/README.md): solo si vas a hacer animaciones. Trae los estilos, el motor de plantillas, las reglas de captura y lo aprendido a la mala.

### Cómo trabajar con la persona

- **Primero el manifiesto, el render al final.** Entrega un `.json` para que lo abra en el editor y lo vea. Renderiza solo
  cuando lo apruebe: un render 4K tarda minutos y la vista previa es instantánea.
- **Varias propuestas → modo Comparar.** Si haces 2–4 versiones, entrégalas como manifiestos separados. Antes, genera sus
  versiones ligeras (`cli/proxies.py`) para que se vean fluidas lado a lado.
- **Revisa sin que te lo pidan.**
  - Antes de proponer cortes, corre `cli/revisar-voz.py`. Detecta arranques fallidos y frases repetidas que una
    transcripción larga esconde.
  - Antes de decir que un render está listo, corre `cli/revisar-entrega.py` y mira su hoja de contacto.
- **Cambia solo lo que te señalen.** Si piden ajustar una parte, no rehagas ni borres piezas que ya estaban aprobadas.
- **No agregues funciones, dependencias ni refactors que nadie pidió.** El proyecto es deliberadamente acotado. Si algo
  grande parece buena idea, propónlo; no lo implementes.
- **No toques el color de las tomas.** El render solo convierte HDR→SDR, y lo hace solo (ver [Render](#render-cli)).
- **Tras cambiar código:** `npm run build` (typecheck y bundle). Si tocaste `graph.ts`, renderiza el ejemplo (abajo).

---

## Instalación

| Pieza | Requiere |
|---|---|
| Editor web y render | Node ≥ 22.18, `ffmpeg`/`ffprobe` en el PATH (o variables `FFMPEG`/`FFPROBE`), un navegador Chromium |
| Transcripción y revisión de voz | `whisper-cli` (`brew install whisper-cpp`) y el modelo [`ggml-large-v3-turbo-q5_0.bin`](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin) en `~/.cache/whisper/` (547 MB, una sola vez) |
| Herramientas en Python (`cli/*.py`, animaciones) | Python 3.10+, `numpy`, `Pillow` |
| Captura de animaciones | Chromium de Playwright (`npx playwright-core install chromium`) o Chrome instalado (`CHROME_PATH`) |
| Limpieza de audio (opcional) | [DeepFilterNet](https://github.com/Rikorose/DeepFilterNet) (`deep-filter` en `~/.local/bin` o `DEEP_FILTER`) |

```bash
npm install
npm run dev          # editor en http://localhost:5173
npm run build        # typecheck + bundle (dist/)
npm run lint
```

### Prueba rápida (sin material propio)

```bash
sh ejemplo/generar.sh                                         # crea tomas, voz y música sintéticas en ejemplo/medios/
node cli/render.ts ejemplo/manifiesto.json --base ejemplo --out salida
```

Debe salir `salida/ejemplo-vertical.mp4` de 9.5 s: dos tomas, un corte interno en la segunda, voz con un corte y música baja.
Para verlo en el editor, abre `ejemplo/manifiesto.json` (botón o arrastrar) y conecta la carpeta `ejemplo/`.

---

## Flujo de un video

Supón una carpeta de medios (`--base`), por ejemplo `~/Videos`, con un proyecto en `seccion/N/` que trae las tomas y la nota de voz.

### 1. Voz

```bash
node cli/recortar-voz.ts seccion/N/voz.wav                 # opcional: quita silencios (silenceremove)
node cli/transcribe.ts seccion/N/voz.wav                   # → voz.transcript.json: cada palabra con su segundo
python3 cli/revisar-voz.py seccion/N/voz.wav --out seccion/N/revision
```

- `transcribe.ts` parte el audio en trozos de ≤ 30 s en los silencios: así Whisper no se cicla en audios largos.
- `revisar-voz.py` transcribe **cada frase por separado** y reporta:
  - arranques fallidos;
  - tomas repetidas y repeticiones;
  - palabras sueltas y ruidos;

  y propone los cortes (`voice.cuts`). Un Whisper de ventana larga junta el intento fallido con la frase buena y no los ves.

### 2. Manifiesto

Escríbelo según [`manifiesto.md`](manifiesto.md):

- Sincroniza las tomas con lo que dice la voz usando la transcripción (§8).
- Usa siempre rutas relativas completas (`seccion/N/IMG_0001.MOV`), nunca solo el nombre.

### 3. Animaciones (opcional)

Hay dos caminos, ambos detallados en [`cli/animaciones/README.md`](cli/animaciones/README.md).

**Motor de plantillas** (recomendado, para los estilos Recorte y Bauhaus):

```bash
python3 cli/animaciones/motor/motor.py seccion/N/guion-motor.json --base ~/Videos [--capturar] [--solo id1,id2]
```

- El guion es un JSON con la lista de escenas y su texto.
- Los tiempos se pueden anclar a palabras de la transcripción (`{"palabra": "enchufe", "n": 1}`).
- Sin `--capturar` genera solo el HTML y un manifiesto con `overlays[].html`, que el editor reproduce **en vivo**.
- Con `--capturar` graba los WebM para el render.

**Guion a mano:** un script de Python por video que usa las librerías de estilo (`recorte.py`, `bauhaus.py`,
`escritorio.py`, `plastilina.py`, `sombras.py`). Hay 40+ guiones reales en `cli/animaciones/ejemplos/` como referencia.
Se graban con:

```bash
node cli/animaciones/capturar.ts escena.html 6.5 escena.webm      # o --lote lista.json para muchas
```

La captura es cuadro por cuadro con `window.__seek(s)`, sale en VP9 con alfa y reusa lo que no cambió.

### 4. Revisión en el editor

`npm run dev`, «📂 Conectar carpeta» (una vez) y abre o arrastra el manifiesto. Los archivos se cargan solos por su ruta.

| Función | Qué hace |
|---|---|
| Vista en vivo | Las capas con `html` se ven sin grabar. El botón «En vivo / Grabado» alterna con el `.webm`. |
| Comparar | Hasta 4 manifiestos sincronizados lado a lado; el audio sale del panel 🔊. Arrastra 2+ `.json` a la ventana, o usa el botón «Comparar». |
| Versiones ligeras | `python3 cli/proxies.py a.json b.json --base ~/Videos` crea `.proxies/` (540p, SDR). Comparar las usa solo. Sin ellas, 2+ tomas 4K a la vez se traban. |
| Edición manual | Recortes, cortes con la tecla S, orden de clips, volumen, capas (posición, tamaño, rango) y «Descargar manifiesto». |

### 5. Render (CLI)

```bash
node cli/render.ts seccion/N/manifest.json --base ~/Videos [--out seccion/N/final] [--encoder maxima|videotoolbox|x264]
```

- **Encoder:** `maxima` por defecto (x264 lento, CRF 14, AAC 320k): un solo archivo final, el de mejor calidad, para todas las
  redes. `videotoolbox` (hardware, macOS) es rápido para pruebas; `x264` es intermedio.
- **Salida:** 60 fps, H.264 High, etiquetado BT.709.
- **Formatos:** `outputs` admite `vertical` (1080×1920) y `horizontal` (1920×1080).
- **Tomas HDR (iPhone HLG/PQ):**
  - Se detectan y pasan a SDR BT.709 con la LUT de `cli/luts/`, en paralelo y con caché en `<out>/.hdr-cache`.
  - La LUT se regenera con `python3 cli/luts/generar.py`.
- **Navegador:** el editor también exporta con `ffmpeg.wasm`, pero solo para material ligero. Nunca lo uses para 4K ni videos largos: no aguanta la memoria y es 5–20× más lento.

### 6. Antes de entregar

```bash
python3 cli/revisar-entrega.py seccion/N/manifest.json --video seccion/N/final/x-vertical.mp4 --base ~/Videos
```

- **Revisa:**
  - micro-clips y capas encimadas;
  - cuadros negros o blancos;
  - «tropiezos» (cambios bruscos de imagen completa);
  - picos de audio.
- **Genera** una hoja de contacto de cada corte.
- **Termina con código 1** si hay algo grave.

### Extras

| Herramienta | Uso |
|---|---|
| `cli/subtitulos.py` | Subtítulos palabra por palabra en el estilo de la sección: una capa transparente. Corrige términos con `cli/subtitulos-diccionario.json`. |
| `cli/portada.py` | 3 portadas de 1080×1920 con un cuadro nítido de la toma y el titular en el estilo. |
| `cli/biblioteca.py` | Catálogo de tomas de relleno (`catalogo.json` + hoja de contacto) con avisos de calidad y búsqueda por tema. |
| `cli/limpiar-audio.ts` | Quita ruido y eco del audio de un clip (DeepFilterNet) sin recomprimir el video. |
| `cli/texto.ts` | Texto animado con fondo transparente (`rebote`, `deslizar`, `maquina`, `resaltar`, `subtitulo`). |
| `cli/textclip.ts` | Graba una animación HTML exportada de TextDecoration como clip MP4. |
| `cli/granja.py` | Reparte capturas pesadas entre esta máquina y una segunda por una carpeta sincronizada (Syncthing). Se configura con `GRANJA_LEGION`, `CAP_MAC` y `CAP_LEGION`. |

---

## Mapa del repo

```
src/                    editor web (React + Vite)
  lib/graph.ts          manifiesto → argumentos de ffmpeg (compartido con el CLI)
  lib/types.ts          tipos del manifiesto
  state.ts              estado del editor, conversión manifiesto ↔ estado, mapeo de tiempos
  components/           PreviewPane (reproductor), CompararPane, HtmlOverlay (escenas en vivo), timeline, inspector…
cli/                    render y herramientas (Node con TypeScript nativo, Python)
  animaciones/          estilos, captura, motor de plantillas y guiones de ejemplo
  luts/                 LUT HDR→SDR
ejemplo/                manifiesto y medios sintéticos para probar
docs/                   plan del motor de animaciones e historial de implementación
manifiesto.md           especificación del manifiesto
```

## Decisiones de diseño

- **Formato distinto al de salida:** el clip va completo y centrado sobre una copia de sí mismo, escalada y desenfocada.
  Con `fit: "cover"` se recorta para llenar el cuadro.
- **Audio de las tomas:** se descarta por defecto. Se conserva por clip con `keepAudio` y su volumen, con `atempo` si
  cambia la velocidad.
- **Mezcla:** `amix` sin renormalizar. La música va a volumen fijo y se corta sola al terminar el video.
- **Reproductor:** el reloj es la voz. Video y capas la siguen y se recolocan si se separan más de 0.12 s; los cortes se
  aplican cuadro a cuadro.
- **Hosting del editor (opcional):** Cloudflare Pages (`npm run build` → `dist`). `ffmpeg.wasm` necesita los headers
  COOP/COEP de `public/_headers`.

## Convenciones del autor (ejemplo, no reglas)

El repo nació para un canal personal; los guiones de `cli/animaciones/ejemplos/` son de sus videos reales. Ahí:

- **Carpeta de medios:** `~/Documents/Videos`, con un proyecto por carpeta numerada dentro de cada sección. Por eso varios
  scripts usan ese valor por defecto, pero todos aceptan `--base` o `SALIDA`.
- **Un estilo por sección:**
  - noticias → Recorte;
  - conceptos → Escritorio;
  - videos generales → Plastilina;
  - gadgets → Bauhaus;
  - terror → Sombras.
- **Propuestas:** viven en una carpeta aparte de «manifiestos de prueba» y se comparan en el editor antes de elegir.

Adáptalo a tu flujo: lo único fijo es el manifiesto.
