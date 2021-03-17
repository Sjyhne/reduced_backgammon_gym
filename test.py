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

"""
    OBSERVATION SPACE

    0: 0 -> 0 spillere, 1 - 4 -> 1 - 4 hvite spillere, 5 - 8 -> 1 - 4 svarte spillere (Value: 9)
    1: ...
    6: 0 -> 0 spillere, 1 - 4 -> 1 - 4 hvite spillere, 5 - 8 -> 1 - 4 svarte spillere (Value: 9)
    7: (Hvit bar) 0 -> 0 spillere, 1 eller flere hvite spillere (Value: 2)
    8: (Svart bar) 0 -> 0 spillere, 1 eller flere svarte spillere (Value: 2)
    9: (Terning) 0 -> (1, 1), 1 -> (1, 2), 2 -> (2, 2) | Alle permutations for antall sider på terningen som er brukt | (Value: 3)
    10: (Player turn) 0 -> Hvit, 1 -> Svart (Value: 2)



    ### OBSERVATION SPACE

    0: 0 -> 0 spillere, 1 - 4 -> 1 - 4 hvite spillere, 5 - 8 -> 1 - 4 svarte spillere (Value: 9)
    1: ...
    6: 0 -> 0 spillere, 1 - 4 -> 1 - 4 hvite spillere, 5 - 8 -> 1 - 4 svarte spillere (Value: 9)
    7: (Hvit bar) 0 -> 0 spillere, 1 eller flere hvite spillere (Value: 2)
    8: (Svart bar) 0 -> 0 spillere, 1 eller flere svarte spillere (Value: 2)
    9: (Terning side 1): 0 -> Ingen flere trekk igjen med verdien 1, 1 -> 1 eller flere trekk igjen med verdien 1
    10: (Terning side 2): 0 -> Ingen flere trekk igjen med veriden 2, 1 -> 1 eller flere trekk igjen med verdien 2

    ### ACTION SPACE

    12: (Src location) 0, 1, 2, 3, 4, 5, 6, BAR (Value: 8)
    13: (Dst location) 0, 1, 2, 3, 4, 5, 6, OFF (Value: 8)
"""


rep = np.zeros((9, 9, 9, 9, 9, 9, 9, 2, 2, 2, 2, 8, 8), np.float16)

print((rep.size * rep.itemsize) / (1024 ** 2))


t = [(1, 2), (2, 2), (2, 1)]

t = sorted(t)

print(t)

import itertools

# (0, 1, 2, 3, 4, 5, 6, 7)
# (0, 1, 2, 3, 4, 5, 6, 7)
# (0, 7) -> 


print(100//21)

data = []

for i in range(100):
    data.append(i)

chunks = [data[x:x+20] for x in range(0, len(data), 20)]

print(chunks)