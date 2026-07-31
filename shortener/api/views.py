from rest_framework import generics
from rest_framework.response import Response

from shortener.models import Shortener
from .serializers import ShortenerSerializer


class ShortenerListCreateView(generics.ListCreateAPIView):
    queryset = Shortener.objects.all()
    serializer_class = ShortenerSerializer


class ShortenerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shortener.objects.all()
    serializer_class = ShortenerSerializer
    lookup_field = "short_code"


class ShortenerStatsView(generics.RetrieveAPIView):
    queryset = Shortener.objects.all()
    serializer_class = ShortenerSerializer
    lookup_field = "short_code"