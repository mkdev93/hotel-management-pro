from django.shortcuts import render
from .models import Room
# Create your views here.
def room_list(request):
    rooms = Room.objects.all()
    context = {
        'rooms':rooms
    }
    return render(request,'rooms/room_list.html',context)
