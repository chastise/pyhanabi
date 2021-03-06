from engine.card import Card, YourCard
from cardstack import CardStack

class Board(object):
    def __init__(self, deck):
        self.deck_size = len(deck)
        self.clock_tokens = 8
        self.MAX_CLOCK_TOKENS = 8
        self.fuse_tokens = 3  # No 4th token for clearer logic
        self.card_stacks = {}
        self.deck_colors = deck.card_colors
        self.deck_numbers = deck.card_numbers
        self.game_almost_over = None

        for color in self.deck_colors:
            self.card_stacks[color] = CardStack(color)
        self.discard = []
        self.discard_stats = {}
        for color in self.deck_colors:
            self.discard_stats[color] = {}
            for number in set(self.deck_numbers):
                self.discard_stats[color][number] = 0

    def __str__(self):
        return "Deck Size: {deck_size}, Clock Tokens: {clock_tokens}, Fuse Tokens: {fuse_tokens}, " \
               "Card Stacks: {card_stacks}\nDiscard Stats: {discard}".format(deck_size=self.deck_size,
                                                                             clock_tokens=self.clock_tokens,
                                                                             fuse_tokens=self.fuse_tokens,
                                                                             card_stacks=[stack for stack in
                                                                                          self.card_stacks.values()],
                                                                             discard=self.discard_stats
                                                                             )

    def __repr__(self):
        return str(self)

    def discard_card(self, card):
        assert isinstance(card, Card)
        self.discard.append(card)
        if not isinstance(card, YourCard): # Because YourCard may not know it's number/color
            self.discard_stats[card.color][card.number] += 1

    def get_count_discarded(self, card):
        assert isinstance(card, Card)
        return self.discard_stats[card.color][card.number]

    def use_clock_token(self):
        assert self.clock_tokens > 0
        self.clock_tokens -= 1

    def use_fuse_token(self):
        if self.fuse_tokens < 1:
            raise Exception("Cannot reduce fuse tokens, current board: {board}".format(board=self))
        self.fuse_tokens -= 1

    def add_clock_token(self):
        if self.clock_tokens < self.MAX_CLOCK_TOKENS:
            self.clock_tokens += 1

    def get_card_stack(self, color):
        assert color in self.card_stacks.keys()
        return self.card_stacks[color]

    def compute_score(self):
        total_score = 0
        for stack in self.card_stacks.values():
            total_score += stack.get_score()
        return total_score
