from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Student
from .forms import Student_Form
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.contrib.auth.models import User
from .decorators import teacher_required 

@teacher_required
def index(request):
    return render(request, 'students/index.html', {
        'students': Student.objects.all()
    })
# def profile(request, id):
#     user = get_object_or_404(User, pk=id)
#     return render(request, 'students/profile.html', {'user': user})
def profile(request, id):
    student = get_object_or_404(Student, user__id=id)
    return render(request, 'students/profile.html', {'student': student})


# def view_student(request, id):
#     student = Student.objects.get(pk=id)
#     return render(request, 'students/profile.html', {'student': student})

def view_student(request, id):
    student = get_object_or_404(Student, pk=id)
    return render(request, 'students/profile.html', {'student': student})

@teacher_required
def add(request):
    if request.method == 'POST':
        form = Student_Form(request.POST)
        if form.is_valid():
            new_student_num = form.cleaned_data['student_number']
            new_fname = form.cleaned_data['first_name']
            new_lname = form.cleaned_data['last_name']
            new_email = form.cleaned_data['email']
            new_program = form.cleaned_data['field_of_study']            
            new_gpa = form.cleaned_data['gpa']

            new_student = Student(
                student_number = new_student_num,
                first_name = new_fname,
                last_name = new_lname,
                email = new_email,
                field_of_study = new_program,
                gpa = new_gpa
            )
            new_student.save()
            return render(request, 'students/add.html', {
                'form': Student_Form(),
                'success': True
            })
    else:
            return render(request, 'students/add.html', {
                'form': Student_Form()
            })

@teacher_required 
def edit(request, id):
    if request.method == 'POST':
        student = Student.objects.get(pk=id)
        form = Student_Form(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return render(request, 'students/edit.html', {
                'form': form,
                'success': True
            })
    else:
        student = Student.objects.get(pk=id)
        form = Student_Form(instance=student)
        if form.is_valid():
            form.save()
    return render(request, 'students/edit.html', {
        'form': form
    })

@teacher_required
def delete(request, id):
    if request.method == 'POST':
        student = Student.objects.get(pk=id)
        student.delete()
    return HttpResponseRedirect(reverse('index'))

# def view(request, id):
    
#     return render(request, 'students/profile.html', {
#         'students': Student.objects.get(pk=id)
#     })