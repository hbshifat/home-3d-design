import PDFKit
let doc = PDFDocument(url: URL(fileURLWithPath: CommandLine.arguments[1]))!
for i in 0..<doc.pageCount { let p = doc.page(at: i)!; print("=== page \(i+1) rot \(p.rotation) media \(p.bounds(for: .mediaBox)) crop \(p.bounds(for: .cropBox))"); print(p.string ?? "") }
