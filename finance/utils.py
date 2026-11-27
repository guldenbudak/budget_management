from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Budget, Transaction


def get_user_budget(user, budget_id):
    """kullanıcının üyesi olduğu bütçeyi döner değilse 404."""
    return get_object_or_404(Budget, pk=budget_id, members=user)


def get_editable_transaction(user, transaction_id):
    """Kullanicinin duzenleyebilecegi islemi doner.

    Uyesi olmadigi butcedeki islem icin 404, uye ama yetkisi yoksa 403 verir.
    select_related('budget') sayesinde can_edit icindeki butce erisimi
    ayri bir sorgu atmaz.
    """
    transaction = get_object_or_404(
        Transaction.objects.select_related('budget'),
        pk=transaction_id,
        budget__members=user,
    )
    if not transaction.can_edit(user):
        raise PermissionDenied
    return transaction
