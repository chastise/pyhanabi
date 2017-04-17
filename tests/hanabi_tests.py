import pytest
from engine import card, deck

class TestCard:
    def test_create(self):
        newcard = card.Card(2, 'blue')
        assert newcard.get_color('blue')
        assert newcard.get_number(2)


class TestDeck:
    def test_create_normal(self):
        assert True

    def test_create_rainbow(self):
        assert True

    def test_shuffle(self):
        assert True