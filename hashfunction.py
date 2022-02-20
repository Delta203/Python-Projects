import sys, time

def stringToBinary(st: str) -> int:
    return int("".join(format(ord(i), "08b") for i in st))

def bAdic(num: int, base: int = 2) -> str:
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

def has(st: str, withblock: bool = False, withbithash: bool = False, blocklen: int = 4, length: int = 64) -> str:
    exp = 8
    b_st = stringToBinary(st)
    b_st_len = len(str(b_st))
    trim = [int("1" + str(b_st)[x*b_st_len//blocklen:(x+1)*b_st_len//blocklen])**exp for x in range(blocklen)] # split bitvalue into blocks
    if withblock: print("block       :", trim)
    #print(trim)
    
    bit_hash = ""
    c = 1
    for val in trim:
        dexp = len(str(val))//5
        if dexp > 4: dexp = 4
        p = getNextPrime(int(str(val)[:5]) * c)**dexp
        bit_hash += str(int(val) % p)
        c += 1
    if withbithash: print("bithash     :", bit_hash)
    hex_hash = bAdic(int(bit_hash), 16)[:length]
    return "0x" + "0"*((length-1)-len(hex_hash)) + hex_hash
    
# usage: python hashfunction.py <words>
w = ""
for i in range(1, len(sys.argv)):
    w += sys.argv[i]
w = w[1:]

start_time = time.time()
print("input       :", w)
print("hash        :", has(w, False, True))
end_time = time.time()
print("process time:", str(round(end_time-start_time, 4)) + "sec")
