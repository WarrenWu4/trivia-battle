from flask import Flask, redirect, render_template, request, g, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from models.game import Game
from models.player import Player
from models.kodak import Kodak
import sqlite3

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5173", "http://localhost:5173"])
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

@app.route('/api/create', methods=['POST'])
def index():
    if not request.json:
        return jsonify({"success": False}), 500

    gameId = request.json.get("gameId")
    username = request.json.get("username")
    gameMode = request.json.get("gameMode")
    playerNum = request.json.get("playerNum")
    questionNum = request.json.get("questionNum")
    questionTimer = request.json.get("questionTimer")
    category = request.json.get("category")
    difficulty = request.json.get("difficulty")

    q, a, ca, code = Kodak().fetch_questions(questionNum, category, difficulty)
    if (code != 0):
        return jsonify({"success": False}), 500
    Game(gameId, gameMode, playerNum, questionNum, questionTimer, category, difficulty, q, a, ca, get_db()).create_game()
    Player(gameId, username, 0, 0, 0, get_db()).create_player()
    return jsonify({"success": True}), 200

@app.route('/api/game', methods=['POST'])
def game():
    if not request.json:
        return jsonify({"success": False}), 500
    gameId = request.json.get("gameId")
    gameData = Kodak().get_game(gameId, get_db())
    if gameData:
        gameData["success"] = True
        return jsonify(gameData), 200
    return jsonify({"success": False}), 404

@app.route('/api/player', methods=['POST'])
def player():
    if not request.json:
        return jsonify({"success": False}), 500
    gameId = request.json.get("gameId")
    username = request.json.get("username")
    playerData = Kodak().get_player(gameId, username, get_db())
    if playerData:
        if len(playerData.keys()) > 0:
            playerData["success"] = True
            return jsonify(playerData), 200
        return jsonify({"success": False}), 404
    return jsonify({"success": False}), 500

if __name__ == "__main__":
    app.run(debug=True)
