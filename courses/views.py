from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import viewsets, authentication, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Assignment, Course, Enrollment, Lesson, Progress, Submission
from .serializers import AssignmentSerializer, CourseSerializer, EnrollmentSerializer, LessonSerializer, ProgressSerializer, SubmissionSerializer
from accounts.permissions import (CanViewAssignmentByEnrolledStudent, CanViewLesson, CanViewLessonByEnrolledStudent, CanViewLessonByInstructor, CanViewStudentProgress, IsCourseInstructor,  IsStudentProgressOwner, IsStudentUser, CanEnrollInCourse, CanViewCourseAssignment, CanSubmitAssignment,
 IsInstructorUser)




class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated & (IsInstructorUser | IsStudentUser)]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, IsStudentUser | IsInstructorUser]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'enroll':
            permission_classes = [IsAuthenticated, CanEnrollInCourse]
        elif self.action == 'submit_assignment':
            permission_classes = [IsAuthenticated, CanSubmitAssignment]
        elif self.request.method == 'POST':
            if self.request.data.get('instructor') and self.request.user.is_instructor:
                permission_classes = [IsAuthenticated, IsInstructorUser]
            else:
               permission_classes = [IsAuthenticated, IsInstructorUser]
        else:
            permission_classes = [IsAuthenticated, IsInstructorUser, IsCourseInstructor]
        return [permission() for permission in permission_classes]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & (IsInstructorUser | IsStudentUser)]
    #permission_classes = [CanViewLesson, CanViewLessonByEnrolledStudent]



    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, IsStudentUser | IsInstructorUser]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, CanViewLesson | CanViewLessonByEnrolledStudent | CanViewLessonByInstructor]
        else:
            permission_classes = [IsAuthenticated, IsInstructorUser]

        return [permission() for permission in permission_classes]



class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated & (IsInstructorUser | IsStudentUser)]
    # permission_classes = [IsAuthenticated, IsInstructorUser]

    # def perform_create(self, serializer):
    #     serializer.save(student=self.request.user)


    # def get_permissions(self):
    #     if self.action in ['list', 'retrieve']:
    #         permission_classes = [IsAuthenticated]
    #     else:
    #         permission_classes = [IsAuthenticated, IsInstructorUser]
    #     return [permission() for permission in permission_classes]

class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
   



    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [CanViewStudentProgress]
        else:
            permission_classes = [IsAuthenticated & IsStudentUser & IsStudentProgressOwner]
        return [permission() for permission in permission_classes]
   



class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsStudentUser | IsInstructorUser, CanViewAssignmentByEnrolledStudent]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, IsStudentUser | IsInstructorUser]
        elif self.action == 'retrieve':
            permission_classes = [IsStudentUser | IsInstructorUser, CanViewAssignmentByEnrolledStudent]
        else:
            permission_classes = [IsInstructorUser]
        return [permission() for permission in permission_classes]




class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated & (IsInstructorUser | IsStudentUser)]

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsAuthenticated, IsStudentUser]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated &(IsInstructorUser | IsStudentUser)]
        else:
            permission_classes = [IsInstructorUser ]
        return [permission() for permission in permission_classes] 

