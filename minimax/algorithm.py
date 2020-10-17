from copy import deepcopy
# import pygame


def minimax(game, depth, max_player):
    if depth == 0 or game.winner is not None:
        return game.calculate_score(), game.board

    if max_player:
        maxEval = float('-inf')
        best_move = None

        all_games = get_all_games(game, "black")

        for game in all_games:
            game.turn_color = "white"
            evaluation = minimax(game, depth - 1, False)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = game

        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        all_games = get_all_games(game, "white")

        for game in all_games:
            game.turn_color = "black"
            evaluation = minimax(game, depth - 1, True)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = game

        return minEval, best_move


def simulate_move(piece, move, board, possible_removal):
    if possible_removal:
        board.remove(possible_removal)

    board.move(piece, move[0], move[1])

    return board


def get_all_games(game, color):
    games = []

    # valid_moves - > dict {piece: all_possible_moves_positions}
    valid_moves = game.get_all_valid_moves(color)

    for piece, direction in valid_moves.items():
        for moves_in_one_direction in direction:
            for move_position in moves_in_one_direction:
                # draw_moves(game, board, piece)
                temp_game = deepcopy(game)
                temp_piece = deepcopy(piece)
                possible_removal = temp_game.board_object.chess_board[move_position[1]][move_position[0]]
                new_board = simulate_move(temp_piece, move_position, temp_game.board_object, possible_removal)
                temp_game.board_object = new_board
                temp_game.board = new_board.chess_board
                games.append(temp_game)

    return games


# def draw_moves(game, board, piece):
#     valid_moves = board.get_valid_moves(piece)
#     board.draw(game.win)
#     pygame.draw.circle(game.win, (0, 255, 0), (piece.x, piece.y), 50, 5)
#     game.draw_valid_moves(valid_moves.keys())
#     pygame.display.update()
#     pygame.time.delay(100)
