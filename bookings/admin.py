from django.contrib import admin
from .models import Booking, ClassSession

admin.site.register(ClassSession)
admin.site.register(Booking)