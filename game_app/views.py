from urllib import request
from flask import Flask, render_template, request


from game_app.models import Boards, Humans
from game_app.ai import AIs


app = Flask(__name__)
app.config.from_object('config')
size = 4

#dico temporaire en attendant l'accès à la DB
boards = {}
#temporaire avant accès à la DB
ids = list(range(1, 100))

@app.route('/')
def index():
    return render_template('index.html', size = size)

@app.route('/game/')
def game():
    return render_template('game.html', size = size)

@app.route('/game/start/')
def start():
    player1 = Humans("password1", "email1", "player1", "human_player1")
    player2 = Humans("password2", "email2", "player2", "human_player2")
    ai = AIs()
    board = Boards(ids[0], size, player1, ai)
    ids.remove(ids[0])
    ai.set_board(board)
    boards[board.id] = board
    is_done = board.play()
    return {"id_board" : board.id, "state_board" : board.get_tab_state(), "turn" : board.turn, "position_p1" : board.positions[0], "position_p2" : board.positions[1], "player1_is_AI" : isinstance(board.player_1, AIs), "player2_is_AI" : isinstance(board.player_2, AIs), "is_done" : is_done[0], "winner" : is_done[1], 'size' : board.size}


@app.route('/game/move/')
def move():
    movement = request.args.get('movement')
    parameter = movement.split("|")
    move = parameter[0]
    id = int(parameter[1])
    turn = int(parameter[2])
    state = ''.join(parameter[3].split(","))
    boards[id].move_player(move)

    if state == boards[id].state_board:
        boards[id].play()
        is_done = boards[id].check_enclosure()
        return {"state_board" : boards[id].get_tab_state(), "turn" : boards[id].turn, "position_p1" : boards[id].positions[0], "position_p2" : boards[id].positions[1], "player1_is_AI" : isinstance(boards[id].player_1, AIs), "player2_is_AI" : isinstance(boards[id].player_2, AIs), "is_done" : is_done[0], "winner" : is_done[1]}
    else:
        #triche
        return {"state_board" : boards[id].get_tab_state(), "turn" : boards[id].turn, "position_p1" : [-1,-1], "position_p2" : [-1,-1], "player1_is_AI" : isinstance(boards[id].player_1, AIs), "player2_is_AI" : isinstance(boards[id].player_2, AIs), "is_done" : is_done[0], "winner" : is_done[1]}




@app.route('/rules/')
def rules():
    return render_template('rules.html')

@app.route('/infos/')
def infos():
    return render_template('infos.html')


