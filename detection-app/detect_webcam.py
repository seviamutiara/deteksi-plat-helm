import cv2
from ultralytics import YOLO
import numpy as np
import requests
import datetime
import base64
import re
from fast_plate_ocr import LicensePlateRecognizer

# --- KONFIGURASI ---
MODEL_PATH = "yolov8_helmet_license_plate_v11_final.pt"
CONFIDENCE_THRESHOLD = 0.5
CAMERA_INDEX = 0
API_ENDPOINT_URL = "http://localhost:9000/api/violations/"
PLATE_VALIDATION_API_URL = "http://localhost:9000/api/plat-terdaftar/"

# --- Inisialisasi OCR ---
ocr_model = LicensePlateRecognizer('cct-xs-v1-global-model')
last_sent_time = {}  # format: {'BP 2871 JG': datetime}

# --- Ambil daftar plat dari Django ---
try:
    resp = requests.get(PLATE_VALIDATION_API_URL)
    daftar_plat_terdaftar = [p.upper().replace(" ", "") for p in resp.json().get("plat_terdaftar", [])]
    print(f"[✓] Daftar plat valid: {daftar_plat_terdaftar}")
except Exception as e:
    print(f"[ERROR] Gagal ambil daftar plat terdaftar: {e}")
    daftar_plat_terdaftar = []

# --- Format plat nomor ---
def format_plat_nomor(raw_text):
    raw = raw_text.upper()
    cleaned = re.sub(r'^[^A-Z0-9]+|[^A-Z0-9]+$', '', raw)
    cleaned = re.sub(r'[^A-Z0-9]', '', cleaned)
    match = re.match(r'^([A-Z]{1,2})(\d{3,4})([A-Z]{1,3})$', cleaned)
    if match:
        return f"{match.group(1)} {match.group(2)} {match.group(3)}"
    return None

# --- Kirim pelanggaran ke Django ---
def send_violation_to_api(payload):
    try:
        r = requests.post(API_ENDPOINT_URL, json=payload)
        if r.status_code in (200, 201):
            print(f"[✓] Terkirim: {payload['plate_number']}")
            return True
        else:
            print(f"[✗] Gagal kirim. Status: {r.status_code} → {r.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Koneksi API gagal: {e}")
        return False

# --- Load YOLO ---
print(f"🔍 Memuat model dari {MODEL_PATH}")
try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    print(f"[ERROR] Gagal load model YOLO: {e}")
    exit()

# --- Buka Webcam ---
cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    print("[ERROR] Gagal buka webcam.")
    exit()

print("🎥 Deteksi dimulai... Tekan 'q' untuk keluar.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("[!] Frame kosong.")
        break

    yolo_res = model.predict(source=frame, conf=CONFIDENCE_THRESHOLD, verbose=False)[0]
    detections = yolo_res.boxes
    frame_out = yolo_res.plot()

    no_helmets, plates = [], []
    for box, cls, conf in zip(detections.xyxy.cpu().numpy(),
                              detections.cls.cpu().numpy(),
                              detections.conf.cpu().numpy()):
        x1, y1, x2, y2 = map(int, box)
        label = model.names[int(cls)]
        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        item = {'box': (x1, y1, x2, y2), 'center': center, 'confidence': float(conf)}
        if label == "no-helmet":
            no_helmets.append(item)
        elif label == "license-plate":
            plates.append(item)

    now = datetime.datetime.now()

    for nh in no_helmets:
        min_d, chosen = float('inf'), None
        for p in plates:
            d = np.linalg.norm(np.array(nh['center']) - np.array(p['center']))
            if d < min_d:
                min_d, chosen = d, p

        if not chosen:
            continue

        x1, y1, x2, y2 = chosen['box']
        crop = frame[y1:y2, x1:x2]

        try:
            rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
            ocr_res = ocr_model.run(rgb)
            raw = ocr_res[0] if isinstance(ocr_res, list) else ocr_res
            raw = raw.upper()
            print(f"[OCR] Mentah: {raw}", end='')

            fmt = format_plat_nomor(raw)
            if not fmt:
                print(" → Format tidak valid")
                continue
            print(f" → Valid: {fmt}")

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

        except Exception as e:
            print(f"[ERROR OCR] {e}")
            continue

    cv2.imshow("Deteksi Kamera Pintar", frame_out)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("✅ Program selesai.")
