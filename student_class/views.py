from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import StudentClass, StudentClassStudent
from decisions.models import Course
from datetime import datetime


@login_required
def home(request):
    if not request.user.is_staff:
        raise Exception('Not allowed for non-staff')
    student_classes = StudentClass.objects.filter(instructor=request.user)
    return render(request, 'student_class/index.html', {
        'student_classes': student_classes,
    })


@login_required
def show(request, id):
    if not request.user.is_staff:
        raise Exception('Not allowed for non-staff')
    student_class = StudentClass.objects.get(pk=id)
    if request.method == 'POST':
        student_class.starting_module = int(request.POST.get('starting_module'))
        student_class.save()
    return render(request, 'student_class/show.html', {
        'student_class': student_class,
        'num_modules': Course.num_modules(),
    })


@login_required
def student(request, id):
    scs = StudentClassStudent.objects.get(pk=id)
    return render(request, 'student_class/student.html', {
        'student': scs,
        'student_class': scs.student_class,
    })


@login_required
def create(request):
    if not request.user.is_staff:
        raise Exception('Not allowed for non-staff')
    student_class = StudentClass()
    student_class.instructor = request.user
    student_class.save()
    return redirect('/class/show/'+str(student_class.id))


@login_required
def join(request, id):
    student_class = StudentClass.objects.get(pk=id)
    student = StudentClassStudent()
    student.student_class = student_class
    student.current_module = student_class.starting_module
    student.course = Course.load_course(request)
    student.save()
    return redirect('/class/student/'+str(student.id))


@login_required
def leave(request, id):
    student_class = StudentClass.objects.get(pk=id)
    scs = StudentClassStudent.objects.filter(student_class=student_class, course=Course.load_course(request)).first()
    scs.delete()
    return redirect('/')


@login_required
def delete(request, id):
    if not request.user.is_staff:
        raise Exception('Not allowed for non-staff')
    student_class = StudentClass.objects.get(pk=id)
    student_class.delete()
    return redirect('/class')


@login_required
def close(request, id):
    if not request.user.is_staff:
        raise Exception('Not allowed for non-staff')
    student_class = StudentClass.objects.get(pk=id)
    student_class.completed_on = datetime.now()
    student_class.save()
    return redirect('/class/'+str(id))


@login_required
def reopen(request, id):
    if not request.user.is_staff:
        raise Exception('Not allowed for non-staff')
    student_class = StudentClass.objects.get(pk=id)
    student_class.completed_on = None
    student_class.save()
    return redirect('/class/'+str(id))
