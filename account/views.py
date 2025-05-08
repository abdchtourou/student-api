from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializer import LoginSerializer, SignupSerializer, UserSerializer
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from student.models import Student
import logging
import traceback

logger = logging.getLogger(__name__)
User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    try:
        data = request.data
        print("\n=== New Signup Request ===")
        print(f"Email: {data.get('email')}")
        print(f"Name: {data.get('name')}")
        print(f"Major: {data.get('major')}")
        
        logger.info("New signup request received", extra={
            'email': data.get('email'),
            'student_name': data.get('name'),
            'major': data.get('major')
        })
        
        serializer = SignupSerializer(data=data)
        if not serializer.is_valid():
            print("\n=== Validation Failed ===")
            print(f"Errors: {serializer.errors}")
            logger.warning("Signup validation failed", extra={'errors': serializer.errors})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=data['email']).exists():
            print("\n=== Email Already Exists ===")
            print(f"Email: {data['email']}")
            logger.warning("Signup failed - Email already exists", extra={'email': data['email']})
            return Response(
                {'error': 'Email already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.create_user(
            email=data['email'],
            password=data['password']
        )
        
        student = Student.objects.create(
            user=user,
            name=data.get('name', data['email'].split('@')[0]),
            email=data['email'],
            major=data.get('major', '')
        )
        
        print("\n=== User Created Successfully ===")
        print(f"User ID: {user.id}")
        print(f"Student ID: {student.id}")
        print(f"Created at: {user.date_joined}")
        print("==============================\n")
        
        logger.info("User and student record created successfully", extra={
            'user_id': user.id,
            'student_id': student.id,
            'created_at': user.date_joined
        })
        
        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)
        
        return Response({
            'message': 'User and Student record created successfully',
            'user': user_serializer.data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        error_traceback = traceback.format_exc()
        print("\n=== Error During Signup ===")
        print(f"Error: {str(e)}")
        print(f"Traceback: {error_traceback}")
        print("==========================\n")
        
        logger.error("Error during user creation", extra={
            'error': str(e),
            'traceback': error_traceback,
            'request_data': data
        })
        return Response(
            {'error': f'An error occurred during registration: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
 
    data = request.data
    serializer = LoginSerializer(data=data)
    
    if not serializer.is_valid():
        logger.warning("Login validation failed", extra={'errors': serializer.errors})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(
        email=serializer.validated_data['email'],
        password=serializer.validated_data['password']
    )
    
    if user is None:
        logger.warning("Login failed - Invalid credentials", extra={'email': data.get('email')})
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    logger.info("User logged in successfully", extra={'user_id': user.id})
    refresh = RefreshToken.for_user(user)
    user_serializer = UserSerializer(user)
    
    return Response({
        'message': 'Login successful',
        'user': user_serializer.data,
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_data(request):
 
    user = request.user
    logger.info("User data retrieved", extra={'user_id': user.id})
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


