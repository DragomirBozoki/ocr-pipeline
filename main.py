import cv2
import re
import pytesseract
import paho.mqtt.client as mqtt
from extraction import extract_frames
from preprocessing import preprocess_frame  # crop + binarizacija
from amountTracker import AmountTracker
# ── MQTT podešavanje ──────────────────────────────────────────
#MQTT_BROKER = "localhost"      # podesiti
#MQTT_PORT   = 1883             # podesiti
#MQTT_TOPIC  = "ocr/amounts"

#client = mqtt.Client()
#client.connect(MQTT_BROKER, MQTT_PORT, 60)
# ──────────────────────────────────────────────────────────────

def extract_amounts(text: str):

    pattern = r'(?:€)?\d{1,3}(?:,\d{3})+(?:\.\d{2})'
    raw = re.findall(pattern, text)

    out = []
    for m in raw:
        num = m.replace('€', '')
        try:
            val = float(num.replace(',', ''))
            if val >= 100:                          # ignoriši sitne i loše
                out.append(m if m.startswith('€') else f"€{m}")
        except ValueError:
            continue
    # ukloni duplikate, očuvaj redosled
    return list(dict.fromkeys(out))


def run_ocr_pipeline(video_path: str):
    
    frames = extract_frames(video_path, fps=1)
    tracker = AmountTracker()

    for i, frame in enumerate(frames, start=1):
        proc = preprocess_frame(frame)
        config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789,.€$'
        text = pytesseract.image_to_string(proc, config=config)
        cleaned_text = text.replace("\n", " ").replace("\x0c", "").strip()

        print(f"[Second {i:>3}] ➜ OCR raw: {cleaned_text}")
        amounts = extract_amounts(cleaned_text)
        if amounts:
            print(f"   ➜ Extracted: {amounts}")

        stable = tracker.update(amounts)
        if stable:
            print(f"Stable value: {stable}")

        cv2.imwrite(f"debug_frame_{i}.png", proc)


    # client.disconnect()


if __name__ == "__main__":
    run_ocr_pipeline("nagrada.mp4")
