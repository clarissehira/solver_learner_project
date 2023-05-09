from accounts.models import  User
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from rest_framework import generics,status,permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import(UserSerializer,RegisterInstructorSerializer,
RegisterStudentSerializer) 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



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





