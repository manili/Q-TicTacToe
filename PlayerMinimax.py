import random
import numpy as np
from Player import Player

class PlayerMinimax(Player):
    def __init__(self, id, minimaxDepth = 2, debug = False):
        super().__init__(id)
        self.debug = debug
        self.minimaxDepth = minimaxDepth

    def play(self, board):
        if self.debug == True:
            print("================")
        def minimax(board, depth, playerId, opponantId, isMax):
            if depth == 0:
                action = -1
                value = self.game.status(board)
                if self.debug == True:
                    print(f"{board}, {depth}, Leaf => {value}, {action}")
                return value, action
            if isMax == True:
                action = -1
                maxValue = -np.Inf
                for move in self.allPossibleMoves(board):
                    b = board.copy()
                    b[move] = playerId
                    temp, _ = minimax(b, depth - 1, playerId, opponantId, False)
                    action = move if temp > maxValue else action
                    maxValue = temp if temp > maxValue else maxValue
                if self.debug == True:
                    print(f"{board}, {depth}, Maximizer => {maxValue}, {action}")
                return maxValue, action
            if isMax == False:
                action = -1
                minValue = +np.Inf
                for move in self.allPossibleMoves(board):
                    b = board.copy()
                    b[move] = opponantId
                    temp, _ = minimax(b, depth - 1, playerId, opponantId, True)
                    action = move if temp < minValue else action
                    minValue = temp if temp < minValue else minValue
                if self.debug == True:
                    print(f"{board}, {depth}, Minimizer => {minValue}, {action}")
                return minValue, action
        
        allPossibleMovesCount = len(self.allPossibleMoves(board))
        if allPossibleMovesCount <= 6:
            self.minimaxDepth = allPossibleMovesCount if self.minimaxDepth > allPossibleMovesCount else self.minimaxDepth
            _, action = minimax(board, self.minimaxDepth, 1, 2, True)
        else:
            action = random.choice(self.allPossibleMoves(board))
        return action