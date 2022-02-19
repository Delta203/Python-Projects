import random

def stringToBinary(st: str) -> int:
    return int("".join(format(ord(i), "08b") for i in st))

''' b-Adic possible to base 35 '''
def bAdic(num: int, base: int = 2, seperator: str = "") -> str:
    def getVal(num_: int) -> str:
        l = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if num_ < 10: return str(num_)
        return l[num_-10]
    result = ""
    while num//base != 0:
        result = getVal(num%base) + result
        num = num//base
    result = getVal(num%base) + result
    return result
    
def hexString(st: str) -> str:
    result = ""
    c = 0
    for i in st:
        if c == 2: 
            result += " "
            c = 0
        result += i
        c+=1
    return result

word = "Hello World"
keys = [128]

exp = random.choice(keys)
g = stringToBinary(word)
p = (g**exp) * 1019 # high primenumber

has = bAdic(g**exp % p, 16)[:64]

print("=>", has)
print("32 byte", hexString(has))