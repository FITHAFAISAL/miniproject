
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import CustomUser, OTPVerification
from .forms import CustomUserCreationForm
import random
from PIL import Image
import os
import shutil
from .gan_model import process_with_gan
from .explainable_ai import compute_image_metrics

from django.conf import settings
MODEL_PATH = os.path.join(settings.BASE_DIR, 'models', 'net_g_latest.pth')


def index(request):
    return render(request, "index.html")
def login(request):
    return render(request, "login.html")

def results(request):
    """Display the processed image with enhancement metrics."""
    output_image_url = "/OutputImages/OutputImage.png"  # Static path for serving output
    
    # Compute enhancement metrics
    enhancement_metrics = compute_image_metrics()
    
    context = {
        "output_image_url": output_image_url,
        "metrics": enhancement_metrics
    }
    return render(request, "results.html", context)

def upload(request):
    # return HttpResponse("Hello")
    print(request.user)
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

import random
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Prevent login before OTP verification
            user.save()

            # Generate OTP
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            request.session['registered_user_id'] = user.id

            # Send OTP email
            send_mail(
                'Your OTP for MedEnhance',
                f'Your OTP is {otp}',
                'noreply@medenhance.com',
                [user.email],
                fail_silently=False,
            )

            return redirect('verify_otp')
    else:
        form = CustomUserCreationForm()    
    return render(request, 'signup.html', {'form': form})
from django.contrib.auth import get_user_model

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_otp = str(request.session.get('otp'))

        if entered_otp == session_otp:
            user_id = request.session.get('registered_user_id')
            User = get_user_model()
            try:
                user = User.objects.get(id=user_id)
                user.is_active = True
                user.save()
                # Clean up session
                del request.session['otp']
                del request.session['registered_user_id']
                return redirect('upload_image')  # redirect to upload.html
            except User.DoesNotExist:
                return render(request, 'verify_otp.html', {'error': 'User not found.'})
        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP. Try again.'})

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

from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import UploadedImage  # Assuming you have a model to store uploaded image info

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.conf import settings
from .models import UploadedImage

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']

        
        # Use MEDIA_ROOT as storage location
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(image.name, image)  # No need to manually add "uploads/"
        
        # Get the URL to access the uploaded image
        uploaded_image_url = fs.url(filename)
        
        # Save the image path in the database
        #new_image = UploadedImage(image=f"media/{filename}")  # Update this based on your model field
        #new_image.save()


        input_path = os.path.join(settings.INPUT_IMAGE_DIR, 'InputImage.png')
        with open(input_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        # Process the image using GAN model
        output_path = process_with_gan()

        return redirect('results')  # Ensure 'results' is a valid URL name

    return render(request, 'upload.html')
 # Render the upload page again if it's a GET request

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
   