from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import SeasonSerializer
from ..models import Season
from ..permissions import IsAdminUser, IsRangerUser

class SeasonHandler(APIView):
    #GET
    def get(self, request):
        if 'id' in request.data:
            try:
                season = Season.objects.get(id=request.data['id'])
                serializer = SeasonSerializer(season)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Season.DoesNotExist:
                return Response({'message': 'Season tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
            
        season = Season.objects.all()
        serializer = SeasonSerializer(season, many=True)
        return Response(serializer.data)
    
    #REGISTER
    def post(self, request):
        serializer = SeasonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response()
    
    #UPDATE
    def patch(self, request):
        request_body = request.data
        season_id = request_body['id']
        name = request_body['name']
        get_season_obj = get_object_or_404(Season, pk=season_id)
        get_season_obj.name = name
        get_season_obj.save()
        return Response({
            "message" : str(get_season_obj) + " is successfully edited!",
        }, status=status.HTTP_200_OK)

    #DELETE
    def delete(self, request):
        request_body = request.data
        season_id = request_body['id']
        get_season_obj = get_object_or_404(Season, pk=season_id)
        get_season_obj.delete()
        return Response({
            "message" : str(get_season_obj) + " is successfully edited!",
        }, status=status.HTTP_200_OK)