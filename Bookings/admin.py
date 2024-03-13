from django.contrib import admin

from Bookings.models import Student, Staff

# Register your models here.
admin.site.register(Staff)
admin.site.register(Student)