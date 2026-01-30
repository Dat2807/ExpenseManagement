from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Category, Transaction
from ..forms import TransactionForm


# NEW: Create transaction với type parameter (income/expense)
def transaction_create_by_type(request, type):
    from ..models import MonthlyBudget
    from datetime import date
    
    # Get year/month from query params if coming from monthly budget
    year = request.GET.get('year')
    month = request.GET.get('month')
    monthly_budget = None
    
    if year and month:
        year, month = int(year), int(month)
        monthly_budget = MonthlyBudget.objects.filter(year=year, month=month).first()
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        form.fields['category'].queryset = Category.objects.filter(type=type)
        
        if form.is_valid():
            transaction = form.save(commit=False)
            
            # Validate date is within the month if coming from monthly budget
            if monthly_budget:
                if transaction.date.year != year or transaction.date.month != month:
                    messages.error(request, f'Date must be within {year}-{month:02d}')
                    return render(request, 'transaction/transaction_form.html', {
                        'form': form,
                        'is_create': True,
                    })
                transaction.monthly_budget = monthly_budget
            
            transaction.save()
            type_label = 'Income' if type == 'income' else 'Expense'
            messages.success(request, f'{type_label} "{transaction.description}" has been added successfully.')
            
            # Redirect to month_detail if coming from monthly budget
            if monthly_budget:
                return redirect(f'/monthly/{year}/{month}/#transactions')
            # If not from monthly budget, redirect to monthly list
            return redirect('monthly_list')
    else:
        initial = {}
        if monthly_budget:
            initial['date'] = date(year, month, 1)
        form = TransactionForm(initial=initial)
        form.fields['category'].queryset = Category.objects.filter(type=type)
        
        # Add min/max date constraints if coming from monthly budget
        if monthly_budget:
            from calendar import monthrange
            last_day = monthrange(year, month)[1]
            form.fields['date'].widget.attrs.update({
                'min': f'{year}-{month:02d}-01',
                'max': f'{year}-{month:02d}-{last_day:02d}'
            })
    
    return render(request, 'transaction/transaction_form.html', {
        'form': form,
        'is_create': True,
    })




# User vào /edit/<id>/ (GET) → Hiển thị form có dữ liệu
# User sửa data, bấm Submit (POST) → Validate → Lưu DB → Redirect về list
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    year = request.GET.get('year')
    month = request.GET.get('month')
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            updated_transaction = form.save()
            messages.success(request, f'Transaction "{updated_transaction.description}" has been updated successfully.')
            
            # Redirect to month_detail if coming from monthly budget
            if year and month:
                return redirect(f'/monthly/{year}/{month}/#transactions')
            return redirect('monthly_list')
    else:
        form = TransactionForm(instance=transaction)
        
        # Add min/max date constraints if coming from monthly budget
        if year and month:
            from calendar import monthrange
            year_int, month_int = int(year), int(month)
            last_day = monthrange(year_int, month_int)[1]
            form.fields['date'].widget.attrs.update({
                'min': f'{year_int}-{month_int:02d}-01',
                'max': f'{year_int}-{month_int:02d}-{last_day:02d}'
            })
        
    return render(request, 'transaction/transaction_form.html', {
        'form': form,
        'is_create': False,
    })



# User vào /delete/<id>/ (GET) → Hiển thị confirm delete
# User bấm OK (POST) → Xóa DB → Redirect về list
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    year = request.GET.get('year')
    month = request.GET.get('month')
    
    if request.method == 'POST':
        description = transaction.description
        transaction.delete()
        messages.success(request, f'Transaction "{description}" has been deleted successfully.')
        
        # Redirect to month_detail if coming from monthly budget
        if year and month:
            return redirect(f'/monthly/{year}/{month}/#transactions')
        return redirect('monthly_list')
    return render(request, 'transaction/transaction_confirm_delete.html', {
        'transaction': transaction
    })
