from rest_framework import serializers
from .models import User, Listing, Booking

class ListingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Listing
    fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Booking
    fields = '__all__'

class UserSerializers(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'
