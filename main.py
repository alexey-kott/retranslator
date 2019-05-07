import asyncio
import json
import re
from asyncio import sleep
from typing import List, Dict, Union

import pandas as pd
import requests
from socks import SOCKS5
from telethon import TelegramClient
from telethon.events import NewMessage
from telethon.tl.custom import Message
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
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


def get_lemmatized_tokens(text: str) -> List[str]:
    mystem = Mystem()
    russian_stopwords = stopwords.words("russian")

    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if
              token not in russian_stopwords and token != " " and token.strip() not in punctuation]

    return tokens


def is_word_matching(text: str, words: List[str]) -> bool:
    lemmatized_tokens = get_lemmatized_tokens(text)
    if set(lemmatized_tokens).intersection(set(words)):
        return True

    return False


def is_regexp_matching(text: str, regexps: str) -> bool:
    for regexp in regexps:
        if re.findall(regexp, text):
            return True

    return False


def is_sender_matching(message: Message, users: str) -> bool:
    for user in users:
        if user.startswith('@'):
            sender_username = message.sender.username.lower()
            if f"@{sender_username}" == user:
                return True
        else:
            sender: User = message.sender
            sender_name = f"{sender.first_name}{' ' + sender.last_name if sender.last_name else ''}"
            if sender_name == user:
                return True

    return False


def check_message(message: Message) -> bool:
    settings = get_settings()
    text = message.text
    for filter_type, filter_items in settings['FILTERS'].items():
        if filter_type == 'WORDS':
            if is_word_matching(text, filter_items):
                return True
        if filter_type == 'REGEXP':
            if is_regexp_matching(text, filter_items):
                return True
        if filter_type == 'USERS':
            if is_sender_matching(message, filter_items):
                return True

    return False


async def get_receivers() -> List[Union[User, Channel]]:
    receiver_entities = []
    settings = get_settings()
    receiver_usernames = settings['RECEIVERS']
    for receiver_username in receiver_usernames:
        entity = await client.get_entity(receiver_username)
        receiver_entities.append(entity)
        await sleep(1)

    return receiver_entities


async def send_out_message(message: Message) -> None:
    receivers = await get_receivers()

    for receiver in receivers:
        if receiver.username == message.sender.username:
            continue
        await client.forward_messages(receiver, message)
        await sleep(1)


@client.on(NewMessage)
async def new_message_handler(event: NewMessage.Event):
    message = event.message
    log_message(message)
    if check_message(message):
        await send_out_message(message)


async def check_chats():
    df = pd.read_excel('telegram_chats.xlsx')
    for i, row in df.iterrows():
        print(row['short'])
        await client.get_entity()


async def main():
    await client.start()
    await check_chats()

    # await client.run_until_disconnected()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
