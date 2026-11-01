# home-3d-design

3D interior and exterior model of the Shifat residence (Sylhet), built in the browser with Three.js.

Live version: https://claude.ai/artifact/GyzM9PcdHyhV9YPPUp637v

## What's here

| Path | What it is |
|---|---|
| `index.html` | The whole 3D viewer in one file: ground floor, 1st floor, roof, exterior, color settings. Open it in a browser (or serve the folder) to run it. |
| `sketchup/palette-60-30-10.rb` | SketchUp Ruby script that recolors the `.skp` model's materials with the 60-30-10 warm-earthy palette. One undo reverts it. |
| `tools/pdf/` | Small Swift scripts (macOS PDFKit) used to render the PDF drawings to images and stitch contact sheets. |
| `tools/patches/` | The Python edit scripts used during the session to change `index.html`. Already applied; kept as a record. |
| `SESSION.md` | Notes from the design session: requests, decisions, sources and open points. |

The PDF drawings and rendered page images are not in the repo (they are the architects' documents).

## Running

```bash
python3 -m http.server 8765
```

Then open http://localhost:8765/ — the page loads Three.js 0.160.0 from jsDelivr, so it needs internet.

## Viewer controls

- **Ground floor / 1st floor / Both / Exterior** — Exterior stacks both floors and looks at the street (east) front.
- **Cutaway / Full walls**, **Labels**, **Realistic** (ambient occlusion + environment light), **Curtains**, **Zoom** (− / slider / + / Fit).
- Room list flies the camera to a room; the color panel edits the 60-30-10 palette (saved in the browser).

## Tools

```bash
swiftc -O tools/pdf/render.swift -o render
./render "drawing.pdf" out/ 4000 2,3,4      # render pages 2–4 at 4000 px wide
swiftc -O tools/pdf/sheet.swift -o sheet
./sheet "$PWD/sheet.png" 4 500 out/p{1..12}.png   # 4-column contact sheet
```
