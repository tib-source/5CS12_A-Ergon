from datetime import datetime
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import TemplateView
from Bookings.models import Booking, Report, Staff, Student, Equipment
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404, render, redirect
from .forms import StudentRegisterForm, StaffRegisterForm
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.http import FileResponse
# from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import tempfile
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active and user.is_staff:
                login(request, user)
                return redirect('/dashboard')
            else:
                return render(request, 'registration/admin_login.html', {'form': form, 'error_message': 'Invalid login'})
    else:
        form = AuthenticationForm()
    return render(request, 'registration/admin_login.html', {'form': form})

class UsersView(LoginRequiredMixin, TemplateView):
    template_name = 'Bookings/users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = None
        if(self.request.user.is_staff): 
            user = self.request.user.staff if hasattr(self.request.user, "staff") else self.request.user
        else:
            user = self.request.user.student
            
        # Get all User objects from the database
        student_queryset = Student.objects.all()
        staff_queryset = Staff.objects.all()

        # Convert queryset to a list of dictionaries
        serialized_student= list(student_queryset.values())
        serialized_staff= list(staff_queryset.values())

        # # Convert choice field values to their human-readable representations
        # for obj in serialized_data:
        #     obj['type'] = dict(Equipment.type_choices).get(obj['type'])
        #     obj['status'] = dict(Equipment.status_choices).get(obj['status'])

        # Serialize the data to JSON
        student_json = json.dumps(serialized_student, cls=DjangoJSONEncoder)
        staff_json = json.dumps(serialized_staff, cls=DjangoJSONEncoder)

        # Add data into context object
        context['staff_all'] = staff_json
        context['students_all'] = student_json
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'Bookings/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = None
        if(self.request.user): 
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


@staff_member_required
def create_user(response):
    ## Check if the user is submitting information 
    if response.method == "POST":
        ## Check if the registration is student or staff 
        response = json.loads(response.body)
        user_type = response.get('user_type')
        ## Use respective form for validation
        ## Return register page with errors if invalid 
        if(user_type == "student"):
            form = StudentRegisterForm(response) 
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': 'User created successfully.'})
            else:
                print(form.errors)
                ##return JsonResponse({'success': False, 'message': 'Invalid form.'})
            print(form)
        if(user_type == "staff"):
            form = StaffRegisterForm(response) 
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': 'User created successfully.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid form.'})
    return JsonResponse({'success': False, 'message': 'Invalid Request Type.'})


class ReportView(LoginRequiredMixin, TemplateView):
    template_name = 'report/report.html'

    def generate_report(self, report_type, time_period):
        print("Report Type Received:", report_type)
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
            start_date = timezone.now() - timedelta(days=30)

        if report_type == 'equipment':
            equipment_queryset = Equipment.objects.filter(last_audit__gte=start_date)
            if not equipment_queryset.exists():
                return "No equipment data available for this time period."
            equipment_serialized_data = list(equipment_queryset.values())
            for obj in equipment_serialized_data:
                obj['type'] = dict(Equipment.type_choices).get(obj['type'])
                obj['status'] = dict(Equipment.status_choices).get(obj['status'])
            return equipment_serialized_data

        else:
            report_type == 'booking'
            print("Generating booking report...")
            approved_bookings = Booking.objects.filter(from_date__gte=start_date)
            if not approved_bookings.exists():
                return "No bookings made within the time period specified."
            booking_serialized_data = list(approved_bookings.values())
            return booking_serialized_data

    def generate_pdf_report(self, report_data):
        if isinstance(report_data, str):  # Check if report_data is a string error message
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            p.drawString(100, 750, report_data)  # Display the error message
            p.save()
            pdf_content = buffer.getvalue()
            buffer.close()
            return pdf_content

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        x = 100
        y = 750
        max_line_width = 75
        page_height = letter[1]
        max_lines_per_page = int((page_height - y) / 15)  # Calculate maximum lines that can fit on a page

        for entry in report_data:
            formatted_entry = ', '.join([f"{key}: {value if key != 'comment' or value else 'no comment'}" for key, value in entry.items()])
            segments = [formatted_entry[i:i+max_line_width] for i in range(0, len(formatted_entry), max_line_width)]

            for segment in segments:
                p.drawString(100, y, segment)
                y -= 15

            # Check if reached end of page, if yes, create a new page
                if y <= 50:
                    p.showPage()
                    y = page_height - 50  # Reset y coordinate for the new page

            y -= 15

        p.save()
        pdf_content = buffer.getvalue()
        buffer.close()
        return pdf_content

    def generate_doc_report(self, report_data):
        if isinstance(report_data, str):  # Check if report_data is a string error message
            doc = Document()
            doc.add_paragraph(report_data)
        else:
            doc = Document()
            for entry in report_data:
                formatted_entry = ', '.join([f"{key}: {value if key != 'comment' or value else 'no comment'}" for key, value in entry.items()])
                doc.add_paragraph(formatted_entry)
                doc.add_paragraph()  # Add an empty paragraph for extra line spacing

        temp_file = tempfile.NamedTemporaryFile(delete=False)
        doc.save(temp_file)
        with open(temp_file.name, 'rb') as f:
            doc_content = f.read()

        return doc_content

    def post(self, request):
        report_type = request.POST.get('report_type')
        time_period = request.POST.get('time_period')
        format_type = request.POST.get('format_type')

        try:
            report_data = self.generate_report(report_type, time_period)

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

            user = request.user
            report = Report.objects.create(
                user=user,
                report_type=report_type,
                time_period=time_period,
                format_type=format_type
            )

            filename = f"report_{report.id}.{file_extension}"
            response = FileResponse(BytesIO(report_content), content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

            return response

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    
@login_required
def handleBooking(req):
    if(req.method == "POST"): 
        # Find equipment 
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
                return JsonResponse({ 'success': True, "message" : "Booking Succesfull"}, status=200)

            else: 
                return JsonResponse({'success': False, "message" : "Equipment is not available"}, status=403)
        except Equipment.DoesNotExist: 
                return JsonResponse({'success': False,"message": "Equipment not found"}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({'success': False,"message": "Failed to book:" + str(e)}, status=500)
    return JsonResponse({'success': False, "message" : "Method not allowed"}, status=405)

@staff_member_required
def add_equipment(request):
    print("meow")

    if request.method == 'POST':
        if (not request.user.is_staff):
            return JsonResponse({'success': False, 'message': 'User is not an admin'})
        # Extract data from the POST request
        data =json.loads(request.body)
        
        equipment_name = data.get('name')
        equipment_quantity = data.get('quantity')
        equipment_type = data.get('type')
        equipment_location = data.get('location')
        equipment_status = data.get('status')
        equipment_comment = data.get('comment')

        # Create or update equipment booking in the database
        try:
            equipment = Equipment.objects.create(
                name=equipment_name,
                quantity = equipment_quantity, 
                type = equipment_type, 
                location = equipment_location, 
                status = equipment_status, 
                comment = equipment_comment,
                last_audit = datetime.now()
            )
            
            equipment.save()
            return JsonResponse({'success': True, 'message': 'Equipment booking saved successfully'})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Only POST requests are allowed'}, status=405)
@staff_member_required
def delete_equipment(request):
    if request.method == "POST":  
        # Check if the user is staff
        if not request.user.is_staff:
            return JsonResponse({'success': False, 'message': 'Permission denied. Only staff members can delete equipment.'}, status=403)
        
        data =json.loads(request.body)
        equipment_id = data.get('id')
        
        print(data)

        # Check if the equipment with the given ID exists
        try:
            equipment = Equipment.objects.get(id=equipment_id)
        except Equipment.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Equipment with the specified ID does not exist.'}, status=404)

        # Delete the equipment
        equipment.delete()
        
        return JsonResponse({'success': True, 'message': 'Equipment deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Only POST requests are allowed'}, status=405)


@staff_member_required
def update_equipment(request):

    if request.method == 'PUT':
        if (not request.user.is_staff):
            return JsonResponse({'success': False, 'message': 'User is not an admin'})
        # Extract data from the POST request
        data =json.loads(request.body)
        
        equipment_id= data.get('id')
        
        equipment = get_object_or_404(Equipment, id=equipment_id)
    
        # Update the equipment
        try:
            equipment.name = data.get('name')
            equipment.quantity = data.get('quantity')
            equipment.type = data.get('type')
            equipment.location = data.get('location')
            equipment.status = data.get('status')
            equipment.comment = data.get('comment')
                
            equipment.save()
            return JsonResponse({'success': True, 'message': 'Equipment updated successfully'})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Only PUT requests are allowed'}, status=405)
    
    
    
@staff_member_required
def delete_user(request): 
    if request.method == 'POST':
        try:
            user_id = json.loads(request.body).get('id')
            # Retrieve the user to be deleted
            user = User.objects.get(pk=user_id)
            # Delete the user
            user.delete()
            return JsonResponse({'success': True, 'message': 'User deleted successfully.'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found.'})
    else:
        return JsonResponse({'success': False, 'message': 'Only POST requests are allowed for deletion.'}, status=405)
    
@staff_member_required 
def update_user(request): 
    if request.method == 'PUT':
        try:
            
            data = json.loads(request.body)
            user_id = data.get('id')
            user_type = data.get('user_type')
            # Retrieve the user to be deleted
            if (user_type == "staff"): 
                user = Staff.objects.get(id=user_id)
                user.username= data.get('username')
                user.first_name = data.get('first_name')
                user.last_name = data.get('last_name')
                user.staff_id = data.get('staff_id')
                user.department = data.get('department')
                user.email = data.get('email')
                user.is_staff = data.get('is_staff')
                user.save()
                return JsonResponse({'success': True, 'message': 'User updated successfully.'})

            else: 
                user = Student.objects.get(id=user_id)
                user.username= data.get('username')
                user.first_name = data.get('first_name')
                user.last_name = data.get('last_name')
                user.student_id= data.get('student_id')
                user.current_course = data.get('current_course')
                user.email = data.get('email')
                user.save()
                return JsonResponse({'success': True, 'message': 'User updated successfully.'})            
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found.'})
    else:
        return JsonResponse({'success': False, 'message': 'Only POST requests are allowed for deletion.'}, status=405)


def booking_history_view(request):
    # Retrieve current bookings for the logged-in user
    current_bookings = Booking.objects.filter(user=request.user, returned=False)

    # Retrieve previous bookings (already returned) for the logged-in user
    previous_bookings = Booking.objects.filter(user=request.user, returned=True)

    context = {
        'current_bookings': current_bookings,
        'previous_bookings': previous_bookings
    }

    return render(request, 'Bookings/booking_history.html', context)

def return_item(request, booking_id):
    # Retrieve the booking object
    booking = get_object_or_404(Booking, id=booking_id)

    # Update the booking details
    booking.returned = True
    booking.return_date = timezone.now()
    booking.status = 'Returned'
    booking.save()

    return redirect('booking_history')

def rebook_item(request, booking_id):
    # Retrieve the booking object
    booking = get_object_or_404(Booking, id=booking_id)

    # Calculate the new from date and return date
    new_from_date = timezone.now()
    new_return_date = new_from_date + timedelta(days=14)

    # Create a new booking with the same details as the previous one
    new_booking = Booking.objects.create(
        return_date = new_return_date,
        approved=False, 
        returned=False, 
        user=booking.user,  
        admin=None,  
        equipment=booking.equipment
    )

    new_booking.save()

    return redirect('booking_history')
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
]
