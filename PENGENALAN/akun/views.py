from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Decorator kustom untuk admin-only
def admin_required(view_func):
    @login_required(login_url='login')
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
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

# ============================
# CRUD Akun Login (Admin Only)
# ============================

@admin_required
def user_list(request):
    users = User.objects.all().order_by('-id')
    return render(request, 'akun/user_list.html', {'users': users})

@admin_required
def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun berhasil dibuat.')
            return redirect('user_list')
        else:
            print("❌ Form errors:", form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'akun/user_form.html', {'form': form, 'title': 'Tambah Akun'})

@admin_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, 'akun/user_form.html', {'form': form, 'title': 'Edit Akun'})

@admin_required
def user_delete(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Akun berhasil dihapus.')
        return redirect('user_list')
    return render(request, 'akun/user_confirm_delete.html', {'user': user})
