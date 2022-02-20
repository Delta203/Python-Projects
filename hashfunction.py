import sys, time

def stringToBinary(st: str) -> int:
    return int("".join(format(ord(i), "08b") for i in st))

def bAdic(num: int, base: int = 2) -> str:
    """
    b-Adic possible to base 35
    
    base : int
        2 : binary
        10 : decimal
        16 : hex
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

def has(st: str, printBlocks: bool = False, printBitHash: bool = False, printFullHash: bool = False) -> str:
    """
    generate hash value
    output: hex 32 byte
    
    printBlocks : list | debug binary value of string
    printBitHash : bool | debug bithash
    printFullHash : bool | debug full hash value
    """
    exp = 32
    blockAmount = 6
    b_st = stringToBinary(st)
    b_st_len = len(str(b_st))
    padding = b_st % len(str(b_st))
    
    trim = [(int("1" + str(b_st)[x*b_st_len//blockAmount:(x+1)*b_st_len//blockAmount])+padding)**exp for x in range(blockAmount)] # split bitvalue into blocks
    if printBlocks: print("block       :", trim)
    
    bit_hash = ""
    c = 1
    for val in trim:
        dexp = blockAmount // 2 # force hash length
        p = getNextPrime(int(str(val)[:5]) * c)**dexp
        bit_hash += str((int(val) % p) + padding)
        c += 1
    if printBitHash: print("bithash     :", bit_hash)
    hex_hash = bAdic(int(bit_hash), 16)
    if printFullHash: print("fullhash    :", "0x" + hex_hash)
    comp_hex_hash = hex_hash[-63:]
    return "0x" + "0"*(63-len(comp_hex_hash)) + comp_hex_hash
    
# usage: python hashfunction.py <words>
w = ""
for i in range(1, len(sys.argv)):
    w = w + " " + sys.argv[i]
w = w[1:]

start_time = time.time()
print("input       :", w)
print("hash        :", has(w, False, False, False))
end_time = time.time()
print("process time:", str(round(end_time-start_time, 4)) + "sec")
