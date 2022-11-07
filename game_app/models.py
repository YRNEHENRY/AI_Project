from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import ast
import logging as lg
import random
import operator as op

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

    #games = db.relationship('Boards', backref='player') # multiple foreign key to board (many to one)

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

    def set_board(self, board):
        self.board = board

    def play(self, position):
        possible_move = self.board.get_possible_move(position)
        
        i_random = random.randint(0, len(possible_move) - 1)
        print("Move possible pour ia",possible_move)
        print("choix i ", i_random)
        print("nbr de choix ", len(possible_move))

        self.board.positions[self.board.turn - 1] = possible_move[i_random]

        self.board.update_state()
        



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

    def __init__(self, size, player_1, player_2):
        self.size = size
        self.state_board = "1" + "0"*((size * size) - 2) + "2"
        self.turn = 1
        self.position_p1 = [0,0]
        self.position_p2 = [self.size-1, self.size-1]
        self.positions = [self.position_p1, self.position_p2]
        self.player_1 = player_1
        self.player_2 = player_2
        self.players = [player_1, player_2]
        #, player_1, player_2

    def play(self):
        is_done = self.is_done()[0]
        print(is_done)
        while isinstance(self.players[self.turn - 1], AIs) and not is_done:
            self.players[self.turn - 1].play(self.positions[self.turn - 1])
            print("(joueur : ", self.turn,")Ia vient de jouer : ", self.get_tab_state())
            is_done = self.is_done()[0]
            print("\n\n")
        return self.is_done()

    def move_player(self, movement):
        print("ancienne pos ", self.positions[self.turn - 1])
        if movement == 'UP':
            self.positions[self.turn - 1][0] -= 1
        elif movement == "DOWN":
            self.positions[self.turn - 1][0] += 1
        elif movement == "LEFT":
            self.positions[self.turn - 1][1] -= 1
        elif movement == "RIGHT":
            self.positions[self.turn - 1][1] += 1

        self.update_state()
        return self.is_done()

    def get_possible_move(self, position):
        possible_move = []
        opponent_turn = 2 if self.turn == 1 else 1


        if (position[0] - 1) >= 0 and self.get_tab_state()[position[0] - 1][position[1]] != opponent_turn:
            possible_move.append([position[0] - 1, position[1]])
        
        if (position[1] - 1) >= 0 and self.get_tab_state()[position[0]][position[1] - 1] != opponent_turn:
            possible_move.append([position[0], position[1] - 1])
        
        if (position[0] + 1) <= 3 and self.get_tab_state()[position[0] + 1][position[1]] != opponent_turn:
            possible_move.append([position[0] + 1, position[1]])

        if (position[1] + 1) <= 3 and self.get_tab_state()[position[0]][position[1] + 1] != opponent_turn:
            possible_move.append([position[0], position[1] + 1])

        return possible_move

    def get_tab_state(self):
        state = []
        i = 0
        for y in range(0, self.size):
            line = []
            for j in range(0, self.size):
                line.append(int(self.state_board[i]))
                i +=1
            state.append(line)
        return state

    def state_to_string(self, state):
        str_sate = ''
        for line in state:
            for s in line:
                str_sate += str(s)
        return str_sate
        

    


    def update_state(self):
        state = self.get_tab_state()
    
        x = self.positions[self.turn - 1][0]
        y = self.positions[self.turn - 1][1]
        print("nouvel pos : ", x, " ", y)
        state[x][y] = 1 if self.turn == 1 else 2
        self.turn = 2 if self.turn == 1 else 1
        self.state_board = self.state_to_string(state)


    def is_done(self):
        is_done = False
        winner = "Nobody"
        for i in range(0, 4):
            if 0 in self.get_tab_state()[i]:
                return is_done, winner

        is_done = True
        nb_1 = op.countOf(self.get_tab_state(), 1)
        nb_2 = op.countOf(self.get_tab_state(), 2)
        if nb_1 > nb_2:
            winner = self.player_1
        elif nb_1 < nb_2:
            winner = self.player_2
        return is_done, winner


#class Position_history(db.Model):
#    __tablename__ = "position_history"
#    def __init__(self) -> None:
#        pass
