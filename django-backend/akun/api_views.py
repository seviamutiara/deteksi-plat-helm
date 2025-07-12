from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Kendaraan, Pelanggaran
from .serializers import PelanggaranSerializer

@api_view(['GET'])
def daftar_plat_terdaftar(request):
    plat_list = list(Kendaraan.objects.values_list('plat_nomor', flat=True))
    return Response({'plat_terdaftar': plat_list})

@api_view(['POST'])
def violations_create(request):
    serializer = PelanggaranSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
