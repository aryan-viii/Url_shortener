from django.urls import path
from .views import ShortenerCreateView, ShortenerRetrieveView

urlpatterns = [
    path('shorten/', ShortenerCreateView.as_view(), name='shorten'),
    path('shorten/<str:short_code>/', ShortenerRetrieveView.as_view(), name='retrieve'),
]