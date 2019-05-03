import asyncio
import json
from typing import List, Dict

from socks import SOCKS5
from telethon import TelegramClient
from telethon.events import NewMessage
from telethon.tl.custom import Message

from config import APP_API_HASH, APP_API_ID, PHONE_NUMBER, SETTINGS_FILE
from utils import init_logger

logger = init_logger()


# proxy = None
proxy = (SOCKS5, '51.144.86.230', 18001, True, 'usrTELE', 'avt231407')
client = TelegramClient(PHONE_NUMBER.strip('+'),
                        APP_API_ID,
                        APP_API_HASH,
                        proxy=proxy,
                        base_logger=logger)


def get_settings() -> Dict:
    with open(SETTINGS_FILE) as file:
        return json.load(file)


def is_word_matching(message: Message, words: List[str]) -> bool:
    
    return False


def is_regexp_matching(message: Message, regexps: str) -> bool:

    return False


def is_sender_matching(message: Message, users: str) -> bool:

    return False


def check_message(message: Message) -> bool:
    settings = get_settings()
    text = message.text
    for filter_type, filter_items in settings['FILTERS'].items():
        if filter_type == 'WORDS':
            if is_word_matching(text, filter_items):
                return True
        if filter_type == 'REGEXP':
            if is_regexp_matching(message, filter_items):
                return True
        if filter_type == 'USERS':
            if is_sender_matching(message, filter_items):
                return True

    return False


def get_receivers() -> List:
    pass


async def send_out_message(message: Message) -> None:
    receivers = get_receivers()


@client.on(NewMessage)
async def new_message_handler(event: NewMessage.Event):
    message = event.message
    print(message)
    if check_message(message):
        await send_out_message(message)


async def main():
    await client.start()
    await client.run_until_disconnected()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
