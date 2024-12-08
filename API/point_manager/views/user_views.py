from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from ..serializers import CustomUserSerializer
from ..models import CustomUser
from ..permissions import IsAdminUser, IsRangerUser


class UserHandler(APIView):
    permission_classes = [AllowAny]
    
    #GET
    def get(self, request, id=None):
        '''if user['is_admin'] == False:
            return Response({'detail' : 'Your credential token is either invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)'''
        if id is not None:
            try:
                user = CustomUser.objects.get(id=id)
                serializer = CustomUserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({'message': 'User tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
        
        user = CustomUser.objects.all()
        serializer = CustomUserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    