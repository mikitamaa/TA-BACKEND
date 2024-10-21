from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import LigaSerializer
from ..models import Liga
from ..permissions import IsAdminUser, IsRangerUser

class LigaHandler(APIView):
    #get
    def get(self, request, id=None):
        # then check the token's validity
        if id is not None:
            try:
                liga = Liga.objects.get(id=id)
                serializer = LigaSerializer(liga)
                return Response({"data" : serializer.data}, status=status.HTTP_200_OK)
            except Liga.DoesNotExist:
                return Response({'message': 'Liga tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
            
        liga = Liga.objects.all()
        serializer = LigaSerializer(liga, many=True)
        return Response(serializer.data)
    
    #register
    def post(self, request):
        serializer = LigaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response()
    
    #update
    def patch(self, request):
        request_body = request.data
        liga_id = request_body['id']
        name = request_body['name']
        get_liga_obj = get_object_or_404(Liga, pk=liga_id)
        get_liga_obj.name = name
        get_liga_obj.save()
        return Response({
            "message" : str(get_liga_obj) + " is successfully edited!",
        }, status=status.HTTP_200_OK)

    #delete
    def delete(self, request):
        request_body = request.data
        liga_id = request_body['id']
        get_liga_obj = get_object_or_404(Liga, pk=liga_id)
        get_liga_obj.delete()
        return Response({
            "message" : str(get_liga_obj) + " is successfully edited!",
        }, status=status.HTTP_200_OK)