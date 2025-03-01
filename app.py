# app.py

from flask import Flask, request, jsonify
from sudoku_solver import solve_sudoku
from flask_cors import CORS


app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route("/")
def index():
    return "Sudoku Solver API is running!"

@app.route("/solve", methods=["POST"])
def solve():
    """
    リクエストボディの例:
      {
        "board": [
          [0,0,0, ..., 0],  # 9×9の二次元リスト
          ...
        ]
      }

    レスポンス:
      成功時:
        {
          "status": "ok",
          "solution": [
            [1,2,3, ..., 9],
            ...
          ]
        }
      失敗時: (解が無い場合など)
        {
          "status": "fail",
          "message": "No solution found."
        }
    """
    data = request.get_json()
    if not data or "board" not in data:
        return jsonify({"status": "error", "message": "No board data provided."}), 400

    board = data["board"]

    # solve_sudoku は board を直接書き換える実装なので、
    # 先にコピーを作るなど必要なら工夫してください。
    if solve_sudoku(board):
        return jsonify({"status": "ok", "solution": board})
    else:
        return jsonify({"status": "fail", "message": "No solution found."})

import random

def generate_valid_sudoku():
    """
    唯一解を持つ数独問題を生成する
    """
    max_attempts = 50  # 最大50回試す
    attempts = 0

    while attempts < max_attempts:
        board = [[0] * 9 for _ in range(9)]

        # 15～20個のランダムな数字を配置
        for _ in range(20):
            row, col = random.randint(0, 8), random.randint(0, 8)
            num = random.randint(1, 9)
            board[row][col] = num

        temp_board = [row[:] for row in board]  # コピーを作る
        if solve_sudoku(temp_board):  # 解けるならOK
            print("✅ 解ける数独が生成されました")
            return board
        
        attempts += 1  # 試行回数を増やす

    # 解ける問題が見つからなかった場合のフォールバック
    print("⚠️ 解ける問題が見つからなかったので、空の盤面を返します")
    return [[0] * 9 for _ in range(9)]



@app.route("/generate", methods=["GET"])
def generate():
    """
    React から GET /generate を受け取ると、数独問題を生成して返す
    """
    print("新しい数独の問題を生成します...")  # ← デバッグ用
    board = generate_valid_sudoku()
    print("生成された問題:", board)  # ← デバッグ用
    return jsonify({"status": "ok", "board": board})

if __name__ == "__main__":
    app.run(debug=True)
