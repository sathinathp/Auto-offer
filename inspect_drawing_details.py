import fitz

def main():
    doc = fitz.open("Gampa Usha Offer letter (1).pdf")
    page = doc[0]
    drawings = page.get_drawings()
    for idx in [0, 1, 3, 4]:
        d = drawings[idx]
        print(f"Drawing {idx}: rect={d['rect']}, fill={d.get('fill')}")
        for item in d["items"]:
            print(f"  item: {item}")

if __name__ == "__main__":
    main()
