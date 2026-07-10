from django.urls import path

from .views import (
    AdminOrderDetailView,
    AdminOrderListView,
    AdminOrderStatusUpdateView,
    AdminSalesChannelStatsView,
    AdminSalesStatsView,
    AdminTopProductsStatsView,
    OrderCreateView,
)

urlpatterns = [
    path('orders', OrderCreateView.as_view(), name='order-create'),
    path('admin/orders', AdminOrderListView.as_view(), name='admin-order-list'),
    path('admin/orders/<int:pk>', AdminOrderDetailView.as_view(), name='admin-order-detail'),
    path('admin/orders/<int:pk>/status', AdminOrderStatusUpdateView.as_view(), name='admin-order-status'),
    path('admin/stats/sales', AdminSalesStatsView.as_view(), name='admin-stats-sales'),
    path('admin/stats/top-products', AdminTopProductsStatsView.as_view(), name='admin-stats-top-products'),
    path('admin/stats/sales-channel', AdminSalesChannelStatsView.as_view(), name='admin-stats-sales-channel'),
]
