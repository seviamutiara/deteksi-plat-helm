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


def artikel(request):
    artikel_list = [
        {
            "judul": "Tips Berkendara Aman di Kota",
            "penulis": "Admin",
            "tanggal": datetime(2025, 6, 1),
            "isi": "Berkendara di kota memerlukan kewaspadaan ekstra. Gunakan sabuk pengaman, patuhi batas kecepatan, dan hindari penggunaan ponsel saat menyetir.",
            "gambar": "tips_aman.png"
        },
        {
            "judul": "Pentingnya Mematuhi Rambu Lalu Lintas",
            "penulis": "Admin",
            "tanggal": datetime(2025, 6, 3),
            "isi": "Rambu lalu lintas dibuat untuk menjaga keselamatan pengendara dan pejalan kaki. Mengabaikannya dapat menyebabkan kecelakaan fatal.",
            "gambar": "rambu_lalin.png"
        },
    ]

    context = {
        "judul_halaman": "Daftar Artikel Edukasi",
        "artikel_list": artikel_list
    }
    return render(request, 'pengguna/artikel.html', context)

def tata_cara(request):
    tata_cara_steps = [
        "Periksa kendaraan sebelum berkendara",
        "Gunakan helm dan perlengkapan keselamatan",
        "Patuhi rambu-rambu lalu lintas",
        "Jangan menggunakan ponsel saat berkendara",
        "Jaga jarak aman dengan kendaraan lain",
    ]
    return render(request, 'pengguna/tata_cara.html', {'tata_cara_steps': tata_cara_steps})
