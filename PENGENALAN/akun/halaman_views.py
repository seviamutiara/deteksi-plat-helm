import paho.mqtt.client as mqtt
import base64
from django.shortcuts import render
from .models import Kendaraan , Pelanggaran , Kamera
from django.contrib.auth.models import User
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
import threading
import json
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from django.utils.timezone import now
from datetime import date, datetime

def kendaraan_list(request):
    kendaraan_list = Kendaraan.objects.all()
    return render(request, 'kendaraan/kendaraan_list.html', {'kendaraan_list': kendaraan_list})


def pelanggaran_list(request):
    today = date.today()
    total_today = Pelanggaran.objects.filter(waktu__date=today).count()
    ditindak = Pelanggaran.objects.filter(status='Ditindak').count()
    selesai = Pelanggaran.objects.filter(status='Selesai').count()

    try:
        kamera_aktif = Kamera.objects.filter(status='Aktif').count()
    except:
        kamera_aktif = 0  

    pelanggarans = Pelanggaran.objects.select_related('kendaraan').all()
    return render(request, 'halaman/dashboard.html', {
        'pelanggarans': pelanggarans,
        'total_today': total_today,
        'ditindak': ditindak,
        'selesai': selesai,
        'kamera_aktif': kamera_aktif,
    })


# --- MQTT untuk kendaraan ---
def on_kendaraan_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print("[MQTT KENDARAAN] Diterima:", data)

        plat_nomor = data.get('plat_nomor')
        jenis_kendaraan = data.get('jenis_kendaraan')
        base64_foto = data.get('foto')
        username = data.get('username')

        if not all([plat_nomor, jenis_kendaraan, base64_foto, username]):
            print("Data kendaraan tidak lengkap")
            return

        user = User.objects.get(username=username)

        format, imgstr = base64_foto.split(';base64,')
        ext = format.split('/')[-1]
        img_data = ContentFile(base64.b64decode(imgstr), name=f"{plat_nomor}.{ext}")

    
        Kendaraan, created = Kendaraan.objects.get_or_create(
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


# --- MQTT untuk pelanggaran ---
def on_pelanggaran_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print("[MQTT PELANGGARAN] Diterima:", data)

        plat_nomor = data.get('plat_nomor')
        lokasi = data.get('lokasi')
        base64_gambar = data.get('bukti')
        id_kamera = data.get('id_kamera')  # ambil id_kamera dari payload
        waktu = now()

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


def start_mqtt():
    client = mqtt.Client()
    client.connect("broker.hivemq.com", 1883, 60)

    client.message_callback_add("kamera/kendaraan", on_kendaraan_message)
    client.message_callback_add("kamera/pelanggaran", on_pelanggaran_message)

    client.subscribe("kamera/kendaraan")
    client.subscribe("kamera/pelanggaran")

    client.loop_forever()


def histori_pelanggaran(request):
    user = request.user

    if user.is_staff:
        pelanggarans = Pelanggaran.objects.filter(status='Selesai').select_related('kendaraan', 'kendaraan__user')
        template = 'halaman/history.html'
    else:
        pelanggarans = Pelanggaran.objects.filter(
            kendaraan__user=user,
            status='Selesai'
        ).select_related('kendaraan')
        template = 'pengguna/history_pengguna.html'

    return render(request, template, {'pelanggarans': pelanggarans})

def download_histori_pdf(request):
    user = request.user
    if user.is_staff:
        pelanggarans = Pelanggaran.objects.filter(status='Selesai').select_related('kendaraan')
    else:
        pelanggarans = Pelanggaran.objects.filter(
            kendaraan__user=user,
            status='Selesai'
        ).select_related('kendaraan')

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 14)
    p.drawString(2 * cm, height - 2 * cm, "Laporan Histori Pelanggaran")

    y = height - 3 * cm
    p.setFont("Helvetica", 10)

    for pel in pelanggarans:
        p.drawString(2 * cm, y, f"ID: {pel.id_pelanggaran} | Plat: {pel.kendaraan.plat_nomor} | Lokasi: {pel.lokasi} | Waktu: {pel.waktu.strftime('%d-%m-%Y %H:%M')}")
        y -= 1 * cm
        if y <= 2 * cm:
            p.showPage()
            y = height - 2 * cm

    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf', headers={
        'Content-Disposition': 'attachment; filename="histori_pelanggaran.pdf"',
    })


