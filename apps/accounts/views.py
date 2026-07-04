from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import (
    AdminTokenObtainPairSerializer,
    EaturkishTokenObtainPairSerializer,
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register — Mijoz ro'yxatdan o'tishi."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    """POST /api/auth/login — Login, JWT token qaytaradi."""

    permission_classes = [AllowAny]
    serializer_class = EaturkishTokenObtainPairSerializer


class AdminLoginView(TokenObtainPairView):
    """POST /api/admin/auth/login — Admin login (role=admin tekshiruvi bilan)."""

    permission_classes = [AllowAny]
    serializer_class = AdminTokenObtainPairSerializer


class RefreshView(TokenRefreshView):
    """POST /api/auth/refresh — Tokenni yangilash."""

    permission_classes = [AllowAny]


class LogoutView(APIView):
    """
    POST /api/auth/logout — Chiqish.
    Refresh tokenni blacklist qilib, uni qayta ishlatib bo'lmaydigan holga
    keltiradi.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'detail': "refresh token yuborilishi shart."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response(
                {'detail': "Token yaroqsiz yoki muddati o'tgan."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({'detail': "Muvaffaqiyatli chiqildi."}, status=status.HTTP_200_OK)


class MeView(generics.RetrieveAPIView):
    """GET /api/auth/me — Joriy foydalanuvchi ma'lumotlari."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
