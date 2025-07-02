import requests
import base64
from datetime import datetime

with open("sample_pelanggaran.jpg", "rb") as img:
    encoded = base64.b64encode(img.read()).decode('utf-8')

data = {
    "plate_number": "BP1234ZK",
    "confidence": 0.89,
    "image_base64": encoded,
    "waktu": datetime.now().isoformat(),
    "lokasi": "Gerbang Utama",
    "status": "Belum Ditindak",
    "kamera": None
}

r = requests.post("http://localhost:8000/akun/api/violations/", json=data)
print(r.status_code)
print(r.json())
