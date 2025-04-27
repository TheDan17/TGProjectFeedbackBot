import asyncio
import logging

from modules.database import DatabaseDriver
from modules import language
from modules.language import LangHelper, CommonHelper
from bot import BotDriver
from bot_handlers import BotHandler
# TODO which module?
def add_form_to_database(db_driver: DatabaseDriver, user_id: int, text: str, language_code: int):
    db_driver.upload_user_form(user_id, text, language_code)


# TODO which module???
def generate_form_from_database(db_driver: DatabaseDriver, user_id: int):
    pass


async def main(*args: str):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S')

    bot = BotDriver()
    handler = BotHandler(bot.bot_dispatcher)
    await bot.start()

    # TODO REFACTOR ?
    user_forms_database_filename = 'user_forms.db'
    db_driver = DatabaseDriver(user_forms_database_filename)

    if '--new' in args:
        db_driver.create_user_forms_database()  # TODO database is closed after recreating???

    # TESTING
    print(language.get_lang_string(LangHelper.Public.GreetingText, CommonHelper.Language.Russian))
    user_id = 15324981
    user_id2 = 356464
    add_form_to_database(db_driver, user_id2, 'NEW ANOTHER AMAZING TEXT', CommonHelper.Language.English)
    print(db_driver.get.get_user_form(user_id))


if __name__ == '__main__':
    asyncio.run(main())
