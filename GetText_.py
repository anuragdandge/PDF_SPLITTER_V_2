# import fitz  # PyMuPDF
# from PIL import Image
# import pytesseract
# import cv2
# import numpy as np

# # Configure Tesseract path (IMPORTANT: Change this!)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# def extract_text_from_pdf(pdf_path, x, y, width, height, page_number=0):
#     """
#     Extracts text from a specified rectangular area in a PDF using OCR and saves images.
#     Args:
#         pdf_path: Path to the PDF file.
#         x: The x-coordinate of the top-left corner of the area.
#         y: The y-coordinate of the top-left corner of the area.
#         width: The width of the area.
#         height: The height of the area.
#         page_number: The page number to extract text from (0-indexed).
#     Returns:
#         Extracted text as a string.
#     """
#     pdf_document = fitz.open(pdf_path)
#     page = pdf_document.load_page(page_number)
#     rect = fitz.Rect(x, y, x + width, y + height)
#     pix = page.get_pixmap(clip=rect)
#     img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

#     img.save("original_cropped_image.png")

#     img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

#     # --- Improved Upscaling and Preprocessing ---
#     upscale_factor = 4  # Increase upscale factor
#     height, width = img.shape[:2]
#     upscale_dim = (width * upscale_factor, height * upscale_factor)
#     upscaled = cv2.resize(img, upscale_dim, interpolation=cv2.INTER_CUBIC)

#     # Apply image processing for clarity
#     gray = cv2.cvtColor(upscaled, cv2.COLOR_BGR2GRAY)
#     sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
#     sharpened = cv2.filter2D(gray, -1, sharpen_kernel)
#     thresh = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

#     cv2.imwrite("upscaled_cropped_image.png", thresh)  # Save processed image

#     text = pytesseract.image_to_string(thresh, config='--psm 6')  # OCR on processed image

#     print(f"Coordinates used: x={x}, y={y}, width={width}, height={height}")

#     return text

# # Example usage
# pdf_path = r'C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\p2.pdf'
# x, y, width, height = 422, 122, 123, 22  # Company ID
# extracted_text = extract_text_from_pdf(pdf_path, x, y, width, height)
# no_spaces_string = extracted_text.replace(" ", "")
# print("Extracted Text:", no_spaces_string) 

# ---------------------v2 ------------------------

import fitz
from PIL import Image
import pytesseract
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

def extract_text_from_pdf(pdf_path, x, y, width, height, page_number=0):
    """Extracts text from a specified area in a PDF using OCR."""
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(page_number)
    rect = fitz.Rect(x, y, x + width, y + height)
    pix = page.get_pixmap(clip=rect)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    img.save("original_cropped_image.png")
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # --- Enhanced Preprocessing ---
    upscale_factor = 4
    height, width = img.shape[:2]
    upscale_dim = (width * upscale_factor, height * upscale_factor)
    upscaled = cv2.resize(img, upscale_dim, interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(upscaled, cv2.COLOR_BGR2GRAY)

    # 1. Gaussian Blur for Noise Reduction:
    blurred = cv2.GaussianBlur(gray, (5, 5), 0) 

    # 2. Adaptive Thresholding:
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)  

    # 3. Morphological Operations (optional, if needed):
    kernel = np.ones((3,3), np.uint8) 
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1) 

    cv2.imwrite("upscaled_cropped_image.png", thresh)
    text = pytesseract.image_to_string(thresh, config='--psm 6') 

    print(f"Coordinates used: x={x}, y={y}, width={width}, height={height}")
    return text

# Example usage 
pdf_path = r'C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\p1.pdf'
x, y, width, height = 415, 122, 127, 25 
extracted_text = extract_text_from_pdf(pdf_path, x, y, width, height)
print("Extracted Text:", extracted_text) 






