import sys

class CoordinateSystem:
  def __init__(self, size: int = 10):
    self.size = size
    self.coordinateSystem = self.buildCoordinateSystem()
  
  def buildCoordinateSystem(self) -> list:
    arr = []
    arr.append(" " * (self.size*2) + "Ʌ y")
    for i in range(self.size*2+1):
      _arr = []
      for j in range(self.size*2*2+1):
        if j == self.size*2:
          if i == self.size:
            _arr.append("+")
          else: _arr.append("|")
        elif i == self.size:
          if j % 2 != 0: _arr.append("-")
          else: _arr.append("+")
        else: _arr.append(" ") # background
      if i == self.size: _arr.append("> x")
      arr.append(_arr)
    return arr
  
  def printCoordinateSystem(self):
    for i in self.coordinateSystem:
      line = ""
      for j in i:
        line += j
      print(line)

  def writeByXandY(self, x: float, y: int, val: str = "X"):
    x = x*2
    y = y*(-1)
    y = y*2 # decimal optimisation
    try:
      self.coordinateSystem[int(y/2)+1+int(self.size)][int(x)+self.size*2] = val # y+1 cause Ʌ y line
    except: pass
  
  def function(self, val : str):
    for i in range(-self.size*2, self.size*2+1):
      i = i/2
      
      _val = val[0]
      for j in range(len(val)-1):
        if val[j].isdigit() and val[j+1] == "x":
          _val += "*"
          _val += val[j+1]
        elif val[j] == "x" and val[j+1].isdigit():
          _val += "*"
          _val += val[j+1]
        elif (val[j].isdigit() or val[j] == "x") and val[j+1] == "(":
          _val += "*"
          _val += val[j+1]
        elif val[j] == ")" and (val[j+1].isdigit() or val[j+1] == "x"):
          _val += "*"
          _val += val[j+1]
        else: _val += val[j+1]
      try:
        val = _val.replace("^", "**")
        equation = eval(val.replace("x", "("+str(i)+")"))
        equation = float("{:.1f}".format(equation))
        if equation <= self.size: 
          if equation % 1 == 0.0: self.writeByXandY(i, equation)
          else: self.writeByXandY(i, equation, "x")
      except: pass

""" evaluation: python functiondrawer.py <func> """
func = "x"
if len(sys.argv) == 2:
    func = str(sys.argv[1])
    
cs = CoordinateSystem()
cs.function(func)
cs.printCoordinateSystem()

print("-> " + func)