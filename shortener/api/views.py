from rest_framework import generics
from rest_framework.response import Response

from shortener.models import Shortener
from .serializers import ShortenerSerializer


class ShortenerCreateView(generics.CreateAPIView):
    queryset = Shortener.objects.all()
    serializer_class = ShortenerSerializer


class ShortenerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shortener.objects.all()
    serializer_class = ShortenerSerializer
    lookup_field = "short_code"

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()

        obj.access_count += 1
        obj.save()

        serializer = self.get_serializer(obj)

        return Response(serializer.data)