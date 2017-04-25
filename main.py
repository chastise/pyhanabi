from engine.gamecontroller import *
from players.human_player import *
from players.random_player import *
from players.basic_mcs_player import *


g = GameController(players=[RandomPlayer(), RandomPlayer(), BasicMCSPlayer()])
score = g.play_game()
