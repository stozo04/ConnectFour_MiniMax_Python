import math
import pygame
import numpy as np
import random

# GLOBAL VARIABLES
ROWS = 6
COLUMNS = 7
CONNECT_X = 4
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 5)
WIDTH = COLUMNS * SQUARE_SIZE
HEIGHT = (ROWS + 1) * SQUARE_SIZE

# COLORS
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

class ConnectFour:
    def __init__(self):
        try:
            pygame.init()
            self.board = self.createBoard()
            self.gameOver = False
            self.turn = 0
            self.window = pygame.display.set_mode((COLUMNS * SQUARE_SIZE, (ROWS + 1) * SQUARE_SIZE))
            self.myfont = pygame.font.SysFont("monospace", 75)
        except pygame.error as e:
            print(f"Error initializing Pygame: {e}")
            raise SystemExit(e)
    
    def createBoard(self):
        return np.zeros((ROWS, COLUMNS))
    
    def printBoard(self):
        print(np.flip(self.board, 0))
    
    def drawBoard(self):
        for c in range(COLUMNS):
            for r in range(ROWS):
                pygame.draw.rect(self.window, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.circle(self.window, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
        
        for c in range(COLUMNS):
            for r in range(ROWS):
                if self.board[r][c] == 1:
                    pygame.draw.circle(self.window, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT-int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(self.window, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT-int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
        
        pygame.display.update()

    def dropPiece(self, board, row, col, player):
        board[row][col] = player

    def isValidLocation(self, col):
        if col < 0 or col >= COLUMNS:
            return False
        return self.board[ROWS - 1][col] == 0

    def getNextOpenRow(self, col):
        for r in range(ROWS):
            if self.board[r][col] == 0:
                return r

    def winningMove(self, player):
        # Check horizontal, vertical, and diagonal win conditions
        for c in range(COLUMNS - 3):
            for r in range(ROWS):
                if self.board[r][c] == player and self.board[r][c + 1] == player and self.board[r][c + 2] == player and self.board[r][c + 3] == player:
                    return True
        
        for c in range(COLUMNS):
            for r in range(ROWS - 3):
                if self.board[r][c] == player and self.board[r + 1][c] == player and self.board[r + 2][c] == player and self.board[r + 3][c] == player:
                    return True

        for c in range(COLUMNS - 3):
            for r in range(ROWS - 3):
                if self.board[r][c] == player and self.board[r + 1][c + 1] == player and self.board[r + 2][c + 2] == player and self.board[r + 3][c + 3] == player:
                    return True

        for c in range(COLUMNS - 3):
            for r in range(3, ROWS):
                if self.board[r][c] == player and self.board[r - 1][c + 1] == player and self.board[r - 2][c + 2] == player and self.board[r - 3][c + 3] == player:
                    return True
    
    def handlePlayerMove(self, player, posx):
        col = int(math.floor(posx / SQUARE_SIZE))
        if not self.isValidLocation(col):
            print(f"Invalid column: {col}. Try again.")
            return False
        row = self.getNextOpenRow(col)
        self.dropPiece(self.board, row, col, player)

        if self.winningMove(player):
            label = self.myfont.render(f"Player {player} Wins!!", 1, RED if player == 1 else YELLOW)
            self.window.blit(label, (40, 10))
            self.gameOver = True
        return True

    def evaluateWindow(self, window, player):
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

    def scorePosition(self, board, player):
        score = 0

        # Score center column
        center_array = [int(i) for i in list(board[:, COLUMNS // 2])]
        center_count = center_array.count(player)
        score += center_count * 3

        # Score Horizontal
        for r in range(ROWS):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(COLUMNS - 3):
                window = row_array[c:c + 4]
                score += self.evaluateWindow(window, player)

        # Score Vertical
        for c in range(COLUMNS):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROWS - 3):
                window = col_array[r:r + 4]
                score += self.evaluateWindow(window, player)

        # Score positive sloped diagonal
        for r in range(ROWS - 3):
            for c in range(COLUMNS - 3):
                window = [board[r + i][c + i] for i in range(4)]
                score += self.evaluateWindow(window, player)

        # Score negative sloped diagonal
        for r in range(ROWS - 3):
            for c in range(COLUMNS - 3):
                window = [board[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluateWindow(window, player)

        return score

    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(COLUMNS):
            if self.isValidLocation(col):
                valid_locations.append(col)
        return valid_locations

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        is_terminal = self.winningMove(1) or self.winningMove(2) or len(self.get_valid_locations(board)) == 0
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winningMove(1):
                    return (None, 100000000000000)
                elif self.winningMove(2):
                    return (None, -10000000000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, self.scorePosition(board, 1))
        
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(self.get_valid_locations(board))
            for col in self.get_valid_locations(board):
                row = self.getNextOpenRow(col)
                b_copy = board.copy()
                self.dropPiece(b_copy,row, col, 1)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else: # Minimizing player
            value = math.inf
            column = random.choice(self.get_valid_locations(board))
            for col in self.get_valid_locations(board):
                row = self.getNextOpenRow(col)
                b_copy = board.copy()
                self.dropPiece(b_copy, row, col, 2)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def runGame(self):
        self.drawBoard()
        pygame.display.update()

        while not self.gameOver:
            if self.turn == 0:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        self.gameOver = True

                    if e.type == pygame.MOUSEMOTION:
                        pygame.draw.rect(self.window, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                        posx = e.pos[0]
                        pygame.draw.circle(self.window, RED if self.turn == 0 else YELLOW, (posx, int(SQUARE_SIZE / 2)), RADIUS)
                        pygame.display.update()

                    if e.type == pygame.MOUSEBUTTONDOWN:
                        pygame.draw.rect(self.window, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                        posx = e.pos[0]
                        if self.handlePlayerMove(1, posx):
                            self.printBoard()
                            self.drawBoard()
                            self.turn = 1

                            if self.gameOver:
                                pygame.time.wait(5000)

            # AI's turn
            if self.turn == 1 and not self.gameOver:
                col, minimax_score = self.minimax(self.board, 5, -math.inf, math.inf, True)
                if self.handlePlayerMove(2, col * SQUARE_SIZE):
                    self.printBoard()
                    self.drawBoard()
                    self.turn = 0

                    if self.gameOver:
                        pygame.time.wait(5000)

        pygame.quit()

if __name__ == "__main__":
    game = ConnectFour()
    game.runGame()
