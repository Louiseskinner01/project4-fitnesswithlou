from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<product_id>/', views.product_details, name='product_details'),
]