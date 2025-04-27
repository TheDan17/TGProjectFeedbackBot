from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from modules.language import LangHelper
from modules.language import get_lang_string_by_user_id as get_string


def get_main_menu_keyboard(user_id) -> ReplyKeyboardMarkup:
    main_menu_keyboard_text = {
        'Create': get_string(user_id, LangHelper.Public.MainMenu.CreateFormKeyboardButton),
        'View': get_string(user_id, LangHelper.Public.MainMenu.ViewFormKeyboardButton),
        'Another': get_string(user_id, LangHelper.Public.MainMenu.ViewAnotherFormKeyboardButton),
        'Delete': get_string(user_id, LangHelper.Public.MainMenu.DeleteFormKeyboardButton),
        'Change': get_string(user_id, LangHelper.Common.ChangeLanguageKeyboardButton)
    }
    main_menu_keyboard_data = [
        [KeyboardButton(text=main_menu_keyboard_text['Create']),
         KeyboardButton(text=main_menu_keyboard_text['View'])
         ],

        [KeyboardButton(text=main_menu_keyboard_text['Another'])],

        [KeyboardButton(text=main_menu_keyboard_text['Delete']),
         KeyboardButton(text=main_menu_keyboard_text['Change'])
         ]
    ]
    main_menu_keyboard = ReplyKeyboardMarkup(keyboard=main_menu_keyboard_data,
                                             resize_keyboard=True)
    return main_menu_keyboard


def get_create_confirm_keyboard(user_id):
    create_confirm_keyboard_text = {
        'ConfirmButton': get_string(user_id, LangHelper.Public.CreateForm.CreateFormConfirmButton)
    }

    CreateConfirmKeyboardData = [
        [KeyboardButton(text=create_confirm_keyboard_text['ConfirmButton'])
         ],
    ]

    create_confirm_keyboard = ReplyKeyboardMarkup(keyboard=CreateConfirmKeyboardData,
                                                  resize_keyboard=True)
    return create_confirm_keyboard


def get_delete_confirm_keyboard(user_id):
    delete_confirm_keyboard_text = {
        'YesButton': get_string(user_id, LangHelper.Public.DeleteForm.YesDeleteKeyboardButton),
        'NoButton': get_string(user_id, LangHelper.Public.DeleteForm.NoDeleteKeyboardButton)
    }

    DeleteConfirmKeyboardData = [
        [KeyboardButton(text=delete_confirm_keyboard_text['YesButton']),
         KeyboardButton(text=delete_confirm_keyboard_text['NoButton'])
         ],
    ]
    delete_confirm_keyboard = ReplyKeyboardMarkup(keyboard=DeleteConfirmKeyboardData,
                                                  resize_keyboard=True)
    return delete_confirm_keyboard


def get_change_lang_keyboard(user_id):
    change_lang_keyboard_text = {
        'RussianButton': get_string(user_id, LangHelper.Common.LanguageType.RussianLangText),
        'EnglishButton': get_string(user_id, LangHelper.Common.LanguageType.EnglishLangText)
    }

    ChangeLangKeyboardDataPublic = [
        [KeyboardButton(text=change_lang_keyboard_text['RussianButton']),
         KeyboardButton(text=change_lang_keyboard_text['EnglishButton'])
         ],
    ]
    change_lang_keyboard = ReplyKeyboardMarkup(keyboard=ChangeLangKeyboardDataPublic,
                                               resize_keyboard=True)
    return change_lang_keyboard
