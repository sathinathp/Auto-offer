import pdfplumber

def inspect_tables(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[4]  # Page 5
        print(f"Page 5 size: {page.width}x{page.height}")
        
        # Extract tables
        tables = page.find_tables()
        print(f"Tables count: {len(tables)}")
        for idx, table in enumerate(tables):
            print(f"\n--- Table {idx + 1} ---")
            print(f"BBox: {table.bbox}")
            # print rows
            for r_idx, row in enumerate(table.extract()[:10]):
                print(f"  Row {r_idx + 1}: {row}")
                
        # Extract drawings (rects, lines) on page 5 to see background colors/fills
        print("\nPage 5 Rectangles:")
        for r_idx, rect in enumerate(page.rects[:10]):
            print(f"  Rect {r_idx}: x0={rect['x0']:.1f}, y0={rect['top']:.1f}, x1={rect['x1']:.1f}, y1={rect['bottom']:.1f}, non_stroking_color={rect.get('non_stroking_color')}, stroking_color={rect.get('stroking_color')}")
            
        print("\nPage 5 Lines:")
        for l_idx, line in enumerate(page.lines[:10]):
            print(f"  Line {l_idx}: x0={line['x0']:.1f}, y0={line['top']:.1f}, x1={line['x1']:.1f}, y1={line['bottom']:.1f}, color={line.get('stroking_color')}")

if __name__ == "__main__":
    inspect_tables("template_original.pdf")
