import sys
import random
import time

def monkey(word : str, letters: str = "abcdefghijklmnopqrstuvwxyz"):
  plain = ""
  prints = 0
  
  print("")
  print("word: " + word)
  print("word length: " + str(len(word)))
  print("alphabet: " + letters, len(letters))
  print("")
  
  time.sleep(3)
  
  if checkword(word, letters) == False:
    print("Word Error: Invalid word format. (letter does not exist in alphabet)")
    sys.exit(0)
    
  while plain[-len(word):] != word:
    rdm = random.randint(0,len(letters)-1)
    target = letters[rdm]
    plain += target
    prints += 1
    if prints % 10000 == 0: print(format(prints, ',d'), plain[-50:])

  #if len(plain) > 10000: print("-> Last 10000 letters: ..." + plain[-10000:], format(prints, ',d'))
  #else: print("-> " + plain, format(prints, ',d'))
  print(format(prints, ',d'), plain[-50:] + " <-")

def checkword(word : str, letters : str) -> bool:
  for l in word:
    if l in letters: pass
    else:
      print("Word Error: Error with letter " + l)
      return False
    
""" evaluation: python main.py <word> <alphabet> """
if len(sys.argv) == 2:
  monkey(str(sys.argv[1]))
elif len(sys.argv) == 3:
  monkey(str(sys.argv[1]), str(sys.argv[2]))
else:
  print("Argument Error: python main.py <word> <alphabet>")
  sys.exit(0)
