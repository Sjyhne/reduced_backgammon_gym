# Reduced Backgammon Gym
A reduced backgammon gym, making it viable for classical reinforcement learning


## Observation and Action Space

### OBSERVATION SPACE

0: 0 -> 0 spillere, 1 - 4 -> 1 - 4 hvite spillere, 5 - 8 -> 1 - 4 svarte spillere (Value: 9)
1: ...
6: 0 -> 0 spillere, 1 - 4 -> 1 - 4 hvite spillere, 5 - 8 -> 1 - 4 svarte spillere (Value: 9)
7: (Hvit bar) 0 -> 0 spillere, 1 eller flere hvite spillere (Value: 2)
8: (Svart bar) 0 -> 0 spillere, 1 eller flere svarte spillere (Value: 2)
9: (Terning) 0 -> (1, 1), 1 -> (1, 2), 2 -> (2, 2) | Alle permutations for antall sider på terningen som er brukt | (Value: 3)
10: (Player turn) 0 -> Hvit, 1 -> Svart (Value: 2)

### ACTION SPACE

12: (Src location) 0, 1, 2, 3, 4, 5, 6, BAR (Value: 8)
13: (Dst location) 0, 1, 2, 3, 4, 5, 6, OFF (Value: 8)