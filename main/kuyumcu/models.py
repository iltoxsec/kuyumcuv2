from django.db import models
from decimal import Decimal, ROUND_DOWN


class KuyumcuKullanicilar(models.Model):
    STATUS = [
        ('Altın Verildi', 'Altın Verildi'),
        ('Altın Alındı!', 'Altın Alındı!'),
        ('İşlem Yok', 'İşlem Yok'),
        ('', '---------'),
    ]
    user = models.ForeignKey('auth.User', verbose_name='Author',
                             related_name='kuyumcu_kullanicilar', on_delete=models.CASCADE)
    tip = models.CharField(max_length=100)
    cins = models.CharField(max_length=100)
    miktar = models.DecimalField(max_digits=10, decimal_places=2)
    milyem_per_cm = models.DecimalField(max_digits=10, decimal_places=3)
    birim = models.CharField(max_length=10)
    alt_toplam = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    aciklama = models.TextField()
    adet = models.IntegerField()
    iscilik = models.DecimalField(max_digits=10, decimal_places=2)
    mm_per_cm = models.CharField(max_length=10)
    isc_toplam = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    islem_tipi = models.CharField(default="", choices=STATUS, max_length=30)
    tarih = models.DateTimeField(
        verbose_name="Tarih")
    genel_toplam = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    fark = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0.00)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.alt_toplam = round(float(self.miktar) * float(self.milyem_per_cm), 2)
        self.isc_toplam = round(float(self.miktar) * float(self.iscilik), 2)
        self.genel_toplam = round(self.alt_toplam + self.isc_toplam, 2)

        altin_verildi_toplam = KuyumcuKullanicilar.objects.filter(islem_tipi='Altın verildi').aggregate(total=models.Sum('genel_toplam'))['total'] or 0
        altin_alindi_toplam = KuyumcuKullanicilar.objects.filter(islem_tipi='Altın Alındı!').aggregate(total=models.Sum('genel_toplam'))['total'] or 0

        self.fark = round(Decimal(altin_alindi_toplam) - Decimal(altin_verildi_toplam), 2)
        
        super().save(*args, **kwargs)

    def round_value(self, value):
        return value.quantize(Decimal('0.0001'), rounding=ROUND_DOWN)

    def __str__(self):
        return f"{self.user} - {self.tip} - {self.cins}"
