import cv2
import numpy as np

# Load Image
# image = cv2.imread(r"C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\zoomed_processed_image.png")
image = cv2.imread(r"C:\Users\Anurag Dandge\Open Source\PDF_SPLITTER_V_2\zoomed_processed_image.png")

# Preprocessing
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# Find Contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter for Rectangles and Crop
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
    if len(approx) == 4:
        x, y, w, h = cv2.boundingRect(approx)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)  # Draw rectangle (optional)
        cropped_image = image[y:y+h, x:x+w]
        cv2.imwrite(f"cropped_rectangle_{x}_{y}.jpg", cropped_image) 

cv2.imshow("Detected Rectangles", image) # Display the image with rectangles (optional)
cv2.waitKey(0)
cv2.destroyAllWindows()