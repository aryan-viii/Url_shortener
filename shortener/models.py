from django.db import models
import string
import secrets


class Shortener(models.Model):
    url = models.URLField(max_length=200)
    short_code = models.CharField(max_length=8, unique=True)
    access_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_short_code(self):
        characters = string.ascii_letters + string.digits

        while True:
            code = ''.join(secrets.choice(characters) for _ in range(6))

            if not Shortener.objects.filter(short_code=code).exists():
                return code

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self.generate_short_code()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.short_code