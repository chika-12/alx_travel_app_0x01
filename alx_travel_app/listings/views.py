from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import ListingSerializer, BookingSerializer, UserSerializers
from .models import Listing, User, Booking

@api_view(["GET", "POST"])
def listings(request):
  if request.method == "GET":
    list_prop = Listing.objects.all()
    serialized_prop = ListingSerializer(list_prop, many=True)
    return Response(serialized_prop.data, status=status.HTTP_200_OK)
  
  if request.method == "POST":
    list_prop = ListingSerializer(data=request.data)
    if list_prop.is_valid():
      list_prop.save()
      return Response(list_prop, status=status.HTTP_201_CREATED)
    else:
      return Response(list_prop.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def listing_details(request, pk):
  try:
    list_prop = Listing.objects.get(pk=pk)
  except Listing.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  if request.method == "GET":
    serialized_prop = ListingSerializer(list_prop)
    return Response(serialized_prop.data, status=status.HTTP_200_OK)
  elif request.method == "PUT":
    serialized_prop = ListingSerializer(list_prop, data=request.data)
    if serialized_prop.is_valid():
      serialized_prop.save()
      return Response(serialized_prop.data, status=status.HTTP_200_OK)
    else:
      return Response(serialized_prop.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == "DELETE":
    list_prop.delete()
    return Response(status=status.HTTP_204_NO_CONTENT) 

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializers
