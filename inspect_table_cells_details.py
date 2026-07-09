import pdfplumber

def inspect_table_cells(pdf_path, output_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[4]  # Page 5
        tables = page.find_tables()
        if not tables:
            print("No tables found")
            return
        
        table = tables[0]
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"Table bbox: {table.bbox}\n")
            f.write(f"Table width: {table.bbox[2] - table.bbox[0]:.2f}\n")
            f.write(f"Table height: {table.bbox[3] - table.bbox[1]:.2f}\n")
            
            # Print cell values and their bboxes
            for r_idx, row in enumerate(table.rows):
                f.write(f"\nRow {r_idx + 1}:\n")
                # Get the text inside the cells
                cells_text = page.crop(table.bbox).extract_table()[r_idx]
                for c_idx, cell in enumerate(row.cells):
                    txt = cells_text[c_idx] if c_idx < len(cells_text) else ""
                    if cell:
                        f.write(f"  Cell {c_idx + 1}: text='{txt}' | bbox=({cell[0]:.2f}, {cell[1]:.2f}, {cell[2]:.2f}, {cell[3]:.2f}) | width={cell[2]-cell[0]:.2f}\n")
                    else:
                        f.write(f"  Cell {c_idx + 1}: None\n")

if __name__ == "__main__":
    inspect_table_cells("softstandard_original.pdf", "softstandard_table_details.txt")
    print("Done! Output in softstandard_table_details.txt")
