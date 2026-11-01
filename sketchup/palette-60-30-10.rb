# 60-30-10 warm-earthy palette for "SHIFAT BHAI- 3D.skp"
# Palette taken from the "3000 sq. ft. Home Is All About Comfort & Calm" video.
#
# HOW TO RUN (SketchUp 2021 or newer):
#   1. Open "SHIFAT BHAI- 3D.skp" and do File > Save As... a COPY first.
#   2. Window > Ruby Console.
#   3. Type:  load "/Users/hasanulbannashifat/Documents/SHIFAT BHAI - 60-30-10 palette.rb"
#      (on Windows, change the path to where you put this file)
#   4. Press Enter. One Ctrl+Z (Cmd+Z) undoes everything.
#
# Only flat-color materials are recolored. Materials with an image texture (wood grain,
# concrete, stone, grass, plants) keep their texture; woods get a warm tint.

PALETTE = {
  # 60% - dominant: walls, ceilings, large surfaces
  cream:      [0xE4, 0xE6, 0xE2], # warm off-white  #E4E6E2 (ceilings, interior walls)
  beige:      [0xD3, 0xC4, 0xAE], # cream-beige     #D3C4AE (main exterior walls)
  greige:     [0xAE, 0xAB, 0x9C], # greige          #AEAB9C (secondary walls, boundary wall)
  # 30% - secondary: wood
  honey_oak:  [0xA6, 0x8C, 0x6D], # #A68C6D
  teak:       [0x91, 0x76, 0x58], # #917658
  walnut:     [0x67, 0x49, 0x2C], # #67492C
  espresso:   [0x4E, 0x2D, 0x19], # #4E2D19
  # 10% - accent: metal, terracotta, sage
  charcoal:   [0x36, 0x3A, 0x2F], # #363A2F
  black:      [0x1B, 0x1A, 0x12], # #1B1A12
  terracotta: [0x96, 0x5D, 0x34], # #965D34
  sage:       [0x80, 0x88, 0x80], # #808880
  glass:      [0x9F, 0xA8, 0xA4]  # neutral grey-green glass tint
}.freeze

# Material name in this model => palette color
MAPPING = {
  # --- 60% walls / ceilings / slabs
  "_auto_1"                   => :cream,     # pure white  -> warm off-white
  "[Color H08]"               => :cream,
  "_42"                       => :cream,
  "_auto_22"                  => :beige,     # light grey walls -> cream-beige
  "_auto_19"                  => :beige,
  "_auto_12"                  => :greige,
  "_auto_11"                  => :greige,
  "_auto_16"                  => :greige,
  "[Polished Concrete New]1"  => :greige,
  "_8"                        => :greige,    # stone cladding (keeps texture, warm grey tint)
  # --- 30% wood
  "_"                         => :teak,
  "Wood 47"                   => :teak,
  "[0119_RosyBrown]"          => :teak,
  "[Wood Veneer 01]2"         => :teak,
  "Wood 43"                   => :teak,
  "_5"                        => :honey_oak,
  "_13"                       => :honey_oak,
  "[Wood_Cherry_Original]1"   => :honey_oak,
  "_17"                       => :honey_oak,
  "_43"                       => :walnut,
  "_48"                       => :walnut,
  "_16"                       => :espresso,
  # --- 10% accents
  "[0136_Charcoal]"           => :black,     # window frames, railings
  "[Color M08]"               => :black,
  "[0135_DarkGray]"           => :charcoal,
  "[Color M07]"               => :charcoal,
  "Material2 metal"           => :charcoal,
  "Material metal2"           => :charcoal,
  "_auto_"                    => :charcoal,
  "_auto_5"                   => :charcoal,
  "_auto_13"                  => :charcoal,
  "21824035__Plastic"         => :charcoal,
  "_1"                        => :terracotta, # orange/brick feature panel
  "[0013_LightCoral]"         => :terracotta,
  "[0037_SandyBrown]"         => :terracotta,
  "_3"                        => :terracotta, # rusty corten panel
  "_auto_3"                   => :terracotta, # bright orange -> burnt clay
  "[0111_SlateGray]"          => :sage,
  "Glass"                     => :glass,
  "_27"                       => :glass
}.freeze

model = Sketchup.active_model
model.start_operation("60-30-10 palette", true)
changed = []
missing = []
begin
  MAPPING.each do |name, key|
    mat = model.materials[name]
    unless mat
      missing << name
      next
    end
    rgb = PALETTE.fetch(key)
    if mat.texture
      # Keep the texture image; tint it toward the palette color.
      mat.colorize_type = Sketchup::Material::COLORIZE_TINT
    end
    mat.color = Sketchup::Color.new(*rgb)
    changed << "#{name} -> #{key}"
  end
  model.commit_operation
rescue => e
  model.abort_operation
  raise e
end

puts "Recolored #{changed.size} materials:"
changed.each { |line| puts "  #{line}" }
puts "Not found (skipped): #{missing.join(', ')}" unless missing.empty?
puts "Done. Ctrl+Z / Cmd+Z undoes it all. Render in Enscape with warm 3000K lights."
