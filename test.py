import numpy as np
import random
"""
    0: 0 -> 0 spillere, 1 - 5 -> 1 - 5 hvite spillere, 6 - 10 -> 1 - 5 svarte spillere (Value: 9)
    1: ...
    7: 0 -> 0 spillere, 1 - 5 -> 1 - 5 hvite spillere, 6 - 10 -> 1 - 5 svarte spillere (Value: 9)
    8: (Hvit bar) 0 -> 0 spillere, 1 - 5 -> 1 - 5 hvite spillere (Value: 2)
    9: (Svart bar) 0 -> 0 spillere, 1 - 5 -> 1 - 5 svarte spillere (Value: 2)
    10: (Terning) 0 -> (1, 1), 1 -> (1, 2), 2 -> (2, 2) (Value: 3)
    11: (Player turn) 0 -> Hvit, 1 -> Svart (Value: 2)
    12: (Src location) 0, 1, 2, 3, 4, 5, 6, 7, BAR (Value: 8)
    13: (Dst location) 0, 1, 2, 3, 4, 5, 6, 7, OFF (Value: 8)
"""



rep = np.zeros((9, 9, 9, 9, 9, 9, 9, 2, 2, 3, 2, 8, 8), np.float16)

print((rep.size * rep.itemsize) / (1024 ** 2))

DOUBLE_CHANCE = 0.3

r1 = [1 for i in range(int(DOUBLE_CHANCE * 100))] + [2 for i in range(int(100 - DOUBLE_CHANCE * 100))]
r2 = [1 for i in range(int(100 - DOUBLE_CHANCE * 100))] + [2 for i in range(int(DOUBLE_CHANCE * 100))]

count1 = 0
count2 = 0

nr = 1000000

for i in range(nr):
    pick = random.choice(r1)
    if pick == 1:
        count1 += 1
    else:
        count2 += 1

print(count1)
print(count2)
print(count1 / nr)
print(count2 / nr)