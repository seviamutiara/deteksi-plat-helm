# middleware/block_non_admin.py
from django.shortcuts import redirect
from django.urls import reverse

class BlockNonAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        admin_only_paths = [
            '/akun/akun/',               
            '/akun/akun/tambah/',
            '/akun/akun/edit/',
            '/akun/dashboard/',
        ]

        if any(request.path.startswith(path) for path in admin_only_paths):
            if not request.user.is_authenticated or request.user.role != 'admin':
                return redirect(reverse('home'))  # arahkan kembali ke halaman aman

        return self.get_response(request)
