from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import UserLoginView, dashboard, register, transaction_create, transaction_delete, transaction_detail, transaction_list, transaction_update

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('transactions/', transaction_list, name='transaction_list'),
    path('transactions/add/', transaction_create, name='transaction_create'),
    path('transactions/<int:pk>/', transaction_detail, name='transaction_detail'),
    path('transactions/<int:pk>/edit/', transaction_update, name='transaction_update'),
    path('transactions/<int:pk>/delete/', transaction_delete, name='transaction_delete'),
]
