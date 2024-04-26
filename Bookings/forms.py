from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Bookings.models import Student

class StudentRegisterForm(UserCreationForm):

    email = forms.EmailField()
    current_course = forms.ChoiceField(
            choices=Student.course_choices,
    )
    class Meta:
        model = Student
        fields = ["first_name", "last_name","username", "current_course", "email", "password1", "password2"]