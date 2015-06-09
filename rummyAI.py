import random, itertools
import rummyTools

class PlayerAI:
  def __init__(self):
    print "AI initialized."
    alive = True

  def setState(self, hand, table):
    self.hand = hand
    self.table = table
    self.playable = []
    print "State loaded."

  def chooseDrawCard(self, faceUp):
    # find all playable groups, with discard in hand
      # add group to playable
      # return True
    # test whether discard is playable as parasite
      # add discard to playable
      # return True
    print "Choosing a blind draw."
    return False # false means choose blind option

  def addCard(self, newCard):
    print "New card is", newCard
    self.hand.append(newCard)
    # find all playable groups
      # add to playable

  def makeMove(self, hand):
    # if hand == self.hand
      # calculate value of each move in playable
        # play the most valuable move
    # else
      # adjust self.hand
      # find all playable groups
      # return makeMove(self, self.hand)
    print "Not making a move."
    return False # no move to make

  def chooseDiscard(self):
    x = random.randint(0, len(self.hand)-1)
    print "Discarding random. Card is:", self.hand[x]
    return self.hand[x]

  def findPlayable(self, hand):
    return []
    #for nCards in range(len(hand), 3):





