# import fitz
# from PIL import Image
# import pytesseract
# import cv2
# import numpy as np
# import re
# import os
# import pandas as pd
# from datetime import datetime

# # Configure Tesseract OCR path
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Replace with your path

# # Constants and settings
# OUTPUT_DIR = "output"
# EXCEL_FILE = "pdf_processing_log.xlsx"
# COMPANY_CODE_PATTERN = r"[A-Z]{3}/[A-Z]{2}\s?\d{4}/[A-Z]{2}/\d{7}"

# def extract_image_from_pdf(pdf_path, page_number, x, y, width, height, zoom_factor, expansion_factor=0.05):
#     """Extracts and preprocesses an image from a specific PDF region."""
#     try:
#         pdf_document = fitz.open(pdf_path)
#         page = pdf_document.load_page(page_number)

#         # Expand bounding box
#         x -= width * expansion_factor / 2
#         y -= height * expansion_factor / 2
#         width *= (1 + expansion_factor)
#         height *= (1 + expansion_factor)

#         rect = fitz.Rect(x, y, x + width, y + height)
#         mat = fitz.Matrix(zoom_factor, zoom_factor)
#         pix = page.get_pixmap(matrix=mat, clip=rect)
#         img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#         img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)  # No need for np.asarray

#         # Image preprocessing (could be a separate function if more complex)
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#         thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
#         kernel = np.ones((3, 3), np.uint8)
#         thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
#         return thresh
#     except Exception as e:
#         print(f"Error extracting image from page {page_number + 1}: {e}")
#         return None  # Return None to indicate failure


# def perform_ocr(image):
#     """Performs OCR on a given image."""
#     if image is None:  # Handle the case where image extraction failed
#         return ""

#     try:
#         text = pytesseract.image_to_string(image, config='--psm 6')
#         return text
#     except Exception as e:
#         print(f"OCR Error: {e}")
#         return ""


# def extract_company_code(text):
#     """Extracts the company code using regex."""
#     match = re.search(COMPANY_CODE_PATTERN, text, re.MULTILINE)
#     return match.group(0) if match else None


# def create_pdf(pdf_document, company_code, output_dir):
#     """Creates a new PDF for the given company code."""
#     pdf_name = company_code.replace(" ", "_").replace("/", "_")
#     pdf_path = os.path.join(output_dir, f"{pdf_name}.pdf")
#     new_pdf = fitz.open()
#     new_pdf.insert_pdf(pdf_document)  # Insert all pages of the current document
#     new_pdf.save(pdf_path)
#     new_pdf.close()


# def process_page(pdf_path, page_number, x, y, width, height, zoom_factor, expansion_factor, df):
#      """Processes a single page of the PDF."""
#      image = extract_image_from_pdf(pdf_path, page_number, x, y, width, height, zoom_factor, expansion_factor)
#      text = perform_ocr(image)
#      company_code = extract_company_code(text)

#      if company_code:
#          try:
#              pdf_document = fitz.open(pdf_path) # Open PDF here to avoid repeated opening
#              create_pdf(pdf_document, company_code, OUTPUT_DIR)
#              pdf_document.close() # Close after use

#              log_entry = {
#                  "PDF File": pdf_path,
#                  "Company Code": company_code,
#                  "Timestamp": datetime.now(),
#                  "Status": "Success",
#                  "Error Description": ""
#              }


#          except Exception as e:
#              log_entry = create_log_entry(pdf_path, "N/A", "Error", str(e))
#              print(f"Error creating PDF for page {page_number + 1}: {e}")

#      else:
#           log_entry = create_log_entry(pdf_path, "N/A", "No Match", "") # Log if no match is found
#      return pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True) # Return updated DataFrame


# def create_log_entry(pdf_path, company_code, status, error):

#     """Creates a log entry for the Excel file."""

#     return {
#          "PDF File": pdf_path,
#          "Company Code": company_code,
#          "Timestamp": datetime.now(),
#          "Status": status,
#          "Error Description": error
#      }


# def process_pdf(pdf_path, x, y, width, height, zoom_factor=4, expansion_factor=0.05):
#     """Main function to process the entire PDF."""
#     os.makedirs(OUTPUT_DIR, exist_ok=True)
#     excel_path = os.path.join(OUTPUT_DIR, EXCEL_FILE)

#     try:
#         df = pd.read_excel(excel_path)
#     except FileNotFoundError:
#         df = pd.DataFrame(columns=["PDF File", "Company Code", "Timestamp", "Status", "Error Description"])

#     pdf_document = fitz.open(pdf_path)


#     for page_number in range(pdf_document.page_count):
#         print(f"Processing page {page_number + 1} of {pdf_document.page_count}")
#         df = process_page(pdf_path, page_number, x, y, width, height, zoom_factor, expansion_factor, df)
#     pdf_document.close()


#     df.to_excel(excel_path, index=False)  # Save the log outside the loop


# pdf_path = r"C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\Input\DM-30701-30800.pdf"
# # x, y, width, height = 430, 126, 115, 23 # for cross
# # x, y, width, height = 417, 121, 114, 18
# # x, y, width, height = 422, 131, 110, 20
# x, y, width, height = 417, 120, 115, 22
# # Coordinates: x=417.0, y=120.0, width=115.0, height=22.0
# # Coordinates: x=422.0, y=131.0, width=110.0, height=20.0
# # Coordinates: x=417.0, y=121.0, width=114.0, height=18.0
# zoom_factor = 4
# expansion_factor = 0.1  # Example: 10% expansion. Adjust as needed.
# process_pdf(pdf_path, x, y, width, height, zoom_factor,
#             expansion_factor=expansion_factor)  # Pass expansion_factor
# print("PDFs created in the 'output' directory.")


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


# -------------------------------------- Modularized with multi coordinates ---------------------

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

# def process_pdf(pdf_path, coordinates_list, zoom_factor=4, output_dir="output"):
#     """Processes PDF, extracts/validates text, creates PDFs, logs to Excel."""
#     os.makedirs(output_dir, exist_ok=True)
#     excel_path = os.path.join(output_dir, "pdf_processing_log.xlsx")

#     try:
#         df = pd.read_excel(excel_path)
#     except FileNotFoundError:
#         df = pd.DataFrame(columns=["PDF File", "Company Code", "Timestamp", "Status", "Error Description"])

#     pdf_document = fitz.open(pdf_path)
#     new_pdf = None
#     current_pdf_name = None

#     for page_number in range(pdf_document.page_count):
#         print(f"Processing page {page_number + 1} of {pdf_document.page_count}")
#         matched_text = None  # Initialize outside the loop
#         for x, y, width, height in coordinates_list:
#             try:
#                 extracted_text = extract_text_from_zoomed_pdf_region(
#                     pdf_path, x, y, width, height, zoom_factor, page_number
#                 )
#                 is_match, matched_text = check_regex_in_multiline_string(extracted_text)
#                 if is_match:
#                     break # Exit loop if match is found
#             except Exception as e:
#                 print(f"Error processing coordinates ({x}, {y}, {width}, {height}): {e}")
#                 continue  # Try next coordinates

#         try:  # Moved try block outside coordinates loop
#              if matched_text: # Check if a match was found in any of the regions
#                 pdf_name = matched_text.replace(" ", "_").replace("/", "_")
#                 company_code = matched_text.split('/')[0]


#                 if pdf_name != current_pdf_name:
#                     if new_pdf:
#                         new_pdf_path = os.path.join(output_dir, f"{current_pdf_name}.pdf")
#                         new_pdf.save(new_pdf_path)
#                         new_pdf.close()

#                         log_entry = { # Create log entry for successful split
#                             "PDF File": pdf_path,
#                             "Company Code": current_pdf_name,
#                             "Timestamp": datetime.now(),
#                             "Status": "Success",
#                             "Error Description": ""
#                         }
#                         df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
#                     new_pdf = fitz.open()
#                     current_pdf_name = pdf_name
#                 new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)

#              elif new_pdf: # Continue to add pages even if there's no match
#                  new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)

#         except Exception as e:

#             log_entry = {  # Create a log entry for any other error
#                  "PDF File": pdf_path, "Company Code": "N/A",
#                  "Timestamp": datetime.now(), "Status": "Error", "Error Description": str(e)
#              }
#             df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)

#             print(f"Error processing page {page_number + 1}: {e}")


#     if new_pdf:  # Save the last PDF after processing all pages
#         new_pdf_path = os.path.join(output_dir, f"{current_pdf_name}.pdf")
#         new_pdf.save(new_pdf_path)
#         new_pdf.close()

#         log_entry = {
#             "PDF File": pdf_path, "Company Code": current_pdf_name,
#             "Timestamp": datetime.now(), "Status": "Success", "Error Description": ""
#         }
#         df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)

#     df.to_excel(excel_path, index=False)


# pdf_path = r"C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\Input\DM-30701-30800.pdf"
# coordinates_list = [
#     (412, 122, 127, 28),
#     (417, 120, 115, 22),
#     (417, 121, 114, 18),
#     (421, 123, 116, 24),
#     (422, 131, 110, 20),
#     (425, 124, 112, 18),
#     (426, 118, 114, 18),
#     (427, 121, 114, 21),
#     (427, 115, 114, 19),
#     (430, 126, 115, 23)
# ]
# zoom_factor = 4
# process_pdf(pdf_path, coordinates_list, zoom_factor)
# print("PDFs created in the 'output' directory.")


# -----------------------------------------------  new with farmer name also ----------------------------

# import fitz
# from PIL import Image
# import pytesseract
# import cv2
# import numpy as np
# import re
# import os
# import pandas as pd
# from datetime import datetime

# # Configure Tesseract OCR path (REQUIRED - Replace with YOUR path)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # <--- REPLACE THIS!!!

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

# def process_pdf(pdf_path, coordinates, zoom_factor=4, output_dir="output"):
#     """Processes PDF, extracts company code and farmer name, creates PDFs, logs to Excel."""
#     os.makedirs(output_dir, exist_ok=True)
#     excel_path = os.path.join(output_dir, "pdf_processing_log.xlsx")

#     try:
#         df = pd.read_excel(excel_path)
#     except FileNotFoundError:
#         df = pd.DataFrame(columns=["PDF File", "Company Code", "Farmer Name", "Timestamp", "Status", "Error Description"])

#     pdf_document = fitz.open(pdf_path)
#     new_pdf = None
#     current_pdf_name = None
#     last_farmer_name = None

#     for page_number in range(pdf_document.page_count):
#         print(f"Processing page {page_number + 1} of {pdf_document.page_count}")

#         for coord_set in coordinates:
#             company_code_coords = coord_set["company_code"]
#             farmer_name_coords = coord_set["farmer_name"]

#             matched_text = None
#             try:
#                 x, y, width, height = company_code_coords
#                 extracted_text = extract_text_from_zoomed_pdf_region(pdf_path, x, y, width, height, zoom_factor, page_number)
#                 is_match, matched_text = check_regex_in_multiline_string(extracted_text)

#                 if is_match:
#                     farmer_name = None
#                     try:
#                         x_farmer, y_farmer, width_farmer, height_farmer = farmer_name_coords
#                         farmer_name = extract_text_from_zoomed_pdf_region(
#                             pdf_path, x_farmer, y_farmer, width_farmer, height_farmer, zoom_factor, page_number
#                          )
#                         farmer_name = farmer_name.strip()
#                     except Exception as e:
#                         print(f"Error extracting Farmer Name: {e}")
#                         farmer_name = "N/A"


#                     try:
#                         if matched_text:
#                             pdf_name = matched_text.replace(" ", "_").replace("/", "_")
#                             company_code = matched_text.split('/')[0]

#                             if pdf_name != current_pdf_name:
#                                 if new_pdf:
#                                     new_pdf_path = os.path.join(output_dir, f"{current_pdf_name}.pdf")
#                                     new_pdf.save(new_pdf_path)
#                                     new_pdf.close()
#                                     log_entry = {
#                                         "PDF File": pdf_path, "Company Code": current_pdf_name, "Farmer Name": last_farmer_name,
#                                         "Timestamp": datetime.now(), "Status": "Success", "Error Description": ""
#                                     }
#                                     df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)

#                                 new_pdf = fitz.open()
#                                 current_pdf_name = pdf_name
#                                 last_farmer_name = farmer_name  # Store farmer name for logging

#                             new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)
#                         elif new_pdf:  # Add page to existing PDF even if no new company code
#                             new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)
#                             last_farmer_name = farmer_name # Update farmer name
#                     except Exception as e:
#                         log_entry = {
#                             "PDF File": pdf_path, "Company Code": "N/A","Farmer Name": farmer_name, # Include the farmer name if extracted
#                             "Timestamp": datetime.now(), "Status": "Error", "Error Description": str(e)
#                         }
#                         df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
#                         print(f"Error processing page {page_number + 1}: {e}")
#                     break #Exit the inner loop after finding a company code match

#             except Exception as e:
#                 print(f"Error processing company code coordinates: {e}")  # More informative error message


#     if new_pdf: #Save the last new_pdf
#         new_pdf_path = os.path.join(output_dir, f"{current_pdf_name}.pdf")
#         new_pdf.save(new_pdf_path)
#         new_pdf.close()
#         log_entry = {
#             "PDF File": pdf_path, "Company Code": current_pdf_name, "Farmer Name": last_farmer_name,
#             "Timestamp": datetime.now(), "Status": "Success", "Error Description": ""
#         }
#         df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)


#     df.to_excel(excel_path, index=False)


# pdf_path = r"C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\Input\DM-30701-30800.pdf"  # <--- REPLACE with your PDF path
# # coordinates_list = [
# #     (412, 122, 127, 28),
# #     (417, 120, 115, 22),
# #     (417, 121, 114, 18),
# #     (421, 123, 116, 24),
# #     (422, 131, 110, 20),
# #     (425, 124, 112, 18),
# #     (426, 118, 114, 18),
# #     (427, 121, 114, 21),
# #     (427, 115, 114, 19),
# #     (430, 126, 115, 23)
# # ]
# coordinates = [
#     {"label": "Set1", "company_code": (412, 122, 127, 28), "farmer_name": (175, 209, 112, 22)},

# ]
# zoom_factor = 4  # Adjust if needed
# process_pdf(pdf_path, coordinates, zoom_factor)
# print("PDFs created and logged in the 'output' directory.")


# ----------------- with farmar name ------------


import fitz
from PIL import Image
import pytesseract
import cv2
import numpy as np
import re
import os
import pandas as pd
from datetime import datetime


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_from_zoomed_pdf_region(pdf_path, x, y, width, height, zoom_factor, page_number):
    """Zooms into a PDF region, extracts image, and performs OCR."""
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(page_number)
    rect = fitz.Rect(x, y, x + width, y + height)

    mat = fitz.Matrix(zoom_factor, zoom_factor)
    pix = page.get_pixmap(matrix=mat, clip=rect)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Convert to BGR for OpenCV
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)       # Convert to grayscale
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)        # Apply Gaussian blur
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)  # Adaptive Thresholding
    # Define a kernel for morphology
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,
                              kernel, iterations=1)  # Morphological closing

    text = pytesseract.image_to_string(thresh, config='--psm 6')  # Perform OCR
    return text


def check_regex_in_multiline_string(text, pattern=r"[A-Z]{3}/[A-Z]{2}\s?\d{4}/[A-Z]{2}/\d{7}"):
    """Checks if regex exists in a multiline string; returns match and text."""
    match = re.search(pattern, text, re.MULTILINE)
    return bool(match), match.group(0) if match else None


def process_pdf(pdf_path, coordinates, zoom_factor=4, output_dir="output"):
    """Processes PDF, extracts company code and farmer name, creates PDFs, logs to Excel."""
    os.makedirs(
        output_dir, exist_ok=True)           # Create output directory if it doesn't exist
    # Path to the Excel log file
    excel_path = os.path.join(output_dir, "pdf_processing_log.xlsx")

    try:
        # Try to read existing log file
        df = pd.read_excel(excel_path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["PDF File", "Company Code", "Farmer Name", "Timestamp",
                          "Status", "Error Description"])  # Create new dataframe if file not exists

    pdf_document = fitz.open(pdf_path)            # Open the PDF
    new_pdf = None                              # Initialize new PDF object
    current_pdf_name = None                     # Initialize current PDF name
    # Initialize last extracted farmer name
    last_farmer_name = None

    for page_number in range(pdf_document.page_count):   # Iterate through all pages
        print(
            f"Processing page {page_number + 1} of {pdf_document.page_count}")

        matched_text = None  # Reset matched_text for each page
        for coord_set in coordinates:                   # Iterate through coordinate sets for each page
            # Get coordinates for company code
            company_code_coords = coord_set["company_code"]
            # Get coordinates for farmer name
            farmer_name_coords = coord_set["farmer_name"]

            try:
                x, y, width, height = company_code_coords    # unpack company code coordinates
                extracted_text = extract_text_from_zoomed_pdf_region(
                    pdf_path, x, y, width, height, zoom_factor, page_number)  # Extract text based on region given
                is_match, matched_text = check_regex_in_multiline_string(
                    extracted_text)  # check if text matches given regex

                if is_match:  # If a match is found for the company code
                    farmer_name = None
                    try:
                        # unpack farmer coordinates
                        x_farmer, y_farmer, width_farmer, height_farmer = farmer_name_coords
                        farmer_name = extract_text_from_zoomed_pdf_region(
                            pdf_path, x_farmer, y_farmer, width_farmer, height_farmer, zoom_factor, page_number
                        )
                        farmer_name = farmer_name.strip()  # Remove leading/trailing whitespace
                    except Exception as e:
                        print(f"Error extracting Farmer Name: {e}")
                        farmer_name = "N/A"
                    break  # Exit the *inner* loop if a company code match is found

            except Exception as e:
                # Handle exceptions during company code extraction
                print(f"Error processing company code coordinates: {e}")

        try:
            if matched_text:  # if a company code is found
                pdf_name = matched_text.replace(" ", "_").replace(
                    "/", "_")   # Create file name for split PDF
                company_code = matched_text.split(
                    '/')[0]             # Extract company code

                if pdf_name != current_pdf_name:            # Check if company code has changed
                    if new_pdf:                            # If a new PDF is being created
                        new_pdf_path = os.path.join(
                            output_dir, f"{current_pdf_name}.pdf")  # Create new pdf path
                        new_pdf.save(new_pdf_path)       # Save the split PDF
                        new_pdf.close()                 # Close the current split PDF

                        log_entry = {                    # Log information to the Excel file
                            "PDF File": pdf_path, "Company Code": current_pdf_name, "Farmer Name": last_farmer_name,
                            "Timestamp": datetime.now(), "Status": "Success", "Error Description": ""
                        }
                        # Add row to dataframe
                        df = pd.concat(
                            [df, pd.DataFrame([log_entry])], ignore_index=True)

                    new_pdf = fitz.open()              # Create new PDF object for next split PDF
                    current_pdf_name = pdf_name         # Update the current PDF name
                    last_farmer_name = farmer_name     # Store extracted farmer name

                # Add the current page to split PDF
                new_pdf.insert_pdf(
                    pdf_document, from_page=page_number, to_page=page_number)

            elif new_pdf:  # Continue adding to current split PDF even if no company code match on this page
                new_pdf.insert_pdf(
                    pdf_document, from_page=page_number, to_page=page_number)
                last_farmer_name = farmer_name  # Update last_farmer_name

        except Exception as e:
            log_entry = {                            # Log information to the Excel file if an error occurs
                # Include farmer name, even in case of error
                "PDF File": pdf_path, "Company Code": "N/A", "Farmer Name": farmer_name,
                "Timestamp": datetime.now(), "Status": "Error", "Error Description": str(e)
            }
            df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
            print(f"Error processing page {page_number + 1}: {e}")

    if new_pdf:  # Check if a PDF is still open after iterating through all pages
        new_pdf_path = os.path.join(
            output_dir, f"{current_pdf_name}.pdf")  # Construct file name
        new_pdf.save(new_pdf_path)       # Save the last new PDF
        new_pdf.close()                 # Close the last new PDF

        log_entry = {                    # Log the creation of the last PDF
            "PDF File": pdf_path, "Company Code": current_pdf_name, "Farmer Name": last_farmer_name,
            "Timestamp": datetime.now(), "Status": "Success", "Error Description": ""
        }
        df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)

    df.to_excel(excel_path, index=False)    # Save the Excel log file


# Example Usage (ADJUST THESE VALUES - Especially the coordinates)
# <--- REPLACE with your PDF path
pdf_path = r"C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\Input\DM-30701-30800.pdf"
coordinates = [
    {"label": "Set1", "company_code": (412, 122, 127, 28), "farmer_name": (175, 209, 112, 21)}, 
    {"label": "Set2", "company_code": (417, 121, 114, 18), "farmer_name": (175, 209, 112, 21)}, 
    {"label": "Set3", "company_code": (421, 123, 116, 24), "farmer_name": (171, 209, 125, 17)}, 
    {"label": "Set4", "company_code": (422, 131, 110, 20), "farmer_name": (173, 220, 125, 16)}, 
    {"label": "Set5", "company_code": (425, 124, 112, 18), "farmer_name": (173, 211, 125, 18)}, 
    {"label": "Set6", "company_code": (426, 118, 114, 18), "farmer_name": (177, 209, 127, 19)}, 
    {"label": "Set7", "company_code": (427, 121, 114, 21), "farmer_name": (176, 209, 128, 18)}, 
    {"label": "Set8", "company_code": (427, 115, 114, 19), "farmer_name": (178, 203, 128, 18)}, 
    {"label": "Set9", "company_code": (430, 126, 115, 23), "farmer_name": (179, 211, 107, 19)}, 
]
zoom_factor = 4  # Adjust if needed
process_pdf(pdf_path, coordinates, zoom_factor)
print("PDFs created and logged in the 'output' directory.")


# ----------------------------- Claude Version with farmer name logic --------------------------------

# import fitz
# from PIL import Image
# import pytesseract
# import cv2
# import numpy as np
# import re
# import os
# import pandas as pd
# from datetime import datetime
# import shutil

# # Configure Tesseract OCR path (REQUIRED - Replace with YOUR path)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# def extract_text_from_zoomed_pdf_region(pdf_path, x, y, width, height, zoom_factor, page_number):
#     """Zooms into a PDF region, extracts image, and performs OCR."""
#     pdf_document = fitz.open(pdf_path)
#     page = pdf_document.load_page(page_number)
#     rect = fitz.Rect(x, y, x + width, y + height)

#     mat = fitz.Matrix(zoom_factor, zoom_factor)
#     pix = page.get_pixmap(matrix=mat, clip=rect)
#     img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

#     # Convert to BGR for OpenCV
#     img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)       # Convert to grayscale
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)        # Apply Gaussian blur
#     thresh = cv2.adaptiveThreshold(
#         blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)  # Adaptive Thresholding
#     # Define a kernel for morphology
#     kernel = np.ones((3, 3), np.uint8)
#     thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,
#                               kernel, iterations=1)  # Morphological closing

#     text = pytesseract.image_to_string(thresh, config='--psm 6')  # Perform OCR
#     return text.strip()


# def check_regex_in_multiline_string(text, pattern=r"[A-Z]{3}/[A-Z]{2}\s?\d{4}/[A-Z]{2}/\d{7}"):
#     """Checks if regex exists in a multiline string; returns match and text."""
#     match = re.search(pattern, text, re.MULTILINE)
#     return bool(match), match.group(0) if match else None


# def process_pdf(pdf_path, coordinates, zoom_factor=4, output_dir="output"):
#     """Processes PDF, handles duplicate company codes and farmer names."""
#     os.makedirs(output_dir, exist_ok=True)
#     duplicate_dir = os.path.join(output_dir, "duplicates")
#     os.makedirs(duplicate_dir, exist_ok=True)
    
#     excel_path = os.path.join(output_dir, "pdf_processing_log.xlsx")

#     try:
#         df = pd.read_excel(excel_path)
#     except FileNotFoundError:
#         df = pd.DataFrame(columns=["PDF File", "Company Code", "Farmer Name", "Timestamp",
#                           "Status", "Error Description", "Duplicate Type"])

#     pdf_document = fitz.open(pdf_path)
    
#     # Tracking dictionaries
#     company_codes = {}
#     farmer_names = {}

#     for page_number in range(pdf_document.page_count):
#         print(f"Processing page {page_number + 1} of {pdf_document.page_count}")

#         matched_text = None
#         farmer_name = None

#         for coord_set in coordinates:
#             company_code_coords = coord_set["company_code"]
#             farmer_name_coords = coord_set["farmer_name"]

#             try:
#                 x, y, width, height = company_code_coords
#                 extracted_text = extract_text_from_zoomed_pdf_region(
#                     pdf_path, x, y, width, height, zoom_factor, page_number)
#                 is_match, matched_text = check_regex_in_multiline_string(extracted_text)

#                 if is_match:
#                     try:
#                         x_farmer, y_farmer, width_farmer, height_farmer = farmer_name_coords
#                         farmer_name = extract_text_from_zoomed_pdf_region(
#                             pdf_path, x_farmer, y_farmer, width_farmer, height_farmer, zoom_factor, page_number
#                         )
#                         farmer_name = farmer_name.strip()
#                     except Exception as e:
#                         print(f"Error extracting Farmer Name: {e}")
#                         farmer_name = "N/A"
#                     break

#             except Exception as e:
#                 print(f"Error processing company code coordinates: {e}")

#         if matched_text:
#             pdf_name = matched_text.replace(" ", "_").replace("/", "_")
#             company_code = matched_text.split('/')[0]

#             # Handle duplicate company codes
#             if company_code in company_codes:
#                 duplicate_path = os.path.join(duplicate_dir, f"{pdf_name}_duplicate.pdf")
#                 new_pdf = fitz.open()
#                 new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)
#                 new_pdf.save(duplicate_path)
#                 new_pdf.close()

#                 log_entry = {
#                     "PDF File": pdf_path,
#                     "Company Code": company_code,
#                     "Farmer Name": farmer_name,
#                     "Timestamp": datetime.now(),
#                     "Status": "Duplicate Company Code",
#                     "Error Description": "",
#                     "Duplicate Type": "Company Code"
#                 }
#                 df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
#                 continue

#             # Handle duplicate farmer names
#             if farmer_name in farmer_names and farmer_name != "N/A":
#                 # Find the existing company code for this farmer name
#                 existing_company_code = farmer_names[farmer_name]
                
#                 if existing_company_code != company_code:
#                     # Skip the first page for this company code
#                     if page_number == 0:
#                         log_entry = {
#                             "PDF File": pdf_path,
#                             "Company Code": company_code,
#                             "Farmer Name": farmer_name,
#                             "Timestamp": datetime.now(),
#                             "Status": "Skipped First Page",
#                             "Error Description": "Duplicate Farmer Name",
#                             "Duplicate Type": "Farmer Name"
#                         }
#                         df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
#                         continue

#             # Track company codes and farmer names
#             company_codes[company_code] = page_number
#             if farmer_name and farmer_name != "N/A":
#                 farmer_names[farmer_name] = company_code

#     # Save the updated log
#     df.to_excel(excel_path, index=False)
#     print("PDFs processed with duplicate handling.")


# # Example Usage (ADJUST THESE VALUES)
# pdf_path = r"C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\Input\DM-30701-30800.pdf"
# coordinates = [
#     {"label": "Set1", "company_code": (412, 122, 127, 28), "farmer_name": (175, 209, 112, 21)}, 
#     {"label": "Set2", "company_code": (417, 121, 114, 18), "farmer_name": (175, 209, 112, 21)}, 
#     {"label": "Set3", "company_code": (421, 123, 116, 24), "farmer_name": (171, 209, 125, 17)}, 
#     {"label": "Set4", "company_code": (422, 131, 110, 20), "farmer_name": (173, 220, 125, 16)}, 
#     {"label": "Set5", "company_code": (425, 124, 112, 18), "farmer_name": (173, 211, 125, 18)}, 
#     {"label": "Set6", "company_code": (426, 118, 114, 18), "farmer_name": (177, 209, 127, 19)}, 
#     {"label": "Set7", "company_code": (427, 121, 114, 21), "farmer_name": (176, 209, 128, 18)}, 
#     {"label": "Set8", "company_code": (427, 115, 114, 19), "farmer_name": (178, 203, 128, 18)}, 
#     {"label": "Set9", "company_code": (430, 126, 115, 23), "farmer_name": (179, 211, 107, 19)}, 
# ]
# zoom_factor = 4  # Adjust if needed
# process_pdf(pdf_path, coordinates, zoom_factor)
# print("PDFs created and logged in the 'output' directory.")