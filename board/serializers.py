import json

from rest_framework import serializers
from .models import Board, BoardDetails


class BoardSerializer(serializers.ModelSerializer):
    extra_data = serializers.CharField(required=False, allow_blank=True, write_only=True)
    name = serializers.CharField(default='Board')

    class Meta:
        model = Board
        fields = ['id', 'name', 'actions', 'user', 'collaborators', 'extra_data']
        read_only_fields = ['collaborators']

    def create(self, validated_data):
        board = Board.objects.create(name=validated_data['name'],
                                     actions=validated_data['actions'],
                                     user=validated_data['user'])
        if validated_data['extra_data'] != '':
            extra_data = json.loads(validated_data['extra_data'])
            BoardDetails.objects.create(coordinates=extra_data['coordinates'],
                                        line_width=extra_data['lineWidth'],
                                        color=extra_data['color'],
                                        board_id=board.id,
                                        user=validated_data['user'])
            board.save()
        return board


class CollaboratorSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True, write_only=True)
    collaborators = serializers.ListField(child=serializers.IntegerField(), required=True, write_only=True)
