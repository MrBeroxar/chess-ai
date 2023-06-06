import time
import random
from typing import List

from tqdm import tqdm

import chess_ai.chess_engine as chess
from chess_ai.evaluate import evaluate_board
from chess_ai.log import debug_info


def next_move(
    depth: int, board: chess.GameState, debug=True, return_debug_info=False
) -> chess.Move:
    if debug:
        debug_info["nodes_searched"] = 0

    move = minimax_root(depth, board)

    if return_debug_info:
        return move, debug_info
    return move


def get_ordered_moves(board: chess.GameState) -> List[chess.Move]:
    def orderer(move):
        return evaluate_board(board, move)

    in_order = sorted(board.getValidMoves(), key=orderer, reverse=(board.white_to_move))
    return list(in_order)


def minimax_root(depth: int, board: chess.GameState) -> chess.Move:
    maximize = board.white_to_move
    best_move = -float("inf") if maximize else float("inf")

    moves = get_ordered_moves(board)

    if len(moves) == 0:
        return None

    best_move_found = moves[0]

    start_time = time.time()
    allocated_time = 100

    for move in tqdm(moves, desc="Searching moves..."):
        if not maximize:
            index = random.randint(0, len(moves) - 1)
            return moves[index]

        if time.time() - start_time >= allocated_time:
            return best_move_found

        board.makeMove(move)
        value = alpha_beta(depth - 1, board, not maximize)
        board.undoMove()

        if maximize and value >= best_move:
            best_move = value
            best_move_found = move
        elif not maximize and value <= best_move:
            best_move = value
            best_move_found = move
    return best_move_found


def alpha_beta(
    depth: int,
    board: chess.GameState,
    is_maximising_player: bool,
) -> float:
    if is_maximising_player:
        return alpha_beta_max(-float("inf"), float("inf"), depth, board)
    else:
        return alpha_beta_min(-float("inf"), float("inf"), depth, board)


def alpha_beta_max(alpha, beta, depth, board):
    debug_info["nodes_searched"] += 1

    if depth == 0:
        return evaluate_board(board)

    moves = get_ordered_moves(board)

    for move in moves:
        board.makeMove(move)
        current_value = alpha_beta_min(alpha, beta, depth - 1, board)
        board.undoMove()

        if current_value >= beta:
            return beta
        if current_value > alpha:
            alpha = current_value
            debug_info["move_details"][depth] = move.coordinate()
    return alpha


def alpha_beta_min(alpha, beta, depth, board):
    debug_info["nodes_searched"] += 1

    if depth == 0:
        return evaluate_board(board)

    moves = get_ordered_moves(board)

    for move in moves:
        board.makeMove(move)
        current_value = alpha_beta_max(alpha, beta, depth - 1, board)
        board.undoMove()

        if current_value <= alpha:
            return alpha
        if current_value < beta:
            beta = current_value
            debug_info["move_details"][depth] = move.coordinate()
    return beta
