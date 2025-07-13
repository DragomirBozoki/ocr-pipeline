from extraction import extract_frames
from preprocessing import preprocess_frame
from OCR import ocr_amount, extract_amounts
import cv2
import pytesseract
import re
import sys
import pathlib

video_path = "path/to/video" # Add path where camera has saved videos
frames = extract_frames(video_path)

def run_ocr_pipeline(video_path):
    frames = extract_frames(video_path, fps=1)
    for i, frame in enumerate(frames, start=1):
        thresh = preprocess_frame(frame)
        text = ocr_text(thresh)
        amounts = extract_amounts(text)
        print(f"[Second {i:>3}] ➜ {amounts or 'No amount found'}")


run_ocr_pipeline(video_path)