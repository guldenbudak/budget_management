from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Transaction

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


@login_required
def transaction_edit(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id, budget__members=request.user)
    if not transaction.can_edit(request.user):
        raise PermissionDenied
    if request.method == 'POST':
        form = TransactionForm(request.POST, budget=transaction.budget, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Değişiklikler başarıyla kaydedilmiştir.')
            return redirect('budget_detail', transaction.budget_id)
    else:
        form = TransactionForm(budget=transaction.budget, instance=transaction)
    return render(request, 'finance/transaction_form.html', {'form': form, 'budget': transaction.budget})


@login_required
def transaction_delete(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id, budget__members=request.user)
    if not transaction.can_edit(request.user):
        raise PermissionDenied
    if request.method == 'POST':
        budget_id = transaction.budget_id
        transaction.delete()
        messages.success(request, 'Kaydınız başarıyla silinmiştir.')
        return redirect('budget_detail', budget_id)
    return render(request, 'finance/transaction_confirm_delete.html', {'transaction': transaction})
