from django.urls import include, path
from Bookings.views import DashboardView, student_register 
from django.views.generic.base import TemplateView  # new

frontend_patterns = [ 
    path('', TemplateView.as_view(template_name='Bookings/landing.html')),
    path('dashboard', DashboardView.as_view())

          
]


urlpatterns=[
  path('', include(frontend_patterns)),
  path('accounts/', include("django.contrib.auth.urls")),
  path('register/student', student_register ),
  path('register/staff', student_register ),
  path('register/admin', student_register )
]



