class Player:
    def __init__(self, gameId:str, username:str, currentQuestion:int, score:int, correct:int, db_connection) -> None:
        self.gameId = gameId
        self.username = username
        self.currentQuestion = currentQuestion
        self.score = score
        self.correct = correct

        self.db_connection = db_connection
        self.db_cursor = self.db_connection.cursor()
        self.init_player_table()
        
    def init_player_table(self) -> None:
        try:
            self.db_connection.execute("PRAGMA foreign_keys = ON;")
            self.db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    uuid INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    currentQuestion INTEGER DEFAULT 0,
                    score INTEGER DEFAULT 0,
                    correct INTEGER DEFAULT 0,
                    gameId TEXT NOT NULL,
                    FOREIGN KEY (gameId) REFERENCES games(gameId)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE
                );
            """)
        except Exception as e:
            print(e)
            raise Exception("Error initializing player table")
    
    def create_player(self) -> None:
        try:
            self.db_cursor.execute("""
                INSERT INTO players (username, currentQuestion, score, correct, gameId)
                VALUES (?, ?, ?, ?, ?)
            """, (self.username, self.currentQuestion, self.score, self.correct, self.gameId))
            self.db_connection.commit()
        except Exception as e:
            print(e)
            raise Exception("Error creating player")
    
    
    def update_score(self, correct:bool) -> None:
        try:
            self.score = self.score+10 if correct else max(0, self.score-10)
            self.db_cursor.execute("""
                UPDATE players SET score = ? WHERE username =
                    (SELECT username FROM players WHERE game_id = ? LIMIT 1)
            """, (self.score, self.game_id))
            self.db_connection.commit()
        except Exception as e:
            print(e)
            raise Exception("Error updating score")
