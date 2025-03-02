from flask import Flask, request, jsonify
from flask_cors import CORS
from sudoku import Sudoku
import traceback
import os

app = Flask(__name__)

# すべてのエンドポイントで CORS を有効化
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def index():
    return "Sudoku Solver API is running!"

@app.route("/solve", methods=["POST"])
def solve():
    try:
        data = request.get_json()
        if not data or "board" not in data:
            return jsonify({"status": "error", "message": "No board data provided."}), 400

        board = data["board"]

        if not isinstance(board, list) or len(board) != 9 or not all(isinstance(row, list) and len(row) == 9 for row in board):
            return jsonify({"status": "fail", "message": "Invalid board format. Must be a 9x9 grid."}), 400

        from sudoku_solver import solve_sudoku
        import copy
        board_copy = copy.deepcopy(board)

        if solve_sudoku(board_copy):
            return jsonify({"status": "ok", "solution": board_copy})
        else:
            return jsonify({"status": "fail", "message": "No solution found."})

    except Exception as e:
        app.logger.error(f"Exception in /solve: {e}\n{traceback.format_exc()}")
        return jsonify({"status": "error", "message": "Internal server error."}), 500

@app.route("/generate", methods=["GET"])
def generate():
    try:
        puzzle = Sudoku(9)  # `difficulty(0.5)` を削除し、問題を簡単にする
        board = puzzle.board

        # `Access-Control-Allow-Origin` を手動で追加
        response = jsonify({"status": "ok", "board": board})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    
    except Exception as e:
        app.logger.error(f"Exception in /generate: {e}\n{traceback.format_exc()}")
        return jsonify({"status": "error", "message": "Internal server error."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render のポートに対応
    app.run(host="0.0.0.0", port=port)
