from django.forms import ModelForm

from .models import City, School, ClassRoom, Student, Teacher, ChosenSchool

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ('name', 'created_at', 'updated_at', )

 
class SchoolForm(ModelForm):
    class Meta:
        model = School
        fields = ('level', 'city', 'name', 'address', 'description', 'is_active', 'created_at', 'updated_at', )


class ClassRoomForm(ModelForm):
    class Meta:
        model = ClassRoom
        fields = ('school', 'name', 'year', )


class ChosenSchoolForm(ModelForm):
    class Meta:
        model = ChosenSchool
        fields = ('user', 'school', )

    
class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ('user', 'class_room', 'nisn', )


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ('user', 'school', 'nip', )
