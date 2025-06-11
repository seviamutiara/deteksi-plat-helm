from django.urls import path
from . import views,pengguna_views,halaman_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/dashboard/', views.admin_dashboard, name='halaman_dashboard'),  
    path('pengguna/', views.user_dashboard, name='home'),  

    #CRUD Akun
    path('akun/', views.user_list, name='user_list'),
    path('akun/tambah/',views.user_create, name='user_create'),
    path('akun/edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('akun/hapus/<int:pk>/', views.user_delete, name='user_delete'),    

    # pengguna
    path('home', pengguna_views.home, name='home'),
    path('rambu', pengguna_views.rambu, name='rambu'),
    path('marka', pengguna_views.marka, name='marka'),
    path('pelanggaran', pengguna_views.pelanggaran, name='pelanggaran'),
    path('artikel', pengguna_views.artikel, name='artikel'),
    path('tata_cara', pengguna_views.tata_cara, name='tata_cara'),
    path('kuis', pengguna_views.kuis, name='kuis'), 

    # halaman admin
    path('dashboard/', halaman_views.dashboard_view, name='dashboard'),
    path('history/', halaman_views.histori_pelanggaran, name='history'),
]