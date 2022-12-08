import random

from game_app.models import historys, insertt



class AI ():

    def __init__(self, id, login):
        self.login = login
        self.id = id
        self.eps = 0.95
        self.Q_table = {}
        self.history_actions = ""
        self.history_states = ""
        self.history_positions = ""

    def set_board(self, board):
        self.board = board

    def exploration_step(self, position):
        old_position = position
        old_state = self.board.state_board
        possible_move, actions = self.board.get_possible_move(position)
        i_random = random.randint(0, len(possible_move) - 1)
        self.board.positions[self.board.turn - 1] = possible_move[i_random]
        self.board.check_enclosure()
        self.board.update_state()
        return actions[str(possible_move[i_random])], old_state, old_position


    def greedy_step(self, state, position):
        old_position = position
        old_state = self.board.state_board
        moves, actions = self.board.get_possible_move(position)
        vmin = None
        vi = None
        for i in range(len(moves)):
            action = moves[i]

        self.board.check_enclosure()
        self.board.update_state()
        return actions[str(action)], old_state, old_position

    
    def play(self, position, state):
        action = {}
        old_state = ""
        #if random.uniform(0, 1) < self.eps:
        if True:
            action, old_state, old_position = self.exploration_step(position)
        else:
            action, old_state, old_position = self.greedy_step(state, position)

        self.history_actions = self.history_actions + str(action)
        self.history_states = self.history_states + old_state + "|"
        self.history_positions = self.history_positions + str(old_position[0]) + str(old_position[1]) + "|"

        
    def save(self):
        actions = self.history_actions
        states = self.history_states
        positions = self.history_positions
        history = historys(actions = actions, states = states, positions = positions)
        insertt(history)