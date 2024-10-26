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

# import fitz
# from PIL import Image
# import pytesseract
# import cv2
# import numpy as np

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

# def extract_text_from_pdf(pdf_path, x, y, width, height, page_number=0):
#     """Extracts text from a specified area in a PDF using OCR."""
#     pdf_document = fitz.open(pdf_path)
#     page = pdf_document.load_page(page_number)
#     rect = fitz.Rect(x, y, x + width, y + height)
#     pix = page.get_pixmap(clip=rect)
#     img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

#     img.save("original_cropped_image.png")
#     img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

#     # --- Enhanced Preprocessing ---
#     upscale_factor = 4
#     height, width = img.shape[:2]
#     upscale_dim = (width * upscale_factor, height * upscale_factor)
#     upscaled = cv2.resize(img, upscale_dim, interpolation=cv2.INTER_CUBIC)

#     gray = cv2.cvtColor(upscaled, cv2.COLOR_BGR2GRAY)

#     # 1. Gaussian Blur for Noise Reduction:
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0) 

#     # 2. Adaptive Thresholding:
#     thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                    cv2.THRESH_BINARY, 11, 2)  

#     # 3. Morphological Operations (optional, if needed):
#     kernel = np.ones((3,3), np.uint8) 
#     thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1) 

#     cv2.imwrite("upscaled_cropped_image.png", thresh)
#     text = pytesseract.image_to_string(thresh, config='--psm 6') 

#     print(f"Coordinates used: x={x}, y={y}, width={width}, height={height}")
#     return text

# # Example usage 
# pdf_path = r'C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\p2.pdf'
# x, y, width, height = 415, 122, 127, 25 
# extracted_text = extract_text_from_pdf(pdf_path, x, y, width, height)
# print("Extracted Text:", extracted_text) 

#------------------------------------- v3 --------------------------------

# import fitz
# from PIL import Image
# import pytesseract
# import cv2
# import numpy as np

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# def extract_text_from_zoomed_pdf_region(pdf_path, x, y, width, height, zoom_factor=2, page_number=0):
#     """
#     Zooms into a PDF region, extracts the image, and performs OCR.
#     """
#     pdf_document = fitz.open(pdf_path)
#     page = pdf_document.load_page(page_number)
#     rect = fitz.Rect(x, y, x + width, y + height)

#     # Zoom into the region
#     mat = fitz.Matrix(zoom_factor, zoom_factor)
#     pix = page.get_pixmap(matrix=mat, clip=rect)
#     img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

#     # Preprocess the zoomed image
#     img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#     thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                    cv2.THRESH_BINARY, 11, 2)
#     kernel = np.ones((3, 3), np.uint8)
#     thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

#     cv2.imwrite("zoomed_processed_image.png", thresh) # Save for inspection

#     # Perform OCR
#     text = pytesseract.image_to_string(thresh, config='--psm 6')

#     print(f"Coordinates used: x={x}, y={y}, width={width}, height={height}")
#     return text

# # Example usage
# pdf_path = r'C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\p2.pdf'
# x, y, width, height = 412, 122, 127, 28
# zoom_factor = 4  # Adjust zoom as needed

# extracted_text = extract_text_from_zoomed_pdf_region(pdf_path, x, y, width, height, zoom_factor)
# print("Extracted Text:", extracted_text)


# ------------ V5 with Multiple pdf and regex ---------------------
# import fitz
# from PIL import Image
# import pytesseract
# import cv2
# import numpy as np
# import re

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# def extract_text_from_zoomed_pdf_region(pdf_path, x, y, width, height, zoom_factor=2, page_number=0):
#     """
#     Zooms into a PDF region, extracts the image, and performs OCR.
#     """
#     pdf_document = fitz.open(pdf_path)
#     page = pdf_document.load_page(page_number)  # Load the specific page
#     rect = fitz.Rect(x, y, x + width, y + height)

#     mat = fitz.Matrix(zoom_factor, zoom_factor)
#     pix = page.get_pixmap(matrix=mat, clip=rect)
#     img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

#     img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#     thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                    cv2.THRESH_BINARY, 11, 2)
#     kernel = np.ones((3, 3), np.uint8)
#     thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)


#     text = pytesseract.image_to_string(thresh, config='--psm 6')

#     return text

# def check_regex(text, pattern=r"[A-Z]{3}/[A-Z]{2}\s?\d{4}/[A-Z]{2}/\d{7}"):
#     match = re.match(pattern, text)
#     return bool(match)


# def process_pdf(pdf_path, x, y, width, height, zoom_factor=4):
#     """Processes all pages of a PDF."""
#     all_extracted_text = []
#     pdf_document = fitz.open(pdf_path)
#     for page_number in range(pdf_document.page_count):
#         extracted_text = extract_text_from_zoomed_pdf_region(
#             pdf_path, x, y, width, height, zoom_factor, page_number
#         )
#         if check_regex(extracted_text.replace(" ", "")):  # Remove spaces and validate
#             all_extracted_text.append(extracted_text)
#         else:
#             print(f"Regex validation failed on page {page_number + 1}. Extracted Text: {extracted_text}")
#     return all_extracted_text


# # Example usage
# pdf_path = r'C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\.pdf'  # Your multi-page PDF
# x, y, width, height = 412, 122, 127, 28  # Coordinates
# zoom_factor = 4

# all_text = process_pdf(pdf_path, x, y, width, height, zoom_factor)

# for i, text in enumerate(all_text):
#     print(f"Page {i+1}: {text}")

# import fitz
# from PIL import Image
# import pytesseract
# import cv2
# import numpy as np
# import re
# import os

# # Configure Tesseract path (IMPORTANT: Set your path here)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  

# def extract_text_from_zoomed_pdf_region(pdf_path, x, y, width, height, zoom_factor=2, page_number=0):
#     """Zooms into a PDF region, extracts the image, and performs OCR."""
#     pdf_document = fitz.open(pdf_path)
#     page = pdf_document.load_page(page_number)
#     rect = fitz.Rect(x, y, x + width, y + height)

#     mat = fitz.Matrix(zoom_factor, zoom_factor)
#     pix = page.get_pixmap(matrix=mat, clip=rect)
#     img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

#     img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#     thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
#     kernel = np.ones((3, 3), np.uint8)
#     thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

#     text = pytesseract.image_to_string(thresh, config='--psm 6')
#     return text

# def check_regex(text, pattern=r"[A-Z]{3}/[A-Z]{2}\s?\d{4}/[A-Z]{2}/\d{7}"):
#     """Checks if the extracted text matches the regex pattern."""
#     match = re.match(pattern, text)
#     return bool(match)

# def process_pdf(pdf_path, x, y, width, height, zoom_factor=4, output_file="extracted_text.txt"):
#     """Processes all pages of a PDF and writes extracted text to a file."""
#     output_filepath = os.path.join(os.path.dirname(pdf_path), output_file)
#     with open(output_filepath, "w", encoding="utf-8") as outfile:
#         pdf_document = fitz.open(pdf_path)
#         for page_number in range(pdf_document.page_count):
#             extracted_text = extract_text_from_zoomed_pdf_region(
#                 pdf_path, x, y, width, height, zoom_factor, page_number
#             )
#             if check_regex(extracted_text.replace(" ", "")):
#                 outfile.write(f"Page {page_number + 1}:\n{extracted_text.strip()}\n\n")
#             else:
#                outfile.write(f"Page {page_number+1}: Regex validation failed. Extracted Text: {extracted_text}\n\n")

# # Example usage:
# pdf_path = r'C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\Input\DM-30701-30800.pdf'  # Replace with your PDF path
# x, y, width, height = 412, 122, 127, 28  # Adjust coordinates as needed
# zoom_factor = 4
# output_filename = "all_extracted_text.txt"  # Set the desired output filename

# process_pdf(pdf_path, x, y, width, height, zoom_factor, output_filename)

# print(f"Extracted text saved to '{output_filename}'")

# ------------------------------- v6 with multiline regex ---------------------------


# import fitz
# from PIL import Image
# import pytesseract
# import cv2
# import numpy as np
# import re
# import os

# # Configure Tesseract path (IMPORTANT: Set your path here)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# def extract_text_from_zoomed_pdf_region(pdf_path, x, y, width, height, zoom_factor=2, page_number=0):
#     """Zooms into a PDF region, extracts the image, and performs OCR."""
#     pdf_document = fitz.open(pdf_path)
#     page = pdf_document.load_page(page_number)
#     rect = fitz.Rect(x, y, x + width, y + height)

#     mat = fitz.Matrix(zoom_factor, zoom_factor)
#     pix = page.get_pixmap(matrix=mat, clip=rect)
#     img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

#     img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#     thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
#     kernel = np.ones((3, 3), np.uint8)
#     thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

#     text = pytesseract.image_to_string(thresh, config='--psm 6')
#     return text

# def check_regex_in_multiline_string(text, pattern=r"[A-Z]{3}/[A-Z]{2}\s?\d{4}/[A-Z]{2}/\d{7}"):
#     """Checks if a regex pattern exists anywhere within a multiline string."""
#     match = re.search(pattern, text, re.MULTILINE)
#     return bool(match), match.group(0) if match else None

# def process_pdf(pdf_path, x, y, width, height, zoom_factor=4, output_file="extracted_text.txt"):
#     """Processes all pages of a PDF and writes extracted text to a file."""
#     output_filepath = os.path.join(os.path.dirname(pdf_path), output_file)
#     with open(output_filepath, "w", encoding="utf-8") as outfile:
#         pdf_document = fitz.open(pdf_path)
#         for page_number in range(pdf_document.page_count):
#             extracted_text = extract_text_from_zoomed_pdf_region(
#                 pdf_path, x, y, width, height, zoom_factor, page_number
#             )

#             is_match, matched_text = check_regex_in_multiline_string(extracted_text)

#             if is_match:
#                 outfile.write(f"Validation matched on Page {page_number + 1}:\n{matched_text.strip()}\n\n")
#             else:
#                 outfile.write(f"Page {page_number+1}: Regex validation failed. Extracted Text: {extracted_text}\n\n")

# # Example usage:
# pdf_path = r'C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\Input\DM-30701-30800.pdf'
# x, y, width, height = 412, 122, 127, 28  # Example: adjust for your PDF
# zoom_factor = 4
# output_filename = "all_extracted_text.txt"

# process_pdf(pdf_path, x, y, width, height, zoom_factor, output_filename)

# print(f"Extracted text saved to '{output_filename}'")

# ------------------- # v7 ------------------------

import fitz
from PIL import Image
import pytesseract
import cv2
import numpy as np
import re
import os

# Configure Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_zoomed_pdf_region(pdf_path, x, y, width, height, zoom_factor=2, page_number=0):
    """Zooms into a PDF region, extracts image, and performs OCR."""
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(page_number)
    rect = fitz.Rect(x, y, x + width, y + height)

    mat = fitz.Matrix(zoom_factor, zoom_factor)
    pix = page.get_pixmap(matrix=mat, clip=rect)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

    text = pytesseract.image_to_string(thresh, config='--psm 6')
    return text

def check_regex_in_multiline_string(text, pattern=r"[A-Z]{3}/[A-Z]{2}\s?\d{4}/[A-Z]{2}/\d{7}"):
    """Checks if regex exists in a multiline string; returns match and text."""
    match = re.search(pattern, text, re.MULTILINE)
    return bool(match), match.group(0) if match else None

def process_pdf(pdf_path, x, y, width, height, zoom_factor=4, output_dir="output"):
    """Processes PDF, extracts/validates text, creates separate PDFs by company code."""
    os.makedirs(output_dir, exist_ok=True)
    pdf_document = fitz.open(pdf_path)
    new_pdf = None
    current_company_code = None

    for page_number in range(pdf_document.page_count):
        extracted_text = extract_text_from_zoomed_pdf_region(pdf_path, x, y, width, height, zoom_factor, page_number)
        is_match, matched_text = check_regex_in_multiline_string(extracted_text)


        if is_match:
            company_code = matched_text.split('/')[0]
            if company_code != current_company_code:
                if new_pdf:
                    new_pdf_path = os.path.join(output_dir, f"{current_company_code}.pdf")
                    new_pdf.save(new_pdf_path) #Save with .pdf extension
                    new_pdf.close()
                new_pdf = fitz.open()
                current_company_code = company_code
            new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)

        elif new_pdf: #Handles pages without company code in between matched ones.
            new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number) #Add page to current PDF

    if new_pdf: # Save the last PDF after processing all pages
        new_pdf.save(os.path.join(output_dir, f"{current_company_code}.pdf"))
        new_pdf.close()



# Example usage (adjust path, coordinates, etc.):
pdf_path = r"C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\Input\DM-30701-30800.pdf"  
x, y, width, height = 412, 122, 127, 28 
zoom_factor = 4
process_pdf(pdf_path, x, y, width, height, zoom_factor)
print("PDFs created in the 'output' directory.")