import PDFKit
import AppKit
let args = CommandLine.arguments
let doc = PDFDocument(url: URL(fileURLWithPath: args[1]))!
let outDir = args[2]
let width = CGFloat(Double(args[3])!)
let pages: [Int] = args.count > 4 ? args[4].split(separator: ",").map { Int($0)! } : Array(1...doc.pageCount)
for n in pages {
  let p = doc.page(at: n - 1)!
  let b = p.bounds(for: .mediaBox)
  let rot = p.rotation % 180 != 0
  let w = rot ? b.height : b.width, h = rot ? b.width : b.height
  let img = p.thumbnail(of: NSSize(width: width, height: width * h / w), for: .mediaBox)
  let rep = NSBitmapImageRep(data: img.tiffRepresentation!)!
  try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: "\(outDir)/p\(n).png"))
  let t = (p.string ?? "").replacingOccurrences(of: "\n", with: " | ")
  print("=== p\(n) [\(Int(b.width))x\(Int(b.height)) rot \(p.rotation)]: \(String(t.prefix(300)))")
}
