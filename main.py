from engine.gamecontroller import *
from players.human_player import *
from players.random_player import *


g = GameController(players=[RandomPlayer(), RandomPlayer()])
score = g.play_game()
