import secrets

from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class MoneyKind(models.TextChoices):
    INCOME = 'income', 'Gelir'
    EXPENSE = 'expense', 'Gider'


class Budget(models.Model):
    """Bir butce: ya bireysel ya da ev (ortak)."""

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
        # Kaydetmeden once davet kodu yoksa uret.
        if not self.invite_code:
            self.invite_code = secrets.token_hex(4)  # orn: 'a3f9c21b'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Membership(models.Model):
    """Kim hangi butcenin uyesi, orada rolu ne?"""

    class Role(models.TextChoices):
        MEMBER = 'member', 'Üye'
        OWNER = 'owner', 'Sahip'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "budget"], name='unique_user_per_budget'),
        ]

    def __str__(self):
        return f'{self.user}, {self.budget}, {self.get_role_display()}'


class Category(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=50)
    kind = models.CharField(max_length=10, choices=MoneyKind.choices, default=MoneyKind.EXPENSE)

    class Meta:
        verbose_name = 'kategori'
        verbose_name_plural = 'kategoriler'

    def __str__(self):
        return f'{self.budget}, {self.name}, {self.get_kind_display()}'


class Transaction(models.Model):
    # Once "bu kayit neye/kime ait" alanlari
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='transactions')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_transactions', null=True)

    # Sonra kaydin kendi degerleri
    kind = models.CharField(max_length=10, choices=MoneyKind.choices, default=MoneyKind.EXPENSE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.amount}, {self.date}, {self.category}'
