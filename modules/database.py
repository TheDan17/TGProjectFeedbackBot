import logging
import sqlite3
import pprint

from modules import common


class UserManagement:
    @staticmethod
    def user_exists(user_id):
        db_driver = DatabaseDriver()
        db_driver.set_database(DatabaseHelper.Databases.UsersDatabase)

        result = db_driver.get('id', user_id, 'language')
        if result is None:
            return False
        else:
            return True

    @staticmethod
    def register_user(user_id: int):
        db_interface = DatabaseInterface()
        db_interface.add_user(user_id)

    @staticmethod
    def delete_user_from_databases(user_id: int):
        db_interface = DatabaseInterface()
        db_interface.delete_user(user_id)

    @staticmethod
    def clear_user_form(user_id: int):
        db_interface = DatabaseInterface()
        db_interface.db_forms.set_user_form(user_id, '')

    @staticmethod
    def append_user_form(user_id: int, form_part: str):
        db_interface = DatabaseInterface()
        old_form = db_interface.db_forms.get_user_form(user_id)
        new_form = old_form + '\n' + form_part
        db_interface.db_forms.set_user_form(user_id, new_form)

    @staticmethod
    def get_user_lang_code(user_id: int):
        db_interface = DatabaseInterface()
        lang_code = db_interface.db_users.get_user_language(user_id)
        return lang_code


class DatabaseHelper:
    class Databases:
        FormsDatabase = 'forms.db'
        UsersDatabase = 'users.db'
        NotifyDatabase = 'notify.db'

    class Columns:
        class UsersDatabase:
            Language = 'language'

        class FormsDatabase:
            Form = 'form'
            Viewed = 'viewed'

        class NotifyDatabase:
            PastViewed = 'viewed_past'
            PresentViewed = 'viewed_present'
            Notified = 'notified'


class DatabaseDriver:
    db_connect: sqlite3.Connection
    db_cursor: sqlite3.Cursor
    db_table: str

    @staticmethod
    def extract_fetchone(fetchone_data):
        return_data = None
        if fetchone_data is not None:
            return_data = fetchone_data[0]
        return return_data

    def set_database(self, database_filename: str):
        database_path = common.get_db_file(database_filename)
        logging.debug('=== ' + str(database_path) + ' ===')
        self.db_connect = sqlite3.connect(database_path)
        self.db_cursor = self.db_connect.cursor()
        self.db_table = common.get_table_name(database_filename)

    def get(self, what_column_find, what_find, what_column_get):
        self.db_cursor.execute(f'SELECT {what_column_get} FROM {self.db_table} WHERE {what_column_find} = ?',
                               (what_find,))
        result = self.db_cursor.fetchone()
        return self.extract_fetchone(result)

    def delete(self, what_column_delete: str, what_delete):
        self.db_cursor.execute(f'DELETE FROM {self.db_table} WHERE {what_column_delete} LIKE ?',
                               (what_delete,))
        self.db_connect.commit()

    def add(self, what_add: tuple):
        what_add_string = pprint.pformat(what_add)
        self.db_cursor.execute(f'INSERT INTO {self.db_table} VALUES {what_add_string}')
        self.db_connect.commit()

    def update(self, what_column_find, what_find, what_column_update, what_update):
        self.db_cursor.execute(f'UPDATE {self.db_table} SET {what_column_update} = ? WHERE {what_column_find} = ?',
                               (what_update, what_find))
        self.db_connect.commit()

    def get_all(self):
        self.db_cursor.execute(f'SELECT * FROM {self.db_table}')
        results = self.db_cursor.fetchall()
        return results

    def get_range(self):
        pass


class DatabaseInterface:
    db_driver: DatabaseDriver

    db_forms = None
    db_users = None
    db_notify = None

    def set_by_id(self, user_id: int, column: str, value):
        self.db_driver.update('id', user_id, column, value)

    def get_by_id(self, user_id: int, column: str):
        return self.db_driver.get('id', user_id, column)

    class Forms:
        db_driver_in: DatabaseDriver

        def __init__(self, db_driver: DatabaseDriver):
            self.db_driver_in = db_driver

        def set_user_form(self, user_id: int, form: str):
            self.db_driver_in.set_database(DatabaseHelper.Databases.FormsDatabase)
            self.db_driver_in.update('id', user_id, 'form', form)

        def get_user_form(self, user_id: int):
            self.db_driver_in.set_database(DatabaseHelper.Databases.FormsDatabase)
            output = self.db_driver_in.get('id', user_id, 'form')
            return output

        def delete_form(self, user_id: int):
            self.db_driver_in.set_database(DatabaseHelper.Databases.FormsDatabase)
            self.db_driver_in.update('id', user_id, 'form', '')

        def set_user_viewed(self, user_id: int, viewed: int):
            self.db_driver_in.set_database(DatabaseHelper.Databases.FormsDatabase)
            self.db_driver_in.update('id', user_id, 'viewed', viewed)

        def get_user_viewed(self, user_id: int):
            self.db_driver_in.set_database(DatabaseHelper.Databases.FormsDatabase)
            output = self.db_driver_in.get('id', user_id, 'viewed')
            return output

        def get_not_viewed_users(self):
            pass

    class Users:
        db_driver_in: DatabaseDriver

        def __init__(self, db_driver: DatabaseDriver):
            self.db_driver_in = db_driver

        def set_user_language(self, user_id: int, language_code: int):
            self.db_driver_in.set_database(DatabaseHelper.Databases.UsersDatabase)
            self.db_driver_in.update('id', user_id, 'language', language_code)

        def get_user_language(self, user_id: int):
            self.db_driver_in.set_database(DatabaseHelper.Databases.UsersDatabase)
            output = self.db_driver_in.get('id', user_id, 'language')
            return output

    class Notify:
        db_driver_in: DatabaseDriver

        def __init__(self, db_driver: DatabaseDriver):
            self.db_driver_in = db_driver

        def set_user_past_viewed(self, user_id, past_viewed):
            self.db_driver_in.set_database(DatabaseHelper.Databases.NotifyDatabase)
            self.db_driver_in.update('id', user_id, 'viewed_past', past_viewed)

        def get_user_past_viewed(self, user_id):
            self.db_driver_in.set_database(DatabaseHelper.Databases.NotifyDatabase)
            output = self.db_driver_in.get('id', user_id, 'viewed_past')
            return output

        def set_user_present_viewed(self, user_id, present_viewed):
            self.db_driver_in.set_database(DatabaseHelper.Databases.NotifyDatabase)
            self.db_driver_in.update('id', user_id, 'viewed_present', present_viewed)

        def get_user_present_viewed(self, user_id):
            self.db_driver_in.set_database(DatabaseHelper.Databases.NotifyDatabase)
            output = self.db_driver_in.get('id', user_id, 'viewed_present')
            return output

        def set_user_notified(self, user_id, notified):
            self.db_driver_in.set_database(DatabaseHelper.Databases.NotifyDatabase)
            self.db_driver_in.update('id', user_id, 'notified', notified)

        def get_user_notified(self, user_id):
            self.db_driver_in.set_database(DatabaseHelper.Databases.NotifyDatabase)
            output = self.db_driver_in.get('id', user_id, 'notified')
            return output

        def get_all_notify_data(self):
            self.db_driver_in.set_database(DatabaseHelper.Databases.NotifyDatabase)
            results = self.db_driver_in.get_all()
            return results

    def __init__(self):
        self.db_driver = DatabaseDriver()

        self.db_forms = DatabaseInterface.Forms(self.db_driver)
        self.db_users = DatabaseInterface.Users(self.db_driver)
        self.db_notify = DatabaseInterface.Notify(self.db_driver)

    def add_user(self, user_id: int):
        try:
            self.db_driver.set_database(DatabaseHelper.Databases.UsersDatabase)
            self.db_driver.add((user_id, -1))
        except sqlite3.IntegrityError:
            pass

        try:
            self.db_driver.set_database(DatabaseHelper.Databases.FormsDatabase)
            self.db_driver.add((user_id, '', 0))
        except sqlite3.IntegrityError:
            pass

        try:
            self.db_driver.set_database(DatabaseHelper.Databases.NotifyDatabase)
            self.db_driver.add((user_id, 0, 0, 1))
        except sqlite3.IntegrityError:
            pass

    def delete_user(self, user_id):
        try:
            self.db_driver.set_database(DatabaseHelper.Databases.UsersDatabase)
            self.db_driver.delete('id', user_id)
        except sqlite3.OperationalError:
            pass

        try:
            self.db_driver.set_database(DatabaseHelper.Databases.FormsDatabase)
            self.db_driver.delete('id', user_id)
        except sqlite3.OperationalError:
            pass

        try:
            self.db_driver.set_database(DatabaseHelper.Databases.NotifyDatabase)
            self.db_driver.delete('id', user_id)
        except sqlite3.OperationalError:
            pass

    def reset_databases(self):
        pass
