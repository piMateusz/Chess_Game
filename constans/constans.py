import os
import pygame

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
