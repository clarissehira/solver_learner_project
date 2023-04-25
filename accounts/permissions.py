from rest_framework.permissions import BasePermission
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework import permissions
from django.shortcuts import get_object_or_404


from courses.models import Assignment, Course, Enrollment, Lesson


class IsStudentUser(BasePermission):
    """
    Allows access only to student users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_student


class CanEnrollInCourse(IsAuthenticated):
    """
    Allows access to authenticated users who are students and can enroll in a course.
    """
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_student


class CanViewCourseAssignment(IsAuthenticated):
    """
    Allows access to authenticated users who are students and can view assignments in a course.
    """
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_student


class CanSubmitAssignment(IsAuthenticated):
    """
    Allows access to authenticated users who are students and can submit assignments.
    """
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_student


class IsStudentProgressOwner(BasePermission):
    """
    Allows access only to the owner of the progress object.
    """
    def has_object_permission(self, request, view, obj):
        return obj.student == request.user.student


class CanViewStudentProgress(BasePermission):
    """
    Allows access only to instructors who own the course that the student is enrolled in.
    """
    def has_object_permission(self, request, view, obj):
        return obj.enrollment.course.instructor == request.user.instructor



class IsInstructorUser(BasePermission):
    """
    Allows access only to instructor users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_instructor


class CanCreateCourse(IsInstructorUser):
    """
    Allows access to authenticated users who are instructors and can create a course.
    """
    def has_permission(self, request, view):
        return super().has_permission(request, view)


class CanUpdateCourse(IsInstructorUser):
    """
    Allows access to authenticated users who are instructors and can update a course they own.
    """
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view) and obj.instructor == request.user.instructor


class CanDeleteCourse(IsInstructorUser):
    """
    Allows access to authenticated users who are instructors and can delete a course they own.
    """
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view) and obj.instructor == request.user.instructor


class CanViewCourse(IsInstructorUser):
    """
    Allows access to authenticated users who are instructors and can view a course they own.
    """
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view) and obj.instructor == request.user.instructor


class CanCreateLesson(IsInstructorUser):
    """
    Allows access to authenticated users who are instructors and can create a lesson in a course they own.
    """
    def has_permission(self, request, view):
        return super().has_permission(request, view)


class CanUpdateLesson(IsInstructorUser):
    """
    Allows access to authenticated users who are instructors and can update a lesson in a course they own.
    """
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view) and obj.course.instructor == request.user.instructor


class CanDeleteLesson(IsInstructorUser):
    """
    Allows access to authenticated users who are instructors and can delete a lesson in a course they own.
    """
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view) and obj.course.instructor == request.user.instructor

class CanViewLesson(IsInstructorUser):
    """
    Allows access to authenticated users who are instructors and can view a lesson in a course they own.
    """
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view) and obj.course.instructor == request.user.instructor




class CanModifyCourse(permissions.BasePermission):
    """
    Custom permission to allow instructors to modify course.
    """
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and user.is_instructor:
            return True
        return False






class IsCourseInstructor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (request.user.is_instructor or obj.instructor == request.user)



class CanViewLessonByEnrolledStudent(BasePermission):
    """
    Custom permission to allow enrolled students to view lessons they are enrolled in.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_instructor:
                return True
            else:
                lesson_id = view.kwargs.get('pk')
                lesson = get_object_or_404(Lesson, pk=lesson_id)
                course = lesson.course
                enrolled = Enrollment.objects.filter(course=course, student=request.user)
                return enrolled.exists()
        return False




class CanViewLessonByInstructor(BasePermission):
    """
    Custom permission to allow instructors to view lessons of the course.
    """

    def has_permission(self, request, view):
        lesson_id = view.kwargs.get('pk')
        lesson = get_object_or_404(Lesson, pk=lesson_id)

        # Check if the user is the instructor of the course that the lesson belongs to
        if request.user.is_authenticated:
            instructor_courses = request.user.instructor_courses.all()
            if instructor_courses.filter(pk=lesson.course.pk).exists():
                return True

        return False





class CanViewAssignmentByEnrolledStudent(BasePermission):
    """
    Custom permission to allow enrolled students to view assignments they are enrolled in.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_instructor:
                return True
            else:
                assignment_id = view.kwargs.get('pk')
                assignment = get_object_or_404(Assignment, pk=assignment_id)
                course = assignment.course
                enrolled_students = Enrollment.objects.filter(course=course, student=request.user)
                return enrolled_students.exists()
        return False

    





