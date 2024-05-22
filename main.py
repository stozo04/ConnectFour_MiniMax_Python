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

def isValidLocation(board, col):
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
            if board[r][c] == player and board[r - 1][c + 1] == player and board[r - 2][c + 2] == player and board[r - 3][c + 3] == player:
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
        if isValidLocation(board, c):  # Ensure the column is not completely filled
            row = getNextOpenRow(board, c)
            moves.append((row, c))
    return moves

def miniMax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = getAvailableMoves(board)
    is_terminal = winningMove(board, 1) or winningMove(board, 2) or isBoardFull(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winningMove(board, 2):
                return (None, 100000000000000)
            elif winningMove(board, 1):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, scorePosition(board, 2))
    if maximizingPlayer:
        value = -math.inf
        best_move = random.choice(valid_locations)
        for move in valid_locations:
            row, col = move
            b_copy = copy.deepcopy(board)
            dropPiece(b_copy, row, col, 2)
            new_score = miniMax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_move = move
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_move, value
    else:  # Minimizing player
        value = math.inf
        best_move = random.choice(valid_locations)
        for move in valid_locations:
            row, col = move
            b_copy = copy.deepcopy(board)
            dropPiece(b_copy, row, col, 1)
            new_score = miniMax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_move = move
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_move, value



def evaluateWindow(window, player):
    score = 0
    opponent = 1 if player == 2 else 2

    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opponent) == 3 and window.count(0) == 1:
        score -= 4

    return score

def scorePosition(board, player):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMNS // 2])]
    center_count = center_array.count(player)
    score += center_count * 6

    ## Score Horizontal
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMNS - 3):
            window = row_array[c:c + CONNECT_X]
            score += evaluateWindow(window, player)

    ## Score Vertical
    for c in range(COLUMNS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROWS - 3):
            window = col_array[r:r + CONNECT_X]
            score += evaluateWindow(window, player)

    ## Score positive sloped diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + i][c + i] for i in range(CONNECT_X)]
            score += evaluateWindow(window, player)

    ## Score negative sloped diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + 3 - i][c + i] for i in range(CONNECT_X)]
            score += evaluateWindow(window, player)

    return score


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

while not gameOver:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            gameOver = True

        if e.type == pygame.MOUSEMOTION:
            pygame.draw.rect(window, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            posx = e.pos[0]
            if player == 1:
                pygame.draw.circle(window, RED, (posx, int(SQUARE_SIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(window, YELLOW, (posx, int(SQUARE_SIZE / 2)), RADIUS)
            pygame.display.update()

        if e.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(window, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            posx = e.pos[0]
            col = int(math.floor(posx / SQUARE_SIZE))

            if isValidLocation(board, col):
                row = getNextOpenRow(board, col)
                dropPiece(board, row, col, player)

                if winningMove(board, player):
                    label = myfont.render("Player 1 wins!!", 1, RED)
                    screen.blit(label, (40, 10))
                    gameOver = True

                player = 2

                if not gameOver:
                    boardCopy = copy.deepcopy(board)
                    move, _ = miniMax(boardCopy, 5, -math.inf, math.inf, True)
                    if move is not None:
                        row, col = move
                        dropPiece(board, row, col, 2)
                        if winningMove(board, 2):
                            label = myfont.render("Player 2 wins!!", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            gameOver = True
                        player = 1

                if isBoardFull(board):
                    gameOver = True

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r:
                board = restartGame(board)
                gameOver = False
                player = 1

    if not gameOver:
        drawBoard(board)
    else:
        pygame.time.wait(3000)
