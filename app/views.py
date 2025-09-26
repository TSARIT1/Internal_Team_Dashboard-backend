from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class CrmViewSet(ModelViewSet):
    queryset = Crm.objects.all()
    serializer_class = CrmSerializer  

class AdminPaymentsSet(ModelViewSet):
    queryset = AdminPayments.objects.all()
    serializer_class = AdminPaymentsSerializer 

class AdminEmployeeRegisterSet(ModelViewSet):
    queryset = AdminEmployeeRegister.objects.all()
    serializer_class = AdminEmployeeRegisterSerializer 

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .models import Employee
from .serializers import EmployeeSerializer

@api_view(['GET', 'POST'])
def employee_list_create(request):
    """
    List all employees or create a new employee
    """
    if request.method == 'GET':
        return get_employees(request)
    elif request.method == 'POST':
        return create_employee(request)

def get_employees(request):
    """
    GET method: Retrieve all employees
    """
    try:
        employees = Employee.objects.all()
        
        # Optional query parameters for filtering
        search = request.query_params.get('search', None)
        role = request.query_params.get('role', None)
        
        if search:
            employees = employees.filter(
                models.Q(name__icontains=search) | 
                models.Q(email__icontains=search) |
                models.Q(employee_id__icontains=search)
            )
        
        if role:
            employees = employees.filter(role__iexact=role)
        
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': 'An error occurred while retrieving employees.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def create_employee(request):
    """
    POST method: Create a new employee
    """
    serializer = EmployeeSerializer(data=request.data)
    
    if serializer.is_valid():
        # Check if email already exists
        email = serializer.validated_data['email']
        if Employee.objects.filter(email=email).exists():
            return Response(
                {'error': 'Employee with this email already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        employee = serializer.save()
        
        # Send confirmation email
        try:
            send_mail(
                'Successfully Registered - Employee Portal',
                f'Dear {employee.name},\n\nYou have been successfully registered in the system.\nYour Employee ID is: {employee.employee_id}\n\nThank you!',
                settings.DEFAULT_FROM_EMAIL,
                [employee.email],
                fail_silently=False,
            )
            print("Email sent successfully")
        except Exception as e:
            # Even if email fails, we still want to return the employee data
            print(f"Email sending failed: {str(e)}")
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FieldworkSet(ModelViewSet):
    queryset = Fieldwork.objects.all()
    serializer_class = FieldworkSerializer

class BillsUploadSet(ModelViewSet):
    queryset = BillsUpload.objects.all()
    serializer_class = BillsUploadSerializer     

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import Employee
from .serializers import EmployeeRegisterSerializer, LoginSerializer, ChangePasswordSerializer
from .utils import generate_password, send_password_email


# ✅ Register employee (Admin)
class EmployeeRegisterView(APIView):
    def post(self, request):
        serializer = EmployeeRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee = serializer.save()

        # generate password
        raw_password = generate_password()
        employee.set_password(raw_password)
        employee.save()

        # send email
        send_password_email(employee.email, employee.employee_id, raw_password)

        return Response({
            "message": "Employee registered successfully. Credentials sent to email.",
            "employee_id": employee.employee_id
        }, status=status.HTTP_201_CREATED)


# ✅ Login employee
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        emp_id = serializer.validated_data['employee_id']
        password = serializer.validated_data['password']

        user = authenticate(request, employee_id=emp_id, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=400)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "employee_id": user.employee_id,
            "name": user.name,
            "role": user.role,
        })


# ✅ Change password (must be logged in)
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        user = request.user
        if not user.check_password(old_password):
            return Response({"error": "Old password incorrect"}, status=400)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully"}, status=200)



class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identifier = serializer.validated_data['identifier']
        password = serializer.validated_data['password']

        try:
            # check by employee_id first, then by email
            if identifier.startswith("TIT"):
                employee = Employee.objects.get(employee_id=identifier)
            else:
                employee = Employee.objects.get(email=identifier)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=404)

        employee.set_password(password)
        employee.save()
        return Response({"message": "Password reset successfully"}, status=200)


from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import EmployeeSerializer
from .models import Employee

class EmployeeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get', 'put', 'patch'], url_path="me")
    def me(self, request):
        user = request.user
        if request.method in ['PUT', 'PATCH']:
            serializer = EmployeeSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = EmployeeSerializer(user)
        return Response(serializer.data)
        
