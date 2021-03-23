

def flip_observation(observation: list, n_pieces: int, n_spots: int) -> list:

    # First reverse the observation
    rev_obs = list(reversed(observation))

    # Then flip the number of players based on the n_pieces variable
    flipped_obs = []

    for o in rev_obs:
        if o > n_pieces:
            flipped_obs.append(o - n_pieces)
        elif o > 0 and o <= n_pieces:
            flipped_obs.append(o + n_pieces)
        else:
            flipped_obs.append(o)
    
    # Now the observation has been flipped
    return flipped_obs

def flip_action(action: tuple, n_spots: int) -> tuple:
    # This takes in an action that is based on a flipped observation
    # It then reverses the flipped action into an ordinary action

    rev_board_indices = list(reversed(range(n_spots)))

    flipped_action = (rev_board_indices[action[0]], rev_board_indices[action[1]])

    return flipped_action