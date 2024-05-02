from django.db import models
from django.contrib.auth.models import User

class ApprovalRequest(models.Model):
    requester = models.ForeignKey(User, related_name='requester', on_delete=models.CASCADE)
    approver = models.ForeignKey(User, related_name='approver', on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    details = models.TextField()

    def __str__(self):
        return f"{self.requester} - {self.status}"
