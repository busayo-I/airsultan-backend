from rest_framework import serializers
from .models import Offer


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Offer
        fields = [
            'id', 'title', 'type', 'provider',
            'duration', 'price', 'banner_image',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class OfferCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Offer
        fields = [
            'title', 'type', 'provider',
            'duration', 'price', 'banner_image', 'status'
        ]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value