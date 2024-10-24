from PIL import Image
import pytesseract

# Configure Tesseract path (if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Replace with your path

# Load the image
image_path = './original_cropped_image.png'  # Replace with your image path
image = Image.open(image_path)

# Use pytesseract to extract text from the image
text = pytesseract.image_to_string(image)

print("Extracted Text:", text)
