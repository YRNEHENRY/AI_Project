from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import ast
import logging as lg

from sqlalchemy import Column, ForeignKey, Integer

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)

def init_db():
    db.drop_all()
    db.create_all()

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(25), nullable = False, unique = True)
    nb_wins = db.Column(db.Integer, nullable = False)
    nb_defeats = db.Column(db.Integer, nullable = False)

    games = db.relationship('Boards', backref='player') # multiple foreign key to board (many to one)

    def __init__(self,login):
        self.login = login


class Humans (db.Model):
    __tablename__ = "humans"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    password = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique = True)
    name = db.Column(db.String(25), nullable = False)
    first_name = db.Column(db.String(25), nullable = False)

    user = db.Column(db.Integer,db.ForeignKey('user.id')) # foreign key to user

    def __init__(self, password, email, name, first_name):
        self.password = password
        self.email = email
        self.name = name
        self.first_name = first_name

class AIs (db.Model):
    __tablename__ = "ais"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    user = db.Column(db.Integer,db.ForeignKey('user.id')) # foreign key to user

    def __init__(self):
        pass

class Boards(db.Model):
    __tablename__ = "boards"

    id = db.Column(db.Integer, primary_key = True)
    size = db.Column(db.Integer, nullable = False)
    state_board = db.Column(db.String(36), nullable = False)
    turn = db.Column(db.Integer, nullable = False)
    position_p1 = db.Column(db.String(2), nullable = False)
    position_p2 = db.Column(db.String(2), nullable = False)

    player_1 = db.Column(Integer, ForeignKey("users.id")) # foreign key to user
    player_2 = db.Column(Integer, ForeignKey("users.id")) # foreign key to user

    def __init__(self, size, state_board, turn, position_p1, position_p2, player_1, player_2):
        self.size = size
        self.state_board = state_board # à la création, faire un algorithme qui remplie le tableau de 0 * X cellules
        self.turn = turn
        self.position_p1 = position_p1
        self.position_p2 = position_p2
        self.player_1 = player_1
        self.player_2 = player_2

    def update_state(self):
        if self.turn == 1:
            x = self.position_p1[0]
            y = self.position_p1[1]
        else:
            x = self.position_p2[0]
            y = self.position_p2[1]
        self.state_board[x][y] = 1 if self.turn == 1 else 2
        self.turn = 2 if self.turn == 1 else 1

#class Position_history(db.Model):
#    __tablename__ = "position_history"
#    def __init__(self) -> None:
#        pass
