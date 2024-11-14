import json
import requests
import random

from models.game import Game

class Helper:
    def __init__(self):
        pass
    
    def create_room(self, room_id, num_questions=10, timer=60) -> Game:
        try:
            url = f'https://opentdb.com/api.php?amount={num_questions}&type=multiple&encode=base64'
            response = requests.get(url)
            data = response.json().get('results')
            validatedData = []
            for entry in data:
                all_answers = entry.get('incorrect_answers') + [entry.get('correct_answer')]
                random.shuffle(all_answers)
                new_entry = {
                    "question": entry.get('question'),
                    "correct_answer": entry.get('correct_answer'),
                    "all_answers": all_answers
                }
                validatedData.append(new_entry)
            return Game(room_id, questions=validatedData, timer=timer)
        except Exception as e:
            print(e)
            return None

    def get_room(self, db, room_id) -> Game:
        try:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM games WHERE room_id = ?', (room_id,))
            data = cursor.fetchone()
            return Game(room_id, data[1], data[2], json.loads(data[3]), json.loads(data[4]), data[5])
        except Exception as e:
            print(e)
            return None
        
    def create_db(self, db) -> bool:
        try:
            cursor = db.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS games (
                    room_id TEXT PRIMARY KEY, 
                    curr_state TEXT NOT NULL, 
                    curr_question INTEGER NOT NULL, 
                    players TEXT NOT NULL, 
                    questions TEXT NOT NULL, 
                    timer INTEGER NOT NULL)
                """
            )
            db.commit()
            return True
        except Exception as e:
            print(e)
            return False