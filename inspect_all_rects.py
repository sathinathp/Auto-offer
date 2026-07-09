import pdfplumber

def inspect_all_rects(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[4]  # Page 5
        print(f"Page 5 size: {page.width}x{page.height}")
        
        # Look for rectangles with fills
        fills = [r for r in page.rects if r.get('non_stroking_color') is not None]
        print(f"Total rectangles: {len(page.rects)}")
        print(f"Fills count: {len(fills)}")
        
        unique_colors = set()
        for r in page.rects:
            color = r.get('non_stroking_color')
            if color is not None:
                if isinstance(color, list) or isinstance(color, tuple):
                    unique_colors.add(tuple(color))
                else:
                    unique_colors.add(color)
        print("Unique background colors in rects:", unique_colors)
        
        # Print a few rects that might have actual colors
        for idx, r in enumerate(page.rects):
            col = r.get('non_stroking_color')
            if col != 1.0 and col != (1, 1, 1) and col is not None:
                print(f"Rect {idx}: bbox=({r['x0']:.1f}, {r['top']:.1f}, {r['x1']:.1f}, {r['bottom']:.1f}), color={col}")
                
if __name__ == "__main__":
    inspect_all_rects("template_original.pdf")
