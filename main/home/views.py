from django.shortcuts import render
from kuyumcu.models import KuyumcuKullanicilar
from django.db.models import Sum
from decimal import Decimal
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    users = User.objects.exclude(id=request.user.id)

    kullanicilar = KuyumcuKullanicilar.objects.all()
    altin_verildi_toplam = KuyumcuKullanicilar.objects.filter(islem_tipi='Altın Verildi').aggregate(total=Sum('genel_toplam'))['total'] or 0
    altin_alindi_toplam = KuyumcuKullanicilar.objects.filter(islem_tipi='Altın Alındı!').aggregate(total=Sum('genel_toplam'))['total'] or 0
    
    context = {
        'users': users,
        'kullanicilar': kullanicilar,
        'altin_verildi_toplam': altin_verildi_toplam,
        'altin_alindi_toplam': altin_alindi_toplam,
        'fark': round(Decimal(altin_alindi_toplam) - Decimal(altin_verildi_toplam), 2)
    }
    return render(request, 'home/index.html', context)