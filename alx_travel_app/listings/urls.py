from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"users",views.UserViewSet, basename="users")
router.register(r"payment", views.PaymentViewset, basename="payment")
urlpatterns = [
  path("listings/", views.listings, name='listings'),
  path("listings/<str:pk>/", views.listing_details, name="listing_details"),
  path("initialize_payment/", views.initialize_payment, name="initialize_payment"),
  path("verify_payment/", views.verify_payment, name="verify_payment")
] + router.urls