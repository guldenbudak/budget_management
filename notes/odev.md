# Django Ödevi: Ev ve Bireysel Gelir-Gider Takibi

> 28 Eki 2026 · @HAKAN

## Ödevin Amacı

Sıfırdan bir gelir-gider takip uygulaması. Herkes kendi kişisel bütçesini tutabilecek;
isteyen bir Ev bütçesi açıp ev arkadaşlarını, eşini veya ailesini davet edebilecek.

Ödev sonunda kendi başına yapabileceklerin:

- Bir model yazıp migration ile veritabanına tablo olarak eklemek
- ForeignKey ile "bu kayıt kime/neye ait" bilgisini tutmak
- Kayıt, giriş, çıkış (Django'nun hazır araçlarıyla)
- Bir kullanıcının sadece kendi verisini görmesini sağlamak
- Ekleme, listeleme, düzenleme, silme (CRUD)
- Toplam gelir/gider gibi hesaplamaları veritabanına yaptırmak (Sum)

**Kural:** Her aşamayı bitirince commit at. Mesajlar anlamlı olsun:
`feat: add transaction model`, `fix: user can see only own budgets`.
Tek seferde "her şeyi yaptım" commit'i kabul edilmez.

**Altın kural:** Bir şeyi kopyalayıp yapıştırdıysan, o satırın ne yaptığını bir cümleyle
söyleyebilmelisin. Söyleyemiyorsan dur, dokümana bak veya sor.

---

## Önce Şunu Anla: Django Nasıl Çalışır?

### 1. Bir sayfa açıldığında ne olur?

```
Tarayıcı → urls.py → views.py → (models.py ile veritabanından veri al) → template (.html) → Tarayıcı
```

- **urls.py:** "Bu adres gelirse hangi fonksiyon çalışsın?" Bir telefon rehberi gibi.
- **views.py:** Asıl işi yapan fonksiyon. Veriyi alır, hazırlar, template'e verir.
- **models.py:** Veritabanı tablolarının Python hâli. Bir model = bir tablo, bir alan = bir kolon.
- **template:** Kullanıcının gördüğü HTML. View'dan gelen veriyi `{{ }}` ile gösterir.

**İpucu:** Bir sayfa hata veriyorsa bu sırayla kontrol et: adres urls.py'de var mı →
view doğru veriyi gönderiyor mu → template doğru ismi kullanıyor mu.

### 2. Model ve Migration

Model yazmak tabloyu oluşturmaz. İki komut gerekir:

```bash
python manage.py makemigrations   # "Değişikliklerin planını çıkar" (dosya oluşturur)
python manage.py migrate          # "Planı veritabanına uygula"
```

Benzetme: `makemigrations` mimarın çizdiği proje, `migrate` inşaat.
Modelde bir alanı her değiştirdiğinde ikisini de çalıştır.

### 3. ForeignKey = "Bu kayıt kime ait?"

Bir harcama kaydı tek bir bütçeye aittir; bir bütçede çok harcama olur.
Buna 1'e çok (1:N) denir:

```python
class Transaction(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='transactions')
```

- `on_delete=models.CASCADE`: Bütçe silinirse ona ait harcamalar da silinsin.
- `related_name='transactions'`: Ters yönden erişim adı. `budget.transactions.all()`

### 4. Giriş yapmış olmak ≠ Yetkili olmak

`@login_required` sadece "giriş yapmış mı?" diye bakar. "Bu bütçe senin mi?" diye bakmaz.

```python
# YANLIŞ: giriş yapan herkes id'yi değiştirip başkasının bütçesini görebilir
budget = get_object_or_404(Budget, pk=pk)

# DOĞRU: sadece üyesi olduğun bütçeler arasında ara
budget = get_object_or_404(Budget, pk=pk, members=request.user)
```

Template'te butonu gizlemek güvenlik değildir. Kullanıcı adresi elle yazabilir.

### 5. Para için asla float kullanma

`0.1 + 0.2` Python'da `0.30000000000000004` eder. Para için `DecimalField` kullan:

```python
amount = models.DecimalField(max_digits=12, decimal_places=2)
```

**Mini alıştırma (kodlamadan önce):** "Kullanıcı `/transactions/add/` adresine gidince
önce ___ dosyası, sonra ___ fonksiyonu, sonra ___ template'i çalışır."

---

## Uygulamanın Fikri ve Veri Modeli

Merkezinde **Bütçe (Budget)** var. Her işlem (gelir veya gider) bir bütçeye kaydedilir.
İki tür:

- **Bireysel:** Sadece sahibi görür. Her kullanıcıya kayıt olduğunda otomatik bir tane açılır.
- **Ev:** Sahibi davet kodu paylaşır, başkaları bu kodla katılır. Tüm üyeler aynı işlemleri
  görür ve ekler.

Böylece "bireysel mi, ev mi" için iki ayrı sistem yazmıyorsun. Tek model, sadece üye sayısı farklı.

### Tablolar ve ilişkiler

```
User (Django'nun hazır modeli)
 │
 ├── 1:N  Membership  N:1  Budget        (kim hangi bütçenin üyesi, rolü ne)
 │                           │
 │                           ├── 1:N  Category     (Market, Kira, Maaş...)
 │                           └── 1:N  Transaction  (gelir/gider kayıtları)
 │
 └── 1:N  Transaction.created_by          (işlemi kim girdi)
```

| Model | Ne tutar? | Önemli alanlar |
|---|---|---|
| `Budget` | Bir bütçe (bireysel veya ev) | `name`, `kind` (personal/household), `owner` → User, `invite_code` (benzersiz), `created_at` |
| `Membership` | Kullanıcı ↔ Bütçe bağlantısı | `user` → User, `budget` → Budget, `role` (owner/member), `joined_at` — aynı kişi aynı bütçeye bir kez üye olabilir |
| `Category` | İşlemin türü | `budget` → Budget, `name`, `kind` (income/expense) |
| `Transaction` | Tek bir gelir veya gider | `budget` → Budget, `category` → Category, `created_by` → User, `kind` (income/expense), `amount` (Decimal), `date`, `description`, `created_at` |

### Kod iskeleti (eksikleri sen tamamla)

```python
# finance/models.py
import secrets
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Budget(models.Model):
    class Kind(models.TextChoices):
        PERSONAL = 'personal', 'Bireysel'
        HOUSEHOLD = 'household', 'Ev'

    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=10, choices=Kind.choices, default=Kind.PERSONAL)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_budgets')
    members = models.ManyToManyField(User, through='Membership', related_name='budgets')
    invite_code = models.CharField(max_length=8, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = secrets.token_hex(4)  # örn: 'a3f9c21b'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Membership(models.Model):
    # TODO: user, budget, role (owner/member), joined_at
    # TODO: Meta içinde UniqueConstraint(fields=['user', 'budget'], ...)
    ...


class Category(models.Model):
    # TODO: budget, name, kind
    ...


class Transaction(models.Model):
    # TODO: budget, category, created_by, kind, amount, date, description, created_at
    # TODO: Meta: ordering = ['-date', '-created_at']
    ...
```

**İpucu (ManyToMany + through):** `members` sayesinde `budget.members.all()` ile üyeleri,
`user.budgets.all()` ile kullanıcının bütçelerini alırsın. `through='Membership'` dediğin
için üyelik kaydına `role` gibi ekstra bilgi koyabiliyorsun.
Üye eklemek için `Membership.objects.create(user=..., budget=..., role='member')`.

**Soru (README):** `category` alanında `on_delete` olarak CASCADE mi, PROTECT mu seçtin?
Bir kategoriyi silince o kategorideki eski harcamalar ne olmalı?

---

## Aşamalar

### Aşama 0 — Hazırlık

- [ ] `django-admin startproject config .`
- [ ] İki app: `accounts` (kayıt/giriş) ve `finance` (bütçe, işlem). İkisini de INSTALLED_APPS'e ekle.
- [ ] `settings.py`: `LANGUAGE_CODE = 'tr'`, `TIME_ZONE = 'Europe/Istanbul'`
- [ ] `SECRET_KEY` ve `DEBUG` değerlerini `.env` dosyasından oku. Repoya `.env.example` koy.
- [ ] `.gitignore`: `db.sqlite3`, `.env`, `__pycache__/`, `venv/` repoda olmamalı.
- [ ] `requirements.txt`: `pip freeze > requirements.txt`

**İpucu:** `.env` değerleri hep metin gelir. `DEBUG = os.getenv('DEBUG') == 'True'`

**Soru (README):** Neden her şeyi tek app'e değil de `accounts` ve `finance` diye ikiye ayırdık?

### Aşama 1 — Kayıt, Giriş, Çıkış

1. `/register/`: `UserCreationForm`'u genişleterek e-posta alanı ekle (zorunlu).
2. `/login/` ve `/logout/` için `LoginView`, `LogoutView`.
3. `settings.py`: `LOGIN_URL = 'login'`, `LOGIN_REDIRECT_URL = 'dashboard'`, `LOGOUT_REDIRECT_URL = 'login'`
4. Kayıt olan kullanıcıya otomatik "Kişisel Bütçem" oluştur, owner üyesi yap. **Signal ile.**

```python
# finance/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Budget, Membership

@receiver(post_save, sender=User)
def create_personal_budget(sender, instance, created, **kwargs):
    if created:  # sadece YENİ kullanıcı oluşunca çalışsın
        budget = Budget.objects.create(name='Kişisel Bütçem', owner=instance)
        # TODO: Membership kaydını oluştur (role='owner')
```

```python
# finance/apps.py
class FinanceConfig(AppConfig):
    name = 'finance'

    def ready(self):
        from . import signals  # noqa — import etmezsen signal hiç çalışmaz!
```

**İpucu:** Signal çalışmıyorsa %90 ihtimalle `ready()` içinde import etmeyi unuttun.

**İpucu:** `LogoutView` Django 5'ten itibaren sadece POST kabul eder:

```html
<form method="post" action="{% url 'logout' %}">
  {% csrf_token %}
  <button type="submit">Çıkış</button>
</form>
```

**Kontrol et:** Yeni kullanıcı kaydol → Admin'de Budget ve Membership tablosunda birer kayıt olmalı.

### Aşama 2 — Modeller ve Admin

1. 4 modeli tamamla, `makemigrations` + `migrate`.
2. Her bütçe oluşunca varsayılan kategoriler eklensin (signal, `post_save` on Budget):
   - Gider: Market, Kira, Faturalar, Ulaşım, Eğlence, Diğer
   - Gelir: Maaş, Ek Gelir, Diğer
3. Admin'e dört modeli de kaydet:
   - `TransactionAdmin`: `list_display = ('date', 'budget', 'kind', 'category', 'amount', 'created_by')`,
     `list_filter = ('kind', 'budget')`, `search_fields = ('description',)`
   - `BudgetAdmin`: Membership'i inline göster (`TabularInline`)

**Kontrol et:** Admin'den elle bir gelir ve bir gider ekleyebiliyorsun, listede filtreleyebiliyorsun.

### Aşama 3 — İşlemler (CRUD) ve "Sadece Benim Verim"

**Ödevin kalbi.** Önce sadece kendi kişisel bütçende çalış.

| Adres | Ne yapar? | Method |
|---|---|---|
| `/` (dashboard) | Kullanıcının bütçelerini listeler | GET |
| `/budgets/<id>/` | Bütçenin işlemleri + bu ayın toplamları | GET |
| `/budgets/<id>/add/` | Yeni işlem ekler | GET + POST |
| `/transactions/<id>/edit/` | İşlemi düzenler | GET + POST |
| `/transactions/<id>/delete/` | Onay sayfası (GET), silme (POST) | GET + POST |

Gereksinimler:

- Tüm view'lar `@login_required`.
- Kullanıcı sadece üyesi olduğu bütçeleri ve işlemleri görebilir. Değilse **404**.
- İşlemi sadece onu ekleyen kişi veya bütçenin sahibi düzenleyebilir/silebilir. Değilse **403**.
- İşlem formunda sadece o bütçenin ve seçilen türe uygun kategoriler çıkmalı.
- Tutar 0 veya negatif olamaz (`clean_amount`).
- Her başarılı işlemden sonra `messages.success(...)`.

```python
# finance/utils.py
from django.shortcuts import get_object_or_404
from .models import Budget

def get_user_budget(user, budget_id):
    """Kullanıcının üyesi olduğu bütçeyi döner, değilse 404."""
    return get_object_or_404(Budget, pk=budget_id, members=user)
```

```python
if form.is_valid():
    tx = form.save(commit=False)   # henüz veritabanına yazma
    tx.budget = budget
    tx.created_by = request.user
    tx.save()
```

```python
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['kind', 'category', 'amount', 'date', 'description']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, budget=None, **kwargs):
        super().__init__(*args, **kwargs)
        if budget:
            self.fields['category'].queryset = budget.categories.all()
```

403 için: `from django.core.exceptions import PermissionDenied` → `raise PermissionDenied`

**Kontrol et:** İki farklı kullanıcıyla gir. A'nın işleminin id'sini B'nin adres çubuğuna yaz → 404.

**Soru (README):** Başkasının bütçesine erişimde neden 403 değil de 404 döndürüyoruz?

### Aşama 4 — Ev Bütçesi ve Üyeler

1. `/budgets/new/` ile yeni Ev bütçesi. Açan kişi otomatik owner üyesi.
2. Bütçe detayında sahibi davet kodunu görür.
3. `/budgets/join/` sayfasına kod yazarak katılım (member olarak).
4. Bütçe detayında üye listesi.
5. Üye ayrılabilir. Sahip bir üyeyi çıkarabilir. Sahip kendi bütçesinden ayrılamaz (silebilir).
6. Kişisel bütçeye kimse katılamaz: kişisel bütçe kodu ile katılmaya çalışılırsa hata mesajı.

**Çözmen gereken durumlar (README'de yaz):**

- Zaten üye olduğun bütçenin kodunu tekrar girersen ne olur?
- Yanlış kod girilirse ne olur?
- Bütçeden ayrılan kişinin daha önce girdiği işlemler ne olacak? Kararını gerekçelendir.

**İpucu:** Katılma, ayrılma, üye çıkarma POST ile yapılmalı. Link değil, form.

```python
class Budget(models.Model):
    ...
    def is_owner(self, user):
        return self.owner_id == user.id
```

**Kontrol et:** A Ev bütçesi açar, B kodla katılır, B gider ekler, A bu gideri listede görür.

### Aşama 5 — Özet ve Raporlar

Bütçe detay sayfasının üstünde bu ayın özeti:

- Toplam gelir, toplam gider, kalan (gelir − gider). Kalan negatifse kırmızı.
- Kategorilere göre gider dağılımı (tablo yeterli).
- Ev bütçesinde: kim ne kadar harcadı (üye bazında toplam gider).
- Ay seçimi: `?month=2026-10` parametresi ile önceki aylar.

```python
from django.db.models import Sum

qs = budget.transactions.filter(date__year=2026, date__month=10)
income = qs.filter(kind='income').aggregate(total=Sum('amount'))['total'] or 0

by_category = (qs.filter(kind='expense')
                 .values('category__name')
                 .annotate(total=Sum('amount'))
                 .order_by('-total'))
```

`or 0` neden var? Hiç işlem yoksa `Sum` sonucu `None` döner. `None - 100` hata verir.

"Kim ne kadar harcadı" için `values('created_by__username')`.

### Aşama 6 — Kalite ve Testler

- [ ] İşlem listesine sayfalama (sayfa başına 20, `Paginator`).
- [ ] Tüm silme işlemleri POST ile, tüm formlarda `{% csrf_token %}`.
- [ ] Tüm ekleme/düzenleme/silme işlemlerinde `messages` ile geri bildirim.
- [ ] İşlem listesinde N+1 sorgu olmamalı: `select_related('category', 'created_by')`.
- [ ] En az 6 test (`finance/tests.py`):
  1. Giriş yapmamış kullanıcı dashboard'a gidince login'e yönlendirilir.
  2. Kayıt olan kullanıcıya otomatik kişisel bütçe oluşur.
  3. Kullanıcı üyesi olmadığı bütçeyi göremez (404).
  4. Kullanıcı başkasının işlemini silemez (403).
  5. Geçerli kodla Ev bütçesine katılınca Membership oluşur.
  6. Aylık toplam gelir/gider doğru hesaplanır.

```python
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class BudgetAccessTests(TestCase):
    def setUp(self):
        self.ali = User.objects.create_user('ali', password='Test12345!')
        self.ayse = User.objects.create_user('ayse', password='Test12345!')

    def test_cannot_see_other_users_budget(self):
        ayse_budget = self.ayse.owned_budgets.first()
        self.client.login(username='ali', password='Test12345!')
        response = self.client.get(reverse('budget_detail', args=[ayse_budget.pk]))
        self.assertEqual(response.status_code, 404)
```

`python manage.py test` — test her seferinde boş veritabanıyla başlar.

---

## Kabul Kriterleri (Teslimden Önce Kendin Dene)

| # | Senaryo | Beklenen |
|---|---|---|
| 1 | Yeni kullanıcı kaydol | Giriş yapılır, dashboard'da "Kişisel Bütçem" görünür |
| 2 | Çıkış yap, `/` adresine git | Login sayfasına yönlendirilir |
| 3 | Kişisel bütçeye 1 gelir, 2 gider ekle | Liste ve aylık toplamlar doğru |
| 4 | 0 veya negatif tutar gir | Form hata mesajı verir |
| 5 | Başka kullanıcının bütçe id'sini adrese yaz | 404 |
| 6 | Ev bütçesi aç, kodu B ile paylaş, B katılsın | B üye listesinde görünür |
| 7 | B bir gider eklesin | A da görür; "kim ne harcadı" tablosunda B çıkar |
| 8 | A, B'nin eklediği gideri silmeye çalışsın | A sahip olduğu için silebilir |
| 9 | B, A'nın eklediği gideri silmeye çalışsın | 403 |
| 10 | Kişisel bütçenin koduyla katılmayı dene | Hata mesajı, katılım olmaz |
| 11 | B bütçeden ayrılsın | B artık o bütçeyi göremez (404) |
| 12 | `python manage.py test` | Tüm testler geçer |
| 13 | `db.sqlite3`'ü silip `migrate` | Hatasız çalışır |

---

## Değerlendirme

| Alan | Puan |
|---|---|
| Aşama 0–1: Hazırlık, kayıt/giriş, signal | 15 |
| Aşama 2: Modeller ve admin | 15 |
| Aşama 3: CRUD ve yetki kontrolü | 25 |
| Aşama 4: Ev bütçesi, davet, üyeler | 20 |
| Aşama 5: Özet ve raporlar | 10 |
| Aşama 6: Testler ve kalite | 10 |
| README ve soruların cevapları | 5 |
| **Toplam** | **100** |

**Otomatik puan kırılan durumlar:**

- `db.sqlite3` veya `.env` repoya commit'lenmişse
- Yetki kontrolü sadece template'te yapılmışsa (view'da da şart)
- Silme işlemi GET ile yapılıyorsa
- Temiz veritabanında `migrate` hata veriyorsa
- Tek dev commit atılmışsa

---

## Bonus (İsteğe Bağlı, +10'a Kadar)

- Aylık gelir/gider grafiği (Chart.js, veriyi view'dan JSON olarak gönder)
- İşlemleri CSV olarak dışa aktarma (`HttpResponse` + `csv`)
- Kategori bazında aylık limit ve limit aşılınca uyarı
- Tekrarlayan işlemler (kira, maaş gibi)
- Ev bütçesinde "kim kime ne kadar borçlu" (harcamaları eşit bölüşme)
- Class-based view'lara geçiş (`ListView`, `CreateView`, `UserPassesTestMixin`)

---

## Teslim

1. `feature/budget` branch'inde çalış, `main`'e Pull Request aç.
2. README'de olsun: kurulum adımları (`.env.example` dahil), veri modeli şeması,
   "Soru" işaretli maddelerin cevapları, birkaç ekran görüntüsü
   (kayıt, dashboard, bütçe detayı, ev bütçesi üyeleri).
3. `requirements.txt` güncel olsun.
4. PR açıklamasında hangi aşamaları bitirdiğini işaretle.

---

## Sık Yapılan Hatalar ve Çözümleri

| Hata / Belirti | Muhtemel sebep | Çözüm |
|---|---|---|
| `no such table: finance_transaction` | Migration yapılmamış | `makemigrations` + `migrate` |
| `NoReverseMatch` | `{% url 'isim' %}` ile urls.py'deki `name=` aynı değil | İsimleri karşılaştır, args eksik mi bak |
| Signal çalışmıyor | `apps.py` `ready()` içinde import yok | `from . import signals` ekle; INSTALLED_APPS'te `'finance.apps.FinanceConfig'` |
| Form kaydetmiyor, hata da göstermiyor | Template'te form hataları basılmıyor | `{{ form.errors }}` ekle |
| `IntegrityError: NOT NULL constraint failed: ...created_by_id` | `commit=False` sonrası alan atanmadı | `tx.created_by = request.user` kontrol et |
| `CSRF verification failed` | Formda token yok | `<form>` içine `{% csrf_token %}` |
| `unsupported operand type(s) ... NoneType` | Hiç işlem yokken `Sum` None döndü | Sonuna `or 0` ekle |

**Son ipucu:** Takıldığında önce hatanın son satırını oku, sonra hangi dosyada ve hangi
satırda olduğuna bak. İlk kaynağın Django dokümantasyonu olsun.
