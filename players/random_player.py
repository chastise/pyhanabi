from engine.player import Player
from players.shared.util import construct_all_legal_moves

import random


class RandomPlayer(Player):
    """A real dumb AI player"""

    def __str__(self):
        return "RandomPlayer"

    def make_move(self, game_state):
        return self.make_random_legal_move(game_state)

    def make_random_legal_move(self, game_state):
        chosen_move = random.choice(construct_all_legal_moves(game_state))
        assert chosen_move.is_playable(game_state)
        return chosen_move
