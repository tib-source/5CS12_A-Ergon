from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
class FrontEnd:
    
    def getLandingPage(request): 
        return render(request, 'Bookings/landing.html')
    
    
    