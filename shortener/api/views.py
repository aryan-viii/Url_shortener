from rest_framework import generics, filters
from rest_framework.response import Response

from shortener.models import Shortener
from .serializers import ShortenerSerializer


class ShortenerListCreateView(generics.ListCreateAPIView):
    queryset = Shortener.objects.all().order_by("-created_at")
    serializer_class = ShortenerSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter,]
    search_fields = ["url", "short_code"]
    ordering_fields = ["created_at", "access_count",]


class ShortenerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shortener.objects.all()
    serializer_class = ShortenerSerializer
    lookup_field = "short_code"


class ShortenerStatsView(generics.RetrieveAPIView):
    queryset = Shortener.objects.all()
    serializer_class = ShortenerSerializer
    lookup_field = "short_code"