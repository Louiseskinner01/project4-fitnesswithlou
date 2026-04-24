# bookings/views.py
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from .models import Booking, ClassSession
from datetime import date
from django.contrib import messages



@login_required
def bookings_list(request):
    bookings = Booking.objects.filter(user=request.user).order_by(
        'session__class_date',
        'session__class_time'
    )

    upcoming_bookings = bookings.filter(
        session__class_date__gte=date.today()
    )

    past_bookings = bookings.filter(
        session__class_date__lt=date.today()
    )

    return render(request, 'bookings/bookings.html', {
        'bookings': bookings,
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
        'total_bookings': bookings.count(),
    })


@login_required
def timetable(request):
    sessions = ClassSession.objects.all().order_by("class_date", "class_time")

    return render(request, "bookings/classes.html", {
        "sessions": sessions
    })


@login_required
def book_session(request, session_id):
    session = get_object_or_404(ClassSession, id=session_id)

    already_booked = Booking.objects.filter(
        user=request.user,
        session=session
    ).exists()

    if already_booked:
        return redirect("bookings:bookings")

    if session.booked_count >= session.capacity:
        return redirect("bookings:timetable")

    Booking.objects.create(
        user=request.user,
        session=session
    )

    session.booked_count += 1
    session.save()

    return redirect("bookings:bookings")
    session = get_object_or_404(ClassSession, id=session_id)

    # Prevent double booking (important)
    already_booked = Booking.objects.filter(
        user=request.user,
        session=session
    ).exists()

    if already_booked:
        return redirect("bookings:bookings")

    # Optional: enforce capacity
    if session.booking_set.count() >= session.capacity:
        return redirect("bookings:classes")

    Booking.objects.create(
        user=request.user,
        session=session
    )

    # Update counter (since you're using it)
    session.booked_count += 1
    session.save()

    return redirect("bookings:bookings")