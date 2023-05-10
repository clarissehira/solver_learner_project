from rest_framework import serializers
from accounts.models import User, Student,Instructor

from django.utils.encoding import force_str
from django.utils.http  import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.response import Response

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_student', 'is_instructor']



class RegisterInstructorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=70, required=True)
    last_name = serializers.CharField(max_length=70, required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(max_length=40, required=True)
    course = serializers.CharField(max_length=30, required=True)
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    username = serializers.CharField(max_length=70, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'course', 'username','password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self, **kwargs):
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        username = self.validated_data['username']
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        phone = self.validated_data['phone']
        course = self.validated_data['course']

        if password != password2:
            raise serializers.ValidationError({"error": "passwords do not match"})

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        user.is_instructor = True
        user.save()
        instructor = Instructor.objects.create(user=user,username=username, phone=phone, email=email, course=course)
        instructor.first_name = first_name
        instructor.last_name = last_name
        instructor.save()

        return user


                    
class RegisterStudentSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    first_name = serializers.CharField(max_length=70, required=True)
    last_name = serializers.CharField(max_length=70, required=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=70, required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            is_student=True
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({"error": "password do not match"})

        user.set_password(password)
        user.save()
        

        student = Student.objects.create(user=user)
        student.first_name = user.first_name
        student.last_name = user.last_name
        student.email = user.email
        student.save()
        return user


#reset password by email

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email=serializers.EmailField(min_length=5)

    class Meta:
        fields= ['email']
    

class SetNewPasswordSerializer(serializers.Serializer):
    newpassword= serializers.CharField(min_length=6, max_length= 64, write_only= True)
    uidb64= serializers.CharField(min_length= 1, write_only= True )
    token= serializers.CharField(min_length= 1, write_only= True )

    class Meta:
        fields= '_all_'
    
    def validate(self, attrs):
        try:
            newpassword= attrs.get('newpassword')
            token= attrs.get('token')
            uidb64= attrs.get('uidb64') 
            
            print(f"token: {token}")
            print(f"uidb64: {uidb64}")           
            
            id= force_str(urlsafe_base64_decode(uidb64))
            user= User.objects.get(id=id)
            
            print(f"User: {user}")
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise exceptions.AuthenticationFailed({'Error':'The Reset link is invalid, It was used before!'}, 401)
            
            user.set_password(newpassword)
            user.save()
            return Response({'user': user})                                      
        except Exception as e: 
            
            print(f"error: {e} ") 
            
            raise exceptions.AuthenticationFailed({'Error':'The Reset link is invalid !' }, 401)

