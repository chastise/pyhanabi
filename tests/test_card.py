from engine.card import Card, YourCard
import pytest
import unittest

class TestCard(unittest.TestCase):
    def test_init(self):
        card_1 = Card(2, 'b')
        assert card_1.color == 'b'
        assert card_1.number == 2
        self.assertIsNone(card_1.public_number)
        self.assertIsNone(card_1.public_color)
        self.assertIs(card_1.in_your_hand, False)

    def test_eq_true(self):
        card_1 = Card(1, 'y')
        card_2 = Card(1, 'y')
        assert card_1 == card_2

    def test_eq_false_number(self):
        card_1 = Card(1, 'y')
        card_2 = Card(2, 'y')
        assert card_1 != card_2

    def test_eq_false_color(self):
        card_1 = Card(1, 'y')
        card_2 = Card(1, 'b')
        assert card_1 != card_2

    def test_eq_true_despite_public(self):
        card_1 = Card(1, 'g')
        card_2 = Card(1, 'g')
        card_2.make_public('color')
        assert card_1 == card_2

    def test_make_public_color(self):
        card_1 = Card(5, 'b')
        card_1.make_public('color')
        assert card_1.public_color == 'b'

    def test_make_public_number(self):
        card_1 = Card(3, 'y')
        card_1.make_public('number')
        assert card_1.public_number == 3

    def test_make_public_invalid_input(self):
        card_1 = Card(1, 'g')
        with pytest.raises(ValueError):
            card_1.make_public('flavor')


class TestYourCard(unittest.TestCase):
    def test_init(self):
        card_1 = Card(2, 'b')
        your_card_1 = YourCard(card_1)
        self.assertIs(your_card_1.number, False)
        self.assertIs(your_card_1.color, False)
        self.assertIsNone(your_card_1.public_number)
        self.assertIsNone(your_card_1.public_color)
        self.assertIs(your_card_1.in_your_hand, True)

    def test_cannot_make_public(self):
        card_1 = Card(2, 'b')
        your_card_1 = YourCard(card_1)
        with pytest.raises(Exception) as excinfo:
            your_card_1.make_public("color")
        assert str(excinfo.value) == "Cannot make YourCards public because actual attributes are hidden."

    def test_made_public_number(self):
        card_1 = Card(2, 'b')
        card_1.make_public('number')
        your_card_1 = YourCard(card_1)
        assert your_card_1.public_number == 2

    def test_made_public_color(self):
        card_1 = Card(2, 'b')
        card_1.make_public('color')
        your_card_1 = YourCard(card_1)
        assert your_card_1.public_color == 'b'

    def test_made_public_both(self):
        card_1 = Card(2, 'b')
        card_1.make_public('color')
        card_1.make_public('number')
        your_card_1 = YourCard(card_1)
        assert your_card_1.public_color == 'b'
        assert your_card_1.public_number == 2
