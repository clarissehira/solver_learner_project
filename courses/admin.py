from django.contrib import admin

from courses.models import  Assignment, Course, Enrollment, Lesson, Progress, Submission

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    def __str__(self):
        return self.name
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(Progress)
admin.site.register(Assignment)
admin.site.register(Submission)