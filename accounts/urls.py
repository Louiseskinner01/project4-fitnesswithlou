from django.urls import path
from . import views

# Accounts app namespace — used to reference URLs as 'accounts:url_name'
app_name = 'accounts'

urlpatterns = [
    # Custom signup page — overrides allauth's default signup URL
    # Provides a customised registration experience for FWL users
    path('accounts/signup/', views.signup, name="signup"),
]
