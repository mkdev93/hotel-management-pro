from django.contrib import admin
from .models import Guest,Booking

# Register your models here.
@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'id_number')
    search_fields = ('first_name', 'last_name', 'id_number')
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest', 'room', 'check_in_date', 'check_out_date', 'status', 'total_price')
    list_filter = ('status', 'check_in_date')
    search_fields = ('guest__first_name', 'guest__last_name', 'room__room_number')