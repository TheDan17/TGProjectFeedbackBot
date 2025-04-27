import asyncio
import logging
from aiogram.exceptions import TelegramNetworkError

from aiogram import Dispatcher, Bot, Router


class BotDriver:
    token = "6541356637:AAGuQTEI1W8LyTmpQrfh0C2bESaP8-G4A7E"
    bot_session: Bot
    bot_dispatcher: Dispatcher

    def __init__(self):
        self.bot_session = Bot(self.token)
        self.bot_dispatcher = Dispatcher()

    async def start(self):
        try:
            await self.bot_session.delete_webhook(drop_pending_updates=True)
        except TelegramNetworkError:
            print('TelegramNetworkError: Cannot connect to host! Check Internet connection!')
            exit(-1)
        await self.bot_dispatcher.start_polling(self.bot_session)
