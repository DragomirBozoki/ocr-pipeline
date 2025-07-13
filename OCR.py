import pytesseract
import re

#  Run Tesseract OCR
def ocr_text(img):
    config = r"--oem 1 --psm 6"
    return pytesseract.image_to_string(img, config=config)


# Extract Euro amounts using regex
_AMOUNT_RE = re.compile(
    r"\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?\s*(?:€|EUR|EU)",
    flags=re.IGNORECASE
)

def extract_amounts(text):
    return _AMOUNT_RE.findall(text)
