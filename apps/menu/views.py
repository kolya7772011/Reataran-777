from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.accounts.permissions import IsAdminRole
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductToggleSerializer


# ---------- Public ----------

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True)
        category_id = self.request.query_params.get('category_id')
        if category_id:
            qs = qs.filter(category_id=category_id)
        return qs


class PopularProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True, is_popular=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


# ---------- Admin: Category ----------

class AdminCategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminRole]


class AdminCategoryUpdateView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminRole]


class AdminCategoryDeleteView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminRole]


# ---------- Admin: Product ----------

class AdminProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminRole]


class AdminProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminRole]


class AdminProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminRole]


class AdminProductToggleView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductToggleSerializer
    permission_classes = [IsAdminRole]