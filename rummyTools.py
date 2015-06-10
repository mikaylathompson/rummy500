
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

def unique(l):
    u = []
    for i in l:
        if i not in u:
            u.append(i)
    return u

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

def isValidParasite(cards, table):
  singles = []
  players = table.keys()
  players.del(players.find('_stack'))
  players.del(players.find('_discard'))
  if len(cards) < 3:
    for player in players:
      for group in table[player]:
        if len(group) == 1:
          singles.append(group)
        if isValidSet(cards + group):
          return True
    if len(cards) == 1:
      for player in players:
        for group in table[player]:
          for s in singles:
            if isValidSet(cards + group + s):
              return True
  return False

