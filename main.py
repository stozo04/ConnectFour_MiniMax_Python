import math
import pygame
import numpy as np

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

    def dropPiece(self, row, col, player):
        self.board[row][col] = player

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
        self.dropPiece(row, col, player)

        if self.winningMove(player):
            label = self.myfont.render(f"Player {player} Wins!!", 1, RED if player == 1 else YELLOW)
            self.window.blit(label, (40, 10))
            self.gameOver = True
        return True

    def runGame(self):
        self.drawBoard()
        pygame.display.update()

        while not self.gameOver:
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
                    if self.handlePlayerMove(self.turn + 1, posx):
                        self.drawBoard()
                        self.turn = (self.turn + 1) % 2

                        if self.gameOver:
                            pygame.time.wait(5000)
        
        pygame.quit()

if __name__ == "__main__":
    game = ConnectFour()
    game.runGame()
