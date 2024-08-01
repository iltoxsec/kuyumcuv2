from django import forms
from django.contrib.auth.models import User
from .models import KuyumcuKullanicilar


class KuyumcuKullanicilarYeniKullaniciForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adı'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Soyadı'}),
        }
    
    def save(self, commit=True):
        user = super(KuyumcuKullanicilarYeniKullaniciForm, self).save(commit=False)
        if not user.username:
            user.username = (user.first_name + user.last_name).lower().replace(' ', '') + str(User.objects.count() + 1)
        if commit:
            user.save()
        return user


class KuyumcuKullanicilarForm(forms.ModelForm):
    tarih = forms.DateTimeField(
        widget=forms.TextInput(attrs={'type': 'date', 'id': 'id_tarih','class': 'form-control'}),
        required=True
    )
    class Meta:
        model = KuyumcuKullanicilar
        fields = ['tip', 'cins', 'miktar', 'milyem_per_cm', 'birim', 'aciklama', 'adet', 'iscilik', 'mm_per_cm','islem_tipi', 'tarih']
        widgets = {
            'tip': forms.TextInput(attrs={'class': 'form-control'}),
            'cins': forms.TextInput(attrs={'class': 'form-control'}),
            'miktar': forms.NumberInput(attrs={'class': 'form-control'}),
            'milyem_per_cm': forms.NumberInput(attrs={'class': 'form-control'}),
            'birim': forms.TextInput(attrs={'class': 'form-control'}),
            'aciklama': forms.TextInput(attrs={'class': 'form-control'}),
            'adet': forms.NumberInput(attrs={'class': 'form-control'}),
            'iscilik': forms.NumberInput(attrs={'class': 'form-control'}),
            'mm_per_cm': forms.NumberInput(attrs={'class': 'form-control'}),
            'islem_tipi': forms.Select(attrs={'class': 'form-control'}),
        }


class KuyumcuFilterForm(forms.ModelForm):
    start_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}))
    
    class Meta:
        model = KuyumcuKullanicilar
        fields = ['tip', 'cins', 'islem_tipi', 'start_date', 'end_date']
        widgets = {
            'tip': forms.TextInput(attrs={'required': False,'class': 'form-control'}),
            'cins': forms.TextInput(attrs={'required': False, 'class': 'form-control'}),
            'islem_tipi': forms.Select(attrs={'required': False, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(KuyumcuFilterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False