import re
import pathlib


root_path: pathlib.Path
db_path: pathlib.Path
lang_path: pathlib.Path
log_path: pathlib.Path


class CommonHelper:
    class Language:
        Russian = 0
        English = 1

    class Viewed:
        Rejected = -1
        NotViewed = 0
        Accepted = 1

    class Notified:
        NotNotified = 0
        IsNotified = 1


def get_log_path() -> pathlib.Path:
    global log_path
    return log_path


def get_lang_file(lang_file: str):
    global lang_path
    return lang_path.joinpath(lang_file)


def get_db_file(db_file: str):
    global db_path
    return db_path.joinpath(db_file)


def setup_main_folders():
    global root_path, db_path, lang_path, log_path
    root_path = pathlib.Path(__file__).parent.parent
    db_path = root_path.joinpath('data')
    lang_path = root_path.joinpath('languages')
    log_path = root_path.joinpath('logs')


def get_table_name(database_filename: str):
    database_filename_parts = re.split('\.', database_filename)
    database_name = database_filename_parts[0]
    database_table = database_name
    return database_table


def get_lang_code(language_str):
    language: int
    if language_str == 'ru' or language_str == 'be':
        language = CommonHelper.Language.Russian
    elif language_str == 'en':
        language = CommonHelper.Language.English
    else:
        language = CommonHelper.Language.English

    return language
