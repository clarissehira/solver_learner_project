

from django.urls import path,re_path

from accounts.views import (ChangePasswordView, InstructorRegisterView,  LoginView, 
LogoutView,ResetpasswordEmailRequest,StudentRegisterView ,  SetNewPasswordApi, 
PasswordCheckTokenApi)


urlpatterns = [
  path('register/instructor/',InstructorRegisterView.as_view(), name="instructorregister"),
  path('register/student/',StudentRegisterView.as_view(), name="studentregister"),
  path('login/',LoginView.as_view(),name="login"),
  path('logout/',LogoutView.as_view(),name="logout"),
  path('change_password/', ChangePasswordView.as_view()),
  path('request-reset-email/',ResetpasswordEmailRequest.as_view(),name='request-reset-email'),
  path('password-reset-confirm/<uidb64>/<token>/',PasswordCheckTokenApi.as_view(),name='password-reset-confirm'),
  path('resetpassword/', SetNewPasswordApi.as_view(), name='password-reset-done'),
 
  
   
]

# from django.urls import path, include
# from rest_framework import routers
# from . import views

# router = routers.DefaultRouter()
# router.register(r'register/instructor/', views.InstructorRegisterView,basename="instructor")
# router.register(r'register/student/', views.StudentRegisterView,basename="student")
# router.register(r'login', views.LoginView,basename="login")
# router.register(r'logout', views.LogoutView,basename="logout")
# router.register(r'change_password/', views.ChangePasswordView,basename="changepassword")



# urlpatterns = [
#     path('', include(router.urls)),]
