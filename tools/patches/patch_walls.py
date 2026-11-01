import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
def rep(old, new):
    global s
    n = s.count(old)
    if n != 1: sys.exit(f"expected 1 of {old[:70]!r}, found {n}")
    s = s.replace(old, new)
rep('''room({ name: "Terrace", dim: "6'-1\\" × 12'-0\\"", r: [1400, 760, 1645, 1100], walls: "", floor: "paving" });''',
    '''room({ name: "Terrace", dim: "6'-1\\" × 12'-0\\"", r: [1395, 804, 1632, 1134], walls: "ns", floor: "paving" });''')
rep('''counter([1560, 770, 1610, 1090], 1.6, C.charcoal, C.grass);
[820, 900, 980, 1050].forEach(y => plant(1585, y, 0.9));''', '''counter([1575, 812, 1625, 1126], 1.6, C.charcoal, C.grass);
[850, 930, 1010, 1090].forEach(y => plant(1600, y, 0.9));''')
rep('''// parking
{ const n''', '''// walls the working drawing shows on the south side: the outer wall below the guest bed,
// and the foyer's south wall behind the shoe cabinet
wallPiece([200, 1166, 490, 1174], 0, H_FULL);
wallPiece([866, 1166, 984, 1174], 0, H_FULL);
// parking
{ const n''')
open(p, "w", encoding="utf-8").write(s)
print("patched")
