import { FFmpeg } from '@ffmpeg/ffmpeg'
import { fetchFile, toBlobURL } from '@ffmpeg/util'
import type { Manifest, OutputFormat } from './types.ts'
import { buildArgs, inputFiles, outputFileName } from './graph.ts'

let instance: FFmpeg | null = null

async function getFFmpeg(): Promise<FFmpeg> {
  if (instance) return instance
  const ffmpeg = new FFmpeg()
  const base = `${import.meta.env.BASE_URL}ffmpeg`
  // toBlobURL evita que Vite intente transformar el core como módulo propio
  await ffmpeg.load({
    coreURL: await toBlobURL(`${base}/ffmpeg-core.js`, 'text/javascript'),
    wasmURL: await toBlobURL(`${base}/ffmpeg-core.wasm`, 'application/wasm'),
    workerURL: await toBlobURL(`${base}/ffmpeg-core.worker.js`, 'text/javascript'),
  })
  instance = ffmpeg
  return ffmpeg
}

const ext = (name: string) => {
  const m = /\.([A-Za-z0-9]+)$/.exec(name)
  return m ? m[1].toLowerCase() : 'bin'
}

/**
 * Renderiza un formato en el navegador.
 * `files` debe venir alineado con inputFiles(manifest).
 */
export async function renderInBrowser(
  manifest: Manifest,
  files: File[],
  format: OutputFormat,
  onProgress: (ratio: number) => void,
): Promise<{ name: string; data: Uint8Array }> {
  const refs = inputFiles(manifest)
  if (files.length !== refs.length) throw new Error('Faltan archivos por asignar')

  const ffmpeg = await getFFmpeg()
  const inputNames = files.map((f, i) => `in${i}.${ext(f.name)}`)
  const outputName = outputFileName(manifest, format)

  const handler = ({ progress }: { progress: number }) => {
    onProgress(Math.max(0, Math.min(1, progress)))
  }
  ffmpeg.on('progress', handler)
  try {
    for (let i = 0; i < files.length; i++) {
      await ffmpeg.writeFile(inputNames[i], await fetchFile(files[i]))
    }
    const args = buildArgs(manifest, { format, encoder: 'wasm', inputNames, outputName })
    const code = await ffmpeg.exec(args)
    if (code !== 0) throw new Error(`ffmpeg terminó con código ${code}`)
    const data = (await ffmpeg.readFile(outputName)) as Uint8Array
    return { name: outputName, data }
  } catch (err) {
    // Un fallo (típicamente memoria) deja el runtime en mal estado: se descarta.
    ffmpeg.terminate()
    instance = null
    throw err
  } finally {
    ffmpeg.off('progress', handler)
    if (instance) {
      for (const name of [...inputNames, outputName]) {
        await ffmpeg.deleteFile(name).catch(() => {})
      }
    }
  }
}

export function downloadBlob(name: string, data: BlobPart, type = 'video/mp4') {
  const url = URL.createObjectURL(new Blob([data], { type }))
  const a = document.createElement('a')
  a.href = url
  a.download = name
  a.click()
  setTimeout(() => URL.revokeObjectURL(url), 10_000)
}
