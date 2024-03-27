from django.urls import include, path

from Bookings.views import BookingView

frontend_patterns = [ 
    path('', BookingView.get_landing_page),
    path('dashboard', BookingView.get_dashboard)
          
]


urlpatterns=[
  path('', include(frontend_patterns)),
  path('', include("django.contrib.auth.urls"))
]



