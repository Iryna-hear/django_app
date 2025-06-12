from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
    )
    user_type = models.CharField(max_length=10, choices=CHOICES)

    def __str__(self):
        return f"{self.username} ({self.user_type})"
    
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    class_name = models.CharField(max_length=50)
    parents = models.ManyToManyField(CustomUser, related_name='children', limit_choices_to={'role': 'parent'})

    def __str__(self):
        return self.user.get_full_name()
    

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=(('present', 'Present'), ('absent', 'Absent')))

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.date} - {self.status}"
    

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    grade = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.grade}"
    
class Homework(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.subject} - Due: {self.due_date}"
    

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From: {self.sender} To: {self.recipient} - {self.subject}"
