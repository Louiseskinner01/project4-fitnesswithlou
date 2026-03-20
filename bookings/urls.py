from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.bookings_list, name='bookings'),
    path('create/', views.create_booking, name='create_booking'),
]