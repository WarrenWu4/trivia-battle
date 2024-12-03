from flask import Flask, redirect, render_template, request, g, jsonify
from flask_socketio import SocketIO
from models.game import Game
import uuid
import sqlite3
import random
import requests

app = Flask(__name__)
socketio = SocketIO(app)
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    if exception:
        print(exception)
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if (request.method == 'POST'):
        num_questions = request.form.get('questions')
        game_id = str(uuid.uuid4())
        trivia_data = {"questions": [], "answers": [], "correct_answers": []}
        try:
            url = f'https://opentdb.com/api.php?amount={num_questions}&type=multiple&encode=base64'
            response = requests.get(url)
            data = response.json().get('results')
            for entry in data:
                all_answers = entry.get('incorrect_answers') + [entry.get('correct_answer')]
                random.shuffle(all_answers)
                trivia_data["questions"].append(entry.get('question'))
                trivia_data["answers"].append(all_answers)
                trivia_data["correct_answers"].append(entry.get('correct_answer'))
            Game(game_id, trivia_data.get('questions'), trivia_data.get('answers'), trivia_data.get('correct_answers'), 0, get_db()).create_game()
        except Exception as e:
            print(e)
            return redirect('/error?msg=Error creating game')
        return redirect(f"/game/{game_id}")
    return render_template('create.html')

@app.route('/game/<game_id>')
def room(game_id):
    game:Game = Game(game_id, [], [], [], 0, get_db()).get_game()
    if (game.curr_question >= len(game.questions)):
        return redirect(f'/game/{game_id}/results')
    return render_template('game.html', game_id=game_id)

@app.route('/game/<game_id>/get_question', methods=['POST'])
def get_question(game_id):
    game:Game = Game(game_id, [], [], [], 0, get_db()).get_game()
    return jsonify({"question": game.questions[game.curr_question], "answers": game.answers[game.curr_question], "curr_question": game.curr_question}), 200

@app.route('/game/<game_id>/check', methods=['POST'])
def check_answer(game_id):
    game:Game = Game(game_id, [], [], [], 0, get_db()).get_game()
    answer = request.json.get('answer')
    if game.check_answer(answer):
        return jsonify({"correct": True}), 200
    else:
        return jsonify({"correct": False}), 200
    
@app.route('/game/<game_id>/next', methods=['POST'])
def next_question(game_id):
    game:Game = Game(game_id, [], [], [], 0, get_db()).get_game()
    game.next_question()
    if (game.curr_question >= len(game.questions)):
        return jsonify({"ok": True, "game_over": True}), 200
    return jsonify({"ok": True, "game_over": False}), 200

@app.route('/game/<game_id>/results')
def results(game_id):
    return render_template('game_over.html')

@app.route('/error')
def error():
    msg = request.args.get('msg')
    return render_template('error.html', msg=msg)

if __name__ == "__main__":
    app.run(debug=True)
