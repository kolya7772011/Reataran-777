"""
EATURKISH — asosiy URL konfiguratsiyasi.

Har bir a'zoning mas'ul bo'lgan endpointlari mos app'ning urls.py fayliga
ajratilgan va shu yerda /api/ prefiksi bilan ulanadi.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="EATURKISH API",
        default_version='v1',
        description=(
            "EATURKISH restoran backend/admin panel API hujjatlari.\n\n"
            "**Modullar:**\n"
            "- Auth & Foydalanuvchilar (1-a'zo)\n"
            "- Kategoriyalar & Menu (2-a'zo)\n"
            "- Yangiliklar / Postlar (3-a'zo)\n"
            "- Buyurtmalar & Statistika (4-a'zo)\n"
            "- Xabarlar, Kontakt & Mijozlar (5-a'zo)\n"
            "- Umumiy Infratuzilma & Fayl yuklash (6-a'zo)\n\n"
            "Himoyalangan endpointlar uchun avval `/api/auth/login` yoki "
            "`/api/admin/auth/login` orqali token oling, so'ng yuqoridagi "
            "**Authorize** tugmasi orqali `Bearer <access_token>` ko'rinishida "
            "kiriting."
        ),
        terms_of_service="https://www.eaturkish.example/terms/",
        contact=openapi.Contact(email="dev@eaturkish.example"),
        license=openapi.License(name="Proprietary"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Swagger UI — Admin (7-a'zo) PR'larni shu orqali test qiladi
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),
    # ReDoc — muqobil, o'qish uchun qulayroq hujjat ko'rinishi
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-docs'),
    # Xom OpenAPI schema (JSON/YAML) — frontend/Postman uchun import qilish mumkin
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),

    # 1-a'zo: Auth & Foydalanuvchilar -> /api/auth/..., /api/admin/auth/...
    path('api/', include('apps.accounts.urls')),

    # 2-a'zo: Kategoriyalar & Menu -> /api/categories, /api/products, /api/admin/...
    path('api/', include('apps.menu.urls')),

    # 3-a'zo: Yangiliklar / Postlar -> /api/posts, /api/admin/posts
    path('api/', include('apps.news.urls')),

    # 4-a'zo: Buyurtmalar & Statistika -> /api/orders, /api/admin/orders, /api/admin/stats/...
    path('api/', include('apps.orders.urls')),

    # 5-a'zo: Xabarlar, Kontakt & Mijozlar -> /api/contact, /api/admin/messages, /api/newsletter, /api/testimonials
    path('api/', include('apps.contact.urls')),

    # 6-a'zo: Umumiy Infratuzilma & Fayl yuklash -> /api/upload/image, /api/gallery, /api/restaurant-info
    path('api/', include('apps.core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
