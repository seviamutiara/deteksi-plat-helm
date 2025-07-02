from django.shortcuts import redirect , reverse

class BlockNonStaffAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_paths = [                      
            '/akun/akun/',               
            '/akun/akun/tambah/',
            '/akun/akun/edit/',
            '/akun/dashboard/',
        ]

        for path in protected_paths:
            if request.path.startswith(path):
                if not request.user.is_authenticated or request.user.role != 'admin':
                    return redirect(reverse('dashboard'))

        return self.get_response(request)
