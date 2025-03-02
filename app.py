from flask import Flask, request, jsonify
from flask_cors import CORS
from sudoku import Sudoku  # 🔥 高速なライブラリ
import traceback

app = Flask(__name__)

# CORS の設定: すべてのドメインからのアクセスを許可
CORS(app, resources={r"/*": {"origins": "https://sudoku-frontend-tan.vercel.app"}})

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
        print("Received board:", board)

        if not isinstance(board, list) or len(board) != 9 or not all(isinstance(row, list) and len(row) == 9 for row in board):
            return jsonify({"status": "fail", "message": "Invalid board format. Must be a 9x9 grid."}), 400

        # 数独の解決
        from sudoku_solver import solve_sudoku  # sudoku_solver.py をインポート
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
        # 9×9の数独を生成
        puzzle = Sudoku(9).difficulty(0.5)  
        board = puzzle.board
        
        return jsonify({"status": "ok", "board": board})
    
    except Exception as e:
        app.logger.error(f"Exception in /generate: {e}\n{traceback.format_exc()}")
        return jsonify({"status": "error", "message": "Internal server error."}), 500

if __name__ == "__main__":
    app.run(debug=True)
