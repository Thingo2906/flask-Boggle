from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "abcdacbeshjk"

boggle_game = Boggle()

@app.route("/")
def homepage():
    """Show board to start the game"""

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    timeplays = session.get("timeplays", 0)

    return render_template("index.html", board=board,
                           highscore=highscore,
                           timeplays=timeplays)


@app.route("/check-word")
def check_word():
    """Check if word is in dictionary."""

    word = request.args["word"]
    board = session['board']
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update timeplays, update high score"""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    timeplays = session.get("timeplays", 0)

    session['timeplays'] = timeplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(bestRecord=score > highscore)