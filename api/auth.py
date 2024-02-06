from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from api.models.employee import Employee
from rest_framework import serializers
from rest_framework import status

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password')

class LoginAPIView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )
        if user:
            login(request, user)
        return response
    
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        logout(request)
        return Response({'success': 'User logged out successfully.'})

class RegisterAPIView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Employee.objects.create(user=user, points=0)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
