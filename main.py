from engine.game import *
from players.human_player import *

g = Game(players=[HumanPlayer(), HumanPlayer()])

score = g.play_game()