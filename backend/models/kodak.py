from models.game import Game
from models.player import Player
import requests
import random

class Kodak:
    def __init__(self):
        pass

    def fetch_questions(self, num_questions, category, difficulty, timer, trivia_data, game_id, username, ready, db):
        url = f'https://opentdb.com/api.php?amount={num_questions}&category={category}&difficulty={difficulty}&type=multiple&encode=base64'
        response = requests.get(url)
        code = response.json().get('response_code')
        if code != 0:
            return code
        data = response.json().get('results')
        for entry in data:
            all_answers = entry.get('incorrect_answers') + [entry.get('correct_answer')]
            random.shuffle(all_answers)
            trivia_data["questions"].append(entry.get('question'))
            trivia_data["answers"].append(all_answers)
            trivia_data["correct_answers"].append(entry.get('correct_answer'))
        Game(game_id, trivia_data.get('questions'), trivia_data.get('answers'), trivia_data.get('correct_answers'), 0, timer, ready, db).create_game()
        Player(game_id, username, 0, db).create_player()
        return code