/**
 * Acceso a la carpeta de medios del usuario vía File System Access API (Chromium).
 * Permite que al abrir un manifiesto los archivos se carguen solos, sin re-seleccionarlos.
 */

export type DirHandle = FileSystemDirectoryHandle

export const supportsFolders = (): boolean => 'showDirectoryPicker' in window

export async function pickFolder(): Promise<DirHandle | null> {
  try {
    return await (window as unknown as { showDirectoryPicker: (o?: object) => Promise<DirHandle> }).showDirectoryPicker({
      id: 'media',
      mode: 'read',
    })
  } catch {
    return null // el usuario canceló
  }
}

// ---- persistencia del handle entre sesiones (IndexedDB) ----

const DB_NAME = 'videassembler'
const STORE = 'handles'

function openDb(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, 1)
    req.onupgradeneeded = () => req.result.createObjectStore(STORE)
    req.onsuccess = () => resolve(req.result)
    req.onerror = () => reject(req.error)
  })
}

export async function saveFolderHandle(handle: DirHandle): Promise<void> {
  try {
    const db = await openDb()
    await new Promise<void>((resolve, reject) => {
      const tx = db.transaction(STORE, 'readwrite')
      tx.objectStore(STORE).put(handle, 'media')
      tx.oncomplete = () => resolve()
      tx.onerror = () => reject(tx.error)
    })
  } catch {
    // handle no serializable (p. ej. en pruebas): la conexión vale solo esta sesión
  }
}

export async function loadFolderHandle(): Promise<DirHandle | null> {
  try {
    const db = await openDb()
    return await new Promise((resolve) => {
      const req = db.transaction(STORE, 'readonly').objectStore(STORE).get('media')
      req.onsuccess = () => resolve(req.result ?? null)
      req.onerror = () => resolve(null)
    })
  } catch {
    return null
  }
}

// ---- permisos ----

interface PermHandle {
  queryPermission?: (o: { mode: string }) => Promise<PermissionState>
  requestPermission?: (o: { mode: string }) => Promise<PermissionState>
}

export async function folderPermission(handle: DirHandle): Promise<PermissionState> {
  const h = handle as unknown as PermHandle
  if (!h.queryPermission) return 'granted'
  return h.queryPermission({ mode: 'read' })
}

/** Requiere gesto del usuario (clic) cuando el permiso está en 'prompt' */
export async function requestFolderPermission(handle: DirHandle): Promise<boolean> {
  const h = handle as unknown as PermHandle
  if (!h.requestPermission) return true
  return (await h.requestPermission({ mode: 'read' })) === 'granted'
}

// ---- búsqueda recursiva por nombre ----

interface EntryHandle {
  kind: 'file' | 'directory'
  getFile?: () => Promise<File>
  entries?: () => AsyncIterable<[string, EntryHandle]>
}

async function walk(dir: EntryHandle, wanted: Set<string>, out: File[], depth: number): Promise<void> {
  if (depth > 6 || wanted.size === 0 || !dir.entries) return
  const dirs: EntryHandle[] = []
  for await (const [name, handle] of dir.entries()) {
    if (name.startsWith('.')) continue
    if (handle.kind === 'file') {
      if (wanted.has(name) && handle.getFile) {
        out.push(await handle.getFile())
        wanted.delete(name)
        if (wanted.size === 0) return
      }
    } else if (name !== 'node_modules') {
      dirs.push(handle)
    }
  }
  for (const d of dirs) {
    await walk(d, wanted, out, depth + 1)
    if (wanted.size === 0) return
  }
}

/** Busca archivos por nombre (recursivo) dentro de la carpeta conectada */
export async function findFilesByName(handle: DirHandle, names: string[]): Promise<File[]> {
  const wanted = new Set(names)
  const out: File[] = []
  await walk(handle as unknown as EntryHandle, wanted, out, 0)
  return out
}
