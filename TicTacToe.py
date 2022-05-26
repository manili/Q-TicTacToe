import random
import numpy as np

class TicTacToe(object):
    EMPTY_VALUE = NO_WINNERS = NO_REWARDS = 0
    CURRENT_PLAYER_WINS = +200
    OPPONENT_PLAYER_WINS = -1000
    NOT_TERMINATED = -1

    def __init__(self, player1, player2, starter = 0):
        self.board = np.full(9, self.EMPTY_VALUE, dtype=np.int8)
        self.players = [player1, player2]
        self.player = random.choice(self.players) if starter == 0 else self.players[0] if starter == 1 else self.players[1]
        self.opponent = self.players[self.players.index(self.player) ^ 1]

    def swapPlayer(self):
        tmp = self.player
        self.player = self.opponent
        self.opponent = tmp

    def status(self, board):
        for i in range(3):
            if (board[i * 3 + 0] == board[i * 3 + 1] == board[i * 3 + 2] != self.EMPTY_VALUE) or \
               (board[i + 3 * 0] == board[i + 3 * 1] == board[i + 3 * 2] != self.EMPTY_VALUE):
                return self.CURRENT_PLAYER_WINS
        if (board[0] == board[4] == board[8] != self.EMPTY_VALUE) or \
           (board[2] == board[4] == board[6] != self.EMPTY_VALUE):
           return self.CURRENT_PLAYER_WINS
        for i in range(9):
            if board[i] == self.EMPTY_VALUE:
                return self.NOT_TERMINATED
        return self.NO_WINNERS

    def step(self, board, player, opponent):
        def play(board, player):
            action = player.play(board)
            if board[action] != self.EMPTY_VALUE:
                reward = self.OPPONENT_PLAYER_WINS
            else:
                board[action] = player.id
                reward = self.status(board)
            return board, action, reward

        oldBoard = board.copy()
        board, action, reward = play(board, player)
        newBoard = board.copy()
        player.update(self.player.id, oldBoard, action, newBoard, reward)
        opponent.update(self.player.id, oldBoard, action, newBoard,
            self.CURRENT_PLAYER_WINS if reward == self.OPPONENT_PLAYER_WINS else 
            self.OPPONENT_PLAYER_WINS if reward == self.CURRENT_PLAYER_WINS else reward)
        return reward, board

    def run(self, debugMode = False):
        stepResult = self.NOT_TERMINATED
        while stepResult == self.NOT_TERMINATED:
            stepResult, self.board = self.step(self.board, self.player, self.opponent)
            if stepResult == self.NOT_TERMINATED:
                self.swapPlayer()
            if debugMode == True:
                self.printBoardLn()
        
        if stepResult == self.OPPONENT_PLAYER_WINS:
            return self.OPPONENT_PLAYER_WINS
        elif stepResult == self.NO_WINNERS:
            return self.NO_WINNERS
        elif stepResult == self.CURRENT_PLAYER_WINS:
            return self.CURRENT_PLAYER_WINS

    def printStarter(self):
        print(f"Starter is {self.player.id}")
    
    def printStarterLn(self):
        self.printStarter()
        print()
    
    def printBoard(self):
        for row in range(3):
            print(f"{self.board[row * 3 + 0]}, {self.board[row * 3 + 1]}, {self.board[row * 3 + 2]}")

    def printBoardLn(self):
        self.printBoard()
        print()

    def runAndPrintFinalResult(self):
        runResult = self.run()
        if runResult == self.NO_WINNERS:
            print(f"No winners!")
        else:
            print(f"Winner is {self.player.id if runResult == self.CURRENT_PLAYER_WINS else self.opponent.id}!")

    def runAndPrintFinalResultLn(self):
        self.runAndPrintFinalResult()
        print()