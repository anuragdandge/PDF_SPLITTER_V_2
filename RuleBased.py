import fitz  

def extract_text_with_rules(pdf_path, page_number=0):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number)

    # Example Rule 1: Get text from a specific region
    rect = fitz.Rect(415, 122, 541, 147)  # x0, y0, x1, y1
    text = page.get_text("text", clip=rect) 
    print("Text from Region 1:", text)

    # Example Rule 2: Get text based on font size
    blocks = page.get_text("blocks")
    for block in blocks:
        if block[0] == 0 and block[1] > 20 and block[3].strip(): # Text block type, font size, text content
            print(f"Large Text: {block[4].strip()}")

# Example usage:
extract_text_with_rules(r"C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\p2.pdf") 

# pdf_path = r''
# x, y, width, height = 415, 122, 127, 25 