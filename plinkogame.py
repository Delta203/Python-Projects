import random

class Plinko:
  def __init__(self, depth: int, symbol="●", symbol_="◌"):
    self.depth = depth
    self.symbol = symbol
    self.symbol_ = symbol_
    self.field = self.__initField()
    
  def __initField(self):
    field = []
    for i in range(self.depth):
      field.append(list("  " * (self.depth-i) + (self.symbol_ + "   ") * (i+1)))
    return field
    
  def drawField(self):
    for f in self.field:
      print("".join(f))
    
  def nextStep(self):
    lastX = 0
    for i in range(len(self.field)):
      line = self.field[i]
      if self.symbol in line:
        lastX = line.index(self.symbol)
        continue
      if i == 0:
        lastX = self.depth*2
        line[lastX] = self.symbol
        return
      lastX += [-2,2][random.randint(0,1)]
      line[lastX] = self.symbol
      return

def simulate(depth: int, position: int, symbol="●"):
  """Game simulation
  Simulate as many games until the specified target is reached.
  
  Parameters
  ----------
  depth : int
    The amount of layers the ball goes through
  position : int
    The position where the ball should land
  symbol : str, optional
    The balls symbol
  """
  games = 0
  while True:
    game = Plinko(depth)
    games+=1
    for i in range(game.depth):
      game.nextStep()
    if game.field[game.depth-1][2+4*position] == symbol:
      game.drawField()
      print("Games:", games)
      break
  
game = Plinko(20)
for i in range(game.depth):
  game.nextStep()
game.drawField()
