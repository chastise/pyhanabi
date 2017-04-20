from engine.player import Player
from engine.move import Move

import random


class RandomPlayer(Player):
    """A real live human player"""

    def __str__(self):
        return "RandomPlayer"

    def make_move(self, game_state):
        return self.make_random_legal_move(game_state)

    def make_random_legal_move(self, game_state):
        chosen_move = random.choice(self.construct_all_legal_moves(game_state))
        try:
            assert chosen_move.is_playable(game_state)
        except AssertionError:
            print "Chosen move was unplayable: {move} ;".format(move=chosen_move)
            print(game_state.board)
            print(game_state.player_hands)
            print(game_state.player_id)
            chosen_move.is_playable(game_state)
        return chosen_move

    def construct_all_legal_moves(self, game_state):
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
