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
        self.board.positions[self.board.turn - 1] = possible_move[i_random]
        self.board.check_enclosure()
        self.board.update_state()
        return actions[str(possible_move[i_random])], old_state, old_position


    def greedy_step(self, state, position):
        old_position = position
        old_state = self.board.state_board
        moves, actions = self.board.get_possible_move(position)
    
        pos_opponent = self.board.positions[0] if self.board.turn == 2 else self.board.positions[1]
        pos1 = self.board.positions[0]
        pos2 = self.board.positions[1]


        state_id = state + str(pos1[0]) + str(pos1[1]) + str(pos2[0]) + str(pos2[1]) + str(self.board.turn)

        action = [0,0]
        qtable = QTableState.query.get(state_id)

        

        if qtable == None or (qtable.up_score == 0 and qtable.left_score == 0 and qtable.down_score == 0 and qtable.right_score == 0):
            #print("explo")
            return self.exploration_step(position)
        else:
            #print("greed")
            moves = []
            scores = []
            if 0 in list(actions.values()):
                #print(qtable.up_score)
                scores.append(qtable.up_score)
                moves.append(0)
            if 1 in list(actions.values()):
                #print(qtable.left_score)
                scores.append(qtable.left_score)
                moves.append(1)
            if 2 in list(actions.values()):
                #print(qtable.down_score)
                scores.append(qtable.down_score)
                moves.append(2)
            if 3 in list(actions.values()):
                #print(qtable.right_score)
                scores.append(qtable.right_score)
                moves.append(3)
            

            index = scores.index(max(scores))
            move = moves[index]

            pos = self.board.positions[self.board.turn - 1]



            if move == 0:
                pos[0] = pos[0] - 1
                self.board.positions[self.board.turn - 1] = pos
                action = pos

            elif move == 1:

                pos[1] = pos[1] - 1
                self.board.positions[self.board.turn - 1] = pos
                action = pos

            elif move == 2:
                pos[0] = pos[0] + 1

                self.board.positions[self.board.turn - 1] = pos
                action = pos

            elif move == 3:
                pos[1] = pos[1] + 1
                self.board.positions[self.board.turn - 1] = pos
                action = pos

            self.board.check_enclosure()
            self.board.update_state()
            return actions[str(action)], old_state, old_position

    
    def get_move(self, position, state):
        actual_state = self.board.state_board
        pos1 = self.board.positions[0]
        pos2 = self.board.positions[1]
        action = {}
        old_state = ""
        turn = self.board.turn
        if random.uniform(0, 1) > self.eps:
            action, old_state, old_position = self.exploration_step(position)
        else:
            action, old_state, old_position = self.greedy_step(actual_state, position)

        if self.board.nb_turn > 2:

            old_state = historys.query.get((self.board.id, self.board.nb_turn - 2))
            self.update_Qtable(old_state, action, pos1, turn, pos2, actual_state)
        self.board.save_history(str(action), actual_state, pos1, pos2)

        

    def update_Qtable(self, state, action, pos1, turn, pos2, statep1):

        
        statep1_id = statep1 + str(pos1[0]) + str(pos1[1]) + str(pos2[0]) + str(pos2[1]) + str(turn)

        turnp1 = "2" if (state.nb_turn % 2 == 0) else "1"

        state_id = state.state + state.position_1 + state.position_2 + turnp1



        reward = self.board.get_reward(state.state, statep1, turn)

        qtable = QTableState.query.get(state_id)
        if qtable == None:
            insertt(QTableState(state = state_id))
            qtable = QTableState.query.get(state_id)

        qtablep1 = QTableState.query.get(statep1_id)
        if qtablep1 == None:
            insertt(QTableState(state = statep1_id))
            qtablep1 = QTableState.query.get(statep1_id)


        score_p1 = max([qtablep1.down_score, qtablep1.up_score, qtablep1.left_score, qtablep1.right_score])

        #UP
        if action == 0:
            qtable.up_score = qtable.up_score + 0.1 * (reward + 0.9 * score_p1 - qtable.up_score)
        #LEFT
        elif action == 1:
            qtable.left_score = qtable.left_score + 0.1 * (reward + 0.9 * score_p1 - qtable.left_score)
        #DOWN
        elif action == 2:
            qtable.down_score = qtable.down_score + 0.1 * (reward + 0.9 * score_p1 - qtable.down_score)
        #RIGHT
        elif action == 3:
            qtable.right_score = qtable.right_score + 0.1 * (reward + 0.9 * score_p1 - qtable.right_score)

        db.session.commit()