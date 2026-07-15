"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.conf import settings
from django.conf.urls.static import static
import os

FRONTEND_DIR = os.path.join(settings.BASE_DIR, 'static', 'frontend')


urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("accounts/", include("apps.accounts.urls")),
    path("contact/", include("apps.contact.urls")),
    path("menu/", include("apps.menu.urls")),
    path("news/", include("apps.news.urls")),
    path("orders/", include("apps.orders.urls")),
    path("core/", include("apps.core.urls")),

    # ---------- Frontend sahifalar ----------
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("menu-page", TemplateView.as_view(template_name="menu.html"), name="menu-page"),
    path("login", TemplateView.as_view(template_name="login.html"), name="login-page"),
    path("register", TemplateView.as_view(template_name="register.html"), name="register-page"),
    path("news-page", TemplateView.as_view(template_name="news.html"), name="news-page"),
    path("about", TemplateView.as_view(template_name="about.html"), name="about-page"),
    path("contact-page", TemplateView.as_view(template_name="contact.html"), name="contact-page"),
    path("admin-panel", TemplateView.as_view(template_name="admin-panel.html"), name="admin-page"),
]

# Frontend CSS/JS/rasmlarni root level da xizmat qilish
# HTML fayllar nisbiy path ishlatadi (href="globals.css"), shuning uchun root da kerak
urlpatterns += [
    re_path(r'^(?P<path>.*\.(css|js|png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf|eot|webp|md))$',
            serve, {'document_root': FRONTEND_DIR}),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)