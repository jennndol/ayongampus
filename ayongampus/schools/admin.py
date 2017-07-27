from django.contrib import admin

from .models import City, School, StudentClassRoom, Student, Teacher, ClassRoom

admin.site.register(City)
admin.site.register(ClassRoom)
admin.site.register(School)
admin.site.register(StudentClassRoom)
admin.site.register(Student)
admin.site.register(Teacher)
