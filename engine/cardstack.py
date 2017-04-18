class CardStack(object):
    """Card stacks are created for each color at the beginning of the game."""

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
