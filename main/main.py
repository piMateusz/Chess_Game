import pygame
from board.board import Board
from chess.chess import Chess, WIN
from minimax.algorithm import minimax


def redraw_game_window(win, game):
    win.fill((255, 255, 179))
    run = game.move(win)
    game.draw(win)
    pygame.display.update()
    return run


board = Board((102, 51, 0))
board.create_board()
chess_game = Chess(board)
RUN = True
DEPTH = 2

# mainloop

if __name__ == "__main__":

    while RUN:

        RUN = redraw_game_window(WIN, chess_game)

        if chess_game.turn_color == chess_game.ai_color:
            if chess_game.check_if_ai_checkmated_or_draw(WIN):
                RUN = chess_game.end_game(WIN)
            else:
                value, new_game = minimax(chess_game, DEPTH, True)
                chess_game.ai_move(WIN, new_game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False

    pygame.quit()
