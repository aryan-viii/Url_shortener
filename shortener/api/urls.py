from django.urls import path
from .views import ShortenerCreateView

urlpatterns = [
    path('shorten/', ShortenerCreateView.as_view(), name='shorten'),
]