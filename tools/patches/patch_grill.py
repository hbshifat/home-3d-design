import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
def rep(old, new):
    global s
    n = s.count(old)
    if n != 1: sys.exit(f"expected 1 of {old[:70]!r}, found {n}")
    s = s.replace(old, new)
rep('''function glassPanel(a, h = H_FULL, y0 = 0) {''', '''// Safety grill (12 mm square MS bars at about 4" centres, sheet A.26) over a glass opening, as in the
// reference photo: horizontal bars in the two outer thirds, vertical bars in the middle third.
// Openings 3 ft or narrower get vertical bars only.
function grill(r, alongX, y0, h, t) {
  const bar = M(C.black, { m: 0.5, r: 0.4 }), len = alongX ? r.w : r.d, s = 0.05, gap = 0.36;
  const at = (u, y, bw, bh) => tall(box(alongX ? bw : t, bh, alongX ? t : bw, alongX ? r.x0 + u : r.cx, y, alongX ? r.cz : r.z0 + u, bar, false), y, bh);
  const [a, b, c, d] = len > 3 ? [0, len / 3, 2 * len / 3, len] : [0, 0, len, len];
  for (const [p, q] of [[a, b], [c, d]]) if (q > p) for (let y = y0 + gap; y < y0 + h - 0.1; y += gap) at((p + q) / 2, y, q - p - 0.1, s);
  for (let u = b + gap / 2; u < c; u += gap) at(u, y0, s, h);
  if (len > 3) for (const u of [b, c]) at(u, y0, 0.1, h);   // flat dividers between the sections
}
function glassPanel(a, h = H_FULL, y0 = 0) {''')
rep('''    tall(box(0.12, h, 0.12, alongX ? r.x0 + f * len : r.cx, y0, alongX ? r.cz : r.z0 + f * len, M(C.black)), y0, h);
  }
}''', '''    tall(box(0.12, h, 0.12, alongX ? r.x0 + f * len : r.cx, y0, alongX ? r.cz : r.z0 + f * len, M(C.black)), y0, h);
  }
  grill(r, alongX, y0, h, 0.14);
}''')
rep('''  for (const e of [0, 1]) tall(box(alongX ? 0.12 : f, h, alongX ? f : 0.12, alongX ? r.x0 + e * len : r.cx, sill, alongX ? r.cz : r.z0 + e * len, M(C.black)), sill, h);
}''', '''  for (const e of [0, 1]) tall(box(alongX ? 0.12 : f, h, alongX ? f : 0.12, alongX ? r.x0 + e * len : r.cx, sill, alongX ? r.cz : r.z0 + e * len, M(C.black)), sill, h);
  grill(r, alongX, sill, h, f);
}''')
# anything that starts above the cutaway height is hidden in Cutaway (high windows, grill bars, door heads)
rep('''    m.visible = !(wallsLow && m.userData.hideLow);''', '''    m.visible = !(wallsLow && (m.userData.hideLow || y0 >= H_LOW));''')
open(p, "w", encoding="utf-8").write(s)
print("patched")
