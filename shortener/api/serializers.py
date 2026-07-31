from django.core.validators import RegexValidator
from rest_framework import serializers

from shortener.models import Shortener


short_code_validator = RegexValidator(
    regex=r"^[A-Za-z0-9_-]+$",
    message="Short codes may only contain letters, numbers, hyphens, and underscores."
)


class ShortenerSerializer(serializers.ModelSerializer):
    short_code = serializers.CharField(
        required=False,
        max_length=8,
        validators=[short_code_validator],
    )

    class Meta:
        model = Shortener
        fields = "__all__"
        # NOTE: short_code is intentionally NOT listed here. It is declared
        # explicitly above, and DRF ignores read_only_fields for any field
        # that is explicitly declared on the serializer -- listing it here
        # would be a no-op. Its "read-only after creation" behavior is
        # enforced entirely by validate_short_code() below.
        read_only_fields = (
            "id",
            "access_count",
            "created_at",
            "updated_at",
        )

    def validate_short_code(self, value):

        if self.instance:
            if value != self.instance.short_code:
                raise serializers.ValidationError(
                    "Short code cannot be changed after creation."
                )

            return value

        if Shortener.objects.filter(short_code=value).exists():
            raise serializers.ValidationError(
                "This short code is already taken."
            )

        return value
