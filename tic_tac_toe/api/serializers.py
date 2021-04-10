from rest_framework import serializers
from .models import Game


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('key', 'player', 'opponent_level', 'board')

    player = serializers.ChoiceField(
        choices=Game.Marker.choices,
        default=Game.Marker.X,
    )
    opponent_level = serializers.ChoiceField(
        choices=Game.OpponentLevel.choices,
        default=Game.OpponentLevel.BEST,
    )


class MoveSerializer(serializers.Serializer):

    row = serializers.IntegerField(
        min_value=1,
        max_value=3,
        required=True
    )
    col = serializers.IntegerField(
        min_value=1,
        max_value=3,
        required=True
    )

    def create(self, validated_data):
        return {
            'row': validated_data.row,
            'col': validated_data.col,
        }

    def update(self, instance, validated_data):
        """
        No-op required abstract method
        """
        return instance
