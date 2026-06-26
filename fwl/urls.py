
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from main import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('bookings/', include('bookings.urls')),
    path('users/', include('users.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('subscriptions/',
         include('subscriptions.urls')),
    path('', include('main.urls')),
    path("contact/",
         TemplateView.as_view(
             template_name="main/contactus.html"), name="contact"),
    path("about/",
         TemplateView.as_view(
             template_name="main/aboutus.html"), name="about"),
    path('nutritional-advice/',
         include('nutrition.urls')),
    path("join/", main_views.join_us, name="join"),
    path("join/success/",
         TemplateView.as_view(
             template_name="main/job_success.html"), name="job_success"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'fwl.views.handler404'
handler500 = 'fwl.views.handler500'
