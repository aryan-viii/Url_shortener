from rest_framework import serializers

from shortener.models import Shortener

class ShortenerSerializer(serializers.ModelSerializer):
    short_code = serializers.CharField(required = False, max_length = 8)
    class Meta:
        model = Shortener
        fields = '__all__'
        read_only_fields = ('id', 
                            'short_code', 
                            'access_count', 
                            'created_at', 
                            'updated_at', 
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