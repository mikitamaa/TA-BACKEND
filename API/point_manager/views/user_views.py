from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from ..serializers import CustomUserSerializer
from ..models import CustomUser
from ..permissions import IsAdminUser, IsRangerUser

class UserHandler(APIView):
    permission_classes = [AllowAny]

    # GET
    def get(self, request, id=None):
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

    # PATCH
    def patch(self, request, id=None):
        if id is None:
            return Response({'message': 'ID diperlukan untuk memperbarui user.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomUserSerializer(user, data=request.data, partial=True)  # Partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    def delete(self, request, id=None):
        if id is None:
            return Response({'message': 'ID diperlukan untuk menghapus user.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(id=id)
            user.delete()
            return Response({'message': 'User berhasil dihapus.'}, status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)

    