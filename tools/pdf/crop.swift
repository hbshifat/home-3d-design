import AppKit
// crop in.png out.png x y w h [outWidth]
let a = CommandLine.arguments
let img = NSImage(contentsOfFile: a[1])!
let rep0 = NSBitmapImageRep(data: img.tiffRepresentation!)!
let x = Int(a[3])!, y = Int(a[4])!, w = Int(a[5])!, h = Int(a[6])!
let ow = a.count > 7 ? Int(a[7])! : w, oh = ow * h / w
let cg = rep0.cgImage!.cropping(to: CGRect(x: x, y: y, width: w, height: h))!
let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: ow, pixelsHigh: oh, bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
NSGraphicsContext.current!.imageInterpolation = .high
NSImage(cgImage: cg, size: NSSize(width: w, height: h)).draw(in: NSRect(x: 0, y: 0, width: ow, height: oh))
NSGraphicsContext.current = nil
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[2]))
