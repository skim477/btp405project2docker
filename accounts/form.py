from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from students.models import Student  

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=255, help_text='Required. Inform a valid email address.')
    student_number = forms.IntegerField(help_text='Required. Inform a valid student number.')
    field_of_study = forms.CharField(max_length=50)
    gpa = forms.FloatField(required=False)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=True)
   
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            # Create UserProfile only if it doesn't already exist
            UserProfile.objects.get_or_create(user=user, defaults={'role': self.cleaned_data['role']})

            if self.cleaned_data['role'] == 'student':
                Student.objects.get_or_create(
                    user=user,
                    defaults={
                        'first_name': self.cleaned_data['first_name'],
                        'last_name': self.cleaned_data['last_name'],
                        'student_number': self.cleaned_data['student_number'],
                        'field_of_study': self.cleaned_data['field_of_study'],
                        'gpa': self.cleaned_data['gpa']
                    }
                )

        return user