# akun/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages

# Decorator kustom untuk admin-only
def admin_required(view_func):
    @login_required(login_url='login')
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        # Kalau user sudah login tapi bukan admin, tampilkan 403
        raise PermissionDenied
    return _wrapped_view

# Decorator kustom untuk user-only
def user_required(view_func):
    @login_required(login_url='login')
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'user':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped_view

def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('dashboard')
        elif request.user.role == 'user':
            return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('dashboard' if user.role == 'admin' else 'home')
        messages.error(request, 'Username atau password salah.')
    else:
        form = AuthenticationForm()

    return render(request, 'akun/login.html', {'form': form})

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, 'Berhasil logout.')
    return redirect('login')

@admin_required
def admin_dashboard(request):
    return render(request, 'halaman/dashboard.html')

@user_required
def user_dashboard(request):
    return render(request, 'pengguna/home.html')
