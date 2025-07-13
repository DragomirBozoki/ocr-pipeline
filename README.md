# ocr-pipeline

# OCR Euro Amount Extractor

This is a lightweight Python pipeline that extracts Euro currency amounts (e.g. "1.000 EUR", "500 €") from video files using OCR.

It is designed to run on low-power devices such as the Raspberry Pi Zero 2 W but can also be tested on any regular laptop or desktop.

## Features

- Extracts one frame per second from a video
- Preprocesses each frame for better OCR results
- Uses Tesseract to extract text
- Parses and returns detected Euro amounts using regular expressions

## Usage

Install dependencies:

```bash
pip install -r requirements.txt
sudo apt install tesseract-ocr
