import string
from random import random

from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from datetime import datetime
import json

from .models import Staff, Admin, Doctor, Login, Patient, Role, Specialization, Appointment
from .serializers import SignupSerializer, LoginSerializer, StaffSerializer, DoctorSerializer, PatientSerializer, \
    RoleSerializer, SpecializationSerializer, EmailSerializer, UpdatePasswordSerializer, AppointmentSerializer
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer


def populate_login_table():
    # Get data from Staff table
    staff_data = Staff.objects.values('email', 'password')

    # Get data from Admin table
    admin_data = Admin.objects.values('username', 'password')

    # Get data from Doctor table
    doctor_data = Doctor.objects.values('email', 'password')

    # Create Login objects from the collected data
    for data in staff_data:
        Login.objects.create(email=data['email'], password=data['password'])

    for data in admin_data:
        Login.objects.create(email=data['username'], password=data['password'])

    for data in doctor_data:
        Login.objects.create(email=data['email'], password=data['password'])


@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        # Create a new Login object
        Login.objects.create(email=email, password=password,role=role)

        return Response({'message': 'Signup successful'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        email = data.get('email')
        password = data.get('password')

        # Check if the email and password match in any of the tables
        user = None
        for model in [Staff, Admin, Doctor]:
            user = model.objects.filter(email=email, password=password).first()
            if user:
                if isinstance(user, Staff) or isinstance(user, Admin):
                    role_details = RoleSerializer(user.role).data
                    staff_details= StaffSerializer(user).data# Serialize role details
                    return Response({'message': 'Login successful', 'role_details': role_details,'staff_details':staff_details},
                                    status=status.HTTP_200_OK)
                elif isinstance(user, Doctor):
                    specialization_details = SpecializationSerializer(user.specialization).data
                    return Response({'message': 'Login successful', 'specialization_details': specialization_details},
                                    status=status.HTTP_200_OK)

        # If user is not found
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

    # If request data is not valid
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def login_list(request):
    if request.method == 'GET':
        logins = Login.objects.all()
        login_data = []
        for login in logins:
            role_serializer = RoleSerializer(login.role)
            login_info = {
                'id': login.id,
                'email': login.email,
                'password': login.password,
                'role': role_serializer.data
            }
            login_data.append(login_info)
        return Response(login_data)



@api_view(['GET', 'POST'])
def staff_list(request):
    if request.method == 'GET':
        staff = Staff.objects.all()
        serializer = StaffSerializer(staff, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleList(APIView):
    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

class SpecializationListView(APIView):
    def get(self, request):
        specializations = Specialization.objects.all()
        serializer = SpecializationSerializer(specializations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
def staff_detail(request, pk):
    try:
        staff = Staff.objects.get(pk=pk)
    except Staff.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StaffSerializer(staff)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StaffSerializer(staff, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        staff.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def doctor_list(request):
    if request.method == 'GET':
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def doctor_detail(request, pk):
    try:
        doctor = Doctor.objects.get(pk=pk)
    except Doctor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def patient_list(request):
    if request.method == 'GET':
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def patient_detail(request, pk):
    try:
        patient = Patient.objects.get(pk=pk)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_doctors_by_specialization_id(request, specialization_id):
    try:
        doctors = Doctor.objects.filter(specialization=specialization_id)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Doctor.DoesNotExist:
        return Response({"error": "Doctors with the specified specialization ID do not exist"}, status=status.HTTP_404_NOT_FOUND)



# views.py
from django.http import JsonResponse
from .models import Staff

def get_emails(request):
    emails = Staff.objects.values_list('email', flat=True)
    return JsonResponse({'emails': list(emails)})

class CheckEmailAPIView(APIView):
    def post(self, request):
        # Deserialize the request data using the EmailSerializer
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if Staff.objects.filter(email=email).exists():
                return Response({'exists': True})
            else:
                return Response({'exists': False})
        else:
            # Return error response if serializer data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def check_email_exists(request):
    email = request.GET.get('email')
    if email:
        email_exists = Staff.objects.filter(email=email).exists()
        return Response(email_exists)
    else:
        return Response(False)

@api_view(['GET'])
def check_phone_number_exists(request):
    phone_number = request.GET.get('phone_number')
    if phone_number:
        phone_number_exists = Staff.objects.filter(phone_number=phone_number).exists()
        return Response(phone_number_exists)
    else:
        return Response(False)

@api_view(['GET'])
def check_phone_number_exists_doctor(request):
    phone_number = request.GET.get('phone_number')
    if phone_number:
        phone_number_exists = Doctor.objects.filter(phone_number=phone_number).exists()
        return Response(phone_number_exists)
    else:
        return Response(False)



@api_view(['GET'])
def check_email_exists_doc(request):
    email = request.GET.get('email')
    if email:
        email_exists = Doctor.objects.filter(email=email).exists()
        return Response(email_exists)
    else:
        return Response(False)

@csrf_exempt
def toggle_active(request, staff_id):
    if request.method == 'PUT':
        staff = get_object_or_404(Staff, pk=staff_id)
        staff.is_active = not staff.is_active
        staff.save()
        return JsonResponse({'success': True})
    else:
        return HttpResponseNotAllowed(['PUT'])

@csrf_exempt
def toggle_active_doctor(request, doctor_id):
    if request.method == 'PUT':
        doctor = get_object_or_404(Doctor, pk=doctor_id)
        doctor.is_active = not doctor.is_active
        doctor.save()
        return JsonResponse({'success': True})
    else:
        return HttpResponseNotAllowed(['PUT'])


@api_view(['GET'])
def check_phone_number_exists_patient(request):
    phone_number = request.GET.get('phone_number')
    if phone_number:
        phone_number_exists = Patient.objects.filter(phone_number=phone_number).exists()
        return Response(phone_number_exists)
    else:
        return Response(False)



@api_view(['GET'])
def check_email_exists_pat(request):
    email = request.GET.get('email')
    if email:
        email_exists = Patient.objects.filter(email=email).exists()
        return Response(email_exists)
    else:
        return Response(False)


@csrf_exempt
def toggle_active_patient(request, patient_id):
    if request.method == 'PUT':
        doctor = get_object_or_404(Patient, pk=patient_id)
        doctor.is_active = not doctor.is_active
        doctor.save()
        return JsonResponse({'success': True})
    else:
        return HttpResponseNotAllowed(['PUT'])


class UpdatePasswordAPIView(APIView):
    def put(self, request, staff_id):
        # Get the staff member
        try:
            staff = Staff.objects.get(pk=staff_id)
        except Staff.DoesNotExist:
            return Response({"error": "Staff member not found."}, status=status.HTTP_404_NOT_FOUND)

        # Deserialize the request data
        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Get the new password
            new_password = serializer.validated_data['new_password']
            # Update the password
            staff.password = new_password
            staff.save()
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookAppointment(APIView):
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@csrf_exempt
def book_appointment(request):
    if request.method == 'POST':
        try:
            # Parse the request body as JSON
            data = json.loads(request.body)

            # Extract appointment data from the request
            patient_id = data.get('patient_id')
            doctor_id = data.get('doctor_id')
            booking_date = data.get('booking_date')
            appointment_time = data.get('appointment_time')
            token_no = data.get('token_no')

            # Convert appointment_time to datetime object
            appointment_datetime = datetime.strptime(f"{booking_date} {appointment_time}", "%Y-%m-%d %H:%M:%S")

            # Create the appointment object
            appointment = Appointment.objects.create(
                patient_id=patient_id,
                doctor_id=doctor_id,
                booking_date=booking_date,
                appointment_time=appointment_datetime.time(),
                token_no=token_no
            )

            # Return success response
            return JsonResponse({'message': 'Appointment booked successfully'}, status=201)
        except Exception as e:
            # Return error response if an exception occurs
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@api_view(['GET', 'POST'])  # Allow both GET and POST methods
def appointment_list(request):
    if request.method == 'GET':
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

def check_patient_exists(request, patient_id):
    try:
        patient = Patient.objects.get(patient_id=patient_id)
        return JsonResponse({'exists': True})
    except Patient.DoesNotExist:
        return JsonResponse({'exists': False})


from django.http import JsonResponse
from .models import Patient  # Assuming you have a Patient model defined in models.py

from django.http import JsonResponse
from .models import Patient  # Assuming you have a Patient model defined in models.py

def get_patient_details(request, phone_number):
    try:
        patient = Patient.objects.get(phone_number=phone_number)
        # Assuming Patient model has fields like first_name, last_name, email, etc.
        patient_details = {
            'patient_id': patient.patient_id,  # Assuming patient.id is the patient's ID field
            'first_name': patient.first_name,
            'last_name': patient.last_name,
            'email': patient.email,
            'gender': patient.gender,
            'blood_group': patient.blood_group,
            'height': patient.height,
            'weight': patient.weight,
            # Add other fields as needed
            # Example:
            'date_of_birth': patient.date_of_birth,
            'address': patient.address,
            # Add other fields as needed
        }
        return JsonResponse(patient_details)
    except Patient.DoesNotExist:
        return JsonResponse({'error': 'Patient not found'}, status=404)


def get_duty_time(request, doctor_id):
    try:
        doctor = Doctor.objects.get(doctor_id=doctor_id)
        duty_time = doctor.Duty_time  # Assuming you have a 'duty_time' field in your Doctor model
        return JsonResponse({'duty_time': duty_time})
    except Doctor.DoesNotExist:
        return JsonResponse({'error': 'Doctor not found'}, status=404)


@api_view(['GET'])
def appointments_by_doctor_id(request, doctor_id):
    appointments = Appointment.objects.filter(doctor_id=doctor_id)
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)

def get_appointments_by_patient_id(request, patient_id):
    appointments = Appointment.objects.filter(patient=patient_id)
    serializer = AppointmentSerializer(appointments, many=True)
    return JsonResponse(serializer.data, safe=False)

def get_appointment_by_id(request, appointment_id):
    try:
        appointment = Appointment.objects.get(pk=appointment_id)
        serializer = AppointmentSerializer(appointment)
        return JsonResponse(serializer.data)
    except Appointment.DoesNotExist:
        return JsonResponse({'error': 'Appointment not found'}, status=404)

