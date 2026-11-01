import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
def rep(old, new):
    global s
    n = s.count(old)
    if n != 1: sys.exit(f"expected 1 of {old[:70]!r}, found {n}")
    s = s.replace(old, new)

rep('''        <button id="f-b" aria-pressed="false">Both</button>''', '''        <button id="f-b" aria-pressed="false">Both</button>
        <button id="f-x" aria-pressed="false">Exterior</button>''')

# courtyard front: solid wall at the west end, triangle jali across the rest (as on the reference)
rep('''r: [490, 965, 865, 1170], walls: "ws", floor: "grass", labelAt: [677, 1110] });''',
    '''r: [490, 965, 865, 1170], walls: "w", floor: "grass", labelAt: [677, 1110] });''')

rep('''// warm interior lights (about 3000 K)''', '''// ================= EXTERIOR (shown with "Both" floors and full walls) =================
// After the reference render: white concrete frame and slabs, a brick-clad box with triangle
// jali on the front right, planters spilling greenery on the 1st-floor ledges, a roof-level
// portal frame with a perforated (round-hole) pergola, and a low front wall with a jali band.
const extItems = [];
function exterior(fn) {
  const n = G.children.length, w = walls.length;
  fn();
  G.children.slice(n).forEach(o => { o.userData.ext = true; extItems.push(o); });
  walls.length = w;                                // exterior parts ignore the cutaway toggle
}
const concrete = M(C.white, { r: 0.8 });
const brickTex = canvasTex(512, (g, n) => {
  const rows = 12, rh = n / rows, bw = n / 4;
  g.fillStyle = "#e6e0d6"; g.fillRect(0, 0, n, n);
  for (let r = 0; r < rows; r++) for (let i = -1; i < 5; i++) {
    const x = i * bw + (r % 2 ? bw / 2 : 0), t = rnd();
    g.fillStyle = `rgb(${196 + t * 30 | 0},${100 + t * 26 | 0},${58 + t * 18 | 0})`;
    g.fillRect(x + 3, r * rh + 3, bw - 6, rh - 6);
  }
}, 3);
const brickClad = new THREE.MeshStandardMaterial({ map: brickTex, roughness: 0.9 });
const holeTex = canvasTex(512, (g, n) => {
  g.fillStyle = "#fff"; g.fillRect(0, 0, n, n);
  g.globalCompositeOperation = "destination-out";
  for (let i = 0; i < 26; i++) { g.beginPath(); g.arc(rnd() * n, rnd() * n, 14 + rnd() * 34, 0, 7); g.fill(); }
}, 8);
const holed = new THREE.MeshStandardMaterial({ color: C.white, map: holeTex, alphaTest: 0.5, side: THREE.DoubleSide, roughness: 0.8 });
// a box between two heights over a plan rect
const slab = (a, y0, y1, mat = concrete) => { const r = R(...a); return box(r.w, y1 - y0, r.d, r.cx, y0, r.cz, mat); };
function jaliAt(a, y0, h) {
  const r = R(...a), alongX = r.w > r.d, len = alongX ? r.w : r.d;
  const map = jaliTex.clone(); map.needsUpdate = true; map.repeat.set(1 / 3, 1 / 3);
  const m = new THREE.MeshStandardMaterial({ color: C.brick, map, alphaTest: 0.5, side: THREE.DoubleSide, roughness: 0.9 });
  (byKey.brick ||= []).push(m);
  box(alongX ? len : 0.3, h, alongX ? 0.3 : len, r.cx, y0, r.cz, m, false);
}
// planter trough with leafy plants spilling over its front edge (front = +z)
function planterGreens(a, y0) {
  const r = R(...a);
  slab(a, y0, y0 + 1.5);
  const leaf = [M(C.leaf, { r: 0.9 }), M(0x7E9A52, { r: 0.9 }), M(0x4F6B3A, { r: 0.9 })];
  const n = Math.round(r.w / 0.8);
  for (let i = 0; i < n; i++) for (let k = 0; k < 3; k++) {
    const b = new THREE.Mesh(new THREE.IcosahedronGeometry(0.5 + rnd() * 0.45, 1), leaf[(i + k) % 3]);
    b.position.set(r.x0 + (i + rnd()) * r.w / n, y0 + 1.4 - k * 0.55 + rnd() * 0.5, r.z1 - 0.1 + k * 0.25);
    b.scale.y = 0.8 + k * 0.25; b.castShadow = true; G.add(b);
  }
}
function wallLight(px, py, y) {
  const [x, z] = ft(px, py);
  box(0.35, 0.8, 0.25, x, y, z, M(C.black, { m: 0.5, r: 0.4 }));
  const glow = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.06, 0.2), new THREE.MeshBasicMaterial({ color: 0xFFD9A0 }));
  glow.position.set(x, y - 0.05, z); G.add(glow);
  const l = new THREE.SpotLight(0xFFC487, 25, 10, 0.7, 0.6, 2); l.position.set(x, y, z + 0.2); l.target.position.set(x, y - 6, z + 0.6); G.add(l, l.target);
}
function barGate(a, y0, h) {
  const r = R(...a), bar = M(C.black, { m: 0.5, r: 0.4 });
  for (let x = r.x0 + 0.15; x < r.x1; x += 0.3) box(0.06, h, 0.06, x, y0, r.cz, bar);
  for (const y of [y0 + 0.2, y0 + h - 0.2]) box(r.w, 0.12, 0.08, r.cx, y, r.cz, bar);
}

// ground floor: courtyard front, slab over the ground floor, front facade, boundary wall + gates
F = { ...FLOORS.g, key: "g" }; G = groups.g;
wallPiece([490, 1166, 610, 1174], 0, H_FULL);
brickJali([610, 1166, 865, 1174]);
exterior(() => {
  for (const a of [[103, 365, 1290, 965], [103, 965, 490, 1180], [865, 965, 1290, 1180]]) slab(a, H_FULL, H_FULL + 0.9);
  slab([200, 1174, 490, 1180], 0, H_FULL, brickClad);                 // brick wall by the entrance gate
  wallLight(345, 1182, 6.2);
  const G0 = -5.35;                                                    // road level
  slab([260, 1186, 1238, 1194], G0, G0 + 3.8);                         // front boundary wall
  jaliAt([870, 1186, 1238, 1194], G0 + 3.8, 2.0);                      // jali band along its top
  slab([260, 1186, 870, 1194], G0 + 3.8, G0 + 5.8);
  barGate([103, 1186, 260, 1194], G0, 6.0);                            // gate on the west
  barGate([1238, 1186, 1395, 1194], G0, 6.0);                          // pedestrian gate by the front steps
});

// 1st floor: roof slab + parapet, brick box with window and jali, planters, roof room and portal frame
F = { ...FLOORS.f, key: "f" }; G = groups.f;
exterior(() => {
  const top = H_FULL + 1.2;
  for (const a of [[105, 205, 1595, 804], [105, 804, 1395, 964], [105, 964, 545, 1172], [1030, 964, 1400, 1172]]) slab(a, H_FULL, top);
  slab([105, 205, 1595, 215], top, top + 3.5); slab([1585, 205, 1595, 804], top, top + 3.5);
  slab([700, 1150, 1400, 1160], top, top + 3.5); slab([1385, 804, 1395, 1150], top, top + 3.5);
  // brick box on the family living front: brick frame, big window on the left, triangle jali on the right
  const B = (a, y0, y1) => slab(a, y0, y1, brickClad);
  B([1030, 1160, 1400, 1172], 0, 1.0); B([1030, 1160, 1400, 1172], 8.2, top + 0.3);
  B([1030, 1160, 1045, 1172], 1.0, 8.2); B([1215, 1160, 1228, 1172], 1.0, 8.2); B([1385, 1160, 1400, 1172], 1.0, 8.2);
  slab([1045, 1163, 1215, 1168], 1.0, 8.2, M(C.glass, { r: 0.08, m: 0.4 }));
  for (const x of [1045, 1130, 1215]) slab([x - 1, 1162, x + 1, 1169], 1.0, 8.2, M(C.black));
  jaliAt([1228, 1163, 1385, 1169], 1.0, 7.2);
  planterGreens([1030, 1172, 1400, 1196], -0.3);
  // west front (Bed-04): glazing behind a planter ledge
  slab([115, 1162, 525, 1166], 1.0, 8.4, M(C.glass, { r: 0.08, m: 0.4 }));
  for (const x of [115, 252, 388, 525]) slab([x - 1, 1161, x + 1, 1167], 1.0, 8.4, M(C.black));
  planterGreens([105, 1166, 535, 1192], -0.3);
  // roof room (stair head) on the west, cantilevered slab in front of it
  slab([105, 600, 700, 1160], top, top + 9.5);
  slab([95, 1160, 710, 1200], top + 7.6, top + 8.2);
  // portal frame: side walls and a roof slab over the whole roof, round holes over the east half
  const roofTop = top + 9.5;
  slab([105, 205, 125, 600], top, roofTop);
  slab([1580, 205, 1600, 1160], top, roofTop, holed);
  slab([105, 205, 1600, 300], roofTop, roofTop + 1.2); slab([105, 700, 1600, 1160], roofTop, roofTop + 1.2);
  slab([105, 300, 1050, 700], roofTop, roofTop + 1.2); slab([1500, 300, 1600, 700], roofTop, roofTop + 1.2);
  slab([1050, 300, 1500, 700], roofTop, roofTop + 1.2, holed);
});

// warm interior lights (about 3000 K)''')

# floors stack directly (wall height + slab) and the exterior shows only with both floors and full walls
rep('''const STACK = 15;''', '''const STACK = H_FULL + 0.9;''')
rep('''  groups.f.visible = mode !== "g";
  groups.f.position.y = mode === "b" ? STACK : 0;''', '''  groups.f.visible = mode !== "g";
  groups.f.position.y = mode === "b" ? STACK : 0;
  applyExt();''')
rep('''  document.getElementById("w-low").setAttribute("aria-pressed", wallsLow);''', '''  applyExt();
  document.getElementById("w-low").setAttribute("aria-pressed", wallsLow);''')
rep('''function applyWalls() {''', '''function applyExt() { extItems.forEach(o => o.visible = mode === "b" && !wallsLow); }
function applyWalls() {''')
rep('''document.getElementById("f-b").onclick = () => setMode("b");''', '''document.getElementById("f-b").onclick = () => setMode("b");
// Exterior: both floors, full walls, camera in front of the south facade
document.getElementById("f-x").onclick = () => {
  mode = "b"; wallsLow = false; activeRoom = null; applyMode(); applyWalls();
  const c = center.g, toT = new THREE.Vector3(c.cx + 4, 12, c.z1);
  anim = { t: 0, fromT: controls.target.clone(), fromP: camera.position.clone(), toT, toP: toT.clone().add(new THREE.Vector3(-14, 6, 78)) };
};''')
open(p, "w", encoding="utf-8").write(s)
print("patched")
