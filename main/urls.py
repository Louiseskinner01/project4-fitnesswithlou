from django.urls import path
from . import views

# Main app namespace — used to reference URLs as 'main:url_name'
app_name = 'main'

urlpatterns = [
    # Landing page — the home page of the FWL site
    path('', views.landing_page, name="landing"),

    # Newsletter signup page — handles email capture form submission
    path('newsletter/', views.newsletter_signup, name='newsletter'),
]
