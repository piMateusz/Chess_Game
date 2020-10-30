from copy import deepcopy


def minimax(game, depth, max_player):

    if depth == 0 or game.board_object.winner is not None:
        return game.calculate_score(), game

    if max_player:
        max_eval = float('-inf')
        best_move = None

        all_games = get_all_games(game, "black")
        for game in all_games:
            game.turn_color = "white"
            evaluation = minimax(game, depth - 1, False)[0]
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = game

        return max_eval, best_move

    else:
        min_eval = float('inf')
        best_move = None

        all_games = get_all_games(game, "white")
        for game in all_games:
            game.turn_color = "black"
            evaluation = minimax(game, depth - 1, True)[0]
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = game

        return min_eval, best_move


def simulate_move(piece, move, board, possible_removal):
    if possible_removal:
        board.remove(possible_removal)

    board.move(piece, move[0], move[1])

    return board


def get_all_games(game, color):
    games = []

    # valid_moves - > dict {piece: [[ [x1, y1,], [x2, y2], ..., [xn, yn] ]]} where [xn, yn] is one possible move pos.
    valid_moves = game.get_all_valid_moves(color)

    for piece, direction in valid_moves.items():
        for moves_in_one_direction in direction:
            for move_position in moves_in_one_direction:
                # method which draws possible moves -> uncomment it to see all AI moves calculations
                # draw_moves(game, game.board, piece)
                temp_game = deepcopy(game)
                temp_piece = deepcopy(piece)
                possible_removal = temp_game.board_object.chess_board[move_position[1]][move_position[0]]
                new_board = simulate_move(temp_piece, move_position, temp_game.board_object, possible_removal)
                temp_game.board_object = new_board
                temp_game.board = new_board.chess_board
                games.append(temp_game)

    return games
