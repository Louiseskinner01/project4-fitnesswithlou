from django.urls import path
from . import views

# Bookings app namespace — used to reference URLs as 'bookings:url_name'
app_name = 'bookings'

urlpatterns = [
    # Display the authenticated user's upcoming and past bookings
    path('', views.bookings_list, name='bookings'),

    # Display the full class timetable for users to browse and book
    path("classes/", views.timetable, name="classes"),

    # Book a specific class session
    # session_id identifies which ClassSession to book
    path(
        "book/<int:session_id>/",
        views.book_session,
        name="book_session"
    ),

    # Cancel an existing booking
    # booking_id identifies which Booking to cancel and delete
    path(
        "cancel/<int:booking_id>/",
        views.cancel_booking,
        name="cancel_booking"
    ),
]
