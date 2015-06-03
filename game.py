# Rummy 500 (simplified)
import random
import rummyAI, rummyHuman

# Game
def runGame():
    # Get players
    players = raw_input("Enter player names, comma seperated. \nStart name with AI if you'd like a computer player.\n").split(', ')
    # Start with zero scores
    scores = {p:0 for p in players}
    engines = {}
    for p in players:
        if p[0:2] == 'AI':
            engines[p] = rummyAI.PlayerAI()
        else:
            engines[p] = rummyHuman.PlayerHuman()

    while (max(scores.values()) < 500):
        raw_input("Ready for next round?  ")
        # play round
        newScores = playRound(players, engines)
        print "This round:", newScores
        # update scores
        for p in players:
            scores[p] += newScores[p]
        print "Total:", scores
    print "Game over!!"
    print "Final scores:", scores

def playRound(players, engines):
    # Deal cards
    state = deal(players)
    table = {p:[] for p in players}
    while True:
        for p in players:
            print "\n\n\n"
            print "="*30
            print "\n",p+"'s Turn"
            state[p].sort()
            #print p+"'s Hand:", state[p]
            #print "Table:", table
            # ask to select draw/discard
            turn(engines[p], p, players, state, table)
            # check that cards remain
            if len(state[p]) == 0:
                print "\nRound finished!\n\n"
                return calculateScores(players, state, table)

def turn(player, p, players, state, table):
    player.setState(state[p], table)
    if len(state['_discard']) > 0:
        draw_choice = player.chooseDrawCard(state['_discard'][-1])
    else:
        player.chooseDrawCard(None)
        draw_choice = False
    if draw_choice:
        newCard = state['_discard'].pop()
    else:
        newCard = state['_stack'].pop()
    state[p].append(newCard)
    player.addCard(newCard)
    move_choice = player.makeMove(state[p])
    while move_choice:
        valid = True
        for c in move_choice:
            if c not in state[p]:
                print "Invalid move. You don't have", c
                valid = False
                break
        if len(move_choice) == len(state[p]):
            print "You must retain a discard."
            valid = False
        if not valid:
            move_choice = player.makeMove(state[p])
            continue
        if not isValidSet(move_choice):
            parasite = False
            singles = []
            if len(move_choice) < 3:
                for pp in players:
                    for s in table[pp]:
                        if len(s) == 1:
                            singles.append(s)
                        if isValidSet(move_choice + s):
                            parasite = True
                            break
                if not parasite and len(move_choice) == 1:
                    for pp in players:
                        for s in table[pp]:
                            for ss in singles:
                                if isValidSet(move_choice + s + ss):
                                    parasite = True
                                    break
            if not parasite:
                print "Invalid attempt."
                move_choice = player.makeMove(state[p])
                continue
        for c in move_choice: # Choice is apparently valid.
            del(state[p][state[p].index(c)])
        table[p].append(move_choice)
        print "Group played!"
        move_choice = player.makeMove(state[p])
    discard_choice = player.chooseDiscard()
    while discard_choice not in state[p]:
        print "Invalid card. Try again."
        discard_choice = player.chooseDiscard()
        continue
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

