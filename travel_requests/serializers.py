from rest_framework import serializers
from .models import TravelRequest


class TravelRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TravelRequest
        fields = [
            'id', 'full_name', 'email', 'phone_number',
            'destination', 'number_of_travelers',
            'travel_date', 'travel_purpose',
            'body', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class TravelRequestCreateSerializer(serializers.ModelSerializer):
    """Used by the customer-facing website to submit requests."""
    class Meta:
        model  = TravelRequest
        fields = [
            'full_name', 'email', 'phone_number',
            'destination', 'number_of_travelers',
            'travel_date', 'travel_purpose', 'body'
        ]

    def validate_number_of_travelers(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Number of travelers must be at least 1."
            )
        return value

    def validate_travel_date(self, value):
        from django.utils import timezone
        if value < timezone.now().date():
            raise serializers.ValidationError(
                "Travel date cannot be in the past."
            )
        return value