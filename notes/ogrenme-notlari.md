# Öğrenme Notları

Bu dosyayı **ben** (Gülden) dolduruyorum. Kural: her takıldığım hatayı buraya,
**kendi cümlelerimle** yazıyorum. Kopyala-yapıştır açıklama yok — kendi kelimelerime
çeviremiyorsam zaten anlamamışım demektir.

Şablon:

```
## <tarih> — <hatanın kısa adı>

**Ne oldu:** (hata mesajının son satırı)
**Neden oldu:** (kendi cümlelerimle)
**Nasıl çözdüm:** (ne değiştirdim)
**Ders:** (bir daha nasıl fark ederim)
```

---

## Aşama 0 soruları (kendim cevaplayacağım)

1. Kullanıcı `/transactions/add/` adresine gidince önce ____ dosyası, sonra ____
   fonksiyonu, sonra ____ template'i çalışır.

2. `makemigrations` ile `migrate` arasındaki fark nedir? Hangisi veritabanına dokunur?

3. `DEBUG = os.getenv('DEBUG')` yazsam ne olurdu? Neden `== 'True'` gerekiyor?

---

<!-- Notlar buradan aşağı eklenecek -->

SET-NULL : kullanma sebebim ali hesabını silebilir ama
harcamaları kaybolmamalı neden harcamalar kaybolursa
sonradan sıkıntı oluşur harcama nerden yapıldı bulamayız.

null=True → veritabanı boş kabul eder
blank=True → form boş bırakmaya izin verir

Ne zaman
list_filter Alanın değerleri sayılı ise: tür, bütçe, durum, rol
search_fields Alan serbest metin ise: açıklama, isim, e-posta
HTML her şeyi metin olarak gönderir. Tarayıcı sayı diye bir şey bilmez, tarih diye bir şey bilmez — hepsi yazı.

Django bu yazıları gerçek Python değerlerine çeviriyor. Sonuç cleaned_data'ya yazılıyor.

super().clean() Django'ya diyor ki: "bu formu doğrularken o kuralları da kontrol et."

403 - 404 farkı nerde ne kullanıyoruz.
403 : kullanıcı giriş yapmış görebiliyor bütçeyi değerleri
bir değişiklik yapmak istedi ama yetkisi yok çünkü ekleyen o
değil bütçe sahibi o değil bu gibi durumlarda 403 hatası alır
veri var ama düzenleme yetkin yok.

404 : bu hata türünde ise kullanıcı giriş yapmamış urlden
deniyor olabilir bilmiyoruz bilgi vermemiz güvenlik
açısından zararlı olduğu için böyle bir veri yok diyoruz
değiştirmek istediği kısım için .
