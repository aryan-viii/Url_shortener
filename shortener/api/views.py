from rest_framework import generics
from shortener.models import Shortener
from .serializers import ShortenerSerializer


class ShortenerCreateView(generics.CreateAPIView):
    queryset = Shortener.objects.all()
    serializer_class = ShortenerSerializer