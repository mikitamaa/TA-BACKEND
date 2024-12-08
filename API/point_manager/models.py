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

    def __str__(self):
        return self.name




# ENTITIES
class Liga(models.Model):
    name = models.CharField(max_length=35, unique=True)
    description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = name = models.CharField(max_length=35, unique=True)

    def __str__(self):
        return self.name

    
class Season(models.Model):
    name = models.CharField(max_length=35, unique=True)
    description = models.CharField(max_length=255, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    STATUS_PENDING = 'P'
    STATUS_COMPLETED = 'C'
    STATUS_ONGOING = 'O'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_ONGOING, 'On Going'),
    ]

    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    max_participant = models.IntegerField()
    base_point = models.IntegerField()
    ranger_assigned = models.ForeignKey(CustomUser, related_name='ranger', on_delete=models.CASCADE)
    managed_by = models.ForeignKey(CustomUser, related_name='admin', on_delete=models.CASCADE)
    liga = models.ForeignKey(Liga, related_name='liga', on_delete=models.CASCADE)
    period = models.DateField(null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_PENDING)

    def __str__(self):
        return self.name


class Participation(models.Model):
    player =  models.ForeignKey(Player, on_delete=models.CASCADE)
    event =  models.ForeignKey(Event, on_delete=models.CASCADE)
    point_received = models.IntegerField(default=0)

    def __str__(self):
        return str(f"{self.player} - {self.event}")
