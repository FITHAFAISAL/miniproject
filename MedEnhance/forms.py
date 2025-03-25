from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    hospital_id = forms.CharField(
        max_length=20, 
        required=False, 
        help_text='Optional: Enter your hospital ID if applicable'
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'hospital_id', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        return user