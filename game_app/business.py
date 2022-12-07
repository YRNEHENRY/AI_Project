from game_app.ai import AI


class User():

    def __init__(self,login):
        self.login = login


class Human(User):

    def __init__(self, login, password, email, name, first_name):
        super().__init__(login)
        self.password = password
        self.email = email
        self.name = name
        self.first_name = first_name


class Board():

    def __init__(self, id, size, player_1, player_2):
        self.id = id
        self.size = size
        self.state_board = "1" + "0"*((size * size) - 2) + "2"
        self.turn = 1
        self.position_p1 = [0,0]
        self.position_p2 = [self.size-1, self.size-1]
        self.positions = [self.position_p1, self.position_p2]
        self.player_1 = player_1
        self.player_2 = player_2
        self.players = [player_1, player_2]

    def play(self):
        is_done = self.is_done()[0]

        while isinstance(self.players[self.turn - 1], AI) and not is_done:
            self.players[self.turn - 1].play(self.positions[self.turn - 1], self.state_board)

            is_done = self.is_done()[0]

        return self.is_done()

    def move_player(self, movement):

        if movement == "UP":
            self.positions[self.turn - 1][0] -= 1
        elif movement == "DOWN":
            self.positions[self.turn - 1][0] += 1
        elif movement == "LEFT":
            self.positions[self.turn - 1][1] -= 1
        elif movement == "RIGHT":
            self.positions[self.turn - 1][1] += 1

        self.update_state()
        return self.is_done()

    def get_possible_move(self, position):
        possible_move = []
        opponent_turn = 2 if self.turn == 1 else 1


        if (position[0] - 1) >= 0 and self.get_tab_state()[position[0] - 1][position[1]] != opponent_turn:
            possible_move.append([position[0] - 1, position[1]])
        
        if (position[1] - 1) >= 0 and self.get_tab_state()[position[0]][position[1] - 1] != opponent_turn:
            possible_move.append([position[0], position[1] - 1])
        
        if (position[0] + 1) <= self.size-1 and self.get_tab_state()[position[0] + 1][position[1]] != opponent_turn:
            possible_move.append([position[0] + 1, position[1]])

        if (position[1] + 1) <= self.size-1 and self.get_tab_state()[position[0]][position[1] + 1] != opponent_turn:
            possible_move.append([position[0], position[1] + 1])

        return possible_move

    def get_tab_state(self):
        state = []
        i = 0
        for y in range(0, self.size):
            line = []
            for j in range(0, self.size):
                line.append(int(self.state_board[i]))
                i +=1
            state.append(line)
        return state

    def state_to_string(self, state):
        str_sate = ''
        for line in state:
            for s in line:
                str_sate += str(s)
        return str_sate
        

    


    def update_state(self):
        state = self.get_tab_state()
        opponent = 2 if self.turn == 1 else 1

        x = self.positions[self.turn - 1][0]
        y = self.positions[self.turn - 1][1]
        if state[x][y] != opponent:
            state[x][y] = self.turn
            self.state_board = self.state_to_string(state)
            self.turn = 2 if self.turn == 1 else 1
        else:
            #triche
            self.state_board = "0" + "0"*((self.size * self.size) - 2) + "0"
        

    def update_enclosure(self, enclosure):
        x = 0
        y = 0
        state = self.get_tab_state()
        for case in enclosure:
            
            x = case[0]
            y = case[1]
            state[x][y] = self.turn

        self.state_board = self.state_to_string(state)



    def check_enclosure(self):
        neutral_cases = self.get_neutral_cases(self.positions[self.turn - 1])
        enclosures = []
        enclosure = []
        for case in neutral_cases:
            enclosure.append(case)
            response = self.check_neighbour(enclosure, case)
            if response == 0:
                enclosure.clear()
            else:
                enclosures = enclosures + enclosure

        
        
        self.update_enclosure(enclosures)
        return self.is_done()
        




        
    def check_neighbour(self, enclosure, position):


        opponent = 2 if self.turn == 1 else 1
        
        neighbours = self.get_all_neighbours(position)
        i = 0
        while i < len(neighbours):
            if self.get_tab_state()[neighbours[i][0]][neighbours[i][1]] == self.turn:
                del neighbours[i]
                i -= 1
            elif neighbours[i] in enclosure:

                del neighbours[i]

                i -= 1
            i += 1

        i = 0
        while i < len(neighbours):
            if self.get_tab_state()[neighbours[i][0]][neighbours[i][1]] == opponent:
                enclosure.clear()
                return 0
            i += 1
        response = 1
        if i == len(neighbours):
            if position not in enclosure:
                enclosure.append(position)
            for neighbour in neighbours:
                response = self.check_neighbour(enclosure, neighbour)
                if response == 0:
                    break

            return response     


    def get_all_neighbours(self, position):
        neighbours = []

        if (position[0] - 1) >= 0:
            neighbours.append([position[0] - 1, position[1]])
        
        if (position[1] - 1) >= 0:
            neighbours.append([position[0], position[1] - 1])
        
        if (position[0] + 1) <= self.size-1:
            neighbours.append([position[0] + 1, position[1]])

        if (position[1] + 1) <= self.size-1:
            neighbours.append([position[0], position[1] + 1])

        return neighbours
 

    def get_neutral_cases(self, position):
        neutral_cases = self.get_possible_move(position)

        i = 0
        while i < len(neutral_cases):
            if self.get_tab_state()[neutral_cases[i][0]][neutral_cases[i][1]] == 1 or self.get_tab_state()[neutral_cases[i][0]][neutral_cases[i][1]] == 2:
                del neutral_cases[i]
                i -= 1
            i +=1

        return neutral_cases
        

    def is_done(self):
        is_done = False
        winner = "Nobody"
        for i in range(0, self.size):
            if 0 in self.get_tab_state()[i]:
                return is_done, winner

        is_done = True
        nb_1 = self.state_board.count('1')
        nb_2 = self.state_board.count('2')
        if nb_1 > nb_2:
            winner = self.player_1.first_name if not isinstance(self.player_1, AI) else "AI n°1"
        elif nb_1 < nb_2:
            winner = self.player_2.first_name if not isinstance(self.player_2, AI) else "AI n°2"
        return is_done, winner


def map_AI(ai):
    login = 'AI n°', ai.id
    return AI(ai.id, login)
