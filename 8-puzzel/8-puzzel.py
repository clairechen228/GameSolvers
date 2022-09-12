import sys
import time


class Node:
    #initial = 120843765
    def __init__(self, initial=None):
        self.state = list(str(initial))
        self.parent = None
        self.action = None
        self.path_cost = 0
    
    #maybe unnecessary
    def getState(self):
        return self.state
    def getParent(self):
        return self.parent
    def getAction(self):
        return self.action
    def getPC(self):
        return self.path_cost
    def setState(self,state):
        self.state = state
    def setParent(self,parent):
        if isinstance(parent,Node):
            self.parent = parent
    def setAction(self,action):
        self.action = action
    def setPC(self,pc):
        self.path_cost = pc+1

# Use the actions Right, Left, Up, and Down, which correspond to 
# how a tile is moved into the blank space to generate the next state
# return possible actions
    def find_blank(self):
        for x in range(0,len(self.state)):
            if self.state[x] == '0':
                return x  
    
    def swap(self,a,b):
        state = self.getState()
        state = state.copy()
        t = state[a]
        state[a] = state[b]
        state[b] = t
        return state
    
    def get_actions(self):
        blank = self.find_blank()
        if blank<0 or blank>8:
            raise Exception('WRONG BLANK')
        if blank == 0:
            return 'Left','Up'
        elif blank == 1:
            return 'Right','Left','Up'
        elif blank == 2:
            return 'Right','Up'
        elif blank == 3:
            return 'Down','Left','Up'
        elif blank == 4:
            return 'Down','Left','Up','Right'
        elif blank == 5:
            return 'Down','Right','Up'
        elif blank == 6:
            return 'Down','Left'
        elif blank == 7:
            return 'Down','Left','Right'
        elif blank == 8:
            return 'Down','Right'
    
# return child state
    def result(self,action,state): 
        blank = self.find_blank()
        if action == 'Left':
            newstate = self.swap(blank,blank+1)
        elif action == 'Right':
            # print(state)
            newstate = self.swap(blank, blank-1)
            # print(state)
        elif action == 'Down':
            newstate = self.swap(blank, blank-3)
        elif action == 'Up': 
            newstate = self.swap(blank, blank+3)
        else:
            raise Exception('WRONG ACTION')
        return newstate

# Given parent node, automatically generate all its child nodes
    def getChildren(self,parent):
        children = []
        actions = parent.get_actions()   
        for act in actions:
            child = Node()
            child.setAction(act)
            child.setPC(parent.getPC())   #not sure if it works
            state = parent.result(act,parent.getState())
            # print(parent.getState())
            # print(state)
            child.setState(state)
            child.setParent(parent)  #not sure if it works
            children.append(child)
        return children

def solution(explored,leaf):
    sol = []
    for node in explored:
        sol.append(node.getAction())
    sol.append(leaf.getAction())
    sol.remove(None)
    return sol

# Depth-First Search
# Write a version of the book's graph_search function that implements depth-first search for this problem. 
#return a set of actions
def DFS(init_state):
    frontier = []
    frontier_state = []
    init = Node(init_state)
    frontier.append(init)
    frontier_state.append(init.getState())
    explored = []
    explored_state = []

    while(True):
        if not len(frontier):
            return None
        leaf = frontier.pop()
        frontier_state.pop()
     
        if leaf.getState() == goal:
            return solution(explored,leaf)

        explored.append(leaf)
        explored_state.append(leaf.getState())
        # print(explored_state)
      
        for child in leaf.getChildren(leaf):
            if child.getState() not in frontier_state and child.getState() not in explored_state:   #### check the identity of 'stste' or 'Node'
                frontier.append(child) 
                frontier_state.append(child.getState())

# Depth-Limited Search
def solution2(init,leaf):
    sol = []
    while leaf != init:
        a = leaf.getAction()
        sol.insert(0,a)
        leaf = leaf.getParent()
    return sol

def DLS(init_state, limit):
    frontier = []
    frontier_state = []
    init = Node(init_state)
    frontier.append(init)
    frontier_state.append(init.getState())

    while(True):
        if not len(frontier):
            return None
        leaf = frontier.pop()
        frontier_state.pop()
     
        if leaf.getState() == goal:
            return solution2(init,leaf)
      
        for child in leaf.getChildren(leaf):
            if child.getState() not in frontier_state and child.getPC() <= limit :   
                frontier.append(child) 
                frontier_state.append(child.getState())

#Iterative Deepening
def ID(init_state):
    limit = 0
    while(True):
        sol = DLS(init_state,limit)
        if sol != None:
            return sol
        else:
            limit +=1
 
# Heuristics
# counts the number of tiles in the wrong location
def num_wrong_tiles(state): 
    wrongN = 0
    for tile in range(0,len(state)):
        if state[tile] != goal[tile] and state[tile] != '0':
            wrongN +=1      
    return wrongN

# Calculates the total manhattan distance (sum of the horizontal and vertical distances) for all tiles to move to their correct locations)
def manhattan_distance (state): 
    dis = 0
    for x in range(1,len(state)):
        a = state.index(str(x))
        b = goal.index(str(x))
        c = abs(a-b)%3
        d = (abs(a-b)-c)//3
        dis = dis + c + d
    return dis

# A* Search
# heuristic: num_wrong_tiles(state) & manhattan_distance (state)
def find_it(frontier, state):
    for x in frontier:
        node = x.get('node', None)
        if node.getState == state:
            return x

def astar(heuristic, init_state):
    frontier = []
    init = Node(init_state)
    frontier.append({'value':heuristic(init.getState()) ,'node':init})
    explored_state = []

    while(True):
        if not len(frontier):
            return None
        leaf_dic = frontier.pop(0)  #priority queue
        leaf = leaf_dic['node']
        leaf_num = leaf_dic['value']
     
        if leaf.getState() == goal:
            return solution2(init,leaf)  

        explored_state.append(leaf.getState())
      
        for child in leaf.getChildren(leaf):
            if find_it(frontier,child.getState()):
                old = find_it(frontier,child.getState())
                value = heuristic(child.getState())
                if value < old.get('value'):
                    frontier.remove(old)
                    frontier.append({'value': value,'node':child})
            elif child.getState() not in explored_state:   
                f_value = leaf_num + heuristic(child.getState())
                frontier.append({'value':f_value,'node':child}) 
        frontier.sort(key=lambda x: x['value'])

def visualize(state):
    space = '   '
    line = '\n'
    grid = line+state[0]+space+state[1]+space+state[2]+line+state[3]+space+state[4]+space+state[5]+line+state[6]+space+state[7]+space+state[8]
    print(grid)

# The program should then solve from this given state using iterative deepening, 
# A* with num_wrong_tiles, and A* with manhattan_distance, reporting its answer and time taken for each. 
def main(argv):
    init_state = argv[1]
    goal = 123804765
    goal = list(str(goal))

    start_time = time.time()
    sol_ID = ID(init_state)
    end_time = time.time()
    a = (end_time-start_time)
    ID_ans = '1. Iterative Deepening: '+str(sol_ID)+' ;execution time: {}'

    start_time = time.time()
    sol_N = astar(num_wrong_tiles,init_state)
    end_time = time.time()
    b = (end_time-start_time)
    N = '\n2. A* with wrong tiles heuristic: '+str(sol_N)+' ;execution time: {}'

    start_time = time.time()
    sol_M = astar(manhattan_distance,init_state)
    end_time = time.time()
    c = (end_time-start_time)
    M = '\n3. A* with Manhattan distance heuristic: '+str(sol_M)+' ;execution time: {}'

    print(ID_ans.format(a) + N.format(b) + M.format(c))
 

if __name__ == '__main__':
    main(sys.argv)
