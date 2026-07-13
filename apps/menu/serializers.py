from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductToggleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
<<<<<<< Updated upstream
        fields = ['is_active']
=======
        fields = ('is_active',)


class AdminProductSerializer(serializers.ModelSerializer):
    """Admin uchun mahsulot qo'shish/tahrirlash (FormData bilan)."""

    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'category', 'category_name',
                  'image', 'is_active', 'is_popular', 'created_at')
        read_only_fields = ('id', 'created_at')


# ---------- Comment ----------

class ProductCommentCreateSerializer(serializers.ModelSerializer):
    """
    Izoh qoldirish uchun — product maydoni view ichida
    (perform_create'da) avtomatik qo'yiladi, shuning uchun bu yerda yo'q.
    """

    class Meta:
        model = ProductComment
        fields = ('id', 'text', 'created_at')
        read_only_fields = ('id', 'created_at')


class ProductCommentSerializer(serializers.ModelSerializer):
    """To'liq ko'rinish — admin uchun (o'chirish, ro'yxat)."""

    class Meta:
        model = ProductComment
        fields = ('id', 'product', 'text', 'created_at')


# ---------- Like / Dislike ----------

class ProductLikeSerializer(serializers.Serializer):
    """
    ProductLikeToggleView faqat is_like qiymatini tekshirish uchun
    ishlatadi — model bilan bog'liq emas, shuning uchun oddiy Serializer.
    """

    is_like = serializers.BooleanField()


# ---------- Rating ----------

class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = ('id', 'product', 'user', 'score')
        read_only_fields = ('id', 'product', 'user')

    def validate_score(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Baho 1 dan 5 gacha bo'lishi kerak.")
        return value
>>>>>>> Stashed changes
