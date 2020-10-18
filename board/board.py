from constants.constants import (ROWS, COLS, CELL_SIZE, BLACK_PAWN_PATH, BLACK_HORSE_PATH, BLACK_BISHOP_PATH,
                                 BLACK_ROOK_PATH, BLACK_QUEEN_PATH, BLACK_KING_PATH, WHITE_PAWN_PATH, WHITE_HORSE_PATH,
                                 WHITE_BISHOP_PATH, WHITE_ROOK_PATH, WHITE_QUEEN_PATH, WHITE_KING_PATH)
from figures.figures import Pawn, Horse, Bishop, Queen, King, Rook
import pygame
import string


class Board:
    def __init__(self, color):
        self.color = color
        self.chess_board = [[0 for _ in range(ROWS)] for _ in range(COLS)]
        self.enemy_previous_move = 0, 0
        self.enemy_previous_position = 0, 0

    def __repr__(self):
        result = "\n"
        for row in self.chess_board:
            result += str(row)
            result += "\n"
        return result

    def create_board(self):
        self.enemy_previous_move = self.enemy_previous_position = 0
        for row in range(ROWS):
            for col in range(COLS):
                if row == 1:
                    pawn = Pawn(col, row, CELL_SIZE, CELL_SIZE, BLACK_PAWN_PATH, 'black', 10)
                    self.chess_board[row][col] = pawn

                elif row == 6:
                    pawn = Pawn(col, row, CELL_SIZE, CELL_SIZE, WHITE_PAWN_PATH, 'white', 10)
                    self.chess_board[row][col] = pawn

                elif row == 0:
                    if col == 1 or col == 6:
                        horse = Horse(col, row, CELL_SIZE, CELL_SIZE, BLACK_HORSE_PATH, 'black', 30)
                        self.chess_board[row][col] = horse
                    if col == 2 or col == 5:
                        bishop = Bishop(col, row, CELL_SIZE, CELL_SIZE, BLACK_BISHOP_PATH, 'black', 30)
                        self.chess_board[row][col] = bishop
                    if col == 3:
                        queen = Queen(col, row, CELL_SIZE, CELL_SIZE, BLACK_QUEEN_PATH, 'black', 90)
                        self.chess_board[row][col] = queen
                    if col == 4:
                        king = King(col, row, CELL_SIZE, CELL_SIZE, BLACK_KING_PATH, 'black', 900)
                        self.chess_board[row][col] = king
                    if col == 0 or col == 7:
                        rook = Rook(col, row, CELL_SIZE, CELL_SIZE, BLACK_ROOK_PATH, 'black', 50)
                        self.chess_board[row][col] = rook

                elif row == 7:
                    if col == 1 or col == 6:
                        horse = Horse(col, row, CELL_SIZE, CELL_SIZE, WHITE_HORSE_PATH, 'white', 30)
                        self.chess_board[row][col] = horse
                    if col == 2 or col == 5:
                        bishop = Bishop(col, row, CELL_SIZE, CELL_SIZE, WHITE_BISHOP_PATH, 'white', 30)
                        self.chess_board[row][col] = bishop
                    if col == 3:
                        queen = Queen(col, row, CELL_SIZE, CELL_SIZE, WHITE_QUEEN_PATH, 'white', 90)
                        self.chess_board[row][col] = queen
                    if col == 4:
                        king = King(col, row, CELL_SIZE, CELL_SIZE, WHITE_KING_PATH, 'white', 900)
                        self.chess_board[row][col] = king
                    if col == 0 or col == 7:
                        rook = Rook(col, row, CELL_SIZE, CELL_SIZE, WHITE_ROOK_PATH, 'white', 50)
                        self.chess_board[row][col] = rook

                else:
                    self.chess_board[row][col] = 0

    def draw(self, win):
        number = 8
        letters = string.ascii_lowercase[:8]
        font = pygame.font.SysFont('comicsans', 20)
        if self.enemy_previous_move:
            if self.enemy_previous_position:
                first_x, first_y = self.enemy_previous_position
                second_x, second_y = self.enemy_previous_move
                pygame.draw.rect(win, (255, 0, 255), (first_x * CELL_SIZE, first_y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 4)
                pygame.draw.rect(win, (255, 0, 255), (second_x * CELL_SIZE, second_y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 4)

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
                    win.blit(text, (col * CELL_SIZE + 5, row * CELL_SIZE + 10))
                if row == 7:
                    text = font.render(str(letters[col]), 1, (0, 0, 0))
                    win.blit(text, (col * CELL_SIZE + CELL_SIZE - 10, row * CELL_SIZE + CELL_SIZE - 20))
                if self.chess_board[row][col]:
                    self.chess_board[row][col].draw(win)

    def move(self, piece, x, y):
        self.chess_board[piece.y][piece.x] = piece
        if str(piece) == "King":
            self.do_castling(piece.x, piece.y, x)
        self.chess_board[piece.y][piece.x], self.chess_board[y][x] = self.chess_board[y][x], self.chess_board[piece.y][piece.x]

        piece.move(x, y)
        # handling piece promotion for AI -> pawn is automatically promoted to queen
        if str(piece) == "Pawn":
            if piece.y == 7:
                queen = Queen(x, y, CELL_SIZE, CELL_SIZE, BLACK_QUEEN_PATH, 'black', 90)
                queen.is_moved = True
                self.chess_board[y][x] = queen

    def remove(self, possible_removal):
        self.chess_board[possible_removal.y][possible_removal.x] = 0

    def do_castling(self, first_click_x, first_click_y, new_x):
        if first_click_x + 2 == new_x:
            self.chess_board[first_click_y][first_click_x + 1] = self.chess_board[first_click_y][
                first_click_x + 3]
            self.chess_board[first_click_y][first_click_x + 3] = 0
            rook = self.chess_board[first_click_y][first_click_x + 1]
            rook.x = first_click_x + 1
            rook.y = first_click_y
            rook.was_moved = True

        if first_click_x - 2 == new_x:
            self.chess_board[first_click_y][first_click_x - 1] = self.chess_board[first_click_y][
                first_click_x - 4]
            self.chess_board[first_click_y][first_click_x - 4] = 0
            rook = self.chess_board[first_click_y][first_click_x - 1]
            rook.x = first_click_x - 1
            rook.y = first_click_y
            rook.was_moved = True
