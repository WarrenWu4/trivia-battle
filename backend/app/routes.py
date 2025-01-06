from app import app, db
from app.models import Player, Game
from flask import jsonify, request
from app.lib import get_trivia_data
import sqlalchemy as sa
import json

# *------------GAME RELATED ROUTES------------*
@app.route('/game/<game_id>', methods=['GET'])
def get_game(game_id):
    if not game_id:
        return jsonify({'error': 'No data provided'}), 400
    game = db.session.scalar(sa.select(Game).where(Game.id == game_id))
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    return jsonify(game.config_dict()), 200

@app.route('/game/create', methods=['POST'])
def create_game():
    if not request.json:
        return jsonify({'success': False, 'msg': 'No data provided'}), 400
    game_id = request.json.get('game_id')
    gamemode = request.json.get('gamemode')
    player_num = request.json.get('player_num')
    question_num = request.json.get('question_num')
    question_timer = request.json.get('question_timer')
    category = request.json.get('category')
    difficulty = request.json.get('difficulty')
    if not game_id or not gamemode or not player_num or not question_num or not question_timer or not category or not difficulty:
        return jsonify({'success': False, 'msg': 'Missing required data'}), 400
    questions, answers, correct_answers = get_trivia_data(question_num, category, difficulty)
    if not questions or not answers or not correct_answers:
        return jsonify({'success': False, 'msg': 'Failed to get trivia data'}), 500
    questions = json.dumps(questions)
    answers = json.dumps(answers)
    correct_answers = json.dumps(correct_answers)
    game = Game(id=game_id, gamemode=gamemode, player_num=player_num, question_num=question_num, question_timer=question_timer, category=category, difficulty=difficulty, questions=questions, answers=answers, correct_answers=correct_answers)
    db.session.add(game)
    db.session.commit()
    return jsonify({'success': True, 'msg': 'Game created'}), 201

@app.route('/game/<game_id>/question/<question_num>', methods=['GET'])
def get_question(game_id, question_num):
    if not game_id or not question_num:
        return jsonify({'success': False, 'msg': 'No data provided'}), 400
    game = db.session.scalar(sa.select(Game).where(Game.id == game_id))
    question_num = int(question_num)
    if not game:
        return jsonify({'success': False, 'msg': 'Game not found'}), 404
    if question_num > game.question_num:
        return jsonify({'success': False, 'msg': 'Question number exceeds number of questsions'}), 404
    game_data = game.data_dict() 
    data = {
        'question': json.loads(game_data.get('questions'))[question_num],
        'answers': json.loads(game_data.get('answers'))[question_num],
    }
    return jsonify({'success': True, 'trivia': data}), 200

@app.route('/game/<game_id>/question/<question_num>/check', methods=['POST'])
def check_answer(game_id, question_num):
    if not game_id or not question_num or not request.json:
        return jsonify({'success': False, 'msg': 'No data provided'}), 400
    if not request.json.get('answer'):
        return jsonify({'success': False, 'msg': 'Missing required data'}), 400
    question_num = int(question_num)
    user_answer = request.json.get('answer')
    game = db.session.scalar(sa.select(Game).where(Game.id == game_id))
    if not game:
        return jsonify({'success': False, 'msg': 'Game not found'}), 404
    if question_num > game.question_num:
        return jsonify({'success': False, 'msg': 'Question number exceeds number of questsions'}), 404
    game_data = game.data_dict()
    correct_answers = json.loads(game_data.get('correct_answers'))
    if correct_answers[question_num] == user_answer:
        return jsonify({'success': True, 'correct': True}), 200
    return jsonify({'success': True, 'correct': False}), 200
# *------------GAME RELATED ROUTES------------*

# *------------PLAYER RELATED ROUTES------------*
@app.route('/players/<game_id>', methods=['GET'])
def get_players(game_id):
    if not game_id:
        return jsonify({'success': False, 'msg': 'No data provided'}), 400
    all_players = db.session.scalars(sa.select(Player).where(Player.game_id == game_id)).all()
    if not all_players:
        return jsonify({'success': False, 'msg': 'No players found'}), 404
    players = [player.to_dict() for player in all_players]
    return jsonify({'success': True, 'players': players}), 200

@app.route('/player/<game_id>/<username>', methods=['GET'])
def get_player(game_id, username):
    if not username or not game_id:
        return jsonify({'success': False, 'msg': 'No data provided'}), 400
    player = db.session.scalar(sa.select(Player).where(Player.username == username and Player.game_id == game_id))
    if not player:
        return jsonify({'success': False, 'msg': 'Player not found'}), 404
    return jsonify({'success': True, 'player': player.to_dict()}), 200

@app.route('/player/<game_id>/<username>', methods=['POST'])
def update_player(game_id, username):
    if not game_id and not username and not request.json:
        return jsonify({'error': 'No data provided'}), 400
    if not request.json.get('score') and not request.json.get('correct') and not request.json.get('current_question'):
        return jsonify({'error': 'Missing required data'}), 400
    player = db.session.scalar(sa.select(Player).where(Player.username == username and Player.game_id == game_id))
    if not player:
        return jsonify({'error': 'Player not found'}), 404
    player.score = request.json.get('score')
    player.correct = request.json.get('correct')
    player.current_question = request.json.get('current_question')
    db.session.commit()
    return jsonify({'message': 'Player updated'}), 200
    
@app.route('/player/create', methods=['POST'])
def create_player():
    if not request.json:
        return jsonify({'success': False, 'msg': 'No data provided'}), 400
    username = request.json.get('username')
    game_id = request.json.get('game_id')
    if not username or not game_id:
        return jsonify({'success': False, 'msg': 'Missing required data'}), 400
    player = Player(username=username, game_id=game_id)
    db.session.add(player)
    db.session.commit()
    return jsonify({'success': True, 'msg': 'Player created'}), 201
# *------------PLAYER RELATED ROUTES------------*