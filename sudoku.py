from flask import Flask, render_template, request, jsonify
from solver import is_valid
from hint import get_hint
from flask import session
import time


app = Flask(__name__)
app.secret_key = "ynofoood"


from solver import generate_full_board, remove_numbers

def get_new_board(difficulty):
    board = generate_full_board()
    return remove_numbers(board, difficulty)




@app.route("/")
def index():
    difficulty = request.args.get("difficulty", "medium")

    board = get_new_board(difficulty)

    session["hints_used"] = 0
    session["start_time"] = time.time()
    session["difficulty"] = difficulty

    return render_template(
        "index.html",
        board=board,
        difficulty=difficulty
    )



@app.route("/check", methods=["POST"])
def check():
    data = request.json
    board = data["board"]

    for r in range(9):
        for c in range(9):
            num = board[r][c]
            if num != 0:
                board[r][c] = 0
                if not is_valid(board, r, c, num):
                    return jsonify({"valid": False})
                board[r][c] = num

    solved = all(all(cell != 0 for cell in row) for row in board)

    if solved:
        elapsed = int(time.time() - session.get("start_time", time.time()))
        hints = session.get("hints_used", 0)

        score = max(0, 1000 - (elapsed * 2) - (hints * 100))

        return jsonify({
            "valid": True,
            "solved": True,
            "time": elapsed,
            "score": score
        })

    return jsonify({"valid": True, "solved": False})


@app.route("/hint", methods=["POST"])
def hint():
    if "hints_used" not in session:
        session["hints_used"] = 0

    if session["hints_used"] >= 5:
        return jsonify({
            "error": "Hint limit reached",
            "remaining": 0
        }), 403

    data = request.json
    board = data["board"]

    hint = get_hint(board)
    if not hint:
        return jsonify({"hint": None})

    session["hints_used"] += 1

    r, c, num = hint
    return jsonify({
        "hint": [r, c, num],
        "remaining": 5 - session["hints_used"]
    })


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
