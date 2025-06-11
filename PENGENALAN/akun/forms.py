from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.hashers import make_password
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'no_hp', 'alamat', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('role') == 'admin':
            user.is_staff = True
            user.is_superuser = True
        else:
           user.is_staff = False
           user.is_superuser = False
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password Baru (Opsional)',
        widget=forms.PasswordInput,
        required=False
    )
    password2 = forms.CharField(
        label='Konfirmasi Password',
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'no_hp', 'alamat')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Password tidak cocok.")
            if len(password1) < 8:
                raise forms.ValidationError("Password harus minimal 8 karakter.")
            if password1.lower() in ['password', '12345678', 'admin']:
                raise forms.ValidationError("Password terlalu umum.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.password = make_password(password)
        if commit:
            user.save()
        return user
