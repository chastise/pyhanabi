class Player(object):
    """Abstract player class"""

    def __str__(self):
        return "AbstractPlayerPleaseIgnore"

    def make_move(self, game_state):
        raise NotImplementedError("You have to implement this yourself")