from django.http import HttpResponseForbidden
from accounts.models import UserProfile

def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to view this page.")
        try:
            profile = UserProfile.objects.get(user=request.user)
            if profile.role != 'teacher':
                return HttpResponseForbidden("You do not have permission to view this page.")
        except UserProfile.DoesNotExist:
            return HttpResponseForbidden("Profile not found.")
        return view_func(request, *args, **kwargs)
    return wrapper