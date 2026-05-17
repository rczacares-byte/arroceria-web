import os
from PIL import Image
from rembg import remove

for file in os.listdir("."):
    if file.lower().endswith((".png", ".webp", ".jpg", ".jpeg")) and not file.endswith("_nobg.png"):
        try:
            img = Image.open(file).convert("RGBA")
            corners = [
                img.getpixel((0, 0)),
                img.getpixel((img.width - 1, 0)),
                img.getpixel((0, img.height - 1)),
                img.getpixel((img.width - 1, img.height - 1))
            ]
            if all(c[3] > 250 for c in corners):
                print(f"Removing background from {file}")
                with open(file, 'rb') as i:
                    input_data = i.read()
                output_data = remove(input_data)
                
                out_name = os.path.splitext(file)[0] + "_nobg.png"
                with open(out_name, 'wb') as o:
                    o.write(output_data)
                
                out_img = Image.open(out_name)
                bbox = out_img.getbbox()
                if bbox:
                    out_img = out_img.crop(bbox)
                    out_img.save(out_name)
                
                print(f"Saved {out_name}")
        except Exception as e:
            print(f"Error {file}: {e}")
