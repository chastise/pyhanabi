from engine.card import Card
import random

class Deck(object):

    def __init__(self, colors=('r', 'y', 'g', 'w', 'b'), numbers=(1, 1, 1, 2, 2, 3, 3, 4, 4, 5), seed=None):
        if len(colors) < 1:
            raise ValueError("Decks must have at least one card color.")
        if len(numbers) < 1:
            raise ValueError("Decks must have at least one card number.")
        self.card_colors = colors
        self.card_numbers = numbers

        self.card_list = []
        for color in self.card_colors:
            for number in self.card_numbers:
                self.card_list.append(Card(number, color))


    def __len__(self):
        return len(self.card_list)

    def __str__(self):
        return "Deck: {card_list}".format(card_list=self.card_list)

    def __repr__(self):
        return str(self)

    def shuffle(self, seed=None):
        if seed:
            random.seed(seed)
        random.shuffle(self.card_list)

    def draw_card(self):
        if len(self.card_list) > 0:
            return self.card_list.pop()
        else:
            raise IndexError("Cannot draw card from an empty deck.")
