import sat_interface

n = '~'
pp = ['A', 'B', 'C']

def tt(pp, kb2):
    ttp = []
    example_prob = sat_interface.KB(kb2)
    if example_prob.is_satisfiable():
        for x in range(len(pp)):
            if example_prob.test_literal(pp[x]) and (not example_prob.test_literal(n+pp[x])):
                ttp.append(x)
        return ttp
    else:
        return False

def print_answer(sol):
    name = ['Amy', 'Bob', 'Cal']
    namestring = ''
    if sol:
        if len(sol) >0:
            for index in sol:
                namestring += name[index]     
            print(namestring+ ' is/are (a) a truth-teller(s)')
        else: 
            print('No one tells the truth')
    else:
        print('not satisfiable')

def tt2():
    kb2 = ['A B C', '~A C', '~B C', 'C B', '~C B ~A']
    sol = tt(pp,kb2)
    print_answer(sol)
    
def tt3():
    kb3 = ['A B C', '~A ~C', 'C A', '~B A', '~B C', '~C B', '~A B ~C']
    sol = tt(pp,kb3)
    print_answer(sol)

def salt():
    #A is  Caterpillar, B is Bill the Lizard, C is Cheshire Cat
    #if A ate the salt: ~A, ~B, C
    #if B ate the salt: A, B, C
    #if C are the salt: ~A, ~b, ~C
    lieortruth = ['A B C', '~A ~B ~C']
    answer = ['Caterpillar ate the salt', 'Bill the Lizard ate the salt', 'Cheshire Cat ate the salt']

    example_prob = sat_interface.KB(lieortruth)
    if example_prob.test_literal('~A') and example_prob.test_literal('B') and example_prob.test_literal('C'):
        print(answer[0])
    elif example_prob.test_literal('A') and example_prob.test_literal('B') and example_prob.test_literal('C'):
        print(answer[1])
    elif example_prob.test_literal('~A') and example_prob.test_literal('~B') and example_prob.test_literal('~C'):
        print(answer[2])
    else:
        print('n/a')

def golf():
    #golfers in line: [A, B, C]
    #if the guy in the middle is Harry: A and ~B
    #if the guy in the middle is Dick: B
    #if the guy in the middle is Tom: C and B
    kb = ['A B C', '~A ~B ~C', '~A ~B', '~B ~C', '~A ~C']
    example_prob = sat_interface.KB(kb)
    if example_prob.test_literal('A') and example_prob.test_literal('~B'):
        #we know that Harry is in the middle
        if not example_prob.test_literal('A'):
            #we know that Dick is the first guy in the line:
            print('Dick, Harry, Tom')
        else:
            print('Tom, Harry, Dick')
    elif example_prob.test_literal('C') and example_prob.test_literal('C'):
         #Tom is in the middle:
        print('Harry, Tom, Dick')
    else:
        #Dick is in the middle:
        if example_prob.test_literal('A'):
            print('Tom, Dick, Harry')
        else:
            print('Harry, Dick, Tom')

def main():
    tt2()
    tt3()
    salt()
    golf()
    
if __name__ == '__main__':
    main()
