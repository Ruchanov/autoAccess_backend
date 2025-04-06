from .models import Car
from django.contrib.auth.models import User
from rest_framework import serializers


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        else:
            return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image_url'] = self.get_image_url(instance)
        return representation