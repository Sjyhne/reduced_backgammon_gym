# import itertools
# from collections import namedtuple

# Variables for the color of the players
WHITE, BLACK = 0, 1
COLORS = {WHITE: "White", BLACK: "Black"}
# The number of spots each player has as home spots
N_HOME_POSITIONS = 2
# Total number of spots, disregarding the BAR and OFF
N_SPOTS = 9
# Number of pieces per player
N_PIECES = 5
# Number of sides on dice
DICE_SIDES = 2
# Max stack size
MAX_N_STACK = 3
# Chance of acquiring 4 actions when throwing two die of the same eyes
DOUBLE_CHANCE = 0.3

# The board looks like this atm
# 0    1    2   3   4   5   6   7    8
# HW | HW | S | S | S | S | S | HB | HB


def initiate_board():
    board = [{"spot": k, "count": 0, "color": None} for k, i in enumerate(range(N_SPOTS))]
    board[0].update({"count": 2, "color": WHITE})
    board[1].update({"count": 1, "color": BLACK})
    board[3].update({"count": 2, "color": WHITE})
    board[5].update({"count": 2, "color": BLACK})
    board[7].update({"count": 1, "color": WHITE})
    board[8].update({"count": 2, "color": BLACK})
    
    return board


class Backgammon:

    def __init__(self):
        # Initiates the board to the starting positions
        self.board = initiate_board()
        # A counter for how many has been moved to the bar
        self.bar = {WHITE: 0, BLACK: 0}
        # Only a counter for how many has been beared off
        self.off = {WHITE: 0, BLACK: 0}
        # The home positions/goal for the pieces before they can bear off
        self.players_home_positions = {WHITE: range(N_SPOTS)[N_SPOTS - N_HOME_POSITIONS:], BLACK: range(N_SPOTS)[:N_HOME_POSITIONS]}

    
    def get_players_positions(self):
        players_positions = {WHITE: [], BLACK: []}
        # Loops and adds them to their respective list
        for i in self.board:
            if i["color"] == WHITE:
                players_positions[WHITE].append(i)
            elif i["color"] == BLACK:
                players_positions[BLACK].append(i)
        
        return players_positions

    def can_bear_off(self, color):
        # Checks if there are any pieces on the bar
        if self.bar[color] > 0:
            print("CANNOT BEAR OFF -> BAR NOT EMPTY")
            return False
        # Get the positions of the current player
        players_positions = self.get_players_positions()[color]
        spots = [i["spot"] for i in players_positions]  
        # Returns True if set(spots) is a subset of set(players_home_positions)
        return set(set(spots)).issubset(self.players_home_positions[color])

    # color is the color of the current player, and action
    # is a tuple for the src and dest for the action (src, dest)
    def is_valid(self, color, action):
        src, target = action
        # Have to check if the action is within bounds of the board
        if self.board[src]["count"] >= 1 and self.board[src]["color"] == color:
            if 0 <= target < N_SPOTS:
                # If the target is within board limits, then we have to check
                # If the target has two or more enemies, or the target reaches
                # The upper limit of how many pieces can be stacked (3)
                if self.board[target]["color"] != color and self.board[target]["count"] > 1:
                    return False
                elif self.board[target]["color"] == color and self.board[target]["count"] > MAX_N_STACK:
                    return False
                else:
                    return True
            # If the target is not within the bounds of the board
            # Then we have to check whether or not the player can
            # Bear off
            elif self.can_bear_off(color):
                print("Tries to bear off")
                return True

        return False

    def get_oppponent_color(self, color):
        if color == WHITE:
            return BLACK
        else:
            return WHITE
        
    def execute_action(self, color, action):
        src, target = action
        # If the action is true
        if self.is_valid(color, action):
            # Check if there is an opponent piece on the target
            if self.board[target]["color"] != color:
                # TODO: Move the opponent piece to the bar and move
                # Our own piece to the spot
                ...
            else:
                # TODO: Move our own piece to the spot
                ...


bg = Backgammon()
for i in bg.board:
    print(i)

print()
for c, s in bg.get_players_positions().items():
    print("COLOR:", COLORS[c])
    for i in s:
        print(i)
    print()

print(bg.can_bear_off(BLACK))

print("ACTION IS TRUE?:", bg.is_valid(BLACK, (2, 8)))