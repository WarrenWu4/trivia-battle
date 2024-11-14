import json

class Game:
    def __init__(self, room_id, curr_state="waiting", curr_question=0, players=[], questions=[], timer=60):
        self.room_id = room_id
        self.curr_state = curr_state
        self.curr_question = curr_question
        self.players = players
        self.questions = questions
        self.timer = timer

    def create_room(self, db):
        try:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO games (room_id, curr_state, curr_question, players, questions, timer) VALUES (?, ?, ?, ?, ?, ?)", (self.room_id, self.curr_state, self.curr_question, json.dumps(self.players), json.dumps(self.questions), self.timer)
            )
            db.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
    def update_state(self, db):
        try:
            cursor = db.cursor()
            cursor.execute(
                "UPDATE games SET curr_state = ? WHERE room_id = ?", (self.curr_state, self.room_id)
            )
            db.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
    def update_player(self, db):
        try:
            cursor = db.cursor()
            cursor.execute(
                "UPDATE games SET players = ? WHERE room_id = ?", (json.dumps(self.players), self.room_id)
            )
            db.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
    def next_question(self, db):
        try:
            self.curr_question += 1
            cursor = db.cursor()
            cursor.execute(
                "UPDATE games SET curr_question = ? WHERE room_id = ?", (self.curr_question, self.room_id)
            )
            db.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
    def check_answer(self, answer):
        if (self.questions[self.curr_question]['correct_answer'] == answer):
            return True
        return False
