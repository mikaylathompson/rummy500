# Rummy 500 (simplified)
import random
import rummyAI

# Game
def runGame():
    print "New Game."
    # Get players
    players = raw_input("Enter player names, comma seperated. \nStart name with AI if you'd like a computer player.\n").split(', ')
    # Start with zero scores
    scores = {p:0 for p in players}
    aiPlayers = {p:False for p in players if p[0:2] != 'AI'}
    for p in players:
        if p[0:2] == 'AI':
            aiPlayers[p] = rummyAI.PlayerAI()

    while (max(scores.values()) < 500):
        raw_input("Ready for next round?  ")
        # play round
        newScores = playRound(players, aiPlayers)
        print "This round:", newScores
        # update scores
        for p in players:
            scores[p] += newScores[p]
        print "Total:", scores
    print "Game over!!"
    print "Final scores:", scores


def playRound(players, aiPlayers):
    # Deal cards
    state = deal(players)
    table = {p:[] for p in players}
    while True:
        for p in players:
            print "\n\n\n",p+"'s Turn\n\n\n"
            state[p].sort()
            print p+"'s Hand:", state[p]
            print "Table:", table
            # ask to select draw/discard
            if not aiPlayers[p]:
                humanTurn(p, players, state, table)
            else:
                aiTurn(aiPlayers[p], p, players, state, table)

            # check that cards remain
            if len(state[p]) == 0:
                print "\nRound finished!\n\n"
                return calculateScores(players, state, table)

def aiTurn(ai, p, players, state, table):
    # give state[p] and table
    ai.setState(state[p], table)
    # ask for draw choice (show discard)
    ai.chooseDrawCard(state['_discard'][-1])
    # give new card (update state)
    ai.addCard(state['_stack'].pop())
    # ask for move(s)
    ai.makeMove()
    # verify/enact moves
    # ask for discard
    ai.chooseDiscard()
    # update state
    print "ai turn completed"

def humanTurn(p, players, state, table):
    try:
        print "Top discard: ", state['_discard'][-1]
        draw_choice = raw_input("Draw from [b]lind or [d]iscard pile?  ")
        if draw_choice == 'b':
            card = state['_stack'].pop()
        else:
            card = state['_discard'].pop()
    except IndexError:
        print "No discard option."
        card = state['_stack'].pop()
    state[p].append(card)
    print "Hand:",state[p]

    # ask for moves
    move_choice = raw_input("Enter move (comma seperated cards) or [p]ass.  ").split(', ')
    while move_choice != ['p']:
        valid = True
        # check that cards are in hand
        for c in move_choice:
            if c not in state[p]:
                print "Invalid move. You don't have", c
                valid = False
                break
        if len(move_choice) == len(state[p]):
            print "You must retain a discard."
            valid = False
        if not valid:
            move_choice = raw_input("Enter move (comma seperated cards) or [p]ass.  ").split(', ')
            continue
        # check that they form a valid set
        if not isValidSet(move_choice):
            parasite = False
            if len(move_choice) < 3:
                for pp in players:
                    for s in table[pp]:
                        if isValidSet(move_choice + s):
                            parasite = True
                            break
            if not parasite:
                move_choice = raw_input("Invalid group. Enter move (comma seperated cards) or [p]ass.  ").split(', ')
                continue
        # remove from hand
        for c in move_choice:
            del(state[p][state[p].index(c)])
        # add to table
        table[p].append(move_choice)
        print "Play made!"
        print "Hand:",state[p]
        move_choice = raw_input("Enter next move or [p]ass.  ").split(', ')

    discard_choice = raw_input("Select card to discard.  ")
    while discard_choice not in state[p]:
        print "Invalid card. Try again."
        discard_choice = raw_input("Select card to discard.  ")
    del(state[p][state[p].index(discard_choice)])
    state['_discard'].append(discard_choice)

def deal(players):
    random.shuffle(deck)
    hands = {p:[] for p in players}
    hands['_stack'] = []
    hands['_discard'] = []
    for i, p in enumerate(players):
        hands[p] += deck[i*7:i*7+7]
    hands['_discard'] = [deck[len(players)*7]]
    hands['_stack'] = deck[len(players)*7+1:]
    #print hands
    return hands


def buildDeck():
    suits = ['h', 'd', 'c', 's']
    cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    deck = []
    for s in suits:
        for c in cards:
            deck.append(s+c)
    return deck

def isValidSet(s):
    if len(s) < 3:
        return False
    # Approve if the numbers are the same
    numbers = [c[1:] for c in s]
    if len(unique(numbers)) == 1:
        return True
    # check if they are the same suit
    suits = [c[0] for c in s]
    if len(unique(suits)) > 1:
        return False
    # check that the numbers are sequential.
    for i in range(len(s)):
        try:
            numbers[i] = int(numbers[i])
        except ValueError:
            trans = {'J':11, 'Q':12, 'K':13}
            try:
                numbers[i] = trans[numbers[i]]
            except KeyError:
                if ('2' in numbers) or (2 in numbers):
                    numbers[i] = 1
                else:
                    numbers[i] = 14
    match = range(min(numbers), max(numbers)+1)
    numbers.sort()
    print "numbers:", numbers
    print "match:", match
    return (match == numbers)

def unique(l):
    u = []
    for i in l:
        if i not in u:
            u.append(i)
    return u

def calculateScores(players, state, table):
    scores = {p:(-1 * calculateValue(state[p])) for p in players}
    for p in players:
        for s in table[p]:
            scores[p] += calculateValue(s)
    return scores

def calculateValue(cards):
    values = {'A': 15, 'J': 10, 'Q': 10, 'K':10, '10':10}
    score = 0
    for c in cards:
        if c == 'sQ':
            score += 40
            continue
        v = c[1:]
        if v in values:
            score += values[v]
        else:
            score += 5
    return score


# Details
deck = buildDeck()
try:
    runGame()
except KeyboardInterrupt:
    print "\n\nGoodbye!\n\n"

