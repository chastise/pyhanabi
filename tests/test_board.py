from engine.board import Board
from engine.cardstack import CardStack
import pytest
import unittest

from mock import patch


class TestBoard(unittest.TestCase):

    # TODO: Move mock deck creation to setUp
    @patch('engine.deck.Deck', autospec=True)
    def test_init_creates_expected_cardstacks(self, mock_deck):
        mock_deck.__len__.return_value = 40
        mock_deck.card_colors = ('red', 'blue')
        mock_deck.card_numbers = (1, 2, 2, 3)
        board = Board(mock_deck)
        # Check that there's a stack for each color in the deck
        for color in mock_deck.card_colors:
            assert isinstance(board.card_stacks[color], CardStack)

    # TODO: Move mock deck creation to setUp
    @patch('engine.deck.Deck', autospec=True)
    def test_init_creates_discard_stats(self, mock_deck):
        mock_deck.__len__.return_value = 40
        mock_deck.card_colors = ('red', 'blue')
        mock_deck.card_numbers = (1, 2, 2, 3)
        board = Board(mock_deck)
        # Assert there's a discard pile with a length:
        assert len(board.discard) == 0
        # Assert there's a discard_stats list with one counter per card number
        for color in mock_deck.card_colors:
            for number in mock_deck.card_numbers:
                assert len(board.discard_stats[color]) == len(set(mock_deck.card_numbers))

    def test_discard_card_to_discard(self):
        pass

    def test_discard_card_updates_stats(self):
        pass

    def test_use_clock_token(self):
        pass

    def test_use_clock_token_no_tokens(self):
        pass

    def test_use_fuse_token(self):
        pass

    def test_use_fuse_token_no_tokens(self):
        pass

    def test_add_clock_token(self):
        pass

    def test_add_clock_token_full(self):
        pass

    def test_get_card_stack(self):
        pass

    def test_get_card_stack_bad_color(self):
        pass

    def test_compute_score_zero(self):
        pass

    def test_compute_score_non_zero(self):
        pass
