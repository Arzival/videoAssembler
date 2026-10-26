// Runtime 3D del estilo «Maqueta» (lo incrusta maqueta.py en cada página; no se carga suelto).
// Mundo en miniatura con cámara ortográfica isométrica, low-poly de sombreado plano y sombras suaves.
// Todo depende del tiempo GLOBAL t (segundos del video final): cada página construye el diorama completo y la
// cámara sigue el mismo recorrido, así el último cuadro de una página es idéntico al primero de la siguiente.
// El mundo de cada episodio es el cuerpo de una función async (M, THREE) que arma piezas y devuelve update(t).
import * as THREE from 'three';

const CFG = window.MAQ;
const FUENTES = ['700 100px "Space Grotesk"', '500 100px "Space Grotesk"', '800 100px Manrope', '600 100px Manrope'];
await Promise.all(FUENTES.map(f => document.fonts.load(f)));
await document.fonts.ready;

const W = 1080, H = 1920, AS = W / H;
const el = document.getElementById('c3');
const ren = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
ren.setPixelRatio(location.hash.includes('preview') ? 1 : CFG.PR);
ren.setSize(W, H);
ren.shadowMap.enabled = true;
ren.shadowMap.type = THREE.PCFSoftShadowMap;
ren.toneMapping = THREE.NeutralToneMapping;
el.appendChild(ren.domElement);
ren.domElement.addEventListener('webglcontextlost', () => { window.__perdido = true });

const scene = new THREE.Scene();
const cam = new THREE.OrthographicCamera(-1, 1, 1, -1, -400, 800);
const hemi = new THREE.HemisphereLight('#fffaf2', '#9d958a', 1.35);
scene.add(hemi);
const sun = new THREE.DirectionalLight('#fff2df', 2.3);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.bias = -0.0005;
sun.shadow.normalBias = 0.03;
sun.shadow.radius = 5;
scene.add(sun, sun.target);
const SOL = new THREE.Vector3(-0.42, 1, 0.62).normalize();

// ---------- utilidades de tiempo ----------
const k = (t, a, d) => Math.min(1, Math.max(0, (t - a) / d));
const eo = p => 1 - Math.pow(1 - p, 3);
const eio = p => p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
const eb = p => { const c = 1.9, c3 = c + 1; return 1 + c3 * Math.pow(p - 1, 3) + c * Math.pow(p - 1, 2) };  // back-out
const h = i => { const x = Math.sin(i * 12.9898 + 4.1) * 43758.5453; return x - Math.floor(x) };

// ---------- materiales y piezas ----------
const MATS = {};
const mat = (c, o) => {
  if (!o) return MATS[c] ??= new THREE.MeshStandardMaterial({ color: c, roughness: .84, metalness: 0, flatShading: true });
  return new THREE.MeshStandardMaterial({ color: c, roughness: .84, metalness: 0, flatShading: true, ...o });
};
const sombra = o => { o.traverse(m => { if (m.isMesh) { m.castShadow = true; m.receiveShadow = true } }); return o };
const malla = (g, c, o) => { const m = new THREE.Mesh(g, c && c.isMaterial ? c : mat(c, o)); m.castShadow = m.receiveShadow = true; return m };
// todas las piezas tienen el origen en su base (y = 0) para que «crezcan» desde el piso
const caja = (w, hh, d, c, x = 0, y = 0, z = 0, o) => { const g = new THREE.BoxGeometry(w, hh, d); g.translate(0, hh / 2, 0); const m = malla(g, c, o); m.position.set(x, y, z); return m };
const cil = (r, hh, c, x = 0, y = 0, z = 0, seg = 10, o) => { const g = new THREE.CylinderGeometry(r, r, hh, seg); g.translate(0, hh / 2, 0); const m = malla(g, c, o); m.position.set(x, y, z); return m };
const cono = (r, hh, c, x = 0, y = 0, z = 0, seg = 8, o) => { const g = new THREE.ConeGeometry(r, hh, seg); g.translate(0, hh / 2, 0); const m = malla(g, c, o); m.position.set(x, y, z); return m };
const bola = (r, c, x = 0, y = 0, z = 0, det = 1, o) => { const m = malla(new THREE.IcosahedronGeometry(r, det), c, o); m.position.set(x, y, z); return m };
const grupo = (x = 0, y = 0, z = 0, ...hijos) => { const g = new THREE.Group(); g.position.set(x, y, z); for (const o of hijos) g.add(o); return g };
const brillo = (c, i = 1.6) => new THREE.MeshStandardMaterial({ color: c, emissive: c, emissiveIntensity: i, roughness: .5, flatShading: true });

// textura de lienzo (letreros, pantallas, carátulas)
const lienzo = (w, hh, dibuja) => {
  const c = document.createElement('canvas'); c.width = w; c.height = hh;
  const g = c.getContext('2d'); dibuja(g, w, hh);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; t.userData = { c, g };
  return t;
};
const ajusta = (g, txt, fam, peso, max, ancho) => {
  let px = max; g.font = `${peso} ${px}px ${fam}`;
  while (px > 10 && Math.max(...txt.split('\n').map(l => g.measureText(l).width)) > ancho) { px -= 2; g.font = `${peso} ${px}px ${fam}` }
  return px;
};
// letrero: caja delgada con el texto en la cara de enfrente (+z). '\n' = varias líneas
const letrero = (txt, { w = 4, h: hh = 1, bg = '#f4f1ea', fg = '#22252b', fam = '"Space Grotesk"', peso = 700, grosor = .14, canto = null, marco = null, align = 'center' } = {}) => {
  const R = 256, cw = Math.round(R * w), ch = Math.round(R * hh);
  const tex = lienzo(cw, ch, (g, cw, ch) => {
    g.fillStyle = bg; g.fillRect(0, 0, cw, ch);
    if (marco) { const m = ch * .07; g.strokeStyle = marco; g.lineWidth = ch * .045; g.strokeRect(m, m, cw - 2 * m, ch - 2 * m) }
    const ls = txt.split('\n');
    const px = ajusta(g, txt, fam, peso, ch * .72 / ls.length, cw * .86);
    g.fillStyle = fg; g.textBaseline = 'middle'; g.textAlign = align;
    const x = align === 'left' ? cw * .07 : cw / 2;
    ls.forEach((l, i) => g.fillText(l, x, ch / 2 + (i - (ls.length - 1) / 2) * px * 1.08 + px * .04));
  });
  const lado = mat(canto || bg);
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, hh, grosor).translate(0, hh / 2, 0),
    [lado, lado, lado, lado, new THREE.MeshStandardMaterial({ map: tex, roughness: .8 }), lado]);
  m.castShadow = m.receiveShadow = true;
  return m;
};
// texto pintado en el piso (calles, plazas)
const pintura = (txt, w, hh, c = '#f4f1ea', fam = '"Space Grotesk"', peso = 700) => {
  const tex = lienzo(Math.round(256 * w), Math.round(256 * hh), (g, cw, ch) => {
    const px = ajusta(g, txt, fam, peso, ch * .8, cw * .94); g.fillStyle = c; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(txt, cw / 2, ch / 2 + px * .04);
  });
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, hh), new THREE.MeshStandardMaterial({ map: tex, transparent: true, roughness: .9 }));
  m.rotation.x = -Math.PI / 2; m.position.y = .02; m.receiveShadow = true; return m;
};

// ---------- figuras del kit (reutilizables) ----------
// persona de maqueta: cuerpo cilíndrico + cabeza, sin cara (como las figuritas de arquitectura)
const persona = (c = '#e8e2d6', x = 0, z = 0) => grupo(x, 0, z, cil(.16, .7, c, 0, 0, 0, 8), bola(.15, c, 0, .86, 0, 0));
const arbol = (x = 0, z = 0, c = '#8fa98b', s = 1) => { const g = grupo(x, 0, z, cil(.07 * s, .5 * s, '#9b8a74', 0, 0, 0, 6), cono(.42 * s, 1.2 * s, c, 0, .4 * s, 0, 7)); g.userData.s = 1; return g };
const camion = (c = '#d9483b', x = 0, z = 0) => grupo(x, 0, z, caja(1.5, .7, .7, '#efebe3', -.25, .18, 0), caja(.55, .55, .68, c, .8, .18, 0),
  ...[-.7, .2, .8].flatMap(px => [-.33, .33].map(pz => { const r = cil(.17, .1, '#2b2d31', px, .17, pz, 10); r.rotation.x = Math.PI / 2; r.position.y = .17; return r })));
// rack de servidor: gabinete con ranuras y un LED por equipo (devuelve {g, leds:[mallas]})
const rack = (x = 0, z = 0, alto = 2.2, an = .9) => {
  const g = grupo(x, 0, z, caja(an, alto, .9, '#4a5059'));
  const leds = [];
  for (let i = 0; i < 6; i++) {
    const y = .25 + i * (alto - .4) / 6;
    g.add(caja(an - .16, .22, .02, '#646b76', 0, y, .455));
    const l = new THREE.Mesh(new THREE.BoxGeometry(.08, .08, .03), brillo('#8a9099', .2)); l.position.set(an / 2 - .17, y + .11, .47); g.add(l); leds.push(l);
  }
  return { g: sombra(g), leds };
};
// LED de color con intensidad (para alarmas/estado)
const led = (m, c, i = 1.8) => { m.material.color.set(c); m.material.emissive.set(c); m.material.emissiveIntensity = i };
// cuarto en corte (casa de muñecas): piso + dos muros al fondo (-x y -z)
const cuarto = (x, z, w, d, alto = 2.6, muro = '#ece7dd', piso = '#d8d1c4', grueso = .2) => grupo(x, 0, z,
  caja(w, .16, d, piso, 0, 0, 0), caja(w, alto, grueso, muro, 0, 0, -d / 2 + grueso / 2), caja(grueso, alto, d, muro, -w / 2 + grueso / 2, 0, 0));
// reloj de pared: carátula + manecillas (devuelve {g, hora(h, m)})
const reloj = (r = .55) => {
  const tex = lienzo(256, 256, (g) => { g.fillStyle = '#f7f4ee'; g.beginPath(); g.arc(128, 128, 124, 0, 7); g.fill(); g.fillStyle = '#22252b';
    for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2; g.fillRect(128 + Math.sin(a) * 100 - 5, 128 - Math.cos(a) * 100 - 5, 10, 10) } });
  const cara = new THREE.Mesh(new THREE.CylinderGeometry(r, r, .08, 24), [mat('#22252b'), new THREE.MeshStandardMaterial({ map: tex, roughness: .7 }), mat('#22252b')]);
  cara.rotation.x = Math.PI / 2;
  const mh = new THREE.Mesh(new THREE.BoxGeometry(.07, r * .55, .03).translate(0, r * .27, 0), mat('#22252b'));
  const mm = new THREE.Mesh(new THREE.BoxGeometry(.05, r * .8, .03).translate(0, r * .4, 0), mat('#d9483b'));
  mh.position.z = mm.position.z = .06;
  const g = grupo(0, 0, 0, cara, mh, mm);
  return { g: sombra(g), hora: (hh, mi) => { mm.rotation.z = -mi / 60 * Math.PI * 2; mh.rotation.z = -(hh % 12 + mi / 60) / 12 * Math.PI * 2 } };
};
// cable por puntos (tubo low-poly); devuelve la malla, con .material.emissiveIntensity animable
const cable = (pts, r = .07, c = '#2f3237') => {
  const curva = new THREE.CatmullRomCurve3(pts.map(p => new THREE.Vector3(...p)), false, 'catmullrom', .1);
  const m = new THREE.Mesh(new THREE.TubeGeometry(curva, Math.max(16, pts.length * 12), r, 6), new THREE.MeshStandardMaterial({ color: c, emissive: '#000', roughness: .6, flatShading: true }));
  m.castShadow = true; m.userData.curva = curva; m.userData.seg = Math.max(16, pts.length * 12); return m;
};
// avance de un cable encendido: muestra solo la fracción p del tubo (0–1)
const avanza = (m, p) => { m.visible = p > 0; m.geometry.setDrawRange(0, Math.ceil(m.userData.seg * Math.min(1, p)) * 36) };
// sobre de correo
const sobre = (c = '#f4f1ea') => { const g = grupo(0, 0, 0, caja(.6, .04, .4, c)); const s = caja(.12, .05, .12, '#d9483b', 0, .02, 0); g.add(s); return sombra(g) };

// ---------- animación de piezas (todas dependen de t global) ----------
const S = o => o.userData.s ?? 1;
// crece desde el piso con rebote (y), con un pequeño ensanche en x/z
const crece = (o, t, t0, d = .55) => {
  const p = k(t, t0, d); o.visible = t >= t0; const s = S(o), y = Math.max(.0001, eb(p)), xz = .75 + .25 * eo(p);
  o.scale.set(s * xz, s * y, s * xz); return p;
};
// se hunde en el piso y desaparece
const hunde = (o, t, t0, d = .4) => {
  if (t < t0) return 0; const p = k(t, t0, d); const s = S(o); o.scale.set(s, Math.max(.0001, s * (1 - eio(p))), s); if (p >= 1) o.visible = false; return p;
};
// vive entre t0 y t1: crece al entrar y se hunde al salir
const vive = (o, t, t0, t1 = 1e9, d = .55) => { if (t < t0) { o.visible = false; return 0 } const p = crece(o, t, t0, d); if (t >= t1) hunde(o, t, t1); return p };
// brota: escala uniforme desde 0 con rebote (piezas chicas, letreros)
const brota = (o, t, t0, d = .45) => { const p = k(t, t0, d); o.visible = t >= t0; const s = S(o) * Math.max(.0001, eb(p)); o.scale.set(s, s, s); return p };
// cae desde arriba con un rebote rígido (juguete); y = altura final
const cae = (o, t, t0, y = 0, alto = 6, d = .55) => {
  const p = k(t, t0, d); o.visible = t >= t0;
  const b = p < .6 ? 1 - Math.pow(p / .6, 2) : Math.abs(Math.sin((p - .6) / .4 * Math.PI)) * .12 * (1 - p);
  o.position.y = y + b * alto; return p;
};
// oscila (campanas, letreros colgados)
const oscila = (o, t, t0, amp = .5, f = 3, d = 2) => { const p = k(t, t0, d); o.rotation.z = t < t0 ? 0 : Math.sin((t - t0) * f * Math.PI * 2) * amp * (1 - p) };

// ---------- cámara ----------
// keys: [[t, {x,y,z, Z, az, el, oy}, dur]] — el primero es el estado inicial. Z = media altura visible (unidades).
let KEYS = [[0, { x: 0, y: 0, z: 0, Z: 10, az: 45, el: 32, oy: 0 }]];
const camEn = t => {
  const v = { ...KEYS[0][1] };
  for (const [a, o, d] of KEYS.slice(1)) { const p = eio(k(t, a, d ?? 1.2)); for (const q in o) v[q] = v[q] + (o[q] - v[q]) * p }
  return v;
};
const aplicaCam = v => {
  const az = v.az * Math.PI / 180, e = v.el * Math.PI / 180;
  const T = new THREE.Vector3(v.x, v.y, v.z);
  cam.position.set(T.x + Math.cos(e) * Math.sin(az) * 200, T.y + Math.sin(e) * 200, T.z + Math.cos(e) * Math.cos(az) * 200);
  cam.up.set(0, 1, 0); cam.lookAt(T);
  const oy = v.oy || 0;
  cam.top = v.Z * (1 - oy); cam.bottom = -v.Z * (1 + oy); cam.left = -v.Z * AS; cam.right = v.Z * AS; cam.updateProjectionMatrix();
  sun.position.copy(T).addScaledVector(SOL, 120); sun.target.position.copy(T);
  const sc = sun.shadow.camera, R = v.Z * 1.25 + 4;
  sc.left = -R; sc.right = R; sc.top = R; sc.bottom = -R; sc.near = 1; sc.far = 400; sc.updateProjectionMatrix();
};
const P = new THREE.Vector3();
window.__proy = p => { P.set(p[0], p[1], p[2]).project(cam); return [(P.x + 1) / 2 * W, (1 - P.y) / 2 * H] };

const M = {
  THREE, scene, cam, hemi, sun, k, eo, eio, eb, h, mat, brillo, sombra, malla, caja, cil, cono, bola, grupo, lienzo, letrero, pintura,
  persona, arbol, camion, rack, led, cuarto, reloj, cable, avanza, sobre, crece, hunde, vive, brota, cae, oscila,
  camara: keys => { KEYS = keys },
  // luz general (0 = noche, 1 = día)
  luz: f => { hemi.intensity = .35 + 1.0 * f; sun.intensity = .25 + 2.05 * f },
};

const update = await (async (M, THREE) => { __MUNDO__ })(M, THREE);
window.__u3 = t => {
  if (window.__perdido || ren.getContext().isContextLost()) throw new Error('contexto WebGL perdido');
  update(t); aplicaCam(camEn(t)); ren.render(scene, cam);
};
window.__u3(CFG.S0);
window.__c3ok();
