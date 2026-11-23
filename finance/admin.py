from django.contrib import admin
from .models import Budget, Membership, Category, Transaction

admin.site.register(Membership)
admin.site.register(Category)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'budget', 'kind', 'category', 'amount', 'created_by')
    list_filter = ('kind', 'budget')
    search_fields = ('description',)


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    inlines = [MembershipInline]
