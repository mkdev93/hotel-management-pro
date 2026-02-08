from django.contrib import admin
from .models import Room

# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number','room_type','price_per_night','room_status','is_active']
    list_filter = ['room_type','room_status','is_active']
    search_fields = ['room_number',]

# admin.site.register(Room)
