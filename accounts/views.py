from accounts.models import  User
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from rest_framework import generics,status,permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import(UserSerializer,RegisterInstructorSerializer,
RegisterStudentSerializer, ResetPasswordEmailRequestSerializer,SetNewPasswordSerializer) 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError, force_bytes
from django.utils.http  import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse 
from accounts.utils import Util



# Create your views here.
class InstructorRegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class=RegisterInstructorSerializer
    def post(self,request, *args, **Kwargs):
         serializer=self.get_serializer(data=request.data)
         serializer.is_valid(raise_exception=True)
         user=serializer.save()
         user_serializer = UserSerializer(user, context=self.get_serializer())
         return Response(
            {
            "user": user_serializer.data,
            "token":Token.objects.get(user=user).key,
            "message":"account created successfully"
            }
         )



class StudentRegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class=RegisterStudentSerializer
    
    def post(self,request, *args, **Kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        user_serializer = UserSerializer(user, context={'request': request})
        return Response({
            "user": user_serializer.data,
            "token":Token.objects.get(user=user).key,
            "message":"account created successfully"
        })



class LoginView(APIView):
    permission_classes = [AllowAny]
    
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            200: 'OK',
            401: 'Unauthorized',
            400: 'Bad Request'
        }
    )

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                # Check if the user has a Token object
                token, created = Token.objects.get_or_create(user=user)

                return Response({'token': token.key})
            else:
                return Response({'error': 'Account is disabled'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
## logout user
class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            200: 'OK',
            401: 'Unauthorized'
        }
    )

    def post(self, request, format=None):
        # Delete the user's token
        request.auth.delete()
        return Response({'message': 'Logged out successfully.'})



class ChangePasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING),
                'new_password1': openapi.Schema(type=openapi.TYPE_STRING),
                'new_password2': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            200: 'OK',
            400: 'Bad Request'
        }
    )

    def post(self, request, format=None):
        user = request.user
        # Create a password change form with the request data
        form = PasswordChangeForm(user, request.data)
        if form.is_valid():
            form.save()
            # Return success response
            return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        else:
            # Return validation error response
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)



#RESET PASSWORD BY EMAIL

class ResetpasswordEmailRequest (generics.GenericAPIView):
    serializer_class=ResetPasswordEmailRequestSerializer
    permission_classes=[]

    def post(self, request):
        serializer= self.serializer_class(data= request.data)   

        email=request.data['email']

        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)

            uidb64= urlsafe_base64_encode(force_bytes(user.id) )
            token=PasswordResetTokenGenerator().make_token(user)
            current_site=get_current_site(
                request=request).domain
            relativeLink=reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token':token})
            abs_url='http://'+current_site+relativeLink
            email_body='Hello '+ user.first_name+'.\n\nUse the link below to reset your password.\n'+ abs_url
            data={'email_body':email_body, 'to_email':user.email,'email_subject': 'Reset your password'}
    
            Util.send_email(data)
            return Response({'Email sent': 'We sent you an email with reset password link.' })                
        return Response({'Error': 'Account with this email not found!' })

class PasswordCheckTokenApi(APIView):
    permission_classes=[]
    def get(self, request, uidb64, token):
        try:
            id= smart_str(urlsafe_base64_decode(uidb64))
            user= User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'Error': 'Token is invalid, Request new one.' })
            return Response({'Success': True, 'Message':'Credentials are valid', 'uidb64': uidb64, 'token': token })
 
        except DjangoUnicodeDecodeError as identifier:
                return Response({'Error': 'Token is invalid, Request new one.' })
           
class SetNewPasswordApi(generics.GenericAPIView):
    serializer_class= SetNewPasswordSerializer
    permission_classes= [AllowAny,]
       
    def patch(self, request):
        serializer= self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception= True)        
        return Response({'Success': True, 'Message':'Password reset successfully'}, status= status.HTTP_200_OK)

        





