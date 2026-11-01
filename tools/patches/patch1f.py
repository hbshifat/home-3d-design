import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
def rep(old, new):
    global s
    n = s.count(old)
    if n != 1: sys.exit(f"expected 1 of {old[:70]!r}, found {n}")
    s = s.replace(old, new)

rep('''// Closed door on a wall:''', '''// Window on a solid wall: framed glass a little proud of both faces, from sill to head height.
function windowOn(a, sill, h) {
  const r = R(...a), alongX = r.w > r.d, len = alongX ? r.w : r.d, t = T + 0.1, f = t + 0.04;
  tall(box(alongX ? len : t, h, alongX ? t : len, r.cx, sill, r.cz, M(C.glass, { r: 0.08, m: 0.4 })), sill, h);
  for (const y of [sill, sill + h - 0.12]) tall(box(alongX ? len : f, 0.12, alongX ? f : len, r.cx, y, r.cz, M(C.black)), y, 0.12);
  for (const e of [0, 1]) tall(box(alongX ? 0.12 : f, h, alongX ? f : 0.12, alongX ? r.x0 + e * len : r.cx, sill, alongX ? r.cz : r.z0 + e * len, M(C.black)), sill, h);
}
// Closed door on a wall:''')

rep('''r: [1225, 205, 1590, 645], extra: [[1090, 450, 1225, 645]], walls: "ne",''', '''r: [1225, 205, 1590, 645], extra: [[1090, 450, 1225, 645]], walls: "n",''')
rep('''r: [1035, 655, 1395, 1160], walls: "es" ,''', '''r: [1035, 655, 1395, 1160], walls: "s",''')
rep('''railing([545, 958, 1030, 964]);''', '''// W-07 full-height glass between the stair and the double-height void, small brick jali at its left, planter ledge
glassPanel([548, 940, 929, 946]);
brickJali([551, 949, 641, 957]);
counter([929, 940, 1027, 966], 1.6, C.charcoal, C.grass);''')

rep('''// ---------- floor modes ----------''', '''// 1st floor doors and windows from the working drawing (sheets A.20 / A.21)
// doors: D-01 bedrooms 3'-4" × 7'-0", D-02 attached toilets 2'-6" × 7'-0"
door([388, 646, 480, 658]); door([658, 646, 744, 658]); door([1139, 646, 1228, 658]); door([398, 799, 490, 811]);
door([460, 441, 529, 453]); door([628, 441, 697, 453]); door([1145, 441, 1214, 453]); door([258, 780, 327, 792]);
// north face: W-02 4'-0" and W-03 6'-6" (× 6'-6"), TW-01 toilet windows 1'-8" × 4'-0", W-01 1'-0" × 9'-6"
windowOn([300, 206, 403, 214], 1.0, 6.5); windowOn([798, 206, 966, 214], 1.0, 6.5); windowOn([1282, 206, 1384, 214], 1.0, 6.5);
windowOn([464, 206, 505, 214], 3.5, 4.0); windowOn([687, 206, 728, 214], 3.5, 4.0); windowOn([1172, 206, 1213, 214], 3.5, 4.0);
windowOn([1446, 206, 1467, 214], 0, H_FULL);
// west face: W-04 7'-0" (Bed-03), TW-01 (Bed-04 toilet), W-05 6'-3" (Bed-04)
windowOn([106, 409, 114, 588], 1.0, 6.5); windowOn([106, 731, 114, 780], 3.5, 4.0); windowOn([106, 931, 114, 1090], 1.0, 6.5);
// Bed-04 east wall onto the void: W-06 3'-6" × 6'-6"
windowOn([526, 988, 534, 1082], 1.0, 6.5);
// Family living west, onto the void: W-08 5'-0" × 6'-6" in a wall
wallPiece([1029, 960, 1037, 1090], 0, 1.0); glassPanel([1031, 960, 1035, 1090], 6.5, 1.0); wallPiece([1029, 960, 1037, 1090], 7.5, 2.0);
wallPiece([1029, 1090, 1037, 1160], 0, H_FULL);
// Family living east: SD-01 sliding glass to the terrace, 18'-2" × 8'-6"
glassPanel([1388, 667, 1394, 1153], 8.5); wallPiece([1387, 667, 1395, 1153], 8.5, 1.0);
// Bed-01 east: SD-02 sliding glass to the planter, 11'-9" × 9'-4", with the brick jali in the planter outside
wallPiece([1582, 210, 1590, 281], 0, H_FULL); glassPanel([1584, 281, 1588, 590], 9.33); wallPiece([1582, 590, 1590, 645], 0, H_FULL);
brickJali([1621, 219, 1629, 431]);

// ---------- floor modes ----------''')
open(p, "w", encoding="utf-8").write(s)
print("patched")
