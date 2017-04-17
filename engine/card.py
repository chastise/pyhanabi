class Card(object):
    def __init__(self, number, color):
        self._number = number
        self._color = color
        self.public_color = False
        self.public_number = False
        self.in_your_hand = False

    # Not sure if needed
    def __eq__(self, other):
        if type(other) != Card:
            return False
        return self._number == other.number and self._color == other.color

    def __str__(self):
        return "Card(" + str(self._number) + str(self._color) + ", Public:" + str(self.public_number) + str(self.public_color) + ")"

    def __repr__(self):
        return str(self)

    def make_public(self, type):
        if type == 'color':
            self.public_color = self._color # Todo: Rainbow/wild color management
        elif type == 'number':
            self.public_number = self._number
        else:
            raise Exception("type must be either 'color' or 'number'")

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value



class YourCard(Card):
    def __init__(self, card):
        self._number = False
        self._color = False
        self.public_number = card.public_number
        self.public_color = card.public_color
        self.in_your_hand = True

    def __str__(self):
        return "Card(unknown,Public:" + str(self.public_number) + str(self.public_color) + ")"

    def __repr__(self):
        return str(self)