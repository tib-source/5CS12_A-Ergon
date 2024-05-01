from datetime import datetime
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView
from Bookings.models import Booking, Report, Student, Equipment
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from .forms import StudentRegisterForm, StaffRegisterForm
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.http import FileResponse
# from docx import Document
from reportlab.pdfgen import canvas
from io import BytesIO
import tempfile



class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'Bookings/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = None
        if(self.request.user.is_staff): 
            user = self.request.user.staff if hasattr(self.request.user, "staff") else self.request.user
        else:
            user = self.request.user.student
            
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
        context['user'] = user
        return context
    

# Registration View 
def register(response):
    ## Check if the user is submitting information 
    if response.method == "POST":
        ## Check if the registration is student or staff 
        user_type = response.POST.get('user_type')
        
        ## Use respective form for validation
        ## Return register page with errors if invalid 
        if(user_type == "student"):
            form = StudentRegisterForm(response.POST) 
            if form.is_valid():
                form.save()
                return redirect("/dashboard")
            else:
                return render(response, "registration/signup.html", {"form" : form})
        if(user_type == "staff"):
            form = StaffRegisterForm(response.POST) 
            if form.is_valid():
                form.save()
                return redirect('/dashboard')
            else:
                return render(response, "registration/signup.html", {"form" : form})
    else:
        form = StudentRegisterForm()

    return render(response, "registration/signup.html", {"form" : form})




class ReportView(LoginRequiredMixin, TemplateView):
    template_name = 'report/report.html'

    def generate_report(self, report_type, time_period):
        # Calculate the start date based on the time period
        if time_period == 'last2weeks':
            start_date = timezone.now() - timedelta(days=14)
        elif time_period == 'last1month':
            start_date = timezone.now() - timedelta(days=30)
        elif time_period == 'last3months':
            start_date = timezone.now() - timedelta(days=90)
        elif time_period == 'last6months':
            start_date = timezone.now() - timedelta(days=180)
        elif time_period == 'last1year':
            start_date = timezone.now() - timedelta(days=365)
        elif time_period == 'last2years':
            start_date = timezone.now() - timedelta(days=730)
        else:
            # Default to last 1 month if time period is not recognized
            start_date = timezone.now() - timedelta(days=30)

        # Query equipment data based on the start date
        equipment_queryset = Equipment.objects.filter(last_audit__gte=start_date)
        
        if not equipment_queryset.exists():
            return "No data available for this time period."

        # Convert queryset to a list of dictionaries
        serialized_data = list(equipment_queryset.values())

        # Convert choice field values to their readable representations
        for obj in serialized_data:
            obj['type'] = dict(Equipment.type_choices).get(obj['type'])
            obj['status'] = dict(Equipment.status_choices).get(obj['status'])

        #Generate report content based on report type
        if report_type == 'equipment':
            report_content = serialized_data
        else:
            report_content = "Report type not supported"

        return report_content

    def generate_pdf_report(self, report_data):
        if isinstance(report_data, str) and report_data.startswith("No data available"):
            # Generate PDF with message indicating no data available
            buffer = BytesIO()
            p = canvas.Canvas(buffer)
            p.drawString(100, 750, report_data)  # Display the no data available message
            p.save()
            pdf_content = buffer.getvalue()
            buffer.close()
            return pdf_content

        # Otherwise, generate PDF with the report data
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        x = 100
        y = 750
        max_line_width = 75

        for entry in report_data:
            formatted_entry = ', '.join([f"{key}: {value if key != 'comment' or value else 'no comment'}" for key, value in entry.items()])
            segments = [formatted_entry[i:i+max_line_width] for i in range(0, len(formatted_entry), max_line_width)]

            for segment in segments:
                p.drawString(100, y, segment)
                y -= 15

            y -= 15

        p.save()
        pdf_content = buffer.getvalue()
        buffer.close()
        return pdf_content

    # def generate_doc_report(self, report_data):
    #     if isinstance(report_data, str) and report_data.startswith("No data available"):
    #         # Generate DOCX with message indicating no data available
    #         doc = Document()
    #         doc.add_paragraph(report_data)
    #         temp_file = tempfile.NamedTemporaryFile(delete=False)
    #         doc.save(temp_file)
    #         with open(temp_file.name, 'rb') as f:
    #             doc_content = f.read()
    #         return doc_content

    #     # Otherwise, generate DOCX with the report data
    #     doc = Document()
    #     for entry in report_data:
    #         formatted_entry = ', '.join([f"{key}: {value if key != 'comment' or value else 'no comment'}" for key, value in entry.items()])
    #         doc.add_paragraph(formatted_entry)
    #         doc.add_paragraph()  # Add an empty paragraph for extra line spacing

    #     temp_file = tempfile.NamedTemporaryFile(delete=False)
    #     doc.save(temp_file)
    #     with open(temp_file.name, 'rb') as f:
    #         doc_content = f.read()

    #     return doc_content
    
    def post(self, request):
      # Retrieve form data
        report_type = request.POST.get('report_type')
        time_period = request.POST.get('time_period')
        format_type = request.POST.get('format_type')

        try:
            # Generate report content
            report_data = self.generate_report(report_type, time_period)

            # Generate report based on format type
            if format_type == 'pdf':
                report_content = self.generate_pdf_report(report_data)
                content_type = 'application/pdf'
                file_extension = 'pdf'
            elif format_type == 'doc':
                report_content = self.generate_doc_report(report_data)
                content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                file_extension = 'docx'
            else:
                raise ValueError("Invalid format type. Must be 'pdf' or 'doc'.")

            # Save report information to the database
            user = request.user
            report = Report.objects.create(
                user=user,
                report_type=report_type,
                time_period=time_period,
                format_type=format_type
            )

            # Prepare file response to download
            filename = f"report_{report.id}.{file_extension}"
            response = FileResponse(BytesIO(report_content), content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

            return response
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    
    
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