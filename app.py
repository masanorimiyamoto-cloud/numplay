# app.py

from flask import Flask, request, jsonify

from flask_cors import CORS
from sudoku import Sudoku  # 🔥 高速なライブラリ

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
    if Sudoku(board):
        
        return jsonify({"status": "ok", "solution": board})
    else:
        return jsonify({"status": "fail", "message": "No solution found."})

import random


@app.route("/generate", methods=["GET"])
def generate():
    """
    高速なライブラリを使って数独を生成
    """
    puzzle = Sudoku(3).difficulty(0.5)
    board = puzzle.board
    return jsonify({"status": "ok", "board": board})

if __name__ == "__main__":
    app.run(debug=True)
