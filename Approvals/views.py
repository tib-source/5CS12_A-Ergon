from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from .models import ApprovalRequest
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class ApprovalListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ApprovalRequest
    template_name = 'approvals.html'
    context_object_name = 'approval_requests'

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        return ApprovalRequest.objects.filter(approver=self.request.user, status='pending').order_by('-request_date')

class UpdateApprovalRequest(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ApprovalRequest
    fields = ['status']
    template_name = 'update_approval.html'
    success_url = reverse_lazy('approvals')

    def test_func(self):
        obj = self.get_object()
        return obj.approver == self.request.user
