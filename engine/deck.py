from engine.card import Card
from random import shuffle, Random

class Deck(object):

    def __init__(self, colors=('r', 'y', 'g', 'w', 'b'), numbers=(1, 1, 1, 2, 2, 3, 3, 4, 4, 5), seed=False):
        self.card_colors = colors
        self.card_numbers = numbers

        deck = []

        for color in self.card_colors:
            for number in self.card_numbers:
                deck.append(Card(number, color))

        self.deck = deck

        if seed:
            Random(seed).shuffle(self.deck)
        else:
            shuffle(self.deck)

    def __len__(self):
        return len(self.deck)

    def __repr__(self):
        return "Deck: {cardlist}".format(cardlist=[c for c in self.deck])

    def draw_card(self):
        if len(self.deck) > 0:
            return self.deck.pop()
        return False

    def _get_deck(self):
        return self.deck

    def get_deck_size(self):
        return len(self.deck)

    def get_num_cards_remaining(self):
        return len(self.deck)

    def get_deck_colors(self):
        return self.card_colors

    def get_deck_numbers(self):
        return self.card_numbers
