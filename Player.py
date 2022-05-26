class Player(object):
    def __init__(self, id):
        self.id = id
        self.s = []
        self.a = None
        self.r = None
        self.s_ = []
        self.game = None
        self.episode = []

    def allPossibleMoves(self, board):
        return [x for x in range(9) if board[x] == self.game.EMPTY_VALUE]

    def update(self, playerId, state, action, stateNext, reward):
        if playerId == self.id:
            self.s = state
            self.a = action
            if reward != self.game.NOT_TERMINATED:
                self.r = reward
                self.s_ = stateNext
                self.episode.append( (self.s, self.a, self.r, self.s_) )
        elif 0 < len(self.s): # Player should have played at least one run...
            self.r = reward
            self.s_ = stateNext
            self.episode.append( (self.s, self.a, self.r, self.s_) )

    def clean(self):
        self.s = []
        self.a = None
        self.r = None
        self.s_ = []
        self.game = None
        self.episode = []
    
    def printPlayerHistory(self):
        print(f"Player{self.id} History:")
        for i in range(0, len(self.episode)):
            print(f"{i}. S: {self.episode[i][0]}, A: {self.episode[i][1]}, R: {self.episode[i][2]}, S':{self.episode[i][3]}")
    
    def printPlayerHistoryLn(self):
        self.printPlayerHistory()
        print()