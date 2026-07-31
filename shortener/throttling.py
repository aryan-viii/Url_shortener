"""
Small, dependency-free rate limiting for plain Django views.

The DRF API already has AnonRateThrottle applied, but the public
redirect and QR-code views bypass DRF entirely, so they were previously
unthrottled. This uses Django's cache framework (works out of the box
with the default LocMemCache, no extra service required) to cap
requests per client IP.
"""

from functools import wraps

from django.core.cache import cache
from django.http import HttpResponse


def throttle(limit=60, window_seconds=60):
    """
    Limit a view to `limit` requests per `window_seconds` per client IP.

    Not suitable for multi-process/multi-server deployments without a
    shared cache backend (e.g. Redis/Memcached) configured in settings,
    but it's a reasonable default for a small deployment or portfolio
    project, and upgrading later just means changing the CACHES setting.
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            client_ip = request.META.get("REMOTE_ADDR", "unknown")
            cache_key = f"throttle:{view_func.__name__}:{client_ip}"

            request_count = cache.get(cache_key, 0)

            if request_count >= limit:
                return HttpResponse(
                    "Too many requests. Please try again shortly.",
                    status=429,
                )

            # First hit in the window sets the expiry; later hits just
            # increment the existing counter.
            if request_count == 0:
                cache.set(cache_key, 1, timeout=window_seconds)
            else:
                cache.incr(cache_key)

            return view_func(request, *args, **kwargs)

        return wrapped

    return decorator
