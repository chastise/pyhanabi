from engine.move import Move
from engine.card import Card
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


def split_moves_by_type(all_moves_list):
    play_moves = [move for move in all_moves_list if move.move_type == 'play']
    info_moves = [move for move in all_moves_list if move.move_type == 'give_information']
    discard_moves = [move for move in all_moves_list if move.move_type == 'discard']
    return (play_moves, info_moves, discard_moves)


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


# Will identify whether a play can earn points. False if not or if unsure.
def card_plays_for_points(game_state, card):
    assert isinstance(card, Card)
    if card.public_color is None or card.public_number is None:
        return False
    else:
        return len(game_state.board.card_stacks[card.public_color].cards_played) == card.public_number


def does_information_reveal_unknown(game_state, move):
    assert move.is_playable(game_state)
    assert move.move_type == 'give_information'
    target_player_hand = game_state.player_hands[move.information['player_id']]
    cards_revealed = 0
    if move.information['information_type'] == 'color':
        color = move.information['information']
        for card in target_player_hand:
            if card.color == color and card.public_color is None:
                cards_revealed += 1
    else:
        number = move.information['information']
        for card in target_player_hand:
            if card.number == number and card.public_number is None:
                cards_revealed += 1
    return cards_revealed > 0
