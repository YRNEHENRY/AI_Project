import random

from game_app.models import QTableState4, QTableState5, QTableState6, historys, insert, db



class AI ():

    def __init__(self, id, login):
        self.login = login
        self.id = id
        self.eps = 1
        self.learning_rate = 0.1
        self.history_actions = ""
        self.history_states = ""
        self.history_positions = ""

    def set_board(self, board):
        """
            Set an object Board business
        """
        self.board = board

    def exploration_step(self, position):
        """
            Exploration method to play (random choice)
        """
        old_state = self.board.state_board
        possible_move, actions = self.board.get_possible_move(position)
        i_random = random.randint(0, len(possible_move) - 1)

        return actions[str(possible_move[i_random])], old_state, possible_move[i_random]


    def greedy_step(self, state, position):
        """
            Greedy step method to play (choose the best possible choice based on QTable)
        """
        old_state = self.board.state_board
        moves, actions = self.board.get_possible_move(position)
    
        pos_opponent = self.board.positions[0] if self.board.turn == 2 else self.board.positions[1]
        pos1 = self.board.positions[0]
        pos2 = self.board.positions[1]


        state_id = state + str(pos1[0]) + str(pos1[1]) + str(pos2[0]) + str(pos2[1]) + str(self.board.turn)

        action = [0,0]
        if self.board.size == 4:
            qtable = QTableState4.query.get(state_id)
        elif self.board.size == 5:
            qtable = QTableState5.query.get(state_id)
        elif self.board.size == 6:
            qtable = QTableState6.query.get(state_id)

        
        if qtable == None or (qtable.up_score == 0 and qtable.left_score == 0 and qtable.down_score == 0 and qtable.right_score == 0):
            return self.exploration_step(position)
        else:
            moves = []
            scores = []
            if 0 in list(actions.values()):
                scores.append(qtable.up_score)
                moves.append(0)
            if 1 in list(actions.values()):
                scores.append(qtable.left_score)
                moves.append(1)
            if 2 in list(actions.values()):
                scores.append(qtable.down_score)
                moves.append(2)
            if 3 in list(actions.values()):
                scores.append(qtable.right_score)
                moves.append(3)
            

            index = scores.index(max(scores))
            move = moves[index]

            pos = self.board.positions[self.board.turn - 1]


            if move == 0:
                pos[0] = pos[0] - 1
                action = pos

            elif move == 1:
                pos[1] = pos[1] - 1
                action = pos

            elif move == 2:
                pos[0] = pos[0] + 1
                action = pos

            elif move == 3:
                pos[1] = pos[1] + 1
                action = pos

            return actions[str(action)], old_state, action

    
    def get_move(self, position):
        """
            Get a move base on epsilon (exploration or greedy) then update the QTable and the state of the board
        """
        actual_state = self.board.state_board
        pos1 = self.board.positions[0]
        pos2 = self.board.positions[1]
        action = {}
        old_state = ""
        turn = self.board.turn
        if random.uniform(0, 1) < self.eps:
            action, old_state, pos = self.exploration_step(position)
        else:
            action, old_state, pos = self.greedy_step(actual_state, position)

        return pos, old_state, action, pos1, turn, pos2, actual_state

        

    def update_Qtable(self, state, action, pos1, turn, pos2, statep1):
        """
            Update the state values from a QTable
        """
        actionp1 = action
        
        statep1_id = statep1 + str(pos1[0]) + str(pos1[1]) + str(pos2[0]) + str(pos2[1]) + str(turn)

        turnp1 = "2" if (state.nb_turn % 2 == 0) else "1"

        state_id = state.state + state.position_1 + state.position_2 + turnp1

        action = int(state.action)


        dim = self.board.size * self.board.size

        reward = self.board.rewards(state.state, statep1[0:dim], turn)
        



        if self.board.size == 4:
            qtable = QTableState4.query.get(state_id)
            if qtable == None:
                qtable = QTableState4(state = state_id)
                insert(qtable)

            qtablep1 = QTableState4.query.get(statep1_id)
            if qtablep1 == None:
                qtablep1 = QTableState4(state = statep1_id)
                insert(qtablep1)


        elif self.board.size == 5:
            qtable = QTableState5.query.get(state_id)
            if qtable == None:
                qtable = QTableState5(state = state_id)
                insert(qtable)

            qtablep1 = QTableState5.query.get(statep1_id)
            if qtablep1 == None:
                qtablep1 = QTableState5(state = statep1_id)
                insert(qtablep1)

        elif self.board.size == 6:
            qtable = QTableState6.query.get(state_id)
            if qtable == None:
                qtable = QTableState6(state = state_id)
                insert(qtable)

            qtablep1 = QTableState6.query.get(statep1_id)
            if qtablep1 == None:
                qtablep1 = QTableState6(state = statep1_id)
                insert(qtablep1)

        score_p1 = max([qtablep1.down_score, qtablep1.up_score, qtablep1.left_score, qtablep1.right_score])
        if action == 0:
            qtable.up_score = qtable.up_score + self.learning_rate * (reward + 0.9 * score_p1 - qtable.up_score)
        elif action == 1:
            qtable.left_score = qtable.left_score + self.learning_rate * (reward + 0.9 * score_p1 - qtable.left_score)
        elif action == 2:
            qtable.down_score = qtable.down_score + self.learning_rate * (reward + 0.9 * score_p1 - qtable.down_score)
        elif action == 3:
            qtable.right_score = qtable.right_score + self.learning_rate * (reward + 0.9 * score_p1 - qtable.right_score)

        

        if self.board.is_done()[0]:
            dim = self.board.size * self.board.size
            reward = self.board.rewards(state.state, statep1[0:dim], turn)

            if actionp1 == 0:
                qtablep1.up_score = reward + 100
            elif actionp1 == 1:
                qtablep1.left_score = reward + 100
            elif actionp1 == 2:
                qtablep1.down_score = reward + 100
            elif actionp1 == 3:
                qtablep1.right_score = reward + 100
            
        db.session.commit()