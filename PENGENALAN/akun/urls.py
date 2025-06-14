from django.urls import path
from . import views,pengguna_views,halaman_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'), 

    #CRUD Akun
    path('halaman/', views.user_list, name='user_list'),
    path('halaman/tambah/',views.user_create, name='user_create'),
    path('halaman/edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('halaman/hapus/<int:pk>/', views.user_delete, name='user_delete'),    

    # pengguna
    path('pengguna/', views.user_dashboard, name='home'),  
    path('home', pengguna_views.home, name='home'),
    path('rambu', pengguna_views.rambu, name='rambu'),
    path('marka', pengguna_views.marka, name='marka'),
    path('history/', halaman_views.histori_pelanggaran, name='history_pengguna'),
    path('artikel', pengguna_views.artikel, name='artikel'),
    path('tata_cara', pengguna_views.tata_cara, name='tata_cara'), 

    # halaman admin
    path('halaman/dashboard/', views.admin_dashboard, name='dashboard'),  
    path('dashboard/', halaman_views.pelanggaran_list, name='dashboard'),
    path('notifikasi/<int:pelanggaran_id>/kirim/', views.kirim_notifikasi, name='kirim_notifikasi'),
    path('notifikasi/saya/', views.notifikasi_user_view, name='notifikasi'),
    path('pelanggaran/<int:pelanggaran_id>/selesai/', views.tandai_selesai, name='tandai_selesai'),
    path('kendaraan', halaman_views.kendaraan_list, name='kendaraan_list'),
    path('history/', halaman_views.histori_pelanggaran, name='history'),
    path('histori/download/', halaman_views.download_histori_pdf, name='download_history_pdf'),
]