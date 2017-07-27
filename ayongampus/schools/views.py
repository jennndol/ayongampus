from django.shortcuts import render

from .models import StudentCampus


def student_campus_list(request):
    student_campus_list = StudentCampus.objects.filter(user=request.user)
    return render(request, 'schools/student_campus_list.html', {'student_campus_list': student_campus_list})
