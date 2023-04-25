from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'courses', views.CourseViewSet,basename="courses")
router.register(r'lessons', views.LessonViewSet,basename="lessons")
router.register(r'enrollments', views.EnrollmentViewSet,basename="enrollments")
router.register(r'progress', views.ProgressViewSet,basename="progress")
router.register(r'assignments', views.AssignmentViewSet,basename="Assignments")
router.register(r'assign/submission', views.SubmissionViewSet,basename="submission")


urlpatterns = [
    path('', include(router.urls)),
]
