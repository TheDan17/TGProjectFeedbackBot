from aiogram import Router, Dispatcher
from aiogram import types, filters
from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    deleting_form = State()
    creating_form = State()
    creating_form_question1 = State()
    creating_form_question2 = State()
    creating_form_question3 = State()
    creating_form_question4 = State()
    creating_form_question5 = State()
    creating_form_question6 = State()


class BotHandler:
    bot_router: Router = Router()

    def __init__(self, external_dispatcher: Dispatcher):
        external_dispatcher.include_router(self.bot_router)

    @bot_router.message(filters.Command("start"))
    async def start(msg: types.Message):
        await msg.answer("")
