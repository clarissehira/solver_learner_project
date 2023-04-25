from rest_framework import serializers
from accounts.models import User, Student,Instructor

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
