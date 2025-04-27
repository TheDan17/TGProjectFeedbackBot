import asyncio

import bot_formatter
from modules import common
from modules.language import LanguageInterface
from modules.database import DatabaseInterface
from modules.bot import BotDriver
from modules.mlogging import Logger
from notifier import BotNotifier


class Bot:
    bot_driver: BotDriver
    bot_notifier: BotNotifier

    bot_handler = None
    db_interface: DatabaseInterface
    logger: Logger

    def __init__(self, token: str):
        common.setup_main_folders()
        LanguageInterface.load_languages()
        bot_formatter.generate_formatted_questions()
        from bot_handlers import BotHandler

        self.bot_driver = BotDriver(token)
        self.db_interface = DatabaseInterface()
        self.bot_notifier = BotNotifier(self.db_interface, self.bot_driver)
        self.bot_handler = BotHandler(self.bot_driver.bot_dispatcher)
        self.logger = Logger()

    async def start(self):
        bot_task = asyncio.create_task(self.bot_driver.start())
        notifier_task = asyncio.create_task(self.bot_notifier.start_tracking())

        await bot_task
        await notifier_task


def main():
    token: str = input('Please enter the token of DIAMONDREQUEST_public bot: \n')
    bot = Bot(token)
    asyncio.run(bot.start())


if __name__ == '__main__':
    main()
