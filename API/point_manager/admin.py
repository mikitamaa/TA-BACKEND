from django.contrib import admin
from .models import CustomUser, Event, Liga, Player, Season, Participation

admin.site.register(CustomUser)
admin.site.register(Liga)
admin.site.register(Event)
admin.site.register(Player)
admin.site.register(Participation)
admin.site.register(Season)