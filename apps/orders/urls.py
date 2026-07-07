from django.urls import path

from .views import (
    AdminOrderListView,
    AdminSalesChannelStatsView,
    AdminSalesStatsView,
    AdminTopProductsStatsView,
    OrderCreateView,
)

urlpatterns = [
    path('orders', OrderCreateView.as_view(), name='order-create'),
    path('admin/orders', AdminOrderListView.as_view(), name='admin-order-list'),
    path('admin/stats/sales', AdminSalesStatsView.as_view(), name='admin-stats-sales'),
    path('admin/stats/top-products', AdminTopProductsStatsView.as_view(), name='admin-stats-top-products'),
    path('admin/stats/sales-channel', AdminSalesChannelStatsView.as_view(), name='admin-stats-sales-channel'),
]
