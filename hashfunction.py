import sys, time

def stringToBinary(st: str) -> int:
    return int("".join(format(ord(i), "08b") for i in st))

def bAdic(num: int, base: int = 2, seperator: str = "") -> str:
    """
    b-Adic possible to base 35
    base:
        2: binary
        10: decimal
        16: hex
    """
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

def getNextPrime(num: int) -> int:
    num += 1
    while True:
        for i in range(2, num):
            if num % i == 0: break
        else: return num
        num += 1

def has(st: str, prefix: str = "0x", longhash: bool = False) -> str:
    """
    one way function: 
        g^exp mod p
        g^exp > p
    g: str
    exp: int
    p: int | high prime number
    
    longhash: bool | mainly for debug
    """
    exp = 64
    g = stringToBinary(st)
    p = getNextPrime(len(str(g)))
    h = bAdic(g**exp % p, 16)
    split = len(h) // 64
    
    if longhash: return h
    result = ""
    for i in range(0, 64):
        result += h[split*i]
    return prefix + result
    
# usage: python hashfunction.py <words>
w = ""
for i in range(1, len(sys.argv)):
    w = w + " " + sys.argv[i]
w = w[1:]

start_time = time.time()
print("input       :", w)
print("hash        :", has(w))
end_time = time.time()
print("process time:", str(round(end_time-start_time, 4)) + "sec")
