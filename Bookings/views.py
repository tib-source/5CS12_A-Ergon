import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from Bookings.models import Student, Equipment
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from .forms import StudentRegisterForm



class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'Bookings/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve the User object and add it to the context
        student = User.objects.get(pk=self.request.user.pk)  
        # Get all Equipment objects from the database
        equipment_queryset = Equipment.objects.all()

        # Convert queryset to a list of dictionaries
        serialized_data = list(equipment_queryset.values())

        # Convert choice field values to their human-readable representations
        for obj in serialized_data:
            obj['type'] = dict(Equipment.type_choices).get(obj['type'])
            obj['status'] = dict(Equipment.status_choices).get(obj['status'])

        # Serialize the data to JSON
        serialized_json = json.dumps(serialized_data, cls=DjangoJSONEncoder)

        # Add data into context object
        context['equipment'] = serialized_json
        context['student'] = student
        
        return context
    

# Registration View 
def student_register(response):
    if response.method == "POST":
        form = StudentRegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/home")
    else:
        form = StudentRegisterForm()

    return render(response, "registration/signup.html", {"form":form})