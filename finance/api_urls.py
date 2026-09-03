from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DashboardSummaryView, TransactionViewSet

router = DefaultRouter()
router.register('transactions', TransactionViewSet, basename='api-transactions')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', DashboardSummaryView.as_view(), name='api-dashboard'),
]
