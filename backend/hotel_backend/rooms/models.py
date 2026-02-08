from django.db import models

# Create your models here.

class Room(models.Model):
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
    # المعلومات الأساسية
    room_number = models.CharField(max_length=10, unique=True,verbose_name='رقم الغرفة')
    floor = models.IntegerField(default=0,verbose_name='الطابق')
    is_active = models.BooleanField(default=True,verbose_name='التوفر')
    # السعة والأسعار
    capacity = models.IntegerField(default=2,verbose_name='السعة')
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="سعر الليلة")
    
    # كيف نكتب الحقول التالية؟
    adult_capacity = models.IntegerField(default=2,verbose_name='أماكن الكبار')
    children_capacity = models.IntegerField(default=1,verbose_name='أماكن الصغار') 
    # Amenities
    has_wifi = models.BooleanField(default=True,verbose_name="الأنترنت wifi")
    has_air_condition = models.BooleanField(default=True,verbose_name='مكيف الهواء')
    has_tv = models.BooleanField(default=True,verbose_name="التلفاز")
    # type:
    room_type = models.CharField(
        max_length=20, 
        choices=ROOM_TYPES, 
        default='single',
          verbose_name='نوع الغرفة'  # هنا نحدد الخيار الافتراضي
    )
    room_status = models.CharField(
        max_length=20, 
        choices=ROOM_STATUS, 
        default='available',
         verbose_name='حالة الغرفة' # هنا نحدد الخيار الافتراضي
    )
    image = models.ImageField(upload_to='rooms/', null=True, blank=True,verbose_name="صور")

    def __str__(self):
        return f"{self.room_number} - {self.room_type}"
    class Meta:
        verbose_name = "الغرفة"
        verbose_name_plural = "الغرف"