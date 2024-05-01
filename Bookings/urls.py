from django.urls import include, path
from Bookings.views import DashboardView, handleBooking, register, ReportView , add_equipment, delete_equipment
from django.views.generic.base import TemplateView  # new

frontend_patterns = [ 
    path('', TemplateView.as_view(template_name='Bookings/landing.html')),
    path('dashboard', DashboardView.as_view()),
    path('report', ReportView.as_view(), name = 'report')
]


backend_patterns = [ 
    path('book/', handleBooking),
    path('equipment/new', add_equipment),
    path('equipment/delete', delete_equipment),
]

urlpatterns=[
  path('', include(frontend_patterns)),
  path('api/', include(backend_patterns)),
  path('accounts/', include("django.contrib.auth.urls")),
  path('register/', register, name="register"),
  path('accounts/admin', register, name='admin' )
]



