from flask import Flask, redirect, render_template, request, g, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from models.game import Game
from utils.colors import print_log, colors
import uuid
import sqlite3
import requests
import json
import random

app = Flask(__name__)
socketio = SocketIO(app)
DATABASE = 'database.db'
CATEGORIES = ['General Knowledge', 'Entertainment', 'Science', 'Mythology', 'Sports', 'Geography', 'History', 'Politics', 'Art', 'Celebrities', 'Animals']

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS games (
                            room_id TEXT PRIMARY KEY,
                            questions TEXT NOT NULL,
                            timer INTEGER NOT NULL,
                            active_players INTEGER NOT NULL,
                            state TEXT NOT NULL,
                            current_question INTEGER NOT NULL)''')
    db.commit()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return redirect('/create')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if (request.method == 'POST'):
        # get form data
        num_questions = request.form.get('questions')
        timer = request.form.get('timer')
        categories = request.form.get('categories')
        
        # generate room id
        room_id = str(uuid.uuid4())
        
        # generate questions
        questions = create_questions(num_questions, categories)
        
        # create game object & store in database
        game = Game(room_id, questions, timer)
        game.create_room(get_db())
        
        return redirect(f"/game/{room_id}")
    else:
        return render_template('create.html', categories=CATEGORIES)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/game/<room_id>')
def game(room_id):
    game = get_room(room_id)
    if (game is None):
        return redirect('/error?msg=Room not found')
    return render_template('game.html', game_data=game, shuffle_questions=shuffle_questions)

@app.route('/error')
def error():
    msg = request.args.get('msg')
    return render_template('error.html', msg=msg)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    room_id = request.form.get('room_id')
    curr_question = request.form.get('curr_question')
    answer = request.form.get('answer')
    game = get_room(room_id)
    if (game is not None):
        if (game.check_answer(curr_question, answer)):
            return jsonify({'correct': True})
    return jsonify({'correct': False})

@socketio.on('add_player')
def on_add_player(data):
    room_id = data.get('room_id')
    game = get_room(room_id)
    game.add_player(get_db())
    if (game.active_players >= 2):
        game.start_game(get_db())

def create_questions(num_questions, categories):
    url = f'https://opentdb.com/api.php?amount={num_questions}&type=multiple'
    response = requests.get(url)
    if (response.status_code == 200):
        return response.json().get('results')
    return []

def get_room(room_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM games WHERE room_id = ?', (room_id,))
        data = cursor.fetchone()
        return Game(data[0], json.loads(data[1]), data[2], data[3], data[4], data[5])
    except:
        return None
    
def shuffle_questions(correct_ans, incorrect_ans):
    answers = incorrect_ans + [correct_ans]
    random.shuffle(answers)
    return answers

if __name__ == "__main__":
    app.run(debug=True)
