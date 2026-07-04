from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking, ClassSession
from datetime import date
from django.contrib import messages


@login_required
def bookings_list(request):
    """
    Display the authenticated user's bookings split into
    upcoming and past bookings.
    Retrieves all bookings for the current user ordered by
    date and time, then filters into two separate querysets
    based on whether the class date is in the future or past.
    Requires the user to be logged in.
    """
    # Get all bookings for the current user ordered by date and time
    bookings = Booking.objects.filter(user=request.user).order_by(
        'session__class_date',
        'session__class_time'
    )

    # Filter bookings where the class date is today or in the future
    upcoming_bookings = bookings.filter(
        session__class_date__gte=date.today()
    )

    # Filter bookings where the class date has already passed
    past_bookings = bookings.filter(
        session__class_date__lt=date.today()
    )

    return render(request, 'bookings/bookings.html', {
        'bookings': bookings,
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
        # Total count displayed in the bookings summary
        'total_bookings': bookings.count(),
    })


@login_required
def timetable(request):
    """
    Display all available class sessions in chronological order.
    Retrieves all ClassSession objects ordered by date and time
    so users can browse upcoming classes and book their spot.
    Requires the user to be logged in.
    """
    # Retrieve all sessions ordered by date then time
    sessions = ClassSession.objects.all().order_by(
        "class_date",
        "class_time"
    )

    return render(request, "bookings/classes.html", {
        "sessions": sessions
    })


@login_required
def cancel_booking(request, booking_id):
    """
    Cancel an existing booking for the authenticated user.
    Retrieves the booking by ID, decrements the session's
    booked_count to free up the space, then deletes the
    booking record from the database.
    Requires the user to be logged in and to own the booking.
    """
    # Retrieve the booking ensuring it belongs to the current user
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    session = booking.session

    # Safely decrement the booked count to free up the space
    # Guard against going below 0 in case of data inconsistency
    if session.booked_count > 0:
        session.booked_count -= 1
        session.save()

    # Delete the booking record from the database
    booking.delete()

    messages.success(request, "Booking cancelled successfully.")
    return redirect("bookings:bookings")


@login_required
def book_session(request, session_id):
    """
    Create a new booking for a class session.
    Performs two defensive checks before creating the booking:
    1. Checks if the user has already booked this session
       to prevent duplicate bookings.
    2. Checks if the session has reached its capacity limit
       to prevent overbooking.
    If both checks pass, creates the booking and increments
    the session's booked_count.
    Requires the user to be logged in.
    """
    # Retrieve the class session or return 404 if not found
    session = get_object_or_404(ClassSession, id=session_id)

    # Check if the user has already booked this session
    already_booked = Booking.objects.filter(
        user=request.user,
        session=session
    ).exists()

    if already_booked:
        # Warn the user and redirect to their bookings page
        messages.warning(request, 'You have already booked this class!')
        return redirect("bookings:bookings")

    # Check if the session has reached its maximum capacity
    if session.booked_count >= session.capacity:
        # Warn the user the class is full and redirect to timetable
        messages.warning(
            request,
            f'Sorry, {session.class_type} is fully booked!'
        )
        return redirect("bookings:classes")

    # Both checks passed — create the booking
    Booking.objects.create(
        user=request.user,
        session=session
    )

    # Increment the session's booked count to reflect the new booking
    session.booked_count += 1
    session.save()

    # Show success confirmation to the user
    messages.success(
        request,
        f'You have successfully booked {session.class_type}!'
    )
    return redirect("bookings:bookings")
