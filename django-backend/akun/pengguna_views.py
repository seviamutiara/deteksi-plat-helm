from django.shortcuts import render
from .models import Pelanggaran, Kendaraan
from .serializers import PelanggaranSerializer

def home(request):
    return render(request, 'pengguna/home.html')
    
def riwayat_pelanggaran_user(request):
    kendaraan_user = Kendaraan.objects.filter(user=request.user)
    plat_user = kendaraan_user.values_list('plat_nomor', flat=True)
    pelanggarans = Pelanggaran.objects.filter(plate_number__in=plat_user, status='Selesai').order_by('-waktu')
    return render(request, 'pengguna/home.html', {'pelanggarans': pelanggarans})

def home(request):
    user = request.user
    if user.is_staff:
        pelanggarans = Pelanggaran.objects.filter(status='Selesai').select_related('kendaraan')
        template = 'halaman/home.html'
    else:
        kendaraan_user = Kendaraan.objects.filter(user=user)
        plat_user = kendaraan_user.values_list('plat_nomor', flat=True)
        pelanggarans = Pelanggaran.objects.filter(
            plate_number__in=plat_user,
            status='Selesai'
        )
        template = 'pengguna/home.html'

    return render(request, template, {'pelanggarans': pelanggarans})