import cv2
import numpy as np


AMOUNT_REGION = (110, 180, 880, 330) # x1, y1, x2, y2

def preprocess_frame(frame):

    x1, y1, x2, y2 = AMOUNT_REGION
    roi = frame[y1:y2, x1:x2]

    # 2. U sivo
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

  
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)


    thresh = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )


    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    dilated = cv2.dilate(thresh, kernel, iterations=1)

    closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

    resized = cv2.resize(closed, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

    return resized
