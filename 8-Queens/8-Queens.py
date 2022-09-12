import math
import random
import sys

class Node:
    def __init__(self, initial=None):
        self.state = initial
        self.value = -1

    def getState(self):
        return self.state
    def setState(self,state):
        self.state = state
    def getValue(self):
        return self.value
    
    def calValue(self):  
    #number of queens in one row(if>1)+ number of of queens in one diagonal (if>1)
        row = 0
        diagonal = 0
        frequency = {}

        #number of queens in one row
        for number in self.state:
            if number in frequency:
                frequency[number] += 1
            else:
                frequency[number] = 1
        
        for x in frequency.values():
            if x > 1:
                row += (math.factorial(x)/(2*math.factorial(x-2)))
        
        # number of of queens in one diagonal
        frequency1 = {}
        frequency2 = {}
        for x in range(0,8):
            Sum = x+self.state[x]  # y=self.state[x]
            Sub = x-self.state[x] 
            if Sum in frequency1:
                frequency1[Sum] += 1
            else:
                frequency1[Sum] = 1
            if Sub in frequency2:
                frequency2[Sub] += 1
            else:
                frequency2[Sub] = 1

        for x in frequency1.values():
            if x > 1:
                diagonal += (math.factorial(x)/(2*math.factorial(x-2)))
        for y in frequency2.values():
            if y > 1:
                diagonal += (math.factorial(y)/(2*math.factorial(y-2)))
        self.value = row + diagonal

    def get_neighbor(self):    #return a list of Nodes
        neighbor = []
        for i in range(0,8):
            for j in range(1,9):
                new = self.state.copy()
                if new[i] == j: continue
                new[i] = j
                n = Node(new)
                n.calValue()  #set Value in function
                neighbor.append(n)
        return neighbor
    
    def random_neighbor(self):
        neighbors = self.get_neighbor()
        random.shuffle(neighbors)
        return neighbors.pop()

# hillclimb_sa
# That uses hill climbing with steepest-ascent to attempt to solve the problem. 
# Have your code detect a plateau or local maximum and give up if those are encountered.
def max_obj(nodes): # Input: a list of Nodes / return min node
    Min = math.inf
    min_node = None
    for x in nodes:
        if not nodes : raise Exception('no neighbor')
        if x.getValue() < Min:
            Min = x.getValue()
            min_node = x
    return min_node

def hillclimb_sa(init):
    step = 0
    current = Node(init)
    current.calValue()
    while True:
        neighbor = max_obj(current.get_neighbor())
        if neighbor.value >= current.value:
            return current.getValue(), step
        current = neighbor
        step += 1

# hillclimb_fc
# That implements first-choice hill climbing for the same problem.
def hillclimb_fc(init):
    step = 0
    n = Node(init)
    n.calValue()
    while True:
        neighbors = n.get_neighbor()
        random.shuffle(neighbors)
        next = neighbors.pop()
        while next.getValue() > n.getValue():   
            if not neighbors or step>100:  
                return n.getValue(), step
            next = neighbors.pop()
        n = next
        step += 1

# sim_anneal
# That implements simulated annealing for the problem. Choose your temperature and schedule.
def schedule(t):    
    if t>100:
        return 0
    else:
        return math.log10(100*(t+6))-4

def sim_anneal(init):
    n = Node(init)
    n.calValue()
    t = 1
    step = 0
    while True:
        T = schedule(t)  

        if T ==0: #max.
            return n.getValue(), step
        next = n.random_neighbor()  

        deltaE = next.getValue() - n.getValue()

        if deltaE < 0:   
            n = next
        elif random.random() <= math.exp(deltaE/T): 
            n = next
        t += 1
        step += 1

def generating():
    init = []
    for x in range(0,8):
        init.append(random.randint(1,8))
    return init

# Calculate the average number of steps overall for each of the algorithms to find a solution.
def main(argv):
    n = argv[1]
    sa = []
    fc = []
    anneal = []
    for i in range(n):
        print(i)
        init = generating()
        sa_result = hillclimb_sa(init)
        if sa_result[0] == 0:    #find soluton
            sa.append(sa_result[1])   
        fc_result = hillclimb_fc(init)
        if fc_result[0] == 0:
            fc.append(fc_result[1])
        ann_result = sim_anneal(init)
        if ann_result[0] == 0:
            anneal.append(ann_result[1])
    
    sa_avg = sum(sa)/len(sa)
    fc_avg = sum(fc)/len(fc)
    if len(anneal)==0:
        ann_avg = -1
        ann_suc = -1
    else:
        ann_avg = sum(anneal)/len(anneal)
        ann_suc = len(anneal)/n*100

    sa_suc = len(sa)/n*100
    fc_suc = len(fc)/n*100
    

    print('The average number of steps: \n' 
    + 'Hill climbing with steepest-ascent(step/percent of sucess): '+ str(sa_avg) +' / '+ str(sa_suc)
    +'\nFirst-choice hill climbing(step/percent of sucess): '+ str(fc_avg) +' / '+ str(fc_suc)
    + '\nSimulated annealing(step/percent of sucess): '+ str(ann_avg) +' / '+ str(ann_suc))


if __name__ == '__main__':
    main(sys.argv)
