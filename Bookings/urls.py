from django.urls import include, path

from Bookings.views import FrontEnd

frontend_patterns = [ 

    path('',FrontEnd.getLandingPage)
          
]


urlpatterns=[
  path('', include(frontend_patterns))
]



