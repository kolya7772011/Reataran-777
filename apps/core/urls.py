from django.urls import path

from .views import GalleryListView, ImageUploadView, RestaurantInfoView

urlpatterns = [
    path('upload/image', ImageUploadView.as_view(), name='upload-image'),
    path('gallery/', GalleryListView.as_view(), name='gallery-list'),
    path('restaurant-info/', RestaurantInfoView.as_view(), name='restaurant-info'),
]
