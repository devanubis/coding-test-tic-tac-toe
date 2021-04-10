from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GameSerializer, MoveSerializer
from .models import Game
from tictactoe import IllegalBoard


class NewGame(APIView):

    def post(self, request):
        """
        Start a new game
        :param request:
        :return: Response
        """
        serializer = GameSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        game = serializer.save()

        return Response(
            {'key': game.key},
            status=status.HTTP_201_CREATED
        )


class PlayGame(APIView):

    def load_game(self, key) -> Game:
        """
        Get a game's state
        :param key: UUID key for the game to load
        :return: Game The game object, or a response object if failed to load
        :raise: IllegalBoard if the loaded game is in an illegal state
        """
        game = Game.objects.get(key=key)
        if not game.is_board_valid():
            raise IllegalBoard
        return game

    def get(self, request, key):
        """
        Get a game's state
        :param request:
        :param key: UUID key for the game to load
        :return: Response
        """
        game = self.load_game(key)
        return GameResponse(game=game)

    def post(self, request, key):
        """
        POST a move to an existing game
        :param request:
        :param key: UUID key for the game to load
        :return: Response
        """
        game = self.load_game(key)
        if game.get_winner():
            return Response(
                {"error": "Game has already been won, no more moves allowed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        move_serializer = MoveSerializer(data=request.data)
        if not move_serializer.is_valid():
            return Response(move_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        game.play(
            # We serialize and validate the values as 1..3, but .play()
            # expects 0..2 so map that here
            row=move_serializer.data["row"] - 1,
            col=move_serializer.data["col"] - 1,
        )

        if not game.get_winner():
            game.opponent_play()

        return GameResponse(game=game)


class GameResponse(Response):

    def __init__(self, game=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if game is not None:
            self.set_game_data(game)

    def set_game_data(self, game):
        if not self.data:
            self.data = {}
        self.data.update(GameSerializer(game).data)

        winner = game.get_winner()
        if winner:
            self.data['winner'] = winner
