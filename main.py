import math
import random
import pygame
import copy
import numpy as np

# GLOBAL VARIABLES

ROWS = 6
COLUMNS = 7
CONNECT_X = 4 # How many connected pieces win
SQUARE_SIZE = 100 # Size of window and playing objects
RADIUS = int(SQUARE_SIZE / 2 - 5)
WIDTH = COLUMNS * SQUARE_SIZE
HEIGHT = (ROWS + 1) * SQUARE_SIZE

# COLORS
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


window = pygame.display.set_mode((COLUMNS * SQUARE_SIZE, (ROWS + 1) * SQUARE_SIZE)) # + 1 is for the space to drop token

# FUNCTIONS

def printBoard(board):
    print(np.flip(board, 0))

def createBoard():
    board = np.zeros((ROWS, COLUMNS))
    return board

def drawBoard(board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            # Board
            pygame.draw.rect(window, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            # Empty Space
            pygame.draw.circle(window, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    for c in range(COLUMNS):
        for r in range(ROWS):
            # Player 1
            if board[r][c] == 1:
                pygame.draw.circle(window, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT-int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            # Player 2
            elif board[r][c] == 2:
                 pygame.draw.circle(window, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT-int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    pygame.display.update()

def dropPiece(board, row, col, player):
    board[row][col] = player

def isValidLoaction(board, col):
    # Check if the top row contains 0 (means it is available)
    return board[ROWS - 1][col] == 0

def getNextOpenRow(board, col):
       for r in range(ROWS):
         if board[r][col] == 0:
             return r

def winningMove(board, player):
     # Check horizontal for win
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board[r][c] == player and board[r][c + 1] == player and board[r][c + 2] == player and board[r][c + 3] == player:
                return True

    # Check vertical for win
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == player and board[r + 1][c] == player and board[r + 2][c] == player and board[r + 3][c] == player:
                return True

    # Check right diagonal for win
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == player and board[r + 1][c + 1] == player and board[r + 2][c + 2] == player and board[r + 3][c + 3] == player:
                return True

    # Check left diagonal for win
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if board[r][c] == player and board[r - 1][c + 1] == player and board[r - 2][c + 2] == player and board[r +- 3][c + 3] == player:
                return True

def restartGame(board):
    board = np.zeros((ROWS, COLUMNS))
    return board

def isBoardFull(board):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == 0:
                return False
    return True

def getAvailableMoves(board):
    moves = []
    for c in range(COLUMNS):
        row = getNextOpenRow(board, c)
        if row is not None:  # Check if the column is not completely filled
            if board[col][row] == 0:
                moves.append((row, c))

    print("Available Moves: ", moves)
    return moves

def miniMax(baordCopy, depth, isMaximizing):
    if depth == 0:
        return (None, 0)
    if winningMove(baordCopy, 1):
        return (None, -math.inf)
    elif winningMove(baordCopy, 2):
        return (None, math.inf)
    elif isBoardFull(baordCopy): # That means there are no valid moves
        return (None, 0)

    if(isMaximizing): # Simulating AI Move (maximize)
        bestScore = -math.inf
        bestMove = (-1, -1)
        for move in getAvailableMoves(baordCopy):
            row, col = move  # Unpack the move tuple into row and col
            # Apply the move to the game state
            baordCopy[row][col] = 2
            printBoard(baordCopy)
            move, minimax_score = miniMax(baordCopy, depth - 1, False)
            if minimax_score is not None and minimax_score > bestScore:
                if move is None:
                    availableMove = getAvailableMoves(baordCopy)
                    bestMove = random.choice(availableMove)
                else:
                    bestMove = move
            bestScore = minimax_score
                
        return bestMove, bestScore

    else: # Human  Player
        lowestScore = math.inf
        worstMove = (-1, -1)
        for move in getAvailableMoves(baordCopy):
            row, col = move  # Unpack the move tuple into row and col
            # Apply the move to the game state
            baordCopy[row][col] = 1
            printBoard(baordCopy)
            move, minimax_score = miniMax(baordCopy, depth - 1, True)

            if minimax_score is not None and minimax_score < lowestScore:
                if move is None:
                    availableMove = getAvailableMoves(baordCopy)
                    worstMove = random.choice(availableMove)
                else:
                    worstMove = move
                    
            lowestScore = minimax_score

        return worstMove, lowestScore

# def bestMove(board, depth, isMaximizing):
#     bestScore = -math.inf
#     bestMove  = (-1, -1)
#     boardCopy = board
#     for move in getAvailableMoves(boardCopy):
#         row, col = move  # Unpack the move tuple into row and col
#          # Apply the move to the game state
#         boardCopy[row][col] = 2
#         score = miniMax(boardCopy, depth, isMaximizing)
#         if score > bestScore:
#             bestScore = score
#             bestMove = move

#     if bestMove != (-1, -1):
#         row, col = move  # Unpack the move tuple into row and col
#         board[row][col] = move
#         return True
#     return False

board = createBoard()
printBoard(board)
gameOver = False
player = 1
pygame.init()
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
drawBoard(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while True:
    for e in pygame.event.get():

        # Check if user wants to quit
        if e.type == pygame.QUIT: 
            gameOver = True

        if e.type == pygame.MOUSEMOTION:
            pygame.draw.rect(window, BLACK, (0,0, WIDTH, SQUARE_SIZE))
            posx = e.pos[0]
            if player == 1:
                pygame.draw.circle(window, RED, (posx, int(SQUARE_SIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(window, YELLOW, (posx, int(SQUARE_SIZE / 2)), RADIUS)
        pygame.display.update()

        if e.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(window, BLACK, (0,0, WIDTH, SQUARE_SIZE))
           
            # Grab location of user mouse click
            posx = e.pos[0]
            col = int(math.floor(posx / SQUARE_SIZE))
            if isValidLoaction(board, col):
                row = getNextOpenRow(board, col)
                dropPiece(board, row, col, player)
                if winningMove(board , player):
                    label = myfont.render("Player 1 wins!!", 1, RED)
                    screen.blit(label, (40, 10)) # Updates specific part of screen
                    gameOver = True
                
                player = 2
                
                if not gameOver:
                    boardCopy = copy.copy(board)
                    move, minimax_score = miniMax(boardCopy, 3, True) # if miniMax(board, 5, True):
                    if move is not None:
                        row, col = move  # Unpack the move tuple into row and col
                        # Apply the move to the game state
                        board[row][col] = 2
                        if winningMove(board, player):
                            gameOver = True
                        player = 1
                
                if not gameOver:
                    if isBoardFull(board):
                        gameOver = True

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r:
                restartGame()
                gameOver = False
                player = 1
    
    if not gameOver:
        # printBoard(board)
        drawBoard(board)
        pygame.display.update()

    else:
        pygame.time.wait(5000)
