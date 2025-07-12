import socket
import struct
import cv2
import numpy as np
import datetime
import base64
import re
import requests
from ultralytics import YOLO
from fast_plate_ocr import LicensePlateRecognizer

# --- KONFIGURASI ---
MODEL_PATH = "yolov8_helmet_license_plate_v11_final.pt"
CONFIDENCE_THRESHOLD = 0.5
PORT = 9999
PLATE_VALIDATION_API_URL = "http://10.10.12.124:9000/api/plat-terdaftar/"
API_ENDPOINT_URL = "http://10.10.12.124:9000/api/violations/"

# --- Inisialisasi Model ---
print("[INFO] Memuat model YOLO...")
model = YOLO(MODEL_PATH)
ocr_model = LicensePlateRecognizer('cct-xs-v1-global-model')

# --- Ambil daftar plat dari Django ---
try:
    resp = requests.get(PLATE_VALIDATION_API_URL, timeout=5)
    daftar_plat_terdaftar = [p.upper().replace(" ", "") for p in resp.json().get("plat_terdaftar", [])]
    print(f"[✓] Daftar plat valid: {daftar_plat_terdaftar}")
except Exception as e:
    print(f"[ERROR] Gagal ambil daftar plat terdaftar: {e}")
    daftar_plat_terdaftar = []

last_sent_time = {}

def format_plat_nomor(raw_text):
    raw = raw_text.upper()
    cleaned = re.sub(r'^[^A-Z0-9]+|[^A-Z0-9]+$', '', raw)
    cleaned = re.sub(r'[^A-Z0-9]', '', cleaned)
    match = re.match(r'^([A-Z]{1,2})(\d{3,4})([A-Z]{1,3})$', cleaned)
    if match:
        return f"{match.group(1)} {match.group(2)} {match.group(3)}"
    return None

def send_violation_to_api(payload):
    try:
        r = requests.post(API_ENDPOINT_URL, json=payload, timeout=5)
        if r.status_code in (200, 201):
            print(f"[✓] Terkirim: {payload['plate_number']}")
            return True
        else:
            print(f"[✗] Gagal kirim. Status: {r.status_code} → {r.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Koneksi API gagal: {e}")
        return False

# --- Socket Setup ---
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', PORT))
server_socket.listen(1)

print(f"[RECEIVER] Menunggu koneksi Raspberry Pi di port {PORT}...")
client_socket, addr = server_socket.accept()
print(f"[RECEIVER] Terhubung dengan {addr}")

data = b""
payload_size = struct.calcsize('>L')

while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4096)
        if not packet:
            break
        data += packet

    packed_size = data[:payload_size]
    data = data[payload_size:]
    frame_size = struct.unpack('>L', packed_size)[0]

    while len(data) < frame_size:
        data += client_socket.recv(4096)

    frame_data = data[:frame_size]
    data = data[frame_size:]

    frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
    if frame is None:
        continue

    now = datetime.datetime.now()
    yolo_res = model.predict(source=frame, conf=CONFIDENCE_THRESHOLD, verbose=False)[0]
    detections = yolo_res.boxes
    frame_out = yolo_res.plot()

    no_helmets, plates = [], []
    for box, cls, conf in zip(detections.xyxy.cpu().numpy(), detections.cls.cpu().numpy(), detections.conf.cpu().numpy()):
        x1, y1, x2, y2 = map(int, box)
        label = model.names[int(cls)]
        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        item = {'box': (x1, y1, x2, y2), 'center': center, 'confidence': float(conf)}
        if label == "no-helmet":
            no_helmets.append(item)
        elif label == "license-plate":
            plates.append(item)

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
            fmt = format_plat_nomor(raw)
            if not fmt:
                continue

            key = fmt.replace(" ", "")
            if key not in daftar_plat_terdaftar:
                continue

            last = last_sent_time.get(fmt)
            if last and (now - last).total_seconds() < 300:
                continue

            _, buf = cv2.imencode('.jpg', frame_out, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
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

    cv2.imshow("Receiver - Kamera + Deteksi", frame_out)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

client_socket.close()
server_socket.close()
cv2.destroyAllWindows()