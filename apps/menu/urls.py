from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('categories', views.CategoryListView.as_view(), name='category-list'),
    path('products', views.ProductListView.as_view(), name='product-list'),
    path('products/popular', views.PopularProductListView.as_view(), name='product-popular'),
    path('products/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    # Admin
    path('admin/categories', views.AdminCategoryCreateView.as_view(), name='admin-category-create'),
    path('admin/categories/<int:pk>', views.AdminCategoryUpdateView.as_view(), name='admin-category-update'),
    path('admin/categories/<int:pk>/delete', views.AdminCategoryDeleteView.as_view(), name='admin-category-delete'),
<<<<<<< Updated upstream
    path('admin/products', views.AdminProductCreateView.as_view(), name='admin-product-create'),
=======
    # ---------- Admin: Product ----------
    path('admin/products', views.AdminProductListView.as_view(), name='admin-product-list'),
>>>>>>> Stashed changes
    path('admin/products/<int:pk>', views.AdminProductUpdateView.as_view(), name='admin-product-update'),
    path('admin/products/<int:pk>/delete', views.AdminProductDeleteView.as_view(), name='admin-product-delete'),
    path('admin/products/<int:pk>/toggle', views.AdminProductToggleView.as_view(), name='admin-product-toggle'),
]
