from engine.card import Card
from random import shuffle, Random

class Deck(object):

    def __init__(self, colors, seed=False):
        self.colors = colors

        deck = []

        # Not sure if this would look prettier rolled into more loops
        for color in self.colors:
            deck.append(Card(1, color))
            deck.append(Card(1, color))
            deck.append(Card(1, color))
            deck.append(Card(2, color))
            deck.append(Card(2, color))
            deck.append(Card(3, color))
            deck.append(Card(3, color))
            deck.append(Card(4, color))
            deck.append(Card(4, color))
            deck.append(Card(5, color))

        self.deck = deck

        if seed:
            Random(seed).shuffle(self.deck)
        else:
            shuffle(self.deck)


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
