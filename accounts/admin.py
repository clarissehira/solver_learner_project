from django.contrib import admin

from accounts.models import Instructor, User, Student

# Register your models here.
admin.site.register(User)
admin.site.register(Instructor)
admin.site.register(Student)
# for displaying in admin
# class InstructorAdmin(admin.ModelAdmin):
#     list_display = ('user', 'first_name', 'last_name', 'phone', 
#                   'email', 'course')

# admin.site.register(Instructor, InstructorAdmin)
