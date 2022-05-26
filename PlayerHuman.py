from Player import Player

class PlayerHuman(Player):
    def play(self, board):
        self.game.printBoardLn()
        return int(input("Input your action:"))