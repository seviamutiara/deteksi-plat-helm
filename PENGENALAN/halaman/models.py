from django.db import models

class Pelanggaran(models.Model):
    gambar = models.ImageField(upload_to='pelanggaran/')
    waktu = models.DateTimeField(auto_now_add=True)
    lokasi = models.CharField(max_length=100)
    plat_nomor = models.CharField(max_length=20)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.plat_nomor
