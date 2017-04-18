class Move(object):
    """Moves must either play, discard or share information with another player about their hand.
    Args:
        move_type (str): Must be 'discard', 'play' or 'give_information'.
        player_index(int): Must be the index of the player making the move.
        card_index (int, optional): Index of the card to be discarded or played. Not used to give_information.
        information (dict, optional): Dictionary containing keys
                                        'player_id': (int) for the index of the player
                                        'information_type': (string) for whether the information is a card color or number.
                                        'information': either a string specifying a color or int specifying card number. 
    """
    def __init__(self, move_type, player_index, card_index=None, information=None):
        self.player_index = player_index
        if move_type == 'discard':
            assert isinstance(card_index, int)
            self.move_type = 'discard'
            self.card_index = card_index
            self.information = None
        elif move_type == 'play':
            assert isinstance(card_index, int)
            self.move_type = 'play'
            self.card_index = card_index
            self.information = None
        elif move_type == 'give_information':
            assert isinstance(information, dict)
            assert information.has_key('player_id')
            assert information.has_key('information_type')
            assert information.has_key('information')
            self.move_type = 'give_information'
            self.card_index = None
            self.information = information
        else:
            raise Exception('Moves must either play, discard, or share information. See the docstring for specifics')

    def __str__(self):
        if self.move_type in ('play', 'discard'):
            return self.move_type + ' card index ' + str(self.card_index) + ' in their hand'
        else:
            return self.move_type + ' with ' + str(self.information)

    def __repr__(self):
        return str(self)

    # Either play index, discard index or give information
    def is_playable(self, game_state):
        from engine.gamecontroller import GameState, PlayerGameState
        assert isinstance(game_state, GameState)
        # If discard or play, just make sure the card's actually in the player's hand.
        if self.move_type in ('discard', 'play'):
            player_hand = game_state.player_hands[self.player_index]
            return self.card_index in range(len(player_hand))
        # If information, check if enough clock_tokens exist and ensure the player_id is not the current player.
        # Information must also be non-zero (e.g. can't indicate "no reds"), so check the target hand for at least one fit.
        elif self.move_type == 'give_information':
            target_player_id = self.information['player_id']
            if target_player_id == self.player_index:
                return False
            if game_state.board.count_clock_tokens() < 1:
                return False
            target_hand = game_state.player_hands[target_player_id]
            information_detail = self.information['information']
            if self.information['information_type'] == 'color':
                cards_to_reveal = [c for c in target_hand if c.color == information_detail]
                if len(cards_to_reveal) < 1:
                    return False
            elif self.information['information_type'] == 'number':
                cards_to_reveal = [c for c in target_hand if c.number == information_detail]
                if len(cards_to_reveal) < 1:
                    return False

            return True

    # Apply the move to the game_state, returning the updated game_state.
    def apply(self, game_state):
        assert self.is_playable(game_state)
        if self.move_type == 'discard':
            player_hand = game_state.player_hands[self.player_index]
            player_card = player_hand.pop(self.card_index)
            board = game_state.board
            board.discard_card(player_card)
            board.add_clock_token()
        elif self.move_type == 'play': # TODO: Firework completion bonus for play
            player_hand = game_state.player_hands[self.player_index]
            player_card = player_hand.pop(self.card_index)
            card_stack = game_state.board.get_card_stack(player_card.color)
            if card_stack.is_legal_play(player_card):
                card_stack.play(player_card)
            else:
                game_state.board.discard_card(player_card)
                game_state.board.use_fuse_token()
        elif self.move_type == 'give_information':
            print("applying information")
            target_player = self.information['player_id']
            target_players_hand = game_state.player_hands[target_player]
            if self.information['information_type'] == 'number':
                number = int(self.information['information'])
                for card in target_players_hand:
                    if card.number == number:
                        card.make_public('number')
            elif self.information['information_type'] == 'color':
                color = self.information['information']
                for card in target_players_hand:
                    if card.color == color:
                        card.make_public('color')
            else:
                raise Exception("tried to apply invalid move {m}".format(m=self))
            game_state.board.use_clock_token()

        return game_state
