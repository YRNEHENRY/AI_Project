
from urllib import request
from flask import Flask, render_template, request
import flask

from game_app.models import AIs, Boards, Humans

app = Flask(__name__)
app.config.from_object('config')
size = 4
player = Humans("password1", "email1", "player1", "human_player1")
ai = AIs()
board = Boards(size, ai, ai)
ai.set_board(board)

@app.route('/')
def index():
    return render_template('index.html', size = size)

@app.route('/game/')
def game():
    return render_template('game.html', size = size)

@app.route('/game/start/')
def start():
    is_done = board.play()
    return {"state_board" : board.get_tab_state(), "turn" : board.turn, "position_p1" : board.positions[0], "position_p2" : board.positions[1], "player1_is_AI" : isinstance(board.player_1, AIs), "player2_is_AI" : isinstance(board.player_2, AIs), "is_done" : is_done[0]}


@app.route('/game/move/')
def move():
    movement = request.args.get('movement')
    
    is_done = board.move_player(movement)
    board.play()
    return {"state_board" : board.get_tab_state(), "turn" : board.turn, "position_p1" : board.positions[0], "position_p2" : board.positions[1], "player1_is_AI" : isinstance(board.player_1, AIs), "player2_is_AI" : isinstance(board.player_2, AIs), "is_done" : is_done[0]}





@app.route('/rules/')
def rules():
    return render_template('rules.html')

@app.route('/infos/')
def infos():
    return render_template('infos.html')


