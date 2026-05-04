import pytesseract
import cv2
import numpy as np

def preprocess_image(image):
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    return thresh

def extract_text(image):
    processed = preprocess_image(image)
    text = pytesseract.image_to_string(processed)
    return text