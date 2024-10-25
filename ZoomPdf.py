import fitz  # PyMuPDF
from PIL import Image

def extract_zoomed_image_from_pdf(pdf_path, x, y, width, height, zoom_factor=2, page_number=0):
    """
    Zooms into a specific rectangular area in a PDF and extracts the image of that area.
    Args:
        pdf_path: Path to the PDF file.
        x: The x-coordinate of the top-left corner of the area.
        y: The y-coordinate of the top-left corner of the area.
        width: The width of the area.
        height: The height of the area.
        zoom_factor: The factor by which to zoom into the specified area.
        page_number: The page number to extract the image from (0-indexed).
    Returns:
        The extracted image of the specified area.
    """
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Select the specified page
    page = pdf_document.load_page(page_number)

    # Define the rect area to extract (x, y, width, height)
    rect = fitz.Rect(x, y, x + width, y + height)

    # Zoom into the specified area
    mat = fitz.Matrix(zoom_factor, zoom_factor)
    pix = page.get_pixmap(matrix=mat, clip=rect)

    # Convert the image to PIL format and save
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    zoomed_image_path = "zoomed_cropped_image.png"
    img.save(zoomed_image_path)

    return img

# Example usage
# pdf_path = r'C:\Users\YourUsername\Path\To\YourPDF.pdf'
# x, y, width, height = 100, 150, 200, 50  # Example coordinates and dimensions
pdf_path = r'C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\p2.pdf'
x, y, width, height = 415, 122, 127, 25 
zoom_factor = 2  # Adjust the zoom factor as needed
extracted_image = extract_zoomed_image_from_pdf(pdf_path, x, y, width, height, zoom_factor)
extracted_image.show()  # This will display the image
