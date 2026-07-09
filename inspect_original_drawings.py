import fitz

def main():
    doc = fitz.open("Gampa Usha Offer letter (1).pdf")
    for i, page in enumerate(doc):
        print(f"--- Page {i+1} Drawings ---")
        drawings = page.get_drawings()
        print(f"Total drawings: {len(drawings)}")
        for idx, d in enumerate(drawings[:15]):
            print(f"Drawing {idx}: type={d['type']}, rect={d['rect']}, fill={d.get('fill')}, color={d.get('color')}, width={d.get('width')}")

if __name__ == "__main__":
    main()
