from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('adjust_cart/<int:item_id>/', views.adjust_cart, name='adjust_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]