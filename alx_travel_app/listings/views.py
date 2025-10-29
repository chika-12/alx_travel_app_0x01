from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import ListingSerializer, BookingSerializer, UserSerializers, PaymentSerializer
from .models import Listing, User, Booking, Payment
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from dotenv import load_dotenv
import json
import requests, uuid, os
from django.shortcuts import redirect
load_dotenv()

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
      return Response(list_prop.data, status=status.HTTP_201_CREATED)
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
  
@csrf_exempt
def initialize_payment(request):
  if request.method == 'POST':
    try:
      input_val = json.loads(request.body)
    except json.JSONDecodeError:
      return JsonResponse({"error": "Invalid or missing JSON body"}, status=400)
    
    if not input_val.get('first_name') or not input_val.get('last_name'):
      return JsonResponse({"First and last name required"}, status=400)
    
    if not input_val.get('email'):
      return JsonResponse({"Email required"}, status=400)
    
    email = input_val.get('email')
    first_name = input_val.get('first_name')
    last_name = input_val.get('last_name')
    amount = input_val.get('amount')
    trx_ref = str(uuid.uuid4())

    Payment.objects.create(first_name=first_name, last_name=last_name, trx_ref=trx_ref, email=email, amount=amount)
    headers = {
      "Authorization": f"Bearer {os.getenv('CHAPA_SECRET_KEY')}",
      "Content-type": "application/json"
    }

    data ={
      "amount" : amount,
      "first_name": first_name,
      "last_name" : last_name,
      "trx_ref": trx_ref,
      "email": email,
      "currency": "ETB",
      "callback_url": "http://localhost:8000/verify-payment/"
    }
    
    response = requests.post("https://api.chapa.co/v1/transaction/initialize", json=data, headers=headers)
    res_data = response.json()
    print(res_data)
    print("Chapa key:", os.getenv('CHAPA_SECRET_KEY'))

    if not res_data.get('data'):
      return JsonResponse({"error": res_data.get('message', 'Transaction not successful')}, status=400)

    return JsonResponse({
      "status": "success",
      "message": "Hosted Link",
      "trx_ref": trx_ref,
      "data": res_data['data']['checkout_url']
    }, status=200)
  

@csrf_exempt
def verify_payment(request):
  if request.method == 'GET':
    #body = json.loads(request.body)
    trx_ref = request.GET.get('trx_ref')

    if not trx_ref:
      return JsonResponse({"error": "trx_ref missing"})
    
    headers = {"Authorization": f"Bearer {os.getenv('CHAPA_SECRET_KEY')}"}
    response = requests.get(f"https://api.chapa.co/v1/transaction/verify/{trx_ref}", headers=headers)
    res_data = response.json()

    try:
      payment = Payment.objects.get(trx_ref=trx_ref)
    except Payment.DoesNotExist:
      return JsonResponse({"error": "data not found"})
    
    # if not res_data['data']:
    #   return JsonResponse({"error": "Payment not verified"})
    if res_data['status'] == 'success':
      payment.status = 'success'
      payment.save()
      return JsonResponse({"success": "Payment Successful 🎉"})
    else:
      payment.status = 'failed'
      payment.save()
      return JsonResponse({"error":"Payment Failed ❌"})
  return JsonResponse({"error": "Invalid request method"}, status=405)

                    
class PaymentViewset(viewsets.ReadOnlyModelViewSet):
  queryset = Payment.objects.all()
  serializer_class = PaymentSerializer

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializers

