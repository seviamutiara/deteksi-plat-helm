from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

# Login View
def login_view(request):
    if request.user.is_authenticated:
        # Redirect langsung jika sudah login
        if request.user.role == 'admin':
            return redirect('admin_dashboard')
        elif request.user.role == 'user':
            return redirect('user_dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect berdasarkan role
                if user.role == 'admin':
                    return redirect('halaman_dashboard')
                elif user.role == 'user':
                    return redirect('pengguna_dashboard')
                else:
                    messages.error(request, 'Role tidak dikenali.')
                    logout(request)
                    return redirect('login')
            else:
                messages.error(request, 'Username atau password salah.')
        else:
            messages.error(request, 'Form tidak valid.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'akun/login.html', {'form': form})


# Logout View
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Berhasil logout.')
    return redirect('login')


# Dashboard untuk Admin
@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Anda tidak memiliki akses ke halaman ini.")
    # Ganti konten di bawah sesuai tampilan dashboard admin
    return render(request, 'akun/halaman_dashboard.html')


# Dashboard untuk User
@login_required
def user_dashboard(request):
    if request.user.role != 'user':
        return HttpResponseForbidden("Anda tidak memiliki akses ke halaman ini.")
    # Ganti konten di bawah sesuai tampilan dashboard user
    return render(request, 'akun/pengguna_home.html')
