from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.display_profile, name='display_profile'),
    path('profile/create/', views.create_profile, name='create_profile'),
]