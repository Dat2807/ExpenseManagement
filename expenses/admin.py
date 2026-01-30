from django.contrib import admin
from .models import Category, Transaction, MonthlyBudget, CategoryBudget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    list_filter = ['type']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'amount', 'description', 'category']
    list_filter = ['category', 'date']


@admin.register(MonthlyBudget)
class MonthlyBudgetAdmin(admin.ModelAdmin):
    list_display = ['year', 'month', 'created_at']
    list_filter = ['year', 'month']
    ordering = ['-year', '-month']


@admin.register(CategoryBudget)
class CategoryBudgetAdmin(admin.ModelAdmin):
    list_display = ['monthly_budget', 'category', 'budgeted_amount']
    list_filter = ['monthly_budget', 'category']
