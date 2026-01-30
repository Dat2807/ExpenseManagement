from django.urls import path
from .views import transaction_views, category_views, dashboard_views

urlpatterns = [
    # Dashboard
    path('', dashboard_views.dashboard_home, name='dashboard_home'),
    
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