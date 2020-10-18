import os
import pygame
import numpy as np


""" SCREEN SETTINGS """
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
ROWS = 8
COLS = 8
CELL_SIZE = SCREEN_WIDTH/8   # 80


""" SOUND SETTINGS """
MOVE_SOUND_PATH = os.path.join('sounds', 'chess_move_sound.wav')
KING_CHECKED_SOUND_PATH = os.path.join('sounds', 'king_checked_sound.wav')


""" IMAGES SETTING"""
BLACK_PAWN_PATH = os.path.join('img', 'black_pawn.png')
BLACK_HORSE_PATH = os.path.join('img', 'black_horse.png')
BLACK_BISHOP_PATH = os.path.join('img', 'black_bishop.png')
BLACK_ROOK_PATH = os.path.join('img', 'black_rook.png')
BLACK_QUEEN_PATH = os.path.join('img', 'black_queen.png')
BLACK_KING_PATH = os.path.join('img', 'black_king.png')

WHITE_PAWN_PATH = os.path.join('img', 'white_pawn.png')
WHITE_HORSE_PATH = os.path.join('img', 'white_horse.png')
WHITE_BISHOP_PATH = os.path.join('img', 'white_bishop.png')
WHITE_ROOK_PATH = os.path.join('img', 'white_rook.png')
WHITE_QUEEN_PATH = os.path.join('img', 'white_queen.png')
WHITE_KING_PATH = os.path.join('img', 'white_king.png')

IMAGES = {
    BLACK_PAWN_PATH: pygame.image.load(BLACK_PAWN_PATH),
    BLACK_HORSE_PATH: pygame.image.load(BLACK_HORSE_PATH),
    BLACK_BISHOP_PATH: pygame.image.load(BLACK_BISHOP_PATH),
    BLACK_ROOK_PATH: pygame.image.load(BLACK_ROOK_PATH),
    BLACK_QUEEN_PATH: pygame.image.load(BLACK_QUEEN_PATH),
    BLACK_KING_PATH: pygame.image.load(BLACK_KING_PATH),
    WHITE_PAWN_PATH: pygame.image.load(WHITE_PAWN_PATH),
    WHITE_HORSE_PATH: pygame.image.load(WHITE_HORSE_PATH),
    WHITE_BISHOP_PATH: pygame.image.load(WHITE_BISHOP_PATH),
    WHITE_ROOK_PATH: pygame.image.load(WHITE_ROOK_PATH),
    WHITE_QUEEN_PATH: pygame.image.load(WHITE_QUEEN_PATH),
    WHITE_KING_PATH: pygame.image.load(WHITE_KING_PATH)
}


""" SCORE BOARDS """
WHITE_KING_SCORE_BOARD = [
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
    [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]
]

WHITE_QUEEN_SCORE_BOARD = [
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
    [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
    [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
    [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
    [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
]

WHITE_ROOK_SCORE_BOARD = [
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]
]

WHITE_BISHOP_SCORE_BOARD = [
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
    [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
    [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
    [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
    [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
]

WHITE_HORSE_SCORE_BOARD = [
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
    [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
    [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
    [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
    [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
    [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
    [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
]

WHITE_PAWN_SCORE_BOARD = [
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
    [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
    [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
    [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
    [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
    [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
]

BLACK_KING_SCORE_BOARD = np.flip(WHITE_KING_SCORE_BOARD, 0)
BLACK_QUEEN_SCORE_BOARD = np.flip(WHITE_QUEEN_SCORE_BOARD, 0)
BLACK_ROOK_SCORE_BOARD = np.flip(WHITE_ROOK_SCORE_BOARD, 0)
BLACK_BISHOP_SCORE_BOARD = np.flip(WHITE_BISHOP_SCORE_BOARD, 0)
BLACK_HORSE_SCORE_BOARD = np.flip(WHITE_HORSE_SCORE_BOARD, 0)
BLACK_PAWN_SCORE_BOARD = np.flip(WHITE_PAWN_SCORE_BOARD, 0)

SCORE_BOARD_DICT = {
                    "whiteKing": WHITE_KING_SCORE_BOARD, "whiteQueen": WHITE_QUEEN_SCORE_BOARD,
                    "whiteRook": WHITE_ROOK_SCORE_BOARD, "whiteBishop": WHITE_BISHOP_SCORE_BOARD,
                    "whiteHorse": WHITE_HORSE_SCORE_BOARD, "whitePawn": WHITE_PAWN_SCORE_BOARD,
                    "blackKing": BLACK_KING_SCORE_BOARD, "blackQueen": BLACK_QUEEN_SCORE_BOARD,
                    "blackRook": BLACK_ROOK_SCORE_BOARD, "blackBishop": BLACK_BISHOP_SCORE_BOARD,
                    "blackHorse": BLACK_HORSE_SCORE_BOARD, "blackPawn": BLACK_PAWN_SCORE_BOARD
}
