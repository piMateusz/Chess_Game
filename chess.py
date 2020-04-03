from figures import screen_width, screen_height, cell_size, rows, cols
from figures import Bishop, Rook, Queen, Horse
from buttons import EndGameButton, FigureButton
from board import Board
import pygame

# Some icons are made by "https://www.flaticon.com/authors/pixel-perfect" from "https://www.flaticon.com/"

pygame.init()

win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Chess')

move_sound = pygame.mixer.Sound('sounds/move_sound.wav')


class Chess:
    def __init__(self, board):
        self.board_object = board
        self.board = board.chess_board      # 2D table of figures
        self.turn_color = 'white'           # white starts
        self.first_click_x = -1
        self.first_click_y = -1
        self.new_x = -2
        self.new_y = -2
        self.is_check = False
        # dict of positions (path) that is between player's king and opponent's queen/bishop/rook:
        self.check_path_dict = {}

    """ handling castling here """

    def check_for_possible_castling(self):
        king_x, king_y = self.get_my_king_pos()
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
                    if rook.__repr__() == 'Rook':
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

    def do_castling(self):
        if self.first_click_x + 2 == self.new_x:
            self.board[self.first_click_y][self.first_click_x + 1] = self.board[self.first_click_y][self.first_click_x + 3]
            self.board[self.first_click_y][self.first_click_x + 3] = 0
            self.board[self.first_click_y][self.first_click_x + 1].x = self.first_click_x + 1
            self.board[self.first_click_y][self.first_click_x + 1].y = self.first_click_y

        if self.first_click_x - 2 == self.new_x:
            self.board[self.first_click_y][self.first_click_x - 1] = self.board[self.first_click_y][self.first_click_x - 4]
            self.board[self.first_click_y][self.first_click_x - 4] = 0
            self.board[self.first_click_y][self.first_click_x - 1].x = self.first_click_x - 1
            self.board[self.first_click_y][self.first_click_x - 1].y = self.first_click_y

    """ handling pawn transition here """

    @ staticmethod
    def choose_pawn_transition_figure(x, y, color):
        change = True
        global run

        if color == 'white':
            queen_button = FigureButton(x, y, cell_size, cell_size, 'img/' + str(color) + '_queen.png', (0, 0, 0))
            rook_button = FigureButton(x, y + cell_size + 3, cell_size, cell_size, 'img/' + str(color) + '_rook.png', (0, 0, 0))
            bishop_button = FigureButton(x, y + 2 * cell_size + 6, cell_size, cell_size, 'img/' + str(color) + '_bishop.png', (0, 0, 0))
            horse_button = FigureButton(x, y + 3 * cell_size + 9, cell_size, cell_size, 'img/' + str(color) + '_horse.png', (0, 0, 0))

        else:
            queen_button = FigureButton(x, y, cell_size, cell_size, 'img/' + str(color) + '_queen.png', (0, 0, 0))
            rook_button = FigureButton(x, y - cell_size - 3, cell_size, cell_size, 'img/' + str(color) + '_rook.png', (0, 0, 0))
            bishop_button = FigureButton(x, y - 2 * cell_size - 6, cell_size, cell_size, 'img/' + str(color) + '_bishop.png', (0, 0, 0))
            horse_button = FigureButton(x, y - 3 * cell_size - 9, cell_size, cell_size, 'img/' + str(color) + '_horse.png', (0, 0, 0))

        buttons = [queen_button, rook_button, bishop_button, horse_button]

        while change:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    change = False
                    run = False

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
                pygame.draw.rect(win, (255, 255, 255), (x, y, cell_size, 4 * cell_size))
            else:
                pygame.draw.rect(win, (255, 255, 255), (x, y - 3 * cell_size, cell_size, 4 * cell_size))

            for button in buttons:
                button.draw(win)

            pygame.display.update()

    def refresh_board(self):
        for row in self.board:
            for figure in row:
                if figure:
                    if figure.is_moved:
                        if figure.__repr__() == 'Pawn':
                            if figure.color == 'white':
                                if figure.y == 0:
                                    img = self.choose_pawn_transition_figure(figure.x * cell_size, figure.y * cell_size, figure.color)
                                    if img == 'img/white_queen.png':
                                        chosen_figure = Queen(figure.x, figure.y, cell_size, cell_size,
                                                              'img/white_queen.png', 'white')
                                    elif img == 'img/white_bishop.png':
                                        chosen_figure = Bishop(figure.x, figure.y, cell_size, cell_size,
                                                              'img/white_bishop.png', 'white')
                                    elif img == 'img/white_rook.png':
                                        chosen_figure = Rook(figure.x, figure.y, cell_size, cell_size,
                                                              'img/white_rook.png', 'white')
                                    else:
                                        chosen_figure = Horse(figure.x, figure.y, cell_size, cell_size,
                                                              'img/white_horse.png', 'white')
                                    chosen_figure.is_moved = True
                                    self.board[figure.y][figure.x] = chosen_figure
                                else:
                                    self.board[figure.y][figure.x] = figure
                            if figure.color == 'black':
                                if figure.y == 7:
                                    img = self.choose_pawn_transition_figure(figure.x * cell_size, figure.y * cell_size, figure.color)
                                    if img == 'img/black_queen.png':
                                        chosen_figure = Queen(figure.x, figure.y, cell_size, cell_size,
                                                              'img/black_queen.png', 'black')
                                    elif img == 'img/black_bishop.png':
                                        chosen_figure = Bishop(figure.x, figure.y, cell_size, cell_size,
                                                              'img/black_bishop.png', 'black')
                                    elif img == 'img/black_rook.png':
                                        chosen_figure = Rook(figure.x, figure.y, cell_size, cell_size,
                                                              'img/black_rook.png', 'black')
                                    else:
                                        chosen_figure = Horse(figure.x, figure.y, cell_size, cell_size,
                                                              'img/black_horse.png', 'black')
                                    chosen_figure.is_moved = True
                                    self.board[figure.y][figure.x] = chosen_figure
                                else:
                                    self.board[figure.y][figure.x] = figure
                        else:
                            self.board[figure.y][figure.x] = figure
                        self.board[self.first_click_y][self.first_click_x] = 0
                        self.change_turn()

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
        if self.first_click_x != -1:
            pygame.draw.rect(win, (255, 0, 0),
                             (self.first_click_x * cell_size, self.first_click_y * cell_size, cell_size, cell_size), 2)
            figure = self.board[self.first_click_y][self.first_click_x]
            if figure:
                for key in figure.valid_positions_dict:
                    position_list = figure.valid_positions_dict[key]
                    for position in position_list:
                        x, y = position[0], position[1]
                        pygame.draw.circle(win, (255, 0, 0), (int(x*cell_size + cell_size//2), int(y*cell_size + cell_size//2)), 5)

    def set_move_that_confirm_king_safety(self, first_click_x, first_click_y):
        first_x_temp, first_y_temp = first_click_x, first_click_y
        clicked_figure = self.board[first_click_y][first_click_x]
        king_x, king_y = self.get_my_king_pos()
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
                if clicked_figure.__repr__() == 'King':
                    king_x, king_y = self.get_my_king_pos()
                for row in self.board:
                    for figure in row:
                        if figure:
                            if figure.color != self.turn_color:
                                self.set_move_validity(figure.x,
                                                       figure.y, figure.color)
                                for figure_key in figure.valid_positions_dict:
                                    pos_list = figure.valid_positions_dict[figure_key]
                                    for pos in pos_list:
                                        if pos[0] == king_x and pos[1] == king_y:
                                            if self.check_move_validity(figure.x,
                                                                        figure.y, king_x, king_y):
                                                if position in temp:
                                                    temp.remove(position)

                last_pos = position
            clicked_figure.valid_positions_dict[key] = temp[:]

        self.board[first_y_temp][first_x_temp] = clicked_figure
        if last_pos:
            self.board[last_pos[1]][last_pos[0]] = previous_figure

    def when_checked(self):
        for row in self.board:
            for figure in row:
                if figure:
                    if figure.color == self.turn_color:
                        for key in figure.valid_positions_dict:
                            position_list = figure.valid_positions_dict[key]
                            temp = position_list[:]
                            for position in position_list:
                                for check_key in self.check_path_dict:
                                    if figure.__repr__() == 'King':
                                        self.set_move_that_confirm_king_safety(figure.x, figure.y)
                                    else:
                                        if len(self.check_path_dict) > 1:
                                            temp.remove(position)
                                        elif position not in self.check_path_dict[check_key]:
                                            if not (position[0] == check_key[0] and position[1] == check_key[1]):
                                                temp.remove(position)

                            if figure.__repr__() != 'King':
                                figure.valid_positions_dict[key] = temp[:]

    def set_move_validity(self, first_click_x, first_click_y, color):
        figure = self.board[first_click_y][first_click_x]
        figure.valid_positions()  # dict {str(move_type)  :  List of Tuples}

        for key in figure.valid_positions_dict:

            valid_path_list = []
            position_list = figure.valid_positions_dict[key]

            for position in position_list:
                x, y = position[0], position[1]

                if figure.__repr__() == 'Pawn':
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

                elif figure.__repr__() == 'Horse' or figure.__repr__() == 'King':
                    if not self.board[y][x]:
                        valid_path_list.append(position)
                    elif self.board[y][x].color != color:
                        valid_path_list.append(position)

                elif figure.__repr__() == 'Bishop' or figure.__repr__() == 'Rook' or figure.__repr__() == 'Queen':
                    if not self.board[y][x]:
                        valid_path_list.append(position)
                    else:
                        if self.board[y][x].color == color:
                            break
                        else:
                            valid_path_list.append(position)
                            break

            figure.valid_positions_dict[key] = valid_path_list

    def check_move_validity(self, first_click_x, first_click_y, second_click_x, second_click_y):
        figure = self.board[first_click_y][first_click_x]
        for key in figure.valid_positions_dict:
            list_pos = figure.valid_positions_dict[key]
            for pos in list_pos:
                if second_click_x == pos[0] and second_click_y == pos[1]:
                    return True
        return False

    def move(self):
        keys = pygame.mouse.get_pressed()
        if keys[0]:
            x, y = pygame.mouse.get_pos()
            x = int(x // cell_size)
            y = int(y // cell_size)
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
                        self.check_for_check()
                        self.set_move_validity(self.first_click_x, self.first_click_y, self.turn_color)
                        if self.is_check:
                            self.when_checked()
                            if self.check_for_checkmate():
                                self.end_game(win)
                        else:
                            self.set_move_that_confirm_king_safety(self.first_click_x, self.first_click_y)
                        self.check_for_possible_castling()
                else:
                    self.new_x, self.new_y = -2, -2

                if self.new_x != -2:
                    if self.check_move_validity(self.first_click_x, self.first_click_y, self.new_x, self.new_y):
                        if figure.__repr__() == 'King':
                            self.do_castling()

                        figure.move(self.new_x, self.new_y)
                        move_sound.play()
                        self.refresh_board()
                        self.is_check = False
                        self.check_path_dict = {}
                    else:
                        self.new_x, self.new_y = -2, -2

    def get_my_king_pos(self):
        king_x, king_y = -1, -1
        for row in range(rows):
            for col in range(cols):
                figure = self.board[row][col]
                if figure:
                    if figure.__repr__() == 'King':
                        if figure.color == self.turn_color:
                            king_x = col
                            king_y = row
        return king_x, king_y

    def check_for_check(self):
        my_king_x, my_king_y = self.get_my_king_pos()
        for row in self.board:
            for figure in row:
                if figure:
                    if figure.color != self.turn_color:
                        self.set_move_validity(figure.x, figure.y, figure.color)
                        for key in figure.valid_positions_dict:
                            pos_list = figure.valid_positions_dict[key]
                            for position in pos_list:
                                if my_king_x == position[0] and my_king_y == position[1]:
                                    key = (figure.x, figure.y)
                                    self.check_path_dict[key] = []
                                    if figure.__repr__() in ['Queen', 'Rook', 'Bishop']:
                                        for check_path_position in pos_list:
                                            self.check_path_dict[key].append(check_path_position)
                                    self.is_check = True

    def check_for_checkmate(self):
        for row in self.board:
            for figure in row:
                if figure:
                    if figure.color == self.turn_color:
                        # print('figure: ', figure)
                        # print('valid dict: ', figure.valid_positions_dict)
                        for key in figure.valid_positions_dict:
                            if figure.valid_positions_dict[key]:
                                return False
        return True

    def reset_game(self):
        self.is_check = False
        self.turn_color = 'white'
        self.first_click_x = -1
        self.first_click_y = -1
        self.new_x = -2
        self.new_y = -2
        self.check_path_dict = {}
        self.board_object.create_board()
        self.board = self.board_object.chess_board

    def end_game(self, win):
        play = True
        global run

        if chess_game.turn_color == 'white':
            chess_game.turn_color = 'black'
        elif chess_game.turn_color == 'black':
            chess_game.turn_color = 'white'

        win.fill((255, 255, 255))
        font = pygame.font.SysFont('comicsans', 50)
        chess_game.refresh_board()
        text = font.render(chess_game.turn_color.upper() + ' WON !', 1, (255, 0, 0))
        win.blit(text, (screen_width // 2 - text.get_width()//2, 100))

        play_again_button = EndGameButton(screen_width // 2 - 100, screen_height // 2 - 100, 200, 100, 'Play Again', (0, 128, 0))
        exit_button = EndGameButton(screen_width // 2 - 100, screen_height // 2 + 50, 200, 100, 'Exit', (128, 0, 0))

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


def redraw_game_window(win):
    win.fill((255, 255, 255))
    chess_game.draw(win)
    chess_game.move()
    pygame.display.update()


run = True
board = Board((122, 155, 122))
board.create_board()
chess_game = Chess(board)

# mainloop

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    redraw_game_window(win)

pygame.quit()
