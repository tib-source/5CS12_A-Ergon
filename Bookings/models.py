from django.db import models
from django.contrib.auth.models import User; 
# Create your models here.



class Student(User):
    """
        Extension of the Django User model to include more information about students
    """
    course_dict = {
    "CS101": "BSc in Computer Science",
    "ENG201": "BA in English Literature",
    "MATH301": "BSc in Mathematics",
    "CHEM101": "BSc in Chemistry",
    "PHYS202": "BSc in Physics",
    "HIST102": "BA in History",
    "PSYC301": "BSc in Psychology",
    "BIO101": "BSc in Biology",
    "ART205": "BFA in Fine Arts",
    "ECON202": "BSc in Economics",
    "PHIL101": "BA in Philosophy",
    "BUS301": "BBA",
    "EDUC202": "Bachelor of Education",
    "MED101": "MBBS",
    "LAW201": "LLB",
    "ARCH301": "BArch",
    "MUSIC202": "BMus",
    "NURS101": "BSN",
    "COMM301": "BA in Communication Studies",
    "SOC101": "BA in Sociology"}
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = "student_user")
    profile_pics = models.ImageField(default='default.jpg', upload_to='profile_pics')
    current_course = models.CharField(max_length = 10, choices=course_dict)   
    student_id = models.CharField(max_length=10, unique=True )
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
    
class Staff(User):
    """
    Extension of the Django User model to include more information about Staff
    """
    department_dict = {
        "CS": "Computer Science Department",
        "ENG": "English Literature Department",
        "MATH": "Mathematics Department",
        "CHEM": "Chemistry Department",
        "PHYS": "Physics Department",
        "HIST": "History Department",
        "PSYC": "Psychology Department",
        "BIO": "Biology Department",
        "ART": "Fine Arts Department",
        "ECON": "Economics Department",
        "PHIL": "Philosophy Department",
        "BUS": "Business Administration Department",
        "EDUC": "Education Department",
        "MED": "Medical Department",
        "LAW": "Law Department",
        "ARCH": "Architecture Department",
        "MUSIC": "Music Department",
        "NURS": "Nursing Department",
        "COMM": "Communication Studies Department",
        "SOC": "Sociology Department"
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = "staff_user")
    profile_pics = models.ImageField(default='default.jpg', upload_to='profile_pics')
    current_course = models.CharField(max_length = 6, choices=department_dict)   
    staff_id = models.CharField(max_length=10, unique=True )    
    
    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"