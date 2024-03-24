from rest_framework import serializers

from .models import Login, Staff, Doctor, Patient, Role, Specialization, Appointment


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = ['role', 'email', 'password']
    def create(self, validated_data):
        return validated_data



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)



class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'



class StaffSerializer(serializers.ModelSerializer):
    role_detail = RoleSerializer(source='role',read_only=True)
    class Meta:
        model = Staff
        fields = '__all__'


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'specialization']


class DoctorSerializer(serializers.ModelSerializer):
    specialization_detail = SpecializationSerializer(source='specialization', read_only=True)
    class Meta:
        model = Doctor
        fields = '__all__'





class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()



class UpdatePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128, required=True)


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = '__all__'