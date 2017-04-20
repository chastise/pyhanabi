from engine.player import Player
from engine.move import Move


class HeuristicPlayer(Player):
    """An AI that uses heuristic techniques to choose moves."""

    def __str__(self):
        return "HeuristicPlayer"

    def make_move(self, game_state):
        raise NotImplementedError
