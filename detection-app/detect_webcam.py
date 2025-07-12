import cv2
from ultralytics import YOLO
import numpy as np
import requests
import datetime
import base64
import re
import logging
from fast_plate_ocr import LicensePlateRecognizer

# --- MATIKAN LOG YOLO ---
logging.getLogger("ultralytics").setLevel(logging.WARNING)

# --- KONFIGURASI ---
MODEL_PATH = "yolov8_helmet_license_plate_v11_final.pt"
CONFIDENCE_THRESHOLD = 0.5
CAMERA_INDEX = 0
API_ENDPOINT_VIOLATIONS = "http://10.10.6.168:9000/api/violations/"
PLATE_VALIDATION_API_URL = "http://10.10.6.168:9000/api/plat-terdaftar/"
RASPI_IP = "10.10.15.190"
BUZZER_API_ENDPOINT = f"http://{RASPI_IP}:5000/buzz"

# --- Inisialisasi Model ---
ocr_model = LicensePlateRecognizer('cct-xs-v1-global-model')
last_sent_time = {}

# --- Ambil Daftar Plat ---
try:
    resp = requests.get(PLATE_VALIDATION_API_URL, timeout=5)
    daftar_plat_terdaftar = [p.upper().replace(" ", "") for p in resp.json().get("plat_terdaftar", [])]
    print(f"[✓] Plat valid: {daftar_plat_terdaftar}")
except Exception as e:
    print(f"[ERROR] Ambil plat: {e}")
    daftar_plat_terdaftar = []

# --- Format Plat Nomor ---
def format_plat_nomor(raw_text):
    raw = raw_text.upper()
    cleaned = re.sub(r'[^A-Z0-9]', '', raw)
    match = re.match(r'^([A-Z]{1,2})(\d{3,4})([A-Z]{1,3})$', cleaned)
    return f"{match.group(1)} {match.group(2)} {match.group(3)}" if match else None

# --- Kirim ke Django ---
def send_violation_to_api(payload):
    try:
        r = requests.post(API_ENDPOINT_VIOLATIONS, json=payload, timeout=5)
        if r.status_code in (200, 201):
            print(f"[✓] Terkirim: {payload['plate_number']}")
            return True
        else:
            print(f"[✗] Gagal kirim. Status: {r.status_code}")
            return False
    except Exception as e:
        print(f"[API ERROR] {e}")
        return False

# --- Trigger Buzzer Raspi ---
def trigger_raspi_buzzer():
    try:
        r = requests.post(BUZZER_API_ENDPOINT, json={"action": "buzz"}, timeout=3)
        print("[BUZZER] Triggered" if r.status_code == 200 else "[BUZZER] Gagal trigger")
    except Exception as e:
        print(f"[BUZZER ERROR] {e}")

# --- Load YOLO ---
print(f"🔍 Memuat model dari {MODEL_PATH}")
model = YOLO(MODEL_PATH)

# --- Buka Kamera ---
cap = cv2.VideoCapture(CAMERA_INDEX)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)    # Resolusi lebih rendah
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
cap.set(cv2.CAP_PROP_FPS, 5)              # FPS lebih rendah

print("🎥 Deteksi dimulai... Tekan 'q' untuk keluar.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("[!] Kamera tidak terbaca.")
        break

    results = model(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)[0]
    frame_out = results.plot()

    no_helmets, plates = [], []
    for box, cls, conf in zip(results.boxes.xyxy.cpu().numpy(),
                              results.boxes.cls.cpu().numpy(),
                              results.boxes.conf.cpu().numpy()):
        x1, y1, x2, y2 = map(int, box)
        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        label = model.names[int(cls)]
        item = {'box': (x1, y1, x2, y2), 'center': center, 'confidence': float(conf)}
        if label == "no-helmet":
            no_helmets.append(item)
        elif label == "license-plate":
            plates.append(item)

    now = datetime.datetime.now()
    for nh in no_helmets:
        chosen = min(plates, key=lambda p: np.linalg.norm(np.array(nh['center']) - np.array(p['center'])), default=None)
        if not chosen:
            continue

        x1, y1, x2, y2 = chosen['box']
        crop = frame[y1:y2, x1:x2]

        try:
            rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
            ocr_res = ocr_model.run(rgb)
            raw = ocr_res[0] if isinstance(ocr_res, list) else ocr_res
            fmt = format_plat_nomor(raw)
            if not fmt:
                print(f"[OCR] {raw} → Format tidak valid")
                continue

            key = fmt.replace(" ", "")
            if key not in daftar_plat_terdaftar:
                print(f"[FILTER] {fmt} tidak terdaftar.")
                continue

            last = last_sent_time.get(fmt)
            if last and (now - last).total_seconds() < 300:
                print(f"[SKIP] {fmt} sudah dikirim {int((now - last).total_seconds())}s lalu")
                continue

            _, buf = cv2.imencode('.jpg', frame_out)
            img_b64 = base64.b64encode(buf).decode('utf-8')
            payload = {
                "waktu": now.isoformat(),
                "plate_number": fmt,
                "confidence": round(nh['confidence'], 2),
                "image_base64": img_b64,
                "lokasi": "Jalur Utama Kampus",
                "status": "Belum Ditindak"
            }

            if send_violation_to_api(payload):
                last_sent_time[fmt] = now
                trigger_raspi_buzzer()

        except Exception as e:
            print(f"[ERROR OCR/Payload] {e}")

    cv2.imshow("Deteksi Kamera", frame_out)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
