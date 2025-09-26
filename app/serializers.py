from rest_framework import serializers
from .models import *
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class CrmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crm
        fields = '__all__' 

class AdminPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminPayments
        fields = '__all__' 

class AdminEmployeeRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminEmployeeRegister
        fields = '__all__'

from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['employee_id', 'name', 'email', 'role', 'phone', 'created_at']
        read_only_fields = ['employee_id', 'created_at']   

class FieldworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fieldwork
        fields = '__all__'  

class BillsUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillsUpload
        fields = '__all__'                    
    
from rest_framework import serializers
from .models import Employee

class EmployeeRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'role', 'phone']

class LoginSerializer(serializers.Serializer):
    employee_id = serializers.CharField()
    password = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

class ForgotPasswordSerializer(serializers.Serializer):
    identifier = serializers.CharField()   # email or employee_id
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data




   