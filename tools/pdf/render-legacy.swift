import PDFKit; import AppKit
let doc = PDFDocument(url: URL(fileURLWithPath: CommandLine.arguments[1]))!
let out = CommandLine.arguments[2]; let scale = CGFloat(Double(CommandLine.arguments[3])!)
print("pages", doc.pageCount)
for i in 0..<doc.pageCount { let p = doc.page(at: i)!; let r = p.bounds(for: .mediaBox)
  print(i+1, r.size, p.string?.prefix(300).replacingOccurrences(of: "\n", with: " | ") ?? "")
  let w = Int(r.width*scale), h = Int(r.height*scale)
  let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: w, pixelsHigh: h, bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
  NSGraphicsContext.saveGraphicsState(); let ctx = NSGraphicsContext(bitmapImageRep: rep)!; NSGraphicsContext.current = ctx
  ctx.cgContext.setFillColor(.white); ctx.cgContext.fill(CGRect(x:0,y:0,width:w,height:h)); ctx.cgContext.scaleBy(x: scale, y: scale)
  p.draw(with: .mediaBox, to: ctx.cgContext); NSGraphicsContext.restoreGraphicsState()
  try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: "\(out)/p\(i+1).png")) }
