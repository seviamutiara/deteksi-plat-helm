from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Kamera, Pelanggaran, Kendaraan, Notifikasi
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'no_hp', 'alamat')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'no_hp', 'alamat')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Kendaraan)
admin.site.register(Kamera)
admin.site.register(Pelanggaran)
admin.site.register(Notifikasi)
