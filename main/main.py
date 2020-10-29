import pygame
from board.board import Board
from chess.chess import Chess, WIN, RUN
from minimax.algorithm import minimax


def redraw_game_window(win):
    win.fill((255, 255, 179))
    chess_game.move(win)
    chess_game.draw(win)
    pygame.display.update()


board = Board((102, 51, 0))
board.create_board()
chess_game = Chess(board)

# mainloop

if __name__ == "__main__":

    while RUN:

        redraw_game_window(WIN)

        if chess_game.turn_color == chess_game.ai_color:
            if chess_game.check_if_ai_checkmated_or_draw(WIN):
                chess_game.end_game(WIN)
            else:
                value, new_game = minimax(chess_game, 2, True)
                chess_game.ai_move(WIN, new_game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False

    pygame.quit()
