import random
from Player import Player

class PlayerQTable(Player):
    def __init__(self, id, qTable = {}, enableTraining = True, epsilon = -1.0, debug = False):
        super().__init__(id)
        self.debug = debug
        self.qTable = qTable
        self.epsilon = epsilon
        self.enableTraining = enableTraining

    def update(self, playerId, state, action, stateNext, reward):
        super().update(playerId, state, action, stateNext, reward)
        if self.enableTraining == True and \
            (playerId == self.id and reward != self.game.NOT_TERMINATED) or \
            (playerId != self.id and 0 < len(self.s)):
            self.trainQTable()

    def trainQTable(self, alpha = 0.1, gama = 1, debug = False):
        def getKey(s, a):
            return str( (str(s), a) ).replace('\'', '')
        
        if self.r == self.game.NO_WINNERS or self.r == self.game.CURRENT_PLAYER_WINS or self.r == self.game.OPPONENT_PLAYER_WINS:
            q_value = self.qTable[getKey(self.s, self.a)] if getKey(self.s, self.a) in self.qTable else 0
            self.qTable[getKey(self.s, self.a)] = (1 - alpha) * q_value + alpha * self.r
        else:
            q_value = self.qTable[getKey(self.s, self.a)] if getKey(self.s, self.a) in self.qTable else 0
            q_value_next = [self.qTable[getKey(self.s_, a)] for a in  self.allPossibleMoves(self.s_) if getKey(self.s_, a) in self.qTable]
            q_value_next_max = max(q_value_next if len(q_value_next) > 0 else [0])
            q_value = (1 - alpha) * q_value + alpha * (self.r + gama * q_value_next_max)
            self.qTable[getKey(self.s, self.a)] = q_value

        if debug == True:
            print(f"============================= Q-Table =============================")
            i = 1
            for item in self.qTable:
                print(f"{i}. {item} => {self.qTable[item]}")
                i += 1

        return self.qTable
    
    def play(self, board):
        def getKey(s, a):
            return str( (str(s), a) ).replace('\'', '')

        if self.epsilon < random.uniform(0.0, 100.0):
            allPossibleMoves = self.allPossibleMoves(board)
            allExistingActionValuesInQTable = [(a, self.qTable[getKey(board, a)]) for a in allPossibleMoves if getKey(board, a) in self.qTable]
            action = random.choice(self.allPossibleMoves(board)) if len(allExistingActionValuesInQTable) == 0 \
                else [av[0] for av in allExistingActionValuesInQTable if av[1] == max([x[1] for x in allExistingActionValuesInQTable])][0]
            return action
        else:
            return random.choice(self.allPossibleMoves(board))