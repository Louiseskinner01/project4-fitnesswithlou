from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from main import views as main_views

urlpatterns = [
    # Django admin panel
    path('admin/', admin.site.urls),

    # Products app — browse, search and manage products
    path('products/', include('products.urls')),

    # Bookings app — class timetable and session bookings
    path('bookings/', include('bookings.urls')),

    # Users app — user profiles and order history
    path('users/', include('users.urls')),

    # Cart app — shopping cart management
    path('cart/', include('cart.urls')),

    # Checkout app — Stripe payment processing and order creation
    path('checkout/', include('checkout.urls')),

    # Custom accounts app — overrides allauth signup with custom view
    # Must be included before allauth.urls to take priority
    path('accounts/', include('accounts.urls')),

    # Allauth URLs — handles login, logout, email verification etc
    path('accounts/', include('allauth.urls')),

    # Subscriptions app — membership plans and Stripe subscription billing
    path('subscriptions/', include('subscriptions.urls')),

    # Main app — landing page, newsletter and other general pages
    path('', include('main.urls')),

    # Static template views — no view logic required for these pages
    # Contact Us page
    path(
        "contact/",
        TemplateView.as_view(
            template_name="main/contactus.html"
        ),
        name="contact"
    ),

    # About Us page
    path(
        "about/",
        TemplateView.as_view(
            template_name="main/aboutus.html"
        ),
        name="about"
    ),

    # Nutritional advice app
    path('nutritional-advice/', include('nutrition.urls')),

    # Join the Team page — handled by main app view for CV upload
    path("join/", main_views.join_us, name="join"),

    # Job application success page — shown after successful CV submission
    path(
        "join/success/",
        TemplateView.as_view(
            template_name="main/job_success.html"
        ),
        name="job_success"
    ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Serves media files during local development
# In production media files are served by Cloudinary

# Custom error handlers
# These override Django's default error pages with styled FWL templates
handler404 = 'fwl.views.handler404'  # Custom 404 page
handler500 = 'fwl.views.handler500'  # Custom 500 page
