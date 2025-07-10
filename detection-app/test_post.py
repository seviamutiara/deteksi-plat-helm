import base64
import requests
from datetime import datetime

# BACA GAMBAR UJI
with open("2.jpg", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

# FORMAT PAYLOAD
payload = {
    "waktu": datetime.now().isoformat(),
    "plate_number": "BP 2871 JG	",
    "confidence": 0.93,
    "image_base64": encoded_image,
    "lokasi": "Simulasi Jalur Utama kampus",
    "status": "Belum Ditindak"
}

# KIRIM KE API DJANGO
response = requests.post("http://localhost:8000/api/violations/", json=payload)

# CEK HASIL
print("Status:", response.status_code)
print("Respon:", response.text)
