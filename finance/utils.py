from django.shortcuts import get_object_or_404
from .models import Budget


def get_user_budget(user, budget_id):
    """kullanıcının üyesi olduğu bütçeyi döner değilse 404."""
    return get_object_or_404(Budget, pk=budget_id, members=user)
