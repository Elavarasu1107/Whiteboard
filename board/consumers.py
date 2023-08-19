import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer


class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.board_id = self.scope["url_route"]["kwargs"]["board_id"]
        self.board_group_name = f"board_{self.board_id}"
        await self.channel_layer.group_add(self.board_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.board_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        # Send action to room group
        await self.channel_layer.group_send(
            self.board_group_name, {"type": "board_actions",
                                    "coordinates": text_data_json["coordinates"],
                                    'lineWidth': text_data_json['lineWidth'],
                                    'color': text_data_json['color'],
                                    'user': text_data_json['user']
                                    }
        )

    async def board_actions(self, event):
        # Send action to WebSocket
        await self.send(text_data=json.dumps({"coordinates": event["coordinates"],
                                              'lineWidth': event['lineWidth'],
                                              'color': event['color'],
                                              'user': event['user']
                                              }))


# class Consumer(AsyncJsonWebsocketConsumer):
#     async def connect(self):
#         self.board_id = self.scope["url_route"]["kwargs"]["board_id"]
#         self.board_group_name = f"board_{self.board_id}"
#         await self.channel_layer.group_add(self.board_group_name, self.channel_name)
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.board_group_name, self.channel_name)
