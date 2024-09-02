from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class EmailMessageConsumer(WebsocketConsumer):
    def connect(self):
        self.account_id = self.scope['url_route']['kwargs']['account_id']
        self.room_group_name = f'email_{self.account_id}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        pass

    def notify_new_message(self, message):
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        print('Отправляемое сообщение:', content)
        self.send_chat_message(content)

    def message_to_json(self, message):
        print(message)
        return {
            'uid': message.uid,
            'subject': message.subject,
            'sent_date': message.sent_date.strftime("%Y-%m-%d %H:%M:%S"),
            'received_date': message.received_date.strftime("%Y-%m-%d %H:%M:%S") if message.received_date else None,
            'message_text': message.message_text,
            'attachments': message.attachments,
        }

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    def chat_message(self, event):
        message = event['message']
        data = {
            'command': 'new_message',
            'message': message
        }
        try:
            self.send(text_data=json.dumps(data))
            print("Сообщение успешно отправлено на клиент:", data)
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")


class EmailCounterConsumer(WebsocketConsumer):
    def connect(self):
        self.account_id = self.scope['url_route']['kwargs']['account_id']
        self.room_group_name = f'account_{self.account_id}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        pass

    def notify_new_message(self, message):
        content = {
            'command': 'count_update',
            'message': self.message_to_json(message)
        }
        print('Отправляемое сообщение:', content)
        self.send_chat_message(content)

    def message_to_json(self, message):
        print(message)
        return {
            'id': message.id,
            'email': message.email,
            'provider': message.provider,
            'count': message.count,
        }

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "count", "message": message}
        )

    def count_message(self, event):
        message = event['message']
        data = {
            'command': 'count_update',
            'message': message
        }
        try:
            self.send(text_data=json.dumps(data))
            print("Сообщение успешно отправлено на клиент:", data)
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")