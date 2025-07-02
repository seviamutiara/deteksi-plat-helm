from rest_framework import serializers
from .models import Pelanggaran

class PelanggaranSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelanggaran
        fields = '__all__'
