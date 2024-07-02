from flask import Flask, redirect, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
socketio = SocketIO(app)

connections = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if (request.method == 'POST'):
        questions = request.form.get('questions')
        timer = request.form.get('timer')
        categories = request.form.get('categories')
        print(f'creating game with {questions} questions and {timer} timer and {categories} categories')
        return redirect('/game/123')
    else:
        return render_template('create.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/game/<game_id>')
def game(game_id):
    game_started = False
    return render_template('game.html', game_started=game_started, game_id=game_id)

@socketio.on('connect')
def on_connect():
    print('client connected')
    
@socketio.on('disconnect')
def on_disconnect():
    leave_room()
    print('client disconnected')
    
@socketio.on('join')
def on_join(data):
    room_id = data.get('room_id')
    join_room(room_id)
    if room_id not in connections:
        connections[room_id] = 0
    connections[room_id] += 1
    emit('update_connections', { 'connections': connections[room_id] }, to=room_id)

if __name__ == "__main__":
    app.run(debug=True)
    # app.run()
