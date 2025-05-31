from django.urls import path
from gomoku.views import InitGame, AIMove, PlayerMove, Settings

urlpatterns = [
    path("init", InitGame.as_view()),
    path("player_move", PlayerMove.as_view()),
    path("ai_move", AIMove.as_view()),
    path("settings", Settings.as_view()),
]
