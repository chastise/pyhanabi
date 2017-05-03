from engine.gamecontroller import GameController
from engine.player import Player
from engine.board import Board
from engine.deck import Deck
from engine.gamestate import GameState
from engine.cardstack import CardStack
import pytest
import unittest

from mock import MagicMock, patch, create_autospec


class TestGameController(unittest.TestCase):

    def test_constructor_fail_not_enough_players(self):
        mock_player = create_autospec(Player)
        with pytest.raises(ValueError) as excinfo:
            GameController(players=[mock_player])
        assert str(excinfo.value) == 'There must be between 2 and 5 players to play Hanabi.'

    def test_constructor_fail_too_many_players(self):
        mock_player = create_autospec(Player)
        with pytest.raises(ValueError) as excinfo:
            GameController(players=[mock_player, mock_player, mock_player,
                                    mock_player, mock_player, mock_player])
        assert str(excinfo.value) == 'There must be between 2 and 5 players to play Hanabi.'

    def test_deal_initial_hand_2p(self):
        mock_deck = create_autospec(Deck)
        mock_deck.draw_card.return_value = "card"
        mock_player = create_autospec(Player)
        gc = GameController([mock_player, mock_player])
        gc.deck = mock_deck
        gc.deal_initial_hand()
        assert len(gc.player_hands) == 2
        assert len(gc.player_hands[0]) == 5

    def test_deal_initial_hand_3p(self):
        mock_deck = create_autospec(Deck)
        mock_deck.draw_card.return_value = "card"
        mock_player = create_autospec(Player)
        gc = GameController([mock_player, mock_player, mock_player])
        gc.deck = mock_deck
        gc.deal_initial_hand()
        assert len(gc.player_hands) == 3
        assert len(gc.player_hands[0]) == 5

    def test_deal_initial_hand_4p(self):
        mock_deck = create_autospec(Deck)
        mock_deck.draw_card.return_value = "card"
        mock_player = create_autospec(Player)
        gc = GameController([mock_player, mock_player, mock_player, mock_player])
        gc.deck = mock_deck
        gc.deal_initial_hand()
        assert len(gc.player_hands) == 4
        assert len(gc.player_hands[0]) == 4

    def test_deal_initial_hand_5p(self):
        mock_deck = create_autospec(Deck)
        mock_deck.draw_card.return_value = "card"
        mock_player = create_autospec(Player)
        gc = GameController([mock_player, mock_player, mock_player, mock_player, mock_player])
        gc.deck = mock_deck
        gc.deal_initial_hand()
        assert len(gc.player_hands) == 5
        assert len(gc.player_hands[0]) == 4

    # TODO: game_over: every escape case works, returns false when they have expected vals
    def test_game_over_no_fuse_tokens(self):
        mock_player = create_autospec(Player)
        gc = GameController([mock_player, mock_player])
        gc.master_game_state.board.fuse_tokens = 0
        assert gc.game_over(0, gc.master_game_state) is True

    def test_game_over_all_stacks_completed(self):
        mock_game_state = create_autospec(GameState)
        mock_board = create_autospec(Board)
        mock_player = create_autospec(Player)
        gc = GameController([mock_player, mock_player])
        gc.master_game_state = mock_game_state
        gc.master_game_state.board = mock_board
        gc.master_game_state.board.fuse_tokens = 1
        # Max score for a default game. Need to update when we add wilds / configurable color counts.
        gc.master_game_state.board.compute_score.return_value = 25
        assert gc.game_over(0, gc.master_game_state) is True

    def test_game_over_last_turn(self):
        # TODO: There's a more-clear way to manage game state and track final player turn.
        # TODO: Finish writing this test, then refactor. Might even need to move game_over to GameState
        # Note, this doesn't need to know about the actual deck
        mock_deck = create_autospec(Deck)
        mock_deck.__len__.return_value = 0
        mock_player = create_autospec(Player)
        mock_game_state = create_autospec(GameState)
        mock_board = create_autospec(Board)
        gc = GameController([mock_player, mock_player])
        gc.deck = mock_deck
        gc.master_game_state = mock_game_state
        gc.master_game_state.board = mock_board
        gc.master_game_state.board.fuse_tokens = 1
        gc.master_game_state.board.game_almost_over = 0
        assert gc.game_over(0, gc.master_game_state)

    def test_game_over_not_over_deck_not_empty(self):
        mock_deck = create_autospec(Deck)
        mock_deck.__len__.return_value = 1
        mock_player = create_autospec(Player)
        mock_game_state = create_autospec(GameState)
        mock_board = create_autospec(Board)
        gc = GameController([mock_player, mock_player])
        gc.deck = mock_deck
        gc.master_game_state = mock_game_state
        gc.master_game_state.board = mock_board
        gc.master_game_state.board.fuse_tokens = 1
        gc.master_game_state.board.game_almost_over = 0

        assert gc.game_over(0, gc.master_game_state) is False

    def test_game_over_not_over_deck_empty(self):
        mock_deck = create_autospec(Deck)
        mock_deck.__len__.return_value = 0
        mock_player = create_autospec(Player)
        mock_game_state = create_autospec(GameState)
        mock_board = create_autospec(Board)
        gc = GameController([mock_player, mock_player])
        gc.deck = mock_deck
        gc.master_game_state = mock_game_state
        gc.master_game_state.board = mock_board
        gc.master_game_state.board.fuse_tokens = 1
        gc.master_game_state.board.game_almost_over = 0

        assert gc.game_over(1, gc.master_game_state) is False


    # TODO: Test play_game fails if player cannot make_move (may belong in make_move?)
    def test_play_game_last_move_wins(self):
        # Because if the final move causes a win we should return true but the game should end with correct points
        pass
