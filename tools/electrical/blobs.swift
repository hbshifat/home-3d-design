import AppKit
// blobs in.png x0 y0 x1 y1 : connected components of saturated (non-gray) pixels inside the box
let a = CommandLine.arguments
let rep = NSBitmapImageRep(data: NSImage(contentsOfFile: a[1])!.tiffRepresentation!)!
let W = rep.pixelsWide, H = rep.pixelsHigh
let bx0 = Int(a[2])!, by0 = Int(a[3])!, bx1 = Int(a[4])!, by1 = Int(a[5])!
var px = [UInt8](repeating: 0, count: W * H * 3)
for y in 0..<H { for x in 0..<W { let c = rep.colorAt(x: x, y: y)!.usingColorSpace(.deviceRGB)!
  let i = (y * W + x) * 3; px[i] = UInt8(c.redComponent * 255); px[i+1] = UInt8(c.greenComponent * 255); px[i+2] = UInt8(c.blueComponent * 255) } }
func sat(_ i: Int) -> Bool { let r = Int(px[i*3]), g = Int(px[i*3+1]), b = Int(px[i*3+2]); return max(r,g,b) - min(r,g,b) > 70 }
var seen = [Bool](repeating: false, count: W * H)
for y in by0..<by1 { for x in bx0..<bx1 { let s = y * W + x; if seen[s] || !sat(s) { continue }
  var st = [s]; seen[s] = true; var n = 0, mnx = x, mxx = x, mny = y, mxy = y, sr = 0, sg = 0, sb = 0
  while let p = st.popLast() { n += 1; let px0 = p % W, py0 = p / W
    mnx = min(mnx, px0); mxx = max(mxx, px0); mny = min(mny, py0); mxy = max(mxy, py0)
    sr += Int(px[p*3]); sg += Int(px[p*3+1]); sb += Int(px[p*3+2])
    for dy in -1...1 { for dx in -1...1 { let qx = px0 + dx, qy = py0 + dy
      if qx < bx0 || qy < by0 || qx >= bx1 || qy >= by1 { continue }
      let q = qy * W + qx; if !seen[q] && sat(q) { seen[q] = true; st.append(q) } } } }
  if n >= 8 { print(String(format: "%d %d %d %d n=%d #%02x%02x%02x", mnx, mny, mxx - mnx + 1, mxy - mny + 1, n, sr/n, sg/n, sb/n)) } } }
