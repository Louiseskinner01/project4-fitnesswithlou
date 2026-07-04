from django.urls import path
from . import views

# Users app namespace — used to reference URLs as 'users:url_name'
app_name = 'users'

urlpatterns = [
    # User profile page — displays and updates delivery information,
    # order history and active subscription status
    path('profile/', views.profile, name='profile'),

    # Individual order detail page — displays full details of a
    # specific historical order identified by its unique order number
    path(
        'order_history/<order_number>/',
        views.order_history,
        name='order_history'
    ),
]
