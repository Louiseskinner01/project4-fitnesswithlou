from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    # Show all subscription plans
    path('',views.subscription_plans, name='subscription_plans'),

    # Susbribe to a plan (requires an id
    path('subscribe/<int:plan_id>/', views.subscribe, name='subscribe'),
]