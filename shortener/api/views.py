from django.db import IntegrityError, transaction
from rest_framework import generics, filters
from rest_framework.exceptions import ValidationError

from shortener.models import Shortener
from .serializers import ShortenerSerializer


class ShortenerListCreateView(generics.ListCreateAPIView):
    queryset = Shortener.objects.all().order_by("-created_at")
    serializer_class = ShortenerSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter,]
    search_fields = ["url", "short_code"]
    ordering_fields = ["created_at", "access_count",]

    def perform_create(self, serializer):
        # validate_short_code() already checks for an existing match, but
        # that check and this save are not atomic -- two requests with the
        # same custom short_code could both pass validation and then race
        # each other to the DB. The unique=True constraint on the model
        # still protects data integrity, but without this try/except the
        # loser of the race would surface as an unhandled 500 IntegrityError
        # instead of a clean 400 response.
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError:
            raise ValidationError(
                {"short_code": "This short code is already taken."}
            )


class ShortenerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shortener.objects.all()
    serializer_class = ShortenerSerializer
    lookup_field = "short_code"


class ShortenerStatsView(generics.RetrieveAPIView):
    queryset = Shortener.objects.all()
    serializer_class = ShortenerSerializer
    lookup_field = "short_code"
