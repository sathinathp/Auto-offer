import fitz
import os
from PIL import Image, ImageChops, ImageDraw

def render_page_to_image(page, dpi=150):
    pix = page.get_pixmap(dpi=dpi)
    img_data = pix.tobytes("png")
    from io import BytesIO
    return Image.open(BytesIO(img_data)).convert("RGB")

def compare_pages(pdf_path_orig, pdf_path_gen, output_dir="visual_diff"):
    os.makedirs(output_dir, exist_ok=True)
    doc_orig = fitz.open(pdf_path_orig)
    doc_gen = fitz.open(pdf_path_gen)
    
    print(f"Original: {len(doc_orig)} pages, Generated: {len(doc_gen)} pages")
    
    for i in range(max(len(doc_orig), len(doc_gen))):
        print(f"Comparing Page {i+1}...")
        
        # Load images
        img_orig = None
        img_gen = None
        
        if i < len(doc_orig):
            img_orig = render_page_to_image(doc_orig[i])
            img_orig.save(os.path.join(output_dir, f"page_{i+1}_orig.png"))
            
        if i < len(doc_gen):
            img_gen = render_page_to_image(doc_gen[i])
            img_gen.save(os.path.join(output_dir, f"page_{i+1}_gen.png"))
            
        if img_orig and img_gen:
            # If size mismatch, resize the generated one to match the original
            if img_orig.size != img_gen.size:
                print(f"  Warning: Page {i+1} size mismatch: Original {img_orig.size} vs Generated {img_gen.size}. Resizing generated.")
                img_gen = img_gen.resize(img_orig.size, Image.Resampling.LANCZOS)
                
            # Create a pixel diff
            diff = ImageChops.difference(img_orig, img_gen)
            diff.save(os.path.join(output_dir, f"page_{i+1}_pixel_diff.png"))
            
            # Create a side-by-side comparison image
            w, h = img_orig.size
            comparison = Image.new("RGB", (w * 2, h))
            comparison.paste(img_orig, (0, 0))
            comparison.paste(img_gen, (w, 0))
            comparison.save(os.path.join(output_dir, f"page_{i+1}_side_by_side.png"))
            
            # Print average pixel difference
            import numpy as np
            diff_arr = np.array(diff)
            mean_diff = np.mean(diff_arr)
            print(f"  Page {i+1} Mean Pixel Difference: {mean_diff:.4f}")
            
if __name__ == "__main__":
    compare_pages("Gampa Usha Offer letter (1).pdf", "output/Gampa_Usha_PetaBytz_Offer_Letter.pdf")
