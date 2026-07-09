import weasyprint

def test():
    html_content = "<html><body><h1>Hello WeasyPrint!</h1></body></html>"
    print("Compiling test HTML...")
    try:
        weasyprint.HTML(string=html_content).write_pdf("test_weasy.pdf")
        print("Success! test_weasy.pdf generated.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test()
