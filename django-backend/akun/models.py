from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    no_hp = models.CharField(max_length=20, blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)

class Kendaraan(models.Model):
    id_kendaraan = models.AutoField(primary_key=True)
    plat_nomor = models.CharField(max_length=15)
    jenis_kendaraan = models.CharField(max_length=50)
    foto_kendaraan = models.ImageField(upload_to='kendaraan/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.plat_nomor

class Kamera(models.Model):
    nama = models.CharField(max_length=100)
    lokasi = models.CharField(max_length=200)
    status = models.CharField(
        max_length=10,
        choices=[('Aktif', 'Aktif'), ('Nonaktif', 'Nonaktif')],
        default='Aktif'
    )
    waktu_ditambahkan = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nama} - {self.lokasi} ({self.status})"

class Pelanggaran(models.Model):
    id_pelanggaran = models.AutoField(primary_key=True)
    kendaraan = models.ForeignKey(Kendaraan, on_delete=models.SET_NULL, null=True, blank=True)
    plate_number = models.CharField(max_length=20, default='UNKNOWN')
    confidence = models.FloatField(default=0.0)
    image_base64 = models.TextField(default='')
    waktu = models.DateTimeField()
    lokasi = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=[
        ('Belum Ditindak', 'Belum Ditindak'),
        ('Ditindak', 'Ditindak'),
        ('Selesai', 'Selesai'),
    ], default='Belum Ditindak')
    kamera = models.ForeignKey(Kamera, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Pelanggaran {self.id_pelanggaran} - {self.plate_number}"

class Notifikasi(models.Model):
    notif_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifikasi_user')
    pelanggaran = models.ForeignKey(Pelanggaran, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifikasi_admin')
    status_baca = models.BooleanField(default=False)
    metode = models.CharField(max_length=50)
    tanggal_kirim = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notifikasi {self.notif_id}"
