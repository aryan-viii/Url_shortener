import qrcode

from io import BytesIO
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.utils import timezone

from .models import Shortener
from .throttling import throttle


class HomeView(TemplateView):
    template_name = "shortener/home.html"


@method_decorator(throttle(limit=60, window_seconds=60), name="get")
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


@method_decorator(throttle(limit=30, window_seconds=60), name="get")
class QRCodeView(View):
    def get(self, request, short_code):
        obj = get_object_or_404(
            Shortener,
            short_code=short_code
        )

        # QR codes only need to change if the short link itself changes,
        # so cache the generated PNG instead of re-rendering it on every
        # request (QR generation is comparatively expensive for a link
        # that might get shared and hit thousands of times).
        cache_key = f"qr-code:{obj.short_code}"
        png_bytes = cache.get(cache_key)

        if png_bytes is None:
            short_url = request.build_absolute_uri(
                f"/{obj.short_code}/"
            )

            qr = qrcode.make(short_url)

            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            png_bytes = buffer.getvalue()

            cache.set(cache_key, png_bytes, timeout=60 * 60 * 24)

        return HttpResponse(
            png_bytes,
            content_type="image/png"
        )
