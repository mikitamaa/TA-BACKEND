from .views import RegisterUser, LoginUser, UserHandler, LigaHandler, PlayerHandler, SeasonHandler, ParticipationHandler, EventHandler
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
    path('participation', ParticipationHandler.as_view()),
    path('event', EventHandler.as_view()),
]