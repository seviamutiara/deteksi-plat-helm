from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'no_hp', 'alamat')

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('role') == 'admin':
            user.is_staff = True
            user.is_superuser = True
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'no_hp', 'alamat')
