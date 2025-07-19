import base64
import requests
from datetime import datetime

# === KONFIGURASI ===
IMAGE_PATH = "1.jpg"
API_URL = "http://127.0.0.1:9000/api/violations/"
KENDARAAN_ID = 3  # Pastikan kendaraan dengan ID ini ada di database

# === BACA & ENCODE GAMBAR ===
import os

BASE_DIR = os.path.dirname(__file__)
IMAGE_PATH = os.path.join(BASE_DIR, "2.jpg")

with open(IMAGE_PATH, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

# === SIAPKAN PAYLOAD ===
payload = {
    "waktu": datetime.now().isoformat(),
    "plate_number": "BP 2871 JG",
    "confidence": 0.93,
    "image_base64": encoded_image,
    "lokasi": "Parkiran Utama kampus",
    "status": "Belum Ditindak",
    "jumlah_denda": "100000.00",
    "bukti_pembayaran": None,
    "kendaraan": KENDARAAN_ID,
    "kamera": None
}

# === KIRIM POST REQUEST ===
try:
    response = requests.post(API_URL, json=payload)
    print(f"\n✅ Status Code: {response.status_code}")
    try:
        print("📦 Response JSON:", response.json())
    except Exception:
        print("📃 Response Text:", response.text)
except requests.exceptions.RequestException as e:
    print("❌ Terjadi error saat mengirim request:", e)
