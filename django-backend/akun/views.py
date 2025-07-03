from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import views as auth_views
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import Pelanggaran, Notifikasi, Kendaraan, User
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Role check decorator
def admin_required(view_func):
    @login_required(login_url='login')
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped_view

def user_required(view_func):
    @login_required(login_url='login')
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'user':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped_view

# Login & Logout
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard' if request.user.role == 'admin' else 'home')

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user:
            login(request, user)
            return redirect('dashboard' if user.role == 'admin' else 'home')
        messages.error(request, 'Username atau password salah.')

    return render(request, 'akun/login.html', {'form': form})

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, 'Berhasil logout.')
    return redirect('login')

# Dashboard
@admin_required
def admin_dashboard(request):
    return render(request, 'halaman/dashboard.html')

@user_required
def user_dashboard(request):
    return render(request, 'pengguna/home.html')

# Reset password views
class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'akun/lupa_password.html'
    email_template_name = 'akun/email_reset_password.html'
    subject_template_name = 'akun/subject_reset_password.txt'

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'akun/lupa_password_dikirim.html'

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'akun/reset_password_konfirmasi.html'

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'akun/reset_password_selesai.html'

# Kelola pengguna
@admin_required
def user_list(request):
    users = User.objects.all().order_by('-id')
    return render(request, 'halaman/user_list.html', {'users': users})

@admin_required
def user_create(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.is_staff = True if user.role == 'admin' else False
        user.save()
        messages.success(request, 'Akun berhasil dibuat.')
        return redirect('user_list')
    return render(request, 'halaman/user_form.html', {'form': form, 'title': 'Tambah Akun'})

@admin_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = CustomUserChangeForm(request.POST or None, instance=user)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.is_staff = True if user.role == 'admin' else False
        user.save()
        return redirect('user_list')
    return render(request, 'halaman/user_form.html', {'form': form, 'title': 'Edit Akun'})

@admin_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Akun berhasil dihapus.')
        return redirect('user_list')
    return render(request, 'halaman/user_confirm_delete.html', {'user': user})

# Notifikasi
@login_required
def kirim_notifikasi(request, pelanggaran_id):
    pelanggaran = get_object_or_404(Pelanggaran, id_pelanggaran=pelanggaran_id)
    admin = request.user
    kendaraan = Kendaraan.objects.filter(plat_nomor=pelanggaran.plate_number).first()

    if kendaraan and kendaraan.user:
        pengguna = kendaraan.user
        subject = "Notifikasi Pelanggaran Lalu Lintas"
        message = f"""
        Halo {pengguna.username},

        Anda telah melakukan pelanggaran lalu lintas:
        - Lokasi: {pelanggaran.lokasi}
        - Waktu: {pelanggaran.waktu.strftime('%d-%m-%Y %H:%M')}
        - Plat Nomor: {pelanggaran.plate_number}

        Silakan tindak lanjuti pelanggaran Anda.

        Terima kasih,
        Kamera Pintar
        """
        send_mail(subject, message, 'vikraselpian@gmail.com', [pengguna.email])
        Notifikasi.objects.create(
            user=pengguna,
            pelanggaran=pelanggaran,
            admin=admin,
            metode='Email',
            tanggal_kirim=timezone.now(),
            status_baca=False
        )
        pelanggaran.status = "Ditindak"
        pelanggaran.save()
    else:
        messages.warning(request, "Kendaraan tidak ditemukan atau tidak memiliki pengguna.")

    return redirect('dashboard')

@login_required
def tandai_selesai(request, pelanggaran_id):
    pelanggaran = get_object_or_404(Pelanggaran, id_pelanggaran=pelanggaran_id)
    pelanggaran.status = "Selesai"
    pelanggaran.save()
    return redirect('dashboard')

@login_required
def notifikasi_user_view(request):
    notifikasi = Notifikasi.objects.filter(user=request.user).order_by('-tanggal_kirim')
    return render(request, 'pengguna/notifikasi.html', {'notifikasi': notifikasi})

# === API ENDPOINT ===
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PelanggaranSerializer

@api_view(['POST'])
def api_tambah_pelanggaran(request):
    data = request.data
    plat = data.get("plate_number")
    kendaraan = Kendaraan.objects.filter(plat_nomor=plat).first()

    pelanggaran = Pelanggaran.objects.create(
        plate_number=plat,
        kendaraan=kendaraan,
        confidence=data.get("confidence", 0.0),
        image_base64=data.get("image_base64", ""),
        waktu=data.get("waktu"),
        lokasi=data.get("lokasi", "Tidak diketahui"),
        status=data.get("status", "Belum Ditindak"),
        kamera=None  # Tambahkan logika kamera jika perlu
    )

    return Response({'message': 'Pelanggaran berhasil disimpan.'})

@api_view(['GET'])
def daftar_plat_terdaftar(request):
    plat_list = list(Kendaraan.objects.values_list('plat_nomor', flat=True))
    return JsonResponse({"plat_terdaftar": plat_list})

# Riwayat pelanggaran pengguna
@login_required
def riwayat_pelanggaran_user(request):
    kendaraan_user = Kendaraan.objects.filter(user=request.user)
    plat_user = kendaraan_user.values_list('plat_nomor', flat=True)
    pelanggarans = Pelanggaran.objects.filter(
        plate_number__in=plat_user,
        status='Selesai'
    ).order_by('-waktu')
    return render(request, 'pengguna/history_pengguna.html', {'pelanggarans': pelanggarans})

@login_required
@user_required
def pengguna_bayar_sanksi(request, pelanggaran_id):
    pelanggaran = get_object_or_404(Pelanggaran, id_pelanggaran=pelanggaran_id)

    # Validasi bahwa pelanggaran ini milik user
    kendaraan_user = Kendaraan.objects.filter(user=request.user)
    if not kendaraan_user.filter(plat_nomor=pelanggaran.plate_number).exists():
        raise PermissionDenied("Pelanggaran ini bukan milik Anda.")

    # Update status
    pelanggaran.status = "Selesai"
    pelanggaran.save()

    messages.success(request, "Terima kasih, pelanggaran telah diselesaikan.")
    return redirect('notifikasi')  # arahkan ke riwayat atau notifikasi user
