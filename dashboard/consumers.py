# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
import channels.layers
from asgiref.sync import async_to_sync


class DashboardConsumer(WebsocketConsumer):
	def connect(self):
		async_to_sync(self.channel_layer.group_add)("dashboard",self.channel_name)

		self.accept()

	def disconnect(self, close_code):
		async_to_sync(self.channel_layer.group_discard)(
            "dashboard",
            self.channel_name
        )
	    # Receive message from room group
	def dashboard_message(self, event):
		message = event['data']

		# Send message to WebSocket
		self.send(text_data=message)