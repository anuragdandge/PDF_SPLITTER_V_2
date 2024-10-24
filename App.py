# import fitz  # PyMuPDF
# from PIL import Image
# import pytesseract

# def extract_text_from_pdf(pdf_path, x, y, width, height, page_number=0):
#     # Open the PDF file
#     pdf_document = fitz.open(pdf_path)

#     # Select the specified page
#     page = pdf_document.load_page(page_number)

#     # Define the rect area to extract (x, y, width, height)
#     rect = fitz.Rect(x, y, x + width, y + height)

#     # Extract the image of the specified area
#     pix = page.get_pixmap(clip=rect)
#     img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

#     # Use pytesseract to extract text from the image
#     text = pytesseract.image_to_string(img)

#     return text

# # Example usage
# pdf_path = r'C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\DM-30901-31000.pdf'
# x, y, width, height = 100, 150, 200, 50  # Specify coordinates and dimensions
# extracted_text = extract_text_from_pdf(pdf_path, x, y, width, height)
# print("Extracted Text:", extracted_text)

#------------------------------------v2------------------------------------
# import fitz  # PyMuPDF
# from PIL import Image
# import pytesseract

# # Configure Tesseract path (IMPORTANT: Change this!)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Replace with your Tesseract path

# def extract_text_from_pdf(pdf_path, x, y, width, height, page_number=0):
#     """
#     Extracts text from a specified rectangular area in a PDF using OCR.
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
#     # Open the PDF file
#     pdf_document = fitz.open(pdf_path)

#     # Select the specified page
#     page = pdf_document.load_page(page_number)

#     # Define the rect area to extract (x, y, width, height)
#     rect = fitz.Rect(x, y, x + width, y + height)

#     # Extract the image of the specified area
#     pix = page.get_pixmap(clip=rect)
#     img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

#     # Use pytesseract to extract text from the image
#     text = pytesseract.image_to_string(img)

#     return text

# pdf_path = r'C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\p1.pdf'
# x, y, width, height = 415, 120, 127, 25  # Company ID 
# extracted_text = extract_text_from_pdf(pdf_path, x, y, width, height)
# print("Extracted Text:", extracted_text)



# --------------------------------v3--------------------------------

# import fitz  # PyMuPDF
# from PIL import Image, ImageEnhance, ImageFilter
# import pytesseract

# # Configure Tesseract path (IMPORTANT: Change this!)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Replace with your Tesseract path

# def extract_text_from_pdf(pdf_path, x, y, width, height, page_number=0):
#     """
#     Extracts text from a specified rectangular area in a PDF using OCR.
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
#     # Open the PDF file
#     pdf_document = fitz.open(pdf_path)

#     # Select the specified page
#     page = pdf_document.load_page(page_number)

#     # Define the rect area to extract (x, y, width, height)
#     rect = fitz.Rect(x, y, x + width, y + height)

#     # Extract the image of the specified area
#     pix = page.get_pixmap(clip=rect)
#     img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

#     # Convert to grayscale
#     img = img.convert('L')
    
#     # Apply image enhancement filters
#     img = img.filter(ImageFilter.MedianFilter())
#     enhancer = ImageEnhance.Contrast(img)
#     img = enhancer.enhance(2)

#     # Use pytesseract to extract text from the image
#     text = pytesseract.image_to_string(img, config='--psm 6')

#     return text

# # Example usage
# pdf_path = r'C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\p1.pdf'
# x, y, width, height = 415, 120, 127, 25  # Company ID
# extracted_text = extract_text_from_pdf(pdf_path, x, y, width, height)
# print("Extracted Text:", extracted_text)

# -------------------------------------- v4 ----------------------------------


# import fitz  # PyMuPDF
# from PIL import Image, ImageEnhance, ImageFilter
# import pytesseract

# # Configure Tesseract path (IMPORTANT: Change this!)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Replace with your Tesseract path

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
#     # Open the PDF file
#     pdf_document = fitz.open(pdf_path)

#     # Select the specified page
#     page = pdf_document.load_page(page_number)

#     # Define the rect area to extract (x, y, width, height)
#     rect = fitz.Rect(x, y, x + width, y + height)

#     # Extract the image of the specified area
#     pix = page.get_pixmap(clip=rect)
#     img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
#     # Save the original cropped image
#     original_img_path = "original_cropped_image.png"
#     img.save(original_img_path)
    
#     # Convert to grayscale
#     img = img.convert('L')
    
#     # Apply image enhancement filters
#     img = img.filter(ImageFilter.MedianFilter())
#     enhancer = ImageEnhance.Contrast(img)
#     img = enhancer.enhance(2)

#     # Save the processed cropped image
#     processed_img_path = "processed_cropped_image.png"
#     img.save(processed_img_path)

#     # Use pytesseract to extract text from the image
#     text = pytesseract.image_to_string(img, config='--psm 6')
    
#     # Print the coordinates used for cropping
#     print(f"Coordinates used: x={x}, y={y}, width={width}, height={height}")

#     return text

# # Example usage
# pdf_path = r'C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\p1.pdf'
# x, y, width, height = 415, 120, 127, 25  # Company ID
# extracted_text = extract_text_from_pdf(pdf_path, x, y, width, height)
# print("Extracted Text:", extracted_text)



# -----------------------------v5 ------------------------------------------
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import cv2
import numpy as np

# Configure Tesseract path (IMPORTANT: Change this!)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Replace with your Tesseract path

def extract_text_from_pdf(pdf_path, x, y, width, height, page_number=0):
    """
    Extracts text from a specified rectangular area in a PDF using OCR and saves images.
    Args:
        pdf_path: Path to the PDF file.
        x: The x-coordinate of the top-left corner of the area.
        y: The y-coordinate of the top-left corner of the area.
        width: The width of the area.
        height: The height of the area.
        page_number: The page number to extract text from (0-indexed).
    Returns:
        Extracted text as a string.
    """
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Select the specified page
    page = pdf_document.load_page(page_number)

    # Define the rect area to extract (x, y, width, height)
    rect = fitz.Rect(x, y, x + width, y + height)

    # Extract the image of the specified area
    pix = page.get_pixmap(clip=rect)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    # Save the original cropped image
    original_img_path = "original_cropped_image.png"
    img.save(original_img_path)
    
    # Convert to OpenCV format
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply GaussianBlur to reduce noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply thresholding to get a binary image
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Upscale the image
    upscale_factor = 2
    height, width = binary.shape[:2]
    upscale_dim = (width * upscale_factor, height * upscale_factor)
    upscaled = cv2.resize(binary, upscale_dim, interpolation=cv2.INTER_LINEAR)
    
    # Save the processed cropped image
    processed_img_path = "processed_cropped_image.png"
    cv2.imwrite(processed_img_path, upscaled)
    
    # Use pytesseract to extract text from the upscaled image
    text = pytesseract.image_to_string(upscaled, config='--psm 6')
    
    # Print the coordinates used for cropping
    print(f"Coordinates used: x={x}, y={y}, width={width}, height={height}")

    return text

# Example usage
pdf_path = r'C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\p1.pdf'
x, y, width, height = 415, 120, 127, 25  # Company ID
extracted_text = extract_text_from_pdf(pdf_path, x, y, width, height)
print("Extracted Text:", extracted_text)
