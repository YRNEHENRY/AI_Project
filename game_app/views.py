
from urllib import request
from flask import Flask, render_template, request
import flask

from game_app.models import AIs, Boards, Humans

app = Flask(__name__)
app.config.from_object('config')
size = 4
player = Humans("password1", "email1", "player1", "human_player1")
ai = AIs()
board = Boards(size, [[2,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1]], 1, [3,3], [0,0], ai, player)
ai.set_board(board)

@app.route('/')
def index():
    return render_template('index.html', size = size)

@app.route('/game/')
def game():
    return render_template('game.html', size = size)

@app.route('/game/play/')
def start():
    return {"state_board" : board.state_board, "turn" : board.turn, "position_p1" : board.position_p1, "position_p2" : board.position_p2, "player1IsAI" : isinstance(board.player_1, AIs), "player2isAI" : isinstance(board.player_2, AIs)}


@app.route('/game/move', methods = ['GET', 'POST'])
def move():
    if flask.request.method == 'POST':
        move = request.args.get('move')
        move = move.split(",")
        move = list(map(int, move))
        if board.turn == 1:
            board.position_p1 = move
        else:
            board.position_p2 = move
        board.update_state()
        
    return {"Success": True}

@app.route('/game/moveAI', methods = ['GET', 'POST'])
def moveAI():
    if flask.request.method == 'POST':
        position = board.position_p1 if board.turn == 1 else board.position_p2
        board.players[board.turn - 1].play(position)
    return {"Success": True}

@app.route('/game/isDone/')
def is_done():
    is_done, winner = board.is_done()
    return {"isDone" : is_done, "winner" : winner}

@app.route('/rules/')
def rules():
    return render_template('rules.html')

@app.route('/infos/')
def infos():
    return render_template('infos.html')


