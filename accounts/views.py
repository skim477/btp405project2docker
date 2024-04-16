# from django.shortcuts import render

# # Create your views here.
# # accounts/views.py
# from django.contrib.auth.forms import UserCreationForm
# from django.urls import reverse_lazy, reverse
# from django.views.generic import CreateView
# from django.views import generic

# from django.contrib.auth import login
# from django.shortcuts import redirect

# class SignUpView(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy("login")
#     template_name = "registration/signup.html"

#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         response = super().form_valid(form)  # Save the user first
#         user = form.save()
#         login(self.request, user)  # Log the user in
#         return redirect(reverse('profile', kwargs={'id': user.id}))  # Redirect to the user's profile
    
    
from django.shortcuts import render

# Create your views here.
# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.views import generic
from .form import SignUpForm, UserProfile
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import redirect


class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        try:
            profile = UserProfile.objects.get(user=user)
            if profile.role == 'teacher':
                return reverse_lazy('index')
            elif profile.role == 'student':
                return reverse_lazy('profile', kwargs={'id': user.id})
        except UserProfile.DoesNotExist:
            return super().get_success_url()  # Fallback to the default success URL

        return super().get_success_url()
    
    
class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        response = super().form_valid(form)  # Save the user first
        user = form.save()
        login(self.request, user)  # Log the user in     
           
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.role == 'teacher':
            return redirect('index')  # Redirect to the main index page
        elif user_profile.role == 'student':
            return redirect('profile', id=user.id)  # Redirect to the student profile page

        return redirect('index')  # Default redirect if role isn't specified

       # return redirect(reverse('profile', kwargs={'id': user.id}))  # Redirect to the user's profile