from django.urls import path
from .views import ShortenerCreateView, ShortenerDetailView, ShortenerStatsView

urlpatterns = [
    path('shorten/', ShortenerCreateView.as_view(), name='shorten'),
    path('shorten/<str:short_code>/stats/', ShortenerStatsView.as_view(), name='stats'),
    path('shorten/<str:short_code>/', ShortenerDetailView.as_view(), name='retrieve'),
]