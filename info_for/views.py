from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from models import CustomUser, Student, Attendance, Grade, Homework, Message
from django.views import View


class StudentView(LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        students = Student.objects.all()
        return render(request, 'info_for/student_list.html', {'students': students})
    







# Create your views here.
