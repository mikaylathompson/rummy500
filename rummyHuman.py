class PlayerHuman:
  def __init__(self):
    print "Human initialized."

  def setState(self, hand, table):
    self.hand = hand
    self.table = table

    self.hand.sort()
    self.printHand(self.hand)
    self.printTable(self.table)

  def chooseDrawCard(self, faceUp):
    if faceUp is None:
      print "No cards in discard pile.  Drawing blind."
      return False
    print "Top discard is", faceUp
    draw_choice = raw_input("Draw from [b]lind or [d]iscard pile?  ")
    if draw_choice == 'b':
      return False
    if draw_choice == 'd':
      return True
    print "Invalid option. Enter b or d."
    return self.chooseDrawCard(faceUp)

  def addCard(self, newCard):
    print "New card is:", newCard

  def makeMove(self, hand):
    self.hand = hand
    hand.sort()
    self.printHand(hand)
    move_choice = raw_input("Input move or press enter to move on.  ").split(', ')
    if move_choice == [""]:
      return False
    return move_choice

  def chooseDiscard(self):
    return raw_input("Select card to discard.  ")

  def printHand(self, hand):
    print "\n\t\t\tMy hand:"
    print "\t\t\t",
    for c in hand:
      print c,
    print "\n"

  def printTable(self, table):
    print "The table:"
    for p in table.keys():
      print "\n",p
      for s in table[p]:
        for c in s:
          print c,
        print
      print "\n"




