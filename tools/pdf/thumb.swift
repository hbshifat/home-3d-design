import PDFKit; import AppKit
let doc = PDFDocument(url: URL(fileURLWithPath: CommandLine.arguments[1]))!
for i in [1,2] { let p = doc.page(at: i)!
  let img = p.thumbnail(of: NSSize(width: 2400, height: 1700), for: .mediaBox)
  let rep = NSBitmapImageRep(data: img.tiffRepresentation!)!
  try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: "\(CommandLine.arguments[2])/r\(i+1).png")); print(img.size) }
