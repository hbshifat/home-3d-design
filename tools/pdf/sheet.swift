import AppKit
// usage: sheet out.png cols cellW file1 file2 ...
let a = CommandLine.arguments
let cols = Int(a[2])!, cw = CGFloat(Double(a[3])!)
let files = Array(a[4...])
let imgs = files.map { NSImage(contentsOfFile: $0)! }
let ch = cw * imgs[0].size.height / imgs[0].size.width
let rows = (imgs.count + cols - 1) / cols
let W = Int(cw) * cols, H = Int(ch + 22) * rows
let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: W, pixelsHigh: H, bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
NSColor.white.setFill(); NSRect(x: 0, y: 0, width: W, height: H).fill()
for (i, img) in imgs.enumerated() {
  let c = i % cols, r = i / cols
  let y = CGFloat(H) - CGFloat(r + 1) * (ch + 22)
  img.draw(in: NSRect(x: CGFloat(c) * cw, y: y, width: cw - 4, height: ch))
  (URL(fileURLWithPath: files[i]).lastPathComponent as NSString).draw(at: NSPoint(x: CGFloat(c) * cw + 4, y: y + ch + 3), withAttributes: [.font: NSFont.boldSystemFont(ofSize: 15), .foregroundColor: NSColor.red])
}
NSGraphicsContext.current = nil
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[1]))
