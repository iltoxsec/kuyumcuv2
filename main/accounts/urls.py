from django.urls import path
from .views import *


app_name = "accounts"
urlpatterns = [
    path('', index,name="index"),
    path('login/', user_login, name="user_login"),
    path("logout/", logoutView, name="logout"),

    path("profile/", userProfile, name="userProfile"),
    path("update/profile/", updateUserProfile, name="updateUserProfile"),
    path("change/password/", changeUserPassword, name="changeUserPassword"),
    
    path('kullanici-ekle/', kuyumcu_kullanici_add, name="kuyumcu_kullanici_add"),
    path('kullanici-duzenle/<int:user_id>', kuyumcu_kullanici_duzenle, name="user_update"),
    path('kullanici-sil/<int:user_id>', kullanici_sil, name="user_delete"),
]
