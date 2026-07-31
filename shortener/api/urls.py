from django.urls import path
from shortener.views import QRCodeView
from .views import ShortenerListCreateView, ShortenerDetailView, ShortenerStatsView

urlpatterns = [
    path('shorten/', ShortenerListCreateView.as_view(), name='shorten'),
    path('shorten/<str:short_code>/stats/', ShortenerStatsView.as_view(), name='stats'),
    path("shorten/<str:short_code>/qr/", QRCodeView.as_view(), name="qr-code"),
    path('shorten/<str:short_code>/', ShortenerDetailView.as_view(), name='retrieve'),
]