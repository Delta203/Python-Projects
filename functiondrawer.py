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

  def writeByXandY(self, x: float, y: int):
    val = "X"
    if int(str(x).split(".")[1]) >= 3 and int(str(x).split(".")[1]) <= 7: val = "x"
  
    x = x*2
    y = y*(-1)
    y = y*2 # decimal optimisation
    
    try:
      self.coordinateSystem[int(y/2)+1+int(self.size)][int(x)+self.size*2] = val # y+1 cause Ʌ y line
    except: pass
  
  def highAndLows(self, func: str, step: int = 0.001) -> list:
    n = -float(self.size)
    result = []
    state = ""
    while n <= self.size:
      res = eval(func.replace("x", "("+str(n)+")"))
      res_next = eval(func.replace("x", "("+str(n + step)+")"))
      if res > res_next and state != "DOWN": 
        state = "DOWN"
        result.append(("PEAK",float("{:.5f}".format(n)),float("{:.5f}".format(res))))
      elif res < res_next and state != "UP":
        state = "UP"
        result.append(("NOUN",float("{:.5f}".format(n)),float("{:.5f}".format(res))))
      n += step
    return result[1:]
    
  def zeroPoints(self, func: str, step: int = 0.001) -> list:
    n = -float(self.size)
    result = []
    search = True
    target = eval(func.replace("x", "("+str(n)+")")) # first index
    while n <= self.size:
      target_next = eval(func.replace("x", "("+str(n + step)+")"))
      if abs(target-0) >= abs(target_next-0):
        target = target_next
        search = True
      else:
        if search == True: 
          result.append((float("{:.5f}".format(n)),float("{:.5f}".format(target))))
          search = False
        target = eval(func.replace("x", "("+str(n)+")")) # set new index if something was found
      
      #print(n, target, search) Debug
      n += step
        
    return result
  
  def function(self, func: str):
    for i in range(-self.size*2, self.size*2+1):
      i = i/2
      
      try:
        equation = eval(func.replace("x", "("+str(i)+")"))
        equation = float("{:.1f}".format(equation))
        if equation <= self.size: 
          self.writeByXandY(i, equation)
      except: pass

def rawFunction(val: str) -> str:
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
  val = _val.replace("^", "**")
  return val

""" evaluation: python functiondrawer.py <func> <size> """
func = "x"
size = 10
if len(sys.argv) == 2:
    func = str(sys.argv[1])
elif len(sys.argv) == 3:
    func = str(sys.argv[1])
    size = int(sys.argv[2])
    
func = rawFunction(func)
cs = CoordinateSystem(size)
cs.function(func)
cs.printCoordinateSystem()

print("-> Function: " + func)
print("Please wait for more information..")
print("Peaks & Nouns: ", cs.highAndLows(func))
print("Zeropoints: ", cs.zeroPoints(func))
