class WrongIdException(Exception):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return f'User with ID {self.id} not found in databases'
