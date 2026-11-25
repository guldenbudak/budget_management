from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .utils import get_user_budget


@login_required
def dashboard(request):
    return render(request, 'finance/dashboard.html', {'budgets': request.user.budgets.all()})


@login_required
def budget_detail(request, budget_id):
    budget = get_user_budget(request.user, budget_id)
    transactions = budget.transactions.select_related('category', 'created_by')
    return render(request, 'finance/budget_detail.html', {'budget': budget, 'transactions': transactions})
