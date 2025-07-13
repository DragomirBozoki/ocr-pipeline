import cv2
import re
import pytesseract
from extraction import extract_frames
from preprocessing import preprocess_frame   # već uključuje crop + binarizaciju

# ---------- RegEx za vađenje validnih € iznosa ----------
def extract_amounts(text):
    pattern = r'(?:€)?\d{1,3}(?:,\d{3})+(?:\.\d{2})'

    raw_matches = re.findall(pattern, text)

    cleaned = []
    for m in raw_matches:
        num = m.replace('€', '')
        try:
            val = float(num.replace(',', ''))
            if val > 100:  # odbaci smešne vrednosti tipa "0,400.26"
                cleaned.append(m if m.startswith('€') else f"€{m}")
        except:
            continue
    return list(dict.fromkeys(cleaned))  # unique


def run_ocr_pipeline(video_path: str):
    frames = extract_frames(video_path, fps=1)

    for i, frame in enumerate(frames, start=1):
        proc = preprocess_frame(frame)  


        config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789,.€$'
        text = pytesseract.image_to_string(proc, config=config)

        cleaned_text = text.replace("\n", " ").replace("\x0c", "").strip()
        print(f"[Second {i:>3}] ➜ OCR raw: {cleaned_text}")

        amounts = extract_amounts(cleaned_text)
        if amounts:
            print(f"   ➜ Extracted amounts: {amounts}")

        cv2.imwrite(f"debug_frame_{i}.png", proc)


if __name__ == "__main__":
    run_ocr_pipeline("nagrada.mp4")
