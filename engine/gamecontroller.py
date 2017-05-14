from engine.board import Board
from engine.deck import Deck
from engine.player import Player
from engine.move import Move
from engine.gamestate import GameState, PlayerGameState
from itertools import cycle


class GameController(object):
    """Takes a list containing each player, as well as a seed for the deck."""

    def __init__(self, players, deck_seed=False):
        num_players = len(players)
        if not 2 <= num_players <= 5:
            raise ValueError("There must be between 2 and 5 players to play Hanabi.")
        for player in players:
            if not isinstance(player, Player):
                raise ValueError("All players must inherit from the Player class.")
        self.colors = ('r', 'y', 'g', 'w', 'b')  # TODO: rainbow/mixed/wilds
        self.numbers = (1, 1, 1, 2, 2, 3, 3, 4, 4, 5)
        self.players = players
        self.deck = Deck(colors=self.colors, numbers=self.numbers)
        self.deck.shuffle(seed=None)
        self.player_hands = [[] for _ in range(len(self.players))]
        self.master_game_state = GameState(Board(self.deck), self.player_hands)

    def deal_initial_hand(self):
        cards_to_deal = 5
        if len(self.players) > 3:
            cards_to_deal = 4
        for rounds in range(cards_to_deal):
            for player in range(len(self.players)):
                self.player_hands[player].append(self.deck.draw_card())
        self.master_game_state.player_hands = self.player_hands

    def game_over(self, current_player, game_state=None):
        if game_state is None:
            game_state=self.master_game_state
        # Check if we blew up
        if game_state.board.fuse_tokens < 1:
            # print("no more fuses")
            return True
        # Check if we've completed all the stacks
        MAX_STACK_SCORE = 5 # Todo: figure out a better place for a global var like this
        if game_state.board.compute_score() == (len(self.colors)*MAX_STACK_SCORE):
            # print("You win!")
            return True
        # Check if the deck is done and everyone played their final turn:
        if len(self.deck) == 0 and current_player == game_state.board.game_almost_over:
            # print("game almost over")
            #print(player_id)
            return True
        # Otherwise, the engine is not over
        return False

    # Turn order: move, check end, draw card, initiate final round, next player
    def play_game(self):
        self.deal_initial_hand()
        self.master_game_state.board.deck_size = len(self.deck)
        for player_id in cycle(range(len(self.players))):
            player_game_state = PlayerGameState(self.master_game_state, player_id)
            new_move = self.players[player_id].make_move(player_game_state)
            assert isinstance(new_move, Move)
            try:
                self.master_game_state = new_move.apply(self.master_game_state)
            except AssertionError, e:
                raise Exception(
                    "{p} submitted unplayable move: {m}".format(p=str(self.players[player_id]), m=str(new_move)), e)
            if self.game_over(player_id):
                game_score = self.master_game_state.board.compute_score()
                print("Game over: Score {score}".format(score=game_score))
                return game_score
            if len(self.deck) > 0:
                self.player_hands[player_id].append(self.deck.draw_card())
                self.master_game_state.player_hands = self.player_hands
                self.master_game_state.board.deck_size = len(self.deck)
            # This triggers when the last card is drawn, every player including this one takes one more turn.
            if len(self.deck) == 0 and self.master_game_state.board.game_almost_over is None:
                self.master_game_state.board.game_almost_over = player_id
