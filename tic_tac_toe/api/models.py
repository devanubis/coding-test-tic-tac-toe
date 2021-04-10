from django.db import models
import tictactoe as tictactoe_lib
import json
import uuid


class Game(models.Model):

    class Marker(models.TextChoices):
        X = 'X'
        O = 'O'

    class OpponentLevel(models.TextChoices):
        RANDOM = 'R', 'Random'
        BEST = 'B', 'Best'

    class BoardDecoder(json.JSONDecoder):
        def decode(self, s, _w=json.decoder.WHITESPACE.match):
            """
            Overrides default JSONDecoder to map a flat list to a tuple because
            that is the format tictactoe-py uses for it's boards, but JSON maps
            as a list because that's way more sensible.
            :param s:
            :param _w:
            :return:
            """
            obj = super().decode(s, _w)
            if isinstance(obj, list):
                obj = tuple(obj)
            return obj

    key = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    player = models.CharField(
        max_length=1,
        choices=Marker.choices,
        default=Marker.X,
    )

    opponent_level = models.CharField(
        max_length=1,
        choices=OpponentLevel.choices,
        default=OpponentLevel.BEST,
    )

    board = models.JSONField(
        default=tuple(tictactoe_lib.EMPTY_BOARD),
        decoder=BoardDecoder,
    )

    def default(self):
        return

    def get_board(self):
        return self.board

    def get_player(self):
        return self.player

    def get_opponent(self):
        return self.Marker.O if self.player == self.Marker.X else self.Marker.X

    def play(self, row, col):
        self.board, winner = tictactoe_lib.play(self.board, self.player, row, col)
        self.save()

    def opponent_play(self):
        if self.opponent_level == self.OpponentLevel.RANDOM:
            self.board, winner = tictactoe_lib.play_random_move(self.board, self.get_opponent())
        elif self.opponent_level == self.OpponentLevel.BEST:
            self.board, winner = tictactoe_lib.play_best_move(self.board, self.get_opponent())
        else:
            raise UnknownOpponentLevel
        self.save()

    def get_winner(self):
        return tictactoe_lib.board_winner(self.board)

    def is_board_valid(self):
        return tictactoe_lib.board_is_valid(self.board)

    def is_finished(self):
        return self.is_board_valid() and self.get_winner() is not None


class UnknownOpponentLevel(Exception):
    pass
