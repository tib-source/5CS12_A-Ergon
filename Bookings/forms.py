from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Bookings.models import Student, Staff

class StudentRegisterForm(UserCreationForm):

    email = forms.EmailField()
    current_course = forms.ChoiceField(
            choices=Student.course_choices,
    )
    student_id = forms.CharField()
    class Meta:
        model = Student
        fields = ["first_name", "last_name","username", "student_id","current_course", "email", "password1", "password2"]
        
        
class StaffRegisterForm(UserCreationForm):

    email = forms.EmailField()
    department = forms.ChoiceField(
            choices=Staff.department_choices,
    )
    staff_id = forms.CharField()
    class Meta:
        model = Staff
        fields = ["first_name", "last_name","username", "staff_id","department", "email", "password1", "password2"]