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