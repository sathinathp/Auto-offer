import pdfplumber

def inspect_table_cells(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[4]  # Page 5
        tables = page.find_tables()
        if not tables:
            print("No tables found")
            return
        
        table = tables[0]
        print(f"Table bbox: {table.bbox}")
        for r_idx, row in enumerate(table.rows):
            print(f"Row {r_idx + 1}:")
            for c_idx, cell in enumerate(row.cells):
                if cell:
                    # cell is a bbox tuple: (x0, y0, x1, y1)
                    print(f"  Cell {c_idx + 1}: bbox=({cell[0]:.1f}, {cell[1]:.1f}, {cell[2]:.1f}, {cell[3]:.1f})")
                else:
                    print(f"  Cell {c_idx + 1}: None")

if __name__ == "__main__":
    inspect_table_cells("template_original.pdf")
