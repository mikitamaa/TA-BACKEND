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
    
    def event_participation(self, request, event_id):
        try:
            event = Participation.objects.filter(event__id=event_id)
            if not event.exists():
                return Response([], status=status.HTTP_404_NOT_FOUND)
            
            serializer = ParticipationSerializer(event, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
            # Check if participation already exists
            Participation.objects.get(player=player, event=event)
            return Response({'message': 'Data partisipasi sudah ada.'}, status=status.HTTP_400_BAD_REQUEST)
        except Participation.DoesNotExist:
            # Create new participation
            serializer = ParticipationSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    # Save the participation
                    serializer.save()
                    return Response({
                        'data': serializer.data,  # This will now include the full player object
                        'message': 'Data Partisipasi berhasil dibuat.'
                    })
                except Exception as e:
                    return Response({'message': 'Masih Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'data': serializer.data, 'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        
    #UPDATE
    def patch(self, request):
        updated_participations = []
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

                    updated_participations.append({
                    "id": get_participation_obj.id,
                    "player": {"id": player.id, "name": player.name},
                    "event": event.id,
                    "point_received": get_participation_obj.point_received
                })
                except Participation.DoesNotExist:
                    return Response({'message': 'Data partisipasi tidak ada.'})
                
            return Response({
                "message": "Data berhasil disunting!",
                "data": updated_participations,
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
        temp = get_participation_obj
        get_participation_obj.delete()
        return Response({
            "message" : str(temp) + " is successfully edited!",
        }, status=status.HTTP_200_OK)