import asyncio
import json
import re
from asyncio import sleep
from random import randint
from typing import List, Dict, Union

import pandas as pd
import requests
from pandas.tests.io.test_packers import nan
from socks import SOCKS5
from telethon import TelegramClient
from telethon.errors import ChatAdminRequiredError
from telethon.events import NewMessage
from telethon.tl.custom import Message
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation

from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import User, Channel
from requests.exceptions import ConnectionError

from config import APP_API_HASH, APP_API_ID, PHONE_NUMBER, SETTINGS_FILE, \
    PROXY_HOST, PROXY_PORT, PROXY_USERNAME, PROXY_PASS
from utils import init_logger

logger = init_logger()

try:
    response = requests.get('https://api.telegram.org')
    proxy = None
except ConnectionError as e:
    proxy = (SOCKS5, PROXY_HOST, PROXY_PORT, True, PROXY_USERNAME, PROXY_PASS)

client = TelegramClient(PHONE_NUMBER.strip('+'),
                        APP_API_ID,
                        APP_API_HASH,
                        proxy=proxy,
                        base_logger=logger)


def get_settings() -> Dict:
    with open(SETTINGS_FILE) as file:
        return json.load(file)


def log_message(message: Message):
    with open("messages.log", "a") as file:
        sender: User = message.sender
        if sender.username:
            sender_username = f"@{sender.username}"
        else:
            sender_username = ''
        sender_full_name = f"{sender.first_name}{' ' + sender.last_name if sender.last_name else ''} {sender_username}"
        file.write(f"{sender_full_name} {message.date} \n{message.text}\n\n")


async def check_chats():
    file_name = 'telegram_chats.xlsx'
    df = pd.read_excel(file_name)
    delay = 3
    for i, row in df.iterrows():
        chat_identificator = row['short']
        # print(type(row['short']))

        participants = await client.get_participants(chat_identificator)
        df.loc[i, 'members'] = participants.total
        print(chat_identificator, participants.total)
            # if row['link'].find('joinchat') != -1:
            #     chat_identificator = row['link']
            #     chat = await client.get_entity(chat_identificator)
            #     print(chat)

            # try:
            #     chat = await client.get_entity(chat_identificator)
            # except:
            #     print(row['link'], 'is disabled')
            #     df.loc[i, 'enable'] = False
        # try:
        #     chat = await client.get_entity(chat_identificator)
        #     # print(chat)
        # except ChatAdminRequiredError as e:
        #     # chat = await client.get_entity(chat_identificator)
        #     # print(chat)
        #     # channel = await client(JoinChannelRequest(chat.access_hash))
        #     # print('channel', channel)
        #     # dialog = await client.get_dialogs(chat_identificator)[0]
        #     # print(dialog)
        #     print(e)
        # except Exception as e:
        #     df.loc[i, 'enable'] = False
        #     await sleep(delay)
        #     continue
        #
        # writer = pd.ExcelWriter(file_name)
        # df.to_excel(writer, 'Sheet1', index=False)
        # writer.save()
        await sleep(delay)

        # if i > 14:
        #     break


async def main():
    await client.start()
    await check_chats()

    # await client.run_until_disconnected()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
