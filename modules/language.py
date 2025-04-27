import ast

from modules import common
from modules.common import CommonHelper
from modules.database import DatabaseInterface
from modules.mlogging import LogMessages


available_languages = [CommonHelper.Language.Russian, CommonHelper.Language.English]
available_languages_data = {}
'''
available_language_data = {
    0: {LangString: "LangString"},
    1: ...
}
'''


def get_lang_string_by_user_id(user_id: int, string_name: str):
    return LanguageInterface.get_lang_string_for_user(string_name, user_id=user_id)


def get_lang_string_by_lang_code(language_code: int, string_name: str):
    return LanguageInterface.get_lang_string_for_user(string_name, language_code=language_code)


def get_lang_strings(string_name: str):
    return LanguageInterface.get_lang_strings(string_name)


class LanguageInterface:
    @staticmethod
    def get_lang_file_from_code(language_code: int):
        if language_code == CommonHelper.Language.Russian:
            return LangHelper.LangFiles.RuLanguage
        if language_code == CommonHelper.Language.English:
            return LangHelper.LangFiles.EnLanguage

    @staticmethod
    def extract_language_data(lang_filename):
        file_path = common.get_lang_file(lang_filename)
        with open(file_path, encoding='utf-8', mode='r') as file:
            data = file.read()

        return ast.literal_eval(data)

    @staticmethod
    def load_languages():
        global available_languages, available_languages_data
        for language_code in available_languages:
            lang_file = LanguageInterface.get_lang_file_from_code(language_code)
            available_languages_data[language_code] = LanguageInterface.extract_language_data(lang_file)

    @staticmethod
    def get_lang_string_for_user(string_name: str, user_id: int = None, language_code: int = None):
        if user_id is not None:
            db_interface = DatabaseInterface()
            user_language_code = db_interface.db_users.get_user_language(user_id)
            if user_language_code is None:
                return '?'
        elif language_code is not None:
            user_language_code = language_code
        else:
            return '?'

        global available_languages_data
        try:
            return available_languages_data[user_language_code][string_name]
        except KeyError as error:
            LogMessages.throw_error(error)
            return 'not found'

    @staticmethod
    def get_lang_strings(string_name):
        strings = []
        for lang_code in available_languages:
            lang_string = LanguageInterface.get_lang_string_for_user(string_name, language_code=lang_code)
            strings.append(lang_string)
        return strings


def get_question_string_by_id(user_id: int, question_number: int):
    db_interface = DatabaseInterface()
    lang_code = db_interface.db_users.get_user_language(user_id)
    question_string = get_question_string(lang_code, question_number)
    return question_string


def get_question_comment_string_by_id(user_id: int, question_number: int):
    db_interface = DatabaseInterface()
    lang_code = db_interface.db_users.get_user_language(user_id)
    question_string = get_question_comment_string(lang_code, question_number)
    return question_string


def get_question_string(language_code: int, question_number: int):
    question_string = ''

    if question_number == 1:
        question_string = get_lang_string_by_lang_code(language_code, LangHelper.Public.CreateForm.QuestionOneText)
    elif question_number == 2:
        question_string = get_lang_string_by_lang_code(language_code, LangHelper.Public.CreateForm.QuestionTwoText)
    elif question_number == 3:
        question_string = get_lang_string_by_lang_code(language_code, LangHelper.Public.CreateForm.QuestionThreeText)
    elif question_number == 4:
        question_string = get_lang_string_by_lang_code(language_code, LangHelper.Public.CreateForm.QuestionFourText)
    elif question_number == 5:
        question_string = get_lang_string_by_lang_code(language_code, LangHelper.Public.CreateForm.QuestionFiveText)
    elif question_number == 6:
        question_string = get_lang_string_by_lang_code(language_code, LangHelper.Public.CreateForm.QuestionSixText)

    return question_string


def get_question_comment_string(language_code: int, question_number: int):
    question_string = ''

    if question_number == 1:
        question_string = get_lang_string_by_lang_code(language_code, LangHelper.Public.CreateForm.QuestionOneCommentText)
    elif question_number == 2:
        question_string = get_lang_string_by_lang_code(language_code, LangHelper.Public.CreateForm.QuestionTwoVariantsText)
    elif question_number == 3:
        question_string = get_lang_string_by_lang_code(language_code, LangHelper.Public.CreateForm.QuestionThreeVariantsText)
    elif question_number == 6:
        question_string = get_lang_string_by_lang_code(language_code, LangHelper.Public.CreateForm.QuestionSixCommentText)

    return question_string


def get_viewed_lang_by_code(viewed_code):
    viewed_lang = None

    if viewed_code == CommonHelper.Viewed.NotViewed:
        viewed_lang = LangHelper.Common.ViewedType.NotViewedText
    elif viewed_code == CommonHelper.Viewed.Rejected:
        viewed_lang = LangHelper.Common.ViewedType.RejectedText
    elif viewed_code == CommonHelper.Viewed.Accepted:
        viewed_lang = LangHelper.Common.ViewedType.AcceptedText

    return viewed_lang


def get_lang_lang_by_code(language_code):
    language_lang = None

    if language_code == CommonHelper.Language.Russian:
        language_lang = LangHelper.Common.LanguageType.RussianLangText
    elif language_code == CommonHelper.Language.English:
        language_lang = LangHelper.Common.LanguageType.EnglishLangText

    return language_lang


# TODO refactor?
def get_user_form(user_id: int, request_id: int):
    # TODO refactor ? (external function)
    db_interface = DatabaseInterface()
    language_code = db_interface.db_users.get_user_language(request_id)
    viewed_code = db_interface.db_forms.get_user_viewed(request_id)
    form_database = db_interface.db_forms.get_user_form(request_id)

    if form_database == '':
        form_string = get_lang_string_by_user_id(request_id, LangHelper.Common.NotEnoughFormText)
    else:
        form_string = form_database

    viewed_string = get_lang_string_by_user_id(user_id,
                                               LangHelper.Common.ViewedHeaderText)
    viewed_lang = get_viewed_lang_by_code(viewed_code)
    viewed_string_value = get_lang_string_by_user_id(user_id, viewed_lang)

    language_string = get_lang_string_by_user_id(user_id,
                                                 LangHelper.Common.LanguageHeaderText)
    language_lang = get_lang_lang_by_code(language_code)
    language_string_value = get_lang_string_by_user_id(user_id, language_lang)

    # TODO refactor ?
    form = f"""  {language_string}: {language_string_value}
  {viewed_string}: {viewed_string_value}
  {form_string}"""

    return form


class LangHelper:

    class LangFiles:
        RuLanguage = 'ru.lang'
        EnLanguage = 'en.lang'

    class Admin:
        GreetingText = "GreetingTextAdmin"
        GreetingButton = "GreetingButtonAdmin"
        MainMenuChangeLanguage = "MainMenuChangeLanguageAdmin"

    class Public:
        class Common:
            StartCommandText = "StartCommandPublic"
            ToMenuText = "ToMenu"
            NotEnoughCommandText = "NotEnoughCommand"

        class MainMenu:
            CreateFormKeyboardButton = "CreateFormKeyboardButton"
            ViewFormKeyboardButton = "ViewFormKeyboardButton"
            ViewAnotherFormKeyboardButton = "ViewAnotherFormKeyboardButton"
            DeleteFormKeyboardButton = "DeleteFormKeyboardButton"
            ChangeLanguageKeyboardButton = "ChangeLanguageKeyboardButton"

        class CreateForm:
            CreateFormKeyboardButton = "CreateFormKeyboardButton"
            CreateFormGreetingText = "CreateFormGreeting"
            CreateFormConfirmButton = "CreateFormConfirmButton"

            QuestionOneText = "QuestionOneText"
            QuestionTwoText = "QuestionTwoText"
            QuestionThreeText = "QuestionThreeText"
            QuestionFourText = "QuestionFourText"
            QuestionFiveText = "QuestionFiveText"
            QuestionSixText = "QuestionSixText"

            QuestionOneCommentText = "QuestionOneCommentText"
            QuestionTwoVariantsText = "QuestionTwoVariantsText"
            QuestionThreeVariantsText = "QuestionThreeVariantsText"
            QuestionSixCommentText = "QuestionSixCommentText"

            CompleteCreateFormText = "CompleteCreateFormText"
            CancelCreateFormText = "CancelCreateFormText"

        GoodByeText = "GoodByeText"

        class DeleteForm:
            DeleteFormKeyboardButton = "DeleteFormKeyboardButton"
            DeleteWarningText = "DeleteWarning"
            NotFormToDeleteText = "NotFormToDelete"
            DeleteFormResultText = "DeleteFormResultText"

            YesDeleteKeyboardButton = "YesDeleteKeyboardButton"
            NoDeleteKeyboardButton = "NoDeleteKeyboardButton"

    class Common:
        ForPublicFormHeaderText = "ForPublicFormHeaderText"

        NotEnoughFormText = "NotEnoughFormText"
        NotEnoughUserText = "NotEnoughUserText"
        EnterIdText = "EnterIdText"
        WrongIdInputText = "WrongIdInputText"

        LanguageHeaderText = "LanguageHeaderText"

        class LanguageType:
            RussianLangText = "RussianLangText"
            EnglishLangText = "EnglishLangText"

        ViewedHeaderText = "ViewedHeaderText"

        class ViewedType:
            NotViewedText = "NotViewedText"
            RejectedText = "RejectedText"
            AcceptedText = "AcceptedText"

        ChangeLanguageText = "ChangeLanguageText"
        ChangeLanguageKeyboardButton = "ChangeLanguageKeyboardButton"

        YourIdText = "YourIdText"

    class Notifier:
        AcceptedFormText = "AcceptedFormText"
        RejectedFormText = "RejectedFormText"
