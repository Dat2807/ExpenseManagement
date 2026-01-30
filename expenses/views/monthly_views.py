from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Q
from datetime import datetime
from ..models import MonthlyBudget, CategoryBudget, Category, Transaction

# Monthly budget views
def monthly_list(request):
    monthly_budgets = MonthlyBudget.objects.all()
    
    # Calculate income, expense, balance for each month
    budget_data = []
    for budget in monthly_budgets:
        # Get all transactions in this month
        transactions = Transaction.objects.filter(
            date__year=budget.year,
            date__month=budget.month
        )
        
        # Calculate income and expense
        income = transactions.filter(
            category__type='income'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        expense = transactions.filter(
            category__type='expense'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        balance = income - expense
        
        budget_data.append({
            'budget': budget,
            'income': income,
            'expense': expense,
            'balance': balance,
        })
    
    context = {
        'budget_data': budget_data,
    }
    return render(request, 'monthly/monthly_list.html', context)

# Monthly budget create view
def month_create(request):
    if request.method == 'POST':
        year = int(request.POST.get('year'))
        month = int(request.POST.get('month'))
        
        # Check if already exists
        if MonthlyBudget.objects.filter(year=year, month=month).exists():
            messages.error(request, f'Budget for {year}-{month:02d} already exists!')
            return redirect('monthly_list')
        
        # Create monthly budget
        monthly_budget = MonthlyBudget.objects.create(year=year, month=month)
        messages.success(request, f'Monthly budget for {year}-{month:02d} created successfully!')
        
        return redirect('month_detail', year=year, month=month)
    
    # GET request - show form
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    context = {
        'current_year': current_year,
        'current_month': current_month,
        'years': range(current_year - 2, current_year + 3),  # 5 years range
        'months': range(1, 13),
    }
    return render(request, 'monthly/month_create.html', context)

# Month detail page with 2 tabs:
# - Tab 1: Budget Summary (Budgeted vs Actual by category)
# - Tab 2: Transactions list
def month_detail(request, year, month):
    monthly_budget = get_object_or_404(MonthlyBudget, year=year, month=month)
    
    # Get all categories
    income_categories = Category.objects.filter(type='income')
    expense_categories = Category.objects.filter(type='expense')
    
    # Get all transactions in this month
    transactions = Transaction.objects.filter(
        date__year=year,
        date__month=month
    )
    
    # Calculate actual amounts by category
    def get_category_data(categories, trans_type):
        data = []
        for category in categories:
            # Get budgeted amount
            try:
                category_budget = CategoryBudget.objects.get(
                    monthly_budget=monthly_budget,
                    category=category
                )
                budgeted = category_budget.budgeted_amount
            except CategoryBudget.DoesNotExist:
                budgeted = 0
            
            # Get actual amount
            actual = transactions.filter(category=category).aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            # Calculate difference
            difference = budgeted - actual
            
            data.append({
                'category': category,
                'budgeted': budgeted,
                'actual': actual,
                'difference': difference,
            })
        
        return data
    
    income_data = get_category_data(income_categories, 'income')
    expense_data = get_category_data(expense_categories, 'expense')
    
    # Calculate totals
    total_income_budgeted = sum(item['budgeted'] for item in income_data)
    total_income_actual = sum(item['actual'] for item in income_data)
    total_expense_budgeted = sum(item['budgeted'] for item in expense_data)
    total_expense_actual = sum(item['actual'] for item in expense_data)
    
    # Calculate total differences
    total_expense_difference = total_expense_budgeted - total_expense_actual
    total_income_difference = total_income_actual - total_income_budgeted
    
    # Separate transactions by type for the 2-column layout
    expenses = transactions.filter(category__type='expense')
    incomes = transactions.filter(category__type='income')
    
    # Calculate month totals
    month_expense = sum(t.amount for t in expenses)
    month_income = sum(t.amount for t in incomes)
    month_balance = month_income - month_expense
    
    context = {
        'monthly_budget': monthly_budget,
        'year': year,
        'month': month,
        'income_data': income_data,
        'expense_data': expense_data,
        'total_income_budgeted': total_income_budgeted,
        'total_income_actual': total_income_actual,
        'total_expense_budgeted': total_expense_budgeted,
        'total_expense_actual': total_expense_actual,
        'total_expense_difference': total_expense_difference,
        'total_income_difference': total_income_difference,
        'transactions': transactions,
        'expenses': expenses,
        'incomes': incomes,
        'month_expense': month_expense,
        'month_income': month_income,
        'month_balance': month_balance,
    }
    return render(request, 'monthly/month_detail.html', context)


# Delete monthly budget
def month_delete(request, year, month):
    monthly_budget = get_object_or_404(MonthlyBudget, year=year, month=month)
    
    if request.method == 'POST':
        from django.db.models.deletion import ProtectedError
        try:
            monthly_budget.delete()
            messages.success(request, f'Monthly budget for {year}-{month:02d} has been deleted successfully.')
            return redirect('monthly_list')
        except ProtectedError:
            messages.error(request, f'Cannot delete monthly budget for {year}-{month:02d} because it has transactions. Please delete all transactions first.')
            return redirect('monthly_list')
    
    return render(request, 'monthly/month_confirm_delete.html', {
        'monthly_budget': monthly_budget,
        'year': year,
        'month': month,
    })


# Update budgeted amount for a specific category
def category_budget_update(request, year, month, category_id):
    monthly_budget = get_object_or_404(MonthlyBudget, year=year, month=month)
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        budgeted_amount = int(request.POST.get('budgeted_amount', 0))
        
        # Update or create CategoryBudget
        category_budget, created = CategoryBudget.objects.update_or_create(
            monthly_budget=monthly_budget,
            category=category,
            defaults={'budgeted_amount': budgeted_amount}
        )
        
        messages.success(request, f'Budget for {category.name} updated to {budgeted_amount:,}đ')
        return redirect('month_detail', year=year, month=month)
    
    return redirect('month_detail', year=year, month=month)

