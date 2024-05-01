from datetime import datetime
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView
from Bookings.models import Booking, Student, Equipment
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder



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
    
    
    
def handleBooking(req):
    print(req.method == "POST")
    if(req.method == "POST"): 
        # Find equipment 
        print("meow")
        try: 
            request = json.loads(req.body)
            to_book = Equipment.objects.get(id=request.get('id')) 
            if(to_book.status == "Avail" and to_book.quantity > 0):
                
                request_data = json.loads(req.body)
                print(request_data)
                return_date_string = request_data.get('to')
                return_date_object = datetime.strptime(return_date_string, '%Y-%m-%d').date()

                # Create a new booking
                new_booking = Booking.objects.create(
                    return_date = return_date_object,
                    approved=False, 
                    returned=False, 
                    user=req.user,  
                    admin=None,  
                    equipment=to_book
                )
                new_booking.save()
                return HttpResponse(json.dumps({"message" : "Booking Succesfull"}), status=200)

            else: 
                return HttpResponse(json.dumps({"message" : "Equipment is not available"}), status=403)
        except Equipment.DoesNotExist: 
                return HttpResponse(json.dumps({"message": "Equipment not found"}), status=404)
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({"message": "Failed to book:" + str(e)}), status=500)
    return HttpResponse("Method not allowed", status=405)