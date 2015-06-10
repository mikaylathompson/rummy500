import random, itertools
import rummyTools

class PlayerAI:
  def __init__(self):
    print "AI initialized."
    alive = True

  def setState(self, hand, table):
    self.hand = hand
    print self.hand
    self.table = table
    self.playable = []
    print "State loaded."

  def chooseDrawCard(self, faceUp):
    print "Faceup card is", faceUp
    if len(self.findPlayable(self.hand + [faceUp])) > 0:
      print "Choosing faceUp because it makes something playable."
      return True
    if rummyTools.isValidParasite([faceUp], self.table):
      print "Choosing faceUp because it's a parasite."
      return True
    print "Choosing a blind draw."
    return False # false means choose blind option

  def addCard(self, newCard):
    print "New card is", newCard

  def makeMove(self, hand):
    if hand == self.hand:
      maxVal = 0
      for play in self.findPlayable(hand):
        v = rummyTools.calculateValue(play)
        if v > maxVal:
          bestPlay = play
          print "Updating best play to", bestPlay
          maxVal = v
      if maxVal > 0:
        print "Playing", bestPlay, "with a value of", maxVal
        return bestPlay
      else:
        print "Not making a move."
        return False
    self.hand = hand
    return self.makeMove(hand)

  def chooseDiscard(self):
    # find "useful" cards:
      # for each card in the deck (thats not in hand or on table)
      # find playable moves, add one to the count of each card in hand
      # discard the card with the lowest total.
    x = random.randint(0, len(self.hand)-1)
    print "Discarding random. Card is:", self.hand[x]
    return self.hand[x]

  def findPlayable(self, hand):
    plays = []
    for nCards in range(3, len(hand)):
      for group in itertools.combinations(hand, nCards):
        if rummyTools.isValidSet(group):
          plays.append(list(group))
    for card in hand:
      if rummyTools.isValidParasite([card], self.table):
        plays.append([card])
    print "plays found:", plays
    return plays



