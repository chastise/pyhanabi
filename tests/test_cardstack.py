from engine.cardstack import CardStack
from engine.card import Card, YourCard
import pytest
import unittest

from mock import create_autospec, patch

class TestCardStack(unittest.TestCase):
    def test_is_legal_play_true(self):
        stack = CardStack('red')
        mock_red_1 = create_autospec(Card)
        mock_red_1.color = 'red'
        mock_red_1.number = 1
        self.assertIs(stack.is_legal_play(mock_red_1), True)

    def test_is_legal_play_wrong_color(self):
        stack = CardStack('red')
        mock_blue_1 = create_autospec(Card)
        mock_blue_1.color = 'blue'
        mock_blue_1.number = 1
        self.assertIs(stack.is_legal_play(mock_blue_1), False)

    def test_is_legal_play_wrong_number(self):
        stack = CardStack('red')
        mock_red_2 = create_autospec(Card)
        mock_red_2.color = 'red'
        mock_red_2.number = 2
        self.assertIs(stack.is_legal_play(mock_red_2), False)

    def test_is_legal_play_stack_full(self):
        stack = CardStack('red')
        stack.cards_played = [create_autospec(Card)]
        mock_red_6 = create_autospec(Card)
        mock_red_6.color = 'red'
        mock_red_6.number = 6 # Because cards are numbered 1-5
        self.assertIs(stack.is_legal_play(mock_red_6), False)

    # Test what happens when you try to play YourCards on stacks.
    def test_is_legal_play_unknown_number(self):
        """Because a YourCard does not know it's number."""
        stack = CardStack('red')
        mock_red_1 = create_autospec(YourCard)
        mock_red_1.number = False
        mock_red_1.color = 'red'  # Cheating here to ensure it doesn't fail the color check
        self.assertIs(stack.is_legal_play(mock_red_1), False)

    def test_is_legal_play_unknown_color(self):
        """Because a YourCard does not know it's color."""
        stack = CardStack('red')
        mock_red_1 = create_autospec(YourCard)
        mock_red_1.number = 1  # Cheating here to ensure it doesn't fail the number check
        mock_red_1.color = False
        self.assertIs(stack.is_legal_play(mock_red_1), False)

    # Test play adds a card to the stack (assuming it's legal)
    def test_play_successful(self):
        with patch.object(CardStack, 'is_legal_play', return_value=True):
            stack = CardStack('blue')
            mock_blue_1 = create_autospec(Card)
            assert len(stack.cards_played) == 0
            stack.play(mock_blue_1)
            assert len(stack.cards_played) == 1

    # Test that get_score returns expected values in a whole host of different states
    def test_get_score_new_stack(self):
        stack = CardStack('green')
        assert stack.get_score() == 0

    def test_get_score_partial_stack(self):
        stack = CardStack('green')
        mock_card = create_autospec(Card)
        stack.cards_played = [mock_card, mock_card]
        assert stack.get_score() == 2

    def test_get_score_full_stack(self):
        stack = CardStack('green')
        mock_card = create_autospec(Card)
        stack.cards_played = [mock_card, mock_card, mock_card, mock_card, mock_card]
        assert stack.get_score() == 5

    # Test is_complete for new, partial and full stacks.
    def test_is_complete_new_stack(self):
        stack = CardStack('white')
        self.assertIs(stack.is_complete(), False)

    def test_is_complete_partial_stack(self):
        stack = CardStack('white')
        mock_card = create_autospec(Card)
        stack.cards_played = [mock_card, mock_card] # There's probably a better way to do this.
        self.assertIs(stack.is_complete(), False)

    def test_is_complete_full_stack(self):
        stack = CardStack('white')
        mock_card = create_autospec(Card)
        stack.cards_played = [mock_card, mock_card, mock_card, mock_card, mock_card]
        self.assertIs(stack.is_complete(), True)