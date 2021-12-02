import random

def monkey(word : str):
  letters = "abcdefghijklmnopqrstuvwxyz"
  plain = ""
  prints = 0
  
  while plain[-len(word):] != word:
    rdm = random.randint(0,len(letters)-1)
    target = letters[rdm]
    plain += target
    prints += 1
    if prints % 10000 == 0: print(format(prints, ',d'))

  print(plain, format(prints, ',d'))

monkey("lea")
