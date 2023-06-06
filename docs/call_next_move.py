import chess_ai.chess_engine as chess
from chess_ai.move import next_move

fen_string = "rnbqkbnr/1pppppp1/p6p/8/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 1 3"

depths = [1, 2, 3]
for depth in depths:
    best_move = next_move(depth, chess.GameState(fen_string))
    print("Best move at depth", depth, ":", best_move)
