from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Budget, Membership, Category, MoneyKind

DEFAULT_CATEGORIES = [
    ('Market', MoneyKind.EXPENSE),
    ('Kira', MoneyKind.EXPENSE),
    ('Faturalar', MoneyKind.EXPENSE),
    ('Ulaşım', MoneyKind.EXPENSE),
    ('Eğlence', MoneyKind.EXPENSE),
    ('Diğer', MoneyKind.EXPENSE),
    ('Maaş', MoneyKind.INCOME),
    ('Ek Gelir', MoneyKind.INCOME),
    ('Diğer', MoneyKind.INCOME),
]


@receiver(post_save, sender=User)
def create_personal_budget(sender, instance, created, **kwargs):
    if created:  # sadece YENİ kullanıcı oluşunca çalışsın
        budget = Budget.objects.create(name='Kişisel Bütçem', owner=instance)
        Membership.objects.create(user=instance, budget=budget, role=Membership.Role.OWNER)


@receiver(post_save, sender=Budget)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        for category_name, category_type in DEFAULT_CATEGORIES:
            Category.objects.create(
                budget=instance,
                name=category_name,
                kind=category_type,
            )
