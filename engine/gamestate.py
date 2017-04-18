from engine.card import YourCard
import copy

class GameState(object):
    def __init__(self, board, player_hands):
        self.num_players = len(player_hands)
        self.board = board
        self.player_hands = player_hands


class PlayerGameState(GameState):
    def __init__(self, game_state, player_id):
        super(PlayerGameState, self).__init__(game_state.board, game_state.player_hands)
        # Add PlayerGameState-only info:
        self.player_id = player_id
        # Sanitize attributes that players shouldn't be able to cheat with:
        self.board = copy.deepcopy(game_state.board)
        hands = game_state.player_hands
        self.player_hands = [
            copy.deepcopy(hands[hand]) if hand != player_id else [YourCard(card) for card in hands[hand]] for hand in
            range(len(hands))]

    def get_my_hand(self):
        return self.player_hands[self.player_id]

    def get_my_id(self):
        return self.player_id