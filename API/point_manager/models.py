from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(max_length=25)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    is_ranger = models.BooleanField(default=True)

    username=None
    first_name=None
    last_name=None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [username]



# ENTITIES
class Liga(models.Model):
    name = models.CharField(max_length=35, unique=True)

class Player(models.Model):
    name = name = models.CharField(max_length=35, unique=True)
    
class Season(models.Model):
    name = models.CharField(max_length=35, unique=True)

class Event(models.Model):
    name = name = models.CharField(max_length=255, unique=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    max_participant = models.IntegerField()
    base_point = models.IntegerField()
    ranger_assigned = models.ForeignKey(CustomUser, related_name='ranger', on_delete=models.CASCADE)
    managed_by = models.ForeignKey(CustomUser, related_name='admin', on_delete=models.CASCADE)
    liga = models.ForeignKey(Liga, related_name='liga', on_delete=models.CASCADE)

class Participation(models.Model):
    player =  models.ForeignKey(Player, on_delete=models.CASCADE)
    event =  models.ForeignKey(Event, on_delete=models.CASCADE)
    point_received = models.IntegerField(default=0)