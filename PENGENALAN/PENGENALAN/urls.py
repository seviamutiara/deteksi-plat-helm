from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('akun/', include('akun.urls')),
    path('', lambda request: redirect('login'), name='halaman/dashboard'),
    
]
