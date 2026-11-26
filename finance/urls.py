from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('budgets/<int:budget_id>/', views.budget_detail, name='budget_detail'),
    path('budgets/<int:budget_id>/add/', views.transaction_create, name='transaction_create'),

]
