# import itertools
# from collections import namedtuple
import random

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
# Tokens for the players
TOKENS = {WHITE: "O", BLACK: "X", None: "-"}
# Integer for representing the BAR location
BAR = -10

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

    # A counter for how many has been moved to the bar
    bar = {WHITE: 0, BLACK: 0}
    # Only a counter for how many has been beared off
    off = {WHITE: 0, BLACK: 0}

    return board, bar, off

def bear_off_board_setup():
    board = [{"spot": k, "count": 0, "color": None} for k, i in enumerate(range(N_SPOTS))]
    board[0].update({"count": 2, "color": BLACK})
    board[1].update({"count": 3, "color": BLACK})
    board[3].update({"count": 3, "color": WHITE})
    board[7].update({"count": 2, "color": WHITE})

    # A counter for how many has been moved to the bar
    bar = {WHITE: 0, BLACK: 0}
    # Only a counter for how many has been beared off
    off = {WHITE: 0, BLACK: 0}
    
    return board, bar, off

def bar_play_board_setup():
    board = [{"spot": k, "count": 0, "color": None} for k, i in enumerate(range(N_SPOTS))]
    board[2].update({"count": 2, "color": BLACK})
    board[4].update({"count": 1, "color": BLACK})
    board[3].update({"count": 1, "color": WHITE})
    board[6].update({"count": 2, "color": WHITE})

    # A counter for how many has been moved to the bar
    bar = {WHITE: 2, BLACK: 2}
    # Only a counter for how many has been beared off
    off = {WHITE: 0, BLACK: 0}
    
    return board, bar, off

class Backgammon:

    def __init__(self):
        # Initiates the board to the starting positions
        self.board, self.bar, self.off = bear_off_board_setup()
        # The home positions/goal for the pieces before they can bear off
        self.players_home_positions = {WHITE: range(N_SPOTS)[N_SPOTS - N_HOME_POSITIONS:], BLACK: range(N_SPOTS)[:N_HOME_POSITIONS]}
        # Keep count of the used and non-used dice
        self.used_dice = []
        self.non_used_dice = list(self.roll())

    def roll(self):
        r1 = random.choice([1, 2])
        r2 = random.choice([1, 2])
        return (r1, r2)

    
    def get_players_positions(self):
        players_positions = {WHITE: [], BLACK: []}
        # Loops and adds them to their respective list
        for i in self.board:
            if i["color"] == WHITE:
                players_positions[WHITE].append(i)
            elif i["color"] == BLACK:
                players_positions[BLACK].append(i)

        if self.bar[WHITE] > 0:
            players_positions[WHITE].append({"spot": BAR, "count": self.bar[WHITE], "color": WHITE})
        
        if self.bar[BLACK] > 0:
            players_positions[BLACK].append({"spot": BAR, "count": self.bar[BLACK], "color": BLACK})
        
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

    # Check for whether the piece is the furthest piece away from bearing off
    # This is relevant when the die shows 2, and the player tries to move
    # the innermost of the two places in home position. (1, 1) -> (1, 0) | 1 OFF
    def is_src_furthest_piece(self, color, action):
        src, dst = action
        player_positions = [i["spot"] for i in self.get_players_positions()[color]]
        if color == WHITE:
            # It is min() for white because their home are at end of board
            if src == min(player_positions):
                return True
            else:
                return False
        else:
            # It is max() for BLACK because their home are at the start of board
            if src == max(player_positions):
                return True
            else:
                return False

    # color is the color of the current player, and action
    # is a tuple for the src and dest for the action (src, dest)
    def is_valid(self, color, action):
        _, (src, target) = action
        # Must check if the player has a piece on the bar, if he has, then he must
        # Move that piece first.
        # Have to check if the action is within bounds of the board
        if self.bar[color] > 0:
            # Then we need to check if the move is moving the piece from the bar
            # And onto the board
            if src == BAR and (0 <= target < N_SPOTS):
                # Check if there are more than two enemies on the target
                print(target)
                if self.board[target]["count"] > 1 and self.board[target]["color"] == self.get_opponent_color(color):
                    return False
                # Check if there are 3 pieces on the spot - if so, then we cannot move
                elif self.board[target]["count"] == MAX_N_STACK:
                    return False
                # If the target is out of bounds
                elif (0 > target) or (target >= N_SPOTS):
                    return False
                # Now I think the wrong targets are removed
                else:
                    return True

        elif self.board[src]["count"] >= 1 and self.board[src]["color"] == color:
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
                # If the target is not 10, then check if the source piece
                # Is the last piece of all pieces in home
                if target > N_SPOTS - 1 or target < -1:
                    if self.is_src_furthest_piece(color, action):
                        return True
                    else:
                        return False
                
                return True

        return False

    def get_opponent_color(self, color):
        if color == WHITE:
            return BLACK
        else:
            return WHITE

    def knock_out_piece(self, color, target):
        # Adding piece to the bar
        self.bar[color] += 1
        # Removing piece from the target spot
        self.board[target].update({"count": 0, "color": None})

    def remove_piece_from_src(self, color, src):
        src_piece_count = self.board[src]["count"]
        # Remove a piece from the src location and remove color if there are none left
        if src_piece_count == 1:
            self.board[src].update({"count": src_piece_count - 1, "color": None})
        # Remove a piece from the src location
        else:
            self.board[src].update({"count": src_piece_count - 1})
    
    def add_piece_to_dst(self, color, dst):
        dst_piece_count = self.board[dst]["count"]
        # Add piece to destination location, and update color if there are no pieces there
        if dst_piece_count == 0:
            self.board[dst].update({"count": dst_piece_count + 1, "color": color})
        # Add piece to destination location
        else:
            self.board[dst].update({"count": dst_piece_count + 1})

    def move_piece_from_src_to_dest(self, color, action):
        _, (src, dst) = action
        src_piece_count = self.board[src]["count"]
        if src_piece_count < 1:
            raise RuntimeError("Cannot move from spot because there are no pieces left")
        
        self.remove_piece_from_src(color, src)
        self.add_piece_to_dst(color, dst)
        
    def move_piece_off(self, color, action):
        _, (src, _) = action
        # Remove piece from src
        self.remove_piece_from_src(color, src)
        # Add piece to "OFF"
        self.off[color] += 1

        print(self.off[color])

    def move_from_bar(self, color, action):
        _, (src, dst) = action
        # Decrement the bar counter
        self.bar[color] -= 1
        # Move the piece onto the board
        self.add_piece_to_dst(color, dst)
        
    def execute_action(self, color, action):
        roll, (src, target) = action
        # If the action is true
        if self.is_valid(color, action):
            # Check if there is an opponent piece on the target
            if self.board[target]["color"] == self.get_opponent_color(color) and target >= 0:
                print("KNOCKOUT")
                # Adding the opponents piece to the bar and removing it from the target
                self.knock_out_piece(self.get_opponent_color(color), target)
                # Move the piece from the source to the target
                if src == BAR:
                    self.move_from_bar(color, action)
                else:
                    self.move_piece_from_src_to_dest(color, action)
            # If the player can bear off (all home) and the target is not in
            # The normal range of spots, then move the player off
            elif self.can_bear_off(color) and target not in range(N_SPOTS):
                self.move_piece_off(color, action)
            elif src == BAR:
                self.move_from_bar(color, action)
            else:
                # Move the piece from the source to the target
                self.move_piece_from_src_to_dest(color, action)
            self.non_used_dice.remove(roll)
            self.used_dice.append(roll)
        else:
            print("ACTION IS NOT VALID")

    # The starting row variable is for when we are moving from bar
    def generate_single_action(self, src, starting_point, roll):
        actions = []
        # Add all actions where the die is added to the starting point
        for i in roll:
            actions.append((i, (src, starting_point + i)))
        # Add all actions where the die is subtracted from the starting point
        for i in roll:
            actions.append((i, (src, starting_point - i)))
        
        return list(set(actions))

    def generate_actions(self, color, roll):
        # First step must be to get all of the positions of the current player
        players_positions = self.get_players_positions()[color]
        spots = [i["spot"] for i in players_positions]
        print("Spots with pieces: ", spots)

        actions = []

        # For each spot, generate an action with the associated source spot
        for spot in spots:
            src = spot
            # Must check if the source is BAR, then the starting position is either
            # -1 or 9, depending on color
            if spot == BAR:
                # An example would be that if WHITE uses a die of value 1 from BAR
                # Then it will land on spot 0, therefore -1 is used
                if color == WHITE:
                    temp_src = -1
                    temp_actions = self.generate_single_action(src, temp_src, roll)
                    actions.extend(temp_actions)
                # Same here, only black is moving the opposite direction
                # So the using a die of value 1 means landing on positions 8
                elif color == BLACK:
                    temp_src = 9
                    temp_actions = self.generate_single_action(src, temp_src, roll)
                    actions.extend(temp_actions)
            # If the src spot is not the bar, then nothing extra needs to be 
            # Taken care of
            else:
                temp_actions = self.generate_single_action(src, src, roll)
                actions.extend(temp_actions)
            
        return actions

    def render(self, round_nr):
        print(round_nr)
        print("=================================================")
        print(" B: {} | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | W: {}".format(self.off[BLACK], self.off[WHITE]))
        print("-------------------------------------------------")
        token_string = f"BAR: {self.bar[BLACK]}|"
        count_string = f"      |"
        for i in range(9):
            token_string += f" {TOKENS[self.board[i]['color']]} |"
            count_string += f" {self.board[i]['count']} |"
        token_string += f"BAR: {self.bar[WHITE]}"

        print(token_string)
        print(count_string)
        print("=================================================")
        print("\n")


bg = Backgammon()

print("INITIAL BOARD!")
bg.render(0)
roll = bg.roll()
actions = bg.generate_actions(BLACK, roll)
print(actions)
for i in actions:
    if bg.is_valid(BLACK, i):
        print(i)
"""print("NONUSED:", bg.non_used_dice)
print("USED:", bg.used_dice)
bg.execute_action(BLACK, (2, (8, 6)))
print("NONUSED:", bg.non_used_dice)
print("USED:", bg.used_dice)
bg.render(2)
bg.execute_action(BLACK, (1, (8, 7)))
print("NONUSED:", bg.non_used_dice)
print("USED:", bg.used_dice)
bg.render(3)"""