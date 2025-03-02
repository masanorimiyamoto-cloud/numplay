# app.py

from flask import Flask, request, jsonify

from flask_cors import CORS
from sudoku import Sudoku  # 🔥 高速なライブラリ

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route("/")
def index():
    return "Sudoku Solver API is running!"

from flask import Flask, request, jsonify
import traceback

app = Flask(__name__)

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
    try:
        data = request.get_json()
        if not data or "board" not in data:
            return jsonify({"status": "error", "message": "No board data provided."}), 400

        board = data["board"]

        # 受け取った board の構造をチェック
        print("Received board:", board)
        print("Type of board:", type(board))

        if not isinstance(board, list) or len(board) != 9 or not all(isinstance(row, list) and len(row) == 9 for row in board):
            return jsonify({"status": "fail", "message": "Invalid board format. Must be a 9x9 grid."}), 400

        # Sudoku インスタンスの作成
        sudoku_solver = Sudoku(board)

        # 数独の解決処理を実行
        if sudoku_solver.solve():
            return jsonify({"status": "ok", "solution": sudoku_solver.board})
        else:
            return jsonify({"status": "fail", "message": "No solution found."})

    except Exception as e:
        app.logger.error(f"Exception in /solve: {e}\n{traceback.format_exc()}")
        return jsonify({"status": "error", "message": "Internal server error."}), 500




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
