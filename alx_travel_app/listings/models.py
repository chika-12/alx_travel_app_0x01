from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  full_name = models.CharField(max_length=300)
  email = models.EmailField(unique=True)
  phone = models.CharField(blank=True, null=True, max_length=20)
  #profile_image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
  username = models.CharField(max_length=150, unique=True, default="user_default")


  def __str__(self):
    return self.username

class Listing(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
  title = models.CharField(max_length=255)
  slug = models.SlugField(unique=True)
  description = models.TextField()
    
  country = models.CharField(max_length=100)
  city = models.CharField(max_length=100)
  address = models.CharField(max_length=255, blank=True, null=True)
  latitude = models.FloatField(blank=True, null=True)
  longitude = models.FloatField(blank=True, null=True)
    
  price = models.DecimalField(max_digits=10, decimal_places=2)
  currency = models.CharField(max_length=10, default="USD")
  available_from = models.DateField()
  available_to = models.DateField()
  is_available = models.BooleanField(default=True)
  
  listing_type = models.CharField(max_length=50, choices=[
    ('hotel', 'Hotel'),
    ('tour', 'Tour'),
    ('apartment', 'Apartment'),
    ('resort', 'Resort'),
  ])
  amenities = models.JSONField(default=list, blank=True)
  max_guests = models.IntegerField(default=1)
  rooms = models.IntegerField(blank=True, null=True)
  duration_days = models.IntegerField(blank=True, null=True)
   
  #image = models.ImageField(upload_to='listing_images/')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
   
  def __str__(self):
    return self.title


class Booking(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.ForeignKey(User, 
    on_delete=models.CASCADE,
    related_name='bookings'
  )
  listing = models.ForeignKey(
   Listing,
    on_delete=models.CASCADE,
    related_name='bookings'
  )

  check_in_date = models.DateField()
  check_out_date = models.DateField()
  number_of_guests = models.PositiveIntegerField(default=1)

  # 💰 Payment & status
  total_price = models.DecimalField(max_digits=10, decimal_places=2)
  payment_status = models.CharField(
    max_length=20,
    choices=[
      ('pending', 'Pending'),
      ('paid', 'Paid'),
      ('cancelled', 'Cancelled'),
    ],
    default='pending'
  )
  booking_status = models.CharField(
    max_length=20,
    choices=[
      ('confirmed', 'Confirmed'),
      ('checked_in', 'Checked In'),
      ('checked_out', 'Checked Out'),
      ('cancelled', 'Cancelled'),
    ],
    default='confirmed'
  )

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"Booking by {self.user.username} for {self.listing}"
  class Meta:
    ordering = ['-created_at']

class Payment(models.Model):
  email = models.EmailField()
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length= 50)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  trx_ref = models.CharField(max_length=300, unique=True, editable=False)
  status = models.CharField(default="pending", max_length=20)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def save(self, *args, **kwargs):
    if not self.trx_ref:
      self.trx_ref = str(uuid.uuid4())
    super().save(*args, **kwargs)
  
  def __str__(self):
    return f"{self.email} {self.trx_ref} {self.status}"