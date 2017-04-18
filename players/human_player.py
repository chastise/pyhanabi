from engine.player import Player
from engine.move import Move


class HumanPlayer(Player):
    """A real live human player"""

    def __str__(self):
        return "HumanPlayer"

    def make_move(self, game_state):
        print("----")
        print("You are player {pid}".format(pid=game_state.get_my_id()))
        for i in range(len(game_state.player_hands)):
            print("Player "+ str(i) + ": " + str(game_state.player_hands[i]))
        print(str(game_state.board))
        move = self.construct_move(game_state)
        if not move.is_playable(game_state):
            print("unplayable move {m}; Please try one more time:".format(m=move))
            move = self.construct_move(game_state)
            if not move.is_playable(game_state):
                raise Exception("Too many invalid move inputs, quitting")

        return move

    def construct_move(self, game_state):
        move_type = None
        while move_type not in ('play', 'discard', 'give_information'):
            move_type = raw_input("Please enter 'play', 'discard', or 'give_information':")
        if move_type in ('play', 'discard'):
            card_index = None
            while card_index not in [str(i) for i in range(len(game_state.player_hands[game_state.get_my_id()]))]:
                print("Your current hand: " + str(game_state.player_hands[game_state.get_my_id()]))
                card_index = raw_input("Please specify the index of the card you'd like to " + move_type + ":")
            return Move(move_type, game_state.get_my_id(), card_index=int(card_index))
        else:
            player_id = False
            information_type = False
            information = False
            while player_id not in [str(i) for i in range(len(game_state.player_hands))] or player_id == str(game_state.get_my_id()):
                player_id = raw_input("Which player would you like to give information?")
            print("Player {pid}'s hand: {hand}".format(pid=player_id, hand=str(game_state.player_hands[int(player_id)])))

            while information_type not in ('number', 'color'):
                information_type = raw_input("Would you like to share a number or a color?")

            if information_type == 'number':
                while information not in ['1', '2', '3', '4', '5']:
                    information = raw_input("Enter the number you would like to reveal.")
                return Move(move_type, game_state.get_my_id(), information={'player_id': int(player_id),
                                                                            'information_type': information_type,
                                                                            'information': int(information)})
            else:
                while information not in game_state.board.deck_colors:
                    information = raw_input("Enter a color from {c}".format(c=game_state.board.deck_colors))
                return Move(move_type, game_state.get_my_id(), information={'player_id': int(player_id),
                                                                            'information_type': information_type,
                                                                            'information': information})