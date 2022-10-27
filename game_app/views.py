from urllib import request
from flask import Flask, render_template

from game_app.models import AI, Board, Human

app = Flask(__name__)
app.config.from_object('config')
size = 4

@app.route('/')
def index():
    return render_template('index.html', size = size)

@app.route('/game/')
def game():
    return render_template('game.html', size = size)

@app.route('/game/start/')
def start():
    player = Human("password1", "email1", "player1", "human_player1")
    ia = AI()
    board = Board(size, [[2,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1]], 1, (3,3), (0,0))
    return {"state_board" : board.state_board, "turn" : board.turn, "position_p1" : board.position_p1, "position_p2" : board.position_p2}


@app.route('/game/move/')
def move():
    return {"test" : "bonjour"}

