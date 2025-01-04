import requests
import random
import time

class Kodak:
    def __init__(self):
        pass

    def get_player(self, gameId, username, db_connection):
        db_cursor = db_connection.cursor()
        try:
            db_cursor.execute("""
                SELECT * FROM players WHERE username = ? AND gameId = ?
            """, (username, gameId))
            player = db_cursor.fetchone()
            if player:
                return dict(player)
        except Exception as e:
            print(e)
            return {}

    def get_game(self, gameId, db_connection):
        db_cursor = db_connection.cursor()
        try:
            db_cursor.execute("""
                SELECT * FROM games WHERE gameId = ?
            """, (gameId,))
            game = db_cursor.fetchone()
            if game:
                return dict(game)
        except Exception as e:
            print(e)
            return {}

    def fetch_questions(self, num_questions, category, difficulty):
        difficulty = difficulty.lower()
        url = f'https://opentdb.com/api.php?amount={num_questions}&category={category}&difficulty={difficulty}&type=multiple&encode=base64'
        response = requests.get(url)
        code = response.json().get('response_code')
        while (code == 5):
            time.sleep(5)
            response = requests.get(url)
            code = response.json().get('response_code')
        print(code)
        if code != 0:
            return [], [], [], code
        data = response.json().get('results')
        questions, answers, correct_answers = [], [], []
        for entry in data:
            all_answers = entry.get('incorrect_answers') + [entry.get('correct_answer')]
            random.shuffle(all_answers)
            questions.append(entry.get('question'))
            answers.append(all_answers)
            correct_answers.append(entry.get('correct_answer'))
        return questions, answers, correct_answers, code
