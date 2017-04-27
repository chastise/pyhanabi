from engine.gamecontroller import GameController
from engine.player import Player
# from engine.board import Board
# from engine.deck import Deck
# from engine.gamestate import GameState
from engine.cardstack import CardStack
import pytest
import unittest

from mock import MagicMock, patch


class TestGameController(unittest.TestCase):
    def setUp(self):
        self.patch_player = patch('engine.player.Player')
        self.patch_player.start()
        self.patch_deck = patch('engine.deck.Deck')
        self.patch_deck.start()
        self.patch_board = patch('engine.board.Board')
        self.patch_board.start()
        self.patch_game_state = patch('engine.gamestate.GameState')
        self.patch_game_state.start()
        self.patch_card_stack = patch('engine.cardstack.CardStack')
        self.patch_card_stack.start()

    def tearDown(self):
        self.patch_player.stop()
        self.patch_deck.stop()
        self.patch_board.stop()
        self.patch_game_state.stop()
        self.patch_card_stack.stop()


    def test_constructor_fail_not_enough_players(self):
        test_player = Player()
        with pytest.raises(ValueError) as excinfo:
            GameController(players=[test_player])
        assert str(excinfo.value) == 'There must be between 2 and 5 players to play Hanabi.'

    def test_constructor_fail_too_many_players(self):
        test_player = Player()
        with pytest.raises(ValueError) as excinfo:
            GameController(players=[test_player, test_player, test_player,
                                    test_player, test_player, test_player])
        assert str(excinfo.value) == 'There must be between 2 and 5 players to play Hanabi.'

    def test_deal_initial_hand_3p(self):
        def mock_draw_card():
            return MagicMock() #Fake instance of card
        self.patch_deck.draw_card = mock_draw_card
        test_player = Player()
        gc = GameController([test_player, test_player, test_player])
        gc.deal_initial_hand()
        assert len(gc.player_hands) == 3
        assert len(gc.player_hands[0]) == 5

    def test_deal_initial_hand_4p(self):
        def mock_draw_card():
            return MagicMock() #Fake instance of card
        self.patch_deck.draw_card = mock_draw_card
        test_player = Player()
        gc = GameController([test_player, test_player, test_player, test_player])
        gc.deal_initial_hand()
        assert len(gc.player_hands) == 4
        assert len(gc.player_hands[0]) == 4

    # TODO: game_over: every escape case works, returns false when they have expected vals
    def test_game_over_no_fuse_tokens(self):
        test_player = Player()
        gc = GameController([test_player, test_player])
        gc.master_game_state.board.fuse_tokens = 0
        assert gc.game_over(0) == True

    @patch('engine.board.Board.get_card_stack')
    def test_game_over_all_stacks_completed(self, mock_get_card_stack):
        def get_mocked_card_stack(color):
            cs = CardStack(color='whatever')
            cs.is_complete.return_value = True
            return cs
        mock_get_card_stack.return_value = get_mocked_card_stack

        gc = GameController([Player(), Player()])
        gc.master_game_state.board.fuse_tokens = 1

        assert gc.master_game_state.board.get_card_stack('somecolor').is_complete() == True

        assert gc.game_over(0) == True

    # TODO: Test play_game fails if player cannot make_move (may belong in make_move?)


