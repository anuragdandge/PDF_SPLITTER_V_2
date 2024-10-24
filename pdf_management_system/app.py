import os
import shutil
import pandas as pd
import numpy as np
import cv2
import json
from pathlib import Path
from PyPDF2 import PdfMerger
import pdf2image
import pytesseract
from PIL import Image, ImageDraw
from dataclasses import dataclass
from typing import Tuple, Dict, Optional

@dataclass
class Coordinates:
    x1: int
    y1: int
    x2: int
    y2: int
    
    def scale(self, scale_x: float, scale_y: float) -> 'Coordinates':
        return Coordinates(
            int(self.x1 * scale_x),
            int(self.y1 * scale_y),
            int(self.x2 * scale_x),
            int(self.y2 * scale_y)
        )

class OCRPreprocessor:
    @staticmethod
    def apply_preprocessing(image: np.ndarray, methods: list) -> np.ndarray:
        """Apply multiple preprocessing methods to improve OCR accuracy"""
        processed = image.copy()
        
        for method in methods:
            if method == 'threshold':
                processed = cv2.threshold(processed, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            elif method == 'denoise':
                processed = cv2.fastNlMeansDenoisingColored(processed, None, 10, 10, 7, 21)
            elif method == 'sharpen':
                kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
                processed = cv2.filter2D(processed, -1, kernel)
            elif method == 'erode':
                kernel = np.ones((2,2), np.uint8)
                processed = cv2.erode(processed, kernel, iterations=1)
            elif method == 'dilate':
                kernel = np.ones((2,2), np.uint8)
                processed = cv2.dilate(processed, kernel, iterations=1)
                
        return processed

class IDValidator:
    @staticmethod
    def validate_company_id(company_id: str) -> bool:
        """Validate company ID format"""
        # Add your specific validation rules here
        if not company_id:
            return False
        
        # Example rules:
        # 1. Must be alphanumeric
        if not company_id.isalnum():
            return False
            
        # 2. Must be between 5-10 characters
        if not (5 <= len(company_id) <= 10):
            return False
            
        # 3. Must start with a letter
        if not company_id[0].isalpha():
            return False
            
        return True
    
    @staticmethod
    def validate_docket_id(docket_id: str) -> bool:
        """Validate docket ID format"""
        if not docket_id:
            return False
        
        # Example rules:
        # 1. Must contain at least one number
        if not any(c.isdigit() for c in docket_id):
            return False
            
        # 2. Must be between 4-12 characters
        if not (4 <= len(docket_id) <= 12):
            return False
            
        # 3. Must not contain special characters
        if not all(c.isalnum() or c == '-' for c in docket_id):
            return False
            
        return True

class DocumentManagementSystem:
    def __init__(self, base_directory: str):
        self.base_directory = Path(base_directory)
        self.duplicates_dir = self.base_directory / "duplicates"
        self.excel_path = self.base_directory / "file_records.xlsx"
        self.duplicate_excel_path = self.base_directory / "duplicate_records.xlsx"
        self.config_path = self.base_directory / "ocr_config.json"
        
        # Create necessary directories
        self.duplicates_dir.mkdir(exist_ok=True)
        
        # Load or create configuration
        self.load_config()
        
        # Initialize Excel files
        self._initialize_excel_files()
        
        # Initialize preprocessor
        self.preprocessor = OCRPreprocessor()
        
        # Initialize validator
        self.validator = IDValidator()
    
    def load_config(self):
        """Load OCR configuration from file or create default"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                config = json.load(f)
        else:
            config = {
                'coordinates': {
                    'company_id': {'x1': 100, 'y1': 100, 'x2': 300, 'y2': 150},
                    'docket_id': {'x1': 400, 'y1': 100, 'x2': 600, 'y2': 150}
                },
                'preprocessing_methods': ['threshold', 'denoise', 'sharpen'],
                'reference_page_size': {'width': 2480, 'height': 3508}  # A4 at 300 DPI
            }
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)
        
        self.config = config
    
    def save_config(self):
        """Save current configuration to file"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, indent=4)
    
    def calibrate_coordinates(self, sample_pdf_path: str) -> Dict[str, Coordinates]:
        """Interactive calibration function to find correct coordinates"""
        # Convert first page of PDF to image
        images = pdf2image.convert_from_path(sample_pdf_path, first_page=1, last_page=1)
        image = np.array(images[0])
        
        # Create a window for calibration
        window_name = 'Calibration'
        cv2.namedWindow(window_name)
        
        coordinates = {}
        fields = ['company_id', 'docket_id']
        
        def mouse_callback(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                param['points'].append((x, y))
        
        for field in fields:
            print(f"\nCalibrating coordinates for {field}")
            print("Click on the top-left and bottom-right corners of the text area")
            
            # Create a copy of the image for this field
            img_copy = image.copy()
            points = []
            
            # Set up mouse callback
            cv2.setMouseCallback(window_name, mouse_callback, {'points': points})
            
            while len(points) < 2:
                cv2.imshow(window_name, img_copy)
                if len(points) == 1:
                    cv2.circle(img_copy, points[0], 5, (0, 255, 0), -1)
                cv2.waitKey(1)
            
            # Save coordinates
            coordinates[field] = Coordinates(
                points[0][0], points[0][1],
                points[1][0], points[1][1]
            )
            
            # Draw rectangle
            cv2.rectangle(img_copy, points[0], points[1], (0, 255, 0), 2)
            cv2.imshow(window_name, img_copy)
            cv2.waitKey(1000)
        
        cv2.destroyAllWindows()
        
        # Update config
        for field, coords in coordinates.items():
            self.config['coordinates'][field] = {
                'x1': coords.x1, 'y1': coords.y1,
                'x2': coords.x2, 'y2': coords.y2
            }
        
        self.save_config()
        return coordinates
    
    def extract_text_from_coordinates(self, image: np.ndarray, field: str) -> str:
        """Extract text from specific coordinates with preprocessing"""
        # Get coordinates and scale them to actual image size
        config_coords = self.config['coordinates'][field]
        ref_size = self.config['reference_page_size']
        
        scale_x = image.shape[1] / ref_size['width']
        scale_y = image.shape[0] / ref_size['height']
        
        coords = Coordinates(
            config_coords['x1'], config_coords['y1'],
            config_coords['x2'], config_coords['y2']
        ).scale(scale_x, scale_y)
        
        # Crop image
        cropped = image[coords.y1:coords.y2, coords.x1:coords.x2]
        
        # Apply preprocessing
        processed = self.preprocessor.apply_preprocessing(
            cropped,
            self.config['preprocessing_methods']
        )
        
        # Perform OCR
        text = pytesseract.image_to_string(
            processed,
            config='--psm 7 --oem 3'
        ).strip()
        
        return text
    
    def process_file(self, original_file_path: str) -> Optional[Path]:
        """Process a single file with enhanced validation and error handling"""
        try:
            # Convert PDF to image
            images = pdf2image.convert_from_path(original_file_path, first_page=1, last_page=1)
            image = cv2.cvtColor(np.array(images[0]), cv2.COLOR_RGB2BGR)
            
            # Extract IDs
            company_id = self.extract_text_from_coordinates(image, 'company_id')
            docket_id = self.extract_text_from_coordinates(image, 'docket_id')
            
            # Clean and validate IDs
            company_id = self._clean_id(company_id)
            docket_id = self._clean_id(docket_id)
            
            if not self.validator.validate_company_id(company_id):
                raise ValueError(f"Invalid Company ID format: {company_id}")
            
            if not self.validator.validate_docket_id(docket_id):
                raise ValueError(f"Invalid Docket ID format: {docket_id}")
            
            # Proceed with file renaming and management
            return self.rename_file(Path(original_file_path), company_id, docket_id)
            
        except Exception as e:
            print(f"Error processing file {original_file_path}: {str(e)}")
            return None
    
    def _clean_id(self, id_text: str) -> str:
        """Clean extracted ID text"""
        # Remove special characters but keep hyphens
        cleaned = ''.join(c for c in id_text if c.isalnum() or c == '-')
        return cleaned.strip()

    # ... (rest of the existing methods remain the same)

def main():
    # Initialize the system
    dms = DocumentManagementSystem(r"C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\Input")
    
    # Optional: Run calibration with a sample PDF
    # dms.calibrate_coordinates("path/to/sample.pdf")
    
    # Process all PDF files in a directory
    #input_directory = Path("C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\Extracted_PDF")
    input_directory = Path(r"C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\Extracted_PDF")
    
    for pdf_file in input_directory.glob("*.pdf"):
        new_path = dms.process_file(pdf_file)
        if new_path:
            print(f"Successfully processed: {pdf_file.name} -> {new_path.name}")
        else:
            print(f"Failed to process: {pdf_file.name}")

if __name__ == "__main__":
    main()