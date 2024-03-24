from django.urls import path

from . import views
from .views import signup, login, staff_detail, staff_list, doctor_detail, doctor_list, patient_list, patient_detail, \
    login_list, RoleList, get_emails, CheckEmailAPIView, check_email_exists, SpecializationListView, \
    check_email_exists_doc, check_email_exists_pat, UpdatePasswordAPIView, book_appointment, appointment_list, \
    check_patient_exists, get_patient_details, get_appointment_by_id

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('login2/', login_list, name='login-list'),
    path('staffs/', staff_list),
    path('staffs/<int:pk>/', staff_detail),
    path('doctors/', doctor_list),
    path('doctors/<int:pk>/', doctor_detail),
    path('patients/', patient_list),
    path('patients/<int:pk>/', patient_detail),
    path('specialization/<int:specialization_id>/', views.get_doctors_by_specialization_id, name='get_doctors_by_specialization'),
    path('roles/', RoleList.as_view(), name='role-list'),
    # path('api/check-email/', check_email, name='check_email'),
    path('api/get-emails/', get_emails, name='get_emails'),
    path('check-email/', CheckEmailAPIView.as_view(), name='check_email'),
    path('api/check-email', check_email_exists, name='check_email_exists_in_staff_table'),
    path('api/check-phone-number', views.check_phone_number_exists, name='check_phone_number_exists'),
    path('specializations/', SpecializationListView.as_view(), name='specializations-list'),
    path('api/check-phone-number-doctor/', views.check_phone_number_exists_doctor, name='check_phone_number_exists_doctor'),
    path('api/check-email-doctor', check_email_exists_doc, name='check_email_exists_in_doctor_table'),
    path('staffs/<int:staff_id>/toggle-active/', views.toggle_active, name='toggle_active'),
    path('doctor/<int:doctor_id>/isActive', views.toggle_active_doctor, name='update_doctor_is_active'),
    path('api/check-phone-number-patient/', views.check_phone_number_exists_patient, name='check_phone_number_exists_patient'),
    path('api/check-email-patient', check_email_exists_pat, name='check_email_exists_in_patient_table'),
    path('patient/<int:patient_id>/isActive', views.toggle_active_patient, name='update_patient_is_active'),
    path('api/update-password/<int:staff_id>/', UpdatePasswordAPIView.as_view(), name='update_password'),
    path('book_appointment/', book_appointment, name='book_appointment'),
    path('appointments/', appointment_list, name='get_appointment_details'),
    path('check_patient/<int:patient_id>/', check_patient_exists, name='check_patient_exists'),
    path('patient-details/<phone_number>/', get_patient_details, name='get_patient_details'),
    path('doctors/<int:doctor_id>/duty-time/', views.get_duty_time, name='get_duty_time'),
    path('appointments/by-doctor/<int:doctor_id>/', views.appointments_by_doctor_id, name='appointments-by-doctor'),
    path('api/appointments/by-patient/<int:patient_id>/', views.get_appointments_by_patient_id, name='get_appointments_by_patient_id'),
    path('appointments/<int:appointment_id>/', get_appointment_by_id, name='get_appointment_by_id'),
]


