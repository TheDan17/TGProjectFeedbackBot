from aiogram import Dispatcher, Bot
from aiogram.exceptions import TelegramNetworkError, TelegramUnauthorizedError
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.enums.parse_mode import ParseMode

from modules import mlogging as log


class BotDriver:
    bot_session: Bot
    bot_dispatcher: Dispatcher
    redis_storage: RedisStorage

    def __init__(self, bot_token: str):
        self.bot_session = Bot(bot_token, parse_mode=ParseMode('MarkdownV2'))
        self.redis_storage = RedisStorage.from_url('redis://localhost:6379/0')
        self.bot_dispatcher = Dispatcher(storage=self.redis_storage)

    async def start(self):
        try:
            await self.bot_session.delete_webhook(drop_pending_updates=True)
            await self.bot_dispatcher.start_polling(self.bot_session)
        except TelegramNetworkError:
            log.LogMessages.throw_critical_error('Not enough Internet connection!')
            exit(-1)
        except TelegramUnauthorizedError:
            log.LogMessages.throw_critical_error('Bot token is invalid!')
            exit(-1)
