# import cv2
# import numpy as np
# import pytesseract  # Ensure Tesseract is installed and configured

# def preprocess_distorted_image(image):
#     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#     """Applies enhanced preprocessing for distorted images."""
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Adaptive Histogram Equalization (CLAHE)
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#     enhanced = clahe.apply(gray)

#     # Unsharp Masking
#     blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)
#     unsharp_mask = cv2.addWeighted(enhanced, 1.5, blurred, -0.5, 0)

#     # Morphological Closing (adjust kernel size as needed)
#     kernel = np.ones((3, 3), np.uint8)  
#     closed = cv2.morphologyEx(unsharp_mask, cv2.MORPH_CLOSE, kernel)

#     # Binarization (Otsu's thresholding)
#     thresh = cv2.threshold(closed, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#     return thresh

# # Example usage:
# image = cv2.imread("dist.png")
# processed_image = preprocess_distorted_image(image)
# extracted_text = pytesseract.image_to_string(processed_image, config='--psm 6')

# print(extracted_text)

# # ... (Rest of your PDF processing code) ...


import cv2
import numpy as np
import pytesseract

# ... (Tesseract configuration) ...


def preprocess_distorted_image(image, debug=False): # Add debug parameter
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
 

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if debug:
        cv2.imwrite("1_grayscale.png", gray)



    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    if debug:
        cv2.imwrite("2_clahe.png", enhanced)


    blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)
    unsharp_mask = cv2.addWeighted(enhanced, 1.5, blurred, -0.5, 0)
    if debug:
        cv2.imwrite("3_unsharp_mask.png", unsharp_mask)



    kernel = np.ones((3, 3), np.uint8)
    closed = cv2.morphologyEx(unsharp_mask, cv2.MORPH_CLOSE, kernel)
    if debug:
        cv2.imwrite("4_morphological_closing.png", closed)


    thresh = cv2.threshold(closed, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    if debug:
        cv2.imwrite("5_thresholding.png", thresh)

    return thresh




# Example usage:
image = cv2.imread("dist.png") # Replace with your image path
processed_image = preprocess_distorted_image(image, debug=True) # Enable debug mode


extracted_text = pytesseract.image_to_string(processed_image, config='--psm 6')
print(extracted_text)

# ... (Rest of your PDF processing code)