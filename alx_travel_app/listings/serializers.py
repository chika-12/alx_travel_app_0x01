from rest_framework import serializers
from .models import User, Listing, Booking, Payment
from django.contrib.auth.hashers import make_password

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
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
    validated_data["password"] = make_password(validated_data["password"])
    return super().create(validated_data)
    
  def update(self, instance, validated_data):
    # Only hash password if it’s being updated
    password = validated_data.get('password', None)
    if password:
      validated_data['password'] = make_password(password)
    return super().update(instance, validated_data)

class PaymentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Payment
    fields = '__all__'