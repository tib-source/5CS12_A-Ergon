import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from Bookings.models import Student, Equipment
from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.serializers.json import DjangoJSONEncoder


class EquipmentSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=Equipment.type_choices)
    status = serializers.ChoiceField(choices=Equipment.status_choices)

    class Meta:
        model = Equipment
        fields = '__all__'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'Bookings/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve the student object and add it to the context
        student = User.objects.get(pk=self.request.user.pk)  # Assuming the user is logged in
        # Get all Equipment objects from the database
        equipment_queryset = Equipment.objects.all()

        # Convert queryset to a list of dictionaries
        serialized_data = list(equipment_queryset.values())

        # Convert choice field values to human-readable representations
        for obj in serialized_data:
            obj['type'] = dict(Equipment.type_choices).get(obj['type'])
            obj['status'] = dict(Equipment.status_choices).get(obj['status'])

        # Serialize the data to JSON
        serialized_json = json.dumps(serialized_data, cls=DjangoJSONEncoder)
        context['equipment'] = serialized_json
        context['student'] = student
        
        return context