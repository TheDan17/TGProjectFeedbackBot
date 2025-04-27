import logging
import asyncio

from modules import language
from modules.database import DatabaseInterface
from modules.bot import BotDriver
from modules.common import CommonHelper
from modules.mlogging import LogMessages


LOOP_TIME_SECONDS = 60


class BotNotifier:
    db_interface: DatabaseInterface
    bot_driver: BotDriver

    keep_tracking = True
    working = True

    def __init__(self, db_interface: DatabaseInterface, bot_driver: BotDriver):
        self.db_interface = db_interface
        self.bot_driver = bot_driver

    @staticmethod
    def _extract_user_data(user_data: tuple):
        user_id = user_data[0]
        past_viewed = user_data[1]
        present_viewed = user_data[2]
        notified = user_data[3]

        return user_id, past_viewed, present_viewed, notified

    @staticmethod
    def _check_need_to_be_notified(past_viewed_code, present_viewed_code, notified_code):
        if notified_code == CommonHelper.Notified.NotNotified:
            if past_viewed_code != present_viewed_code:
                return True
            else:
                return False
        else:
            return False

    def _send_notification(self, user_id: int, message_str: str):
        self.bot_driver.bot_session.send_message(chat_id=user_id, text=message_str)
        log_message = f'Notification "{message_str}" was send to #{str(user_id)} tg user'
        LogMessages.send_tracking_info('Notifier', log_message)

    def _iterate_users(self, registered_users: tuple):
        for user in registered_users:
            user_id, past_viewed, present_viewed, notified = self._extract_user_data(user)

            need_notified = self._check_need_to_be_notified(past_viewed, present_viewed, notified)

            if need_notified:
                string_name = None
                if present_viewed == CommonHelper.Viewed.Accepted:
                    string_name = language.LangHelper.Notifier.AcceptedFormText
                elif present_viewed == CommonHelper.Viewed.Rejected:
                    string_name = language.LangHelper.Notifier.RejectedFormText

                message_str = language.get_lang_string_by_user_id(user_id, string_name)
                self._send_notification(user_id, message_str)

    async def start_tracking(self):
        logging.info('Notifier tracking is started')
        self.working = True
        while self.keep_tracking is True:
            await asyncio.sleep(LOOP_TIME_SECONDS)

            all_users_with_data = self.db_interface.db_notify.get_all_notify_data()
            self._iterate_users(all_users_with_data)

        self.working = False

    async def stop_tracking(self):
        self.keep_tracking = False

        while self.working is not False:
            pass
        else:
            return True
