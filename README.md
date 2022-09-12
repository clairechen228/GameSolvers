# Game_Solvers[^1]
Solving strategy and logic games using AI

## Classic Search: 8-Puzzle
The 8-Puzzle is a type of sliding tile puzzle consisting of a 3x3 grid of numbered tiles, with one tile (#9) missing. The object of the puzzle is to get the tiles in a particular order, subject to the constraints of physically sliding one tile at a time into the open space.

The program takes one command-line argument: the initial state
The following state is our goal

| 1 | 2 | 3 |
| - | - | - |
| 8 | . | 4 |
| 7 | 6 | 5 |

- Uninformed Search: Depth-First Search, Depth-Limited Search, Iterative Deepening
- Informed Search: Heuristics, A* Search

The program returns the solution and time taken for each algorithm. 



## Classic Search: 8-Queens Problem
This is the problem of placing eight chess queens on an 8×8 chessboard so that no two queens threaten each other; thus, a solution requires that no two queens share the same row, column, or diagonal. 


- Hill climbing with steepest-ascent
- First-choice hill climbing
- Simulated annealing 

Generate a large number of random initial states and run each of the algorithms on those states. Calculate the average number of steps overall for each of the algorithms to find a solution.

Testing:

`python 8-Queens.py 2000`

input: 2000 => generate 2000 random initial states)

> The average number of steps:

> Hill climbing with steepest-ascent(step/percent of sucess): 3.9764309764309766 / 14.85

> First-choice hill climbing(step/percent of sucess): 41.23354321694333 / 87.35000000000001

> Simulated annealing(step/percent of sucess): 93.0 / 8.15



## Adversarial Search: Othello

Othello, also known by its non-trademark name reversi, is a strategy game for two players.

- Create a **MinimaxPlayer** class that implements the minimax search algorithm to decide its moves.
- Create an **AlphabetaPlayer** class that implements minimax search with alpha-beta pruning to decide its moves.

default parameters:
number of games = 10 
depth limit = 5

Testing:

Minimax Agent: `python3 othello.py Minimax`

> Winning rate is  0.8
> average time per step is  18.27

Alpha-Beta Agent: `python3 othello.py AB`

> Winning rate is  1.0
> average time per step is  9.01


## Propositional Logic: Basic Logic Games

1. Liars and Truth-tellers II

   Three people, Amy, Bob, and Cal, are each either a liar or a truth-teller. Assume that liars always lie, and truth-tellers always tell the truth.

   - Amy says, "Cal and I are truthful."

   - Bob says, "Cal is a liar."

   - Cal says, "Bob speaks the truth or Amy lies."

2. Liars and Truth-tellers III

   Three people, Amy, Bob, and Cal, are each either a liar or a truth-teller. Assume that liars always lie, and truth-tellers always tell the truth.

   - Amy says, "Cal is not honest."
   
   - Bob says, "Amy and Cal never lie."
   
   - Cal says, "Bob is correct."

3. Robbery and a Salt

   The salt has been stolen! Well, it was found that the culprit was either the Caterpillar, Bill the Lizard or the Cheshire Cat. The three were tried and made the following statements in court:

   - CATERPILLAR: Bill the Lizard ate the salt.
   
   - BILL THE LIZARD: That is true!
   
   - CHESHIRE CAT: I never ate the salt.
   
   - As it happened, at least one of them lied and at least one told the truth. Who ate the salt?

4. An honest name

   Three golfers named Tom, Dick, and Harry are walking to the clubhouse.

   - The first man in line says, "The guy in the middle is Harry."
   
   - The man in the middle says, "I’m Dick."
   
   - The last man says, "The guy in the middle is Tom."
   
   - Tom, the best golfer of the three, always tells the truth.
   
   - Dick sometimes tells the truth, while Harry, the worst golfer, never does.

   Figure out who is who.

Answers:
> Cal is/are (a) a truth-teller(s)

> Amy is/are (a) a truth-teller(s)

> Caterpillar ate the salt

> Tom, Harry, Dick


## Propositional Logic: Clue Game Reasoner

Use propositional logic and a satisfiability reasoning tool to solve a a game of clue.

The main basis of the game is deduction

- The suspects are: Miss Scarlet (sc), Colonel Mustard (mu), Miss White (wh), Mr. Green (gr), Miss Peacock (pe), Professor Plum (pl)

- The weapons are: Knife (kn), Candlestick (ca), Revolver (re), Rope (ro), Pipe (pi), Wrench (wr)

- The rooms are: Hall (ha), Lounge (lo), Dining Room (di), Kitchen (ki), Ballroom (ba), Conservatory (co), Billiards Room (bi), Library (li), Study (st)

- Confusing our terminology is the fact that in the game, the players play as suspects. So there is a card named "Miss Scarlet" but also one of the players is playing as "Miss Scarlet".

## First-Order Logic: Prolog

Use First Order Logic in the form of prolog programs in order to represent knowledge.

Build the program online at: https://swish.swi-prolog.org/ .


[^1]: Problem sets and partial codes are from UMN Fall 2020 CSCI 5511 course material
