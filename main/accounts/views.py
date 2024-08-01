from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def index(request):
    query = request.GET.get('q', '')
    order_by = request.GET.get('order_by', 'date_joined')
    direction = request.GET.get('direction', 'asc')

    users = User.objects.exclude(id=request.user.id)

    if query:
        users = users.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        )

    if direction == 'desc':
        order_by = '-' + order_by

    users = users.order_by(order_by)

    context = {
        'users': users, 
        'query': query, 
        'order_by': order_by, 
        'direction': direction
    }

    return render(request, 'accounts/index.html', context)

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(
                request, f"{request.user.first_name} Hoşgeldiniz.")
            return redirect("home:index")
        else:
            return render(request, "accounts/login.html", {
                "error": "Check your username or password!"
            })
    return render(request, 'accounts/login.html')

@login_required
def userProfile(request):
    return render(request, 'accounts/profile.html')

@login_required
def updateUserProfile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profiliniz güncellendi!')
            return redirect('accounts:userProfile')
        else:
            return render(request, 'accounts/update_profile.html', {'form': user_form})

    user_form = UserUpdateForm(instance=request.user)
    return render(request, 'accounts/update_profile.html', {'form': user_form})

@login_required 
def changeUserPassword(request):

    form = ChangeUserPasswordForm(data=request.POST, user=request.user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            user = authenticate(request, username=request.user.username, password=form.new_password2)
            login(request, user)
            messages.success(
                request, 'Parolanız başarıyla güncellendi.')
            return redirect("accounts:userProfile")

    context = {
        'form': form
    }
    return render(request, 'accounts/change_password.html', context)

@login_required
def logoutView(request):
    logout(request)
    messages.success(
                request, f"Çıkış Yapıldı!")
    return redirect("accounts:user_login")




@login_required
def kuyumcu_kullanici_add(request):
    if request.method == 'POST':
        form = KuyumcuKullanicilarYeniKullaniciForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.success(request, "Kullanıcı eklendi.")
            return redirect('kuyumcu:kullanici_veri_ekle', user_id=new_user.id)
            
    else:
        form = KuyumcuKullanicilarYeniKullaniciForm()
        users = User.objects.exclude(id=request.user.id)
    
    context = {
        'users': users,
        'form': form
    }
    return render(request, 'accounts/kullanici_add.html', context)

@login_required
def kuyumcu_kullanici_duzenle(request,user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = KuyumcuKullanicilarYeniKullaniciForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"{user.first_name} adlı kullanıcı düzenlendi")
            return redirect('kuyumcu:kullanici_veri_getir', user_id=user.id)
        
    else:
        form = KuyumcuKullanicilarYeniKullaniciForm(instance=user)
        users = User.objects.exclude(id=request.user.id)
    
    context = {
        'users': users,
        'user': user,
        'form': form
    }
    return render(request, 'accounts/kullanici_duzenle.html', context)

@login_required
def kullanici_sil(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(
                request, "Hesap Başarıyla silindi.")
    return redirect('accounts:index')

