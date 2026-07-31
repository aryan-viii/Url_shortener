import qrcode

from io import BytesIO
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.utils import timezone

from .models import Shortener


class RedirectView(View):
    def get(self, request, short_code):
        obj = get_object_or_404(
            Shortener,
            short_code=short_code
        )

        if obj.expires_at and obj.expires_at <= timezone.now():
            return HttpResponse(
                "This short link has expired.",
                status=410
            )

        obj.access_count += 1
        obj.save(update_fields=["access_count"])

        return redirect(obj.url)


class QRCodeView(View):
    def get(self, request, short_code):
        obj = get_object_or_404(
            Shortener,
            short_code=short_code
        )

        short_url = request.build_absolute_uri(
            f"/{obj.short_code}/"
        )

        qr = qrcode.make(short_url)

        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        return HttpResponse(
            buffer.getvalue(),
            content_type="image/png"
        )