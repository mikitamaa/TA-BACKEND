from django.shortcuts import get_object_or_404
from django.db import models
from django.db.models import Q, Sum

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from ..serializers import ParticipationSerializer, AggregatedParticipationSerializer
from ..models import Player, Participation, Event
from ..permissions import IsAdminUser, IsRangerUser

class ParticipationHandler(viewsets.ViewSet):
    #GET
    def all_participation(self, request):
        participation = Participation.objects.all()
        serializer = ParticipationSerializer(participation, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def event_participation(self, request):
        participation_event = request.data['event']
        try:
            event = Participation.objects.filter(event__id=participation_event)
            serializer = ParticipationSerializer(event, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Participation.DoesNotExist:
            return Response({'message': 'Data partisipasi tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
    
    def liga_participation(self, request):
        participation_liga = request.data['liga']
        try:
            event = Participation.objects.filter(event__liga=participation_liga) \
                                    .values('player__name') \
                                    .annotate(total_points=models.Sum('point_received')) \
                                    .order_by('-total_points')
            serializer = AggregatedParticipationSerializer(event, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Participation.DoesNotExist:
            return Response({'message': 'Data partisipasi tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
    
    #REGISTER
    def post(self, request):
        player = request.data['player']
        event = request.data['event']
        try:
            Participation.objects.get(player=player, event=event)
        except Participation.DoesNotExist:
            serializer = ParticipationSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save()
                except:
                    return Response({'message': 'Masih Error!'})
            return Response({'message': 'Data Partisipasi berhasil dibuat.'})
        
        return Response({'message': 'Data partisipasi sudah ada.'})
    
    #UPDATE
    def patch(self, request):
        try:
            for data in request.data:
                try:
                    request_body = data
                    participation_id = request_body['id']
                    player = Player.objects.get(id=request_body['player'])
                    event = Event.objects.get(id=request_body['event'])
                    point_received = request_body['point_received']

                    get_participation_obj = get_object_or_404(Participation, pk=participation_id)
                    get_participation_obj.player = player
                    get_participation_obj.event = event
                    get_participation_obj.point_received = point_received
                    get_participation_obj.save()
                except Participation.DoesNotExist:
                    return Response({'message': 'Data partisipasi tidak ada.'})
                
            return Response({
                "message" : "Data berhasil disunting!",
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                "message" : str(len(request.data)) + " Gak Bisa!",
            })

    #DELETE
    def delete(self, request):
        request_body = request.data
        participation_id = request_body['id']
        get_participation_obj = get_object_or_404(Participation, pk=participation_id)
        get_participation_obj.delete()
        return Response({
            "message" : str(get_participation_obj) + " is successfully edited!",
        }, status=status.HTTP_200_OK)