from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Category, Transaction
from ..forms import TransactionForm


# Flow: User vào / → lấy all transactions → render ra HTML
def transaction_list(request):
    # Filter transactions theo loại
    expenses = Transaction.objects.filter(category__type='expense')
    incomes = Transaction.objects.filter(category__type='income')
    
    # Tính tổng
    total_expense = sum(t.amount for t in expenses)
    total_income = sum(t.amount for t in incomes)
    balance = total_income - total_expense
    
    # 2 form riêng
    expense_form = TransactionForm(prefix='expense')
    income_form = TransactionForm(prefix='income')
    
    # Filter category cho mỗi form
    expense_form.fields['category'].queryset = Category.objects.filter(type='expense')
    income_form.fields['category'].queryset = Category.objects.filter(type='income')
    
    if request.method == 'POST':
        if 'expense_submit' in request.POST:
            expense_form = TransactionForm(request.POST, prefix='expense')
            expense_form.fields['category'].queryset = Category.objects.filter(type='expense')
            if expense_form.is_valid():
                transaction = expense_form.save()
                messages.success(request, f'Expense "{transaction.description}" has been added successfully.')
                return redirect('transaction_list')
        elif 'income_submit' in request.POST:
            income_form = TransactionForm(request.POST, prefix='income')
            income_form.fields['category'].queryset = Category.objects.filter(type='income')
            if income_form.is_valid():
                transaction = income_form.save()
                messages.success(request, f'Income "{transaction.description}" has been added successfully.')
                return redirect('transaction_list')
    
    return render(request, 'expenses/transaction_list.html', {
        'expenses': expenses,
        'incomes': incomes,
        'total_expense': total_expense,
        'total_income': total_income,
        'balance': balance,
        'expense_form': expense_form,
        'income_form': income_form,
    })


# User vào /add/ (GET) → Hiển thị form trống
# User nhập data, bấm Submit (POST) → Validate → Lưu DB → Redirect về list
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'expenses/transaction_form.html', {
        'form': form,
        'title': 'Add Transaction'
    })

# User vào /edit/<id>/ (GET) → Hiển thị form có dữ liệu
# User sửa data, bấm Submit (POST) → Validate → Lưu DB → Redirect về list
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            updated_transaction = form.save()
            messages.success(request, f'Transaction "{updated_transaction.description}" has been updated successfully.')
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'expenses/transaction_form.html', {
        'form': form,
        'title': 'Edit Transaction'
    })

# User vào /delete/<id>/ (GET) → Hiển thị confirm delete
# User bấm OK (POST) → Xóa DB → Redirect về list
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        description = transaction.description
        transaction.delete()
        messages.success(request, f'Transaction "{description}" has been deleted successfully.')
        return redirect('transaction_list')
    return render(request, 'expenses/transaction_confirm_delete.html', {
        'transaction': transaction
    })