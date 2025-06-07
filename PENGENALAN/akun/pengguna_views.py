from django.shortcuts import render
from datetime import datetime

def home(request):
    return render(request, 'pengguna/home.html')

def rambu(request):
    rambu_list = [
        "Rambu Stop", "Rambu Dilarang Masuk", "Rambu Belok Kiri", "Rambu Pejalan Kaki"
    ]
    return render(request, 'pengguna/rambu.html', {'rambu_list': rambu_list})

def marka(request):
    marka_list = [
        "Marka Garis Putih", "Marka Zebra Cross", "Marka Panah", "Marka Bus Lane"
    ]
    return render(request, 'pengguna/marka.html', {'marka_list': marka_list})

def pelanggaran(request):
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
    return render(request, 'pengguna/pelanggaran.html', {'pelanggarans': pelanggarans})

def artikel(request):
    artikel_list = [
        {"judul": "Tips Berkendara Aman di Kota", "penulis": "Admin", "tanggal": "1 Juni 2025"},
        {"judul": "Pentingnya Mematuhi Rambu Lalu Lintas", "penulis": "Admin", "tanggal": "3 Juni 2025"},
    ]
    return render(request, 'pengguna/artikel.html', {'artikel_list': artikel_list})

def tata_cara(request):
    tata_cara_steps = [
        "Periksa kendaraan sebelum berkendara",
        "Gunakan helm dan perlengkapan keselamatan",
        "Patuhi rambu-rambu lalu lintas",
        "Jangan menggunakan ponsel saat berkendara",
        "Jaga jarak aman dengan kendaraan lain",
    ]
    return render(request, 'pengguna/tata_cara.html', {'tata_cara_steps': tata_cara_steps})

def kuis(request):
    kuis = {
        "pertanyaan": "Apa arti rambu stop?",
        "pilihan": ["Berhenti", "Berjalan", "Belok kiri", "Dilarang masuk"],
        "jawaban": "Berhenti"
    }
    return render(request, 'pengguna/kuis.html', {'kuis': kuis})
