class Player:
    def __init__(self, game_id:str, username:str, score:int, db_connection) -> None:
        self.game_id = game_id
        self.username = username
        self.score = score
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
                    score INTEGER DEFAULT 0,
                    game_id TEXT NOT NULL,
                    FOREIGN KEY (game_id) REFERENCES games(game_id)
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
                INSERT INTO players (username, score, game_id)
                VALUES (?, ?, ?)
            """, (self.username, self.score, self.game_id))
            self.db_connection.commit()
        except Exception as e:
            print(e)
            raise Exception("Error creating player")
    
    def get_player(self, username, game_id):
        try:
            self.db_cursor.execute("""
                SELECT * FROM players WHERE username = ? AND game_id = ?
            """, (username, game_id))
            player = self.db_cursor.fetchone()
            if player:
                self.username = player[1]
                self.score = player[2]
                self.game_id = player[3]
                return self
            else:
                raise Exception("Player not found")
        except Exception as e:
            print(e)
            raise Exception("Error getting player")
    
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