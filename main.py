from engine.gamecontroller import *
from players.human_player import *
from players.random_player import *
from players.basic_mcs_player import *
from players.heuristic_player import *
import numpy


def run_and_score_games(player1, player2, num_games):
    scores = []
    for _ in range(num_games):
        g = GameController(players=[player1, player2])
        score = g.play_game()
        scores += [score]
    print("{p1} and {p2} played {n} games. Mean score: {mean}; Max score: {max}".format(p1=str(player1),
                                                                                        p2=str(player2),
                                                                                        n=num_games,
                                                                                        mean=numpy.mean(scores),
                                                                                        max=max(scores)))

run_and_score_games(RandomPlayer(), RandomPlayer(), 100)
run_and_score_games(PointsHeuristicPlayer(), PointsHeuristicPlayer(), 100)
run_and_score_games(GenerousPointsHeuristicPlayer(), GenerousPointsHeuristicPlayer(), 100)