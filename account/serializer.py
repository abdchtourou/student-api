from rest_framework import serializers
from django.contrib.auth import get_user_model
from student.models import Student

User = get_user_model()

class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True, min_length=8)
    name = serializers.CharField(required=False, allow_blank=True)
    major = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class UserSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()

    def get_student(self, obj):
        if hasattr(obj, 'student'):
            return {
                'name': obj.student.name,
                'email': obj.student.email,
                'major': obj.student.major
            }
        return None

    class Meta:
        model = User
        fields = ['id', 'email', 'date_joined', 'student']
        read_only_fields = ['id', 'date_joined']


