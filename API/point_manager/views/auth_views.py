from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers import CustomUserSerializer
from ..models import CustomUser
from ..permissions import IsAdminUser, IsRangerUser

class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('Data Salah!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Data Salah!')
        
        token = RefreshToken.for_user(user)

        response_data = {
                'refresh': str(token),
                'access': str(token.access_token),
                'name': user.name,
                'id': user.id,
                'is_admin': user.is_admin,
                'is_ranger': user.is_ranger
            }
        return Response(response_data, status=status.HTTP_200_OK)
