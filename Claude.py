import os
import shutil
import fitz
import cv2
import pytesseract
import pandas as pd
from pathlib import Path
import numpy as np
from typing import Dict, Tuple, List, Optional
import logging
import json
from dataclasses import dataclass
import argparse

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@dataclass
class Coordinates:
    """Stores coordinates for ID extraction from PDFs"""
    x1: int
    y1: int
    x2: int
    y2: int

class PDFProcessor:
    def __init__(self, config_path: str = "config.json"):
        """Initialize the PDF processor with configuration"""
        self.config = self._load_config(config_path)
        self.tracking_data = []
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            return config
        except FileNotFoundError:
            # Create default config if not found
            default_config = {
                "form_types": {
                    "type1": {
                        "identifier_text": "Form Type 1",
                        "company_id_coords": {"x1": 100, "y1": 100, "x2": 200, "y2": 150},
                        "docket_id_coords": {"x1": 300, "y1": 100, "x2": 400, "y2": 150}
                    }
                },
                "output_directory": "organized_pdfs"
            }
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
            return default_config

    def _extract_text_from_region(self, image: np.ndarray, coords: Coordinates) -> str:
        """Extract text from a specific region using OCR"""
        try:
            region = image[coords.y1:coords.y2, coords.x1:coords.x2]
            text = pytesseract.image_to_string(region).strip()
            return text
        except Exception as e:
            logging.error(f"OCR extraction failed: {str(e)}")
            return ""

    def _identify_form_type(self, pdf_path: str) -> Optional[str]:
        """Identify the form type based on content"""
        try:
            doc = fitz.open(pdf_path)
            first_page = doc[0]
            pix = first_page.get_pixmap()
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
                pix.height, pix.width, pix.n)
            
            for form_type, config in self.config["form_types"].items():
                # Convert identifier text to image and use template matching
                if config["identifier_text"].lower() in first_page.get_text().lower():
                    return form_type
            
            return None
        except Exception as e:
            logging.error(f"Form type identification failed for {pdf_path}: {str(e)}")
            return None

    def _extract_ids(self, pdf_path: str, form_type: str) -> Tuple[str, str]:
        """Extract Company ID and Docket ID from the PDF"""
        try:
            doc = fitz.open(pdf_path)
            first_page = doc[0]
            pix = first_page.get_pixmap()
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
                pix.height, pix.width, pix.n)
            
            coords = self.config["form_types"][form_type]
            company_coords = Coordinates(**coords["company_id_coords"])
            docket_coords = Coordinates(**coords["docket_id_coords"])
            
            company_id = self._extract_text_from_region(img, company_coords)
            docket_id = self._extract_text_from_region(img, docket_coords)
            
            return company_id, docket_id
        except Exception as e:
            logging.error(f"ID extraction failed for {pdf_path}: {str(e)}")
            return "", ""

    def _generate_new_filename(self, 
                             company_id: str, 
                             docket_id: str, 
                             form_type: str, 
                             naming_choice: str) -> str:
        """Generate new filename based on user choice"""
        if naming_choice == "company":
            return f"{company_id}_{form_type}.pdf"
        else:
            return f"{docket_id}_{form_type}.pdf"

    def process_pdf(self, 
                   pdf_path: str, 
                   naming_choice: str = "company") -> Optional[Dict]:
        """Process a single PDF file"""
        try:
            form_type = self._identify_form_type(pdf_path)
            if not form_type:
                logging.warning(f"Could not identify form type for {pdf_path}")
                return None

            company_id, docket_id = self._extract_ids(pdf_path, form_type)
            if not company_id or not docket_id:
                logging.warning(f"Could not extract IDs for {pdf_path}")
                return None

            new_filename = self._generate_new_filename(
                company_id, docket_id, form_type, naming_choice)
            
            return {
                "original_filename": os.path.basename(pdf_path),
                "company_id": company_id,
                "docket_id": docket_id,
                "form_type": form_type,
                "new_filename": new_filename
            }
        except Exception as e:
            logging.error(f"Processing failed for {pdf_path}: {str(e)}")
            return None

    def organize_pdfs(self, 
                     input_directory: str, 
                     naming_choice: str = "company") -> None:
        """Organize PDFs from input directory"""
        output_dir = Path(self.config["output_directory"])
        output_dir.mkdir(exist_ok=True)
        
        for pdf_file in Path(input_directory).glob("*.pdf"):
            result = self.process_pdf(str(pdf_file), naming_choice)
            if not result:
                continue
                
            form_type_dir = output_dir / result["form_type"]
            form_type_dir.mkdir(exist_ok=True)
            
            target_path = form_type_dir / result["new_filename"]
            
            # Handle duplicates
            if target_path.exists():
                duplicates_dir = form_type_dir / "duplicates"
                duplicates_dir.mkdir(exist_ok=True)
                target_path = duplicates_dir / result["new_filename"]
                result["is_duplicate"] = "Yes"
                result["duplicate_path"] = str(target_path)
            else:
                result["is_duplicate"] = "No"
                result["duplicate_path"] = ""
            
            shutil.copy2(pdf_file, target_path)
            self.tracking_data.append(result)
            
        # Create tracking spreadsheet
        if self.tracking_data:
            df = pd.DataFrame(self.tracking_data)
            excel_path = output_dir / "organized_pdfs.xlsx"
            df.to_excel(excel_path, index=False)
            logging.info(f"Created tracking spreadsheet at {excel_path}")

def main():
    parser = argparse.ArgumentParser(description="PDF Document Organizer")
    parser.add_argument("input_directory", help="Directory containing PDF files to process")
    parser.add_argument(
        "--naming", 
        choices=["company", "docket"],
        default="company",
        help="Naming convention to use (company or docket ID)"
    )
    parser.add_argument(
        "--config",
        default="config.json",
        help="Path to configuration file"
    )
    
    args = parser.parse_args()
    
    processor = PDFProcessor(args.config)
    processor.organize_pdfs(args.input_directory, args.naming)

if __name__ == "__main__":
    main()