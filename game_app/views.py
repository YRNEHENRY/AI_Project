from urllib import request
from flask import Flask, render_template, request, jsonify


from game_app.models import Boards, Humans, QTableState, historys, insert, init_db, AIs, db
from game_app.ai import AI
from game_app.business import Human, Board, map_AI, map_Human, map_board


app = Flask(__name__)
app.config.from_object('config')
size = 4


boards = {}


@app.route('/')
def index():
    """ Render the homepage template on the / route """
    """
    init_db()
    insert(Humans(password = "ratio", email = "deuxiemeRatio@yahoo.fr", name = "Giri", first_name = "Oni"))
    insert(AIs())
    insert(AIs())
    print(Humans.query.all())
    print(AIs.query.all())
    """
    #qtable_overview(10)
    return render_template('index.html', size = size)

@app.route('/game/')
def game():
    """ Render the game template on the /game route"""
    historys.query.delete()
    Boards.query.delete()
    db.session.commit()
    return render_template('game.html', size = size)

@app.route('/game/start/')
def start():
    """ Start a new game """
    player = map_Human(Humans.query.get(1))
    
    ai = map_AI(AIs.query.get(1))
    ai2 = map_AI(AIs.query.get(2))
    ai.eps = 1
    ai2.eps = 1

    # player 1
    # new_board = Boards(size = size, fk_player_1 = Humans.query.get(1).id, fk_player_2 = AIs.query.get(1).id, turn = 1, position_p1 = "00", position_p2 = "33", state_board = ("1" + "0"*((size * size) - 2) + "2"))
    # insert(new_board)
    # board = map_board(new_board, player, ai)

    # ai 1
    new_board = Boards(size = size, fk_player_1 = AIs.query.get(1).id, fk_player_2 = Humans.query.get(1).id, turn = 1, position_p1 = "00", position_p2 = "33", state_board = ("1" + "0"*((size * size) - 2) + "2"))
    insert(new_board)
    board = map_board(new_board, ai, player)

    ai.set_board(board)
    ai2.set_board(board)
    boards[board.id] = board
    is_done = board.play()

    return {"id_board" : board.id, "state_board" : board.get_tab_state(), "turn" : board.turn, "position_p1" : board.positions[0], "position_p2" : board.positions[1], "player1_is_AI" : isinstance(board.player_1, AI), "player2_is_AI" : isinstance(board.player_2, AI), "is_done" : is_done[0], "winner" : is_done[1], 'size' : board.size}



@app.route('/game/move/', methods=['POST'])
def move():
    """ Move a player in the game"""
    data = request.get_json()
    move = data['move']
    id = data['idBoard']
    turn = data['turn']
    state = data['state_board']

    boards[id].move_player(move)
    if state == boards[id].get_tab_state():
        boards[id].play()
        boards[id].check_enclosure()
        is_done = boards[id].is_done()
        boards[id].turn = 2 if boards[id].turn == 1 else 1
        boards[id].check_enclosure()
        if not boards[id].is_done()[0]:
            boards[id].turn = 2 if boards[id].turn == 1 else 1
        is_done = boards[id].is_done()

        return {"state_board" : boards[id].get_tab_state(), "turn" : boards[id].turn, "position_p1" : boards[id].positions[0], "position_p2" : boards[id].positions[1], "player1_is_AI" : isinstance(boards[id].player_1, AI), "player2_is_AI" : isinstance(boards[id].player_2, AI), "is_done" : is_done[0], "winner" : is_done[1]}
    else:
        #triche
        return {"state_board" : boards[id].get_tab_state(), "turn" : boards[id].turn, "position_p1" : [-1,-1], "position_p2" : [-1,-1], "player1_is_AI" : isinstance(boards[id].player_1, AI), "player2_is_AI" : isinstance(boards[id].player_2, AI), "is_done" : is_done[0], "winner" : is_done[1]}

    



@app.route('/train/')
def train():
    """ Render the train template on the /train route"""
    return render_template('train.html')

@app.route('/train/ai/')
def train_ai():
    """ Train the AI """
    ai = map_AI(AIs.query.get(1))
    ai2 = map_AI(AIs.query.get(2))

    historys.query.delete()
    Boards.query.delete()
    ai.eps = 0.5
    ai2.eps = 0.5

    print(f"Training AI {ai.eps} started")
    for ind in range(1, 251):
        print(ind)
        for i in range(1, 1000):
            #new_board = Boards(size = size, fk_player_1 = AIs.query.get(1).id, fk_player_2 = AIs.query.get(2).id, turn = 1, position_p1 = "00", position_p2 = "33", state_board = ("1" + "0"*((size * size) - 2) + "2"))
            #insert(new_board)
            
            #board = map_board(new_board, ai2, ai)
            board = Board((ind*1000)+i, size, ai2, ai)
            ai.set_board(board)
            ai2.set_board(board)
            #boards[board.id] = board
            is_done = board.play()
    print(f"Training  AI {ai.eps} done")

    historys.query.delete()
    Boards.query.delete()

    return {"id_done" : True}





@app.route('/rules/')
def rules():
    """ Render the rules template on the /rules route"""
    return render_template('rules.html')

@app.route('/infos/')
def infos():
    """ Render the infos template on the /infos route who contains the informations about a player"""
    return render_template('infos.html')


