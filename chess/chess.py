from constants.constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, ROWS, COLS
from constants.constants import (BLACK_HORSE_PATH, BLACK_BISHOP_PATH, BLACK_ROOK_PATH, BLACK_QUEEN_PATH,
                                 WHITE_HORSE_PATH, WHITE_BISHOP_PATH, WHITE_ROOK_PATH, WHITE_QUEEN_PATH)
from constants.constants import SCORE_BOARD_DICT
from constants.constants import MOVE_SOUND_PATH, KING_CHECKED_SOUND_PATH
from figures.figures import Bishop, Rook, Queen, Horse
from buttons.buttons import EndGameButton, FigureButton
from copy import deepcopy
import pygame

# Some icons are made by "https://www.flaticon.com/authors/pixel-perfect" from "https://www.flaticon.com/"

pygame.init()

MOVE_SOUND = pygame.mixer.Sound(MOVE_SOUND_PATH)
KING_CHECKED_SOUND = pygame.mixer.Sound(KING_CHECKED_SOUND_PATH)

WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Chess')


class Chess:
    def __init__(self, board):
        self.board_object = board
        self.board = board.chess_board  # 2D table of figures
        self.turn_color = 'white'  # white starts
        self.first_click_x = -1
        self.first_click_y = -1
        self.new_x = -2
        self.new_y = -2
        self.is_check = False
        # dict of positions (path) that is between player's king and opponent's queen/bishop/rook:
        self.check_path_dict = {}
        self.player_color = "white"
        self.ai_color = "black"

    def __repr__(self):
        return str(self.board_object)

    """ handles castling """

    def check_for_possible_castling(self):
        king_x, king_y = self.get_my_king_pos(self.turn_color)
        my_king = self.board[king_y][king_x]

        for key in my_king.valid_positions_dict:
            if key == 'long-castling' or key == 'short-castling':
                if key == 'long-castling':
                    rook_x = 0
                    temp = -1
                    if self.turn_color == 'white':
                        rook = self.board[7][0]
                    else:
                        rook = self.board[0][0]
                else:
                    rook_x = 7
                    temp = 1
                    if self.turn_color == 'white':
                        rook = self.board[7][7]
                    else:
                        rook = self.board[0][7]

                if rook:
                    if str(rook) == 'Rook':
                        if not rook.was_moved:
                            if self.check_for_empty_castling_path(rook_x, king_x, king_y):
                                if not self.is_check:
                                    for normal_move_key in my_king.valid_positions_dict:
                                        if normal_move_key == 'normal_moves':
                                            position_list = my_king.valid_positions_dict[normal_move_key]
                                            if [king_x + temp, king_y] not in position_list:
                                                my_king.valid_positions_dict[key] = []
                                else:
                                    my_king.valid_positions_dict[key] = []
                            else:
                                my_king.valid_positions_dict[key] = []
                        else:
                            my_king.valid_positions_dict[key] = []
                else:
                    my_king.valid_positions_dict[key] = []

    def check_for_empty_castling_path(self, rook_x, king_x, y):
        if rook_x < king_x:
            for x in range(rook_x + 1, king_x):
                if self.board[y][x]:
                    return False
        else:
            for x in range(king_x + 1, rook_x):
                if self.board[y][x]:
                    return False

        return True

    """ handling pawn transition here """

    def choose_pawn_transition_figure(self, win, x, y, color):
        change = True

        if color == 'white':
            queen_button = FigureButton(x, y, CELL_SIZE, CELL_SIZE, WHITE_QUEEN_PATH, (0, 0, 0))
            rook_button = FigureButton(x, y + CELL_SIZE + 3, CELL_SIZE, CELL_SIZE, WHITE_ROOK_PATH, (0, 0, 0))
            bishop_button = FigureButton(x, y + 2 * CELL_SIZE + 6, CELL_SIZE, CELL_SIZE, WHITE_BISHOP_PATH, (0, 0, 0))
            horse_button = FigureButton(x, y + 3 * CELL_SIZE + 9, CELL_SIZE, CELL_SIZE, WHITE_HORSE_PATH, (0, 0, 0))

        else:
            queen_button = FigureButton(x, y, CELL_SIZE, CELL_SIZE, BLACK_QUEEN_PATH, (0, 0, 0))
            rook_button = FigureButton(x, y - CELL_SIZE - 3, CELL_SIZE, CELL_SIZE, BLACK_ROOK_PATH, (0, 0, 0))
            bishop_button = FigureButton(x, y - 2 * CELL_SIZE - 6, CELL_SIZE, CELL_SIZE, BLACK_BISHOP_PATH, (0, 0, 0))
            horse_button = FigureButton(x, y - 3 * CELL_SIZE - 9, CELL_SIZE, CELL_SIZE, BLACK_HORSE_PATH, (0, 0, 0))

        buttons = [queen_button, rook_button, bishop_button, horse_button]

        while change:
            self.draw(win)
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    change = False

                for button in buttons:
                    if button.is_over(pos):
                        button.color = (0, 255, 0)
                    else:
                        button.color = (0, 0, 0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.is_over(pos):
                            return button.content

            if color == 'white':
                pygame.draw.rect(win, (255, 255, 255), (x, y, CELL_SIZE, 4 * CELL_SIZE))
            else:
                pygame.draw.rect(win, (255, 255, 255), (x, y - 3 * CELL_SIZE, CELL_SIZE, 4 * CELL_SIZE))

            for button in buttons:
                button.draw(win)

            pygame.display.update()

    def refresh_board(self, win):
        for row in self.board:
            for figure in row:
                if figure:
                    if figure.is_moved:
                        MOVE_SOUND.play()
                        if str(figure) == 'Pawn':
                            if figure.color == 'white':
                                if figure.y == 0:
                                    img = self.choose_pawn_transition_figure(win, figure.x * CELL_SIZE, figure.y * CELL_SIZE,
                                                                             figure.color)
                                    if img == WHITE_QUEEN_PATH:
                                        chosen_figure = Queen(figure.x, figure.y, CELL_SIZE, CELL_SIZE,
                                                              WHITE_QUEEN_PATH, 'white', 90)
                                    elif img == WHITE_BISHOP_PATH:
                                        chosen_figure = Bishop(figure.x, figure.y, CELL_SIZE, CELL_SIZE,
                                                               WHITE_BISHOP_PATH, 'white', 30)
                                    elif img == WHITE_ROOK_PATH:
                                        chosen_figure = Rook(figure.x, figure.y, CELL_SIZE, CELL_SIZE,
                                                             WHITE_ROOK_PATH, 'white', 50)
                                    else:
                                        chosen_figure = Horse(figure.x, figure.y, CELL_SIZE, CELL_SIZE,
                                                              WHITE_HORSE_PATH, 'white', 30)
                                    chosen_figure.is_moved = True
                                    self.board[figure.y][figure.x] = chosen_figure
                                else:
                                    self.board[figure.y][figure.x] = figure

                            # if figure.color == 'black':
                            #     if figure.y == 7:
                            #         img = self.choose_pawn_transition_figure(win, figure.x * CELL_SIZE, figure.y * CELL_SIZE,
                            #                                                  figure.color)
                            #         if img == BLACK_QUEEN_PATH:
                            #             chosen_figure = Queen(figure.x, figure.y, CELL_SIZE, CELL_SIZE,
                            #                                   BLACK_QUEEN_PATH, 'black', 90)
                            #         elif img == BLACK_BISHOP_PATH:
                            #             chosen_figure = Bishop(figure.x, figure.y, CELL_SIZE, CELL_SIZE,
                            #                                    BLACK_BISHOP_PATH, 'black', 30)
                            #         elif img == BLACK_ROOK_PATH:
                            #             chosen_figure = Rook(figure.x, figure.y, CELL_SIZE, CELL_SIZE,
                            #                                  BLACK_ROOK_PATH, 'black', 50)
                            #         else:
                            #             chosen_figure = Horse(figure.x, figure.y, CELL_SIZE, CELL_SIZE,
                            #                                   BLACK_HORSE_PATH, 'black', 30)
                            #         chosen_figure.is_moved = True
                            #         self.board[figure.y][figure.x] = chosen_figure
                            #     else:
                            #         self.board[figure.y][figure.x] = figure

                        else:
                            self.board[figure.y][figure.x] = figure
                        if self.turn_color == self.player_color:
                            self.board[self.first_click_y][self.first_click_x] = 0
                        self.change_turn()
                        return figure.x, figure.y

    def change_turn(self):
        for row in self.board:
            for figure in row:
                if figure:
                    if figure.is_moved:
                        figure.is_moved = False
                        self.first_click_x, self.first_click_y = -1, -1
                        self.new_x, self.new_y = -2, -2
                        if self.turn_color == 'white':
                            self.turn_color = 'black'
                        elif self.turn_color == 'black':
                            self.turn_color = 'white'

    def draw(self, win):
        self.board_object.draw(win)
        if self.turn_color == self.player_color:
            if self.first_click_x != -1:
                pygame.draw.rect(win, (0, 102, 0), 
                                 (self.first_click_x * CELL_SIZE, self.first_click_y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 4)
                figure = self.board[self.first_click_y][self.first_click_x]
                if figure:
                    for key in figure.valid_positions_dict:
                        position_list = figure.valid_positions_dict[key]
                        for position in position_list:
                            x, y = position[0], position[1]
                            pygame.draw.circle(win, (0, 102, 0), (int(x * CELL_SIZE + CELL_SIZE // 2), 
                                                                  int(y * CELL_SIZE + CELL_SIZE // 2)), 8)

    def set_move_that_confirm_king_safety(self, win, first_click_x, first_click_y):
        first_x_temp, first_y_temp = first_click_x, first_click_y
        clicked_figure = self.board[first_click_y][first_click_x]
        king_x, king_y = self.get_my_king_pos(self.turn_color)
        previous_figure = 0
        last_pos = []
        
        for key in clicked_figure.valid_positions_dict:
            position_list = clicked_figure.valid_positions_dict[key]
            temp = position_list[:]
            for position in position_list:
                new_x, new_y = position[0], position[1]
                self.board[first_click_y][first_click_x] = previous_figure

                previous_figure = self.board[new_y][new_x]

                self.board[new_y][new_x] = clicked_figure
                first_click_x, first_click_y = new_x, new_y
                if str(clicked_figure) == 'King':
                    king_x, king_y = self.get_my_king_pos(self.turn_color)
                    
                for row in self.board:
                    for figure in row:
                        if figure:
                            if figure.color != self.turn_color:
                                self.set_move_validity(figure.x, figure.y, figure.color)
                                for figure_key in figure.valid_positions_dict:
                                    pos_list = figure.valid_positions_dict[figure_key]
                                    for pos in pos_list:
                                        if pos[0] == king_x and pos[1] == king_y:
                                            if self.check_move_validity(win, figure.x, figure.y, king_x, king_y):
                                                if position in temp:
                                                    temp.remove(position)

                last_pos = position
            clicked_figure.valid_positions_dict[key] = temp[:]

        self.board[first_y_temp][first_x_temp] = clicked_figure
        
        if last_pos:
            self.board[last_pos[1]][last_pos[0]] = previous_figure

    def when_checked(self, win, color):
        for row in self.board:
            for figure in row:
                if figure:
                    if figure.color == color:
                        for key in figure.valid_positions_dict:
                            position_list = figure.valid_positions_dict[key]
                            temp = position_list[:]
                            for position in position_list:
                                for check_key in self.check_path_dict:
                                    if str(figure) == 'King':
                                        self.set_move_that_confirm_king_safety(win, figure.x, figure.y)
                                    else:
                                        if len(self.check_path_dict) > 1:
                                            if position in temp:
                                                temp.remove(position)
                                        elif position not in self.check_path_dict[check_key]:
                                            if not (position[0] == check_key[0] and position[1] == check_key[1]):
                                                temp.remove(position)

                            if str(figure) != 'King':
                                figure.valid_positions_dict[key] = temp[:]

    def set_move_validity(self, first_click_x, first_click_y, color):
        figure = self.board[first_click_y][first_click_x]
        figure.valid_positions()  # dict {move_type: str -> 2D List of positions [x, y]}

        for key in figure.valid_positions_dict:

            valid_path_list = []
            position_list = figure.valid_positions_dict[key]

            for position in position_list:
                x, y = position[0], position[1]

                if str(figure) == 'Pawn':
                    if key != 'up' and key != 'double-up':
                        if self.board[y][x]:
                            if self.board[y][x].color != color:
                                valid_path_list.append(position)
                    else:
                        if not self.board[y][x]:
                            if key == 'up':
                                valid_path_list.append(position)
                            else:
                                if figure.color == 'white':
                                    if not self.board[y + 1][x]:
                                        valid_path_list.append(position)
                                if figure.color == 'black':
                                    if not self.board[y - 1][x]:
                                        valid_path_list.append(position)

                elif str(figure) in ['Horse', 'King']:
                    if not self.board[y][x]:
                        valid_path_list.append(position)
                    elif self.board[y][x].color != color:
                        valid_path_list.append(position)

                elif str(figure) in ['Bishop', 'Rook', 'Queen']:
                    if not self.board[y][x]:
                        valid_path_list.append(position)
                    else:
                        if self.board[y][x].color == color:
                            break
                        else:
                            valid_path_list.append(position)
                            break

            figure.valid_positions_dict[key] = valid_path_list

    def check_move_validity(self, win, first_click_x, first_click_y, second_click_x, second_click_y):
        figure = self.board[first_click_y][first_click_x]
        for key in figure.valid_positions_dict:
            list_pos = figure.valid_positions_dict[key]
            for pos in list_pos:
                if second_click_x == pos[0] and second_click_y == pos[1]:
                    return True
        if self.is_check:
            KING_CHECKED_SOUND.play()
            king_x, king_y = self.get_my_king_pos(self.turn_color)
            pygame.draw.rect(win, (255, 0, 0), (king_x * CELL_SIZE, king_y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 4)
            self.draw(win)
            pygame.display.update()
            pygame.time.delay(1000)
        return False

    def move(self, win):
        run = True
        if self.turn_color == self.player_color:
            keys = pygame.mouse.get_pressed()
            if keys[0]:
                x, y = pygame.mouse.get_pos()
                x = int(x // CELL_SIZE)
                y = int(y // CELL_SIZE)
                if self.board[y][x] and (x != self.new_x or y != self.new_y):
                    if self.board[y][x].color == self.turn_color:
                        self.first_click_x = x
                        self.first_click_y = y
                if self.first_click_x != -1 and (x != self.first_click_x or y != self.first_click_y):
                    if self.board[y][x]:
                        if self.board[y][x].color != self.turn_color:
                            self.new_x = x
                            self.new_y = y
                    else:
                        self.new_x = x
                        self.new_y = y

                if self.first_click_x != -1:
                    figure = self.board[self.first_click_y][self.first_click_x]
                    if figure:
                        if figure.color != self.turn_color:
                            self.first_click_x, self.first_click_y = -1, -1
                            self.new_x, self.new_y = -2, -2
                        else:
                            self.check_for_check(self.turn_color)
                            self.set_move_validity(self.first_click_x, self.first_click_y, self.turn_color)
                            if self.is_check:
                                self.when_checked(win, self.turn_color)
                                if self.check_for_checkmate(self.turn_color):
                                    self.board_object.winner = self.ai_color
                                    run = self.end_game(win)
                            else:
                                self.set_move_that_confirm_king_safety(win, self.first_click_x, self.first_click_y)
                                if self.check_for_checkmate(self.turn_color):
                                    self.board_object.winner = "draw"
                                    run = self.end_game(win)

                            self.check_for_possible_castling()
                    else:
                        self.new_x, self.new_y = -2, -2

                    if self.new_x != -2:
                        if self.check_move_validity(win, self.first_click_x, self.first_click_y, self.new_x, self.new_y):
                            if str(figure) == 'King':
                                self.board_object.do_castling(self.first_click_x, self.first_click_y, self.new_x)

                            figure.move(self.new_x, self.new_y)
                            self.refresh_board(win)
                            self.is_check = False
                            self.check_path_dict = {}
                        else:
                            self.new_x, self.new_y = -2, -2
        return run

    def get_my_king_pos(self, color):
        king_x, king_y = -1, -1
        for row in range(ROWS):
            for col in range(COLS):
                figure = self.board[row][col]
                if figure:
                    if str(figure) == 'King':
                        if figure.color == color:
                            king_x = col
                            king_y = row
        return king_x, king_y

    def check_for_check(self, color):
        my_king_x, my_king_y = self.get_my_king_pos(color)
        for row in self.board:
            for figure in row:
                if figure:
                    if figure.color != color:
                        self.set_move_validity(figure.x, figure.y, figure.color)
                        for key in figure.valid_positions_dict:
                            pos_list = figure.valid_positions_dict[key]
                            for position in pos_list:
                                if my_king_x == position[0] and my_king_y == position[1]:
                                    key = (figure.x, figure.y)
                                    self.check_path_dict[key] = []
                                    if str(figure) in ['Queen', 'Rook', 'Bishop']:
                                        for check_path_position in pos_list:
                                            self.check_path_dict[key].append(check_path_position)
                                    self.is_check = True

    def check_for_checkmate(self, color):
        for row in self.board:
            for figure in row:
                if figure:
                    if figure.color == color:
                        for key in figure.valid_positions_dict:
                            if figure.valid_positions_dict[key]:
                                return False

        return True

    # calculates score for minimax algorithm
    def calculate_score(self) -> int:
        white_score = black_score = 0
        for row in self.board:
            for figure in row:
                if figure != 0:
                    key = figure.color + str(figure)
                    if figure.color == "white":
                        white_score += figure.score + SCORE_BOARD_DICT[key][figure.y][figure.x]
                    else:
                        black_score += figure.score + SCORE_BOARD_DICT[key][figure.y][figure.x]
        return black_score - white_score

    """ get_all_valid_moves(self, color)
        returns dict { piece: [[ [x1, y1,], [x2, y2], ..., [xn, yn] ]] } 
        where [xn, yn] is one possible move position for current user """
    
    def get_all_valid_moves(self, color, win=WIN):
        all_valid_positions = {}

        for row in self.board:
            for figure in row:
                if figure != 0:
                    if figure.color == color:
                        self.check_for_check(color)
                        self.set_move_validity(figure.x, figure.y, color)
                        if self.is_check:
                            self.when_checked(win, color)
                            if self.check_for_checkmate(color):
                                self.board_object.winner = color
                                # self.end_game(win)
                        else:
                            self.set_move_that_confirm_king_safety(win, figure.x, figure.y)
                            if self.check_for_checkmate(color):
                                self.board_object.winner = "draw"
                                # self.end_game(win)

                        self.check_for_possible_castling()

                        all_valid_positions[figure] = figure.valid_positions_dict.values()
                        all_valid_positions[figure] = [el for el in all_valid_positions[figure] if el]
                        if not all_valid_positions[figure]:
                            del all_valid_positions[figure]

                        self.is_check = False
                        self.check_path_dict = {}

        return all_valid_positions

    def ai_move(self, win, game):
        if self.board_object.winner is None:
            first_x, first_y = self.get_latest_ai_move(game)
            self.board_object = deepcopy(game.board_object)
            self.board = self.board_object.chess_board
            new_x, new_y = self.refresh_board(win)
            self.board_object.enemy_previous_move = new_x, new_y
            self.board_object.enemy_previous_position = first_x, first_y

    def get_latest_ai_move(self, game):
        changed_positions = []
        for y in range(ROWS):
            for x in range(COLS):
                if str(self.board[y][x]) != str(game.board[y][x]):
                    changed_positions.append((x, y))
        if len(changed_positions) > 2:
            return 4, 0
        else:
            for x, y in changed_positions:
                if not game.board[y][x]:
                    return x, y

    def reset_game(self):
        self.is_check = False
        self.turn_color = 'white'
        self.first_click_x = -1
        self.first_click_y = -1
        self.new_x = -2
        self.new_y = -2
        self.check_path_dict = {}
        self.board_object.create_board()
        self.board_object.winner = None
        self.board = self.board_object.chess_board

    def check_if_ai_checkmated_or_draw(self, win):
        for row in self.board:
            for figure in row:
                if figure != 0:
                    if figure.color == self.ai_color:
                        self.check_for_check(self.ai_color)
                        self.set_move_validity(figure.x, figure.y, figure.color)
                        if self.is_check:
                            self.when_checked(win, self.ai_color)
                        else:
                            self.set_move_that_confirm_king_safety(win, figure.x, figure.y)

        if self.is_check:
            if self.check_for_checkmate(self.ai_color):
                self.board_object.winner = self.player_color
                return True
        else:
            if self.check_for_checkmate(self.ai_color):
                self.board_object.winner = "draw"
                return True

        return False

    def end_game(self, win):
        play = True
        run = True

        if self.turn_color == 'white':
            self.turn_color = 'black'
        elif self.turn_color == 'black':
            self.turn_color = 'white'

        win.fill((255, 255, 255))
        font = pygame.font.SysFont('comicsans', 50)
        self.refresh_board(win)
        winner = self.board_object.winner.upper()
        if self.board_object.winner != "draw":
            winner += " WON"
        text = font.render(winner, 1, (255, 0, 0))
        win.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 100))

        play_again_button = EndGameButton(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 100, 'Play Again',
                                          (0, 128, 0))
        exit_button = EndGameButton(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 100, 'Exit', (128, 0, 0))

        while play:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    play = False
                    run = False

                if play_again_button.is_over(pos):
                    play_again_button.color = (0, 255, 0)
                else:
                    play_again_button.color = (0, 128, 0)
                if exit_button.is_over(pos):
                    exit_button.color = (255, 0, 0)
                else:
                    exit_button.color = (128, 0, 0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_button.is_over(pos):
                        pygame.time.delay(500)
                        self.reset_game()
                        play = False
                    if exit_button.is_over(pos):
                        play = False
                        run = False

            play_again_button.draw(win)
            exit_button.draw(win)
            pygame.display.update()

        return run
