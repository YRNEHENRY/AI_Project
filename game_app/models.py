from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "user"
    __abstract__ = True

    id = db.Column(db.Integer, primary_key = True)
    #games = relationship("Board")


class Human (User):
    __tablename__ = "human"
    #__table_args__ = (UniqueConstraint('login'))

    login = db.Column(db.String(25), nullable = False)
    password = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), nullable = False)
    name = db.Column(db.String(25), nullable = False)
    first_name = db.Column(db.String(25), nullable = False)

    def __init__(self, login, password, email, name, first_name):
        super().__init__()
        self.login = login
        self.password = password
        self.email = email
        self.name = name
        self.first_name = first_name

class AI (User):
    __tablename__ = "ai"

    def __init__(self):
        pass

class Board(db.Model):
    __tablename__ = "board"

    id = db.Column(db.Integer, primary_key = True)
    size = db.Column(db.Integer, nullable = False)
    state_board = db.Column(db.String(36), nullable = False)
    turn = db.Column(db.Integer, nullable = False)
    position_p1 = db.Column(db.String(2), nullable = False)
    position_p2 = db.Column(db.String(2), nullable = False)

    #player1_id = Column(Integer, ForeignKey("user.id"))
    #player2_id = Column(Integer, ForeignKey("user.id"))

    def __init__(self, size, state_board, turn, position_p1, position_p2):
        self.size = size
        self.state_board = state_board
        self.turn = turn
        self.position_p1 = position_p1
        self.position_p2 = position_p2

#class Position_history(db.Model):
#    __tablename__ = "position_history"
#    def __init__(self) -> None:
#        pass
