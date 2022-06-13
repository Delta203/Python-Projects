class Matrix:
    matrix = []
    def __init__(self, A: int):
        self.matrix = A
    
    def getColumns(self) -> int:
        return len(self.matrix[0])
    
    def getRows(self) -> int:
        return len(self.matrix)
    
    def print(self):
        print(" ")
        for a in self.matrix:
            print('\t'.join(str(i) for i in a))
"""
[-64,16,-4,1,-3],
[-8,4,-2,1,-11],
[1,1,1,1,-0.5],
[64,16,4,1,-17],
"""
A = Matrix([
    [2,2,3,75],
    [1,2,2,50],
    [1,1,2,40],
    ])

A.print()

# Zeilenstufenform
A.matrix = sorted(A.matrix, reverse=True)
for i in range(0, A.getRows()):
    # convert negative numbers to positive
    for j in range(i, A.getRows()):
        if A.matrix[j][i] < 0: A.matrix[j] = [n * -1 for n in A.matrix[j]]
    # calculate equation
    for j in range(i+1, A.getRows()):
        if A.matrix[i][i] != 0 and A.matrix[j][i] != 0:
            m, m_ = A.matrix[i][i], A.matrix[j][i]
            A.matrix[i] = [n * m_ for n in A.matrix[i]]
            A.matrix[j] = [n * m for n in A.matrix[j]]
            # subtract elements
            A.matrix[j] = [r - s for(r, s) in zip(A.matrix[i], A.matrix[j])]
    A.matrix[i] = [n / A.matrix[i][i] for n in A.matrix[i]]
    A.print()
# unit matrix    
for i in range(A.getRows()-1, -1, -1):
    c = A.matrix[i][A.getColumns()-1]
    r = 1
    for j in range(i+1, A.getColumns()-1):
        c -= A.matrix[i][j] * A.matrix[i+r][A.getColumns()-1]
        r += 1
        if i != j: A.matrix[i][j] = 0
    A.matrix[i][A.getColumns()-1] = c

A.print()
# https://www.share-code.eu/?c=srbximv
