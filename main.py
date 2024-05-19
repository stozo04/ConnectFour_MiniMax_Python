import math
import pygame
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
 

board = createBoard()
printBoard(board)
gameOver = False
turn = 0
pygame.init()
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
drawBoard(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not gameOver:
    
    for e in pygame.event.get():

        # Check if user wants to quit
        if e.type == pygame.QUIT: 
            gameOver = True

        if e.type == pygame.MOUSEMOTION:
            pygame.draw.rect(window, BLACK, (0,0, WIDTH, SQUARE_SIZE))
            posx = e.pos[0]
            if turn == 0:
                pygame.draw.circle(window, RED, (posx, int(SQUARE_SIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(window, YELLOW, (posx, int(SQUARE_SIZE / 2)), RADIUS)
        pygame.display.update()

        if e.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(window, BLACK, (0,0, WIDTH, SQUARE_SIZE))
            if turn == 0:
                # Grab location of user mouse click
                posx = e.pos[0]
                col = int(math.floor(posx / SQUARE_SIZE))

                if isValidLoaction(board, col):
                    row = getNextOpenRow(board, col)
                    dropPiece(board, row, col, 1)

                    if winningMove(board , 1):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10)) # Updates specific part of screen
                        gameOver = True

            else:
                  # Grab location of user mouse click
                posx = e.pos[0]
                col = int(math.floor(posx / SQUARE_SIZE))

                if isValidLoaction(board, col):
                    row = getNextOpenRow(board, col)
                    dropPiece(board, row, col, 2)

                    if winningMove(board , 2):
                        label = myfont.render("Player 1 wins!!", 1, YELLOW)
                        screen.blit(label, (40, 10)) # Updates specific part of screen
                        gameOver = True

            printBoard(board)
            drawBoard(board)
            turn += 1
            turn = turn % 2

            if gameOver:
                pygame.time.wait(5000)

quit()
