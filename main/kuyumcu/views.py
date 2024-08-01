from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.db.models import Q
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib import messages


@login_required
def index(request):
    query = request.GET.get('q', '')
    users = User.objects.exclude(id=request.user.id)

    if query:
        users = users.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        )

    kullanicilar = KuyumcuKullanicilar.objects.all()
    altin_verildi_toplam = KuyumcuKullanicilar.objects.filter(islem_tipi='Altın Verildi').aggregate(total=Sum('genel_toplam'))['total'] or 0
    altin_alindi_toplam = KuyumcuKullanicilar.objects.filter(islem_tipi='Altın Alındı!').aggregate(total=Sum('genel_toplam'))['total'] or 0
    
    context = {
        'users': users, 
        'query': query, 
        'kullanicilar': kullanicilar,
        'altin_verildi_toplam': altin_verildi_toplam,
        'altin_alindi_toplam': altin_alindi_toplam,
        'fark': round(Decimal(altin_alindi_toplam) - Decimal(altin_verildi_toplam), 2)
    }

    return render(request, 'kuyumcu/index.html', context)


@login_required
def kullanici_veri_getir(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    filter_form = KuyumcuFilterForm(request.GET or None)
    kuyumcular = KuyumcuKullanicilar.objects.filter(user=user)

    altin_verildi_toplam = kuyumcular.filter(islem_tipi='Altın Verildi').aggregate(total=Sum('genel_toplam'))['total'] or 0
    altin_alindi_toplam = kuyumcular.filter(islem_tipi='Altın Alındı!').aggregate(total=Sum('genel_toplam'))['total'] or 0
    genel_fark = altin_alindi_toplam - altin_verildi_toplam

    if request.GET:
        if filter_form.is_valid():
            if filter_form.cleaned_data['tip']:
                kuyumcular = kuyumcular.filter(tip=filter_form.cleaned_data['tip'])
            if filter_form.cleaned_data['cins']:
                kuyumcular = kuyumcular.filter(cins=filter_form.cleaned_data['cins'])
            if filter_form.cleaned_data['islem_tipi']:
                kuyumcular = kuyumcular.filter(islem_tipi=filter_form.cleaned_data['islem_tipi'])
            if filter_form.cleaned_data['start_date']:
                kuyumcular = kuyumcular.filter(tarih__gte=filter_form.cleaned_data['start_date'])
            if filter_form.cleaned_data['end_date']:
                kuyumcular = kuyumcular.filter(tarih__lte=filter_form.cleaned_data['end_date'])

    context = {
        'filter_form': filter_form,
        'kuyumcular': kuyumcular,
        'user': user,
        'genel_fark': genel_fark
    }
    return render(request, 'kuyumcu/kullanici_veri_getir.html', context)


@login_required
def kullanici_veri_ekle(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = KuyumcuKullanicilarForm(request.POST)
        if form.is_valid():
            kuyumcu_kullanici = form.save(commit=False)
            kuyumcu_kullanici.user = user
            kuyumcu_kullanici.save()
            messages.success(
                request, f"{user.first_name} Kullanıcıya yeni verisi eklendi.")
            return redirect('kuyumcu:kullanici_veri_ekle', user_id=user_id)
    else:
        form = KuyumcuKullanicilarForm()

    filter_form = KuyumcuFilterForm(request.GET or None)
    kuyumcular = KuyumcuKullanicilar.objects.filter(user=user)

    altin_verildi_toplam = kuyumcular.filter(islem_tipi='Altın Verildi').aggregate(total=Sum('genel_toplam'))['total'] or 0
    altin_alindi_toplam = kuyumcular.filter(islem_tipi='Altın Alındı!').aggregate(total=Sum('genel_toplam'))['total'] or 0
    genel_fark = altin_alindi_toplam - altin_verildi_toplam

    if request.GET:
        if filter_form.is_valid():
            if filter_form.cleaned_data['tip']:
                kuyumcular = kuyumcular.filter(tip=filter_form.cleaned_data['tip'])
            if filter_form.cleaned_data['cins']:
                kuyumcular = kuyumcular.filter(cins=filter_form.cleaned_data['cins'])
            if filter_form.cleaned_data['islem_tipi']:
                kuyumcular = kuyumcular.filter(islem_tipi=filter_form.cleaned_data['islem_tipi'])
            if filter_form.cleaned_data['start_date']:
                kuyumcular = kuyumcular.filter(tarih__gte=filter_form.cleaned_data['start_date'])
            if filter_form.cleaned_data['end_date']:
                kuyumcular = kuyumcular.filter(tarih__lte=filter_form.cleaned_data['end_date'])

    context = {
        'form': form,
        'filter_form': filter_form,
        'kuyumcular': kuyumcular,
        'user': user,
        'genel_fark': genel_fark
    }
    return render(request, 'kuyumcu/kullanici_veri_ekle.html', context)

@login_required
def kullanici_veri_duzenle(request, veri_id):
    veri = get_object_or_404(KuyumcuKullanicilar, id=veri_id)
    if request.method == 'POST':
        form = KuyumcuKullanicilarForm(request.POST, instance=veri)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"{veri.user.first_name} Kullanıcı verisi düzenlendi.")
            return redirect('kuyumcu:kullanici_veri_ekle', user_id=veri.user.id)
    else:
        form = KuyumcuKullanicilarForm(instance=veri)
    return render(request, 'kuyumcu/kullanici_veri_duzenle.html', {'form': form, 'veri': veri})

@login_required
def kullanici_veri_sil(request, veri_id):
    veri = get_object_or_404(KuyumcuKullanicilar, id=veri_id)
    user_id = veri.user.id
    veri.delete()
    messages.success(
                request, f"{veri.user.first_name} Kullanıcı verisi silindi.")
    return redirect('kuyumcu:kullanici_veri_ekle', user_id=user_id)