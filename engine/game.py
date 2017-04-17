from engine.card import Card, YourCard
from engine.deck import Deck
from engine.player import Player
from engine.move import Move
from itertools import cycle
import copy


class Game(object):
    """Takes a list containing each player, as well as parameters for the engine."""
    def __init__(self, players, deck_seed=False):
        num_players = len(players)
        if not 2 <= num_players <= 5:
            raise Exception("There must be between 2 and 5 players")
        for player in players:
            if not isinstance(player, Player):
                raise Exception("All players must inherit from the Player class.")
        self.colors = ('r', 'y', 'g', 'w', 'b') #todo: rainbow/mixed/wilds
        self.players = players
        self.deck = Deck(self.colors, seed=deck_seed)
        self.player_hands = [[] for _ in range(len(self.players))]
        self.master_game_state = GameState(Board(self.colors,
                                                 self.deck.get_deck_size(),
                                                 range(len(self.players))),
                                                 self.player_hands
                                           )
        self.game_almost_over = None

    def deal_initial_hand(self):
        cards_to_deal = 5
        if len(self.players) < 3:
            cards_to_deal = 4
        for rounds in range(cards_to_deal):
            for player in range(len(self.players)):
                self.player_hands[player].append(self.deck.draw_card())
        self.master_game_state.player_hands = self.player_hands

    def game_over(self, player_id):
        # Check if we blew up
        if self.master_game_state.board.count_fuse_tokens() < 1:
            print("no more fuses")
            return True
        # Check if we've completed all the stacks
        completed_stacks = 0
        for color, stack in self.master_game_state.board.card_stacks.iteritems():
            if stack.is_complete():
                completed_stacks += 1
        if completed_stacks == len(self.colors):
            print("You win!")
            return True
        # Check if the deck is done and everyone played their final turn:
        if player_id == self.game_almost_over:
            print("game almost over")
            print(player_id)
            return True
        # Otherwise, the engine is not over
        return False

    # Turn order: move, check end, draw card, initiate final round, next player
    def play_game(self):
        self.deal_initial_hand()
        self.master_game_state.board.update_deck_size(self.deck.get_deck_size())
        for player_id in cycle(range(len(self.players))):
            player_game_state = PlayerGameState(self.master_game_state, player_id)
            new_move = self.players[player_id].make_move(player_game_state)
            assert isinstance(new_move, Move)
            try:
                self.master_game_state = new_move.apply(self.master_game_state)
            except AssertionError, e:
                raise Exception("{p} submitted unplayable move: {m}".format(p=str(self.players[player_id]), m=str(new_move)), e)
            if self.game_over(player_id):
                game_score = self.master_game_state.board.compute_score()
                print("Game over: Score {score}".format(score=game_score))
                return game_score
            if self.deck.get_deck_size() > 0:
                self.player_hands[player_id].append(self.deck.draw_card())
                self.master_game_state.player_hands = self.player_hands
                self.master_game_state.board.update_deck_size(self.deck.get_deck_size())
            # This triggers when the last card is drawn, every player including this one takes one more turn.
            if self.deck.get_deck_size() == 0 and self.game_almost_over == None:
                self.game_almost_over = player_id


class Board(object):
    def __init__(self, colors, deck_size, player_ids):
        self.deck_size = deck_size
        self.clock_tokens = 8
        self.MAX_CLOCK_TOKENS = 8
        self.fuse_tokens = 3 # No 4th token for clearer logic
        self.card_stacks = {}
        self.deck_colors = colors
        for color in self.deck_colors:
            self.card_stacks[color] = CardStack(color)
        self.discard = []
        self.discard_stats = {}
        for color in self.deck_colors:
            self.discard_stats[color] = [0] * 5

    #def __str__(self):

    def __repr__(self):
        return "Deck Size: {deck_size}, Clock Tokens: {clock_tokens}, Fuse Tokens: {fuse_tokens}, Card Stacks: {card_stacks}\n"\
            "Discard Stats: {discard}".format(deck_size=self.get_remaining_cards(),
                                                clock_tokens=self.count_clock_tokens(),
                                                fuse_tokens=self.count_fuse_tokens(),
                                                card_stacks=[stack for stack in self.card_stacks.values()],
                                                discard=self.discard_stats
                                        )

    def discard_card(self, card):
        assert isinstance(card, Card)
        self.discard.append(card)
        self.discard_stats[card.color][card.number-1] += 1

    def get_remaining_cards(self):
        return self.deck_size

    def count_clock_tokens(self):
        return self.clock_tokens

    def count_fuse_tokens(self):
        return self.fuse_tokens

    def use_clock_token(self):
        assert self.clock_tokens > 0
        self.clock_tokens -= 1

    def use_fuse_token(self):
        assert self.fuse_tokens > 0
        self.fuse_tokens -= 1

    def add_clock_token(self):
        if self.clock_tokens < self.MAX_CLOCK_TOKENS:
            self.clock_tokens += 1

    def get_card_stack(self, color):
        assert self.card_stacks.has_key(color)
        return self.card_stacks[color]

    def update_deck_size(self, new_deck_size):
        self.deck_size = new_deck_size

    def compute_score(self):
        total_score = 0
        for stack in self.card_stacks.values():
            total_score += stack.get_score()
        return total_score


class CardStack(object):
    """Card stacks are created for each color at the beginning of the engine."""
    def __init__(self, color):
        self.color = color
        self.cards_played = []

    def __repr__(self):
        return "CardStack: {color}, {current_top}".format(color=self.color, current_top=len(self.cards_played))

    def play(self, card):
        try:
            assert self.is_legal_play(card)
        except AssertionError, e:
            raise Exception("Invalid play, ", e)
        self.cards_played.append(card)

    def is_legal_play(self, card):
        try:
            assert card.color == self.color
        except AssertionError, e:
            # This is an exception because stacks are looked up by color, so this should not happen.
            raise Exception("Attempted to put a card on the wrong color stack. ", e)
        return card.number == len(self.cards_played) + 1

    def get_score(self):
        return len(self.cards_played)

    def is_complete(self):
        return self.get_score() == 5



class GameState(object):
    def __init__(self, board, player_hands):
        self.num_players = len(player_hands)
        self.board = board
        self.player_hands = player_hands
        #Todo: Better and safer accessors for player_hands


class PlayerGameState(GameState):
    def __init__(self, game_state, player_id):
        super(PlayerGameState, self).__init__(game_state.board, game_state.player_hands)
        # Add PlayerGameState-only info:
        self.player_id = player_id
        # Sanitize attributes that players shouldn't be able to cheat with:
        self.board = copy.deepcopy(game_state.board)
        hands = game_state.player_hands
        self.player_hands = [copy.deepcopy(hands[hand]) if hand != player_id else [YourCard(card) for card in hands[hand]] for hand in range(len(hands))]

    def get_my_hand(self):
        return self.player_hands[self.player_id]

    def get_my_id(self):
        return self.player_id
