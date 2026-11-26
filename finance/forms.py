from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        fields = ['kind', 'category', 'amount', 'date', 'description']

    def __init__(self, *args, budget=None, **kwargs):
        super().__init__(*args, **kwargs)
        if budget:
            self.fields['category'].queryset = budget.categories.all()

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError('Tutar 0 veya negatif olamaz.')
        return amount

    def clean(self):
        cleaned = super().clean()
        kind = cleaned.get('kind')
        category = cleaned.get('category')
        if kind and category and category.kind != kind:
            raise forms.ValidationError('Seçilen kategori işlem türüyle uyuşmuyor.')
        return cleaned
