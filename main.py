from engine.gamecontroller import *
from players.human_player import *

g = GameController(players=[HumanPlayer(), HumanPlayer()])

score = g.play_game()