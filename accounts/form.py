from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from students.models import Student  
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

class SignUpForm(UserCreationForm):
    
    alpha_validator = RegexValidator(r'^[a-zA-Z]*$', 'Only alphabetic characters are allowed.')
    
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=255, help_text='Required. Inform a valid email address.')
    student_number = forms.IntegerField(required=False, help_text='Optional unless you are a student.')
    field_of_study = forms.CharField(max_length=50, required=False, help_text='Optional unless you are a student.', validators=[alpha_validator])
    gpa = forms.FloatField(
        required=False, 
        help_text='Optional unless you are a student.',
        validators=[MinValueValidator(0), MaxValueValidator(4)]
        )
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=True)
   
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role')
    
    def save(self, commit=True):
        user = super().save(commit=False)


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
                        'email': self.cleaned_data['email'],
                        'student_number': self.cleaned_data['student_number'],
                        'field_of_study': self.cleaned_data['field_of_study'],
                        'gpa': self.cleaned_data['gpa']
                    }
                )

        return user
    
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        student_number = cleaned_data.get('student_number')
        field_of_study = cleaned_data.get('field_of_study')
        gpa  = cleaned_data.get('gpa')
        # Check if the role is 'student' and if so, enforce that student_number is provided
        if role == 'student' and not student_number:
            self.add_error('student_number', 'Student number is required for students.')
        if role == 'student' and not field_of_study:
            self.add_error('field_of_study', 'field of study is required for students.')
        if role == 'student' and not gpa:
            self.add_error('gpa', 'gpa is required for students.') 
        return cleaned_data