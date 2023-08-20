import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Board


class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        # print(self.scope)
        self.board_id = self.scope["url_route"]["kwargs"]["board_id"]
        self.board_group_name = f"board_{self.board_id}"
        await self.channel_layer.group_add(self.board_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.board_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text_data_json['type'] = 'board_actions'
        # Send action to room group
        await self.channel_layer.group_send(self.board_group_name, text_data_json)

        await self.save_canvas(text_data_json)

    async def board_actions(self, event):
        # Send action to WebSocket
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_canvas(self, data):
        board = Board.objects.filter(id=int(data['board_id'])).first()
        if board:
            board.boarddetails_set.create(user_id=board.user.id,
                                          coordinates=data['coordinates'],
                                          line_width=data['lineWidth'],
                                          color=data['color'],
                                          board_id=board.id)
