from django.db import models
from rooms.models import Room
from django.core.exceptions import ValidationError # لاستخدامها في "صافرة الإنذار"
from django.utils import timezone
# Create your models here.
class Guest(models.Model):
    # قائمة أنواع الهوية
    ID_CARD_TYPES = [
        ('national_id', 'بطاقة تعريف وطنية'),
        ('passport', 'جواز سفر'),
        ('driver_license', 'رخصة سياقة'),
    ]
    # المعلومات الشخصية
    first_name = models.CharField(max_length=50, verbose_name="الإسم")
    last_name = models.CharField(max_length=50, verbose_name="اللقب")
    date_of_birth = models.DateField(verbose_name="تاريخ الميلاد")
    place_of_birth = models.CharField(max_length=100, verbose_name="مكان الميلاد")
    address = models.TextField(verbose_name="عنوان السكن")
    nationality = models.CharField(max_length=50, default='جزائري', verbose_name="الجنسية")
    phone_number = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    # بيانات الهوية
    id_type = models.CharField(
        max_length=20, 
        choices=ID_CARD_TYPES, 
        default='national_id',
        verbose_name="نوع الهوية"
    )
    id_number = models.CharField(max_length=50, unique=True, verbose_name="رقم الهوية")
    id_issue_date = models.DateField(verbose_name="تاريخ صدور الهوية")
    id_issuing_authority = models.CharField(max_length=100, verbose_name="السلطة الصادرة للهوية")
    # التوقيت
    created_at = models.DateTimeField(auto_now_add=True)
    def clean(self):
        today = timezone.now().date()
        if self.id_issue_date and self.id_issue_date > today:
            raise ValidationError("تاريخ إصدار الهوية يجب أن يكون في الماضي.")
        limit_date= today.replace(year=today.year - 18)
        if self.date_of_birth > limit_date:
            raise ValidationError("يجب أن يكون عمر النزيل 18 سنة على الأقل لإتمام الحجز.")

    def save(self, *args, **kwargs):
        self.clean() # استدعاء الحارس قبل الحفظ
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    class Meta:
        verbose_name = "النزيل"
        verbose_name_plural = "النزلاء"
    

class Booking(models.Model):
    BOOKING_STATUS = [
        ('pending', 'قيد الانتظار'),
        ('confirmed', 'مؤكد'),
        ('cancelled', 'ملغي'),
        ('checked_out', 'تم المغادرة'),
    ]
    # الربط مع النزيل والغرفة
    guest = models.ForeignKey(Guest,on_delete=models.CASCADE,related_name='booking_guest',verbose_name="النزيل")
    room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name='booking_room', verbose_name='الغرفة')
    # التواريخ
    check_in_date = models.DateField(verbose_name="تاريخ الدخول")
    check_out_date = models.DateField(verbose_name="تاريخ الخروج")
    # تفاصيل مالية وحالة
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر الإجمالي")
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending', verbose_name="حالة الحجز")
    created_at = models.DateTimeField(auto_now_add=True)
    def clean(self):
        today = timezone.now().date()
        if self.check_in_date < today:
            raise ValidationError("لا يمكن حجز الغرفة بتاريخ قديم، يجب أن يبدأ الحجز من اليوم فصاعداً.")
        if self.check_out_date < self.check_in_date:
            raise ValidationError("تاريخ الخروج يجب أن يكون بعد تاريخ الدخول (على الأقل ليلة واحدة).")
        # ✅ التحقق من تداخل الحجوزات
        overlapping_bookings = Booking.objects.filter(
            room=self.room,
            check_in_date__lt=self.check_out_date,
            check_out_date__gt=self.check_in_date
        ).exclude(pk=self.pk)

        if overlapping_bookings.exists():
            raise ValidationError("هذه الغرفة محجوزة في هذا التاريخ.")

        
    def __str__(self):
        return f"حجز {self.guest} - غرفة {self.room.room_number}"
    class Meta:
        verbose_name = "حجز"
        verbose_name_plural = "الحجوزات"