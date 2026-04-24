from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.bookings_list, name='bookings'),
    path("classes/", views.timetable, name="classes"),
    path("book/<int:session_id>/", views.book_session, name="book_session"),
]