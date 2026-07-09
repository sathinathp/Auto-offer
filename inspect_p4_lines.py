import fitz

def main():
    doc = fitz.open("Gampa Usha Offer letter (1).pdf")
    page = doc[3]
    drawings = page.get_drawings()
    print(f"Total drawings: {len(drawings)}")
    for idx, d in enumerate(drawings):
        r = d["rect"]
        height = r[3] - r[1]
        width = r[2] - r[0]
        # Look for horizontal lines/strokes
        if height < 2 and width > 100:
            print(f"Horizontal Line {idx}: y={round(r[1], 2)}, width={round(width, 2)}, height={round(height, 2)}, color={d.get('color')}, fill={d.get('fill')}")

if __name__ == "__main__":
    main()
