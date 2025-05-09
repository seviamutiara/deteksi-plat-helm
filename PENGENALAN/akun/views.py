from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect ke halaman yang diinginkan setelah login berhasil
                return redirect('halaman/dashboard')  # Ganti 'halaman_beranda' dengan nama URL Anda
            else:
                # Tampilkan pesan error jika autentikasi gagal
                return render(request, 'akun/login.html', {'form': form, 'error': 'Username atau password salah.'})
        else:
            # Tampilkan form dengan error jika tidak valid
            return render(request, 'akun/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'akun/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    # Redirect ke halaman setelah logout (misalnya, halaman login lagi)
    return redirect('login')