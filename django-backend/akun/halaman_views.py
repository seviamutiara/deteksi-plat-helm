from django.shortcuts import render, redirect, get_object_or_404
from .models import Kendaraan, Pelanggaran, Kamera
from .forms import KendaraanForm  
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.http import HttpResponse
from io import BytesIO
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from datetime import datetime, date
from PIL import Image
import paho.mqtt.client as mqtt
import base64
import threading
import json

def kendaraan_list(request):
    kendaraan_list = Kendaraan.objects.all()
    return render(request, 'kendaraan/kendaraan_list.html', {'kendaraan_list': kendaraan_list})

def kendaraan_create(request):
    if request.method == 'POST':
        form = KendaraanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('kendaraan_list')
    else:
        form = KendaraanForm()
    return render(request, 'kendaraan/kendaraan_form.html', {'form': form})

def pelanggaran_list(request):
    today = date.today()
    total_today = Pelanggaran.objects.filter(waktu__date=today).count()
    ditindak = Pelanggaran.objects.filter(status='Ditindak').count()
    selesai = Pelanggaran.objects.filter(status='Selesai').count()

    try:
        kamera_aktif = Kamera.objects.filter(status='Aktif').count()
    except:
        kamera_aktif = 0

    pelanggarans = Pelanggaran.objects.all().select_related('kendaraan')
    return render(request, 'halaman/dashboard.html', {
        'pelanggarans': pelanggarans,
        'total_today': total_today,
        'ditindak': ditindak,
        'selesai': selesai,
        'kamera_aktif': kamera_aktif,
    })

def histori_pelanggaran(request):
    user = request.user
    if user.is_staff:
        pelanggarans = Pelanggaran.objects.filter(status='Selesai').select_related('kendaraan')
        template = 'halaman/history.html'
    else:
        kendaraan_user = Kendaraan.objects.filter(user=user)
        plat_user = kendaraan_user.values_list('plat_nomor', flat=True)
        pelanggarans = Pelanggaran.objects.filter(
            plate_number__in=plat_user,
            status='Selesai'
        )
        template = 'pengguna/history_pengguna.html'

    return render(request, template, {'pelanggarans': pelanggarans})

def download_histori_pdf(request):
    user = request.user
    if user.is_staff:
        pelanggarans = Pelanggaran.objects.filter(status='Selesai')
    else:
        kendaraan_user = Kendaraan.objects.filter(user=user)
        plat_user = kendaraan_user.values_list('plat_nomor', flat=True)
        pelanggarans = Pelanggaran.objects.filter(
            plate_number__in=plat_user,
            status='Selesai'
        )

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 14)
    p.drawString(2 * cm, height - 2 * cm, "Laporan Histori Pelanggaran")

    y = height - 3 * cm
    p.setFont("Helvetica", 10)

    for pel in pelanggarans:
        plat = pel.plate_number if pel.plate_number else "-"
        waktu = pel.waktu.strftime('%d-%m-%Y %H:%M') if pel.waktu else "-"
        lokasi = pel.lokasi or "-"
        p.drawString(2 * cm, y, f"ID: {pel.id_pelanggaran} | Plat: {plat} | Lokasi: {lokasi} | Waktu: {waktu}")
        y -= 1 * cm
        if y <= 2 * cm:
            p.showPage()
            y = height - 2 * cm

    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf', headers={
        'Content-Disposition': 'attachment; filename="histori_pelanggaran.pdf"',
    })

# ✅ Fungsi hapus pelanggaran
def hapus_pelanggaran(request, id):
    pelanggaran = get_object_or_404(Pelanggaran, id_pelanggaran=id)
    pelanggaran.delete()
    return redirect('dashboard')
