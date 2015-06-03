import random

class PlayerAI:
  def __init__(self):
    print "AI initialized."
    alive = True

  def setState(self, hand, table):
    self.hand = hand
    self.table = table
    print "State loaded."

  def chooseDrawCard(self, faceUp):
    print "Choosing a blind draw."
    return False # false means choose blind option

  def addCard(self, newCard):
    print "New card is", newCard
    self.hand += newCard

  def makeMove(self):
    print "Not making a move."
    return False # no move to make

  def chooseDiscard(self):
    print "Discarding", self.hand[-1]
    return self.hand[-1]

  
#def aiTurn(ai, p, players, state, table):
    # give state[p] and table
    # ask for draw choice (show discard)
    # give new card (update state)
    # ask for move(s)
    # verify/enact moves
    # ask for discard
    # update state
    #print "ai turn completed"

