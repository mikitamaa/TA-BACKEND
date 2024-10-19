# views.py
from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CustomUserSerializer, LigaSerializer, PlayerSerializer, SeasonSerializer, ParticipationSerializer, EventSerializer
from .models import CustomUser, Liga, Player, Season, Participation, Event
from .permissions import IsAdminUser, IsRangerUser

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
                'is_admin': user.is_admin,
                'is_ranger': user.is_ranger
            }
        return Response(response_data, status=status.HTTP_200_OK)


class UserHandler(APIView):
    #GET
    def get(self, request, id=None):
        # then check the token's validity
        user = request.data
        if user['is_admin'] == False:
            return Response({'detail' : 'Your credential token is either invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if id is not None:
            try:
                user = CustomUser.objects.get(id=id)
                serializer = CustomUserSerializer(user)
                return Response({"data" : serializer.data}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({'message': 'User tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
        
        user = CustomUser.objects.all()
        serializer = CustomUserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

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

class PlayerHandler(APIView):
    #get
    def get(self, request, id=None):
        if id is not None:
            try:
                player = Player.objects.get(id=id)
                serializer = PlayerSerializer(player)
                return Response({"data" : serializer.data}, status=status.HTTP_200_OK)
            except Player.DoesNotExist:
                return Response({'message': 'Palyer tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
        
        player = Player.objects.all()
        serializer = PlayerSerializer(player, many=True)
        return Response(serializer.data)
    
    #register
    def post(self, request):
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response()
    
    #update
    def patch(self, request):
        request_body = request.data
        player_id = request_body['id']
        name = request_body['name']
        get_player_obj = get_object_or_404(Player, pk=player_id)
        get_player_obj.name = name
        get_player_obj.save()
        return Response({
            "message" : str(get_player_obj) + " is successfully edited!",
        }, status=status.HTTP_200_OK)

    #delete
    def delete(self, request):
        request_body = request.data
        player_id = request_body['id']
        get_player_obj = get_object_or_404(Player, pk=player_id)
        get_player_obj.delete()
        return Response({
            "message" : str(get_player_obj) + " is successfully edited!",
        }, status=status.HTTP_200_OK)
    
class SeasonHandler(APIView):
    #GET
    def get(self, request, id=None):
        if id is not None:
            try:
                season = Player.objects.get(id=id)
                serializer = SeasonSerializer(season)
                return Response({"data" : serializer.data}, status=status.HTTP_200_OK)
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
    
class EventHandler(APIView):
    #GET
    def get(self, request):
        if 'id' in request.data:
            event_id = request.data['id']
            try:
                event = Event.objects.get(id=event_id)
                serializer = EventSerializer(event)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Event.DoesNotExist:
                return Response({'message': 'Event tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
        
        if 'season' in request.data:
            event_season = request.data['season']['id']
            try:
                event = Event.objects.filter(season__id=event_season)
                serializer = EventSerializer(event, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Event.DoesNotExist:
                return Response({'message': 'Event tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
            
        if 'liga' in request.data:
            event_liga = request.data['liga']['id']
            try:
                event = Event.objects.filter(liga__id=event_liga)
                serializer = EventSerializer(event, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Event.DoesNotExist:
                return Response({'message': 'Event tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
            
        if 'ranger_assigned' in request.data:
            ranger_assigned = request.data['ranger_assigned']['id']
            try:
                ranger = Event.objects.filter(ranger_assigned__id=ranger_assigned)
                serializer = EventSerializer(ranger, many=True)
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

class ParticipationHandler(APIView):
    #GET
    def get(self, request):
        if 'id' in request.data:
            participation_id = request.data['id']
            try:
                participation = Participation.objects.get(id=participation_id)
                serializer = ParticipationSerializer(participation)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Participation.DoesNotExist:
                return Response({'message': 'Data partisipasi tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
        
            
        if 'event' in request.data:
            participation_event = request.data['event']
            try:
                event = Participation.objects.filter(event__id=participation_event)
                serializer = ParticipationSerializer(event, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Participation.DoesNotExist:
                return Response({'message': 'Data partisipasi tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
    

        event = Participation.objects.all()
        serializer = ParticipationSerializer(event, many=True)
        return Response(serializer.data)
    
    #REGISTER
    def post(self, request):
        serializer = ParticipationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except:
                return Response({'message': 'Masih Error!'})
        return Response({'message': 'Data Partisipasi berhasil dibuat.'})
    
    #UPDATE
    def patch(self, request):
        try:
            for data in request.data:
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
            return Response({
                "message" : str(get_participation_obj) + " is successfully edited!",
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