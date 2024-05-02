from django.urls import path
from .views import ApprovalListView, UpdateApprovalRequest

urlpatterns = [
    path('approvals/', ApprovalListView.as_view(), name='approvals'),
    path('approvals/update/<int:pk>/', UpdateApprovalRequest.as_view(), name='update_approval'),
]
