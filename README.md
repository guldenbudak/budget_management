# Bütçe Takip — Ev ve Bireysel Gelir-Gider Takibi

Django ile yazılmış, hem kişisel hem de ev (ortak) bütçesi tutmaya yarayan bir gelir-gider
takip uygulaması. Her kullanıcı kendi kişisel bütçesini görür; isteyen bir "Ev" bütçesi açıp
davet koduyla başkalarını (ev arkadaşı, eş, aile) aynı bütçeye dahil edebilir.

---

## Kurulum

```bash
# 1. Depoyu klonla
git clone <repo-adresi>
cd budget_management

# 2. Sanal ortam oluştur ve etkinleştir
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Bağımlılıkları kur
pip install -r requirements.txt

# 4. Ortam değişkenlerini ayarla
cp .env.example .env
# .env dosyasını açıp SECRET_KEY değerini doldur. Yeni key üretmek için:
#   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 5. Veritabanını oluştur
python manage.py migrate

# 6. Yönetici hesabı aç (admin paneline girmek için)
python manage.py createsuperuser

# 7. Sunucuyu başlat
python manage.py runserver
```

Uygulama: http://127.0.0.1:8000/ · Admin paneli: http://127.0.0.1:8000/admin/

### Ortam değişkenleri

| Değişken | Açıklama | Örnek |
|---|---|---|
| `SECRET_KEY` | Django'nun kriptografik imzalama anahtarı. Gizli tutulmalı, repoya girmez. | `snk@$#9i9...` |
| `DEBUG` | Geliştirme modu. `.env`'den metin geldiği için `== 'True'` ile bool'a çevriliyor. | `True` |

---

## Veri Modeli

<!-- TODO (Aşama 2): Şema ve alan tabloları buraya -->

---

## Soruların Cevapları

<!-- TODO: Ödevde "Soru (README)" işaretli maddeler -->

### Neden her şeyi tek app'e değil de `accounts` ve `finance` diye ikiye ayırdık?

<!-- TODO (Aşama 0) -->

### `category` alanında `on_delete` olarak ne seçtin? Bir kategoriyi silince eski harcamalar ne olmalı?

<!-- TODO (Aşama 2) -->

### Başkasının bütçesine erişimde neden 403 değil de 404 döndürüyoruz?

<!-- TODO (Aşama 3) -->

### Üyelik durumları: zaten üye olan kodu tekrar girerse / yanlış kod / ayrılan kişinin işlemleri

<!-- TODO (Aşama 4) -->

---

## Ekran Görüntüleri

<!-- TODO: kayıt, dashboard, bütçe detayı, ev bütçesi üyeleri -->

---

## Testler

```bash
python manage.py test
```

<!-- TODO (Aşama 6): hangi testler var, ne kontrol ediyorlar -->
