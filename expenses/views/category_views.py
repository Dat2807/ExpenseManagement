from django.shortcuts import render, redirect, get_object_or_404
from ..models import Category
from ..forms import CategoryForm

# Flow: User vào /categories/ → lấy all categories → render ra HTML
def category_list(request):
    income_categories = Category.objects.filter(type='income')
    expense_categories = Category.objects.filter(type='expense')
    return render(request, 'category/category_list.html', {
        'income_categories': income_categories,
        'expense_categories': expense_categories
    })


# User vào /categories/add/ (GET) → Hiển thị form trống
# User nhập data, bấm Submit (POST) → Validate → Lưu DB → Redirect về list
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category/category_form.html', {
        'form': form,
        'title': 'Add Category'
    })


# User vào /categories/edit/<id>/ (GET) → Hiển thị form có dữ liệu
# User sửa data, bấm Submit (POST) → Validate → Lưu DB → Redirect về list
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category/category_form.html', {
        'form': form,
        'title': 'Edit Category'
    })

# User vào /categories/delete/<id>/ (GET) → Hiển thị confirm delete
# User bấm OK (POST) → Xóa DB → Redirect về list
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'category/category_confirm_delete.html', {
        'category': category
    })