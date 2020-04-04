from figures import ROWS, COLS, CELL_SIZE, Pawn, Horse, Bishop, Queen, King, Rook
import pygame
import string
import os


class Board:
    def __init__(self, color):
        self.color = color
        self.chess_board = [[0 for _ in range(ROWS)] for _ in range(COLS)]

    def create_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                if row == 1:
                    pawn = Pawn(col, row, CELL_SIZE, CELL_SIZE, os.path.join('img', 'black_pawn.png'), 'black')
                    self.chess_board[row][col] = pawn

                elif row == 6:
                    pawn = Pawn(col, row, CELL_SIZE, CELL_SIZE, os.path.join('img', 'white_pawn.png'), 'white')
                    self.chess_board[row][col] = pawn

                elif row == 0:
                    if col == 1 or col == 6:
                        horse = Horse(col, row, CELL_SIZE, CELL_SIZE, os.path.join('img', 'black_horse.png'), 'black')
                        self.chess_board[row][col] = horse
                    if col == 2 or col == 5:
                        bishop = Bishop(col, row, CELL_SIZE, CELL_SIZE, os.path.join('img', 'black_bishop.png'), 'black')
                        self.chess_board[row][col] = bishop
                    if col == 3:
                        queen = Queen(col, row, CELL_SIZE, CELL_SIZE, os.path.join('img', 'black_queen.png'), 'black')
                        self.chess_board[row][col] = queen
                    if col == 4:
                        king = King(col, row, CELL_SIZE, CELL_SIZE, os.path.join('img', 'black_king.png'), 'black')
                        self.chess_board[row][col] = king
                    if col == 0 or col == 7:
                        rook = Rook(col, row, CELL_SIZE, CELL_SIZE, os.path.join('img', 'black_rook.png'), 'black')
                        self.chess_board[row][col] = rook

                elif row == 7:
                    if col == 1 or col == 6:
                        horse = Horse(col, row, CELL_SIZE, CELL_SIZE, os.path.join('img', 'white_horse.png'), 'white')
                        self.chess_board[row][col] = horse
                    if col == 2 or col == 5:
                        bishop = Bishop(col, row, CELL_SIZE, CELL_SIZE, os.path.join('img', 'white_bishop.png'), 'white')
                        self.chess_board[row][col] = bishop
                    if col == 3:
                        queen = Queen(col, row, CELL_SIZE, CELL_SIZE, os.path.join('img', 'white_queen.png'), 'white')
                        self.chess_board[row][col] = queen
                    if col == 4:
                        king = King(col, row, CELL_SIZE, CELL_SIZE, os.path.join('img', 'white_king.png'), 'white')
                        self.chess_board[row][col] = king
                    if col == 0 or col == 7:
                        rook = Rook(col, row, CELL_SIZE, CELL_SIZE, os.path.join('img', 'white_rook.png'), 'white')
                        self.chess_board[row][col] = rook

                else:
                    self.chess_board[row][col] = 0

    def draw(self, win):
        number = 8
        letters = string.ascii_lowercase[:8]
        font = pygame.font.SysFont('comicsans', 20)

        for row in range(ROWS):
            for col in range(COLS):
                if row % 2:
                    if not col % 2:
                        pygame.draw.rect(win, self.color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                if not row % 2:
                    if col % 2:
                        pygame.draw.rect(win, self.color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                if col == 0:
                    text = font.render(str(number), 1, (0, 0, 0))
                    number -= 1
                    win.blit(text, (col*CELL_SIZE + 5, row*CELL_SIZE + 10))
                if row == 7:
                    text = font.render(str(letters[col]), 1, (0, 0, 0))
                    win.blit(text, (col*CELL_SIZE + CELL_SIZE - 10, row*CELL_SIZE + CELL_SIZE - 20))
                if self.chess_board[row][col]:
                    self.chess_board[row][col].draw(win)
