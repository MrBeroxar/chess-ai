import os
from io import StringIO
import timeit
import contextlib
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

import chess_ai.chess_engine as chess
from chess_ai import move


script_dir = os.path.dirname(os.path.abspath(__file__))
benchmark_file = os.path.join(script_dir, "boards_and_moves.txt")
current_best_move = None
current_debug_info = {}
df_benchmarkings = pd.DataFrame(
    columns=["function", "depth", "iterations", "nodes", "average_time", "total_time"]
)
current_date = date.today().strftime("%Y-%m-%d")


def suppress_prints():
    return StringIO()


def bench_best_move(depth, board):
    with contextlib.redirect_stdout(suppress_prints()):
        with contextlib.redirect_stderr(suppress_prints()):
            global current_best_move
            global current_debug_info

            best_move, debug_info = move.next_move(depth, board, return_debug_info=True)
            current_best_move = best_move
            current_debug_info = debug_info


def benchmark_to_df(function, depth, iteration, nodes, avg, tot):
    df_benchmarkings.loc[len(df_benchmarkings)] = {
        "function": function,
        "depth": depth,
        "iterations": iteration,
        "nodes": nodes,
        "average_time": avg,
        "total_time": tot,
    }


def benchmark_template(msg, n, result_func, depth, board):
    print(f"\n=========\n{msg}\n=========\n")

    result = result_func.__call__(depth, board)

    msg = "Total: {}s, Average: {}ms - {} - {}"
    total_time = round(result, 4)
    average_time = round(result / n * 1000, 2)

    print(
        msg.format(
            total_time,
            average_time,
            len(board.getValidMoves()),
            board.fen(),
        )
    )

    move_details = [str(x) for x in current_debug_info["move_details"].values()]
    move_details.reverse()
    benchmark_to_df(
        result_func,
        depth,
        n,
        current_debug_info["nodes_searched"],
        average_time,
        total_time,
    )
    return str(current_best_move), (
        current_debug_info["nodes_searched"],
        move_details,
    )


def benchmark_best_move(depth, boards, n, msg):
    def bench(depth, board):
        return timeit.timeit(
            lambda: bench_best_move(depth, board),
            number=n,
            globals=locals(),
        )

    return [benchmark_template(msg, n, bench, depth, board) for board in boards]


def plot():
    grouped = df_benchmarkings.groupby("nodes")
    plt.figure(figsize=(8, 6))
    for name, group in grouped:
        depth = group["depth"]
        average_time = group["average_time"]
        label = f"Nodes: {name}"
        plt.bar(depth, average_time, label=label)
    plt.xlabel("Depth")
    plt.ylabel("Average Time in ms")
    plt.title("Average Time vs Depth (Grouped by Nodes)")
    plt.legend()
    plt.grid(True)
    plt.savefig(
        f"benchmarks/depth_benchmarking/plot_{current_date}.png",
        dpi=300,
        bbox_inches="tight",
    )


def benchmark():
    max_depth = 5
    number_of_runs = [500, 100, 20, 5, 1]
    boards = [
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "r1bqkbnr/pppppppp/n7/6N1/8/8/PPPPPPPP/RNBQKB1R b - - 0 1",
    ]
    msg = "Benchmark best move for depth #, number of iterations $"

    for i in range(max_depth):
        info = benchmark_best_move(
            i + 1,
            [chess.GameState(board) for board in boards],
            number_of_runs[i],
            msg.replace("#", str(i + 1)).replace("$", str(number_of_runs[i])),
        )
        print(info)
    df_benchmarkings.to_csv(
        f"benchmarks/depth_benchmarking/bestmove_benchmarking_{current_date}.csv"
    )
    plot()


if __name__ == "__main__":
    benchmark()
