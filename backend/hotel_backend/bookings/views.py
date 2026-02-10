from django.shortcuts import render,redirect
from .forms import BookingForm
from .models import Booking
from django.contrib import messages
# Create your views here.
def book_room(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            messages.success(request, f'تم الحجز بنجاح! السعر: {booking.total_price}')
            return redirect('room_list')
    else:
        # --- التعديل الجديد يبدأ هنا ---
        # نحاول التقاط رقم الغرفة من الرابط (إذا وجد)
        room_id = request.GET.get('room') 
        
        if room_id:
            # إذا وجدنا رقماً، نملأ الاستمارة به مبدئياً
            form = BookingForm(initial={'room': room_id})
        else:
            # إذا لم يوجد رقم، نعرض الاستمارة فارغة كالمعتاد
            form = BookingForm()
        # --- انتهى التعديل ---
            
    return render(request, 'bookings/book_room.html', {'form': form})

def booking_list(request):
    bookings = Booking.objects.select_related('room', 'guest').all()
    return render(request,'bookings/booking_list.html',{'bookings':bookings})