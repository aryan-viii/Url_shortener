from django.core.management.base import BaseCommand
from django.utils import timezone

from shortener.models import Shortener


class Command(BaseCommand):
    help = "Delete short links whose expiration date has passed."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show how many links would be deleted without deleting them.",
        )

    def handle(self, *args, **options):
        expired = Shortener.objects.filter(
            expires_at__isnull=False,
            expires_at__lte=timezone.now(),
        )

        count = expired.count()

        if options["dry_run"]:
            self.stdout.write(
                self.style.WARNING(
                    f"{count} expired link(s) would be deleted (dry run)."
                )
            )
            return

        expired.delete()

        self.stdout.write(
            self.style.SUCCESS(f"Deleted {count} expired link(s).")
        )
