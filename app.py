from flask import Flask, redirect, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from models.game import Game
from utils.colors import print_log, colors
import uuid
import threading

app = Flask(__name__)
socketio = SocketIO(app)

games = {}

@app.route('/')
def index():
    return redirect('/create')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if (request.method == 'POST'):
        room_id = str(uuid.uuid4())
        host = request.form.get('username')
        games[room_id] = Game(room_id)
        games[room_id].add_player(host)
        return redirect(f"/game/{room_id}")
    else:
        return render_template('create.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/game/<room_id>')
def game(room_id):
    curr_game = games.get(room_id)
    if (curr_game is None):
        return redirect('/error?msg=Room not found')
    start = request.args.get('start')
    if (start == 'yes'):
        curr_game.update_game_state("active")
        games[room_id] = curr_game
    return render_template('game.html', game_data=curr_game)

@app.route('/error')
def error():
    msg = request.args.get('msg')
    return render_template('error.html', msg=msg)
    
@socketio.on('disconnect')
def on_disconnect():
    # leave all rooms on disconnect
    print_log(colors.fg.red ,"Disconnecting client from all rooms")
    for room_id in rooms():
        leave_room(room_id)
        curr_game = games.get(room_id)
        if (curr_game is None):
            continue
        connections, error = curr_game.update_active_connections(curr_game.active_connections - 1)
        if (connections == 0):
            timer = threading.Timer(60, del_game_room, args=[room_id])
            timer.start()
        if (error):
            return redirect(f"/error?msg={error}")
        emit('update_connections', { 'connections': connections }, to=room_id)

@socketio.on('join')
def on_join(data):
    room_id = data.get('room_id')
    join_room(room_id)
    curr_game = games.get(room_id)
    if (curr_game is None):
        return redirect('/error?msg=Room not found')
    connections, error = curr_game.update_active_connections(curr_game.active_connections + 1)
    if (error):
        return redirect(f"/error?msg={error}")
    emit('update_connections', { 'connections': connections }, to=room_id)
    
@socketio.on('start_game')
def on_start_game(data):
    room_id = data.get('room_id')
    curr_game = games.get(room_id)
    curr_game.update_game_state("active")
    emit('client_start_game', to=room_id)
    
@socketio.on('answer')
def on_answer(answer_choice):
    room_id = answer_choice.get('room_id')
    curr_game = games.get(room_id)
    if (curr_game is None):
        return redirect('/error?msg=Room not found')
    answer = answer_choice.get('answer')
    if (answer == curr_game.questions[curr_game.current_question - 1]['correct']):
        emit('correct_answer', to=room_id)
    else:
        emit('incorrect_answer', to=room_id)

@socketio.on('add_player')
def on_add_player(data):
    room_id = data.get('room_id')
    username = data.get('username')
    curr_game = games.get(room_id)
    if (curr_game is None):
        return redirect('/error?msg=Room not found')
    curr_game.add_player(username)
    emit('update_players', { 'players': curr_game.players }, to=room_id)
    
def del_game_room(id):
    curr_game = games.get(id)
    if curr_game and curr_game.active_connections == 0:
        del games[id]
        print_log(colors.fg.red, f"Deleted game room {id}")

if __name__ == "__main__":
    app.run(debug=True)
