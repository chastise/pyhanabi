from engine.deck import Deck
import pytest
import unittest


from mock import patch

# Todo: Make this mock Card properly
class TestDeck(unittest.TestCase):

    def test_init_defaults(self):
        deck = Deck()
        # Ensure card count == whatever defaults should predict
        assert len(deck) == len(deck.card_colors)*len(deck.card_numbers)

    def test_init_custom_colors(self):
        colors = ('red', 'blue')
        deck = Deck(colors=colors)
        assert len(deck) == 2*len(deck.card_numbers)

    def test_init_custom_numbers(self):
        numbers = (1,2,3)
        deck = Deck(numbers=numbers)
        assert len(deck) == len(deck.card_colors)*3

    def test_init_custom_everything(self):
        numbers = (1,2,3)
        colors = ('red', 'blue')
        deck = Deck(colors=colors, numbers=numbers)
        assert len(deck) == 6

    def test_init_empty_colors(self):
        with pytest.raises(ValueError) as excinfo:
            colors = ()
            deck = Deck(colors=colors)
        assert str(excinfo.value) == "Decks must have at least one card color."

    def test_init_empty_numbers(self):
        with pytest.raises(ValueError) as excinfo:
            numbers = ()
            deck = Deck(numbers=numbers)
        assert str(excinfo.value) == "Decks must have at least one card number."

    @patch('random.shuffle', autospec=True)
    @patch('random.seed', autospec=True)
    def test_shuffle_seed(self, mock_seed, mock_shuffle):
        # Assert the seed is used before shuffle is called
        deck = Deck()
        deck.shuffle(seed=1234)
        mock_seed.assert_called_once_with(1234)
        mock_shuffle.assert_called_once_with(deck.card_list)

    @patch('random.shuffle', autospec=True)
    @patch('random.seed', autospec=True)
    def test_shuffle_no_seed(self, mock_seed, mock_shuffle):
        # call it twice, ensure it's the same order?
        deck = Deck()
        deck.shuffle()
        assert not mock_seed.called, 'seed was set and should not have been'
        mock_shuffle.assert_called_once_with(deck.card_list)

    def test_draw_card_fresh_deck(self):
        deck = Deck(colors=('red', 'blue'), numbers=(1,2,3))
        len_before = len(deck)
        card = deck.draw_card()
        len_after = len(deck)
        assert len_before == len_after + 1
        assert card not in deck.card_list


    # Ensure deck maintains state, deck len decreases
    def test_draw_card_multiple_draws(self):
        deck = Deck(colors=('red', 'blue'), numbers=(1,2,3))
        len_before = len(deck)
        card1 = deck.draw_card()
        card2 = deck.draw_card()
        card3 = deck.draw_card()
        len_after = len(deck)
        assert len_before == len_after + 3
        assert card1 not in deck.card_list
        assert card2 not in deck.card_list
        assert card3 not in deck.card_list

    # Ensure this raises an exception
    def test_draw_card_empty(self):
        deck = Deck(colors=('red', ), numbers=(1,2))
        card1 = deck.draw_card()
        card2 = deck.draw_card()
        assert len(deck) == 0
        assert card1 not in deck.card_list
        assert card2 not in deck.card_list
        with pytest.raises(IndexError) as excinfo:
            card3 = deck.draw_card()
        assert str(excinfo.value) == "Cannot draw card from an empty deck."
