# Design session notes

Session dates: 30 October – 1 November 2026. Owner: Hasanul Banna Shifat. Built with Claude Code.

## Sources

| Source | Used for |
|---|---|
| YouTube video "3000 sq. ft. Home Is All About Comfort & Calm" | Color palette (frames sampled, k-means clustered) |
| `SHIFAT BHAI- 3D.skp` (SketchUp 2021) | Material list for the 60-30-10 recolor script (geometry is not readable outside SketchUp) |
| Minimal Ltd furniture layout PDF (20.05.26) | Room layout and furniture positions (traced; "Scale: N/A") |
| Dhaka Designer "Final Architectural Working Drawing, April 2026" (36 sheets) | Door/window schedules, tile sizes, stair, foyer, brick jali, roof floor and roof slab |
| Exterior reference render (brick box with triangle jali, perforated roof frame) | Street-front design |
| Reference photos | Wooden slat screen, window safety grill |
| Minimal Ltd "Electrical & Plumbing Drawing" (05.07.26, 11 sheets) | Lights, fans, switch boards, sockets, AC and exhaust points |

## Palette (60-30-10, warm earthy)

| Role | Colors |
|---|---|
| 60% base | Warm off-white `#E4E6E2`, cream-beige `#D3C4AE`, greige `#AEAB9C` |
| 30% wood | Honey oak `#A68C6D`, teak `#917658`, walnut `#67492C`, espresso `#4E2D19` |
| 10% accent | Terracotta `#965D34`, sage `#808880`, charcoal `#363A2F`, black `#1B1A12` |

Presets in the viewer: Warm earthy, Scandi light, Moody dark, Coastal.

## What was built, in order

1. **Palette** from the video, and a SketchUp Ruby script applying it to the `.skp` materials.
2. **3D viewer** from the furniture layout: both floors, rooms, furniture, labels, room list, cutaway/full walls.
3. **Color settings panel** with presets, saved per browser.
4. **Stair**: three flights with two landings, starting at the guest bed wall.
5. **Comment-driven fixes**: removed a tree, glass behind the stair, short brick jali at the left, dining and drawing room opened up, foyer walls with the small full-height glass, main door.
6. **Matched to the working drawing**:
   - stair 3 + landing + 12 + landing + 4 steps (stair lighting plan);
   - glass W-06 and swing door SW-01 behind the stair;
   - foyer opens into the drawing room; W-07 window and W-08 full-height glass;
   - doors D-01 to D-04 (ground) and D-01, D-02 (1st floor) at schedule sizes;
   - all windows W-01 to W-09 and TW-01 on both floors, sliding doors SD-01 and SD-02;
   - floor tiles: common 32×32", kitchen/toilets 12×24", storage 24×24", balcony 6×36", parking 8×8", entrance 12×36";
   - brick jali as the triangle-block pattern from the south elevation.
7. **Main door** per detail D-01: 3'-4" leaf with perforated brass panel, 1'-2" glass sidelight. **Front steps** per plan levels (+0'-0" to +5'-0"), plinth, road-level parking.
   The owner later changed the front steps from six to three (1'-0" each, +0'-0" to +3'-0").
8. **Walls**: neighbouring rooms' walls merged; missing walls added; generator room removed; storage/kitchen-balcony wall removed.
9. **Wooden slat screen** between dining and drawing room (from photo).
10. **Safety grill** on every window and glass panel (pattern from photo, MS square bars at about 4").
11. **Realistic rendering**: environment light, GTAO ambient occlusion, wood/fabric/plaster/tile textures, warm room lights, ground.
12. **Curtains** with pleats, drapes and sheers on every living-space window; Curtains on/off button. **Zoom** controls.
13. **Exterior** after the reference render, on the street (east) face: facing-brick foyer wall with wall light, gates, low jali wall, terrace planters, brick box with window and jali on Bed-01.
14. **Roof** from sheets A.03 and A.12: stair head and corridor under Slab-1 (10'-6"), east terrace under Slab-2 (13'-6") with round cut-outs, perforated north wall. The two roof bedrooms (Bed-05, Bed-06) were then removed at the owner's request; that part is open roof with parapets.
15. **Boundary wall** from the ground floor plan: 7 ft walls on the north, back (west) and south sides, and on the street side a low wall with a jali band before the formal living planter, the car and pedestrian gates, and pillars.
16. **Measurement audit** against sheet A.16 (ground) and A.20 (1st floor), mapped at one scale for both axes:
    most rooms, walls, doors and windows were within about 0.5 ft. Fixed: kitchen balcony depth (it ran over the
    common toilet), the west side steps and side path (+4'-6" down to +1'-6"), the planter on the street side
    running to the TV wall line, the formal living north wall over the jali strip, room labels (kitchen
    10'-10" × 16'-5", storage 6'-7" × 10'-8", stair 17'-6" × 7'-0", parking 19'-3" × 8'-2"), and the Bed-01 brick
    box proportions from the street elevation (8'-0" jali, 5'-6" window).

17. **Roof shed circles**: the Slab-2 cut-outs and the north wall holes follow A.12 and the A.06 elevation (4 × 5 grid, 1'-0" and 1'-8" holes). The south side of the shed went back to a solid wall.
18. **Electrical layout** from the Minimal Ltd E&P drawing: ceiling spot lights, down lights, ceiling fans, chandeliers,
    wall lights (7'-6"), exhaust fans, split AC units (7'-0" top), switch boards (4'-4"), and bed side (2'-0"),
    fridge (1'-6") and counter (42") sockets on both floors. Symbols were found by color on the rendered sheets
    (`tools/electrical/`) and mapped onto the plan; wall items snap to the nearest wall face. Electrical on/off button.
    Then the smaller points: geysers (from the geyser layouts), CCTV cameras, Wi-Fi mesh routers, SDBs, kitchen hood
    multi socket, basin sockets (4'-4"), calling bell (7'-6") and dish (Akash line) outlets.

## Decisions made by the owner

- No separation wall between drawing and dining room (the drawing shows a dining-wagon partition); a wooden slat screen instead.
- Brick jali behind the stair only as a short piece at the left.
- Street front is the east face (main door side), not the south face.
- Grill pattern kept as in the photo.
- No rooms on the roof.

## Known simplifications and open points

- Plans were traced from PDFs marked "Scale: N/A": sizes are close, not survey-exact. The 1st-floor trace sits about 2.5 ft behind the ground-floor front; the exterior brings the front elements forward to compensate.
- Entrance levels: the plan labels the platform +3'-6" and step 8 +4'-6" (a 1 ft riser); followed as drawn.
- Main door hand (leaf south, sidelight north) read from the door swing.
- Windows are drawn on the wall faces, not cut through them.
- Bed-03's west window W-04 is mostly behind the oak panel wall from the furniture layout.
- W-09 (stair east wall) is hidden behind the family living brick feature wall.
- Roof cut-out circles are placed loosely, not on A.12's exact grid.
- Facing brick on the foyer street wall is modelled; other "facing brick" notes only where visible from the street.
- It is a real-time web model; photo-quality renders need Enscape/V-Ray on the SketchUp model.
