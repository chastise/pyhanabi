from engine.card import Card
from random import shuffle, Random

class Deck(object):

    def __init__(self, colors, values=(1, 1, 1, 2, 2, 3, 3, 4, 4, 5), seed=False):
        self.colors = colors

        deck = []

        for color in self.colors:
            for value in values:
                deck.append(Card(value, color))

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
        return self.colors
