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

        self.bar_spot = self.n_spots
        self.off_spot = self.n_spots

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

    def custom_board(self):
        """ 
            Use this function for creating your own custom board for the backgammon game
            Take inspiration from the function above
        """
        ...

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
            players_positions[self.white].append({"spot": self.n_spots, "count": self.bar[self.white], "color": self.white})
        
        if self.bar[self.black] > 0:
            players_positions[self.black].append({"spot": self.n_spots, "count": self.bar[self.black], "color": self.black})
        
        return players_positions

    def can_bear_off(self, color):
        # Checks if there are any pieces on the bar
        if self.bar[color] > 0:
            #print("CANNOT BEAR OFF -> BAR NOT EMPTY")
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
        roll, (src, dst) = action
        player_positions = [i["spot"] for i in self.get_players_positions()[color]]
        if set(player_positions).issubset(self.players_home_positions[color]):
            if color == self.white:
                # It is min() for white because their home are at end of board
                if len(player_positions) > 0 and src == min(player_positions):
                    return True
                else:
                    return False
            else:
                # It is max() for BLACK because their home are at the start of board
                if len(player_positions) > 0 and src == max(player_positions) and src != self.bar_spot:
                    return True
                else:
                    return False
        return False


    def new_is_valid(self, color, action):
        roll, (src, target) = action

        # 1, (4, 5)
        # (2, 1)

        if not self.can_bear_off(color) and target == self.off_spot:
            return False

        # If the roll is not in the non_used_dice, then it cannot use the action
        if abs(roll) not in self.non_used_dice:
            return False

        if color == self.white:
            if not self.is_src_furthest_piece(color, action) and roll + src > self.off_spot:
                if src != self.bar_spot:
                    return False
                
        elif color == self.black:
            if not self.is_src_furthest_piece(color, action) and src - roll < -1:
                return False
        
        # If the target has more than two enemies, then it cannot move there.
        if target != self.n_spots and self.board[target]["count"] >= 2 and self.board[target]["color"] == self.get_opponent_color(color):
            return False

        # (7, 1)
        if color == self.white and src != self.bar_spot:
            # If the color is white, then the target must be smaller than the source
            # So if it is the same or bigger, then return False

            if target <= src:
                return False
        
        elif color == self.black and target != self.off_spot:
            # If the target is smaller or the same as src, then action cannot be done
            if target >= src:
                return False

        # First check if someone is on the bar
        if self.bar[color] > 0:
            # IF someone is on the bar, then the source must be n_sptos
            if src != self.bar_spot:
                return False

        elif self.bar[color] == 0:
            if src == self.bar_spot:
                return False

        if src != self.n_spots and self.board[src]["color"] != color:
            return False
        
        if src != self.n_spots and self.board[src]["count"] == 0:
            return False

        # If none of the conditions above is satisfied, then the action can be done.
        return True

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
        roll, (src, target) = action
        src_piece_count = self.board[src]["count"]
        if src_piece_count < 1:
            raise RuntimeError("Cannot move from spot because there are no pieces left")
        
        self.remove_piece_from_src(color, src)
        self.add_piece_to_dst(color, target)
        
    def move_piece_off(self, color, action):
        roll, (src, target) = action
        # Remove piece from src
        self.remove_piece_from_src(color, src)
        # Add piece to "OFF"
        self.off[color] += 1

    def move_from_bar(self, color, action):
        roll, (src, target) = action
        # Decrement the bar counter
        self.bar[color] -= 1
        # Move the piece onto the board
        self.add_piece_to_dst(color, target)
        

    def alternate_execute_action(self, color, action):

        roll, (src, target) = action
    
        # If the action is true
        if self.new_is_valid(color, action):
            # Check if there is an opponent piece on the target
            # If the player can bear off (all home) and the target is not in
            # The normal range of spots, then move the player off
            if self.can_bear_off(color) and target == self.n_spots:
                self.move_piece_off(color, action)
            elif self.board[target]["color"] == self.get_opponent_color(color) and self.board[target]["count"] == 1:
                # Adding the opponents piece to the bar and removing it from the target
                self.knock_out_piece(self.get_opponent_color(color), target)
                # Move the piece from the source to the target
                if src == self.n_spots and self.bar[color] > 0:
                    self.move_from_bar(color, action)
                else:
                    self.move_piece_from_src_to_dest(color, action)
            elif src == self.n_spots:
                self.move_from_bar(color, action)
            else:
                # Move the piece from the source to the target
                self.move_piece_from_src_to_dest(color, action)

            self.non_used_dice.remove(abs(roll))
            self.used_dice.append(roll)
            return True
        else:
            #print("ACTION IS NOT VALID")
            return False

    def alternate_generate_actions(self, color):
        normal = list(itertools.combinations_with_replacement(range(8), 2))
        rev = list(itertools.combinations_with_replacement(reversed(range(8)), 2))
        temp = normal + rev

        

        final = []

        for idx, i in enumerate(reversed(range(self.n_spots)[self.n_spots - self.n_home_positions:])):
            for index, die in enumerate(range(self.dice_sides - idx)):
                final.append((range(self.dice_sides, 0, -1)[index], (i, self.n_spots)))

        for idx, i in enumerate(range(self.n_spots)[:self.n_home_positions]):
            for index, die in enumerate(range(self.dice_sides - idx)):
                final.append((range(self.dice_sides, 0, -1)[index], (i, self.n_spots)))

        for action in temp:
            src, dst = action
            if color == self.white:
                if action[0] == 7:
                    final.append((dst - (-1), (action)))
                else:
                    final.append((dst - src, (action)))
            else:
                if action[0] == 7:
                    final.append((src - dst, (action)))
                elif action[1] == 7:
                    final.append((-1 - src, (action)))
                else:
                    final.append((dst - src, (action)))

        return list(set(final))

    def get_valid_actions(self, color):
        all_actions = self.alternate_generate_actions(color)

        valid_actions = []

        for action in all_actions:
            if self.new_is_valid(color, action):
                valid_actions.append(action)

        return valid_actions


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
        roll_1 = [2]
        roll_2 = [2]

        nvec = []

        # SPOTS
        nvec.extend(spots)
        # BAR
        nvec.extend(bar)
        # AVAILABLE DICE
        # TODO: Undo hardcoded
        nvec.extend(roll_1)
        nvec.extend(roll_2)

        return nvec

    def get_current_observation(self):
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

        for side in range(1, self.dice_sides + 1):
            spotted = False
            for die in self.non_used_dice:
                if side == die:
                    spotted = True
            if spotted:
                observation.append(1)
            else:
                observation.append(0)

        return observation


if __name__ == '__main__':

    bg = Backgammon()
    print(bg.non_used_dice)
    print(bg.get_current_observation(0))

    
"""    bg = Backgammon()
    agent = 0
    bg.render(0)
    for r in range(10000):
        bg.roll()
        print("AGENT:", bg.colors[agent])
        print("ROLL:", bg.non_used_dice)
        print(bg.players_home_positions[agent])
        print(bg.get_players_positions())
        print(bg.can_bear_off(agent))
        for _ in range(len(bg.non_used_dice)):
            actions = bg.alternate_generate_actions(agent)
            print(actions)
            for action in actions:
                if bg.new_is_valid(agent, action):
                    print("Valid:", action)
            executed = False
            for _ in range(len(actions)):
                action = random.choice(actions)
                executed = bg.alternate_execute_action(agent, action)
                if executed:
                    print("ACTION DONE:", action)
                    break
                else:
                    actions.remove(action)

            #print("LEN NON USED DICE:", len(bg.non_used_dice))
            
        bg.render(r)
        if bg.off[agent] == bg.n_pieces:
            print(bg.colors[agent], "WON!")
            break
        agent = bg.get_opponent_color(agent)
        print("\n")"""


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
