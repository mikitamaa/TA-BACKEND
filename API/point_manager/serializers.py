# serializers.py
from rest_framework import serializers
from .models import CustomUser, Liga, Player, Season, Participation, Event
from django.contrib.auth.password_validation import validate_password

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'password', 'is_admin', 'is_ranger']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        # Hash Password
        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance
    
class LigaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liga
        fields = '__all__'

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def to_representation(self, instance):
        # Get the original serialized data
        data = super().to_representation(instance)

        liga_data = LigaSerializer(instance.liga).data
        season_data = SeasonSerializer(instance.season).data
        ranger_data = CustomUserSerializer(instance.ranger_assigned).data
        admin_data = CustomUserSerializer(instance.managed_by).data

        data['liga'] = liga_data  
        data['season'] = season_data 
        data['ranger_assigned'] = ranger_data
        data['managed_by'] = admin_data

        return data
        

class ParticipationSerializer(serializers.ModelSerializer):
    player = serializers.PrimaryKeyRelatedField(queryset=Player.objects.all())  # Accept only player id

    class Meta:
        model = Participation
        fields = '__all__'

    def to_representation(self, instance):
        # Get the original serialized data (including player id)
        data = super().to_representation(instance)

        # Serialize the player to include its full object (id + name)
        player_data = PlayerSerializer(instance.player).data
        data['player'] = player_data  # Replace player ID with the full player object

        return data
    

class AggregatedParticipationSerializer(serializers.Serializer):
    id = serializers.CharField(source='player__id')
    name = serializers.CharField(source='player__name')
    total_points = serializers.IntegerField()