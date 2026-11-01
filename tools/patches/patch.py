import sys, re
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit(f"expected {count} of {old[:70]!r}, found {n}")
    s = s.replace(old, new)

# --- floors: tile grid sized from the working drawing
rep('''  const floorMat = M({ tile: C.tile, wood: C.oak, wet: C.wetTile, grass: C.grass, paving: C.paving, stone: 0xB4ADA0 }[def.floor || "tile"], { r: def.floor === "tile" ? 0.55 : 0.85 });
  parts.forEach(p => { const s = box(p.w, 0.3, p.d, p.cx, -0.3, p.cz, floorMat, false); s.receiveShadow = true; });''',
'''  const floorHex = { tile: C.tile, wood: C.oak, wet: C.wetTile, grass: C.grass, paving: C.paving, stone: 0xB4ADA0 }[def.floor || "tile"];
  const floorMat = M(floorHex, { r: def.floor === "tile" ? 0.55 : 0.85 });
  parts.forEach(p => {
    const mat = def.tile ? tileMat(floorHex, p.w, p.d, ...def.tile) : floorMat;
    const s = box(p.w, 0.3, p.d, p.cx, -0.3, p.cz, mat, false); s.receiveShadow = true;
  });''')

rep('''function room(def) {''', '''// Floor tiles: a grout-line texture repeated at the tile size from the working drawing (inches).
const gridTex = (() => {
  const c = document.createElement("canvas"); c.width = c.height = 128;
  const g = c.getContext("2d");
  g.fillStyle = "#fff"; g.fillRect(0, 0, 128, 128);
  g.fillStyle = "#b3ada3"; g.fillRect(0, 0, 128, 3); g.fillRect(0, 0, 3, 128);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  return t;
})();
function tileMat(hex, w, d, tw, td = tw) {
  const map = gridTex.clone(); map.needsUpdate = true;
  map.repeat.set(w * 12 / tw, d * 12 / td);
  const m = new THREE.MeshStandardMaterial({ color: hex, map, roughness: 0.5 });
  const key = hexKey[hex]; if (key) (byKey[key] ||= []).push(m);
  return m;
}

function room(def) {''')

# --- new builders: glass panels, brick jali, interior doors
rep('''function plant(px, py, s = 1) {''', '''// Glass along the long side of a plan rect, with black frames at the ends and about every 4 ft.
function glassPanel(a, h = H_FULL, y0 = 0) {
  const r = R(...a), alongX = r.w > r.d, len = alongX ? r.w : r.d;
  tall(box(alongX ? len : 0.08, h, alongX ? 0.08 : len, r.cx, y0, r.cz, M(C.glass, { r: 0.1, t: 0.3 }), false), y0, h);
  const n = Math.max(1, Math.round(len / 4));
  for (let i = 0; i <= n; i++) {
    const f = i / n;
    tall(box(0.12, h, 0.12, alongX ? r.x0 + f * len : r.cx, y0, alongX ? r.cz : r.z0 + f * len, M(C.black)), y0, h);
  }
}
// Plain wall piece over a plan rect between two heights (around windows and door heads).
function wallPiece(a, y0, h) {
  const r = R(...a), alongX = r.w > r.d;
  tall(box(alongX ? r.w : T, h, alongX ? T : r.d, r.cx, y0, r.cz, M(C.wall)), y0, h);
}
// Brick jali as drawn on the south elevation: square terracotta blocks, each with a solid
// triangle and an open triangle, turned so they form a pinwheel pattern.
const jaliTex = (() => {
  const c = document.createElement("canvas"); c.width = c.height = 256;
  const g = c.getContext("2d"), s = 64, b = 7;
  g.fillStyle = "#fff";
  for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) {
    const x = i * s, y = j * s;
    g.fillRect(x, y, s, b); g.fillRect(x, y + s - b, s, b); g.fillRect(x, y, b, s); g.fillRect(x + s - b, y, b, s);
    const k = (i + 2 * j) % 4, pts = [[x, y], [x + s, y], [x + s, y + s], [x, y + s]];
    g.beginPath(); [0, 1, 2].forEach((q, n) => { const [px, py] = pts[(k + q) % 4]; n ? g.lineTo(px, py) : g.moveTo(px, py); }); g.fill();
    g.fillRect(x, y, s, 3);
  }
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace;
  return t;
})();
function brickJali(a, h = H_FULL) {
  const r = R(...a), alongX = r.w > r.d, len = alongX ? r.w : r.d;
  const map = jaliTex.clone(); map.needsUpdate = true;
  map.repeat.set(len / 3, h / 3);                 // 9" blocks
  const m = new THREE.MeshStandardMaterial({ color: C.brick, map, alphaTest: 0.5, side: THREE.DoubleSide, roughness: 0.9 });
  (byKey.brick ||= []).push(m);
  tall(box(alongX ? len : 0.3, h, alongX ? 0.3 : len, r.cx, 0, r.cz, m, false), 0, h);
}
// Closed door on a wall: a walnut leaf a little proud of both faces, with a black pull.
function door(a, h = 7.0) {
  const r = R(...a), alongX = r.w > r.d, len = alongX ? r.w : r.d, t = T + 0.12;
  tall(box(alongX ? len : t, h, alongX ? t : len, r.cx, 0, r.cz, M(C.walnut, { r: 0.6 })), 0, h);
  const hx = alongX ? r.x1 - 0.35 : r.cx, hz = alongX ? r.cz : r.z1 - 0.35;
  tall(box(alongX ? 0.1 : t + 0.16, 0.9, alongX ? t + 0.16 : 0.1, hx, 3.1, hz, M(C.black, { m: 0.6, r: 0.3 })), 3.1, 0.9);
  wallPiece(a, h, H_FULL - h);
}

function plant(px, py, s = 1) {''')

# --- stair: 3 + landing + 12 + landing + 4 (GF stair electrical plan numbers 1-21)
rep('''  const r = R(...a), n1 = 4, n2 = 10, n3 = 4, riser = rise / (n1 + n2 + n3);''',
    '''  const r = R(...a), n1 = 3, n2 = 12, n3 = 4, riser = rise / (n1 + n2 + n3 + 3);   // treads + 2 landings + arrival''')
rep('''  const y1 = n1 * riser;''', '''  const y1 = (n1 + 1) * riser;                // landing 1''')
rep('''  const y2 = y1 + n2 * riser;''', '''  const y2 = y1 + (n2 + 1) * riser;           // landing 2''')
rep('''// Three-flight stair as drawn:''', '''// Three-flight stair as drawn (working drawing: 3 steps, landing, 12 steps, landing, 4 steps):''')

# --- ground floor rooms with drawing tile sizes
rep('''r: [103, 365, 245, 595] });''', '''r: [103, 365, 245, 595], tile: [24, 24] });''')
rep('''r: [103, 600, 245, 825], walls: "nws" });''', '''r: [103, 600, 245, 825], walls: "nws", tile: [6, 36] });''')
rep('''r: [103, 1020, 200, 1170], floor: "stone" });''', '''r: [103, 1020, 200, 1170], floor: "stone", tile: [24, 24] });''')
rep('''r: [250, 370, 515, 720], walls: "nws" });''', '''r: [250, 370, 515, 720], walls: "nws", tile: [12, 24] });''')
rep('''r: [515, 370, 865, 790], walls: "n" });''', '''r: [515, 370, 865, 790], walls: "n", tile: [32, 32] });''')
rep('''r: [205, 725, 410, 825], floor: "wet" });''', '''r: [205, 725, 410, 825], floor: "wet", tile: [12, 24] });''')
rep('''r: [205, 830, 485, 1110], floor: "wood" });''', '''r: [205, 830, 485, 1110], tile: [32, 32] });''')
rep('''r: [490, 790, 865, 960], walls: "w", floor: "stone" });''', '''r: [490, 790, 865, 960], walls: "w", tile: [32, 32] });''')
rep('''dim: "17'-9\\" × 16'-5\\"", r: [870, 370, 1260, 720], walls: "ns" });''',
    '''dim: "17'-9\\" × 18'-0\\"", r: [870, 370, 1260, 760], walls: "n", tile: [32, 32] });''')
rep('''r: [870, 730, 980, 1170], walls: "" });''', '''r: [870, 760, 980, 1170], walls: "", tile: [32, 32] });''')
rep('''r: [985, 735, 1390, 940], walls: "", floor: "paving" });''', '''r: [985, 770, 1390, 940], walls: "", floor: "paving", tile: [8, 8] });''')
rep('''r: [985, 945, 1135, 1170], walls: "", floor: "paving" });''', '''r: [985, 945, 1135, 1170], walls: "", floor: "paving", tile: [12, 36] });''')

# --- stair back: W-06 glass, SW-01 glass door, small jali at the left, courtyard pavers
rep('''// full-height glass behind the stair (stair / courtyard side), with slim black mullions
(() => {
  const g = R(490, 958, 865, 962);
  tall(box(g.w, H_FULL, 0.08, g.cx, 0, g.cz, M(C.glass, { r: 0.1, t: 0.3 }), false), 0, H_FULL);
  const n = Math.round(g.w / 4);
  for (let i = 0; i <= n; i++) tall(box(0.12, H_FULL, 0.14, g.x0 + i * g.w / n, 0, g.cz, M(C.black)), 0, H_FULL);
})();''',
'''// behind the stair: W-06 full-height glass (14'-2" × 9'-6") and the SW-01 glass door (3'-4" × 9'-6") to the courtyard
glassPanel([494, 945, 788, 949]);
glassPanel([790, 945, 863, 949]);
tall(box(0.1, 2.4, 0.3, R(850, 945, 852, 949).cx, 3.0, R(850, 945, 852, 949).cz, M(C.black, { m: 0.6, r: 0.3 })), 3.0, 2.4);''')

# --- formal living: open to the foyer, TV wall on the south, SD-01 sliding glass to the planter, brick jali outside
rep('''tv([985, 700, 1230, 718], "x");
panelWall([1060, 712, 1160, 720], C.walnut, 8.6);''', '''tv([985, 738, 1230, 756], "x");
panelWall([1060, 752, 1160, 758], C.walnut, 8.6);
wall(R(966, 0, 0, 0).x0, R(0, 762, 0, 0).z0, R(1281, 0, 0, 0).x0, R(0, 762, 0, 0).z0);   // TV wall; open to the foyer west of it''')
rep('''panelWall([1265, 375, 1285, 710], C.brick, 9.2);''', '''glassPanel([1252, 381, 1258, 705]);            // SD-01 sliding glass door, 15'-3" × 9'-6"
wallPiece([1252, 705, 1258, 762], 0, H_FULL);
brickJali([1263, 381, 1271, 572]);              // brick jali in the planter outside''')

# --- interior doors from the ground floor door schedule
rep('''// stair + jali + garden
stair([495, 795, 862, 945]);
panelWall([495, 975, 600, 990], C.brick, 9.2);   // short jali at the west (left) end only''',
'''// doors from the schedule: D-02 guest bed 3'-4", D-03 kitchen balcony 3'-0", D-04 toilet + generator 2'-6", all 7'-0" high
door([477, 846, 489, 918]);
door([246, 615, 258, 680]);
door([356, 723, 410, 735]);
door([115, 1016, 169, 1028]);
// stair + small brick jali at its left (west) end + courtyard
stair([495, 795, 862, 945]);
brickJali([495, 951, 565, 959]);
for (let i = 0; i < 14; i++) { const x = 516 + i * 24.2; rbox(R(x, 986, x + 17, 1058), 0.08, M(C.paving, { r: 0.9 }), 0.001); }''')

# --- foyer
rep('''counter([875, 960, 900, 1060], 3.0, C.teak, C.teak);
wardrobe([875, 1145, 980, 1170], 7.2);''', '''cushionSeat([876, 958, 898, 1137]);            // low height cabinet with seater
counter([876, 1140, 976, 1168], 3.0, C.teak, C.stone);   // shoe cabinet''')
start = s.index("// foyer walls as drawn")
end = s.index("// parking\n", start)
s = s[:start] + '''// foyer walls as drawn
//   west (stair side): wall, W-07 window 5'-0" × 6'-6", wall
//   east (parking side): W-08 small full-height glass 2'-0" × 7'-6", facing brick wall, D-01 main door 5'-0" × 7'-6", return
(() => {
  const W = 874, E = 984, seg = (px, y0, y1) => { const a = R(px - 4, y0, px + 4, y1); wall(a.cx, a.z0, a.cx, a.z1); };
  seg(W, 809, 960);
  wallPiece([W - 4, 960, W + 4, 1058], 0, 1.0); glassPanel([W - 2, 960, W + 2, 1058], 6.5, 1.0); wallPiece([W - 4, 960, W + 4, 1058], 7.5, 2.0);
  seg(W, 1058, 1170);
  glassPanel([E - 2, 770, E + 2, 813], 7.5); wallPiece([E - 4, 770, E + 4, 813], 7.5, 2.0);
  seg(E, 813, 1029);
  const d = R(E - 4, 1029, E + 4, 1133), dh = 7.5;
  tall(box(0.25, dh, d.d - 0.1, d.cx, 0, d.cz, M(C.walnut, { r: 0.6 })), 0, dh);
  for (let g = 1; g < 5; g++) tall(box(0.29, dh - 0.8, 0.04, d.cx, 0.4, d.z0 + g * d.d / 5, M(C.espresso)), 0.4, dh - 0.8);
  tall(box(0.4, 3.0, 0.1, d.cx, 2.2, d.z1 - 0.5, M(C.black, { m: 0.6, r: 0.3 })), 2.2, 3.0);
  wallPiece([E - 4, 1029, E + 4, 1133], dh, H_FULL - dh);
  seg(E, 1133, 1170);
})();
''' + s[end:]

# --- 1st floor tile sizes (common 32" × 32", toilets 12" × 24")
s = s.replace('floor: "wet" });', 'floor: "wet", tile: [12, 24] });')
for name in ["Sister Bed", "Parents Bed", "Primary Bed", "Bother Bed"]:
    i = s.index(f'name: "{name}"'); j = s.index("});", i)
    s = s[:i] + s[i:j].replace('floor: "wood"', 'tile: [32, 32]') + s[j:]
for name in ["Corridor", "Family Living"]:
    i = s.index(f'name: "{name}"'); j = s.index("});", i)
    s = s[:i] + s[i:j] + ', tile: [32, 32]' + s[j:]
i = s.index('name: "Stair", dim: "17\'-6'); j = s.index("});", i)
s = s[:i] + s[i:j].replace('floor: "stone"', 'tile: [32, 32]') + s[j:]

rep('''["oak", "Light wood & bedroom floor"]''', '''["oak", "Light wood"]''')
rep('''["brick", "Brick jali & feature walls"]''', '''["brick", "Brick jali & feature walls"]''')
rep('''["tile", "Floor tile"]''', '''["tile", "Floor tile (32\\" × 32\\")"]''')
open(p, "w", encoding="utf-8").write(s)
print("patched")
