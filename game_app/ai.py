import random

from game_app.models import QTableState, historys, insertt, db



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
        rewards = self.board.get_rewards()
        self.board.positions[self.board.turn - 1] = possible_move[i_random]
        self.board.check_enclosure()
        self.board.update_state()
        return actions[str(possible_move[i_random])], old_state, old_position, rewards


    def greedy_step(self, state, position):
        rewards = self.board.get_rewards()
        old_position = position
        old_state = self.board.state_board
        moves, actions = self.board.get_possible_move(position)
    
        pos_opponent = self.board.positions[0] if self.board.turn == 2 else self.board.positions[1]
        pos1 = position if self.board.turn == 1 else pos_opponent
        pos2 = position if self.board.turn == 2 else pos_opponent
        state_id = state + str(pos1[0]) + str(pos1[1]) + str(pos2[0]) + str(pos2[1]) + str(self.board.turn)
        action = [0,0]
        qtable = QTableState.query.get(state_id)
        if qtable == None or qtable.up_score == 0 and qtable.left_score == 0 and qtable.down_score == 0 and qtable.right_score == 0:
            return self.exploration_step(position)
        else:
            index = [qtable.up_score, qtable.left_score, qtable.down_score, qtable.right_score].index(max([qtable.up_score, qtable.left_score, qtable.down_score, qtable.right_score]))
            pos = self.board.positions[self.board.turn - 1]
            if index == 0:
                pos[0] = pos[0] - 1
                self.board.positions[self.board.turn - 1] = pos
                action = pos

            elif index == 1:

                pos[1] = pos[1] - 1
                self.board.positions[self.board.turn - 1] = pos
                action = pos

            elif index == 2:
                pos[0] = pos[0] + 1

                self.board.positions[self.board.turn - 1] = pos
                action = pos

            elif index == 3:
                pos[1] = pos[1] + 1
                self.board.positions[self.board.turn - 1] = pos
                action = pos

            self.board.check_enclosure()
            self.board.update_state()
            return actions[str(action)], old_state, old_position, rewards

    
    def get_move(self, position, state):
        action = {}
        old_state = ""
        rewards = {}
        turn = self.board.turn
        pos_opponent = self.board.positions[0] if turn == 2 else self.board.positions[1]
        if random.uniform(0, 1) > self.eps:
            action, old_state, old_position, rewards = self.exploration_step(position)
        else:
            action, old_state, old_position, rewards = self.greedy_step(state, position)

        self.update_Qtable(rewards, old_state, action, old_position, turn, pos_opponent, self.board.state_board)
        self.history_actions = self.history_actions + str(action)
        self.history_states = self.history_states + old_state + "|"
        self.history_positions = self.history_positions + str(old_position[0]) + str(old_position[1]) + "|"

        
    def save(self):
        actions = self.history_actions
        states = self.history_states
        positions = self.history_positions
        history = historys(actions = actions, states = states, positions = positions)
        insertt(history)

    def update_Qtable(self, rewards, state, action, position, turn, pos_opponent, statep1):

        pos1 = position if turn == 1 else pos_opponent
        pos2 = position if turn == 2 else pos_opponent
        state_id = state + str(pos1[0]) + str(pos1[1]) + str(pos2[0]) + str(pos2[1]) + str(turn)


        statep1_id = statep1 + str(self.board.positions[0][0]) + str(self.board.positions[0][1]) + str(self.board.positions[1][0]) + str(self.board.positions[1][1]) + str(self.board.turn)


        qtable = QTableState.query.get(state_id)
        if qtable == None:
            insertt(QTableState(state = state_id))
            qtable = QTableState.query.get(state_id)

        qtablep1 = QTableState.query.get(statep1_id)
        if qtablep1 == None:
            insertt(QTableState(state = statep1_id))
            qtablep1 = QTableState.query.get(statep1_id)

        #UP
        if action == 0:

            qtable.up_score = qtable.up_score + 0.1 * (rewards['0'] + 0.9 * qtablep1.up_score - qtable.up_score)
        #LEFT
        elif action == 1:

            qtable.left_score = qtable.left_score + 0.1 * (rewards['1'] + 0.9 * qtablep1.left_score - qtable.left_score)
        #DOWN
        elif action == 2:

            qtable.down_score = qtable.down_score + 0.1 * (rewards['2'] + 0.9 * qtablep1.down_score - qtable.down_score)
        #RIGHT
        elif action == 3:

            qtable.right_score = qtable.right_score + 0.1 * (rewards['3'] + 0.9 * qtablep1.right_score - qtable.right_score)

        db.session.commit()