import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
def rep(old, new):
    global s
    n = s.count(old)
    if n != 1: sys.exit(f"expected 1 of {old[:70]!r}, found {n}")
    s = s.replace(old, new)

# HUD toggle
rep('''        <button id="l-tog" aria-pressed="true">Labels</button>
      </div>''', '''        <button id="l-tog" aria-pressed="true">Labels</button>
      </div>
      <div class="seg" role="group" aria-label="Render quality">
        <button id="q-tog" aria-pressed="true">Realistic</button>
      </div>''')

rep('''import { CSS2DRenderer, CSS2DObject } from "three/addons/renderers/CSS2DRenderer.js";''',
'''import { CSS2DRenderer, CSS2DObject } from "three/addons/renderers/CSS2DRenderer.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { GTAOPass } from "three/addons/postprocessing/GTAOPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";''')

# procedural surface textures, picked by palette color in M()
rep('''const mats = {};
const M = (hex, o = {}) => {
  const k = hex + JSON.stringify(o);
  if (mats[k]) return mats[k];
  const m = mats[k] = new THREE.MeshStandardMaterial({ color: hex, roughness: o.r ?? 0.85, metalness: o.m ?? 0, transparent: !!o.t, opacity: o.t ?? 1 });''',
'''const mats = {};
// Procedural surface textures in near-white greys, so the palette color still sets the hue.
// Box UVs are in feet (see box()), so repeat = 1 / (feet covered by one texture tile).
function canvasTex(size, draw, feetW, feetH = feetW) {
  const c = document.createElement("canvas"); c.width = c.height = size;
  draw(c.getContext("2d"), size);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  t.repeat.set(1 / feetW, 1 / feetH);
  return t;
}
let seed = 7;
const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
const woodTex = canvasTex(512, (g, n) => {
  g.fillStyle = "#e9e9e9"; g.fillRect(0, 0, n, n);
  for (let i = 0; i < 140; i++) {                 // long wavy grain lines running up the board
    const x0 = rnd() * n, w = 0.6 + rnd() * 2.4, l = 150 + rnd() * 90 | 0;
    g.strokeStyle = `rgba(${l},${l},${l},${0.25 + rnd() * 0.35})`; g.lineWidth = w;
    g.beginPath();
    for (let y = -8; y <= n + 8; y += 16) { const x = x0 + Math.sin(y / 70 + x0) * 6; y < 0 ? g.moveTo(x, y) : g.lineTo(x, y); }
    g.stroke();
  }
  for (let i = 0; i < 6; i++) { const x = rnd() * n; g.fillStyle = "rgba(255,255,255,0.18)"; g.fillRect(x, 0, 8 + rnd() * 26, n); }
}, 2, 4);
const fabricTex = canvasTex(256, (g, n) => {
  g.fillStyle = "#f0f0f0"; g.fillRect(0, 0, n, n);
  for (let y = 0; y < n; y += 2) { g.fillStyle = `rgba(0,0,0,${0.03 + rnd() * 0.05})`; g.fillRect(0, y, n, 1); }
  for (let x = 0; x < n; x += 2) { g.fillStyle = `rgba(0,0,0,${0.02 + rnd() * 0.04})`; g.fillRect(x, 0, 1, n); }
}, 1.2);
const plasterTex = canvasTex(256, (g, n) => {
  g.fillStyle = "#f6f6f6"; g.fillRect(0, 0, n, n);
  for (let i = 0; i < 900; i++) { const v = 225 + rnd() * 30 | 0; g.fillStyle = `rgba(${v},${v},${v},0.25)`; g.beginPath(); g.arc(rnd() * n, rnd() * n, 2 + rnd() * 9, 0, 7); g.fill(); }
}, 6);
const SURFACE = {
  [C.oak]: [woodTex, 0.6], [C.teak]: [woodTex, 0.6], [C.walnut]: [woodTex, 0.55], [C.espresso]: [woodTex, 0.55], [0xC07A3E]: [woodTex, 0.5],
  [C.linen]: [fabricTex, 0.95], [C.curtain]: [fabricTex, 1], [C.bedding]: [fabricTex, 0.95], [C.sage]: [fabricTex, 0.95], [C.rug]: [fabricTex, 1],
  [C.wall]: [plasterTex, 0.92]
};
const M = (hex, o = {}) => {
  const k = hex + JSON.stringify(o);
  if (mats[k]) return mats[k];
  const [map, rough] = SURFACE[hex] || [null, null];
  const m = mats[k] = new THREE.MeshStandardMaterial({ color: hex, map, roughness: o.r ?? rough ?? 0.85, metalness: o.m ?? 0, transparent: !!o.t, opacity: o.t ?? 1 });''')

# renderer, environment light, softer and finer sun shadows
rep('''renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;''', '''renderer.toneMapping = THREE.AgXToneMapping;
renderer.toneMappingExposure = 1.15;''')
rep('''scene.add(new THREE.HemisphereLight(0xFFF4E2, 0x8A7F6E, 1.15));
const sun = new THREE.DirectionalLight(0xFFE6C4, 1.9);
sun.position.set(-30, 70, 40);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
Object.assign(sun.shadow.camera, { left: -60, right: 60, top: 60, bottom: -60, near: 1, far: 220 });
sun.shadow.bias = -0.0004;''', '''// Image-based light from a neutral studio room gives soft fill and real reflections on glass,
// tile and metal; the sun adds warm late-afternoon light with crisp shadows.
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(renderer), 0.04).texture;
scene.add(new THREE.HemisphereLight(0xFFF4E2, 0x8A7F6E, 0.35));
const sun = new THREE.DirectionalLight(0xFFE2BC, 2.6);
sun.position.set(-30, 70, 40);
sun.castShadow = true;
sun.shadow.mapSize.set(4096, 4096);
Object.assign(sun.shadow.camera, { left: -60, right: 60, top: 60, bottom: -60, near: 1, far: 220 });
sun.shadow.bias = -0.0003; sun.shadow.normalBias = 0.03;''')

# box UVs in feet, so textures keep their real size on every surface
rep('''function box(w, h, d, x, y, z, mat, shadow = true) {
  const m = new THREE.Mesh(new THREE.BoxGeometry(Math.max(w, .05), Math.max(h, .05), Math.max(d, .05)), mat);''',
'''function box(w, h, d, x, y, z, mat, shadow = true) {
  const geo = new THREE.BoxGeometry(Math.max(w, .05), Math.max(h, .05), Math.max(d, .05));
  const uv = geo.attributes.uv, dims = [[d, h], [d, h], [w, d], [w, d], [w, h], [w, h]];   // faces +x −x +y −y +z −z
  for (let i = 0; i < 24; i++) { const f = dims[i >> 2]; uv.setXY(i, uv.getX(i) * f[0], uv.getY(i) * f[1]); }
  const m = new THREE.Mesh(geo, mat);''')

# tiles: 4 × 4 tiles per texture with slight tone variation; repeats now per foot
rep('''const gridTex = (() => {
  const c = document.createElement("canvas"); c.width = c.height = 128;
  const g = c.getContext("2d");
  g.fillStyle = "#fff"; g.fillRect(0, 0, 128, 128);
  g.fillStyle = "#b3ada3"; g.fillRect(0, 0, 128, 3); g.fillRect(0, 0, 3, 128);''', '''const gridTex = (() => {
  const c = document.createElement("canvas"); c.width = c.height = 512;
  const g = c.getContext("2d");
  for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) {
    const v = 238 + (rnd() * 17 | 0); g.fillStyle = `rgb(${v},${v},${v - 2})`; g.fillRect(i * 128, j * 128, 128, 128);
    for (let k = 0; k < 40; k++) { g.fillStyle = `rgba(255,255,255,${rnd() * 0.25})`; g.fillRect(i * 128 + rnd() * 128, j * 128 + rnd() * 128, 2 + rnd() * 10, 1 + rnd() * 3); }
  }
  g.fillStyle = "#b3ada3";
  for (let i = 0; i < 4; i++) { g.fillRect(0, i * 128, 512, 3); g.fillRect(i * 128, 0, 3, 512); }''')
rep('''  map.repeat.set(w * 12 / tw, d * 12 / td);
  const m = new THREE.MeshStandardMaterial({ color: hex, map, roughness: 0.5 });''',
    '''  map.repeat.set(12 / tw / 4, 12 / td / 4);
  const m = new THREE.MeshStandardMaterial({ color: hex, map, roughness: 0.35 });''')
rep('''  map.repeat.set(len / 3, h / 3);                 // 9" blocks''', '''  map.repeat.set(1 / 3, 1 / 3);                   // 4 blocks per 3 ft = 9" blocks''')
rep('''map.repeat.set((lw - 0.7) * 3, 6.2 * 3);''', '''map.repeat.set(3, 3);''')

# glass: clearer, with environment reflections
rep('''function glassPanel(a, h = H_FULL, y0 = 0) {''', '''function glassPanel(a, h = H_FULL, y0 = 0) {   // glass uses M(C.glass, { r: 0.1, t: 0.3 }), reflective through the environment light''')

# warm interior lights and the site ground
rep('''// ---------- floor modes ----------''', '''// warm interior lights (about 3000 K) near ceiling height in the main rooms, one floor group each
function lamp(px, py, power = 45) {
  const [x, z] = ft(px, py), l = new THREE.PointLight(0xFFC487, power, 26, 2);
  l.position.set(x, 8.4, z); G.add(l);
}
F = { ...FLOORS.g, key: "g" }; G = groups.g;
[[690, 560], [1060, 540], [380, 540], [925, 950], [345, 980], [680, 870]].forEach(([x, y]) => lamp(x, y));
F = { ...FLOORS.f, key: "f" }; G = groups.f;
[[1215, 900], [275, 430], [905, 430], [1405, 430], [320, 980], [700, 710]].forEach(([x, y]) => lamp(x, y));
// site ground at road level, so the raised house sits on something
{
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(500, 500), new THREE.MeshStandardMaterial({ color: 0xA7A08C, roughness: 1 }));
  ground.rotation.x = -Math.PI / 2; ground.position.set(30, -5.35, 30); ground.receiveShadow = true; scene.add(ground);
}

// ---------- floor modes ----------''')

# post-processing: ambient occlusion (GTAO) for contact shadows in corners and under furniture
rep('''function resize() {
  const w = view.clientWidth, h = view.clientHeight;
  renderer.setSize(w, h); labelRenderer.setSize(w, h);''', '''const composer = new EffectComposer(renderer);
composer.setPixelRatio(Math.min(devicePixelRatio, 1.5));
composer.addPass(new RenderPass(scene, camera));
const ao = new GTAOPass(scene, camera, 1, 1);
ao.updateGtaoMaterial({ radius: 1.6, distanceExponent: 1.5, thickness: 1.5, scale: 1.2, samples: 16 });
ao.blendIntensity = 0.9;
// glass and the cut-out jali shouldn't cast ambient occlusion
const baseHide = ao.overrideVisibility.bind(ao);
ao.overrideVisibility = function () {
  baseHide();
  scene.traverse(o => { if (o.isMesh && (o.material.transparent || o.material.alphaTest > 0)) o.visible = false; });
};
composer.addPass(ao);
composer.addPass(new OutputPass());
let realistic = true;
document.getElementById("q-tog").onclick = e => { realistic = !realistic; e.currentTarget.setAttribute("aria-pressed", realistic); };

function resize() {
  const w = view.clientWidth, h = view.clientHeight;
  renderer.setSize(w, h); labelRenderer.setSize(w, h); composer.setSize(w, h);''')
rep('''  controls.update();
  renderer.render(scene, camera);''', '''  controls.update();
  if (realistic) composer.render(); else renderer.render(scene, camera);''')
open(p, "w", encoding="utf-8").write(s)
print("patched")
