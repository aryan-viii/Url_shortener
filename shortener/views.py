from django.shortcuts import get_object_or_404, redirect
from django.views import View

from shortener.models import Shortener

# Create your views here.

class RedirectView(View):
    def get(self, request, short_code):
        obj = get_object_or_404(Shortener, short_code=short_code)

        obj.access_count += 1
        obj.save(update_fields=["access_count"])
        
        return redirect(obj.url)