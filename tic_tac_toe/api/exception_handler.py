from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response
from .models import Game, UnknownOpponentLevel
from tictactoe import IllegalBoard, IllegalMove


def custom_exception_handler(exc, context):
    if isinstance(exc, IllegalMove):
        return Response(
            {"error": "Illegal move, please try again"},
            status=status.HTTP_400_BAD_REQUEST
        )
    if isinstance(exc, IllegalBoard):
        return Response(
            {"error": "Game board is in an illegal state, please start a new game"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    if isinstance(exc, UnknownOpponentLevel):
        return Response(
            {"error": "Illegal opponent level, please use either 'X' or 'O'"},
            status.HTTP_404_NOT_FOUND
        )
    if isinstance(exec, Game.DoesNotExist):
        return Response(
            {"error": "Game not found with that key, please check and try again"},
            status=status.HTTP_404_NOT_FOUND
        )
    return exception_handler(exc, context)
