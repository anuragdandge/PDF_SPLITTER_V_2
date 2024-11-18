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

def extract_text_from_region(pdf_path, coords, page_number, zoom_factor):
    """Extracts text from a zoomed PDF region."""
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(page_number)
    x, y, width, height = coords
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
    return pytesseract.image_to_string(thresh, config='--psm 6')

def check_regex(text, pattern=r"[A-Z]{3}/[A-Z]{2}\s?\d{4}/[A-Z]{2}/\d{7}"):
    match = re.search(pattern, text, re.MULTILINE)
    return bool(match), match.group(0) if match else None

def process_pdf(pdf_path, coordinates, zoom_factor=4, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    excel_path = os.path.join(output_dir, "pdf_processing_log.xlsx")

    try:
        df = pd.read_excel(excel_path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["PDF File", "Company Code", "Farmer Name", "Timestamp", "Status", "Error Description"])

    pdf_document = fitz.open(pdf_path)
    new_pdf = None
    current_pdf_name = None
    last_farmer_name = None

    for page_number in range(pdf_document.page_count):
        print(f"Processing page {page_number + 1} of {pdf_document.page_count}")
        matched_text = None

        for coord_set in coordinates:
            company_code_coords = coord_set["company_code"]
            farmer_name_coords = coord_set["farmer_name"]

            try:
                extracted_text = extract_text_from_region(pdf_path, company_code_coords, page_number, zoom_factor)
                is_match, matched_text = check_regex(extracted_text)

                if is_match:
                    farmer_name = extract_text_from_region(pdf_path, farmer_name_coords, page_number, zoom_factor)
                    farmer_name = farmer_name.strip()
                    break

            except Exception as e:
                print(f"Error processing coordinates: {e}")

        try:
            if matched_text:
                pdf_name = matched_text.replace(" ", "_").replace("/", "_")
                company_code = matched_text.split('/')[0]

                if pdf_name != current_pdf_name:
                    if new_pdf:
                        new_pdf_path = os.path.join(output_dir, f"{current_pdf_name}.pdf")
                        new_pdf.save(new_pdf_path)
                        new_pdf.close()

                        df = pd.concat([df, pd.DataFrame({"PDF File": pdf_path, "Company Code": current_pdf_name, "Farmer Name": last_farmer_name,
                                                          "Timestamp": datetime.now(), "Status": "Success", "Error Description": ""}, index=[0])], ignore_index=True)

                    new_pdf = fitz.open()
                    current_pdf_name = pdf_name
                    last_farmer_name = farmer_name

                new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)

            elif new_pdf:
                new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)
                last_farmer_name = farmer_name

        except Exception as e:
            df = pd.concat([df, pd.DataFrame({"PDF File": pdf_path, "Company Code": "N/A", "Farmer Name": farmer_name,
                                              "Timestamp": datetime.now(), "Status": "Error", "Error Description": str(e)}, index=[0])], ignore_index=True)
            print(f"Error processing page {page_number + 1}: {e}")

    if new_pdf:
        new_pdf_path = os.path.join(output_dir, f"{current_pdf_name}.pdf")
        new_pdf.save(new_pdf_path)
        new_pdf.close()

        df = pd.concat([df, pd.DataFrame({"PDF File": pdf_path, "Company Code": current_pdf_name, "Farmer Name": last_farmer_name,
                                          "Timestamp": datetime.now(), "Status": "Success", "Error Description": ""}, index=[0])], ignore_index=True)

    df.to_excel(excel_path, index=False)

# Example Usage (REPLACE with your PDF path and coordinates)
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
zoom_factor = 4
process_pdf(pdf_path, coordinates, zoom_factor)
print("PDFs created and logged in the 'output' directory.")