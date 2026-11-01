import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
def rep(old, new):
    global s
    n = s.count(old)
    if n != 1: sys.exit(f"expected 1 of {old[:70]!r}, found {n}")
    s = s.replace(old, new)

# room floors can sit at another level (feet relative to the house floor)
rep('''    const s = box(p.w, 0.3, p.d, p.cx, -0.3, p.cz, mat, false); s.receiveShadow = true;''',
    '''    const s = box(p.w, 0.3, p.d, p.cx, (def.level || 0) - 0.3, p.cz, mat, false); s.receiveShadow = true;''')
rep('''    lab.position.set(lp.cx, 0.6, lp.cz);''', '''    lab.position.set(lp.cx, 0.6 + (def.level || 0), lp.cz);''')

# parking at road level; entrance platform at +3'-6" (house floor is +5'-0")
rep('''r: [985, 770, 1390, 940], walls: "", floor: "paving", tile: [8, 8] });''',
    '''r: [985, 770, 1390, 940], walls: "", floor: "paving", tile: [8, 8], level: -4.5 });''')
rep('''r: [985, 945, 1135, 1170], walls: "", floor: "paving", tile: [12, 36] });''',
    '''r: [1027, 942, 1133, 1131], walls: "", floor: "paving", tile: [12, 36], level: -1.5 });''')

# perforated brass panel for the main door
rep('''// Closed door on a wall:''', '''// Perforated brass sheet (main door panel): a grid of round holes.
const perfTex = (() => {
  const c = document.createElement("canvas"); c.width = c.height = 64;
  const g = c.getContext("2d");
  g.fillStyle = "#fff"; g.fillRect(0, 0, 64, 64);
  g.fillStyle = "#2a2118";
  for (const [x, y] of [[16, 16], [48, 16], [0, 48], [32, 48], [64, 48]]) { g.beginPath(); g.arc(x, y, 7, 0, Math.PI * 2); g.fill(); }
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace;
  return t;
})();
// Closed door on a wall:''')

# main door D-01 as detailed on sheet A.18
rep('''  const d = R(E - 4, 1029, E + 4, 1133), dh = 7.5;
  tall(box(0.25, dh, d.d - 0.1, d.cx, 0, d.cz, M(C.walnut, { r: 0.6 })), 0, dh);
  for (let g = 1; g < 5; g++) tall(box(0.29, dh - 0.8, 0.04, d.cx, 0.4, d.z0 + g * d.d / 5, M(C.espresso)), 0.4, dh - 0.8);
  tall(box(0.4, 3.0, 0.1, d.cx, 2.2, d.z1 - 0.5, M(C.black, { m: 0.6, r: 0.3 })), 2.2, 3.0);''',
'''  // D-01 (sheet A.18), 5'-0" × 7'-6": 2" walnut frame, 1'-2" fixed glass sidelight in two panes,
  // 3'-4" leaf with a perforated brass panel and a long pull handle on the latch side
  const d = R(E - 4, 1029, E + 4, 1133), dh = 7.5, fr = 2 / 12, side = 14 / 12, x = d.cx;
  const frame = M(C.walnut, { r: 0.6 });
  const post = z => tall(box(0.35, dh, fr, x, 0, z, frame), 0, dh);
  const zS = d.z0 + fr, zM = zS + side, zL = zM + fr;          // sidelight from zS to zM, leaf from zL to the far post
  post(d.z0 + fr / 2); post(zM + fr / 2); post(d.z1 - fr / 2);
  tall(box(0.35, fr, d.d, x, dh - fr, d.cz, frame), dh - fr, fr);
  tall(box(0.06, dh - fr, side, x, 0, (zS + zM) / 2, M(C.glass, { r: 0.1, t: 0.3 }), false), 0, dh - fr);
  tall(box(0.3, 0.12, side, x, 2.75, (zS + zM) / 2, frame), 2.75, 0.12);
  const lw = d.z1 - fr - zL, lc = zL + lw / 2;
  tall(box(0.22, dh - fr, lw, x, 0, lc, frame), 0, dh - fr);
  const map = perfTex.clone(); map.needsUpdate = true; map.repeat.set((lw - 0.7) * 3, 6.2 * 3);
  tall(box(0.26, 6.2, lw - 0.7, x, 0.55, lc, new THREE.MeshStandardMaterial({ color: 0xC9A86A, map, metalness: 0.55, roughness: 0.4 })), 0.55, 6.2);
  tall(box(0.42, 3.6, 0.1, x, 1.9, zL + 0.25, M(C.black, { m: 0.6, r: 0.3 })), 1.9, 3.6);''')

# road-level parking: car down, plinth under the raised house, front steps and outside paving
rep('''car([1010, 752, 1330, 888]);''', '''{ const n = G.children.length; car([1010, 785, 1330, 925]); G.children.slice(n).forEach(o => o.position.y -= 4.5); }
// plinth: the house floor stands 5'-0" above the road (sheet A.01 levels)
{ const pl = M(0xB4ADA0); for (const a of [[103, 365, 985, 1170], [985, 365, 1395, 770]]) { const r = R(...a); box(r.w, 4.7, r.d, r.cx, -5, r.cz, pl, false); } }
// front entrance steps (sheet A.01): outside +0'-0", steps 1–6 rise 6" each to +3'-0",
// entrance platform (7) at +3'-6", step 8 at +4'-6" by the main door, foyer +5'-0"
{
  const LV = l => l - 5;
  const block = (a, top, tile = [12, 36]) => { const r = R(...a); box(r.w, top - LV(0), r.d, r.cx, LV(0), r.cz, tileMat(C.paving, r.w, r.d, ...tile)); };
  [1133, 1150, 1167, 1185, 1203, 1220].forEach((x0, i, xs) => block([x0, 942, xs[i + 1] ?? 1238, 1086], LV(3.0 - i * 0.5)));
  block([984, 942, 1027, 1131], LV(4.5));
  box(R(1027, 942, 1133, 1131).w, 3.2, R(1027, 942, 1133, 1131).d, R(1027, 942, 1133, 1131).cx, LV(0), R(1027, 942, 1133, 1131).cz, M(0xB4ADA0), false);
  block([984, 1131, 1133, 1168], LV(3.5));
  { const n = G.children.length; counter([988, 1136, 1124, 1166], 1.4, C.charcoal, C.grass); G.children.slice(n).forEach(o => o.position.y += LV(3.5)); }
  const out = R(1133, 942, 1395, 1168);
  box(out.w, 0.3, out.d, out.cx, LV(0) - 0.3, out.cz, tileMat(C.paving, out.w, out.d, 8, 16), false);
}''')
open(p, "w", encoding="utf-8").write(s)
print("patched")
