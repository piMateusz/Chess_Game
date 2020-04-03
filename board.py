from figures import rows, cols, cell_size, Pawn, Horse, Bishop, Queen, King, Rook
import pygame
import string


class Board:
    def __init__(self, color):
        self.color = color
        self.chess_board = [[0 for _ in range(rows)] for _ in range(cols)]

    def create_board(self):
        for row in range(rows):
            for col in range(cols):
                if row == 1:
                    pawn = Pawn(col, row, cell_size, cell_size, 'img/black_pawn.png', 'black')
                    self.chess_board[row][col] = pawn

                elif row == 6:
                    pawn = Pawn(col, row, cell_size, cell_size, 'img/white_pawn.png', 'white')
                    self.chess_board[row][col] = pawn

                elif row == 0:
                    if col == 1 or col == 6:
                        horse = Horse(col, row, cell_size, cell_size, 'img/black_horse.png', 'black')
                        self.chess_board[row][col] = horse
                    if col == 2 or col == 5:
                        bishop = Bishop(col, row, cell_size, cell_size, 'img/black_bishop.png', 'black')
                        self.chess_board[row][col] = bishop
                    if col == 3:
                        queen = Queen(col, row, cell_size, cell_size, 'img/black_queen.png', 'black')
                        self.chess_board[row][col] = queen
                    if col == 4:
                        king = King(col, row, cell_size, cell_size, 'img/black_king.png', 'black')
                        self.chess_board[row][col] = king
                    if col == 0 or col == 7:
                        rook = Rook(col, row, cell_size, cell_size, 'img/black_rook.png', 'black')
                        self.chess_board[row][col] = rook

                elif row == 7:
                    if col == 1 or col == 6:
                        horse = Horse(col, row, cell_size, cell_size, 'img/white_horse.png', 'white')
                        self.chess_board[row][col] = horse
                    if col == 2 or col == 5:
                        bishop = Bishop(col, row, cell_size, cell_size, 'img/white_bishop.png', 'white')
                        self.chess_board[row][col] = bishop
                    if col == 3:
                        queen = Queen(col, row, cell_size, cell_size, 'img/white_queen.png', 'white')
                        self.chess_board[row][col] = queen
                    if col == 4:
                        king = King(col, row, cell_size, cell_size, 'img/white_king.png', 'white')
                        self.chess_board[row][col] = king
                    if col == 0 or col == 7:
                        rook = Rook(col, row, cell_size, cell_size, 'img/white_rook.png', 'white')
                        self.chess_board[row][col] = rook

                else:
                    self.chess_board[row][col] = 0

    def draw(self, win):
        number = 8
        letters = string.ascii_lowercase[:8]
        font = pygame.font.SysFont('comicsans', 20)

        for row in range(rows):
            for col in range(cols):
                if row % 2:
                    if not col % 2:
                        pygame.draw.rect(win, self.color, (col * cell_size, row * cell_size, cell_size, cell_size))
                if not row % 2:
                    if col % 2:
                        pygame.draw.rect(win, self.color, (col * cell_size, row * cell_size, cell_size, cell_size))
                if col == 0:
                    text = font.render(str(number), 1, (0, 0, 0))
                    number -= 1
                    win.blit(text, (col*cell_size + 5, row*cell_size + 10))
                if row == 7:
                    text = font.render(str(letters[col]), 1, (0, 0, 0))
                    win.blit(text, (col*cell_size + cell_size - 10, row*cell_size + cell_size - 20))
                if self.chess_board[row][col]:
                    self.chess_board[row][col].draw(win)
