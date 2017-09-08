from engine.player import Player
from engine.move import Move
from players.shared.util import *

import random


class HeuristicPlayer(Player):
    """An AI that uses heuristic techniques to choose moves."""

    def __str__(self):
        return "HeuristicPlayer"

    def make_move(self, game_state):
        raise NotImplementedError


class PointsHeuristicPlayer(Player):
    """An AI that uses heuristic techniques to choose moves."""

    def __str__(self):
        return "PointsHeuristicPlayer"

    def make_move(self, game_state):
        all_moves = construct_all_legal_moves(game_state)
        for move in all_moves:
            if move.move_type == 'play' and card_plays_for_points(game_state, game_state.get_my_hand()[move.card_index]):
                return move
        return random.choice(all_moves)


class GenerousPointsHeuristicPlayer(Player):
    """An AI that uses heuristic techniques to choose moves."""

    def __str__(self):
        return "GenerousPointsHeuristicPlayer"

    def make_move(self, game_state):
        all_moves = construct_all_legal_moves(game_state)
        play_moves, info_moves, discard_moves = split_moves_by_type(all_moves)
        for move in play_moves:
            if card_plays_for_points(game_state, game_state.get_my_hand()[move.card_index]):
                return move
        if game_state.board.clock_tokens > 0:
            for move in info_moves:
                if does_information_reveal_unknown(game_state, move):
                    return move
        # elif game_state.board.clock_tokens == 0:
        #     for move in discard_moves:
        #         return move

        return random.choice(all_moves)
