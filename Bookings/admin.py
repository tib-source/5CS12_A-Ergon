from django.contrib import admin

from Bookings.models import *

# Register your models here.
admin.site.register(Admin)
admin.site.register(Staff)
admin.site.register(Student)
admin.site.register(Booking)
admin.site.register(Equipment)
admin.site.register(Report)