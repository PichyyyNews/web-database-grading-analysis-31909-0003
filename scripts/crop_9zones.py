import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw

def split_9_zones(image_path, output_dir=None):
    img_path = Path(image_path)
    if not img_path.exists():
        raise FileNotFoundError(f"Image not found: {img_path}")
    
    img = Image.open(img_path).convert('RGB')
    width, height = img.size
    
    if output_dir is None:
        output_dir = img_path.parent / "inspection_9zones"
    else:
        output_dir = Path(output_dir)
        
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Calculate 3x3 step sizes
    w_step = width // 3
    h_step = height // 3
    
    zone_names = [
        "zone_1_top_left",
        "zone_2_top_center",
        "zone_3_top_right",
        "zone_4_mid_left",
        "zone_5_mid_center",
        "zone_6_mid_right",
        "zone_7_bottom_left",
        "zone_8_bottom_center",
        "zone_9_bottom_right"
    ]
    
    generated_crops = []
    
    # Create an annotated contact sheet
    contact_sheet = img.copy()
    draw = ImageDraw.Draw(contact_sheet)
    
    index = 0
    for row in range(3):
        for col in range(3):
            left = col * w_step
            upper = row * h_step
            right = width if col == 2 else (col + 1) * w_step
            lower = height if row == 2 else (row + 1) * h_step
            
            crop_box = (left, upper, right, lower)
            
            # Crop tile
            tile = img.crop(crop_box)
            tile_filename = f"{zone_names[index]}.png"
            tile_path = output_dir / tile_filename
            tile.save(tile_path, "PNG")
            generated_crops.append(str(tile_path))
            
            # Draw boundary on contact sheet
            draw.rectangle([left, upper, right, lower], outline="#DC2626", width=2)
            # Label the zone number
            draw.rectangle([left + 6, upper + 6, left + 26, upper + 26], fill="#DC2626")
            draw.text((left + 10, upper + 8), str(index + 1), fill="#FFFFFF")
            
            index += 1
            
    contact_sheet_path = output_dir / "contact_sheet_9zones.png"
    contact_sheet.save(contact_sheet_path, "PNG")
    generated_crops.append(str(contact_sheet_path))
    
    print(f"Successfully generated 9 inspection zones + contact sheet in: {output_dir}")
    return generated_crops

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_img = sys.argv[1]
    else:
        target_img = r"C:\Users\Newsk\.gemini\config\skills\charts\score_component_boxplot.png"
    split_9_zones(target_img)
