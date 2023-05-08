from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import User
from accounts.models import Instructor,Student


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=200)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='instructed_courses')
    description=models.TextField()
    
    def __str__(self):
        return self.name



class Lesson(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    
    def __str__(self):
        return self.name


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['course', 'student']

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} enrolled in {self.course.name}"


class Progress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='progresses')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progresses')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='progress')
    completed_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('enrollment', 'lesson')
    
    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name}'s progress in {self.lesson.name}"

class Assignment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    #instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    file = models.FileField(upload_to='assignments/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    



class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/%Y/%m/%d/',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    github_link = models.CharField(max_length=200, blank=True)  
    
    
    def __str__(self):
        return f"{self.student.first_name} - {self.assignment.name}"