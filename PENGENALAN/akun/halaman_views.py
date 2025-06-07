from django.shortcuts import render
from datetime import datetime

def dashboard_view(request):
    # Data dummy
    pelanggarans = [
        {
            'id_pelanggaran': 1,
            'bukti_gambar': {'url': '/media/dashboard/img/sample1.jpg'},
            'waktu': datetime.strptime('2025-05-03 08:00', '%Y-%m-%d %H:%M'),
            'lokasi': 'Jl. Merdeka',
            'status': 'Belum Ditindak',
            'kendaraan': {'plat_nomor': 'B 1234 CD'},
        },
        {
            'id_pelanggaran': 2,
            'bukti_gambar': {'url': '/media/dashboard/img/sample2.jpg'},
            'waktu': datetime.strptime('2025-05-03 09:30', '%Y-%m-%d %H:%M'),
            'lokasi': 'Jl. Sudirman',
            'status': 'Selesai',
            'kendaraan': {'plat_nomor': 'D 5678 EF'},
        },
    ]

    # Hitung statistik dari data dummy
    total_today = len(pelanggarans)
    ditindak = sum(1 for p in pelanggarans if p['status'] == 'Ditindak')
    selesai = sum(1 for p in pelanggarans if p['status'] == 'Selesai')

    # Dummy lokasi kamera aktif
    kamera_aktif = 3  # misal 3 kamera aktif secara statis

    context = {
        'pelanggarans': pelanggarans,
        'total_today': total_today,
        'ditindak': ditindak,
        'selesai': selesai,
        'kamera_aktif': kamera_aktif,
    }

    return render(request, 'halaman/dashboard.html', context)

def histori_pelanggaran(request):
    pelanggarans = [
        {
            'id_pelanggaran': 1,
            'bukti_gambar': {'url': '/media/dashboard/img/sample1.jpg'},
            'waktu': datetime.strptime('2025-05-03 08:00', '%Y-%m-%d %H:%M'),
            'lokasi': 'Jl. Merdeka',
            'status': 'Belum Ditindak',
            'kendaraan': {'plat_nomor': 'B 1234 CD'},
        },
        {
            'id_pelanggaran': 2,
            'bukti_gambar': {'url': '/media/dashboard/img/sample2.jpg'},
            'waktu': datetime.strptime('2025-05-03 09:30', '%Y-%m-%d %H:%M'),
            'lokasi': 'Jl. Sudirman',
            'status': 'Selesai',
            'kendaraan': {'plat_nomor': 'D 5678 EF'},
        },
    ]

    return render(request, 'halaman/history.html', {'pelanggarans': pelanggarans})
