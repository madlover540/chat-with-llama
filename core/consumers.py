import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from core.tasks import send_email_task

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'chat'
        # todo change it to kwargs from url
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()



    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message', # the function
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']
        email = 'abdullah@gmail.com'
        send_email_task.delay(email, message)
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))


