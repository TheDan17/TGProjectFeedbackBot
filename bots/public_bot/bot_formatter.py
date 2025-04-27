from aiogram.utils.markdown import text, bold, italic

from modules.language import get_question_string, get_question_comment_string
from modules import language
from modules import database
from modules.language import LangHelper


formatted_questions = {
}


def generate_formatted_question(question_header, question_comment):
    formatted_question = text(
        bold(question_header), '\n',
        italic(question_comment), sep=''
    )
    return formatted_question


def generate_formatted_questions():
    global formatted_questions
    for lang_code in language.available_languages:
        questions_list = []
        for i in range(1, 7):  # from 1 to 6
            question_header = get_question_string(lang_code, i)
            question_comment = get_question_comment_string(lang_code, i)
            question = generate_formatted_question(question_header, question_comment)
            questions_list.append(question)
        formatted_questions[lang_code] = questions_list


def get_formatted_question(user_id: int, question_number: int) -> str:
    lang_code = database.UserManagement.get_user_lang_code(user_id)
    question_index = question_number - 1
    question_string = formatted_questions[lang_code][question_index]
    return question_string


def clear_reserved_characters(input_text: str):
    reserved_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    first_char, second_char = None, None
    copy_text = input_text
    reserved_chars_count = 0
    for index, i_char in enumerate(input_text):
        second_char = first_char
        first_char = i_char
        if second_char is not None:
            if (second_char != '\\' or (second_char not in reserved_chars)) and first_char in reserved_chars:
                slice_number = index + reserved_chars_count
                copy_text = copy_text[:slice_number] + '\\' + copy_text[slice_number:]
                reserved_chars_count += 1
    return copy_text


class CommandHelper:
    create = LangHelper.Public.MainMenu.CreateFormKeyboardButton
    delete = LangHelper.Public.MainMenu.DeleteFormKeyboardButton
    view = LangHelper.Public.MainMenu.ViewFormKeyboardButton
    view_by_id = LangHelper.Public.MainMenu.ViewAnotherFormKeyboardButton
    change_language = LangHelper.Public.MainMenu.ChangeLanguageKeyboardButton

    class Create:
        confirm = LangHelper.Public.CreateForm.CreateFormConfirmButton

    class Delete:
        yes = LangHelper.Public.DeleteForm.YesDeleteKeyboardButton
        no = LangHelper.Public.DeleteForm.NoDeleteKeyboardButton

    class Language:
        russian = LangHelper.Common.LanguageType.RussianLangText
        english = LangHelper.Common.LanguageType.EnglishLangText
