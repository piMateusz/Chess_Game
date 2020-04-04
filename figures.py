from abc import ABC
import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
ROWS = 8
COLS = 8
CELL_SIZE = SCREEN_WIDTH/8   # 80


class ChessPiece(ABC):
    def __init__(self, x, y, width, height, img, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(img)
        self.color = color
        self.is_moved = False
        self.valid_positions_dict = {}
        self.was_moved = False

    # abstract method
    def valid_positions(self):
        pass

    # abstract method
    def __repr__(self):
        pass

    def move(self, new_x, new_y):
        self.x, self.y = new_x, new_y
        self.is_moved = True
        if not self.was_moved:
            self.was_moved = True

    def draw(self, win):
        win.blit(self.image, (self.x*CELL_SIZE + self.width // 2 - self.image.get_width() // 2,
                              self.y*CELL_SIZE + self.height // 2 - self.image.get_height() // 2))


class Pawn(ChessPiece):
    def __repr__(self):
        return "Pawn"

    def valid_positions(self):
        x, y = self.x, self.y
        self.valid_positions_dict = {'up': [], 'up-right': [], 'up-left': [], 'double-up': []}
        if self.color == 'white':
            if y == 6:
                self.valid_positions_dict['double-up'].append([x, y - 2])
            if y - 1 >= 0:
                self.valid_positions_dict['up'].append([x, y - 1])
                if x - 1 >= 0:
                    self.valid_positions_dict['up-left'].append([x - 1, y - 1])
                if x + 1 < COLS:
                    self.valid_positions_dict['up-right'].append([x + 1, y - 1])
        if self.color == 'black':
            if y == 1:
                self.valid_positions_dict['double-up'].append([x, y + 2])
            if y + 1 < ROWS:
                self.valid_positions_dict['up'].append([x, y + 1])
                if x - 1 >= 0:
                    self.valid_positions_dict['up-left'].append([x - 1, y + 1])
                if x + 1 < COLS:
                    self.valid_positions_dict['up-right'].append([x + 1, y + 1])


class Horse(ChessPiece):
    def __repr__(self):
        return "Horse"

    def valid_positions(self):
        x, y = self.x, self.y
        self.valid_positions_dict = {'all_moves': []}
        if x - 2 >= 0:
            if y + 1 < ROWS:
                self.valid_positions_dict['all_moves'].append([x - 2, y + 1])
            if y - 1 >= 0:
                self.valid_positions_dict['all_moves'].append([x - 2, y - 1])

        if x - 1 >= 0:
            if y + 2 < ROWS:
                self.valid_positions_dict['all_moves'].append([x - 1, y + 2])
            if y - 2 >= 0:
                self.valid_positions_dict['all_moves'].append([x - 1, y - 2])

        if x + 1 < COLS:
            if y - 2 >= 0:
                self.valid_positions_dict['all_moves'].append([x + 1, y - 2])
            if y + 2 < ROWS:
                self.valid_positions_dict['all_moves'].append([x + 1, y + 2])

        if x + 2 < COLS:
            if y - 1 >= 0:
                self.valid_positions_dict['all_moves'].append([x + 2, y - 1])
            if y + 1 < ROWS:
                self.valid_positions_dict['all_moves'].append([x + 2, y + 1])


class King(ChessPiece):
    def __repr__(self):
        return "King"

    def valid_positions(self):
        x, y = self.x, self.y
        self.valid_positions_dict = {'short-castling': [], 'long-castling': [], 'normal_moves': []}
        for j in range(-1, 2):
            for k in range(-1, 2):
                if not j == k == 0:
                    if 0 <= x + j < COLS:
                        if 0 <= y + k < ROWS:
                            self.valid_positions_dict['normal_moves'].append([x + j, y + k])

        if not self.was_moved:
            if self.color == 'white':
                self.valid_positions_dict['long-castling'].append([2, 7])
                self.valid_positions_dict['short-castling'].append([6, 7])
            if self.color == 'black':
                self.valid_positions_dict['long-castling'].append([2, 0])
                self.valid_positions_dict['short-castling'].append([6, 0])


class Rook(ChessPiece):
    def __repr__(self):
        return "Rook"

    def valid_positions(self):
        x, y = self.x, self.y
        self.valid_positions_dict = get_valid_pos_straight(x, y)


class Bishop(ChessPiece):
    def __repr__(self):
        return "Bishop"

    def valid_positions(self):
        x, y = self.x, self.y
        self.valid_positions_dict = get_valid_pos_cross(x, y)


class Queen(ChessPiece):
    def __repr__(self):
        return "Queen"

    def valid_positions(self):
        x, y = self.x, self.y
        valid_positions_dict_straight = get_valid_pos_straight(x, y)
        self.valid_positions_dict = get_valid_pos_cross(x, y)
        # all keys are different so simply
        self.valid_positions_dict.update(valid_positions_dict_straight)


""" 
    This function takes 3 input arguments:
        list:      list of lists which contains x, y positions
        x:         x_position
        y:         y_position
    And have 1 output:
        new_list which is sorted input list
        
    new_list is sorted from elements with the lowest distance from its position_x, position_y 
        to input arguments x, y, to this with the biggest distance 
"""


def sorting(position_list, x, y):
    new_list = []
    for pos in position_list:
        new_pos = pos[:]
        pos_x, pos_y = pos[0], pos[1]
        x_distance = abs(x - pos_x)
        y_distance = abs(y - pos_y)
        new_pos.append(x_distance + y_distance)
        new_list.append(new_pos)
    new_list = sorted(new_list, key=lambda element: element[2])
    for pos in new_list:
        pos.pop(2)
    return new_list


def get_valid_pos_cross(x, y):
    val_positions = {'right-up': [], 'right-down': [], 'left-up': [], 'left-down': []}
    for j in range(-7, 8):
        if j:
            if 0 <= x + j < COLS:
                if 0 <= y + j < ROWS:
                    if j > 0:
                        val_positions['right-down'].append([x + j, y + j])
                    else:
                        val_positions['left-up'].append([x + j, y + j])
            if 0 <= x + j < COLS:
                if 0 <= y - j < ROWS:
                    if j > 0:
                        val_positions['right-up'].append([x + j, y - j])
                    else:
                        val_positions['left-down'].append([x + j, y - j])

    # sorting
    for key in val_positions:
        val_positions[key] = sorting(val_positions[key], x, y)

    return val_positions


def get_valid_pos_straight(x, y):
    val_positions = {'up': [], 'down': [], 'right': [], 'left': []}
    for j in range(-7, 8):
        if j:
            if 0 <= x + j < COLS:
                if j > 0:
                    val_positions['right'].append([x + j, y])
                else:
                    val_positions['left'].append([x + j, y])
            if 0 <= y + j < ROWS:
                if j > 0:
                    val_positions['up'].append([x, y + j])
                else:
                    val_positions['down'].append([x, y + j])

    # sorting
    for key in val_positions:
        val_positions[key] = sorting(val_positions[key], x, y)

    return val_positions
