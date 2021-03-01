import random
import itertools

# Variables for the color of the players
#WHITE, BLACK = 0, 1
# COLORS = {WHITE: "White", BLACK: "Black"}
# The number of spots each player has as home spots
# N_HOME_POSITIONS = 2
# Total number of spots, disregarding the BAR and OFF
# N_SPOTS = 7
# Number of pieces per player
# N_PIECES = 4
# Number of sides on dice
# DICE_SIDES = 2
# Max stack size
# MAX_N_STACK = 4
# Chance of acquiring 4 actions when throwing two die of the same eyes
# Works only when the number of DICE_SIDES are limited to 2
# DOUBLE_CHANCE = 0.3
# Tokens for the players
#TOKENS = {WHITE: "O", BLACK: "X", None: "-"}
# Integer for representing the BAR location
#BAR = {WHITE: -100, BLACK: 100}

# The board looks like this atm
# 0    1    2   3   4   5   6   7    8
# HW | HW | S | S | S | S | S | HB | HB

class Backgammon:

    def __init__(self, n_spots=7, n_home_positions=2, n_pieces=4, dice_sides=2, max_n_stack=4, double_chance=0.3):

        self.n_spots = n_spots
        self.n_home_positions = n_home_positions
        self.n_pieces = n_pieces
        self.dice_sides = dice_sides
        self.max_n_stack = max_n_stack
        self.double_chance = double_chance

        self.white, self.black = 0, 1
        self.colors = {self.white: "White", self.black: "Black"}
        self.tokens = {self.white: "O", self.black: "X", None: "-"}
        self.bar_spots = {self.white: -100, self.black: 100}

        # Initiates the board to the starting positions
        self.board, self.bar, self.off = self.initiate_board()

        # The home positions/goal for the pieces before they can bear off
        self.players_home_positions = {self.white: range(self.n_spots)[self.n_spots - self.n_home_positions:], self.black: range(self.n_spots)[:self.n_home_positions]}

        # Just picking a random starting agent - Should probably be decided by throwing the dice
        # And choosing the one with the higher number - But ultimately it is just the same as
        # Picking the starting agent at random
        self.starting_agent = random.choice([self.white, self.black])

        self.dice = self.roll()

    def initiate_board(self):
        board = [{"spot": k, "count": 0, "color": None} for k, i in enumerate(range(self.n_spots))]
        board[0].update({"count": 2, "color": self.white})
        board[2].update({"count": 2, "color": self.black})
        board[4].update({"count": 2, "color": self.white})
        board[6].update({"count": 2, "color": self.black})

        # A counter for how many has been moved to the bar
        bar = {self.white: 0, self.black: 0}
        # Only a counter for how many has been beared off
        off = {self.white: 0, self.black: 0}

        return board, bar, off

    def roll(self):
        self.used_dice = []
        
        self.non_used_dice = []

        if self.dice_sides == 2:
            r1 = random.choice([1 for i in range(int(self.double_chance * 100))] + [2 for i in range(int(100 - self.double_chance * 100))])
            r2 = random.choice([1 for i in range(int(100 - self.double_chance * 100))] + [2 for i in range(int(self.double_chance * 100))])
        else:
            r1 = random.choice(range(1, self.dice_sides + 1))
            r2 = random.choice(range(1, self.dice_sides + 1))

        if r1 == r2:
            self.non_used_dice = [r1 for i in range(4)]
        else:
            self.non_used_dice = [r1, r2]

        return (r1, r2)
    
    def get_players_positions(self):
        players_positions = {self.white: [], self.black: []}
        # Loops and adds them to their respective list
        for i in self.board:
            if i["color"] == self.white:
                players_positions[self.white].append(i)
            elif i["color"] == self.black:
                players_positions[self.black].append(i)

        if self.bar[self.white] > 0:
            players_positions[self.white].append({"spot": self.bar_spots[self.white], "count": self.bar[self.white], "color": self.white})
        
        if self.bar[self.black] > 0:
            players_positions[self.black].append({"spot": self.bar_spots[self.black], "count": self.bar[self.black], "color": self.black})
        
        return players_positions

    def can_bear_off(self, color):
        # Checks if there are any pieces on the bar
        if self.bar[color] > 0:
            print("CANNOT BEAR OFF -> BAR NOT EMPTY")
            return False
        # Get the positions of the current player
        spots = [i["spot"] for i in self.get_players_positions()[color]]  
        # Returns True if set(spots) is a subset of set(players_home_positions)
        return set(set(spots)).issubset(self.players_home_positions[color])


    # Check for whether the piece is the furthest piece away from bearing off
    # This is relevant when the die shows 2, and the player tries to move
    # the innermost of the two places in home position. (1, 1) -> (1, 0) | 1 OFF

    # [1, 1] -> (7, 9)
    def is_src_furthest_piece(self, color, action):
        _, (src, dst) = action
        player_positions = [i["spot"] for i in self.get_players_positions()[color]]
        if color == self.white:
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
        if color == self.white and target > src:
            if self.bar[color] > 0:
                # Then we need to check if the move is moving the piece from the bar
                # And onto the board
                if src == self.bar[self.white] and (0 <= target < self.n_spots):
                    # Check if there are more than two enemies on the target
                    if self.board[target]["count"] > 1 and self.board[target]["color"] == self.get_opponent_color(color):
                        return False
                    # Check if there are 3 pieces on the spot - if so, then we cannot move
                    elif self.board[target]["count"] == self.max_n_stack:
                        return False
                    else:
                        return True

            elif self.board[src]["count"] >= 1 and self.board[src]["color"] == color:
                if 0 <= target < self.n_spots:
                    # If the target is within board limits, then we have to check
                    # If the target has two or more enemies, or the target reaches
                    # The upper limit of how many pieces can be stacked (3)
                    if self.board[target]["color"] != color and self.board[target]["count"] > 1:
                        return False
                    elif self.board[target]["color"] == color and self.board[target]["count"] == self.max_n_stack:
                        return False
                    else:
                        return True
                # If the target is not within the bounds of the board
                # Then we have to check whether or not the player can
                # Bear off
                elif self.can_bear_off(color):
                    # If the target is not self.n_spots, then check if the source piece
                    # Is the last piece of all pieces in home
                    if target > self.n_spots or target < -1:
                        if self.is_src_furthest_piece(color, action):
                            return True
                        else:
                            return False
                    
                    return True

            return False
        elif color == self.black and target < src:
            if self.bar[color] > 0:
                # Then we need to check if the move is moving the piece from the bar
                # And onto the board
                if src == self.bar_spots[self.black] and (0 <= target < self.n_spots):
                    # Check if there are more than two enemies on the target
                    if self.board[target]["count"] > 1 and self.board[target]["color"] == self.get_opponent_color(color):
                        return False
                    # Check if there are 3 pieces on the spot - if so, then we cannot move
                    elif self.board[target]["count"] == self.max_n_stack:
                        return False
                    else:
                        return True

            elif self.board[src]["count"] >= 1 and self.board[src]["color"] == color:
                if 0 <= target < self.n_spots:
                    # If the target is within board limits, then we have to check
                    # If the target has two or more enemies, or the target reaches
                    # The upper limit of how many pieces can be stacked (3)
                    if self.board[target]["color"] != color and self.board[target]["count"] > 1:
                        return False
                    elif self.board[target]["color"] == color and self.board[target]["count"] == self.max_n_stack:
                        return False
                    else:
                        return True
                # If the target is not within the bounds of the board
                # Then we have to check whether or not the player can
                # Bear off
                elif self.can_bear_off(color):
                    # If the target is not self.n_spots, then check if the source piece
                    # Is the last piece of all pieces in home
                    if target > self.n_spots or target < -1:
                        if self.is_src_furthest_piece(color, action):
                            return True
                        else:
                            return False
                    
                    return True

            return False
        else:
            return False

    def get_opponent_color(self, color):
        if color == self.white:
            return self.black
        else:
            return self.white

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
            # If the player can bear off (all home) and the target is not in
            # The normal range of spots, then move the player off
            if self.can_bear_off(color) and target not in range(self.n_spots):
                self.move_piece_off(color, action)
            elif self.board[target]["color"] == self.get_opponent_color(color) and self.board[target]["count"] == 1:
                # Adding the opponents piece to the bar and removing it from the target
                self.knock_out_piece(self.get_opponent_color(color), target)
                # Move the piece from the source to the target
                if src == self.bar_spots[color]:
                    self.move_from_bar(color, action)
                else:
                    self.move_piece_from_src_to_dest(color, action)
            elif src == self.bar_spots[color]:
                self.move_from_bar(color, action)
            else:
                # Move the piece from the source to the target
                self.move_piece_from_src_to_dest(color, action)

            self.non_used_dice.remove(roll)
            self.used_dice.append(roll)
            return True
        else:
            #print("ACTION IS NOT VALID")
            return False

    # The starting row variable is for when we are moving from bar
    def generate_single_action(self, src, starting_point, roll):
        actions = []
        # Add all actions where the die is added to the starting point
        # Add all actions where the die is subtracted from the starting point
        for die in roll:
            actions.append((die, (src, starting_point + die)))
            actions.append((die, (src, starting_point - die)))
        
        return list(set(actions))

    def generate_actions(self, color, roll):
        # First step must be to get all of the positions of the current player
        spots = [i["spot"] for i in self.get_players_positions()[color]]
        actions = []

        # For each spot, generate an action with the associated source spot
        for spot in spots:
            src = spot
            # Must check if the source is BAR, then the starting position is either
            # -1 or 8, depending on color
            if src == self.bar_spots[color]:
                # An example would be that if WHITE uses a die of value 1 from BAR
                # Then it will land on spot 0, therefore -1 is used
                if color == self.white:
                    temp_src = -1
                    temp_actions = self.generate_single_action(src, temp_src, roll)
                    actions.extend(temp_actions)
                # Same here, only black is moving the opposite direction
                # So the using a die of value 1 means landing on positions 8
                elif color == self.black:
                    temp_src = self.n_spots
                    temp_actions = self.generate_single_action(src, temp_src, roll)
                    actions.extend(temp_actions)
            # If the src spot is not the bar, then nothing extra needs to be 
            # Taken care of
            else:
                temp_actions = self.generate_single_action(src, src, roll)
                actions.extend(temp_actions)
            
        return list(set(actions))

    def render(self, round_nr):
        print(f"BLACK              ROUND: {round_nr}           WHITE")
        print("=============================================")
        #print(" B: {} | 0 | 1 | 2 | 3 | 4 | 5 | 6 | W: {}".format(self.off[BLACK], self.off[WHITE]))
        spot_string = "OFF: {}|".format(self.off[self.black])
        token_string = f"WBAR:{self.bar[self.white]}|"
        count_string = f"      |"
        for i in range(self.n_spots):
            token_string += f" {self.tokens[self.board[i]['color']]} |"
            count_string += f" {self.board[i]['count']} |"
            spot_string += f" {i} |"
        spot_string += "OFF: {}".format(self.off[self.white])
        token_string += f"BBAR:{self.bar[self.black]}"
        print(spot_string)
        print("---------------------------------------------")
        print(token_string)
        print(count_string)
        print("=============================================")

    def get_action_space(self):
        """
            The action space is defined by the number of spots a piece can move to other spots
        """
        nvec = [self.n_spots + 1 for i in range(2)]
        return nvec

    def get_observation_space(self):
        """
            The observation space is defined from the number of spots, the bar, the possible die rolls and the turn of the player
            Therefore we need to calculate these by using the static variables on top
        """
        spots = [self.max_n_stack * 2 + 1 for i in range(self.n_spots)]
        bar = [2 for i in range(2)]
        roll = [len(list(itertools.combinations_with_replacement(range(1, self.dice_sides + 1), 2)))]
        player_turn = [2]

        nvec = []

        # SPOTS
        nvec.extend(spots)
        # BAR
        nvec.extend(bar)
        # ROLL
        nvec.extend(roll)
        # PLAYER TURN
        nvec.extend(player_turn)

        return nvec

    def get_current_observation(self, current_player):
        """
            0 -> 0 Pieces 
            1 - (self.max_n_stack) -> 1 - (self.max_n_stack) White Pieces
            self.max_n_stack + 1 - 2*self.max_n_stack + 1 -> self.max_n_stack + 1 - 2*self.max_n_stack + 1 Black Pieces
        """
        observation = []
        for spot in self.board:
            if spot["color"] == self.white:
                observation.append(spot["count"])
            elif spot["color"] == self.black:
                observation.append(spot["count"] + self.max_n_stack)
            else:
                observation.append(spot["count"])

        # self.bar[COLOR] returns the count of how many are on the bar
        # Therefore we need to change it to only indicating whether there are zero, or 1 or more
        # On the bar for each color
        observation.append(0 if self.bar[self.white] == 0 else 1)
        observation.append(0 if self.bar[self.black] == 0 else 1)

        # combination_with_replacements returns the perfect values for our case
        dice_combinations = list(itertools.combinations_with_replacement(range(1, self.dice_sides + 1), 2))
        # sorted sorts the items and the tuple then makes it a tuple - Which is needed for
        # finding the tuple in the dice_combinations list of tuples.
        observation.append(dice_combinations.index(tuple(sorted(self.dice))))

        observation.append(current_player)
        
        return observation


if __name__ == '__main__':
    bg = Backgammon()
    print(bg.get_current_observation(0))

    
    bg = Backgammon()
    agent = 0
    bg.render(0)
    for r in range(50):
        bg.roll()
        print("AGENT:", bg.colors[agent])
        print("ROLL:", bg.non_used_dice)
        for _ in bg.non_used_dice:
            actions = bg.generate_actions(agent, bg.non_used_dice)
            print("ACTIONS:", actions)
            print("VALID ACTIONS")
            for a in actions:
                if bg.is_valid(agent, a):
                    print(a)
            executed = False
            for _ in actions:
                action = random.choice(actions)
                executed = bg.execute_action(agent, action)
                if executed:
                    print("ACTION DONE:", action)
                    break
                else:
                    print("ACTION NOT DONE:", action)
                    actions.remove(action)
            print("LEN NON USED DICE:", len(bg.non_used_dice))
            
        bg.render(r)
        if bg.off[agent] == bg.n_pieces:
            print(bg.colors[agent], "WON!")
            break
        agent = bg.get_opponent_color(agent)
        print("\n")
    


"""

    def skip_board(self):
        board = [{"spot": k, "count": 0, "color": None} for k, i in enumerate(range(N_SPOTS))]
        board[0].update({"count": 2, "color": WHITE})
        board[1].update({"count": 2, "color": BLACK})
        board[2].update({"count": 2, "color": BLACK})

        # A counter for how many has been moved to the bar
        bar = {WHITE: 0, BLACK: 0}
        # Only a counter for how many has been beared off
        off = {WHITE: 0, BLACK: 0}

        return board, bar, off

    def bear_off_board_setup(self):
        board = [{"spot": k, "count": 0, "color": None} for k, i in enumerate(range(N_SPOTS))]
        board[0].update({"count": 2, "color": BLACK})
        board[1].update({"count": 3, "color": BLACK})
        board[3].update({"count": 3, "color": WHITE})
        board[6].update({"count": 2, "color": WHITE})

        # A counter for how many has been moved to the bar
        bar = {WHITE: 0, BLACK: 0}
        # Only a counter for how many has been beared off
        off = {WHITE: 0, BLACK: 0}
        
        return board, bar, off

    def bar_play_board_setup(self):
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
"""