from engine.move import Move
from engine.gamestate import PlayerGameState


def construct_all_legal_moves(game_state):
    moves = []
    my_hand = game_state.get_my_hand()
    # all discards and all plays
    for card_index in range(len(my_hand)):
        moves.append(Move('discard', game_state.player_id, card_index=card_index))
        moves.append(Move('play', game_state.player_id, card_index=card_index))

    # all information that could be given
    # Ensure info tokens exist before we bother constructing info moves
    if game_state.board.clock_tokens > 0:
        for pid in range(len(game_state.player_hands)):
            if pid != game_state.player_id:
                card_colors = set([])
                card_numbers = set([])
                hand = game_state.player_hands[pid]
                for card_index in range(len(hand)):
                    card_colors.add(hand[card_index].color)
                    card_numbers.add(hand[card_index].number)
                for color in card_colors:
                    moves.append(Move('give_information',
                                      game_state.player_id,
                                      information={'player_id': pid,
                                                   'information_type': 'color',
                                                   'information': color}))
                for number in card_numbers:
                    moves.append(Move('give_information',
                                      game_state.player_id,
                                      information={'player_id': pid,
                                                   'information_type': 'number',
                                                   'information': number}))

    return moves

# Warning: Will construct a state with multiple YourCard hands.
def construct_next_game_state_from_pgs(game_state, move):
    current_player = game_state.player_id
    next_player = current_player + 1
    if next_player > len(game_state.player_hands):
        next_player = 0
    new_game_state = move.apply(game_state)
    new_game_state = PlayerGameState(new_game_state, next_player)
    # Adjust last-player-hand to not be "in_your_hand"
    last_hand = new_game_state.player_hands[current_player]
    for card in last_hand:
        card.in_your_hand = False
    print(new_game_state)
    return new_game_state
