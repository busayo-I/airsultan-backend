from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from drf_spectacular.utils import extend_schema, OpenApiExample

from .serializers import LoginSerializer, AdminUserSerializer, ChangePasswordSerializer

User = get_user_model()


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Auth'],
        summary='Admin Login',
        description='Authenticate admin user with email and password. Returns JWT access and refresh tokens.',
        request=LoginSerializer,
        responses={200: AdminUserSerializer},
        examples=[
            OpenApiExample(
                'Login Example',
                value={'email': 'admin@airsultan.com.ng', 'password': 'yourpassword'},
                request_only=True,
            )
        ]
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email    = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user     = authenticate(request, email=email, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'status'  : 'success',
                    'message' : 'Login successful',
                    'data'    : {
                        'user'          : AdminUserSerializer(user).data,
                        'access_token'  : str(refresh.access_token),
                        'refresh_token' : str(refresh),
                    }
                }, status=status.HTTP_200_OK)

            return Response({
                'status'  : 'error',
                'message' : 'Invalid email or password'
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            'status'  : 'error',
            'message' : serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Auth'],
        summary='Admin Logout',
        description='Blacklist the refresh token to log out the admin user.',
        request=None,
        responses={200: None},
        examples=[
            OpenApiExample(
                'Logout Example',
                value={'refresh_token': 'your-refresh-token-here'},
                request_only=True,
            )
        ]
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                'status'  : 'success',
                'message' : 'Logged out successfully'
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                'status'  : 'error',
                'message' : 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Auth'],
        summary='Change Admin Password',
        description='Change the currently logged-in admin password. Requires old password for verification.',
        request=ChangePasswordSerializer,
        responses={200: None},
        examples=[
            OpenApiExample(
                'Change Password Example',
                value={
                    'old_password'    : 'oldpassword123',
                    'new_password'    : 'newpassword123',
                    'confirm_password': 'newpassword123'
                },
                request_only=True,
            )
        ]
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user

            if not user.check_password(serializer.validated_data['old_password']):
                return Response({
                    'status'  : 'error',
                    'message' : 'Old password is incorrect'
                }, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return Response({
                'status'  : 'success',
                'message' : 'Password changed successfully'
            }, status=status.HTTP_200_OK)

        return Response({
            'status'  : 'error',
            'message' : serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Auth'],
        summary='Get Logged-in Admin',
        description='Returns the profile details of the currently authenticated admin user.',
        responses={200: AdminUserSerializer},
    )
    def get(self, request):
        return Response({
            'status' : 'success',
            'data'   : AdminUserSerializer(request.user).data
        }, status=status.HTTP_200_OK)