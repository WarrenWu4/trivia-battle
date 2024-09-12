import json

class Game:
    def __init__(self, room_id, questions, timer, active_players=0, state='waiting', current_question=1):
        self.room_id = room_id
        self.questions = questions
        self.timer = timer
        self.active_players = active_players
        self.state = state
        self.current_question = current_question
        
    def create_room(self, db):
        try:
            cursor = db.cursor()
            cursor.execute('''INSERT INTO games (room_id, questions, timer, active_players, state, current_question) VALUES (?, ?, ?, ?, ?, ?)''', (self.room_id, json.dumps(self.questions), self.timer, self.active_players, self.state, self.current_question))
            db.commit()
            return True
        except Exception as e:
            print(e)
            return False
    
    def add_player(self, db):
        try:
            self.active_players += 1
            cursor = db.cursor()
            cursor.execute('''UPDATE games SET active_players = ? WHERE room_id = ?''', (self.active_players, self.room_id))
            db.commit()
            return True
        except Exception as e:
            print(e)
            return False
    
    def start_game(self, db):
        try:
            self.state = "active"
            cursor = db.cursor()
            cursor.execute('''UPDATE games SET state = ? WHERE room_id = ?''', (self.state, self.room_id))
            db.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
    def check_answer(self, curr_question, answer):
        self.current_question += 1
        if (self.questions[curr_question-1].get('correct_answer') == answer):
            return True
        return False