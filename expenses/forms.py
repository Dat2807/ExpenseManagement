from django import forms
from django.utils import timezone
from .models import Category, Transaction


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True
            }),
            'type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'amount', 'description', 'category']
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Description',
                'required': True
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Amount',
                'min': '1',
                'required': True
            }),
            'date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mặc định date = hôm nay
        if not self.instance.pk:  # Chỉ set khi tạo mới, không set khi edit
            self.fields['date'].initial = timezone.now().date()