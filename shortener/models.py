from django.db import models

# Create your models here.

class Shortener(models.Model):
    url = models.URLField(max_length=200)
    short_code = models.CharField(max_length=8, unique=True)
    access_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.short_code