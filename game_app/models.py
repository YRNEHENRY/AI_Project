from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from game_app.ai import AI
from sqlalchemy import Column, ForeignKey, Integer, insert

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)

def init_db():
    db.drop_all()
    db.create_all()

def insertt(test):
    db.session.add(test)
    db.session.commit()

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(25), nullable = False, unique = True)
    nb_wins = db.Column(db.Integer, nullable = False)
    nb_defeats = db.Column(db.Integer, nullable = False)

    #games = db.relationship('Boards', backref='player') # multiple foreign key to board (many to one)



class Humans (db.Model):
    __tablename__ = "humans"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    password = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique = True)
    name = db.Column(db.String(25), nullable = False)
    first_name = db.Column(db.String(25), nullable = False)

    user = db.Column(db.Integer,db.ForeignKey('users.id')) # foreign key to user



class AIs (db.Model):
    __tablename__ = "ais"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user = db.Column(db.Integer,db.ForeignKey('users.id')) # foreign key to user
    Q_table = db.Column(db.String(10000), nullable = True)



class Boards(db.Model):
    __tablename__ = "boards"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    size = db.Column(db.Integer, nullable = False)
    state_board = db.Column(db.String(36), nullable = False)
    turn = db.Column(db.Integer, nullable = False)
    position_p1 = db.Column(db.String(2), nullable = False)
    position_p2 = db.Column(db.String(2), nullable = False)

    player_1 = db.Column(Integer, ForeignKey("users.id")) # foreign key to user
    player_2 = db.Column(Integer, ForeignKey("users.id")) # foreign key to user



#class Position_history(db.Model):
#    __tablename__ = "position_history"
#    def __init__(self) -> None:
#        pass
