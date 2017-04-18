class Card(object):
    def __init__(self, number, color):
        self.number = number
        self.color = color
        self.public_color = False
        self.public_number = False
        self.in_your_hand = False

    def __eq__(self, other):
        if type(other) != Card:
            return False
        return self.number == other.number and self.color == other.color

    def __str__(self):
        return "Card({number}:{color}, Public:{public_number}:{public_color})".format(number=self.number,
                                                                                      color=self.color,
                                                                                      public_number=self.public_number,
                                                                                      public_color=self.public_color)

    def __repr__(self):
        return str(self)

    def make_public(self, information_type):
        if information_type == 'color':
            self.public_color = self.color  # Todo: Rainbow/wild color management
        elif information_type == 'number':
            self.public_number = self.number
        else:
            raise Exception("type must be either 'color' or 'number'")


class YourCard(Card):
    def __init__(self, card):
        self._number = False
        self._color = False
        self.public_number = card.public_number
        self.public_color = card.public_color
        self.in_your_hand = True

    def __str__(self):
        return "Card(?:?,Public:{public_number}:{public_color})".format(public_number=self.public_number,
                                                                        public_color=self.public_color)

    def __repr__(self):
        return str(self)

    def make_public(self, type):
        raise Exception("Cannot make YourCards public because actual attributes are hidden.")

