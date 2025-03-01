# sudoku_solver.py

def solve_sudoku(board):
    """
    9x9 の二次元リスト `board` を与えられると、再帰的なバックトラッキング方式で解答します。
    空マスは 0 で表現し、解答が見つかった場合は board 自体を書き換えて True を返します。
    解けない場合は False を返します。
    """
    empty_spot = find_empty_spot(board)
    if not empty_spot:
        # 空マスがない → 既に完成している
        return True
    
    row, col = empty_spot

    # 1～9 を試す
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num  # 仮置き
            if solve_sudoku(board):
                return True
            board[row][col] = 0    # 戻す

    return False

def find_empty_spot(board):
    """
    board の中から 0（空マス）を探し、その (row, col) を返す。
    もし空マスがなければ None。
    """
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return (r, c)
    return None

def is_valid(board, row, col, num):
    """
    board[row][col] に num を置いても矛盾がないかをチェックする。
    （行・列・3x3ブロックの検証）
    """
    # 行の重複チェック
    if num in board[row]:
        return False

    # 列の重複チェック
    for r in range(9):
        if board[r][col] == num:
            return False

    # 3x3 ブロックの重複チェック
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if board[r][c] == num:
                return False

    return True

def print_board(board):
    """
    board の内容をコンソールに整形して表示する補助関数。
    """
    for r in range(9):
        if r % 3 == 0 and r != 0:
            print("-" * 21)  # 3 行ごとに区切り線
        for c in range(9):
            if c % 3 == 0 and c != 0:
                print("| ", end="")
            val = board[r][c]
            print(val if val != 0 else ".", end=" ")
        print()  # 改行

if __name__ == "__main__":
    # サンプルの 9x9 の数独問題 (0 が空マス)
    puzzle = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    print("【問題】")
    print_board(puzzle)

    if solve_sudoku(puzzle):
        print("\n【解答】")
        print_board(puzzle)
    else:
        print("\n解けませんでした。")
