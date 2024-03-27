from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
class BookingView:
    
    def get_landing_page(request): 
        return render(request, 'Bookings/landing.html')
    
    @login_required(login_url="login/")
    def get_dashboard(request):
        return render(request, "Bookings/dashboard.html")