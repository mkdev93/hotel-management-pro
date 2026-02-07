from django.db import models

# Create your models here.
ROOM_TYPES = [
    ('single', 'Single Room'),
    ('double', 'Double Room'),
    ('suite', 'Suite'),
]
ROOM_STATUS = [
    ('available', 'Available'),
    ('occupied', 'Occupied'),
    ('cleaning', 'Cleaning'),
    ('maintenance', 'Under Maintenance'),
]
class Room(models.Model):
    # المعلومات الأساسية
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=20) 
    floor = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    # السعة والأسعار
    capacity = models.IntegerField(default=2)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    
    # كيف نكتب الحقول التالية؟
    adult_capacity = models.IntegerField(default=2)
    children_capacity = models.IntegerField(default=1) 
    # Amenities
    has_wifi = models.BooleanField(default=True)
    has_air_condition = models.BooleanField(default=True)
    has_tv = models.BooleanField(default=True)
    # type:
    room_type = models.CharField(
        max_length=20, 
        choices=ROOM_TYPES, 
        default='single'  # هنا نحدد الخيار الافتراضي
    )
    room_status = models.CharField(
        max_length=20, 
        choices=ROOM_STATUS, 
        default='available'  # هنا نحدد الخيار الافتراضي
    )
    image = models.ImageField(upload_to='rooms/', null=True, blank=True)