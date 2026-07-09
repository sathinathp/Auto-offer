import fitz

def main():
    doc = fitz.open("Gampa Usha Offer letter (1).pdf")
    for i, page in enumerate(doc):
        print(f"--- Page {i+1} ---")
        blocks = page.get_text("dict")["blocks"]
        for j, b in enumerate(blocks):
            if b["type"] == 1:  # Image block
                bbox = [round(x, 2) for x in b["bbox"]]
                print(f"Image Block {j}: bbox={bbox}, width={round(bbox[2]-bbox[0], 2)}, height={round(bbox[3]-bbox[1], 2)}")
        
        # Let's also check images returned by get_images()
        images = page.get_images()
        for idx, img in enumerate(images):
            # get rects
            rects = page.get_image_rects(img[0])
            print(f"  get_images[{idx}]: xref={img[0]}, width={img[2]}, height={img[3]}, rects={[r for r in rects]}")

if __name__ == "__main__":
    main()
