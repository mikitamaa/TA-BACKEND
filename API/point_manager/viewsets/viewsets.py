from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from ..models import CustomUser
from ..serializers import CustomUserSerializer

class UserViewSets(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'id'