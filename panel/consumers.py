from channels.generic.websocket import AsyncWebsocketConsumer
import json
from socks import SOCKS5

import requests
from telethon import TelegramClient
from requests.exceptions import ConnectionError

from config import APP_API_HASH, APP_API_ID, PHONE_NUMBER, SETTINGS_FILE, \
    PROXY_HOST, PROXY_PORT, PROXY_USERNAME, PROXY_PASS

try:
    response = requests.get('https://api.telegram.org')
    proxy = None
except ConnectionError as e:
    proxy = (SOCKS5, PROXY_HOST, PROXY_PORT, True, PROXY_USERNAME, PROXY_PASS)

clients = {}


class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('CONNECT')
        await self.accept()

    async def disconnect(self, close_code):
        print('DISCONNECT')
        await self.close()
        pass

    async def receive(self, text_data):
        print('RECEIVE')
        print(text_data)
        data = json.loads(text_data)

        if data['method'] == 'auth_account':
            phone = data['phone']
            clients[phone] = TelegramClient(phone.strip('+'),
                                            APP_API_ID,
                                            APP_API_HASH,
                                            proxy=proxy)





