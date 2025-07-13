import cv2
import re
import pytesseract
import paho.mqtt.client as mqtt
from extraction import extract_frames
from preprocessing import preprocess_frame  # crop + binarizacija

# ── MQTT podešavanje ──────────────────────────────────────────
MQTT_BROKER = "localhost"      # podesiti
MQTT_PORT   = 1883             # podesiti
MQTT_TOPIC  = "ocr/amounts"

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)
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

    for i, frame in enumerate(frames, start=1):
        proc = preprocess_frame(frame)

        # OCR: samo cifre, zarez, tačka, €
        config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789,.€'
        raw_text = pytesseract.image_to_string(proc, config=config)
        cleaned = raw_text.replace("\n", " ").replace("\x0c", "").strip()
        print(f"[Second {i:>3}] ➜ OCR raw: {cleaned}")

        amounts = extract_amounts(cleaned)
        if amounts:
            print(f"   ➜ Extracted amounts: {amounts}")
            for amt in amounts:
                payload = f"second={i},amount={amt}"
                client.publish(MQTT_TOPIC, payload)
                print(f"MQTT sent ➜ {payload}")

        cv2.imwrite(f"debug_frame_{i}.png", proc)

    client.disconnect()


if __name__ == "__main__":
    run_ocr_pipeline("nagrada.mp4")
