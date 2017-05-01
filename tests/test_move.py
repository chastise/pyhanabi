from engine.move import Move
from engine.gamestate import GameState
from engine.board import Board
from engine.card import Card
from engine.cardstack import CardStack

import pytest
import unittest

from mock import create_autospec


class TestMove(unittest.TestCase):
    def test_create_bad_move_type(self):
        with pytest.raises(ValueError) as exinfo:
            Move(move_type='cheat', player_index=0)
        assert str(exinfo.value) == 'Moves must either play, discard, or share information.'

    def test_create_bad_move_info(self):
        with pytest.raises(AssertionError):
            info_dict = {'has_no_useful_keys': 'or values!'}
            Move(move_type='give_information', player_index=0, information=info_dict)

    def test_is_playable_play(self):
        """move.is_playable returns true so long as there's a card in that player's hand at that index."""
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.player_hands = [['card0', 'card1', 'card2', 'card3'], ['card4', 'card5', 'card6']]
        move = Move(move_type='play', player_index=0, card_index=3)
        assert move.is_playable(mock_gamestate) is True

    def test_is_playable_play_hand_too_small_fails(self):
        """move.is_playable returns false when there's no card in that player's hand at that index."""
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.player_hands = [['card0', 'card1', 'card2'], ['card3', 'card4', 'card5', 'card6']]
        move = Move(move_type='play', player_index=0, card_index=3)
        assert move.is_playable(mock_gamestate) is False

    def test_is_playable_play_bad_index_fails(self):
        """move.is_playable returns false when there's no card in that player's hand at that index."""
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.player_hands = [['card0', 'card1', 'card2'], ['card3', 'card4', 'card5', 'card6']]
        move = Move(move_type='play', player_index=0, card_index=-1)
        assert move.is_playable(mock_gamestate) is False

    def test_is_playable_discard(self):
        """move.is_playable returns true so long as there's a card in that player's hand at that index."""
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.player_hands = [['card0', 'card1', 'card2', 'card3'], ['card4', 'card5', 'card6']]
        move = Move(move_type='discard', player_index=0, card_index=3)
        assert move.is_playable(mock_gamestate) is True

    def test_is_playable_discard_hand_too_small_fails(self):
        """move.is_playable returns false when there's no card in that player's hand at that index."""
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.player_hands = [['card0', 'card1', 'card2'], ['card3', 'card4', 'card5', 'card6']]
        move = Move(move_type='discard', player_index=0, card_index=3)
        assert move.is_playable(mock_gamestate) is False

    def test_is_playable_discard_bad_index_fails(self):
        """move.is_playable returns false when there's no card in that player's hand at that index."""
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.player_hands = [['card0', 'card1', 'card2'], ['card3', 'card4', 'card5', 'card6']]
        move = Move(move_type='discard', player_index=0, card_index=-1)
        assert move.is_playable(mock_gamestate) is False

    def test_is_playable_information_color(self):
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.board = create_autospec(Board)
        mock_gamestate.board.clock_tokens = 1
        mock_card = create_autospec(Card)
        mock_card.color = 'blue'
        mock_gamestate.player_hands = [[mock_card, mock_card],
                                       ['is_playable should', 'not look at players cards']]
        info_dict = {'player_id': 0, 'information_type': 'color', 'information': 'blue'}
        move = Move(move_type='give_information', player_index=1, information=info_dict)
        assert move.is_playable(mock_gamestate)

    def test_is_playable_information_color_subset_of_cards(self):
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.board = create_autospec(Board)
        mock_gamestate.board.clock_tokens = 1
        mock_card = create_autospec(Card)
        mock_card.color = 'blue'
        mock_card_not_blue = create_autospec(Card)
        mock_card_not_blue.color = 'red'
        mock_gamestate.player_hands = [[mock_card, mock_card_not_blue, mock_card_not_blue, mock_card_not_blue],
                                       ['is_playable should', 'not look at players cards']]
        info_dict = {'player_id': 0, 'information_type': 'color', 'information': 'blue'}
        move = Move(move_type='give_information', player_index=1, information=info_dict)
        assert move.is_playable(mock_gamestate)

    def test_is_playable_information_number(self):
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.board = create_autospec(Board)
        mock_gamestate.board.clock_tokens = 1
        mock_card = create_autospec(Card)
        mock_card.number = 2
        mock_gamestate.player_hands = [['is_playable should', 'not look at players cards'],
                                       [mock_card, mock_card, mock_card]]
        info_dict = {'player_id': 1, 'information_type': 'number', 'information': 2}
        move = Move(move_type='give_information', player_index=0, information=info_dict)
        assert move.is_playable(mock_gamestate)

    def test_is_playable_information_number_subset_of_cards(self):
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.board = create_autospec(Board)
        mock_gamestate.board.clock_tokens = 1
        mock_card = create_autospec(Card)
        mock_card.number = 2
        mock_card_not_two = create_autospec(Card)
        mock_card_not_two.number = 4
        mock_gamestate.player_hands = [['is_playable should', 'not look at players cards'],
                                       [mock_card_not_two, mock_card, mock_card_not_two, mock_card]]
        info_dict = {'player_id': 1, 'information_type': 'number', 'information': 2}
        move = Move(move_type='give_information', player_index=0, information=info_dict)
        assert move.is_playable(mock_gamestate)

    def test_is_playable_information_give_self_information_fails(self):
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.board = create_autospec(Board)
        mock_gamestate.board.clock_tokens = 1
        mock_card = create_autospec(Card)
        mock_card.number = 2
        mock_gamestate.player_hands = [[mock_card, mock_card, mock_card],
                                       [mock_card, mock_card, mock_card]]
        info_dict = {'player_id': 0, 'information_type': 'number', 'information': 2}
        move = Move(move_type='give_information', player_index=0, information=info_dict)
        assert move.is_playable(mock_gamestate) is False

    def test_is_playable_information_no_clock_tokens(self):
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.board = create_autospec(Board)
        mock_card = create_autospec(Card)
        mock_card.number = 2
        mock_gamestate.player_hands = [['is_playable should', 'not look at players cards'],
                                       [mock_card, mock_card, mock_card]]
        mock_gamestate.board.clock_tokens = 0
        info_dict = {'player_id': 0, 'information_type': 'number', 'information': 2}
        move = Move(move_type='give_information', player_index=1, information=info_dict)
        assert move.is_playable(mock_gamestate) is False

    def test_is_playable_information_no_colors_fails(self):
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.board = create_autospec(Board)
        mock_gamestate.board.clock_tokens = 1
        mock_card = create_autospec(Card)
        mock_card.color = 'blue'
        mock_gamestate.player_hands = [[mock_card, mock_card],
                                       ['is_playable should', 'not look at players cards']]
        info_dict = {'player_id': 0, 'information_type': 'color', 'information': 'red'}
        move = Move(move_type='give_information', player_index=1, information=info_dict)
        assert move.is_playable(mock_gamestate) is False

    def test_is_playable_information_no_numbers_fails(self):
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.board = create_autospec(Board)
        mock_gamestate.board.clock_tokens = 1
        mock_card = create_autospec(Card)
        mock_card.number = 3
        mock_gamestate.player_hands = [['is_playable should', 'not look at players cards'],
                                       [mock_card, mock_card, mock_card]]
        info_dict = {'player_id': 1, 'information_type': 'number', 'information': 2}
        move = Move(move_type='give_information', player_index=0, information=info_dict)
        assert move.is_playable(mock_gamestate) is False

    def test_is_playable_information_no_player_fails(self):
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.board = create_autospec(Board)
        mock_gamestate.board.clock_tokens = 1
        mock_card = create_autospec(Card)
        mock_card.number = 2
        mock_gamestate.player_hands = [['is_playable should', 'not look at players cards'],
                                       [mock_card, mock_card, mock_card]]
        info_dict = {'player_id': 3, 'information_type': 'number', 'information': 2}
        move = Move(move_type='give_information', player_index=0, information=info_dict)
        assert move.is_playable(mock_gamestate) is False

    # Todo: Rebuild this when wilds are properly implemented.
    def test_is_playable_information_color_is_wild_fail(self):
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.board = create_autospec(Board)
        mock_gamestate.board.clock_tokens = 1
        mock_card = create_autospec(Card)
        mock_card.color = 'wild'
        mock_gamestate.player_hands = [[mock_card, mock_card],
                                       ['is_playable should', 'not look at players cards']]
        info_dict = {'player_id': 0, 'information_type': 'color', 'information': 'wild'}
        move = Move(move_type='give_information', player_index=1, information=info_dict)
        assert move.is_playable(mock_gamestate) is False

    def test_is_playable_information_bad_information_type_fails(self):
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.board = create_autospec(Board)
        mock_gamestate.board.clock_tokens = 1
        mock_card = create_autospec(Card)
        mock_card.number = 2
        mock_gamestate.player_hands = [['is_playable should', 'not look at players cards'],
                                       [mock_card, mock_card, mock_card]]
        info_dict = {'player_id': 1, 'information_type': 'board talk is for cheaters', 'information': 2}
        move = Move(move_type='give_information', player_index=0, information=info_dict)
        assert move.is_playable(mock_gamestate) is False

    def test_apply_bad_move_fails(self):
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.player_hands = [['card0', 'card1', 'card2'], ['card3', 'card4', 'card5', 'card6']]
        move = Move(move_type='discard', player_index=0, card_index=-1)
        with pytest.raises(AssertionError) as exinfo:
            move.apply(mock_gamestate)
        assert str(exinfo.value) == 'Cannot apply move discard card index -1 in their hand, not playable.'

    def test_apply_discard(self):
        """Discard should remove a card from the player's hand, add it to the discard pile and add back a clock token."""
        mock_gamestate = create_autospec(GameState)
        mock_card = create_autospec(Card)
        mock_card_for_discard = create_autospec(Card)
        mock_gamestate.player_hands = [[mock_card], [mock_card, mock_card_for_discard]]
        mock_gamestate.board = create_autospec(Board)
        move = Move(move_type='discard', player_index=1, card_index=1)
        mock_gamestate = move.apply(game_state=mock_gamestate)
        assert len(mock_gamestate.player_hands[1]) == 1
        mock_gamestate.board.discard_card.assert_called_with(mock_card_for_discard)
        mock_gamestate.board.add_clock_token.assert_called_once()

    def test_apply_play_blow_fuse(self):
        """Play (blow fuse) should discard the card marked for play and call board.use_fuse_token"""
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.board = create_autospec(Board)
        mock_card = create_autospec(Card)
        mock_card_for_play = create_autospec(Card)
        mock_card_for_play.color = 'red'
        mock_gamestate.player_hands = [[mock_card], [mock_card_for_play, mock_card]]
        mock_stack = create_autospec(CardStack)
        mock_stack.is_legal_play.return_value = False
        mock_gamestate.board.get_card_stack.return_value = mock_stack
        move = Move(move_type='play', player_index=1, card_index=0)
        mock_gamestate = move.apply(game_state=mock_gamestate)
        mock_gamestate.board.get_card_stack.assert_called_with('red')
        assert len(mock_gamestate.player_hands[1]) == 1
        mock_gamestate.board.use_fuse_token.assert_called_once()
        mock_gamestate.board.discard_card.assert_called_with(mock_card_for_play)

    def test_apply_play_successful_play_incomplete_stack(self):
        """Play (successful) should 
                remove the card from hand, 
                add it to the stack of the right color, 
                not call board.add_clock_token
        """
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.board = create_autospec(Board)
        mock_card = create_autospec(Card)
        mock_card_for_play = create_autospec(Card)
        mock_card_for_play.color = 'green'
        mock_gamestate.player_hands = [[mock_card], [mock_card_for_play, mock_card]]
        mock_stack = create_autospec(CardStack)
        mock_stack.is_legal_play.return_value = True
        mock_stack.is_complete.return_value = False
        mock_gamestate.board.get_card_stack.return_value = mock_stack
        move = Move(move_type='play', player_index=1, card_index=0)
        mock_gamestate = move.apply(game_state=mock_gamestate)

        mock_gamestate.board.get_card_stack.assert_called_with('green')
        mock_stack.play.assert_called_with(mock_card_for_play)
        assert len(mock_gamestate.player_hands[1]) == 1
        mock_gamestate.board.add_clock_token.assert_not_called()

    def test_apply_play_successful_play_complete_stack(self):
        """Play (successful) should 
                  remove the card from hand, 
                  add it to the stack of the right color, 
                  call board.add_clock_token
          """
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.board = create_autospec(Board)
        mock_card = create_autospec(Card)
        mock_card_for_play = create_autospec(Card)
        mock_card_for_play.color = 'green'
        mock_gamestate.player_hands = [[mock_card], [mock_card_for_play, mock_card]]
        mock_stack = create_autospec(CardStack)
        mock_stack.is_legal_play.return_value = True
        mock_stack.is_complete.return_value = True
        mock_gamestate.board.get_card_stack.return_value = mock_stack
        move = Move(move_type='play', player_index=1, card_index=0)
        mock_gamestate = move.apply(game_state=mock_gamestate)

        mock_gamestate.board.get_card_stack.assert_called_with('green')
        mock_stack.play.assert_called_with(mock_card_for_play)
        assert len(mock_gamestate.player_hands[1]) == 1
        mock_gamestate.board.add_clock_token.assert_called_once()

    def test_apply_give_information_color_once(self):
        """Give information (color) should:
            call make_public('color') on all cards with that color in a hand
            call board.use_clock_token()
        """
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.board = create_autospec(Board)
        mock_gamestate.board.clock_tokens = 2
        mock_card = create_autospec(Card)
        mock_card.color = 'blue'
        mock_card_other_colors = create_autospec(Card)
        mock_card_other_colors.color = 'red'
        mock_gamestate.player_hands = [[mock_card_other_colors, mock_card_other_colors, mock_card, mock_card],
                                       [mock_card, mock_card_other_colors]]
        info_dict = {'player_id': 1, 'information_type': 'color', 'information': 'blue'}
        move = Move(move_type='give_information', player_index=0, information=info_dict)
        mock_gamestate = move.apply(game_state=mock_gamestate)
        mock_card.make_public.assert_called_once_with('color')
        mock_gamestate.board.use_clock_token.assert_called_once()

    def test_apply_give_information_color_multiple_cards(self):
        """Give information (color) should:
            call make_public('color') on all cards with that color in a hand
            call board.use_clock_token()
        """
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.board = create_autospec(Board)
        mock_gamestate.board.clock_tokens = 2
        mock_card = create_autospec(Card)
        mock_card.color = 'blue'
        mock_card_other_colors = create_autospec(Card)
        mock_card_other_colors.color = 'red'
        mock_gamestate.player_hands = [[mock_card_other_colors, mock_card_other_colors, mock_card],
                                       [mock_card, mock_card_other_colors, mock_card]]
        info_dict = {'player_id': 1, 'information_type': 'color', 'information': 'blue'}
        move = Move(move_type='give_information', player_index=0, information=info_dict)
        mock_gamestate = move.apply(game_state=mock_gamestate)
        mock_card.make_public.assert_called_with('color')
        assert mock_card.make_public.call_count == 2
        mock_gamestate.board.use_clock_token.assert_called_once()

    def test_apply_give_information_number(self):
        """Give information (number) should:
            call make_public('number') on all cards with that number in a hand
            call board.use_clock_token()
        """
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.board = create_autospec(Board)
        mock_gamestate.board.clock_tokens = 1
        mock_card = create_autospec(Card)
        mock_card.number = 2
        mock_card_other_number = create_autospec(Card)
        mock_card_other_number.number = 4
        mock_gamestate.player_hands = [[mock_card_other_number, mock_card, mock_card],
                                       [mock_card, mock_card_other_number, mock_card_other_number]]
        info_dict = {'player_id': 1, 'information_type': 'number', 'information': 2}
        move = Move(move_type='give_information', player_index=0, information=info_dict)
        mock_gamestate = move.apply(game_state=mock_gamestate)
        mock_card.make_public.assert_called_once_with('number')
        mock_gamestate.board.use_clock_token.assert_called_once()

    def test_apply_give_information_number_multiple_cards(self):
        """Give information (number) should:
            call make_public('number') on all cards with that number in a hand
            call board.use_clock_token()
        """
        mock_gamestate = create_autospec(GameState)
        mock_gamestate.board = create_autospec(Board)
        mock_gamestate.board.clock_tokens = 1
        mock_card = create_autospec(Card)
        mock_card.number = 2
        mock_card_other_number = create_autospec(Card)
        mock_card_other_number.number = 4
        mock_gamestate.player_hands = [[mock_card_other_number, mock_card, mock_card_other_number],
                                       [mock_card, mock_card_other_number, mock_card]]
        info_dict = {'player_id': 1, 'information_type': 'number', 'information': 2}
        move = Move(move_type='give_information', player_index=0, information=info_dict)
        mock_gamestate = move.apply(game_state=mock_gamestate)
        mock_card.make_public.assert_called_with('number')
        assert mock_card.make_public.call_count == 2
        mock_gamestate.board.use_clock_token.assert_called_once()
