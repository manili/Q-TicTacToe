import random
from Player import Player

class PlayerRandom(Player):
    def play(self, board):
        return random.choice(self.allPossibleMoves(board))