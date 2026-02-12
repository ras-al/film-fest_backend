from rest_framework import serializers
from .models import UserProfile, Ticket, Film

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['name', 'mobile_number', 'branch', 'year']

class TicketSerializer(serializers.ModelSerializer):
    film_title = serializers.ReadOnlyField(source='film.title')
    user_name = serializers.ReadOnlyField(source='user.name')
    user_mobile = serializers.ReadOnlyField(source='user.mobile_number')
    
    class Meta:
        model = Ticket
        fields = ['id', 'user_name', 'user_mobile', 'film_title', 'qr_code', 'is_checked_in']