import logging

from aiogram import Router, Dispatcher, types
from aiogram.filters import StateFilter, Command
from aiogram.fsm.state import State, StatesGroup, any_state
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown
from aiogram import F

import bot_input
import bot_formatter
from modules import language
from modules import common
from modules.language import LangHelper
from modules.language import get_lang_string_by_user_id as get_lang_string
from modules.language import get_user_form
from modules.common import CommonHelper
from modules import exceptions
from modules import database
from bot_formatter import get_formatted_question
from modules.mlogging import LogMessages
from modules.language import get_lang_strings as get_strings
from bot_formatter import CommandHelper


def generate_user_tg_link(user_id):
    user_link = f'tg://openmessage?user_id={user_id}'
    return user_link


def generate_user_formatted_form(user_id: int, request_id: int):
    if database.UserManagement.user_exists(request_id):
        request_link = generate_user_tg_link(request_id)
        request_form = get_user_form(user_id, request_id)
        request_form = bot_formatter.clear_reserved_characters(request_form)
        logging.debug(request_form)

        title = get_lang_string(user_id, LangHelper.Common.ForPublicFormHeaderText)
        form = markdown.text(markdown.bold(title),
                             markdown.text(' \#'), markdown.link(str(request_id), request_link),
                             markdown.text('\n'),
                             markdown.text(request_form), sep='')
        return form
    else:
        return None


class States(StatesGroup):
    main_menu = State()
    deleting_form = State()
    creating_form = State()
    creating_form_question1 = State()
    creating_form_question2 = State()
    creating_form_question3 = State()
    creating_form_question4 = State()
    creating_form_question5 = State()
    creating_form_question6 = State()
    changing_language = State()
    viewing_by_id = State()


class BotHandler:
    bot_router: Router = Router()

    def __init__(self, external_dispatcher: Dispatcher):
        external_dispatcher.include_router(self.bot_router)

    # MAIN
    @bot_router.message(any_state, Command("start"))
    async def start(msg: types.Message, state: FSMContext):
        user_id = msg.from_user.id
        user_language = msg.from_user.language_code
        user_lang_code = common.get_lang_code(user_language)
        database.UserManagement.register_user(user_id)
        db_interface = database.DatabaseInterface()
        db_interface.db_users.set_user_language(user_id, user_lang_code)

        await state.set_state(States.main_menu)
        await msg.answer(text=get_lang_string(user_id, LangHelper.Public.Common.StartCommandText),
                         reply_markup=bot_input.get_main_menu_keyboard(user_id))

    @bot_router.message(any_state, Command("menu"))
    async def set_menu_state(msg: types.Message, state: FSMContext):
        await state.clear()
        await state.set_state(States.main_menu)

        user_id = msg.from_user.id
        await msg.answer(text=get_lang_string(user_id, LangHelper.Public.Common.ToMenuText),
                         reply_markup=bot_input.get_main_menu_keyboard(user_id))

    @bot_router.message(any_state, Command("cancel"))
    async def cancel_operations(msg: types.Message, state: FSMContext):
        current_state = await state.get_state()
        user_id = msg.from_user.id

        creating_form_states = [States.creating_form_question1, States.creating_form_question2,
                                States.creating_form_question3, States.creating_form_question4,
                                States.creating_form_question5, States.creating_form_question6]
        if current_state in creating_form_states:
            database.UserManagement.clear_user_form(user_id=user_id)
            msg_text = get_lang_string(user_id, LangHelper.Public.CreateForm.CancelCreateFormText)
            await msg.answer(msg_text)

        await BotHandler.set_menu_state(msg, state)

    # CREATE
    @staticmethod
    async def append_user_form(msg: types.Message, question_number: int):
        user_id = msg.from_user.id
        user_message = msg.text
        question = language.get_question_string_by_id(user_id, question_number)

        user_question_and_answer = question + '\n' + user_message
        database.UserManagement.append_user_form(user_id, user_question_and_answer)

    @staticmethod
    def get_formatted_question(msg: types.Message, question_number: int) -> str:
        question = get_formatted_question(msg.from_user.id, question_number)
        return question

    @bot_router.message(StateFilter(States.main_menu), Command("create"))
    @bot_router.message(StateFilter(States.main_menu), F.text.in_(get_strings(CommandHelper.create)))
    async def set_creating_status(msg: types.Message, state: FSMContext):
        user_id = msg.from_user.id
        await state.set_state(States.creating_form)
        await msg.answer(text=get_lang_string(user_id, LangHelper.Public.CreateForm.CreateFormGreetingText),
                         reply_markup=bot_input.get_create_confirm_keyboard(user_id))

    @bot_router.message(StateFilter(States.creating_form), Command("yes"))
    @bot_router.message(StateFilter(States.creating_form), F.text.in_(get_strings(CommandHelper.Create.confirm)))
    async def ask_question1(msg: types.Message, state: FSMContext):
        user_id = msg.from_user.id
        database.UserManagement.clear_user_form(user_id)
        await state.set_state(States.creating_form_question1)

        question_text = markdown.text(
            markdown.bold(get_lang_string(user_id, LangHelper.Public.CreateForm.QuestionOneText)),
            markdown.italic(get_lang_string(user_id, LangHelper.Public.CreateForm.QuestionOneCommentText))
        )
        await msg.answer(text=question_text, reply_markup=types.ReplyKeyboardRemove())

    @bot_router.message(StateFilter(States.creating_form_question1))
    async def operating_after_question1(msg: types.Message, state: FSMContext):
        await BotHandler.append_user_form(msg, question_number=1)

        question_text = BotHandler.get_formatted_question(msg, question_number=2)
        await msg.answer(question_text)
        await state.set_state(States.creating_form_question2)

    @bot_router.message(StateFilter(States.creating_form_question2))
    async def operating_after_question2(msg: types.Message, state: FSMContext):
        await BotHandler.append_user_form(msg, question_number=2)

        question_text = BotHandler.get_formatted_question(msg, question_number=3)
        await msg.answer(question_text)
        await state.set_state(States.creating_form_question3)

    @bot_router.message(StateFilter(States.creating_form_question3))
    async def operating_after_question3(msg: types.Message, state: FSMContext):
        await BotHandler.append_user_form(msg, question_number=3)

        question_text = BotHandler.get_formatted_question(msg, question_number=4)
        await msg.answer(question_text)
        await state.set_state(States.creating_form_question4)

    @bot_router.message(StateFilter(States.creating_form_question4))
    async def operating_after_question4(msg: types.Message, state: FSMContext):
        await BotHandler.append_user_form(msg, question_number=4)

        question_text = BotHandler.get_formatted_question(msg, question_number=5)
        await msg.answer(question_text)
        await state.set_state(States.creating_form_question5)

    @bot_router.message(StateFilter(States.creating_form_question5))
    async def operating_after_question5(msg: types.Message, state: FSMContext):
        await BotHandler.append_user_form(msg, question_number=5)

        question_text = BotHandler.get_formatted_question(msg, question_number=6)
        await msg.answer(question_text)
        await state.set_state(States.creating_form_question6)

    @bot_router.message(StateFilter(States.creating_form_question6))
    async def end_creating_form(msg: types.Message, state: FSMContext):
        await BotHandler.append_user_form(msg, question_number=6)

        final_text = get_lang_string(msg.from_user.id, LangHelper.Public.CreateForm.CompleteCreateFormText)
        await msg.answer(final_text)
        await BotHandler.set_menu_state(msg, state)

    # DELETE
    @bot_router.message(StateFilter(States.main_menu), Command("delete"))
    @bot_router.message(StateFilter(States.main_menu), F.text.in_(get_strings(CommandHelper.delete)))
    async def ask_delete(msg: types.Message, state: FSMContext):
        await state.set_state(States.deleting_form)
        user_id = msg.from_user.id
        await msg.answer(text=get_lang_string(user_id, LangHelper.Public.DeleteForm.DeleteWarningText),
                         reply_markup=bot_input.get_delete_confirm_keyboard(user_id))

    @bot_router.message(StateFilter(States.deleting_form), Command("yes"))
    @bot_router.message(StateFilter(States.deleting_form), F.text.in_(get_strings(CommandHelper.Delete.yes)))
    async def delete_form(msg: types.Message, state: FSMContext):
        user_id = msg.from_user.id
        database.UserManagement.clear_user_form(user_id)

        await msg.answer(text=get_lang_string(user_id, LangHelper.Public.DeleteForm.DeleteFormResultText))
        await BotHandler.set_menu_state(msg, state)

    @bot_router.message(StateFilter(States.deleting_form), Command("no"))
    @bot_router.message(StateFilter(States.deleting_form), F.text.in_(get_strings(CommandHelper.Delete.no)))
    async def cancel_delete(msg: types.Message, state: FSMContext):
        await BotHandler.cancel_operations(msg, state)

    # LANGUAGE
    @bot_router.message(StateFilter(States.main_menu), Command("language"))
    @bot_router.message(StateFilter(States.main_menu), F.text.in_(get_strings(CommandHelper.change_language)))
    async def show_change_language_keyboard(msg: types.Message, state):
        user_id = msg.from_user.id
        await state.set_state(States.changing_language)
        await msg.answer(text=get_lang_string(user_id, LangHelper.Common.ChangeLanguageText),
                         reply_markup=bot_input.get_change_lang_keyboard(user_id))

    @bot_router.message(StateFilter(States.changing_language), Command("russian"))
    @bot_router.message(StateFilter(States.changing_language), F.text.in_(get_strings(CommandHelper.Language.russian)))
    async def change_language_to_russian(msg: types.Message, state):
        user_id = msg.from_user.id
        db_interface = database.DatabaseInterface()
        db_interface.db_users.set_user_language(user_id, CommonHelper.Language.Russian)
        await BotHandler.set_menu_state(msg, state)

    @bot_router.message(StateFilter(States.changing_language), Command("english"))
    @bot_router.message(StateFilter(States.changing_language), F.text.in_(get_strings(CommandHelper.Language.english)))
    async def change_language_to_english(msg: types.Message, state):
        user_id = msg.from_user.id
        db_interface = database.DatabaseInterface()
        db_interface.db_users.set_user_language(user_id, CommonHelper.Language.English)
        await BotHandler.set_menu_state(msg, state)

    # VIEW BY ID
    @bot_router.message(StateFilter(States.main_menu), Command("view_by_id"))
    @bot_router.message(StateFilter(States.main_menu), F.text.in_(get_strings(CommandHelper.view_by_id)))
    async def set_view_by_id_state(msg: types.Message, state: FSMContext):
        await state.set_state(States.viewing_by_id)
        user_id = msg.from_user.id
        await msg.answer(get_lang_string(user_id, LangHelper.Common.EnterIdText),
                         reply_markup=types.ReplyKeyboardRemove())

    @bot_router.message(StateFilter(States.viewing_by_id))
    async def show_form_by_id(msg: types.Message, state: FSMContext):
        user_id = msg.from_user.id

        id_str = msg.text
        try:
            request_id = int(id_str)
        except ValueError:
            error = get_lang_string(user_id, LangHelper.Common.WrongIdInputText)
            await msg.answer(error)
        else:
            answer_form = generate_user_formatted_form(user_id, request_id)
            if answer_form is not None:
                await msg.answer(answer_form)
                await BotHandler.set_menu_state(msg, state)
            else:
                LogMessages.send_warning_info(exceptions.WrongIdException(user_id))
                error = get_lang_string(user_id, LangHelper.Common.NotEnoughUserText)
                await msg.answer(error)

    # OTHER
    @bot_router.message(StateFilter(States.main_menu), Command("view"))
    @bot_router.message(StateFilter(States.main_menu), F.text.in_(get_strings(CommandHelper.view)))
    async def show_user_form(msg: types.Message):
        user_id = msg.from_user.id
        request_id = user_id

        view_text = generate_user_formatted_form(user_id, request_id)
        await msg.answer(text=view_text)

    @bot_router.message(StateFilter(States.main_menu), Command("id"))
    async def id(msg: types.Message):
        user_id = msg.from_user.id
        text = get_lang_string(user_id, LangHelper.Common.YourIdText)
        await msg.answer(text=f'{text}: {msg.from_user.id}')

    @bot_router.message(StateFilter(States.main_menu), Command("help"))
    async def show_help(msg: types.Message):
        pass

    @bot_router.message(StateFilter(States.main_menu), Command("delete_account"))
    async def delete_user_from_database(msg: types.Message):
        user_id = msg.from_user.id
        goodbye_text = get_lang_string(user_id, LangHelper.Public.GoodByeText)
        await msg.answer(goodbye_text, reply_markup=types.ReplyKeyboardRemove())
        database.UserManagement.delete_user_from_databases(user_id)
