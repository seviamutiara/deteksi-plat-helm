from django.urls import path
from . import views, pengguna_views, halaman_views
from .api_views import daftar_plat_terdaftar
from django.urls import path
from . import api_views
from django.urls import path
from . import views

urlpatterns = [
    path('', halaman_views.pelanggaran_list, name='beranda'),  # ✅ Arahkan root ke dashboard

    # AUTENTIKASI
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('lupa-password/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('lupa-password/dikirim/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password-selesai/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # CRUD AKUN
    path('halaman/', views.user_list, name='user_list'),
    path('halaman/tambah/', views.user_create, name='user_create'),
    path('halaman/edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('halaman/hapus/<int:pk>/', views.user_delete, name='user_delete'),

    # Pengguna
    path('pengguna/', views.user_dashboard, name='user_dashboard'),
    path('home/', pengguna_views.home, name='home'),
    
    # Admin dan Data
    path('dashboard/', halaman_views.pelanggaran_list, name='dashboard'),
    path('kendaraan/', halaman_views.kendaraan_list, name='kendaraan_list'),
    path('kendaraan/tambah/', halaman_views.kendaraan_create, name='kendaraan_create'),
    path('history/', halaman_views.histori_pelanggaran, name='history'),
    path('histori/download/', halaman_views.download_histori_pdf, name='download_history_pdf'),
    path('pelanggaran/hapus/<int:id>/', halaman_views.hapus_pelanggaran, name='hapus_pelanggaran'),
    path('dashboard/pelanggaran/<int:id_pelanggaran>/verifikasi/', views.verifikasi_pembayaran, name='verifikasi_pembayaran'),


    # Notifikasi
    path('notifikasi/<int:pelanggaran_id>/kirim/', views.kirim_notifikasi, name='kirim_notifikasi'),
    path('notifikasi/saya/', views.notifikasi_user_view, name='notifikasi'),
    path('pelanggaran/<int:id_pelanggaran>/selesai/', views.tandai_selesai, name='tandai_selesai'),
    path('pelanggaran/<int:id_pelanggaran>/bayar/', views.pengguna_bayar_sanksi, name='pengguna_bayar_sanksi'),


    # API
    path('api/violations/', views.create_violation, name='api_tambah_pelanggaran'),
    path('api/plat-terdaftar/', daftar_plat_terdaftar, name='daftar_plat_terdaftar'),

    path('kendaraan/edit/<int:id>/', halaman_views.kendaraan_edit, name='kendaraan_edit'),
    path('kendaraan/hapus/<int:id>/', halaman_views.kendaraan_delete, name='kendaraan_delete'),


]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
