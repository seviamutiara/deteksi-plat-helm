from django.shortcuts import render

def dashboard_view(request):
    pelanggarans = [  # Data dummy, tidak akses database
        {
            'gambar': 'dashboard/img/sample1.jpg',
            'waktu': '2025-05-03 08:00',
            'lokasi': 'Jl. Merdeka',
            'plat_nomor': 'B 1234 CD',
            'status': 'Belum Ditindak',
        },
        {
            'gambar': 'dashboard/img/sample2.jpg',
            'waktu': '2025-05-03 09:30',
            'lokasi': 'Jl. Sudirman',
            'plat_nomor': 'D 5678 EF',
            'status': 'Selesai',
        },
    ]
    return render(request, 'dashboard/dashboard.html', {'pelanggarans': pelanggarans})
