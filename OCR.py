import re
import pytesseract

# ----------------- OCR -----------------
def ocr_text(img) -> str:
    """
    Run Tesseract on the pre-processed image and return raw text.
    """
    config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789€.,C'
    text = pytesseract.image_to_string(img, config=config)
    # normalizuj C→€, ukloni \n i kontrolne znakove
    return (text.replace("C", "€")
                .replace("\n", " ")
                .replace("\x0c", "")
                .strip())

# ----------------- REGEX -----------------
# Dozvoljava i bez € – dodat ćemo ga poslije
_AMOUNT_RE = re.compile(
    r'(?:€)?\d{1,3}(?:[.,]\d{3})+(?:[.,]\d{2})',  # npr. €221,634.56 ili 221.634,56
    flags=re.IGNORECASE
)

# ----------------- EKSTRAKCIJA -----------------
def extract_amounts(text: str):
    """
    Return list of raw matches (može biti bez € ili s lošim separatorima).
    """
    return _AMOUNT_RE.findall(text)

# ----------------- ČIŠĆENJE & VALIDACIJA -----------------
def clean_amounts(raw_matches):
    """
    • Dodaje € ako ga nema.
    • Uklanja razmake.
    • Normalizuje decimalni separator u '.'.
    • Zadržava samo iznose sa TAČNO dvije decimale i vrijednošću ≥ 1.
    """
    cleaned = []
    for m in raw_matches:
        amt = m.replace(" ", "")
        if not amt.startswith("€"):
            amt = "€" + amt
        # zamijeni eventualne zareze za decimale u točku (hiljade ostaju zarez)
        euros, decimals = amt.rsplit(".", 1) if "." in amt else (amt, "")
        euros = euros.replace(",", "")
        try:
            val = float(f"{euros[1:]}.{decimals}") if decimals else float(euros[1:])
            if val >= 1 and len(decimals) == 2:
                # formatiraj nazad: hiljade zarez, decimale točka
                formatted = f"€{val:,.2f}"
                cleaned.append(formatted)
        except ValueError:
            continue
    # ukloni duplikate, zadrži redoslijed
    return list(dict.fromkeys(cleaned))

# ----------------- FULL POST-PROCESS -----------------
def postprocess(text: str):
    """
    High-level helper: OCR-raw string → list of valid, formatted euro amounts.
    """
    raw = extract_amounts(text)
    return clean_amounts(raw)
