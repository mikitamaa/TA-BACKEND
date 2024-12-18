from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import EventSerializer
from ..models import CustomUser, Liga, Season, Event
from ..permissions import IsAdminUser, IsRangerUser

class EventHandler(APIView):
    #GET
    def get(self, request, id=None):
        if id is not None:
            try:
                event = Event.objects.get(id=id)
                serializer = EventSerializer(event)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Event.DoesNotExist:
                return Response({'message': 'Event tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
        
        if 'season' in request.query_params:
            event_season = request.query_params.get('season')
            try:
                event = Event.objects.filter(season__id=event_season)
                serializer = EventSerializer(event, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Event.DoesNotExist:
                return Response({'message': 'Event tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
            
        if 'liga' in request.query_params:
            event_liga = request.query_params.get('liga')
            try:
                event = Event.objects.filter(liga__id=event_liga)
                serializer = EventSerializer(event, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Event.DoesNotExist:
                return Response({'message': 'Event tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
            
        if 'ranger_assigned' in request.query_params:
            ranger_assigned = request.query_params.get('ranger_assigned')
            try:
                ranger = Event.objects.filter(ranger_assigned__id=ranger_assigned)
                serializer = EventSerializer(ranger, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({'message': 'Event tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
            
        if 'managed_by' in request.query_params:
            admin_assigned = request.query_params.get('managed_by')
            try:
                admin = Event.objects.filter(managed_by=admin_assigned)
                serializer = EventSerializer(admin, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({'message': 'Event tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
            
        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data)
        
    
    
    #REGISTER
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except:
                return Response({'message': 'Masih Error!'})
        return Response({'message': 'Event berhasil dibuat.'})
    
    #UPDATE
    def patch(self, request):
        request_body = request.data
        event_id = request_body['id']
        name = request_body['name']
        season = Season.objects.get(id=request_body['season'])
        liga = Liga.objects.get(id=request_body['liga'])
        managed_by = CustomUser.objects.get(id=request_body['managed_by'])
        ranger_assigned = CustomUser.objects.get(id=request_body['ranger_assigned'])
        max_participant = request_body['max_participant']
        base_point = request_body['base_point']

        get_event_obj = get_object_or_404(Event, pk=event_id)
        get_event_obj.name = name
        get_event_obj.name = name
        get_event_obj.season = season
        get_event_obj.liga = liga
        get_event_obj.managed_by = managed_by
        get_event_obj.ranger_assigned = ranger_assigned
        get_event_obj.max_participant = max_participant
        get_event_obj.base_point = base_point
        get_event_obj.save()
        return Response({
            "message" : str(get_event_obj) + " is successfully edited!",
        }, status=status.HTTP_200_OK)

    #DELETE
    def delete(self, request):
        request_body = request.data
        event_id = request_body['id']
        get_season_obj = get_object_or_404(Event, pk=event_id)
        get_season_obj.delete()
        return Response({
            "message" : str(get_season_obj) + " is successfully edited!",
        }, status=status.HTTP_200_OK)