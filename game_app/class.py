class User:

    def __init__(self, login):
        self.login = login


class Human (User):

    def __init__(self, login, password, email, name, first_name):
        super().__init__(login)
        self.password = password
        self.email = email
        self.name = name
        self.first_name = first_name

class AI (User):

    def __init__(self, login):
        super().__init__(login)

class Player:

    def __init__(self, position):
        self.position = position

class Board:

    def __init__(self, id, size, state_board, turn):
        self.id = id
        self.size = size
        self.state_board = state_board
        self.turn = turn

class Position_history:

    def __init__(self) -> None:
        pass
