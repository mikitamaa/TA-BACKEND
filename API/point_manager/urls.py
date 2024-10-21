from .views.auth_views import *
from .views.event_views import *
from .views.liga_views import *
from .views.participation_views import *
from .views.player_views import *
from .views.season_view import *
from .views.user_views import *

from django.urls import path

urlpatterns = [
    path('register', RegisterUser.as_view()),
    path('login', LoginUser.as_view()),
    path('user', UserHandler.as_view()),
    path('user/<int:id>/', UserHandler.as_view()),
    path('liga', LigaHandler.as_view()),
    path('liga/<int:id>/', LigaHandler.as_view()),
    path('player', PlayerHandler.as_view()),
    path('season', SeasonHandler.as_view()),
    path('event', EventHandler.as_view()),
    path('participation', ParticipationHandler.as_view({'get': 'all_participation'})),
    path('participation/event', ParticipationHandler.as_view({'get': 'event_participation'})),
    path('participation/liga', ParticipationHandler.as_view({'get': 'liga_participation'})),
    path('participation/register', ParticipationHandler.as_view({'post': 'post'})),
    path('participation/edit', ParticipationHandler.as_view({'patch': 'patch'})),
    path('participation/edit', ParticipationHandler.as_view({'delete': 'delete'})),
]