from typing import List
from models.player import Player
import json

class Game:
    def __init__(self, game_id:str, questions:List[str], answers:List[str], correct_answers:List[str], curr_question:int, timer:int, ready:bool, db_connection):
        self.game_id = game_id
        self.questions = questions
        self.answers = answers
        self.correct_answers = correct_answers
        self.curr_question = curr_question
        self.timer = timer
        self.ready = ready
        self.db_connection = db_connection
        self.db_cursor = self.db_connection.cursor()
        self.init_game_table()
    
    def init_game_table(self):
        try:
            self.db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS games (
                    game_id TEXT PRIMARY KEY,
                    questions TEXT,
                    answers TEXT,
                    correct_answers TEXT,
                    curr_question INTEGER DEFAULT 0,
                    timer INTEGER DEFAULT 60,
                    ready BOOLEAN DEFAULT 0
                );
            """)
        except Exception as e:
            print(e)
            raise Exception("Error initializing game table")
    
    def create_game(self):
        try:
            self.db_cursor.execute("""
                INSERT INTO games (game_id, questions, answers, correct_answers, curr_question, timer, ready)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (self.game_id, json.dumps(self.questions), json.dumps(self.answers), json.dumps(self.correct_answers), self.curr_question, self.timer, self.ready))
            self.db_connection.commit()
        except Exception as e:
            print(e)
            raise Exception("Error generating game")
    
    def get_game(self):
        try:
            self.db_cursor.execute("""
                SELECT * FROM games WHERE game_id = ?
            """, (self.game_id,))
            game = self.db_cursor.fetchone()
            if game:
                self.questions = json.loads(game[1])
                self.answers = json.loads(game[2])
                self.correct_answers = json.loads(game[3])
                self.curr_question = game[4]
                self.timer = game[5]
                self.ready = game[6]
            return self
        except Exception as e:
            print(e)
            raise Exception("Error getting game")
    
    def get_players(self):
        try:
            players_arr = []
            self.db_cursor.execute("""
                SELECT * FROM players WHERE game_id = ?
            """, (self.game_id, ))
            players = self.db_cursor.fetchall()
            for player in players:
                players_arr.append((player[1], player[2]))
            return players_arr
        except Exception as e:
            print(e)
            raise Exception("Error getting players")
    
    def add_player(self, username):
        try:
            player = Player(self.game_id, username, 0, self.db_connection)
            player.create_player()
        except Exception as e:
            print(e)
            raise Exception("Error adding player")
        
    def check_answer(self, answer:str) -> bool:
        """
        compare base64 encoded answer to the correct answer in case there are special characters
        """
        return self.correct_answers[self.curr_question] == answer
    
    def next_question(self):
        try:
            self.curr_question += 1
            self.db_cursor.execute("""
                UPDATE games SET curr_question = ? WHERE game_id = ?
            """, (self.curr_question, self.game_id))
            self.db_connection.commit()
        except Exception as e:
            print(e)
            raise Exception("Error getting next question")
    
    def start_game(self):
        self.ready = True
        try:
            self.db_cursor.execute("""
                UPDATE games SET ready = ? WHERE game_id = ?
            """, (self.ready, self.game_id))
            self.db_connection.commit()
        except Exception as e:
            print(e)
            raise Exception("Error starting game")