from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"users",views.UserViewSet, basename="users")
urlpatterns = [
  path("listings/", views.listings, name='listings'),
  path("listing/<str:pk>", views.listing_details, name="listing_details")
] + router.urls