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

# ------------------------------------- v3 --------------------------------

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

# import fitz
# from PIL import Image
# import pytesseract
# import cv2
# import numpy as np
# import re
# import os

# # Configure Tesseract OCR path
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# def extract_text_from_zoomed_pdf_region(pdf_path, x, y, width, height, zoom_factor=2, page_number=0):
#     """Zooms into a PDF region, extracts image, and performs OCR."""
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
#     """Checks if regex exists in a multiline string; returns match and text."""
#     match = re.search(pattern, text, re.MULTILINE)
#     return bool(match), match.group(0) if match else None

# def process_pdf(pdf_path, x, y, width, height, zoom_factor=4, output_dir="output"):
#     """Processes PDF, extracts/validates text, creates separate PDFs by company code."""
#     os.makedirs(output_dir, exist_ok=True)
#     pdf_document = fitz.open(pdf_path)
#     new_pdf = None
#     current_company_code = None

#     for page_number in range(pdf_document.page_count):
#         extracted_text = extract_text_from_zoomed_pdf_region(pdf_path, x, y, width, height, zoom_factor, page_number)
#         is_match, matched_text = check_regex_in_multiline_string(extracted_text)


#         if is_match:
#             company_code = matched_text.split('/')[0]
#             if company_code != current_company_code:
#                 if new_pdf:
#                     new_pdf_path = os.path.join(output_dir, f"{current_company_code}.pdf")
#                     new_pdf.save(new_pdf_path) #Save with .pdf extension
#                     new_pdf.close()
#                 new_pdf = fitz.open()
#                 current_company_code = company_code
#             new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)

#         elif new_pdf: #Handles pages without company code in between matched ones.
#             new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number) #Add page to current PDF

#     if new_pdf: # Save the last PDF after processing all pages
#         new_pdf.save(os.path.join(output_dir, f"{current_company_code}.pdf"))
#         new_pdf.close()


# # Example usage (adjust path, coordinates, etc.):
# pdf_path = r"C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\Input\DM-30701-30800.pdf"
# x, y, width, height = 412, 122, 127, 28
# zoom_factor = 4
# process_pdf(pdf_path, x, y, width, height, zoom_factor)
# print("PDFs created in the 'output' directory.")


# -------------------- v8 :  ---------------------
# Bellow code is extracting pdf's with the  company code
# import fitz
# from PIL import Image
# import pytesseract
# import cv2
# import numpy as np
# import re
# import os

# # Configure Tesseract OCR path (IMPORTANT: Set your path here)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# def extract_text_from_zoomed_pdf_region(pdf_path, x, y, width, height, zoom_factor=2, page_number=0):
#     """Zooms into a PDF region, extracts image, and performs OCR."""
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
#     """Checks if regex exists in a multiline string; returns match and text."""
#     match = re.search(pattern, text, re.MULTILINE)
#     return bool(match), match.group(0) if match else None

# def process_pdf(pdf_path, x, y, width, height, zoom_factor=4, output_dir="output"):
#     """Processes PDF, extracts/validates text, creates separate PDFs by company code."""
#     os.makedirs(output_dir, exist_ok=True)
#     pdf_document = fitz.open(pdf_path)
#     new_pdf = None
#     current_pdf_name = None

#     for page_number in range(pdf_document.page_count):
#         extracted_text = extract_text_from_zoomed_pdf_region(
#             pdf_path, x, y, width, height, zoom_factor, page_number
#         )
#         is_match, matched_text = check_regex_in_multiline_string(extracted_text)

#         if is_match:
#             pdf_name = matched_text.replace(" ", "_").replace("/", "_")
#             if pdf_name != current_pdf_name:
#                 if new_pdf:
#                     new_pdf_path = os.path.join(output_dir, f"{current_pdf_name}.pdf")
#                     new_pdf.save(new_pdf_path)
#                     new_pdf.close()

#                 new_pdf = fitz.open()
#                 current_pdf_name = pdf_name

#             new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)
#         elif new_pdf:  # Append to the current PDF if no match but within a section
#              new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)

#     if new_pdf:  # Save the last PDF after processing all pages
#         new_pdf.save(os.path.join(output_dir, f"{current_pdf_name}.pdf"))
#         new_pdf.close()

# # Example usage (adjust path, coordinates, zoom, etc.):
# pdf_path = r"C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\Input\DM-30701-30800.pdf"  # Replace with your PDF's path
# x, y, width, height = 412, 122, 127, 28  # Example: Adjust for your PDF
# zoom_factor = 4
# process_pdf(pdf_path, x, y, width, height, zoom_factor)
# print("PDFs created in the 'output' directory.")


# -------------------- v9 --------------------

# import fitz
# from PIL import Image
# import pytesseract
# import cv2
# import numpy as np
# import re
# import os
# import pandas as pd
# from datetime import datetime

# # Configure Tesseract OCR path (IMPORTANT: Set your path here)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# def extract_text_from_zoomed_pdf_region(pdf_path, x, y, width, height, zoom_factor, page_number):
#     """Zooms into a PDF region, extracts image, and performs OCR."""
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
#     """Checks if regex exists in a multiline string; returns match and text."""
#     match = re.search(pattern, text, re.MULTILINE)
#     return bool(match), match.group(0) if match else None

# def process_pdf(pdf_path, x, y, width, height, zoom_factor=4, output_dir="output"):
#     """Processes PDF, extracts/validates text, creates PDFs, logs to Excel."""
#     os.makedirs(output_dir, exist_ok=True)
#     excel_path = os.path.join(output_dir, "pdf_processing_log.xlsx")

#     try:
#         df = pd.read_excel(excel_path)
#     except FileNotFoundError:
#         df = pd.DataFrame(columns=["PDF File", "Company Code", "Timestamp", "Status"])

#     pdf_document = fitz.open(pdf_path)
#     new_pdf = None
#     current_pdf_name = None

#     for page_number in range(pdf_document.page_count):
#         extracted_text = extract_text_from_zoomed_pdf_region(
#             pdf_path, x, y, width, height, zoom_factor, page_number
#         )
#         print(" Company Code  " , extracted_text)
#         is_match, matched_text = check_regex_in_multiline_string(extracted_text)

#         if is_match:
#             pdf_name = matched_text.replace(" ", "_").replace("/", "_")
#             company_code = matched_text.split('/')[0]

#             if pdf_name != current_pdf_name:
#                 if new_pdf:
#                     new_pdf_path = os.path.join(output_dir, f"{current_pdf_name}.pdf")
#                     new_pdf.save(new_pdf_path)
#                     new_pdf.close()
#                     log_entry = {
#                         "PDF File": pdf_path, "Company Code": current_pdf_name,
#                         "Timestamp": datetime.now(), "Status": "Success"
#                     }
#                     df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)

#                 new_pdf = fitz.open()
#                 current_pdf_name = pdf_name

#             new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)
#         elif new_pdf:
#             new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)

#     if new_pdf: # Make sure to save the last created PDF and add log
#         new_pdf_path = os.path.join(output_dir, f"{current_pdf_name}.pdf")
#         new_pdf.save(new_pdf_path)
#         new_pdf.close()
#         log_entry = {
#             "PDF File": pdf_path, "Company Code": current_pdf_name,
#             "Timestamp": datetime.now(), "Status": "Success"
#         }
#         df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)


#     df.to_excel(excel_path, index=False)


# # Example usage (Adjust path, coordinates, zoom, etc.):
# pdf_path = r"C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\Input\DM-30701-30800.pdf"
# x, y, width, height = 412, 122, 127, 28
# zoom_factor = 4
# process_pdf(pdf_path, x, y, width, height, zoom_factor)
# print("PDFs created in the 'output' directory.")


# ---------------------- v10 --------------------------

import fitz
from PIL import Image
import pytesseract
import cv2
import numpy as np
import re
import os
import pandas as pd
from datetime import datetime

# Configure Tesseract OCR path (IMPORTANT: Set your path here)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Replace with your path

def extract_text_from_zoomed_pdf_region(pdf_path, x, y, width, height, zoom_factor, page_number):
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
    """Processes PDF, extracts/validates text, creates PDFs, logs to Excel."""
    os.makedirs(output_dir, exist_ok=True)
    excel_path = os.path.join(output_dir, "pdf_processing_log.xlsx")

    try:
        df = pd.read_excel(excel_path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["PDF File", "Company Code", "Timestamp", "Status", "Error Description"])

    pdf_document = fitz.open(pdf_path)
    new_pdf = None
    current_pdf_name = None

    for page_number in range(pdf_document.page_count):
        print(f"Processing page {page_number + 1} of {pdf_document.page_count}")
        try:
            extracted_text = extract_text_from_zoomed_pdf_region(
                pdf_path, x, y, width, height, zoom_factor, page_number
            )
            is_match, matched_text = check_regex_in_multiline_string(extracted_text)

            if is_match:
                pdf_name = matched_text.replace(" ", "_").replace("/", "_")
                company_code = matched_text.split('/')[0]

                if pdf_name != current_pdf_name:
                    if new_pdf:
                        new_pdf_path = os.path.join(output_dir, f"{current_pdf_name}.pdf")
                        new_pdf.save(new_pdf_path)
                        new_pdf.close()
                        log_entry = {
                            "PDF File": pdf_path, "Company Code": current_pdf_name,
                            "Timestamp": datetime.now(), "Status": "Success", "Error Description": ""
                        }
                        df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)

                    new_pdf = fitz.open()
                    current_pdf_name = pdf_name

                new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)
            elif new_pdf:  # Continue adding pages to the current PDF even if no match
                new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)

        except Exception as e:
            log_entry = {
                "PDF File": pdf_path, "Company Code": "N/A",
                "Timestamp": datetime.now(), "Status": "Error", "Error Description": str(e)
            }
            df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
            print(f"Error processing page {page_number + 1}: {e}")

    if new_pdf:  # Save the last PDF
        new_pdf_path = os.path.join(output_dir, f"{current_pdf_name}.pdf")
        new_pdf.save(new_pdf_path)
        new_pdf.close()
        log_entry = {
            "PDF File": pdf_path, "Company Code": current_pdf_name,
            "Timestamp": datetime.now(), "Status": "Success", "Error Description": ""
        }
        df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)

    df.to_excel(excel_path, index=False)


# Example usage (Adjust path, coordinates, zoom, etc.):
pdf_path = r"C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\Input\DM-30701-30800.pdf"  # Replace with your PDF path
# x, y, width, height = 412, 122, 127, 28  # Adjust coordinates
# x, y, width, height = 417, 120, 115, 22
# x, y, width, height = 417, 121, 114, 18
# x, y, width, height = 422, 131, 110, 20
x, y, width, height = 430, 126, 115, 23  # Adjust coordinates 
# x,430, y=126, width=115, height=23
zoom_factor = 4 # Adjust zoom
process_pdf(pdf_path, x, y, width, height, zoom_factor)
print("PDFs created in the 'output' directory.")


# -----------------------------v 11 Claude ----------------------------

# import fitz
# from PIL import Image
# import pytesseract
# import cv2
# import numpy as np
# import re
# import os
# import pandas as pd
# from datetime import datetime

# # Configure Tesseract OCR path (IMPORTANT: Set your path here)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Replace with your path

# def extract_text_from_zoomed_pdf_region(pdf_path, x, y, width, height, zoom_factor, page_number):
#     """Zooms into a PDF region, extracts image, and performs OCR."""
#     with fitz.open(pdf_path) as pdf_document:
#         page = pdf_document[page_number]
#         rect = fitz.Rect(x, y, x + width, y + height)
#         mat = fitz.Matrix(zoom_factor, zoom_factor)
#         pix = page.get_pixmap(matrix=mat, clip=rect)
#         img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

#     img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#     thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
#     kernel = np.ones((3, 3), np.uint8)
#     thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

#     text = pytesseract.image_to_string(thresh, config='--psm 6')
#     return text

# def check_regex_in_multiline_string(text, pattern=r"[A-Z]{3}/[A-Z]{2}\s?\d{4}/[A-Z]{2}/\d{7}"):
#     """Checks if regex exists in a multiline string; returns match and text."""
#     match = re.search(pattern, text, re.MULTILINE)
#     return bool(match), match.group(0) if match else None

# def process_pdf(pdf_path, x, y, width, height, zoom_factor=4, output_dir="output"):
#     """Processes PDF, extracts/validates text, creates PDFs, logs to Excel."""
#     os.makedirs(output_dir, exist_ok=True)
#     excel_path = os.path.join(output_dir, "pdf_processing_log.xlsx")
#     unprocessed_excel_path = os.path.join(output_dir, "unprocessed_pages_log.xlsx")

#     try:
#         df = pd.read_excel(excel_path)
#     except FileNotFoundError:
#         df = pd.DataFrame(columns=["PDF File", "Company Code", "Timestamp", "Status", "Error Description"])

#     try:
#         unprocessed_df = pd.read_excel(unprocessed_excel_path)
#     except FileNotFoundError:
#         unprocessed_df = pd.DataFrame(columns=["PDF File", "Page Number", "Timestamp", "Error Description"])

#     with fitz.open(pdf_path) as pdf_document:
#         new_pdf = None
#         current_pdf_name = None
#         unprocessed_pages = []

#         for page_number in range(pdf_document.page_count):
#             print(f"Processing page {page_number + 1} of {pdf_document.page_count}")
#             try:
#                 extracted_text = extract_text_from_zoomed_pdf_region(
#                     pdf_path, x, y, width, height, zoom_factor, page_number
#                 )
#                 is_match, matched_text = check_regex_in_multiline_string(extracted_text)

#                 if is_match:
#                     pdf_name = matched_text.replace(" ", "_").replace("/", "_")
#                     company_code = matched_text.split('/')[0]

#                     if pdf_name != current_pdf_name:
#                         if new_pdf:
#                             new_pdf_path = os.path.join(output_dir, f"{current_pdf_name}.pdf")
#                             new_pdf.save(new_pdf_path)
#                         new_pdf = fitz.open()
#                         current_pdf_name = pdf_name

#                     new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)
#                 elif new_pdf:  # Continue adding pages to the current PDF even if no match
#                     new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)
#                 else:
#                     unprocessed_pages.append(page_number)

#             except Exception as e:
#                 log_entry = {
#                     "PDF File": pdf_path, "Company Code": "N/A",
#                     "Timestamp": datetime.now(), "Status": "Error", "Error Description": str(e)
#                 }
#                 df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
#                 unprocessed_pages.append(page_number)
#                 print(f"Error processing page {page_number + 1}: {e}")

#         if new_pdf:  # Save the last PDF
#             new_pdf_path = os.path.join(output_dir, f"{current_pdf_name}.pdf")
#             new_pdf.save(new_pdf_path)

#     df.to_excel(excel_path, index=False)

#     if unprocessed_pages:
#         unprocessed_pdf_path = os.path.join(output_dir, "unprocessed_pages.pdf")
#         with fitz.open(pdf_path) as pdf_document, fitz.open(unprocessed_pdf_path, "w") as unprocessed_pdf:
#             for page_number in unprocessed_pages:
#                 unprocessed_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)

#         unprocessed_log_entry = {
#             "PDF File": pdf_path, "Page Number": unprocessed_pages,
#             "Timestamp": datetime.now(), "Error Description": "Page(s) not processed"
#         }
#         unprocessed_df = pd.concat([unprocessed_df, pd.DataFrame([unprocessed_log_entry])], ignore_index=True)
#         unprocessed_df.to_excel(unprocessed_excel_path, index=False)

#     print("PDFs created in the 'output' directory.")

# # Example usage (Adjust path, coordinates, zoom, etc.):
# pdf_path = r"C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\Input\DM-30701-30800.pdf"  # Replace with your PDF path
# x, y, width, height = 412, 122, 127, 28  # Adjust coordinates
# zoom_factor = 4  # Adjust zoom
# process_pdf(pdf_path, x, y, width, height, zoom_factor)


# ---------------------------------------------- v12 with box expansion technique  -------------------------------------------


# import fitz
# from PIL import Image
# import pytesseract
# import cv2
# import numpy as np
# import re
# import os
# import pandas as pd
# from datetime import datetime

# # Configure Tesseract OCR path (IMPORTANT: Set your path here)
# # Replace with your path
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# # Added expansion_factor
# def extract_text_from_zoomed_pdf_region(pdf_path, x, y, width, height, zoom_factor, page_number, expansion_factor=0.05):
#     """Zooms into a PDF region, extracts image, and performs OCR, with optional bounding box expansion."""
#     pdf_document = fitz.open(pdf_path)
#     page = pdf_document.load_page(page_number)

#     # Expand the bounding box
#     x -= width * expansion_factor / 2
#     y -= height * expansion_factor / 2
#     width *= (1 + expansion_factor)
#     height *= (1 + expansion_factor)

#     rect = fitz.Rect(x, y, x + width, y + height)
#     mat = fitz.Matrix(zoom_factor, zoom_factor)
#     pix = page.get_pixmap(matrix=mat, clip=rect)
#     img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

#     img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#     thresh = cv2.adaptiveThreshold(
#         blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
#     kernel = np.ones((3, 3), np.uint8)
#     thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
#     # Use psm 6 for better block detection
#     text = pytesseract.image_to_string(thresh, config='--psm 6')

#     return text


# def check_regex_in_multiline_string(text, pattern=r"[A-Z]{3}/[A-Z]{2}\s?\d{4}/[A-Z]{2}/\d{7}"):
#     match = re.search(pattern, text, re.MULTILINE)
#     return bool(match), match.group(0) if match else None


# def process_pdf(pdf_path, x, y, width, height, zoom_factor=4, output_dir="output", expansion_factor=0.05):  # Added expansion_factor
#     """Processes PDF, extracts/validates text, creates PDFs, logs to Excel."""
#     os.makedirs(output_dir, exist_ok=True)
#     excel_path = os.path.join(output_dir, "pdf_processing_log.xlsx")
#     unprocessed_excel_path = os.path.join(
#         output_dir, "unprocessed_pages_log.xlsx")

#     try:
#         df = pd.read_excel(excel_path)
#     except FileNotFoundError:
#         df = pd.DataFrame(
#             columns=["PDF File", "Company Code", "Timestamp", "Status", "Error Description"])

#     try:
#         unprocessed_df = pd.read_excel(unprocessed_excel_path)
#     except FileNotFoundError:
#         unprocessed_df = pd.DataFrame(
#             columns=["PDF File", "Page Number", "Timestamp", "Error Description"])

#     with fitz.open(pdf_path) as pdf_document:
#         new_pdf = None
#         current_pdf_name = None
#         unprocessed_pages = []

#         for page_number in range(pdf_document.page_count):
#             print(
#                 f"Processing page {page_number + 1} of {pdf_document.page_count}")
#             try:
#                 extracted_text = extract_text_from_zoomed_pdf_region(
#                     pdf_path, x, y, width, height, zoom_factor, page_number, expansion_factor
#                 )
#                 is_match, matched_text = check_regex_in_multiline_string(
#                     extracted_text)

#                 if is_match:
#                     pdf_name = matched_text.replace(" ", "_").replace("/", "_")
#                     company_code = matched_text.split('/')[0]

#                     if pdf_name != current_pdf_name:
#                         if new_pdf:
#                             new_pdf_path = os.path.join(
#                                 output_dir, f"{current_pdf_name}.pdf")
#                             new_pdf.save(new_pdf_path)
#                         new_pdf = fitz.open()
#                         current_pdf_name = pdf_name

#                     new_pdf.insert_pdf(
#                         pdf_document, from_page=page_number, to_page=page_number)
#                 elif new_pdf:  # Continue adding pages to the current PDF even if no match
#                     new_pdf.insert_pdf(
#                         pdf_document, from_page=page_number, to_page=page_number)
#                 else:
#                     unprocessed_pages.append(page_number)

#             except Exception as e:
#                 log_entry = {
#                     "PDF File": pdf_path, "Company Code": "N/A",
#                     "Timestamp": datetime.now(), "Status": "Error", "Error Description": str(e)
#                 }
#                 df = pd.concat([df, pd.DataFrame([log_entry])],
#                                ignore_index=True)
#                 unprocessed_pages.append(page_number)
#                 print(f"Error processing page {page_number + 1}: {e}")

#         if new_pdf:  # Save the last PDF
#             new_pdf_path = os.path.join(output_dir, f"{current_pdf_name}.pdf")
#             new_pdf.save(new_pdf_path)

#     df.to_excel(excel_path, index=False)

#     if unprocessed_pages:
#         unprocessed_pdf_path = os.path.join(
#             output_dir, "unprocessed_pages.pdf")
#         with fitz.open(pdf_path) as pdf_document, fitz.open(unprocessed_pdf_path, "w") as unprocessed_pdf:
#             for page_number in unprocessed_pages:
#                 unprocessed_pdf.insert_pdf(
#                     pdf_document, from_page=page_number, to_page=page_number)

#         unprocessed_log_entry = {
#             "PDF File": pdf_path, "Page Number": unprocessed_pages,
#             "Timestamp": datetime.now(), "Error Description": "Page(s) not processed"
#         }
#         unprocessed_df = pd.concat([unprocessed_df, pd.DataFrame(
#             [unprocessed_log_entry])], ignore_index=True)
#         unprocessed_df.to_excel(unprocessed_excel_path, index=False)

#     print("PDFs created in the 'output' directory.")


# # Example usage
# pdf_path = r"C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\Input\DM-30701-30800.pdf"
# x, y, width, height = 430, 126, 115, 23 # for cross 
# # x, y, width, height = 417, 121, 114, 18
# # x, y, width, height = 422, 131, 110, 20
# # x, y, width, height = 417, 120, 115, 22
# # Coordinates: x=417.0, y=120.0, width=115.0, height=22.0
# # Coordinates: x=422.0, y=131.0, width=110.0, height=20.0
# # Coordinates: x=417.0, y=121.0, width=114.0, height=18.0
# zoom_factor = 4
# expansion_factor = 0.1  # Example: 10% expansion. Adjust as needed.
# process_pdf(pdf_path, x, y, width, height, zoom_factor,
#             expansion_factor=expansion_factor)  # Pass expansion_factor
# print("PDFs created in the 'output' directory.")
