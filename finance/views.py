from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import TransactionForm
from .utils import get_user_budget


@login_required
def dashboard(request):
    return render(request, 'finance/dashboard.html', {'budgets': request.user.budgets.all()})


@login_required
def budget_detail(request, budget_id):
    budget = get_user_budget(request.user, budget_id)
    transactions = budget.transactions.select_related('category', 'created_by')
    return render(request, 'finance/budget_detail.html', {'budget': budget, 'transactions': transactions})


@login_required
def transaction_create(request, budget_id):
    budget = get_user_budget(request.user, budget_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST, budget=budget)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.budget = budget
            transaction.created_by = request.user
            transaction.save()
            messages.success(request, 'Kaydınız başarıyla oluşmuştur.')
            return redirect('budget_detail', budget_id)
    else:
        form = TransactionForm(budget=budget)
    return render(request, 'finance/transaction_form.html', {'budget': budget, 'form': form})
