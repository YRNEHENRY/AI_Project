from urllib import request
from flask import Flask, render_template, request, jsonify
import random
import pandas as pd

from game_app.models import Boards, Humans, QTableState4, QTableState5, QTableState6, historys, insert, init_db, AIs, db
from game_app.ai import AI
from game_app.business import Human, Board, map_AI, map_Human, map_board

app = Flask(__name__)
app.config.from_object('config')

boards = {}
size = 4

path_builder = lambda folder, eps, lr: f"data/{folder}/ais_eps{eps*100}_lr{lr*100}.csv"
"""
Function Name: path_builder

Description:
This lambda function constructs a file path string based on the provided parameters: folder, eps, and lr.
The resulting string follows the format: "data/{folder}/ais_eps{eps*100}_lr{lr*100}.csv".

Parameters:
- folder (str): The name of the folder.
- eps (float): The epsilon value, multiplied by 100 to represent a percentage.
- lr (float): The learning rate value, multiplied by 100 to represent a percentage.

Returns:
str: The file path string constructed using the provided parameters.
"""

clear_games = lambda: (
    historys.query.delete(),
    Boards.query.delete(),
    db.session.commit()
)


def training_to_csv(ai1 : AI, ai2 : AI, size_board, nb_games : int, sessions : int, nb_tests : int, eps : float, eps_dec : float, lr : float):
    """
    """
    df = pd.DataFrame(columns=["winner", "p1_squares", "p2_squares", "turns"])

    QTableState4.delete_all()
    clear_games()

    ai1.learning_rate, ai2.learning_rate = lr, lr
    nb_games = (nb_games / sessions) * 1000
    eps = eps + eps_dec

    print(f"Training started - eps {eps} & lr {lr}")
    # we train the AI for all the sessions
    for phase in range(1, sessions + 1):
        # we decrease epsilon each session
        eps = eps - eps_dec if eps > 0 else 0
        ai1.eps, ai2.eps = eps, eps
    
        # we train the AI for 1 session
        print(f"Session {phase} : training...")
        for i in range(1, nb_games + 1):
            board = Board(i, size, ai2, ai1)
            ai1.set_board(board)
            ai2.set_board(board)
            is_done = board.play()

        clear_games()
        ai1.eps, ai2.eps = 0, 0
        print(f"Session {phase} : results...")
        # we test the AI for 1 session
        for i in range(1, nb_tests + 1):
            board = Board(i, size, ai2, ai1)
            ai1.set_board(board)
            ai2.set_board(board)
            is_done = board.play()

            p1_squares, p2_squares = board.count_squares()
            winner = "p1" if p1_squares > p2_squares else "p2"
            df.loc[len(df)] = [winner, p1_squares, p2_squares, board.nb_turn]
        
    print(f"Training done - eps {eps} & lr {lr}")

    file_path = path_builder("trains", eps, lr)
    df.to_csv(file_path, index=False)

    file_path = path_builder("ai", eps, lr)
    QTableState4.export_to_csv(file_path)

    print("Export as csv completed\n\n")

def training(ai1 : AI, ai2 : AI, size, nb_games : int, eps : float, lr : float):
    clear_games()
    ai1.eps, ai2.eps = eps, eps
    ai1.learning_rate, ai2.learning_rate = lr, lr

    print(f"Training started - eps {eps} & lr {lr}")
    for ind in range(1, nb_games + 1):
        print(ind)
        for i in range(1, 1000):
            board = Board((ind*1000)+i, size, ai2, ai1)
            ai1.set_board(board)
            ai2.set_board(board)
            is_done = board.play()
            
    print(f"Training done - eps {eps} & lr {lr}")

@app.route('/')
def index():

    """ Render the homepage template on the / route """
    return render_template('index.html', size = size)

@app.route('/game/')
def game():
    """ Render the game template on the /game route"""
    size = int(request.args.get("size"))

    db.session.commit()
    return render_template('game.html', size = size)

@app.route('/game/start')
def start():
    """ Start a new game """
    parameters = request.args.get("players")
    
    p1 = parameters.split('/')[0]
    p2 = parameters.split('/')[1]
    size = int(parameters.split('/')[2])

    if p1 == 'human':
        player1 = Humans.query.get(1).id
        mapped_player1 = map_Human(Humans.query.get(1))
    else:
        player1 = AIs.query.get(2).id
        mapped_player1 = map_AI(AIs.query.get(2))
        mapped_player1.eps = 0

    if p2 == 'human':
        player2 = Humans.query.get(2).id
        mapped_player2 = map_Human(Humans.query.get(2))
    else:
        player2 = AIs.query.get(1).id
        mapped_player2 = map_AI(AIs.query.get(1))
        mapped_player2.eps = 0
    

    swap = lambda a, b, mapped_a, mapped_b: (b, a, mapped_b, mapped_a) if random.random() < 0.5 else (a, b, mapped_a, mapped_b)
    player1, player2, mapped_player1, mapped_player2 = swap(player1, player2, mapped_player1, mapped_player2)

    new_board = Boards(size = size, fk_player_1 = player1, fk_player_2 = player2, turn = 1, position_p1 = "00", position_p2 = "33", state_board = ("1" + "0"*((size * size) - 2) + "2"))
    insert(new_board)
    board = map_board(new_board, mapped_player1, mapped_player2)

    if isinstance(mapped_player1, AI):
        mapped_player1.set_board(board)
    if isinstance(mapped_player2, AI):
        mapped_player2.set_board(board)

    namep1 = mapped_player1.first_name if not isinstance(mapped_player1, AI) else mapped_player1.login
    namep2 = mapped_player2.first_name if not isinstance(mapped_player2, AI) else mapped_player2.login


    if isinstance(mapped_player1, AI) and isinstance(mapped_player2, AI):
        mapped_player1.eps = 0.2
        mapped_player2.eps = 0.2
    boards[board.id] = board
    is_done = board.play()

    return {"id_board" : board.id, "state_board" : board.get_tab_state(), "turn" : board.turn, "position_p1" : board.positions[0], "position_p2" : board.positions[1], "player1_is_AI" : isinstance(board.player_1, AI), "player2_is_AI" : isinstance(board.player_2, AI), "is_done" : is_done[0], "winner" : is_done[1], 'size' : board.size, "namep1" : namep1, "namep2" : namep2}



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
    size = int(request.args.get("size"))

    ai1 = map_AI(AIs.query.get(1))
    ai2 = map_AI(AIs.query.get(2))


    training_to_csv(ai1, ai2, size, 10, 10, 20, 0.9, 0.08, 0.9)
    return {"id_done" : True}

@app.route('/infos/')
def infos():
    """ Render the infos template on the /infos route who contains the informations about a player"""
    return render_template('infos.html')

@app.route('/infos/user/')
def infos_user():
    """ Render the infos template on the /infos/user route who contains the informations about a player"""
    return render_template('infos.html')


@app.route('/properties/')
def properties():
    """ Render the properties template on the /properties route who contains the properties of the AI"""
    return render_template('properties.html')

@app.route('/properties/reboot/')
def properties_reboot():
    """ Reboot the db """
    init_db()
    insert(Humans(password = "ratio", email = "deuxiemeRatio@yahoo.fr", name = "Giri", first_name = "Oni"))
    insert(Humans(password = "Nouveauratio", email = "troisiemeRatio@yahoo.fr", name = "Cool", first_name = "Samuraï"))
    insert(AIs())
    insert(AIs())
    return render_template('properties.html')

@app.route('/properties/delete/')
def properties_delete():
    """ Delete the AI """
    QTableState4.delete_all()
    return render_template('properties.html')

@app.route('/properties/import/')
def properties_import():
    """ Import the AI """
    QTableState4.import_from_csv("data/ai/ais_eps90.0_lr90.0.csv")
    return render_template('properties.html')