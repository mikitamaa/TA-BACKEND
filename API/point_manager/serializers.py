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
    season = SeasonSerializer(read_only=True)
    liga = LigaSerializer(read_only=True)
    ranger_assigned = CustomUserSerializer(read_only=True)
    managed_by = CustomUserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'season', 'max_participant', 'base_point', 'managed_by', 'ranger_assigned', 'liga']

class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = '__all__'