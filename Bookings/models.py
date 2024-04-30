from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Admin(User):
    pass    

class Student(User):
    """
        Extension of the Django User model to include more information about students
    """
    course_choices = [
    ("CS101", "BSc in Computer Science"),
    ("ENG201", "BA in English Literature"),
    ("MATH301", "BSc in Mathematics"),
    ("CHEM101", "BSc in Chemistry"),
    ("PHYS202", "BSc in Physics"),
    ("HIST102", "BA in History"),
    ("PSYC301", "BSc in Psychology"),
    ("BIO101", "BSc in Biology"),
    ("ART205", "BFA in Fine Arts"),
    ("ECON202", "BSc in Economics"),
    ("PHIL101", "BA in Philosophy"),
    ("BUS301", "BBA"),
    ("EDUC202", "Bachelor of Education"),
    ("MED101", "MBBS"),
    ("LAW201", "LLB"),
    ("ARCH301", "BArch"),
    ("MUSIC202", "BMus"),
    ("NURS101", "BSN"),
    ("COMM301", "BA in Communication Studies"),
    ("SOC101", "BA in Sociology")
]
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    current_course = models.CharField(max_length = 10, choices=course_choices)   
    student_id = models.CharField(max_length=10, unique=True )
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
    
class Staff(User):
    """
    Extension of the Django User model to include more information about Staff
    """
    department_choices = [
        ("CS", "Computer Science Department"),
        ("ENG", "English Literature Department"),
        ("MATH", "Mathematics Department"),
        ("CHEM", "Chemistry Department"),
        ("PHYS", "Physics Department"),
        ("HIST", "History Department"),
        ("PSYC", "Psychology Department"),
        ("BIO", "Biology Department"),
        ("ART", "Fine Arts Department"),
        ("ECON", "Economics Department"),
        ("PHIL", "Philosophy Department"),
        ("BUS", "Business Administration Department"),
        ("EDUC", "Education Department"),
        ("MED", "Medical Department"),
        ("LAW", "Law Department"),
        ("ARCH", "Architecture Department"),
        ("MUSIC", "Music Department"),
        ("NURS", "Nursing Department"),
        ("COMM", "Communication Studies Department"),
        ("SOC", "Sociology Department")
    ]
    

    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    department = models.CharField(max_length = 6, choices=department_choices)   
    staff_id = models.CharField(max_length=10, unique=True )    
    
    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"

    
class Equipment(models.Model): 
    
    type_choices= [('PC', 'PC/Laptop'), ('VRH', 'VR Headset'), ('CS', 'Camera/Sensors'), ('PP', 'PC Peripherals'), ('Furn', 'Furniture'), ('Trip', 'Tripod'), ('Oth', 'Other'), ('VRC', 'VR Controller'), ('PT', 'Phones/Tablets'), ('PCBL', 'Power/Cable')]

    status_choices = (
        ("Pend", "Pending"),
        ("Avail", "Available"),
        ("Decom", "Decommisioned"),
        ("Unavail", "Unavailable"),
        ("Loan", "On Loan"),
        ("Repair", "Repairing")
    )
    name = models.CharField(max_length = 100)
    type = models.CharField(max_length = 25, choices = type_choices )
    location = models.CharField(max_length = 50)
    status = models.CharField(max_length = 15, choices = status_choices)
    quantity = models.IntegerField()
    last_audit = models.DateField()
    comment =  models.TextField()
    
    
class Booking(models.Model):
    returnDate = models.DateField()
    approvalStatus = models.BooleanField()
    returnStatus = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    admin = models.ForeignKey(Admin, on_delete = models.CASCADE, related_name="approved_by")
    equipment = models.ForeignKey(Equipment, on_delete = models.CASCADE)
    
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=100)
    time_period = models.CharField(max_length=100)
    format_type = models.CharField(max_length=50)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s {self.report_type} Report"