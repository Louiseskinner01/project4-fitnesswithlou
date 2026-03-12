# bookings/views.py
from django.shortcuts import render, redirect
from .forms import BookingForm
from django.contrib.auth.decorators import login_required
from .models import Booking
from datetime import date
from django.contrib import messages



# Create your views here.

@login_required
def bookings_list(request):
    # All bookings for the logged-in user
    bookings = Booking.objects.filter(user=request.user).order_by('class_date', 'class_time')

    # Separate upcoming and past bookings
    upcoming_bookings = bookings.filter(class_date__gte=date.today())
    past_bookings = bookings.filter(class_date__lt=date.today())

    # Context dictionary to send to the template
    context = {
        'bookings': bookings,
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
        'total_bookings': bookings.count(),
    }

    # Render the template with context (load the HTML template)
    return render(request, 'bookings/bookings.html', context)


# Requires the user to be logged in
@login_required
def create_booking(request):

    if request.method == 'POST':
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.user= request.user
            booking.save()

            return redirect('bookings')

    else:
        form = BookingForm()

    context = {
        'form' : form,
            }

    return render(request, 'bookings/booking_form.html', context)

    messages.success(request, "Your booking has successfully ben created!")