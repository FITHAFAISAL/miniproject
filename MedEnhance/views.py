"""from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
import random

from .forms import CustomUserCreationForm
from .models import OTPVerification, HospitalVerification
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")

def results(request):
    return render(request, "results.html")

def upload(request):
    return render(request, "upload.html")

def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def send_otp_email(user, otp):
    send_mail(
        'Your OTP for Email Verification',
        f'Your OTP is: {otp}',
        'your_email@example.com',  # Replace with your actual email
        [user.email],
        fail_silently=False,
    )

def user_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until verified
            user.save()

            # Generate and send OTP
            otp = generate_otp()
            OTPVerification.objects.create(user=user, otp=otp)
            send_otp_email(user, otp)

            # Create Hospital Verification entry
            if user.hospital_id:
                HospitalVerification.objects.create(user=user)

            messages.success(request, 'Please check your email to verify your account.')
            return redirect('verify_otp')
    else:
        form = CustomUserCreationForm()
    return render(request, 'login.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        try:
            otp_verification = OTPVerification.objects.get(otp=otp)
            user = otp_verification.user
            user.is_active = True
            user.is_email_verified = True
            user.save()

            # Delete OTP record after verification
            otp_verification.delete()

            messages.success(request, 'Email verified successfully!')
            return redirect('login')
        except OTPVerification.DoesNotExist:
            messages.error(request, 'Invalid OTP. Please try again.')
    
    return render(request, 'verify_otp.html')

@login_required
def admin_dashboard(request):
    if request.user.user_type != 'admin':
        return redirect('login')

    pending_verifications = HospitalVerification.objects.filter(verification_status='pending')
    return render(request, 'admin_dashboard.html', {
        'pending_verifications': pending_verifications
    })

@login_required
def verify_hospital_id(request, verification_id):
    if request.user.user_type != 'admin':
        return redirect('login')

    verification = HospitalVerification.objects.get(id=verification_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        notes = request.POST.get('notes', '')
        
        if action == 'approve':
            verification.verification_status = 'approved'
            verification.user.is_hospital_verified = True
        else:
            verification.verification_status = 'rejected'
        
        verification.admin_notes = notes
        verification.verified_by = request.user
        verification.save()
        verification.user.save()
        
        return redirect('admin_dashboard')

    return render(request, 'verify_hospital_id.html', {'verification': verification})
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import CustomUser, OTPVerification
from .forms import CustomUserCreationForm
import random
def index(request):
    return render(request, "index.html")
def login(request):
    return render(request, "login.html")

def results(request):
    return render(request, "results.html")

def upload(request):
    return render(request, "upload.html")

def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def send_verification_email(user, otp):
    send_mail(
        'Verify Your Email',
        f'Your verification OTP is: {otp}',
        'noreply@medenhance.com',
        [user.email],
        fail_silently=False,
    )

def user_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till email is verified
            
            # Set user type based on form data
            user_type = request.POST.get('user_type', 'user')
            user.user_type = user_type
            
            user.save()

            # Generate and send OTP
            otp = generate_otp()
            OTPVerification.objects.create(user=user, otp=otp)
            send_verification_email(user, otp)

            messages.success(request, 'Account created. Please verify your email.')
            return redirect('verify_otp')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        try:
            otp_verification = OTPVerification.objects.get(otp=otp)
            user = otp_verification.user
            user.is_active = True
            user.is_email_verified = True
            user.save()

            # Delete OTP record
            otp_verification.delete()

            messages.success(request, 'Email verified successfully!')
            return redirect('login')
        except OTPVerification.DoesNotExist:
            messages.error(request, 'Invalid OTP. Please try again.')
    
    return render(request, 'verify_otp.html')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST.get('user_type', 'user')
        
        # Try to authenticate with username or email
        user = authenticate(
            request, 
            username=username, 
            password=password
        )
        
        if user is not None:
            # Check user type
            if user.user_type == user_type:
                login(request, user)
                
                # Redirect based on user type
                if user_type == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid user type.')
        else:
            messages.error(request, 'Invalid login credentials.')
    
    return render(request, 'login.html')
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse, reverse_lazy

class CustomPasswordResetView(PasswordResetView):
    template_name = 'custom_password_reset.html'  # Your custom template
    email_template_name = 'custom_password_reset_email.html'  # Your custom email template
    subject_template_name = 'custom_password_reset_subject.txt'  # Your custom subject template
    success_url = reverse_lazy('password_reset_done')  # Redirect URL after success

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'custom_password_reset_confirm.html'  # Your custom template
    success_url = reverse_lazy('password_reset_complete')  # Redirect URL after password reset
   