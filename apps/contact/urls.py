from django.urls import path

from .views import (
    AdminMessageDeleteView,
    AdminMessageListView,
    AdminMessageMarkReadView,
    ContactMessageCreateView,
    NewsletterSubscribeView,
    TestimonialListView,
)

urlpatterns = [
    path('contact', ContactMessageCreateView.as_view(), name='contact-create'),
    path('admin/messages', AdminMessageListView.as_view(), name='admin-message-list'),
    path('admin/messages/<int:id>/read', AdminMessageMarkReadView.as_view(), name='admin-message-read'),
    path('admin/messages/<int:id>', AdminMessageDeleteView.as_view(), name='admin-message-delete'),
    path('newsletter/subscribe', NewsletterSubscribeView.as_view(), name='newsletter-subscribe'),
    path('testimonials', TestimonialListView.as_view(), name='testimonial-list'),
]
