from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Kendaraan

@api_view(['GET'])
def daftar_plat_terdaftar(request):
    plat_list = list(Kendaraan.objects.values_list('plat_nomor', flat=True))
    return Response({'plat_terdaftar': plat_list})
