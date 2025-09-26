import random, string
from django.core.mail import send_mail

def generate_password(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def send_password_email(email, emp_id, password):
    subject = "Your Employee Login Credentials"
    message = f"Hello,\n\nYour Employee ID: {emp_id}\nPassword: {password}\n\nPlease login and change your password."
    send_mail(subject, message, "admin@example.com", [email])

