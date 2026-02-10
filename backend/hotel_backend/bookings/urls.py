from django.urls import path
from .views import book_room,booking_list

urlpatterns=[
    path('new/',book_room,name='book_room'),
    path('list/',booking_list,name="booking_list")
]