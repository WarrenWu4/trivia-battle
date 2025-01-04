import json

class Game:
    def __init__(self, gameId:str, gameMode, playerNum, questionNum, questionTimer, category, difficulty, questions, answers, correctAnswers, db_connection):
        self.gameId = gameId

        # config
        self.gameMode = gameMode
        self.playerNum = playerNum
        self.questionNum = questionNum
        self.questionTimer = questionTimer
        self.category = category
        self.difficulty = difficulty

        # data
        self.questions = questions
        self.answers = answers
        self.correctAnswers = correctAnswers 

        # db
        self.db_connection = db_connection
        self.db_cursor = self.db_connection.cursor()
        self.init_game_table()
    
    def init_game_table(self):
        try:
            self.db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS games (
                    gameId TEXT PRIMARY KEY,
                    gameMode TEXT,
                    playerNum INTEGER,
                    questionNum INTEGER,
                    questionTimer INTEGER,
                    category TEXT,
                    difficulty TEXT,
                    questions TEXT,
                    answers TEXT,
                    correctAnswers TEXT
                );
            """)
        except Exception as e:
            print(e)
            raise Exception("Error initializing game table")
    
    def create_game(self):
        try:
            self.db_cursor.execute("""
                INSERT INTO games (gameId, gameMode, playerNum, questionNum, questionTimer, category, difficulty, questions, answers, correctAnswers)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.gameId, self.gameMode, self.playerNum, self.questionNum, self.questionTimer, self.category, self.difficulty, json.dumps(self.questions), json.dumps(self.answers), json.dumps(self.correctAnswers)))
            self.db_connection.commit()
        except Exception as e:
            print(e)
            raise Exception("Error generating game")
    
    
    def get_players(self):
        try:
            players_arr = []
            self.db_cursor.execute("""
                SELECT * FROM players WHERE game_id = ?
            """, (self.gameId, ))
            players = self.db_cursor.fetchall()
            for player in players:
                players_arr.append((player[1], player[2]))
            return players_arr
        except Exception as e:
            print(e)
            raise Exception("Error getting players")
    
    def check_answer(self, answer:str, currentQuestion:int) -> bool:
        """
        compare base64 encoded answer to the correct answer in case there are special characters
        """
        return self.correctAnswers[currentQuestion] == answer
