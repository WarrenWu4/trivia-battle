from flask import Flask, redirect, render_template, request, g, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from models import game, helper
import uuid
import sqlite3
import json
import base64
import qrcode
import io

app = Flask(__name__)
socketio = SocketIO(app)
DATABASE = 'database.db'
HELPER = helper.Helper()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    HELPER.create_db(db)
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
        room_id = str(uuid.uuid4())
        game = HELPER.create_room(room_id, num_questions=num_questions)
        if (game == None):
            return redirect('/error?msg=Error creating room')
        game.create_room(get_db())
        return redirect(f"/game/{room_id}")
    
    return render_template('create.html')

@app.route('/game/<room_id>')
def game(room_id):
    # check if game already exists
    game = HELPER.get_room(get_db(), room_id)
    
    if (game == None):
        return redirect('/error?msg=Game does not exist')
    
    return render_template('game.html', room_id=room_id, state=game.curr_state)

@app.route('/waiting_room/<room_id>')
def waiting_room():
    print(request.path)
    qr = qrcode.make(request.url_root + request.path)
    img_io = io.BytesIO()
    qr.save(img_io, 'PNG')
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.getvalue()).decode()
    return render_template('waiting_room.html', qrcode=img_base64)

"""
@app.route('/create', methods=['GET', 'POST'])
def create():
    if (request.method == 'POST'):
        # get form data
        num_questions = request.form.get('questions')
        # timer = request.form.get('timer')
        # categories = request.form.get('categories')
        
        # generate room id
        room_id = str(uuid.uuid4())
        
        # generate questions
        data = trivia_data(num_questions).get_trivia_data()
        
        # create game object & store in database
        game = Game(room_id, data)
        res = game.create_room(get_db())
        if (not res):
            return redirect('/error?msg=Error creating room')
        
        return redirect(f"/game/{room_id}")
    else:
        return render_template('create.html', categories=CATEGORIES)

@app.route('/game/<room_id>')
def game(room_id):
    game = get_room(room_id)
    if (game is None):
        return redirect('/error?msg=Room not found')
    return render_template('game.html', initial_state=game.state)

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
        # if (game.check_answer(curr_question, answer)):
        return jsonify({'correct': True})
    return jsonify({'correct': False})

@app.route('/get_content', methods=['POST'])
def get_content():
    state = request.form.get('state')
    if (state == 'initial'):
        return render_template('waiting_room.html')
    else:
        return render_template('question.html', question="testing")
    
@socketio.on('connect_player')
def on_connect_player(data):
    room_id = data.get('room_id')
    join_room(room_id)
    print_log(colors.fg.green, f"Player joined room {room_id}")
    emit('update_message', {'message': 'shit :)'}, room=room_id)
    
@socketio.on('start_game')
def on_start_game(data):
    room_id = data.get('room_id')
    print_log(colors.fg.blue, f"Game ${room_id} starting")
    emit('start_game', {'html': render_question(room_id, 0)}, room=room_id)

@socketio.on('new_question')
def on_new_question(data):
    room_id = data.get('room_id')
    question_idx = data.get('question_idx')
    print_log(colors.fg.cyan, "Generating new question")
    emit('new_question', {'html': render_question(room_id, question_idx)}, room=room_id)

@socketio.on('leave_game')
def on_leave_game(data):
    room_id = data.get('room_id')
    leave_room(room_id)
    print_log(colors.fg.red, f"Player left room {room_id}")
    emit('update_message', {'message': 'goodbye :)'}, room=room_id)

def render_question(room_id, question_idx):
    game = get_room(room_id)
    question = base64.b64decode(game.data[question_idx].get('question'))
    return render_template('question.html', question=question)

def get_room(room_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM games WHERE room_id = ?', (room_id,))
        data = cursor.fetchone()
        return Game(data[0], json.loads(data[1]), data[2])
    except:
        return None
"""

if __name__ == "__main__":
    app.run(debug=True)
