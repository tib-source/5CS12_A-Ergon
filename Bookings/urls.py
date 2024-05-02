from django.urls import include, path
from Bookings.views import *
from django.views.generic.base import TemplateView  # new
from django.urls import path
from .views import account_view


frontend_patterns = [ 
    path('', TemplateView.as_view(template_name='Bookings/landing.html')),
    path('dashboard', DashboardView.as_view()),
    path('users', UsersView.as_view()),
    path('report', ReportView.as_view(), name = 'report')
]


backend_patterns = [ 
    path('book', handleBooking),
    path('equipment/new', add_equipment),
    path('equipment/delete', delete_equipment),
    path('equipment/update', update_equipment),
    path('user/new', create_user),
    path('user/delete', delete_user),
    path('user/update', update_user),
]

urlpatterns=[
  path('', include(frontend_patterns)),
  path('api/', include(backend_patterns)),
  path('accounts/', include("django.contrib.auth.urls")),
  path('register/', register, name="register"),
  path('accounts/adminLogin', admin_login, name='admin' ),
  path('booking_history/', booking_history_view, name='booking_history'),
  path('return-item/<int:booking_id>/', return_item, name='return_item'),
  path('rebook-item/<int:booking_id>/', rebook_item, name='rebook_item'),
  path('notifications/', NotificationListView.as_view(), name='notifications'),
  path('approvals/', ApprovalListView.as_view(), name='approvals'),
  path('approvals/update/<int:pk>/', UpdateApprovalRequest.as_view(), name='update_approval'),
  path('account/', account_view, name='account_view'),
]

]



