from rest_framework import serializers

from shortener.models import Shortener

class ShortenerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shortener
        fields = '__all__'
        read_only_fields = ('id', 
                            'short_code', 
                            'access_count', 
                            'created_at', 
                            'updated_at', 
                            )