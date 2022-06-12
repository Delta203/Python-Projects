import matplotlib.pyplot as plt

num = 88

x = []
y = []

c = 0
even = 0
odd = 0

def foo(bar: int) -> int:
    global c, even, odd
    while bar != 1:
        x.append(c)
        y.append(bar)
        print(c, bar)
        
        if bar % 2 == 0:
            bar = bar // 2
            even += 1
        else:
            bar = 3 * bar + 1
            odd += 1
        c += 1
    x.append(c)
    y.append(bar)
    print(c, bar)
        
foo(num)
print("steps:", c, "even:", even, "odd:", odd)

plt.plot(x, y, marker='x', markersize=5)
plt.xlabel("x - axis")
plt.ylabel("y - axis")
plt.title(str(num))

plt.show()