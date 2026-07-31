from django.urls import path
from .views import HomeView, RedirectView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('<str:short_code>/', RedirectView.as_view(), name='redirect-url'),
]