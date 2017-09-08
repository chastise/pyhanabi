from engine.player import Player
from engine.gamecontroller import GameController
from engine.gamestate import PlayerGameState
from engine.deck import Deck
from players.shared import util
import random, copy, time
from itertools import cycle



class BasicMCSPlayer(Player):
    """
    An AI that uses monte carlo search techniques to choose moves.
    
    Strategy: 
        For all moves, simulate the rest of the game given available and guessed information,
        and using AIs that play randomly. Score is the score at the end of that game.
        
    """

    def __str__(self):
        return "BasicMCSPlayer"

    def make_move(self, game_state):
        print(self)
        available_moves = util.construct_all_legal_moves(game_state)
        available_move_score_gain = [[] for _ in xrange(len(available_moves))]
        # Create a deck for copy to each simulated move state.
        sim_deck = self.construct_inferred_deck(game_state)
        # Score each state in a loop for 2 seconds:
        time_out = time.time() + 1 # ~3 seconds of looping
        while time_out > time.time():
            for move_index, move in enumerate(available_moves):
                deck = copy.deepcopy(sim_deck)
                # shuffle deck
                random.shuffle(deck.card_list)
                # Draw simulated cards for YourCards in player's hand. Replace YourCards with Cards.
                my_hand = self.draw_possible_hand(game_state.get_my_hand(), deck)
                # Copy gamestate and un-YourCard player cards.
                sim_game_state = copy.deepcopy(game_state)
                sim_game_state.player_hands[sim_game_state.player_id] = my_hand
                # Create simulation GameController
                controller = SimulatedGameController(sim_game_state, deck, move)
                # Execute move on simulated gamestate
                score = controller.play_game()
                available_move_score_gain[move_index].append(score)
                # Continue game with random actors, collect resulting score
        #print(available_moves)
        #print(available_move_score_gain)
        # Trying a dumb score heuristic:
        #  if the move is discard or give_information, take the mean.
        #  if the move is play, take the min.
        for index, move in enumerate(available_moves):
            if move.move_type == 'play':
                available_move_score_gain[index] = min(available_move_score_gain[index])
            else:
                available_move_score_gain[index] = sum(available_move_score_gain[index]) / \
                                                   float(len(available_move_score_gain[index]))

        # For now, let's be dumb and return the move with the best score:
        print(available_move_score_gain)
        score, index = max([(v,i) for i,v in enumerate(available_move_score_gain)])
        print(score, index)
        print(available_moves[index])
        return available_moves[index]

    def construct_inferred_deck(self, game_state):
        new_deck = Deck(colors=game_state.board.deck_colors, numbers=game_state.board.deck_numbers, seed=42)
        # remove cards that have been discarded
        for card in game_state.board.discard:
            new_deck.card_list.remove(card)
        # remove cards in other player's hands
        hand_indexes = range(len(game_state.player_hands))
        hand_indexes.remove(game_state.player_id)
        for hand_id in hand_indexes:
            for card in game_state.player_hands[hand_id]:
                new_deck.card_list.remove(card)
        # remove cards that have already scored points
        for color, stacked_cards in game_state.board.card_stacks.iteritems():
            for card in stacked_cards.cards_played:
                new_deck.card_list.remove(card)
        return new_deck

    def draw_possible_hand(self, my_hand, deck):
        known_cards, known_partial_cards, unknown_cards = [], [], []
        result_hand = []
        for index, card in enumerate(my_hand):
            if card.public_color and card.public_number:
                known_cards.append((card, index))
            elif card.public_color or card.public_number:
                known_partial_cards.append((card, index))
            else:
                unknown_cards.append((card, index))
        for card in known_cards:
            for index, candidate in enumerate(deck.card_list):
                if candidate.number == card[0].public_number and candidate.color == card[0].public_color:
                    result_hand.append((deck.card_list[index], card[1]))
                    deck.card_list.remove(candidate)
        # (potentially) repeatedly search the deck and known cards for cards we can use.
        partial_result_hand = []
        while len(known_partial_cards) > 0:
            print(known_partial_cards)
            print(partial_result_hand)
            card = known_partial_cards.pop()
            card_found = False
            for index, candidate in enumerate(deck.card_list):
                if (card[0].public_number and candidate.number == card[0].public_number) or \
                   (card[0].public_color and candidate.color == card[0].public_color):
                    partial_result_hand.append((deck.card_list[index], card[1], card[0]))
                    deck.card_list.remove(candidate)
                    card_found = True
                    break
            if not card_found:
                # Then one of the cards must already be in the hand. It can't be in result_hand because we know those.
                # Pull the 0th item
                if len(partial_result_hand) == 0:
                    raise Exception("Failed to find sim cards to match cards in the player's hand in simulated deck.")
                card_found_in_selected = False
                for index, candidate in enumerate(partial_result_hand):
                    if (card[0].public_number and candidate[0].number == card[0].public_number) or \
                        (card[0].public_color and candidate[0].color == card[0].public_color):
                        # Leave this pulled card in, but we need to return it's known_partial reference card and
                        #  hand-position index to known_partial_cards, and update it's reference card and hand_index
                        #  in partial_result_hand
                        # Put that hand's card back in known_partial_cards. Insert to 0 to avoid thrashing/cycles.
                        known_partial_cards.insert(0, (candidate[1], candidate[2]))
                        # Take the sim'd card and put it in for a new slot in the hand:
                        partial_result_hand[index] = (candidate[0], card[1], card[0])
                        card_found_in_selected = True
                        break
                if not card_found_in_selected:
                    raise Exception("Failed to find sim cards to match cards in the player's hand in already-picked cards.")
        for card_tuple in partial_result_hand:
            result_hand.append(card_tuple)
        # Draw some cards from the deck for cards with no info
        for card in unknown_cards:
            if len(deck) < 1:
                raise Exception("Tried to fill in an unknown card in hand but deck was empty")
            result_hand.append((deck.draw_card(), card[1]))
        # Order the whole hand by the original order:
        result_hand.sort(key=lambda x: x[1])
        result_hand = [card_tuple[0] for card_tuple in result_hand]
        # Mark cards that have been pulled with their public info, now that we have a plausible hand.
        for index, card in enumerate(my_hand):
            if card.public_number:
                result_hand[index].make_public('number')
            if card.public_color:
                result_hand[index].make_public('color')

        return result_hand


class MCSRandomPlayer(Player):
    """An AI that MCS uses to simulate random future moves."""
    def __str__(self):
        return "MCSRandomPlayer"

    def make_move(self, game_state):
        print(game_state.board)
        print(game_state.get_my_id())
        print(game_state.player_hands)
        print(game_state.board.game_almost_over)
        moves = util.construct_all_legal_moves(game_state)
        move = random.choice(moves)
        return move


class SimulatedGameController(GameController):
    """
    Implement a custom init and a 'finish_game' function to replace 'play_game'
    Since we can't draw cards or operate on unknown information, for now just play whatever is visible.
    Effectively, plays out current cards to the best of it's ability.
    """
    def __init__(self, game_state, deck, initial_move):
        # print("initializing simulated game controller")
        self.colors = game_state.board.deck_colors
        self.numbers = game_state.board.deck_numbers
        self.players = [MCSRandomPlayer() for _ in range(len(game_state.player_hands))]
        self.deck = deck
        self.player_hands = game_state.player_hands
        self.master_game_state = game_state
        self.initial_move = initial_move

    def play_game(self):
        # Apply the MCSPlayer's move, ensure the game's not over,
        #  then start playing MCSRandom moves for subsequent turns.
        self.master_game_state = self.initial_move.apply(self.master_game_state)
        if self.game_over(self.master_game_state.player_id):
            game_score = self.master_game_state.board.compute_score()
            return game_score
        if len(self.deck) > 0:
            new_card = self.deck.draw_card()
            if not new_card:
                print("How did I get this far when the deck was empty?")
                print(self.deck)
                raise Exception("Deck drew card while empty")
            self.player_hands[self.master_game_state.player_id].append(new_card)
            self.master_game_state.player_hands = self.player_hands
            self.master_game_state.board.deck_size = len(self.deck)
        self.master_game_state.player_id += 1
        if self.master_game_state.player_id > len(self.master_game_state.player_hands) - 1:
            self.master_game_state.player_id = 0

        cycle_starter = range(len(self.players))
        while cycle_starter[0] != self.master_game_state.player_id:
            val = cycle_starter[0]
            cycle_starter.remove(val)  # pull item off front
            cycle_starter.append(val)  # put item on the end

        for player_id in cycle(cycle_starter):
            player_game_state = PlayerGameState(self.master_game_state, player_id)
            new_move = self.players[player_id].make_move(player_game_state)
            try:
                # print(player_id)
                # print(self.master_game_state.player_hands)
                # print(self.game_over(player_id))
                # print(self.master_game_state.board)
                self.master_game_state = new_move.apply(self.master_game_state)
            except AssertionError, e:
                raise Exception(
                    "{p} submitted unplayable move: {m}, {e}".format(p=str(self.players[player_id]), m=str(new_move), e=e))
            if self.game_over(player_id):
                game_score = self.master_game_state.board.compute_score()
                return game_score
            if len(self.deck) > 0:
                new_card = self.deck.draw_card()
                if not new_card:
                    print("How did I get this far when the deck was empty?")
                    print(self.deck)
                    raise Exception("Deck drew card while empty")
                self.player_hands[player_id].append(new_card)
                self.master_game_state.player_hands = self.player_hands
                self.master_game_state.board.deck_size = len(self.deck)
            # This triggers when the last card is drawn, every player including this one takes one more turn.
            if len(self.deck) == 0 and self.master_game_state.board.game_almost_over is None:
                self.master_game_state.board.game_almost_over = player_id
