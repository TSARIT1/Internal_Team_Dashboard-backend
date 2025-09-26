from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket-rise')
router.register(r'crm', CrmViewSet, basename='crm')
router.register(r'adminpayments', AdminPaymentsSet, basename='adminpayments')
router.register(r'adminemployeeregister', AdminEmployeeRegisterSet, basename='adminemployeeregister')
router.register(r'fieldwork',FieldworkSet, basename='fieldwork')
router.register(r'billsupload',BillsUploadSet, basename='billsupload')


router.register(r'user', EmployeeViewSet, basename="user")







urlpatterns = [
   path('',include(router.urls)),
   path('register/', EmployeeRegisterView.as_view(), name="employee_register"),
   path('login/', LoginView.as_view(), name="employee_login"),
   path('change-password/', ChangePasswordView.as_view(), name="change_password"),
   path('forgot-password/', ForgotPasswordView.as_view(), name="forgot_password"),
   
    
]



