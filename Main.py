import json
from os.path import exists
from TicTacToe import TicTacToe
from PlayerHuman import PlayerHuman
from PlayerRandom import PlayerRandom
from PlayerQTable import PlayerQTable
from PlayerMinimax import PlayerMinimax

def singleTest(player1, player2):
    game = TicTacToe(player1, player2)
    player1.game = game
    player2.game = game
    game.printStarterLn()
    game.runAndPrintFinalResultLn()
    game.printBoardLn()
    player1.printPlayerHistoryLn()
    player2.printPlayerHistoryLn()

def generateGames(player1, player2, gamesCount, agentEvaluation = False):
    p1Episodes = []
    p2Episodes = []
    p1Win = 0
    p2Win = 0
    noWin = 0

    for i in range(0, gamesCount):
        starter = 0 if gamesCount == 1 else 1 if i < gamesCount / 2 else 2
        game = TicTacToe(player1, player2, starter = starter)
        player1.game = game
        player2.game = game
        result = game.run()
        p1Episodes.append(player1.episode)
        p2Episodes.append(player2.episode)

        if agentEvaluation == True:
            if result == game.NO_WINNERS:
                noWin += 1
            elif result == game.CURRENT_PLAYER_WINS:
                if game.player.id == 1:
                    p1Win += 1
                else:
                    p2Win += 1
            elif result == game.OPPONENT_PLAYER_WINS:
                if game.opponent.id == 1:
                    p1Win += 1
                else:
                    p2Win += 1
        
        player1.clean()
        player2.clean()
    
    if agentEvaluation == True:
        print(f"Player1 => {p1Win / gamesCount * 100}%, Player2 => {p2Win / gamesCount * 100}%, Draw => {noWin / gamesCount * 100}%")
    
    return (p1Episodes, p2Episodes)

def saveQTableTo(path, qTable):
    file = open(path, "w")
    json.dump(qTable, file)

def loadQTableFrom(path):
    file = open(path, "r")
    qTable = json.load(file)
    return qTable

EPSILON = 10
BATCH_SIZE = 500
LEARN_GAMES = 10_000
TEST_GAMES = 10_000
TRAIN_AGENT = False
TEST_AGENT = True

p1QTablePath = "Modify this and put your path to the Q-Table!" #TODO
p2QTablePath = "Modify this and put your path to the Q-Table!" #TODO
p1QTable = loadQTableFrom(p1QTablePath) if exists(p1QTablePath) else {}
p2QTable = loadQTableFrom(p2QTablePath) if exists(p2QTablePath) else {}

if TRAIN_AGENT == True:
    for i in range(0, BATCH_SIZE):
        print(f"=========================== Start Batch {i}... ===========================")
        print("Playing Q-Table vs. Q-Table Game...")
        generateGames( \
            PlayerQTable(1, qTable = p1QTable, enableTraining = True, epsilon = EPSILON, debug = False), \
            PlayerQTable(2, qTable = p2QTable, enableTraining = True, epsilon = EPSILON, debug = False), \
            LEARN_GAMES, True)
        saveQTableTo(p1QTablePath, p1QTable)
        saveQTableTo(p2QTablePath, p2QTable)

if TEST_AGENT == True:
    print(f"=========================== Start  Testing... ===========================")
    print("Playing Q-Table vs. Random Game...")
    generateGames(PlayerQTable(1, qTable = p1QTable, enableTraining = False), PlayerRandom(2), TEST_GAMES, True)
    print("Playing Q-Table vs. Minimax Game...")
    generateGames(PlayerQTable(1, qTable = p1QTable, enableTraining = False), PlayerMinimax(2), TEST_GAMES, True)
    print("Playing Q-Table vs. Human Game...")
    singleTest(PlayerQTable(1, qTable = p1QTable, enableTraining = False), PlayerHuman(2))