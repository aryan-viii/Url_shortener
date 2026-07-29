from rest_framework import generics
from shortener.models import Shortener
from .serializers import ShortenerSerializer


class ShortenerCreateView(generics.CreateAPIView):
    queryset = Shortener.objects.all()
    serializer_class = ShortenerSerializer


class ShortenerRetrieveView(generics.RetrieveAPIView):
    queryset = Shortener.objects.all()
    serializer_class = ShortenerSerializer
    lookup_field = "short_code"

    def get_object(self):
        obj = super().get_object()

        obj.access_count += 1
        obj.save()

        return obj