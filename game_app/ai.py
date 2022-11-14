from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import random
from sqlalchemy import Column, ForeignKey, Integer

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)

def init_db():
    db.drop_all()
    db.create_all()



class AIs (db.Model):
    __tablename__ = "ais"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    user = db.Column(db.Integer,db.ForeignKey('user.id')) # foreign key to user

    def __init__(self):
        pass

    def set_board(self, board):
        self.board = board

    def play(self, position):
        possible_move = self.board.get_possible_move(position)
        
        i_random = random.randint(0, len(possible_move) - 1)

        self.board.positions[self.board.turn - 1] = possible_move[i_random]

        self.board.update_state()