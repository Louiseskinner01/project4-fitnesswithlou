from django.urls import path
from . import views

# Nutrition app namespace — used to reference URLs as 'nutrition:url_name'
app_name = 'nutrition'

urlpatterns = [
    # Nutritional advice page — displays static nutritional guidance content
    # Accessible to all users including unauthenticated visitors
    path('', views.nutritional_advice, name='nutritional_advice'),
]
