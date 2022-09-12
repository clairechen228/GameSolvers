import sat_interface

# Initialize important variables

CASE_FILE = "CF"
POSSIBLE_PLAYERS = ["SC", "MU", "WH", "GR", "PE", "PL"]
POSSIBLE_CARD_LOCATIONS = POSSIBLE_PLAYERS + [CASE_FILE]
SUSPECTS = ["mu", "pl", "gr", "pe", "sc", "wh"]
WEAPONS = ["kn", "ca", "re", "ro", "pi", "wr"]
ROOMS = ["ha", "lo", "di", "ki", "ba", "co", "bi", "li", "st"]
CARDS = SUSPECTS + WEAPONS + ROOMS

class ClueGameReasoner:
    '''This class represents a clue game reasoner, a tool that can be used
    to track the information during a game of clue and deduce information
    about the game. (Hopefully help you win!)
    '''

    def __init__(self, player_order, card_nums = None):
        '''init for a particular clue game.
            player_order is a list of strings of players in the order that they
            are sitting around the table. Note: This may not include all the suspects,
            as there may be fewer than 6 players in any given game.
            card_nums is a list of numbers of cards in players' hands. It is
            possible that different players have different numbers of cards!
        '''
        self.players = player_order
        clauses = []

        # Each card is in at least one place (including case file).
        # If you want to change the string representation of the variables,
        #   go ahead!
        for c in CARDS:
            clause = ""
            for p in POSSIBLE_CARD_LOCATIONS:
                clause += c + "_" + p + " "
            clauses.append(clause)

        # A card cannot be in two places.
        for c in CARDS:
            for i in range(len(POSSIBLE_CARD_LOCATIONS)):
                if i+1 == len(POSSIBLE_CARD_LOCATIONS):
                    break
                for j in range(i+1,len(POSSIBLE_CARD_LOCATIONS)):
                    clause = "~" + c + "_" + POSSIBLE_CARD_LOCATIONS[i] + " " + "~" + c + "_" + POSSIBLE_CARD_LOCATIONS[j]
                    clauses.append(clause)

        # At least one card of each category is in the case file.
        category=[SUSPECTS, WEAPONS,ROOMS]
        for cat in category:
            clause = ""
            for c in cat:
                clause += c + "_" + CASE_FILE + " "
            clauses.append(clause)

        # No two cards in each category can both be in the case file.
        for cat in category:
            for i in range(len(cat)):
                if i+1 == len(cat):
                    break
                for j in range(i+1, len(cat)):
                    clause = "~" + cat[i] + "_" + CASE_FILE + " " + "~" + cat[j] + "_" + CASE_FILE
                    clauses.append(clause)

        self.KB = sat_interface.KB(clauses)

    def add_hand(self, player_name, hand_cards):
        '''Add the information about the given player's hand to the KB'''
        for c in hand_cards:
            clause = c + "_" + player_name
            self.KB.add_clause(clause)

    def suggest(self, suggester, c1, c2, c3, refuter, cardshown = None):
        '''Add information about a given suggestion to the KB'''
        start = self.players.index(suggester)
        if refuter != None:
            stop = self.players.index(refuter)
            py = self.players[stop]
            #if it's not your turn
            if cardshown == None:
                clause = c1 + "_" + py + " " + c2 + "_" + py + " " + c3 + "_" + py + " "
                self.KB.add_clause(clause)
            else:  #my turn
                clause = cardshown + "_" + py
                self.KB.add_clause(clause)
        else: #cards are either in the suggester's hand or in the case file
            stop = start
            card = [c1,c2,c3]
            for c in card:
                clause = c + "_" + suggester + " " + c + "_" + CASE_FILE
                self.KB.add_clause(clause)
            
        x = (start+1)%len(self.players)
        #none of the suggested cards are in other players' hand
        while x != stop:
            py = self.players[x]
            clause = "~" + c1 + "_" + py   #a little but lazy...
            self.KB.add_clause(clause)
            clause = "~" + c2 + "_" + py
            self.KB.add_clause(clause)
            clause = "~" + c3 + "_" + py
            self.KB.add_clause(clause)
            x = (x+1)%len(self.players)
        

    def accuse(self, accuser, c1, c2, c3, iscorrect):
        '''Add information about a given accusation to the KB'''
        card = [c1,c2,c3]
        # correct
        if iscorrect:
            for c in card:
                clause = c + "_" + CASE_FILE
                self.KB.add_clause(clause)
        else: #incorrect
            clause = "~" + c1 + "_" + CASE_FILE +  "~" + c2 + "_" + CASE_FILE +  "~" + c3 + "_" + CASE_FILE
            self.KB.add_clause(clause)



    def print_notepad(self):
        print("Clue Game Notepad:")
        for player in self.players:
            print('\t'+ player, end='')
        print('\t'+ CASE_FILE)
        for card in CARDS:
            print(card,'\t',end='')
            for player in self.players:
                print(self.get_test_string(card + "_" + player),'\t',end='')
            print(self.get_test_string(card + "_" + CASE_FILE))

    def get_test_string(self, variable):
        '''test a variable and return 'Y', 'N' or '-'
            'Y' if this positive literal is entailed by the KB
            'N' if its reverse is entailed
            '-' if neither is entailed
            additionally, the entailed literal (if any) will be added to the KB
        '''
        res = self.KB.test_add_variable(variable)
        if res == True:
            return 'Y'
        elif res == False:
            return 'N'
        else:
            return '-'


def play_clue_game1():
    # the game begins! add players to the game
    cgr = ClueGameReasoner(["SC", "MU", "WH", "GR", "PE", "PL"])

    # Add information about our hand: We are Miss Scarlet,
    # and we have the cards Mrs White, Library, Study
    cgr.add_hand("SC",["wh", "li", "st"])

    # We go first, we suggest that it was Miss Scarlet,
    # with the Rope in the Lounge. Colonel Mustard refutes us
    # by showing us the Miss Scarlet card.
    cgr.suggest("SC", "sc", "ro", "lo", "MU", "sc")

    # Mustard takes his turn. He suggests that it was Mrs. Peacock,
    # in the Dining Room with the Lead Pipe.
    # Mrs. White and Mr. Green cannot refute, but Mrs. Peacock does.
    cgr.suggest("MU", "pe", "pi", "di", "PE", None)

    # Mrs. White takes her turn
    cgr.suggest("WH", "mu", "re", "ba", "PE", None)

    # and so on...
    cgr.suggest("GR", "wh", "kn", "ba", "PL", None)
    cgr.suggest("PE", "gr", "ca", "di", "WH", None)
    cgr.suggest("PL", "wh", "wr", "st", "SC", None)
    cgr.suggest("SC", "pl", "ro", "co", "MU", "pl")
    cgr.suggest("MU", "pe", "ro", "ba", "WH", None)
    cgr.suggest("WH", "mu", "ca", "st", "GR", None)
    cgr.suggest("GR", "pe", "kn", "di", "PE", None)
    cgr.suggest("PE", "mu", "pi", "di", "PL", None)
    cgr.suggest("PL", "gr", "kn", "co", "WH", None)
    cgr.suggest("SC", "pe", "kn", "lo", "MU", "lo")
    cgr.suggest("MU", "pe", "kn", "di", "WH", None)
    cgr.suggest("WH", "pe", "wr", "ha", "GR", None)
    cgr.suggest("GR", "wh", "pi", "co", "PL", None)
    cgr.suggest("PE", "sc", "pi", "ha", "MU", None)
    cgr.suggest("PL", "pe", "pi", "ba", None, None)
    cgr.suggest("SC", "wh", "pi", "ha", "PE", "ha")

    # aha! we have discovered that the lead pipe is the correct weapon
    # if you print the notepad here, you should see that we know that
    # it is in the case file. But it looks like the jig is up and
    # everyone else has figured this out as well...

    cgr.suggest("WH", "pe", "pi", "ha", "PE", None)
    cgr.suggest("PE", "pe", "pi", "ha", None, None)
    cgr.suggest("SC", "gr", "pi", "st", "WH", "gr")
    cgr.suggest("MU", "pe", "pi", "ba", "PL", None)
    cgr.suggest("WH", "pe", "pi", "st", "SC", "st")
    cgr.suggest("GR", "wh", "pi", "st", "SC", "wh")
    cgr.suggest("PE", "wh", "pi", "st", "SC", "wh")

    # At this point, we are still unsure of whether it happened
    # in the kitchen, or the billiard room. printing our notepad
    # here should reflect that we know all the other information
    cgr.suggest("PL", "pe", "pi", "ki", "GR", None)

    # Aha! Mr. Green must have the Kitchen card in his hand
    print('Before accusation: should show a single solution.')
    cgr.print_notepad()
    print()
    cgr.accuse("SC", "pe", "pi", "bi", True)
    print('After accusation: if consistent, output should remain unchanged.')
    cgr.print_notepad()

def play_clue_game2():
    '''This game recorded by Brooke Taylor and played by Sean Miller,
    George Ashley, Ben Limpich, Melissa Kohl and Andy Exley. Thanks to all!
    '''
    cgr = ClueGameReasoner(["SC","MU","WH","GR","PE","PL"])
    cgr.add_hand("WH",["kn","ro","ki"])

    # all suggestions
    cgr.suggest("MU", "mu", "di", "pi", "PE", None)
    cgr.suggest("WH", "pl", "ca", "ba", "PE", "ba")
    cgr.suggest("GR", "pe", "ba", "ro", "PE", None)
    cgr.suggest("PE", "ki", "sc", "re", "WH", "ki")
    cgr.suggest("SC", "wh", "st", "ro", "MU", None)
    cgr.suggest("MU", "lo", "pl", "kn", "WH", "kn")
    cgr.suggest("WH", "li", "re", "pl", "GR", "re")
    cgr.suggest("PE", "st", "sc", "wr", "MU", None)
    cgr.suggest("PL", "bi", "gr", "wr", "SC", None)
    cgr.suggest("MU", "co", "pe", "ca", "GR", None)
    cgr.suggest("PE", "lo", "mu", "ro", "PL", None)
    cgr.suggest("PL", "co", "mu", "wr", "GR", None)
    cgr.suggest("SC", "ha", "ro", "pe", "WH", "ro")
    cgr.suggest("MU", "pe", "pi", "ba", "PE", None)
    cgr.suggest("WH", "sc", "pi", "ha", "PE", "sc")
    cgr.suggest("PE", "pl", "wr", "co", "PL", None)
    cgr.suggest("PL", "ba", "mu", "wr", "PE", None)
    cgr.suggest("SC", "st", "pi", "pe", "MU", None)
    cgr.suggest("WH", "ca", "st", "gr", "SC", "ca")
    cgr.suggest("GR", "sc", "ki", "wr", "PE", None)
    cgr.suggest("PE", "ki", "mu", "wr", "WH", "ki")
    cgr.suggest("MU", "st", "gr", "wr", "SC", None)
    cgr.suggest("WH", "gr", "ha", "wr", "SC", "ha")
    cgr.suggest("PE", "pe", "st", "wr", "MU", None)
    cgr.suggest("PL", "ki", "gr", "wr", "SC", None)
    cgr.suggest("SC", "li", "wr", "pe", "PL", None)
    cgr.suggest("WH", "di", "pe", "wr", None, None)

    cgr.print_notepad()
    # final accusation
    cgr.accuse("WH", "di", "pe", "wr", True)
    # Brooke wins!

def play_clue_game3():
 
    cgr = ClueGameReasoner(["SC","MU","WH","GR","PE","PL"])
    cgr.add_hand("PE",["sc","mu","ba"])
    cgr.suggest("MU", "mu", "di", "pi", "PE", "mu")
    cgr.suggest("WH", "pl", "ca", "ba", "PE", "ba")
    cgr.suggest("GR", "pe", "ba", "ro", "PE", "ba")
    cgr.suggest("PE", "ki", "sc", "re", "WH", "ki")
    cgr.suggest("SC", "wh", "st", "ro", "MU", None)
    cgr.suggest("MU", "lo", "pl", "kn", "WH", None)
    cgr.suggest("WH", "li", "re", "pl", "GR", None)
    cgr.suggest("PE", "st", "sc", "wr", "MU", "st")
    cgr.suggest("PL", "bi", "gr", "wr", "SC", None)
    cgr.suggest("MU", "co", "pe", "ca", "GR", None)
    cgr.suggest("PE", "lo", "mu", "ro", "PL", "lo")
    cgr.suggest("PL", "co", "mu", "wr", "GR", None)
    cgr.suggest("SC", "ha", "ro", "pe", "WH", None)
    cgr.suggest("MU", "pe", "pi", "ba", "PE", "ba")
    cgr.suggest("WH", "sc", "pi", "ha", "PE", "sc")
    cgr.suggest("PE", "pl", "wr", "co", "PL", "pl")
    cgr.suggest("PL", "ba", "mu", "wr", "PE", "ba")
    cgr.suggest("SC", "st", "pi", "pe", "MU", None)
    cgr.suggest("WH", "ca", "st", "gr", "SC", None)
    cgr.suggest("GR", "sc", "ki", "wr", "PE", "sc")
    cgr.suggest("PE", "ki", "mu", "wr", "WH", "ki")
    cgr.suggest("MU", "st", "gr", "wr", "SC", None)
    cgr.suggest("WH", "gr", "ha", "wr", "SC", None)
    cgr.suggest("PE", "pe", "st", "wr", "MU", None)
    cgr.suggest("PL", "ki", "gr", "wr", "SC", None)
    cgr.suggest("SC", "li", "wr", "pe", "PL", None)

    # right before Mrs. White ends the game, I still
    # don't know what room it is in. :(
    cgr.print_notepad()
    cgr.suggest("WH", "di", "pe", "wr", None, None)
    cgr.accuse("WH", "di", "pe", "wr", True)

# Change which game gets called down here if you want to test
# other games
if __name__ == '__main__':
    # play_clue_game1()
    # play_clue_game2()
    play_clue_game3()
