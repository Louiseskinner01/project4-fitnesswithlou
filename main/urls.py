from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.landing_page, name="landing"),
    path('newsletter/', views.newsletter_signup, name='newsletter'),
]
