import random
import copy
import sys
import time

WHITE = 1
BLACK = -1
EMPTY = 0
SIZE = 8
SKIP = "SKIP"

# choose a random move from among all legal moves on its turn
class RadomPlayer:
    def __init__(self, mycolor):
        self.color = mycolor

    def get_color(self):
        return self.color

    def make_move(self, state):
        #Given the state, returns a legal action for the agent to take in the state
        curr_move = None
        legals = actions(state)
        length = len(legals)
        r = random.randint(0,length-1)
        if r < 0 :
            curr_move = SKIP
        else:
            curr_move = legals[r]
        return curr_move

#Utility Function
def utility(state,mycolor):
    ut = 0
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board_array[i][j] != EMPTY:
                if state.board_array[i][j] == mycolor:
                    ut += 1
                else:
                    ut -= 1
    return ut

# Minimax Agent
class MinimaxPlayer:
    def __init__(self, mycolor, limit):
        self.color = mycolor
        self.limit = limit
    def get_color(self):
        return self.color

    def make_move(self, state):
        curr_move = None
        depth = 0
        legals = actions(state)
        maxN = float('-inf')
        for a in legals:
            N = self.Min_value(result(state,a),depth)
            if maxN < N:
                maxN = N
                curr_move = a
        return curr_move

    def Min_value(self,state,depth):
        depth += 1
        if terminal_test(state) or depth == self.limit:
            return utility(state,self.color)
        val = float('inf')
        for a in actions(state):
            val = min(val,self.Max_value(result(state,a), depth))
        return val

    def Max_value(self,state,depth):
        depth += 1
        if terminal_test(state) or depth == self.limit:
            return utility(state, self.color)
        val = float('-inf')
        for a in actions(state):
            val = max(val,self.Min_value(result(state,a),depth))
        return val

# Alpha-Beta Agent
class ABagnet:
    def __init__(self, mycolor, limit):
        self.color = mycolor
        self.limit = limit
    def get_color(self):
        return self.color

    def make_move(self, state):
        curr_move = None
        depth = 0
        alpha = float('-inf')
        beta = float('inf')
        legals = actions(state)
        maxN = float('-inf')
        for a in legals:
            N = self.Min_value(result(state,a),depth,alpha,beta)
            if maxN < N:
                maxN = N
                curr_move = a
        return curr_move

    def Min_value(self,state,depth,alpha,beta):
        depth += 1
        if terminal_test(state) or depth == self.limit:
            return utility(state,self.color)
        val = float('inf')
        for a in actions(state):
            val = min(val,self.Max_value(result(state,a), depth,alpha,beta))
            if val <= alpha:
                return val
            beta = max(beta,val)
        return val

    def Max_value(self,state,depth,alpha,beta):
        depth += 1
        if terminal_test(state) or depth == self.limit:
            return utility(state, self.color)
        val = float('-inf')
        for a in actions(state):
            val = max(val,self.Min_value(result(state,a),depth,alpha,beta))
            if val >= beta:
                return val
            alpha = min(alpha,val)
        return val


class OthelloState:  #unchanged
    def __init__(self, currentplayer, otherplayer, board_array = None, num_skips = 0):
        if board_array != None:
            self.board_array = board_array
        else:
            self.board_array = [[EMPTY] * SIZE for i in range(SIZE)]
            self.board_array[3][3] = WHITE
            self.board_array[4][4] = WHITE
            self.board_array[3][4] = BLACK
            self.board_array[4][3] = BLACK
        self.num_skips = num_skips
        self.current = currentplayer
        self.other = otherplayer

def player(state):  #unchanged
    return state.current

def actions(state): #unchanged
    '''Return a list of possible actions given the current state
    '''
    legal_actions = []
    for i in range(SIZE):
        for j in range(SIZE):
            if result(state, (i,j)) != None:
                legal_actions.append((i,j))
    if len(legal_actions) == 0:
        legal_actions.append(SKIP)
    return legal_actions

def result(state, action):  #unchanged
    '''Returns the resulting state after taking the given action
    (This is the workhorse function for checking legal moves as well as making moves)
    If the given action is not legal, returns None
    '''
    # first, special case! an action of SKIP is allowed if the current agent has no legal moves
    # in this case, we just skip to the other player's turn but keep the same board
    if action == SKIP:
        newstate = OthelloState(state.other, state.current, copy.deepcopy(state.board_array), state.num_skips + 1)
        return newstate

    if state.board_array[action[0]][action[1]] != EMPTY:
        return None

    color = state.current.get_color()
    # create new state with players swapped and a copy of the current board
    newstate = OthelloState(state.other, state.current, copy.deepcopy(state.board_array))

    newstate.board_array[action[0]][action[1]] = color
    
    flipped = False
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    for d in directions:
        i = 1
        count = 0
        while i <= SIZE:
            x = action[0] + i * d[0]
            y = action[1] + i * d[1]
            if x < 0 or x >= SIZE or y < 0 or y >= SIZE:
                count = 0
                break
            elif newstate.board_array[x][y] == -1 * color:
                count += 1
            elif newstate.board_array[x][y] == color:
                break
            else:
                count = 0
                break
            i += 1

        if count > 0:
            flipped = True

        for i in range(count):
            x = action[0] + (i+1) * d[0]
            y = action[1] + (i+1) * d[1]
            newstate.board_array[x][y] = color

    if flipped:
        return newstate
    else:  
        # if no pieces are flipped, it's not a legal move
        return None

def terminal_test(state): #unchanged
    '''Simple terminal test
    '''
    # if both players have skipped
    if state.num_skips == 2:
        return True

    # if there are no empty spaces
    empty_count = 0
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board_array[i][j] == EMPTY:
                empty_count += 1
    if empty_count == 0:
        return True
    return False

def display(state):  #unchanged
    '''Displays the current state in the terminal window
    '''
    print('  ', end='')
    for i in range(SIZE):
        print(i,end='')
    print()
    for i in range(SIZE):
        print(i, '', end='')
        for j in range(SIZE):
            if state.board_array[j][i] == WHITE:
                print('W', end='')
            elif state.board_array[j][i] == BLACK:
                print('B', end='')
            else:
                print('-', end='')
        print()

def display_final(state): 
    '''Displays the score and declares a winner (or tie)
    '''
    wcount = 0
    bcount = 0
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board_array[i][j] == WHITE:
                wcount += 1
            elif state.board_array[i][j] == BLACK:
                bcount += 1

    print("Black: " + str(bcount))
    print("White: " + str(wcount))
    if wcount > bcount:
        print("White wins")
        return False
    elif wcount < bcount:
        print("Black wins")
        return True
    else:
        print("Tie")
        return False

def play_game(p1,limit):   
    '''Plays a game with two players. By default, uses two humans
    '''
    if p1 == 'Minimax':
        p1 = MinimaxPlayer(BLACK,limit)
    elif p1 == 'AB':
        p1 = ABagnet(BLACK,limit)
    p2 = RadomPlayer(WHITE)

    s = OthelloState(p1, p2)
    total = 0
    step = 0
    while True:
        tic = time.time()
        action = p1.make_move(s)
        toc = time.time()
        take = toc-tic
        step += 1
        total += take
        print(take, 's')
        s = result(s, action)
        display(s)
        if terminal_test(s):
            print("Game Over")
            display(s)
            return display_final(s), total/step  
        action = p2.make_move(s)
        s = result(s, action)
        display(s)
        if terminal_test(s):
            print("Game Over")
            display(s)
            return display_final(s), total/step

def main(argv):
    agent = argv[1]  # Minimax or AB
    game = 10   #how many games to play
    limit = 5  #depth limit
    win = 0
    rest = 0
    time = 0
    for n in range(game):   #change
        Result = play_game(agent,limit)
        if Result[0]:
            win += 1
        else:
            rest += 1
        time += Result[1]
        
    print('Winning rate is ', win/(win+rest))
    print('average time per step is ', time/game)


if __name__ == '__main__':
    main(sys.argv)
