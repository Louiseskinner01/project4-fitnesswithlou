from django.urls import path
from . import views

app_name = 'nutrition'



urlpatterns = [
    path('', views.nutritional_advice, name='nutritional_advice'),
]