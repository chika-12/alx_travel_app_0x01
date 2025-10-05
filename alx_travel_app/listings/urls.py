from django.urls import path
from . import views
urlpatterns = [
  path("listings/", views.listings, name='listings'),
  path("listing/<str:pk>", views.listing_details, name="listing_details")
]