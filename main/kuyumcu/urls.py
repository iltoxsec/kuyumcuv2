from django.urls import path
from .views import *


app_name = "kuyumcu"

urlpatterns = [
    path('', index,name="index"),

    path('kullanici-veri-getir/<int:user_id>/', kullanici_veri_getir, name="kullanici_veri_getir"),
    path('kullanici-veri-ekle/<int:user_id>/', kullanici_veri_ekle, name="kullanici_veri_ekle"),
    path('kullanici-veri-duzenle/<int:veri_id>/', kullanici_veri_duzenle, name="kullanici_veri_duzenle"),
    path('kullanici-veri-sil/<int:veri_id>/', kullanici_veri_sil, name="kullanici_veri_sil"),

]
