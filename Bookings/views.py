from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from Bookings.models import Student
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'Bookings/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve the student object and add it to the context
        student = Student.objects.get(pk=self.request.user.pk)  # Assuming the user is logged in
        context['student'] = student
        return context