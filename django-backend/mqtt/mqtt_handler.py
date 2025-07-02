import os
import sys
import json
import base64
import threading
from datetime import datetime

from django.utils.timezone import now
from django.core.files.base import ContentFile

import paho.mqtt.client as mqtt

# --- Hanya setup Django jika file dijalankan langsung ---
if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PENGENALAN.settings')
    import django
    django.setup()

    from django.contrib.auth.models import User
    from akun.models import Kendaraan, Pelanggaran, Kamera


# --- Callback untuk topik kendaraan ---
def on_kendaraan_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print("[MQTT KENDARAAN] Diterima:", data)

        plat_nomor = data.get('plat_nomor')
        jenis_kendaraan = data.get('jenis_kendaraan')
        base64_foto = data.get('foto')
        username = data.get('username')

        if not all([plat_nomor, jenis_kendaraan, base64_foto, username]):
            print("[!] Data kendaraan tidak lengkap")
            return

        from django.contrib.auth.models import User
        from akun.models import Kendaraan

        user = User.objects.filter(username=username).first()
        if not user:
            print(f"[!] User dengan username '{username}' tidak ditemukan.")
            return

        format, imgstr = base64_foto.split(';base64,')
        ext = format.split('/')[-1]
        img_data = ContentFile(base64.b64decode(imgstr), name=f"{plat_nomor}.{ext}")

        kendaraan_obj, created = Kendaraan.objects.get_or_create(
            plat_nomor=plat_nomor,
            defaults={
                'jenis_kendaraan': jenis_kendaraan,
                'foto_kendaraan': img_data,
                'user': user,
            }
        )

        if created:
            print("[✓] Kendaraan baru ditambahkan")
        else:
            print("[i] Kendaraan sudah ada")

    except Exception as e:
        print("[!] Gagal menyimpan kendaraan:", e)


# --- Callback untuk topik pelanggaran ---
def on_pelanggaran_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print("[MQTT PELANGGARAN] Diterima:", data)

        plat_nomor = data.get('plat_nomor')
        lokasi = data.get('lokasi')
        base64_gambar = data.get('bukti')
        id_kamera = data.get('id_kamera') 
        waktu = now()

        from akun.models import Kendaraan, Kamera, Pelanggaran

        kendaraan = Kendaraan.objects.filter(plat_nomor=plat_nomor).first()
        if not kendaraan:
            print(f"[!] Kendaraan dengan plat {plat_nomor} tidak ditemukan.")
            return

        kamera = Kamera.objects.filter(id=id_kamera, status="Aktif").first()
        if not kamera:
            print(f"[!] Kamera dengan ID {id_kamera} tidak ditemukan atau tidak aktif.")
            return

        format, imgstr = base64_gambar.split(';base64,')
        ext = format.split('/')[-1]
        img_data = ContentFile(base64.b64decode(imgstr), name=f"pelanggaran_{plat_nomor}_{int(datetime.timestamp(waktu))}.{ext}")

        Pelanggaran.objects.create(
            kendaraan=kendaraan,
            kamera=kamera,
            waktu=waktu,
            lokasi=lokasi,
            bukti_gambar=img_data,
            status="Belum Ditindak"
        )

        print("[✓] Pelanggaran berhasil disimpan.")

    except Exception as e:
        print("[!] Gagal menyimpan pelanggaran:", e)


# --- Fungsi untuk menjalankan MQTT ---
def start_mqtt():
    client = mqtt.Client()
    client.connect("broker.hivemq.com", 1883, 60)

    client.message_callback_add("kamera/kendaraan", on_kendaraan_message)
    client.message_callback_add("kamera/pelanggaran", on_pelanggaran_message)

    client.subscribe("kamera/kendaraan")
    client.subscribe("kamera/pelanggaran")

    print("[MQTT] Subscribed dan berjalan...")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[MQTT] Dihentikan oleh pengguna (Ctrl+C)")
        client.disconnect()


# --- Fungsi untuk menjalankan di thread (jika dari Django) ---
def run_mqtt_thread():
    thread = threading.Thread(target=start_mqtt)
    thread.daemon = True
    thread.start()


# --- Jika dijalankan langsung ---
if __name__ == '__main__':
    print("[START] Menjalankan MQTT handler...")
    start_mqtt()
