import random



class AI ():

    def __init__(self, id, login):
        self.login = login
        self.id = id
        self.eps = 0.95
        self.Q_table = []



    def set_board(self, board):
        self.board = board

    def exploration_step(self, position):
        possible_move = self.board.get_possible_move(position)
        
        i_random = random.randint(0, len(possible_move) - 1)

        self.board.positions[self.board.turn - 1] = possible_move[i_random]

        self.board.update_state()


    def greedy_step(self, state, position):
        actions = self.board.get_possible_move(position)

        vmin = None
        vi = None
        for i in range(len(actions)):
            action = actions[i]



        self.board.update_state()

    def get_state(self,action,state):
        return 
    

    def play(self, position, state):

        #if random.uniform(0, 1) < self.eps:
        if True:
            self.exploration_step(position)
        else:
            self.greedy_step(state, position)