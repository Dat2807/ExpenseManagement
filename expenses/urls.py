from django.urls import path
from .views import transaction_views, category_views, dashboard_views, monthly_views

urlpatterns = [
    # Dashboard
    path('', dashboard_views.dashboard_home, name='dashboard_home'),
    
    # Monthly Budget
    path('monthly/', monthly_views.monthly_list, name='monthly_list'),
    path('monthly/create/', monthly_views.month_create, name='month_create'),
    path('monthly/<int:year>/<int:month>/', monthly_views.month_detail, name='month_detail'),
    path('monthly/<int:year>/<int:month>/budget/<int:category_id>/', monthly_views.category_budget_update, name='category_budget_update'),
    path('monthly/<int:year>/<int:month>/delete/', monthly_views.month_delete, name='month_delete'),
    
    # Transactions (keep for backward compatibility, will be integrated into monthly detail later)
    path('transactions/', transaction_views.transaction_list, name='transaction_list'),
    path('transactions/add/<str:type>/', transaction_views.transaction_create_by_type, name='transaction_create_by_type'),
    path('transactions/edit/<int:pk>/', transaction_views.transaction_update, name='transaction_update'),
    path('transactions/delete/<int:pk>/', transaction_views.transaction_delete, name='transaction_delete'),
    
    # Categories
    path('categories/', category_views.category_list, name='category_list'),
    path('categories/add/', category_views.category_create, name='category_create'),
    path('categories/edit/<int:pk>/', category_views.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', category_views.category_delete, name='category_delete'),
]