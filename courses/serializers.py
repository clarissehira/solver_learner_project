from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Assignment, Course, Enrollment, Lesson, Progress, Submission

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'instructor', 'description']



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model= Lesson
        fields=['id', 'name', 'course', 'description']



class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'student', 'enrolled_date']

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ['id', 'lesson','enrollment','student','completed','completed_date']




class AssignmentSerializer(serializers.ModelSerializer):
    github_link = serializers.CharField(max_length=200, required=False)

    class Meta:
        model = Assignment
        fields = ['id', 'name', 'description', 'course', 'created_at', 'github_link']


class SubmissionSerializer(serializers.ModelSerializer):
    github_link = serializers.CharField(max_length=200, required=False)

    class Meta:
        model = Submission
        fields = '__all__'

